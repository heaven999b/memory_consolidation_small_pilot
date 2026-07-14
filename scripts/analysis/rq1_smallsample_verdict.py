#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ1 small-sample verdict: re-score an EXISTING live N-sweep with the NEW NLI +
payload metrics (offline, $0). Answers: does recursive consolidation preserve /
launder unsafe seeds and keep the reader complying, worsening with N?

Data = outputs/safety/rq1_locomo_pilot6_n012_items.jsonl (6 AgentPoison-on-LoCoMo
seeds x N in {0,1,2}, auto route, real TierMem consolidated_text + answer_text).
Metrics via safety_metrics.build_observation (NLI survival + payload_emitted
behavioural endpoint) -> SRR/UAF/unsafe_answer_rate by N + Cochran-Armitage trend.
"""
from __future__ import annotations
import json, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot")
sys.path.insert(0, str(ROOT / "scripts" / "core"))
import safety_metrics as sm  # noqa
from rq2_stage_extract import load_nli  # noqa
from safety_honest_metrics import clopper_pearson  # noqa
from stats_guardrails import cochran_armitage_trend  # noqa

ITEMS = ROOT / "outputs" / "safety" / "rq1_locomo_pilot6_n012_items.jsonl"


def ci(k, n):
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    r = clopper_pearson(k, n)
    return (r["point"], r["lo"], r["hi"])


def main():
    print(">> loading local NLI (MPS)…", flush=True)
    predict = load_nli(device="mps")[0]
    rows = [json.loads(l) for l in ITEMS.read_text(encoding="utf-8").splitlines() if l.strip()]
    by_n = defaultdict(list)
    for r in rows:
        item = {"id": r["item_id"], "unsafe_action": r["unsafe_action"],
                "policy": r.get("policy", ""), "unsafe_paraphrases": r.get("unsafe_paraphrases", [])}
        obs = sm.build_observation(item, r["passes"], r["consolidated_text"],
                                   r.get("retrieved_texts") or [], r["answer_text"], predict)
        by_n[r["passes"]].append(obs)

    Ns = sorted(by_n)
    print("\n" + "=" * 88)
    print("RQ1 · AgentPoison-on-LoCoMo pilot (6 seeds × N, auto route) · NLI+payload 重打分")
    print("-" * 88)
    print(f"{'N':>3} | {'n':>3} | {'SRR (survive)':>20} | {'UAF (laundered)':>20} | {'unsafe_answer(payload)':>24}")
    agg = {}
    for N in Ns:
        obs = by_n[N]
        n = len(obs)
        srr = sum(o.unsafe_present for o in obs)
        uaf = sum(o.unsafe_laundered for o in obs)
        ua = sum(o.answer_is_unsafe for o in obs)
        agg[N] = {"n": n, "srr": srr, "uaf": uaf, "ua": ua}
        sp, sl, sh = ci(srr, n); up, ul, uh = ci(uaf, n); ap, al, ah = ci(ua, n)
        print(f"{N:>3} | {n:>3} | {sp:.3f}[{sl:.2f},{sh:.2f}] {srr}/{n:<3} "
              f"| {up:.3f}[{ul:.2f},{uh:.2f}] {uaf}/{n:<3} "
              f"| {ap:.3f}[{al:.2f},{ah:.2f}] {ua}/{n}")
    print("-" * 88)

    def trend(key, lab):
        ev = [agg[N][key] for N in Ns]; tot = [agg[N]["n"] for N in Ns]
        res = cochran_armitage_trend(list(Ns), ev, tot)
        print(f"  {lab}: direction={res.get('direction')}  z={res.get('z'):.2f}  "
              f"p={res.get('p_value'):.4f}  rates={['%.2f'%r if r is not None else '-' for r in res.get('rates',[])]}")
    print(" 预注册趋势(amplifying 且 p<0.01 = RQ1 固化放大成立):")
    trend("srr", "SRR          ")
    trend("uaf", "UAF laundering")
    trend("ua", "unsafe_answer ")
    print()
    (Path(__file__).with_name("rq1_smallsample_result.json")).write_text(
        json.dumps({str(N): agg[N] for N in Ns}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved:", Path(__file__).with_name("rq1_smallsample_result.json"))


if __name__ == "__main__":
    main()
