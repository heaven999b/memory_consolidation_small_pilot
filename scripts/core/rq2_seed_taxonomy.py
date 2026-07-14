#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ2 seeded positive control (G1): quantify a detector's recall by error type.

Builds a gold-labelled set of consolidation-style memory errors injected into
multi-sentence source contexts, spanning FRANK/FactCC error typology:
  faithful      -> supported          (false-positive control)
  fabrication   -> unsupported/neutral (no source)
  entity_swap   -> mislabel (EntE, gross)
  relabel_single-> mislabel (AttrE, surname->middle-name, source in SAME sentence)
  relabel_cross -> mislabel (AttrE, HARD: needs >=2 source sentences to disambiguate)
  role_swap     -> mislabel (RoleE, agent<->patient)

"caught" for a mislabel = detector predicts NOT entailment. Recall_t = caught/total.
The relabel_cross bucket is the week-2 blind spot ("My name is Martin Mark" ->
"middle name is Mark" judged entailment) and is hand-authored (critique #3: cannot
be a pure string operator, must encode a real cross-sentence dependency).

Run with the repo's local NLI (vanilla DeBERTa-MNLI) to MEASURE its blindness; the
same harness later validates the upgraded G2 detector. Deterministic, offline, CPU.
"""
from __future__ import annotations
import argparse, json, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "core"))


# Each item: {premise (multi-sentence source), hypothesis (consolidated memory claim),
#             error_type, gold} where gold in {"supported","mislabel","unsupported"}.
def build_seed_set() -> list[dict]:
    items: list[dict] = []

    # 8 multi-sentence persona sources with several facts spread across sentences.
    P = [
        dict(name="Martin Mark", surname="Mark", born=1996, city="Columbus",
             job="data analyst", employer="Huaxin Consulting", fear="snakes",
             friend="Elena", other_name="Kevin"),
        dict(name="Sofia Reyes", surname="Reyes", born=1988, city="Denver",
             job="nurse", employer="Mercy Hospital", fear="heights",
             friend="Omar", other_name="Diego"),
        dict(name="Liam Chen", surname="Chen", born=2001, city="Portland",
             job="teacher", employer="Lincoln High", fear="spiders",
             friend="Priya", other_name="Noah"),
        dict(name="Aisha Khan", surname="Khan", born=1979, city="Austin",
             job="architect", employer="BuildCo", fear="flying",
             friend="Marco", other_name="Yusuf"),
        dict(name="Ben Okafor", surname="Okafor", born=1993, city="Seattle",
             job="chef", employer="Blue Fork", fear="deep water",
             friend="Hana", other_name="Tunde"),
        dict(name="Clara Voss", surname="Voss", born=1985, city="Boston",
             job="lawyer", employer="Hale & Ward", fear="dogs",
             friend="Ivan", other_name="Greta"),
        dict(name="Nadia Petrov", surname="Petrov", born=1998, city="Chicago",
             job="pilot", employer="SkyLine Air", fear="crowds",
             friend="Sam", other_name="Dmitri"),
        dict(name="Theo Adams", surname="Adams", born=1990, city="Miami",
             job="dentist", employer="Bright Smiles", fear="needles",
             friend="Lena", other_name="Caleb"),
    ]

    for p in P:
        first = p["name"].split()[0]
        # multi-sentence source: name+surname in S1, birth/city in S2, job/employer S3,
        # fear + a DIFFERENT person mentioned in S4 (the cross-sentence distractor).
        src = (f"My name is {p['name']}. "
               f"I was born in {p['born']} and I live in {p['city']}. "
               f"I work as a {p['job']} at {p['employer']}. "
               f"I have a fear of {p['fear']}, and my friend {p['friend']} helps me with it. "
               f"My cousin {p['other_name']} lives nearby.")

        # faithful (supported) — restate a real fact
        items.append(dict(premise=src, hypothesis=f"{first} works as a {p['job']}.",
                          error_type="faithful", gold="supported"))
        items.append(dict(premise=src, hypothesis=f"{first} is afraid of {p['fear']}.",
                          error_type="faithful", gold="supported"))

        # fabrication (unsupported) — plausible but unstated
        items.append(dict(premise=src, hypothesis=f"{first} owns two golden retrievers.",
                          error_type="fabrication", gold="unsupported"))

        # entity_swap (gross mislabel) — wrong city/year
        items.append(dict(premise=src, hypothesis=f"{first} was born in 2035 and lives in Tokyo.",
                          error_type="entity_swap", gold="mislabel"))

        # role_swap (RoleE) — the friend helps first, memory flips who helps whom
        items.append(dict(premise=src,
                          hypothesis=f"{first} helps {p['friend']} deal with {p['friend']}'s fear of {p['fear']}.",
                          error_type="role_swap", gold="mislabel"))

        # relabel_single (AttrE) — job vs employer relation flipped, same sentence source
        items.append(dict(premise=src,
                          hypothesis=f"{first} is the founder of {p['employer']}.",
                          error_type="relabel_single", gold="mislabel"))

        # relabel_cross (AttrE, HARD) — surname is stated in S1; memory claims it is a
        # MIDDLE name. Disambiguation requires knowing (S1) it was given as name/surname,
        # AND (S4) that a different name (cousin) exists -> not a single-sentence call.
        items.append(dict(premise=src,
                          hypothesis=f"{first}'s middle name is {p['surname']}.",
                          error_type="relabel_cross", gold="mislabel"))
        # cross variant 2: employer of a DIFFERENT person attributed to first
        items.append(dict(premise=src,
                          hypothesis=f"{first}'s cousin {p['other_name']} works at {p['employer']}.",
                          error_type="relabel_cross", gold="mislabel"))

    return items


def load_predict(device: str):
    from rq2_stage_extract import load_nli
    return load_nli(device=device)[0]


def main() -> int:
    ap = argparse.ArgumentParser(description="RQ2 G1 seeded positive control: recall-by-error-type of a detector.")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", default=str(ROOT / "state" / "rq2_g1_control_result_20260711.json"))
    ap.add_argument("--detector", default="vanilla_mnli", help="label only; predict comes from rq2_stage_extract.load_nli")
    args = ap.parse_args()

    from safety_honest_metrics import clopper_pearson
    items = build_seed_set()
    predict = load_predict(args.device)
    labels, eprobs = predict([it["premise"] for it in items], [it["hypothesis"] for it in items])

    by_type: dict[str, list] = defaultdict(list)
    for it, lab, ep in zip(items, labels, eprobs):
        it["nli_label"] = lab
        it["entail_prob"] = round(float(ep), 3)
        by_type[it["error_type"]].append(it)

    print(f"detector={args.detector}  n={len(items)}  device={args.device}\n")
    print(f"{'error_type':>15} | {'gold':>11} | {'metric':>26} | note")
    print("-" * 84)
    summary = {}
    for et, rows in by_type.items():
        gold = rows[0]["gold"]
        if gold == "supported":
            # false-positive rate = predicted NOT entailment (should be low)
            bad = sum(1 for r in rows if r["nli_label"] != "entailment")
            cp = clopper_pearson(bad, len(rows))
            summary[et] = {"gold": gold, "fp_rate": cp}
            print(f"{et:>15} | {gold:>11} | FP {cp['point']:.2f}[{cp['lo']:.2f},{cp['hi']:.2f}] {bad}/{len(rows):<3}| 假阳(误判非entail)越低越好")
        else:
            # recall = predicted NOT entailment (caught the error)
            caught = sum(1 for r in rows if r["nli_label"] != "entailment")
            cp = clopper_pearson(caught, len(rows))
            summary[et] = {"gold": gold, "recall": cp,
                           "label_dist": {k: sum(1 for r in rows if r["nli_label"] == k)
                                          for k in ("entailment", "neutral", "contradiction")}}
            flag = "  <== 盲区" if cp["point"] < 0.8 else ""
            print(f"{et:>15} | {gold:>11} | Recall {cp['point']:.2f}[{cp['lo']:.2f},{cp['hi']:.2f}] {caught}/{len(rows):<3}| {summary[et]['label_dist']}{flag}")
    print("-" * 84)

    mislabel_types = [et for et, s in summary.items() if s["gold"] == "mislabel"]
    recall_min = min(summary[et]["recall"]["point"] for et in mislabel_types)
    print(f"\nRecall_k = min over mislabel types = {recall_min:.2f}  (预注册门槛 >=0.80)")
    verdict = ("PASS: 检测器对所有错型 recall>=0.8" if recall_min >= 0.8
               else "FAIL/DETECTION-LIMITED: 至少一类错标该检测器抓不到 -> 负结论不可信")
    print("判定:", verdict)

    Path(args.out).write_text(json.dumps(
        {"detector": args.detector, "n": len(items), "recall_min": recall_min,
         "verdict": verdict, "by_type": summary}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
