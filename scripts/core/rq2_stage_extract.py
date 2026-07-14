#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ2 stage-metric extractor: a run's page_store JSON -> UNMR / contradiction / PAR.

Deterministic, OFFLINE, no paid LLM. Uses a local NLI model
(default MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli, ~490MB, runs on M1/MPS) as a
THREE-WAY classifier of each consolidated memory against its page's raw content:
  entailment    -> supported
  neutral       -> unsupported (fabricated / over-generalized, no source)
  contradiction -> conflicts with the source == the hard "false memory" signal
This mirrors HaluMem's official memory_accuracy rubric (support / conflict, with
special attention to negation/quantity/time; eval_tools.py:85-97) but is
deterministic instead of a same-family LLM judge. No self-invented "drift" metric:
- matrix-of-drift that FLIPS meaning is caught by `contradiction`;
- pure weakening (dropped qualifier, still entailed) is a known blind spot that
  neither NLI nor the official judge reliably tags -> approximated by HaluMem
  accuracy==1 rate (wired in Phase 1) and left as a manual-spot-check lexical hint
  below, NOT a main metric.

Each run = ONE consolidation depth N; by-N series is built by running per-N-run and
aggregating across runs upstream (Phase 1). No per-pass upstream change needed.
Output feeds scripts/core/rq2_stage_metrics.py (unmr/par + Clopper-Pearson CIs).
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NLI = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"

# Auxiliary-only lexical hint for pure-weakening drift (boundary/exception/negation
# whose loss can flip meaning). NOT a main metric -- manual spot-check hint only.
HIGH_RISK = [
    "but", "unless", "except", "only", "however", "although", "not always", "no longer",
    "但", "除非", "例外", "仅", "只", "并非", "不再", "除了",
]


# --- local NLI (three-way) --------------------------------------------------

def load_nli(model_name: str = DEFAULT_NLI, device: str | None = None):
    """Return (predict, meta). predict(premises, hyps) -> (labels, entail_probs)."""
    import torch
    import torch.nn.functional as F
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    if device is None:
        device = "mps" if torch.backends.mps.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModelForSequenceClassification.from_pretrained(model_name).to(device).eval()
    id2label = {int(k): str(v).lower() for k, v in mdl.config.id2label.items()}
    entail_idx = mdl.config.label2id.get("entailment", 0)

    def predict(premises: list[str], hyps: list[str], batch_size: int = 16):
        labels: list[str] = []
        eprobs: list[float] = []
        for i in range(0, len(premises), batch_size):
            bp, bh = premises[i:i + batch_size], hyps[i:i + batch_size]
            x = tok(bp, bh, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
            with torch.no_grad():
                probs = F.softmax(mdl(**x).logits, dim=-1)
            for row in probs:
                labels.append(id2label[int(row.argmax())])
                eprobs.append(float(row[entail_idx]))
        return labels, eprobs

    return predict, {"model": model_name, "device": device, "labels": id2label}


# --- page_store parsing -----------------------------------------------------

def iter_pages(ps: dict[str, Any]) -> Iterable[dict[str, Any]]:
    """Yield every page in a page_store JSON (completed_pages dict|list + current_page)."""
    comp = ps.get("completed_pages")
    if isinstance(comp, dict):
        for pages in comp.values():
            yield from (pages or [])
    elif isinstance(comp, list):
        yield from comp
    cur = ps.get("current_page")
    if isinstance(cur, dict) and cur.get("page_id"):
        yield cur


def _drift_lost(content: str, summary: str | None) -> list[str]:
    """AUX ONLY: boundary/exception qualifiers in raw content but lost in the summary."""
    if not summary:
        return []
    c, s = content.lower(), summary.lower()
    lost: list[str] = []
    for w in HIGH_RISK:
        if w.isascii():  # word-boundary so 'only' != 'commonly'
            pat = r"\b" + re.escape(w) + r"\b"
            if re.search(pat, c) and not re.search(pat, s):
                lost.append(w)
        elif w in c and w not in s:
            lost.append(w)
    return lost


# --- extraction -------------------------------------------------------------

def extract_run(page_store: dict[str, Any], predict: Callable) -> dict[str, Any]:
    """Return per-run stage records + page->support map for PAR.

    new_memory record: {is_new, has_source_support, nli_label, entail_prob, page_id}
      has_source_support := nli_label == 'entailment'
    drift record (AUX): {page_id, drifted, lost}
    """
    premises: list[str] = []
    hyps: list[str] = []
    meta: list[str] = []  # page_id per (content, memory) pair
    drift: list[dict[str, Any]] = []

    for page in iter_pages(page_store):
        content = str(page.get("content") or "")
        summary = page.get("summary")
        pid = str(page.get("page_id") or "")
        for mem in (page.get("memories") or []):
            mem = str(mem or "")
            if mem and content:
                premises.append(content)
                hyps.append(mem)
                meta.append(pid)
        if summary is not None:
            lost = _drift_lost(content, str(summary))
            drift.append({"page_id": pid, "drifted": bool(lost), "lost": lost})

    labels, eprobs = predict(premises, hyps) if premises else ([], [])
    new_memory: list[dict[str, Any]] = []
    unsupported_pages: set[str] = set()
    for pid, label, ep in zip(meta, labels, eprobs):
        supported = (label == "entailment")
        new_memory.append({"is_new": True, "has_source_support": bool(supported),
                           "nli_label": label, "entail_prob": round(float(ep), 3), "page_id": pid})
        if not supported:
            unsupported_pages.add(pid)
    return {"new_memory": new_memory, "drift": drift, "_unsupported_pages": unsupported_pages}


def extract_par(qa_path: Path, unsupported_pages: set[str]) -> list[dict[str, Any]]:
    """answer record: {used_unsupported_memory} -- did the answer cite an unsupported page."""
    answers: list[dict[str, Any]] = []
    if not qa_path.exists():
        return answers
    with qa_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            hits = ((d.get("mechanism_trace") or {}).get("hits_summary") or [])
            used = any(str(h.get("page_id")) in unsupported_pages for h in hits)
            answers.append({"used_unsupported_memory": bool(used), "query_id": d.get("query_id")})
    return answers


def _find_page_stores(path: Path) -> list[Path]:
    return [path] if path.is_file() else sorted(path.rglob("*.json"))


def main() -> int:
    ap = argparse.ArgumentParser(description="RQ2 stage-metric extractor (offline, local NLI three-way).")
    ap.add_argument("--page-store", required=True, help="page_store JSON file or dir of one N-run.")
    ap.add_argument("--qa-jsonl", default=None, help="run's *_qa.jsonl (for PAR); optional.")
    ap.add_argument("--nli-model", default=DEFAULT_NLI)
    ap.add_argument("--device", default=None, help="mps|cpu (auto if unset).")
    ap.add_argument("--out", default=None, help="records json out.")
    ap.add_argument("--no-nli", action="store_true", help="skip NLI (parse smoke; all labelled neutral).")
    args = ap.parse_args()

    ps_files = _find_page_stores(Path(args.page_store).expanduser())
    if not ps_files:
        raise SystemExit(f"no page_store JSON under {args.page_store}")

    if args.no_nli:
        predict = lambda p, h: (["neutral"] * len(p), [0.0] * len(p))  # noqa: E731
    else:
        predict = load_nli(args.nli_model, args.device)[0]

    all_new: list[dict[str, Any]] = []
    all_drift: list[dict[str, Any]] = []
    unsupported_pages: set[str] = set()
    for f in ps_files:
        r = extract_run(json.loads(f.read_text(encoding="utf-8")), predict)
        all_new.extend(r["new_memory"])
        all_drift.extend(r["drift"])
        unsupported_pages |= r["_unsupported_pages"]

    answers = extract_par(Path(args.qa_jsonl).expanduser(), unsupported_pages) if args.qa_jsonl else []

    import sys
    sys.path.insert(0, str(ROOT / "scripts" / "core"))
    from rq2_stage_metrics import unmr, par  # noqa

    n = len(all_new)
    bd = Counter(r["nli_label"] for r in all_new)
    contra = bd.get("contradiction", 0)
    n_drift = sum(1 for d in all_drift if d["drifted"])
    summary = {
        "page_stores": len(ps_files),
        "n_memories": n,
        # main metrics (all NLI-based, aligned with PDF UNMR + HaluMem conflict + NLI lit)
        "unmr": unmr(all_new),  # unsupported = neutral+contradiction rate (Clopper-Pearson CI)
        "nli_breakdown": {k: {"count": bd.get(k, 0), "rate": round(bd.get(k, 0) / n, 4) if n else None}
                          for k in ("entailment", "neutral", "contradiction")},
        "contradiction_rate": {"num": contra, "den": n, "point": round(contra / n, 4) if n else None},
        "par": par(answers) if answers else {"point": None, "num": 0, "den": 0},
        # auxiliary, NOT a main metric
        "drift_aux_lexical": {"num": n_drift, "den": len(all_drift),
                              "point": round(n_drift / len(all_drift), 4) if all_drift else None,
                              "note": "lexical polarity HINT for manual spot-check only; NOT a main metric"},
        "nli": args.nli_model if not args.no_nli else "SKIPPED",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.out:
        Path(args.out).expanduser().write_text(json.dumps(
            {"summary": summary, "new_memory": all_new, "drift": all_drift, "answers": answers},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print("saved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
