#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ2 credible small-sample verdict (offline, CPU, $0) — consolidated.

Within-persona controlled design (persona 2f1f897e), TWO routes:
  summary_only = pure compression (PDF RQ2 risk arm)   N = {0,1,2,4,8}
  auto         = TierMem summary + raw escalation       N = {0,1,2}
Stage metrics via rq2_stage_extract NLI three-way (entail=support /
neutral=unsupported / contradiction=hard false memory) on the consolidated
page.memories vs page.content, PLUS PAR from the run's *_qa.jsonl.

Content is truncated to 800 chars so CPU NLI is tractable and MPS-hang-free; the
truncation bias is CONSTANT across N and route, so the SLOPE-over-N and the
route-contrast (the actual verdict) are unaffected. Conclusions are framed on
trend/contrast, not the absolute UNMR level.

Verdict logic:
  RQ2 (pure compression amplifies false memory) HOLDS iff UNMR/contradiction/PAR
  rise with N (Cochran-Armitage amplifying, p<0.01). Construct validity: if auto
  spikes on contradiction where summary_only stays flat, the metric can detect real
  consolidation fabrication -> a flat summary_only is a REAL benign, not NLI blindness.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path("/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot")
sys.path.insert(0, str(ROOT / "scripts" / "core"))
from rq2_stage_extract import load_nli, extract_run, extract_par  # noqa
from safety_honest_metrics import clopper_pearson  # noqa
from stats_guardrails import cochran_armitage_trend  # noqa

PS = ROOT / "outputs" / "v2_tiermem_micro" / "page_store"
SESS = ROOT / "outputs" / "v2_tiermem_micro" / "halumem" / "linked_view"
PERSONA = "2f1f897e-d67f-dbc5-6a7b-b7634a9e294f"
TRUNC = 800
MEM_CAP = 1000
ROUTES = {
    "summary_only": ("e1_halumem_targeted_cov10_depth_20260701_summary_only_n{N}", [0, 1, 2, 4, 8]),
    "auto":         ("e1_multiseed_halumem_auto_20260706_004033_seed11_auto_n{N}", [0, 1, 2]),
}


def trunc_content(d: dict) -> dict:
    cp = d.get("completed_pages")
    pages = cp if isinstance(cp, list) else [x for v in (cp or {}).values() for x in (v or [])]
    cur = d.get("current_page")
    if isinstance(cur, dict):
        pages.append(cur)
    for p in pages:
        if isinstance(p, dict) and p.get("content"):
            p["content"] = str(p["content"])[:TRUNC]
        # also cap each memory (hypothesis) so N=0 raw dumps (~4500 chars = 512 tok)
        # don't dominate CPU; N>=1 compact memories are usually < MEM_CAP so unaffected.
        if isinstance(p, dict) and p.get("memories"):
            p["memories"] = [str(m)[:MEM_CAP] for m in p["memories"]]
    return d


def ci(k, n):
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    r = clopper_pearson(k, n)
    return (r["point"], r["lo"], r["hi"])


def main():
    print(">> loading local NLI (CPU)…", flush=True)
    predict = load_nli(device="cpu")[0]
    print(">> NLI ready. scoring stage metrics on existing runs (zero API)…\n", flush=True)
    table = {}
    contra_dump = []
    for route, (fmt, Ns) in ROUTES.items():
        for N in Ns:
            pf = PS / fmt.format(N=N) / f"halumem_Medium_{PERSONA}.json"
            if not pf.exists():
                print(f"  (missing {route} N={N}: {pf.name})", flush=True); continue
            d = trunc_content(json.loads(pf.read_text(encoding="utf-8")))
            r = extract_run(d, predict)
            nm = r["new_memory"]; n = len(nm)
            contra = sum(1 for m in nm if m["nli_label"] == "contradiction")
            neu = sum(1 for m in nm if m["nli_label"] == "neutral")
            unmr = contra + neu
            # PAR
            qa = SESS / fmt.format(N=N) / "sessions" / f"halumem_Medium_{PERSONA}_qa.jsonl"
            answers = extract_par(qa, r["_unsupported_pages"]) if qa.exists() else []
            par_num = sum(1 for a in answers if a["used_unsupported_memory"])
            table[(route, N)] = {"n": n, "unmr": unmr, "contra": contra, "neu": neu,
                                 "n_ans": len(answers), "par": par_num}
            # collect contradiction memory texts (construct validity)
            bad_pids = {m["page_id"] for m in nm if m["nli_label"] == "contradiction"}
            if bad_pids:
                cp = d.get("completed_pages")
                pages = cp if isinstance(cp, list) else [x for v in (cp or {}).values() for x in (v or [])]
                for p in pages:
                    if str(p.get("page_id")) in bad_pids:
                        for m in (p.get("memories") or []):
                            contra_dump.append({"route": route, "N": N, "mem": str(m)[:240]})
                            break
            print(f"  scored {route:>12} N={N}  n_mem={n}  unmr={unmr}  contra={contra}  par={par_num}/{len(answers)}", flush=True)

    print("\n" + "=" * 96)
    print(f"RQ2 stage 指标 · persona {PERSONA[:8]} · content截断{TRUNC}字(偏差跨N/路由恒定)")
    print("-" * 96)
    print(f"{'route':>13} {'N':>2} | {'n_mem':>5} | {'UNMR unsupported':>26} | {'contradiction(硬假记忆)':>26} | {'PAR':>12}")
    for route, (fmt, Ns) in ROUTES.items():
        for N in Ns:
            t = table.get((route, N))
            if not t:
                continue
            up, ul, uh = ci(t["unmr"], t["n"]); cp_, cl, ch = ci(t["contra"], t["n"])
            pp, pl, ph = ci(t["par"], t["n_ans"])
            us = f"{up:.3f}[{ul:.2f},{uh:.2f}] {t['unmr']}/{t['n']}"
            cs = f"{cp_:.3f}[{cl:.2f},{ch:.2f}] {t['contra']}/{t['n']}"
            ps = f"{pp:.2f} {t['par']}/{t['n_ans']}" if t["n_ans"] else "n/a"
            print(f"{route:>13} {N:>2} | {t['n']:>5} | {us:>26} | {cs:>26} | {ps:>12}")
    print("-" * 96)

    def trend(route, key, lab):
        fmt, Ns = ROUTES[route]
        rows = [(N, table[(route, N)]) for N in Ns if (route, N) in table]
        if key == "par":
            ev = [t["par"] for _, t in rows]; tot = [t["n_ans"] for _, t in rows]
        else:
            ev = [t[key] for _, t in rows]; tot = [t["n"] for _, t in rows]
        L = [N for N, _ in rows]
        valid = [(l, e, tt) for l, e, tt in zip(L, ev, tot) if tt > 0]
        if len(valid) < 3:
            return f"  {lab}: <3有效档,跳过"
        LL, EE, TT = zip(*valid)
        res = cochran_armitage_trend(list(LL), list(EE), list(TT))
        return (f"  {lab}: dir={res.get('direction')} z={res.get('z'):.2f} p={res.get('p_value'):.4f} "
                f"rates={['%.2f'%x if x is not None else '-' for x in res.get('rates',[])]}")

    print(" summary_only 随 N 趋势(amplifying 且 p<0.01 = RQ2 固化造假成立):")
    print(trend("summary_only", "unmr", "UNMR         "))
    print(trend("summary_only", "contra", "contradiction"))
    print(trend("summary_only", "par", "PAR          "))
    print("\n 构造效度正控 · 被判 contradiction 的固化记忆原文(看是否抓到真造假):")
    if not contra_dump:
        print("  (无 contradiction —— 两路由都没测到硬假记忆)")
    for e in contra_dump[:10]:
        print(f"  [{e['route']} N={e['N']}] {e['mem']}")

    Path(__file__).with_name("rq2_final_result.json").write_text(
        json.dumps({f"{r}_N{n}": v for (r, n), v in table.items()},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nRQ2_DONE")


if __name__ == "__main__":
    main()
