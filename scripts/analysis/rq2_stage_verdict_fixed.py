#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ2 stage verdict — F1 FIX (optimized): quantify the N=0 truncation artifact.

Three views on summary_only (N={0,1,2,4,8}):
  (A) ORIG-trunc, all N        -> reproduces the buggy premise[:800] result
  (B) ORIG-trunc, N>=1 only    -> drop the N=0 raw-dump artifact point (DECISIVE)
  (C) FIXED window-maxpool, N>=1 -> full source content, no 800-char premise cut
N=0 is EXCLUDED from view C on purpose: at N=0 the "memory" IS the whole raw dump
(hypothesis longer than any premise window) -> not a comparable consolidation point
(red-team: N=0 is a raw baseline, trend must be read from N>=1). View A keeps N=0
only to display the artifact spike.

If the descending trend in (A) flattens in (B) and (C), the 'consolidation makes
memory better' read was a truncation artifact -> honest answer is FLAT (benign).
Zero API, CPU, offline. Reuses load_nli (same DeBERTa-MNLI model).
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

ROOT = Path("/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot")
sys.path.insert(0, str(ROOT / "scripts" / "core"))
from rq2_stage_extract import load_nli, iter_pages, extract_run  # noqa
from safety_honest_metrics import clopper_pearson  # noqa
from stats_guardrails import cochran_armitage_trend  # noqa

PS = ROOT / "outputs" / "v2_tiermem_micro" / "page_store"
PERSONA = "2f1f897e-d67f-dbc5-6a7b-b7634a9e294f"
TRUNC = 800; MEM_CAP = 1000
FMT = "e1_halumem_targeted_cov10_depth_20260701_summary_only_n{N}"
NS = [0, 1, 2, 4, 8]
WIN = 700; STRIDE = 550; MAX_WIN = 12; MEM_TRUNC = 1500


def windows(text: str) -> list[str]:
    text = str(text or "")
    if len(text) <= WIN:
        return [text] if text else [""]
    out, i = [], 0
    while i < len(text) and len(out) < MAX_WIN:
        out.append(text[i:i + WIN]); i += STRIDE
    return out


def load_ps(N: int):
    pf = PS / FMT.format(N=N) / f"halumem_Medium_{PERSONA}.json"
    return json.loads(pf.read_text(encoding="utf-8")) if pf.exists() else None


def score_trunc(ps: dict, predict) -> dict:
    """Original behaviour: premise=content[:800], hyp=memory[:1000], whole-premise NLI."""
    d = json.loads(json.dumps(ps))
    for p in list(iter_pages(d)):
        if p.get("content"):
            p["content"] = str(p["content"])[:TRUNC]
        if p.get("memories"):
            p["memories"] = [str(m)[:MEM_CAP] for m in p["memories"]]
    r = extract_run(d, predict)
    nm = r["new_memory"]
    contra = sum(1 for m in nm if m["nli_label"] == "contradiction")
    neu = sum(1 for m in nm if m["nli_label"] == "neutral")
    return {"n": len(nm), "unmr": contra + neu, "contra": contra}


def score_fixed(ps: dict, predict) -> dict:
    """FIXED: per memory, NLI over ALL content windows (batched per page), column-max entail."""
    n = unmr = contra = 0
    pages = [p for p in iter_pages(ps) if (p.get("memories") and p.get("content"))]
    for pi, p in enumerate(pages):
        wins = windows(str(p.get("content") or ""))
        mems = [str(m)[:MEM_TRUNC] for m in (p.get("memories") or []) if str(m).strip()]
        if not mems:
            continue
        prem, hyp, idx = [], [], []
        for mi, mem in enumerate(mems):
            for w in wins:
                prem.append(w); hyp.append(mem); idx.append(mi)
        labels, eprobs = predict(prem, hyp, batch_size=32)
        best_e = [-1.0] * len(mems); best_lab = [None] * len(mems); has_c = [False] * len(mems)
        for lab, e, mi in zip(labels, eprobs, idx):
            if lab == "contradiction":
                has_c[mi] = True
            if e > best_e[mi]:
                best_e[mi] = e; best_lab[mi] = lab
        for mi in range(len(mems)):
            n += 1
            lab = "entailment" if best_lab[mi] == "entailment" else ("contradiction" if has_c[mi] else "neutral")
            if lab in ("neutral", "contradiction"):
                unmr += 1
            if lab == "contradiction":
                contra += 1
        if (pi + 1) % 20 == 0:
            print(f"      …page {pi+1}/{len(pages)} n_mem={n}", flush=True)
    return {"n": n, "unmr": unmr, "contra": contra}


def rate(k, n):
    if not n:
        return (float("nan"),) * 3
    r = clopper_pearson(k, n); return (r["point"], r["lo"], r["hi"])


def trend(rows, key):
    valid = [(N, t) for N, t in rows if t and t["n"] > 0]
    if len(valid) < 3:
        return "  <3 有效档"
    L = [N for N, _ in valid]; E = [t[key] for _, t in valid]; T = [t["n"] for _, t in valid]
    res = cochran_armitage_trend(L, E, T)
    return (f"dir={res.get('direction')} z={res.get('z'):.2f} p={res.get('p_value'):.4f} "
            f"rates={['%.2f'%x if x is not None else '-' for x in res.get('rates', [])]}")


def main():
    print(">> loading NLI (CPU)…", flush=True)
    predict = load_nli(device="cpu")[0]
    print(">> ready\n", flush=True)
    A, C = {}, {}
    for N in NS:
        ps = load_ps(N)
        if ps is None:
            print(f"  (missing N={N})"); continue
        t0 = time.time()
        A[N] = score_trunc(ps, predict)
        if N >= 1:  # view C excludes N=0 (raw-dump hypothesis, non-comparable)
            C[N] = score_fixed(ps, predict)
        cs = f" FIXED unmr={C[N]['unmr']}/{C[N]['n']}" if N in C else " FIXED=skip(raw baseline)"
        print(f"  N={N} ({time.time()-t0:4.0f}s): ORIG unmr={A[N]['unmr']}/{A[N]['n']}{cs}", flush=True)

    def show(tag, table, Ns):
        print(f"\n[{tag}]")
        for N in Ns:
            t = table.get(N)
            if not t:
                continue
            up, ul, uh = rate(t["unmr"], t["n"]); cp, cl, ch = rate(t["contra"], t["n"])
            print(f"   N={N}: UNMR {up:.3f}[{ul:.2f},{uh:.2f}] {t['unmr']}/{t['n']}   contra {cp:.3f} {t['contra']}/{t['n']}")
        print("   UNMR   trend:", trend([(N, table.get(N)) for N in Ns], "unmr"))
        print("   contra trend:", trend([(N, table.get(N)) for N in Ns], "contra"))

    print("\n" + "=" * 82)
    print("RQ2 F1 — N=0 截断伪影三视图对照 (summary_only)")
    print("=" * 82)
    show("A · ORIG 截断 premise[:800], 全 N(含 N=0 伪影点)", A, NS)
    show("B · ORIG 截断, 去 N=0(最便宜的翻案刀)", A, [n for n in NS if n != 0])
    show("C · FIXED 切块 full-premise max-pool, N>=1", C, [n for n in NS if n != 0])
    print("=" * 82)
    Path(__file__).with_name("rq2_f1_fixed_result.json").write_text(
        json.dumps({"orig_trunc": {str(k): v for k, v in A.items()},
                    "fixed_maxpool": {str(k): v for k, v in C.items()}},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("RQ2_F1_DONE")


if __name__ == "__main__":
    main()
