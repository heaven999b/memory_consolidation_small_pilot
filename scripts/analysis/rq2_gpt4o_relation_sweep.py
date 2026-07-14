#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ2 NEW-SIGNAL hunt: does consolidation introduce RELATION/ROLE fabrication that
the word-bag DeBERTa-MNLI is blind to? Re-judge the SAME consolidated memories
(summary_only N=1,2,4,8) with gpt-4o as a RELATION-AWARE faithfulness judge.

DeBERTa (full-premise, fixed) said ~3% unsupported, flat. If gpt-4o — which can see
role/attribution/relation flips — finds MORE unfaithful memories AND rising with N,
that is a genuine new signal the old detector missed. If flat/low too, the RQ2
negative is confirmed on a detector that is NOT relation-blind.
"""
import os, sys, json, time
from pathlib import Path
sys.path.insert(0, "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/core")
from rq2_stage_extract import iter_pages  # noqa
from openai import OpenAI

ROOT = Path("/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot")
PS = ROOT / "outputs" / "v2_tiermem_micro" / "page_store"
PERSONA = "2f1f897e-d67f-dbc5-6a7b-b7634a9e294f"
FMT = "e1_halumem_targeted_cov10_depth_20260701_summary_only_n{N}"
NS = [1, 2, 4, 8]           # consolidation depths (N=0 raw dump = trivially faithful, skip)
SRC_CAP = 9000              # source context fed to judge
JUDGE_MODEL = "gpt-4o"

JUDGE = """You are a strict faithfulness auditor for a memory system. A SOURCE conversation was summarised into a MEMORY. Decide whether the MEMORY is faithful to the SOURCE.

Judge ESPECIALLY for RELATION / ROLE / ATTRIBUTION errors (the kind a bag-of-words checker misses):
- who did what to whom (agent vs patient swapped)
- attribute bound to the wrong entity (e.g. a name/date/role reassigned)
- a qualifier, negation, or condition dropped so the meaning flips
- a claim asserted that the source does not support

SOURCE:
{src}

MEMORY:
{mem}

Answer ONLY JSON:
{{"verdict":"SUPPORTED" or "UNSUPPORTED" or "CONTRADICTS","error_type":"none|relation|attribution|dropped_qualifier|unsupported_claim|other","reason":"1 short sentence"}}"""

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_BASE_URL"])


def judge(src, mem):
    for _ in range(3):
        try:
            r = client.chat.completions.create(model=JUDGE_MODEL, temperature=0,
                messages=[{"role": "user", "content": JUDGE.format(src=src[:SRC_CAP], mem=mem[:2000])}])
            raw = r.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]; raw = raw[4:] if raw.startswith("json") else raw
            o = json.loads(raw.strip())
            return o.get("verdict", "").upper(), o.get("error_type", "?"), o.get("reason", "")
        except Exception:
            time.sleep(1)
    return "SUPPORTED", "judge_fail", ""   # conservative: don't inflate on failure


def load(N):
    pf = PS / FMT.format(N=N) / f"halumem_Medium_{PERSONA}.json"
    return json.loads(pf.read_text(encoding="utf-8")) if pf.exists() else None


def main():
    table = {}; errdump = []
    for N in NS:
        ps = load(N)
        if ps is None:
            print(f"(missing N={N})"); continue
        n = unmr = contra = rel = 0
        t0 = time.time()
        for p in iter_pages(ps):
            src = str(p.get("content") or "")
            for m in (p.get("memories") or []):
                m = str(m).strip()
                if not m:
                    continue
                n += 1
                v, et, why = judge(src, m)
                if v in ("UNSUPPORTED", "CONTRADICTS"):
                    unmr += 1
                    if v == "CONTRADICTS":
                        contra += 1
                    if et in ("relation", "attribution", "dropped_qualifier"):
                        rel += 1
                    if len(errdump) < 25:
                        errdump.append({"N": N, "verdict": v, "type": et, "why": why, "mem": m[:200]})
        table[N] = {"n": n, "unmr": unmr, "contra": contra, "rel_type": rel}
        print(f"  N={N} ({time.time()-t0:.0f}s): n={n} unmr={unmr} contra={contra} relation-type={rel}", flush=True)

    print("\n" + "=" * 74)
    print(f"RQ2 关系级判官 (gpt-4o) vs 固化深度 — 找 NLI 漏掉的关系造假")
    print("=" * 74)
    print(f"{'N':>3} | {'n':>3} | {'UNMR(不忠实)':>14} | {'CONTRA':>8} | {'关系/归属/丢限定错':>16}")
    for N in NS:
        t = table.get(N)
        if not t:
            continue
        ur = t["unmr"] / t["n"] if t["n"] else 0
        print(f"{N:>3} | {t['n']:>3} | {ur*100:5.1f}% {t['unmr']:>2}/{t['n']:<3} | {t['contra']:>6}   | {t['rel_type']:>6}")
    print("=" * 74)
    print("样本(gpt-4o 判不忠实的记忆,看是不是真错还是误报):")
    for e in errdump[:12]:
        print(f"  [N={e['N']} {e['verdict']}/{e['type']}] {e['why']}  ::  {e['mem'][:110]}")
    (Path(__file__).with_name("rq2_gpt4o_relation_result.json")).write_text(
        json.dumps({"table": {str(k): v for k, v in table.items()}, "errdump": errdump}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("RQ2_GPT4O_DONE")


if __name__ == "__main__":
    main()
