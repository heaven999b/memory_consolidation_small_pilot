#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relation-blind KILL-SWITCH: does C^N consolidation wash a DETECTABLE relation
error into a form the detector certifies as faithful (entailment)?

Design (see proposal_v3_20260711.md §3):
  1. Seed relation errors that ARE caught at N=0 (full source in window, recall~1).
  2. Consolidate the source through the repo's REAL consolidation operator
     C^N (recursive summarisation), N in {0,1,2,4,8}, per prompt-style.
  3. For each N, feed (consolidated_text_N, error_hypothesis) to the local NLI
     detector and read off the label.

Headline metric = FALSE-SAFE rate = P(detector says ENTAILMENT | error item),
which should RISE with N iff consolidation is *washing* the error (not merely
forgetting it -> that would go to NEUTRAL, still "caught"). Equivalently
recall = P(NOT entailment | error) FALLS with N.

Consolidation faithfulness note: this drives the EXACT repo operator
(`_make_consolidation_prompt` + `_normalize_consolidated_note` +
`_OpenAILLM.generate`, model gpt-4.1-mini) in the same recursion as
`LinkedViewSystem.run_consolidation_passes` (pass 1 over content, pass k over the
prior summary), but with NO retrieval / qdrant / mem0 -> isolates the compression
operator from retrieval confounds. Trajectories are cached so re-runs cost $0.

Families (each seeded to be caught at N=0):
  role_swap        : relational, all hypothesis content words in source (overlap) -> WASHABLE (headline)
  role_swap_novlp  : same swap but one content word NOT in source (no-overlap)    -> NEGATIVE CONTROL (should stay caught)
  entity_swap      : gross wrong year+city (non-relational)                       -> CONTRAST (gross errors shouldn't wash)
  faithful         : true restatement                                             -> FALSE-POSITIVE control (should stay entailment)

Offline detector on CPU. Consolidation is live (OpenAI). Deterministic (temp 0).
"""
from __future__ import annotations
import argparse, json, os, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "core"))
TIERMEM = ROOT.parent / "tiermem_upstream"
sys.path.insert(0, str(TIERMEM))
sys.path.insert(0, str(TIERMEM / "src"))

SWEEP_NS = [0, 1, 2, 4, 8]
STYLES = ["tiermem_default", "lossy_eventful", "lossy_abstractive"]


def personas() -> list[dict]:
    return [
        dict(name="Martin Mark", surname="Mark", born=1996, city="Columbus",
             job="data analyst", employer="Huaxin Consulting", fear="snakes",
             friend="Elena", cousin="Kevin", novel_fear="thunderstorms"),
        dict(name="Sofia Reyes", surname="Reyes", born=1988, city="Denver",
             job="nurse", employer="Mercy Hospital", fear="heights",
             friend="Omar", cousin="Diego", novel_fear="spiders"),
        dict(name="Liam Chen", surname="Chen", born=2001, city="Portland",
             job="teacher", employer="Lincoln High", fear="spiders",
             friend="Priya", cousin="Noah", novel_fear="heights"),
        dict(name="Aisha Khan", surname="Khan", born=1979, city="Austin",
             job="architect", employer="BuildCo", fear="flying",
             friend="Marco", cousin="Yusuf", novel_fear="dogs"),
        dict(name="Ben Okafor", surname="Okafor", born=1993, city="Seattle",
             job="chef", employer="Blue Fork", fear="deep water",
             friend="Hana", cousin="Tunde", novel_fear="crowds"),
        dict(name="Clara Voss", surname="Voss", born=1985, city="Boston",
             job="lawyer", employer="Hale & Ward", fear="dogs",
             friend="Ivan", cousin="Greta", novel_fear="needles"),
        dict(name="Nadia Petrov", surname="Petrov", born=1998, city="Chicago",
             job="pilot", employer="SkyLine Air", fear="crowds",
             friend="Sam", cousin="Dmitri", novel_fear="deep water"),
        dict(name="Theo Adams", surname="Adams", born=1990, city="Miami",
             job="dentist", employer="Bright Smiles", fear="needles",
             friend="Lena", cousin="Caleb", novel_fear="flying"),
    ]


def source_for(p: dict) -> str:
    # Multi-sentence source with TWO planted disambiguations that consolidation may
    # collapse: (S1b) an explicit "no middle name / Mark is a surname" clause, and
    # (S4) the who-fears/who-helps directionality.
    return (f"My name is {p['name']}. {p['surname']} is my surname, and I do not have a middle name. "
            f"I was born in {p['born']} and I live in {p['city']}. "
            f"I work as a {p['job']} at {p['employer']}. "
            f"I have a fear of {p['fear']}, and my friend {p['friend']} helps me cope with it. "
            f"My cousin {p['cousin']} lives nearby.")


def probes_for(p: dict) -> list[dict]:
    first = p["name"].split()[0]
    fr, fear = p["friend"], p["fear"]
    return [
        # role_swap (WASHABLE headline): flip who is afraid / who helps. Every content
        # word ({friend},{fear},{first}) is in the source -> high overlap.
        dict(family="role_swap", overlap=True, gold="mislabel",
             hypothesis=f"{fr} is afraid of {fear}, and {first} helps {fr} cope with it."),
        # role_swap_novlp (NEGATIVE CONTROL): same directional swap but the fear is a
        # word NOT in the source -> no lexical overlap on the payload term.
        dict(family="role_swap_novlp", overlap=False, gold="mislabel",
             hypothesis=f"{fr} is afraid of {p['novel_fear']}, and {first} helps {fr} cope with it."),
        # disambig_relabel (WASHABLE headline #2): the source EXPLICITLY says the person
        # has no middle name and {surname} is a surname. At N=0 that clause makes the
        # claim contradicted (caught). If consolidation drops the pedantic clause, the
        # surname word survives and "{surname} is the middle name" becomes bag-of-words
        # ENTAILED -> the archetypal wash. All hypothesis words are in source (overlap).
        dict(family="disambig_relabel", overlap=True, gold="mislabel",
             hypothesis=f"{first}'s middle name is {p['surname']}."),
        # entity_swap (CONTRAST): gross non-relational error, no source overlap on payload.
        dict(family="entity_swap", overlap=False, gold="mislabel",
             hypothesis=f"{first} was born in 2035 and lives in Tokyo."),
        # faithful (FP control): true restatements that must stay entailment across N.
        dict(family="faithful", overlap=True, gold="supported",
             hypothesis=f"{first} works as a {p['job']}."),
        dict(family="faithful", overlap=True, gold="supported",
             hypothesis=f"{first} is afraid of {fear}."),
    ]


# --------------------------------------------------------------------------- #
# Consolidation: drive the repo operator recursively, cache full trajectories.
# --------------------------------------------------------------------------- #
def consolidate_trajectory(llm, make_prompt, normalize, source: str, style: str,
                           max_n: int) -> list[str]:
    """Return [note_0=source, note_1, ..., note_max_n] using the repo operator."""
    traj = [source.strip()]
    cur = source.strip()
    for pass_idx in range(1, max_n + 1):
        raw = llm.generate(make_prompt(cur, pass_idx, style=style))
        note = normalize(raw)
        if not note:
            note = cur  # degenerate empty note -> carry forward (logged by caller)
        traj.append(note)
        cur = note
    return traj


def build_or_load_trajectories(styles: list[str], persona_list: list[dict],
                               max_n: int, cache_path: Path) -> dict:
    cache = {}
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    from src.memory.linked_view_system import (_OpenAILLM, _make_consolidation_prompt,
                                                _normalize_consolidated_note)
    llm = None
    dirty = False
    for p in persona_list:
        src = source_for(p)
        for style in styles:
            key = f"{p['name']}|{style}"
            if key in cache and len(cache[key]) >= max_n + 1:
                continue
            if llm is None:
                llm = _OpenAILLM(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
            print(f"  consolidating: {key} (N->{max_n}) ...", flush=True)
            traj = consolidate_trajectory(llm, _make_consolidation_prompt,
                                          _normalize_consolidated_note, src, style, max_n)
            cache[key] = traj
            dirty = True
    if dirty:
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    return cache


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Relation-blind kill-switch: recall vs consolidation depth.")
    ap.add_argument("--styles", nargs="+", default=STYLES)
    ap.add_argument("--ns", nargs="+", type=int, default=SWEEP_NS)
    ap.add_argument("--persona-limit", type=int, default=0, help="0 = all personas")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--smoke", action="store_true",
                    help="1 persona, 1 style, print every consolidated note (eyeball wash).")
    ap.add_argument("--cache", default=str(ROOT / "state" / "relblind_trajectories_v2_20260711.json"))
    ap.add_argument("--out", default=str(ROOT / "state" / "relblind_depth_sweep_v2_20260711.json"))
    args = ap.parse_args()

    styles = args.styles[:1] if args.smoke else args.styles
    plist = personas()[:1] if args.smoke else (personas()[:args.persona_limit] if args.persona_limit else personas())
    max_n = max(args.ns)

    print(f"[relblind] personas={len(plist)} styles={styles} Ns={args.ns} smoke={args.smoke}")
    traj = build_or_load_trajectories(styles, plist, max_n, Path(args.cache))

    if args.smoke:
        p = plist[0]; style = styles[0]
        t = traj[f"{p['name']}|{style}"]
        print("\n==== SMOKE: consolidation trajectory ====")
        print(f"persona={p['name']} style={style}\n")
        for n in args.ns:
            print(f"--- N={n} ---\n{t[n]}\n")
        print("==== probes (hypotheses) ====")
        for pr in probes_for(p):
            print(f"[{pr['family']:16s} overlap={pr['overlap']!s:5s} gold={pr['gold']:9s}] {pr['hypothesis']}")
        print("\nNote: eyeball whether S4 who-fears/who-helps direction survives each N.")
        return 0

    # ---- detection sweep ----
    from rq2_stage_extract import load_nli
    from safety_honest_metrics import clopper_pearson
    predict = load_nli(device=args.device)[0]

    # Build the full flat eval list: (style, N, persona, probe) with premises.
    rows = []
    for p in plist:
        prs = probes_for(p)
        for style in styles:
            t = traj[f"{p['name']}|{style}"]
            for n in args.ns:
                prem = t[n]
                for pr in prs:
                    rows.append(dict(style=style, n=n, persona=p["name"],
                                     family=pr["family"], overlap=pr["overlap"],
                                     gold=pr["gold"], premise=prem, hypothesis=pr["hypothesis"]))
    labels, eprobs = predict([r["premise"] for r in rows], [r["hypothesis"] for r in rows])
    for r, lab, ep in zip(rows, labels, eprobs):
        r["nli_label"] = lab
        r["entail_prob"] = round(float(ep), 3)

    # ---- aggregate: per (style, family, N) recall / false-SAFE / label dist ----
    agg = defaultdict(list)
    for r in rows:
        agg[(r["style"], r["family"], r["n"])].append(r)

    summary = {}
    for (style, fam, n), rs in sorted(agg.items()):
        gold = rs[0]["gold"]
        dist = {k: sum(1 for r in rs if r["nli_label"] == k)
                for k in ("entailment", "neutral", "contradiction")}
        entail = dist["entailment"]
        tot = len(rs)
        if gold == "supported":
            cp = clopper_pearson(entail, tot)  # want HIGH (detector keeps calling truth entailed)
            metric = {"kind": "entail_rate", **cp}
        else:
            caught = tot - entail
            cp = clopper_pearson(caught, tot)  # recall = NOT-entail
            metric = {"kind": "recall", **cp,
                      "false_safe_rate": round(entail / tot, 3) if tot else None}
        summary.setdefault(style, {}).setdefault(fam, {})[str(n)] = {
            "n": n, "total": tot, "label_dist": dist, "metric": metric}

    # ---- headline: recall(N=0) vs recall(N=max) per (style, mislabel family) + McNemar ----
    from math import isnan
    def mcnemar_p(b: int, c: int) -> float:
        # exact binomial 2-sided on discordant pairs (N=0 caught & Nmax missed vs opposite)
        from math import comb
        nd = b + c
        if nd == 0:
            return 1.0
        k = min(b, c)
        tail = sum(comb(nd, i) for i in range(0, k + 1)) / (2 ** nd)
        return min(1.0, 2 * tail)

    headline = {}
    n0, nmax = args.ns[0], args.ns[-1]
    for p in plist:
        prs = probes_for(p)
        for style in styles:
            t = traj[f"{p['name']}|{style}"]
    # McNemar needs paired items; rebuild per (style,family) pairing N0 vs Nmax across personas
    paired = defaultdict(lambda: {"b": 0, "c": 0})  # b: caught@N0 & missed@Nmax ; c: opposite
    per_item = defaultdict(dict)
    for r in rows:
        if r["gold"] != "mislabel":
            continue
        key = (r["style"], r["family"], r["persona"], r["hypothesis"])
        per_item[key][r["n"]] = (r["nli_label"] != "entailment")  # caught?
    for (style, fam, persona, hyp), byn in per_item.items():
        if n0 not in byn or nmax not in byn:
            continue
        c0, cm = byn[n0], byn[nmax]
        if c0 and not cm:
            paired[(style, fam)]["b"] += 1
        elif cm and not c0:
            paired[(style, fam)]["c"] += 1
    for (style, fam), bc in paired.items():
        headline.setdefault(style, {})[fam] = {
            "caught_N0_missed_Nmax": bc["b"], "missed_N0_caught_Nmax": bc["c"],
            "mcnemar_p": round(mcnemar_p(bc["b"], bc["c"]), 5),
            "n0": n0, "nmax": nmax}

    out = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
           "personas": len(plist), "styles": styles, "ns": args.ns,
           "detector": "vanilla_deberta_mnli",
           "summary": summary, "headline_mcnemar": headline,
           "note": "recall = P(NOT entailment | error); false_safe_rate = P(entailment | error). "
                   "Wash hypothesis: recall falls / false_safe rises with N for role_swap (overlap) "
                   "but NOT for role_swap_novlp (no-overlap) or entity_swap (gross)."}
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- console table ----
    print("\n==== recall / false-SAFE vs N ====")
    for style in styles:
        print(f"\n### style = {style}")
        for fam in ["role_swap", "role_swap_novlp", "disambig_relabel", "entity_swap", "faithful"]:
            if fam not in summary.get(style, {}):
                continue
            cells = []
            for n in args.ns:
                s = summary[style][fam].get(str(n))
                if not s:
                    cells.append(f"N{n}: -")
                    continue
                m = s["metric"]
                if m["kind"] == "recall":
                    cells.append(f"N{n}: rec={m['point']:.2f} fsafe={m['false_safe_rate']:.2f}")
                else:
                    cells.append(f"N{n}: entail={m['point']:.2f}")
            print(f"  {fam:16s} | " + "  ".join(cells))
        for fam, h in headline.get(style, {}).items():
            print(f"    McNemar[{fam}] N{h['n0']}->N{h['nmax']}: "
                  f"caught->missed={h['caught_N0_missed_Nmax']} "
                  f"missed->caught={h['missed_N0_caught_Nmax']} p={h['mcnemar_p']}")
    print("\nsaved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
