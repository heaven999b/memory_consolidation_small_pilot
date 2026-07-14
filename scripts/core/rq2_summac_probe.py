#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2 probe: does a SummaC-style sentence-pair reconstruction (over the SAME cached
DeBERTa-MNLI) fix the cross-sentence relabel blind spot S1 found? Offline, CPU, $0.

SummaC (2111.09525) = split premise into sentences, NLI(each source sentence, claim),
aggregate by column-max entailment. Reuses rq2_seed_taxonomy.build_seed_set so it's the
SAME gold control as S1. Expected (honest): max-pooling over source sentences makes it
EASIER to find the one sentence that spuriously entails "middle name is Mark" ("My name is
Martin Mark"), so relabel_cross recall does NOT improve (likely drops) -> confirms the fix
needs a different model class (MiniCheck/QASem), not available offline.
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "core"))


def split_sents(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description="SummaC-style probe on the S1 seeded control.")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--tau", type=float, default=0.5, help="entail_prob threshold for 'supported'.")
    ap.add_argument("--out", default=str(ROOT / "state" / "rq2_summac_probe_result_20260711.json"))
    args = ap.parse_args()

    from rq2_seed_taxonomy import build_seed_set
    from rq2_stage_extract import load_nli
    from safety_honest_metrics import clopper_pearson

    predict = load_nli(device=args.device)[0]
    items = build_seed_set()

    # For each item, NLI(source_sentence_i, hypothesis) over all i; column-max entailment.
    premises, hyps, owner = [], [], []
    per_item_sents: list[list[int]] = []
    for idx, it in enumerate(items):
        sents = split_sents(it["premise"])
        idxs = []
        for s in sents:
            premises.append(s); hyps.append(it["hypothesis"]); owner.append(idx); idxs.append(len(premises) - 1)
        per_item_sents.append(idxs)

    labels, eprobs = predict(premises, hyps)

    by_type = defaultdict(list)
    for idx, it in enumerate(items):
        pair_idx = per_item_sents[idx]
        max_ent = max((eprobs[j] for j in pair_idx), default=0.0)
        any_contra = any(labels[j] == "contradiction" for j in pair_idx)
        # SummaC label: supported if any source sentence entails the claim >= tau
        if max_ent >= args.tau:
            pred = "entailment"
        elif any_contra:
            pred = "contradiction"
        else:
            pred = "neutral"
        it2 = dict(it); it2["summac_label"] = pred; it2["max_entail"] = round(float(max_ent), 3)
        by_type[it["error_type"]].append(it2)

    print(f"SummaC-over-DeBERTa-MNLI (tau={args.tau}) on S1 control · device={args.device}\n")
    print(f"{'error_type':>15} | {'gold':>11} | {'metric':>26} | vs vanilla")
    print("-" * 78)
    VANILLA = {"faithful": 0.00, "fabrication": 1.00, "entity_swap": 1.00,
               "role_swap": 1.00, "relabel_single": 1.00, "relabel_cross": 0.50}
    summary = {}
    for et, rows in by_type.items():
        gold = rows[0]["gold"]
        if gold == "supported":
            bad = sum(1 for r in rows if r["summac_label"] != "entailment")
            cp = clopper_pearson(bad, len(rows)); summary[et] = {"gold": gold, "fp_rate": cp["point"]}
            print(f"{et:>15} | {gold:>11} | FP {cp['point']:.2f} {bad}/{len(rows):<3}          | vanilla FP {VANILLA[et]:.2f}")
        else:
            caught = sum(1 for r in rows if r["summac_label"] != "entailment")
            cp = clopper_pearson(caught, len(rows)); summary[et] = {"gold": gold, "recall": cp["point"]}
            delta = cp["point"] - VANILLA[et]
            flag = "  <== 仍盲" if cp["point"] < 0.8 else ""
            print(f"{et:>15} | {gold:>11} | Recall {cp['point']:.2f}[{cp['lo']:.2f},{cp['hi']:.2f}] {caught}/{len(rows):<3}| vanilla {VANILLA[et]:.2f} (Δ{delta:+.2f}){flag}")
    print("-" * 78)
    mis = [et for et, s in summary.items() if s["gold"] == "mislabel"]
    rk = min(summary[et]["recall"] for et in mis)
    print(f"\nRecall_k(SummaC) = {rk:.2f}  vs vanilla 0.50  门槛>=0.80")
    print("结论:", "SummaC 修好了盲区" if rk >= 0.8 else
          "SummaC 仍 DETECTION-LIMITED —— 句级 max-pool 修不了跨句 relabel,需 MiniCheck/QASem 类模型(离线无)")
    Path(args.out).write_text(json.dumps({"tau": args.tau, "recall_k": rk, "by_type": summary},
                                         ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
