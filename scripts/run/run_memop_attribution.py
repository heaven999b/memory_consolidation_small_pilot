#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Memory-op counterfactual attribution MINIMAL kill-switch (candidate gap-1).

Question: when a memory-augmented agent answers WRONG, can counterfactual
"restore-one-op" replay localize WHICH memory OPERATION caused it
(write-drop / consolidate-drop / retrieve-miss) — and does it beat the cheap
LLM-judge attribution baseline (CAR reports LLM-judge step-attribution ~14%)?

Pipeline (per query needing key fact F):  write(source) -> consolidate(C^1)
  -> retrieve(top-k lines) -> answer(gpt).  Correct = gold token in answer.

Held-out ORACLE: inject exactly ONE culprit op per item (we KNOW the culprit):
  write_drop     : F omitted from the source.
  consolidate_drop: F in source, consolidation told to omit health details.
  retrieve_miss  : F survives consolidation, retrieval returns non-F lines.

ATTRIBUTOR (counterfactual restore): for each op, apply its restore intervention,
re-run downstream, re-answer. Attributed culprit = the op whose restore flips the
answer wrong->correct. NON-tautological control: restoring a RANDOM non-culprit op
must NOT fix the answer (drives the OUTCOME = correctness, not the op's own value).

POSITIVE (worth pursuing) = localization accuracy high AND clearly > LLM-judge
baseline AND random-op restore ~0. If LLM-judge already localizes as well, the
counterfactual primitive adds nothing over CAR-in-a-new-setting -> not worth it.

Live gpt-4.1-mini (temp 0). Cache -> re-run cheap.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "core"))
TIERMEM = ROOT.parent / "tiermem_upstream"
sys.path.insert(0, str(TIERMEM))

OPS = ["write", "consolidate", "retrieve"]


def personas() -> list[dict]:
    base = [
        dict(name="Martin", city="Austin", job="data analyst", pet="two cats",
             hobby="cello", key="allergic to penicillin", q="What is Martin allergic to?", gold="penicillin"),
        dict(name="Sofia", city="Seattle", job="nurse", pet="a beagle",
             hobby="pottery", key="allergic to sulfa drugs", q="What is Sofia allergic to?", gold="sulfa"),
        dict(name="Liam", city="Chicago", job="teacher", pet="a parrot",
             hobby="climbing", key="allergic to aspirin", q="What is Liam allergic to?", gold="aspirin"),
        dict(name="Aisha", city="Dallas", job="architect", pet="a turtle",
             hobby="painting", key="allergic to latex", q="What is Aisha allergic to?", gold="latex"),
        dict(name="Ben", city="Atlanta", job="chef", pet="a husky",
             hobby="chess", key="allergic to shellfish", q="What is Ben allergic to?", gold="shellfish"),
        dict(name="Clara", city="Denver", job="lawyer", pet="a corgi",
             hobby="cycling", key="allergic to ibuprofen", q="What is Clara allergic to?", gold="ibuprofen"),
    ]
    return base


def source_lines(p: dict, drop_key: bool) -> list[str]:
    n = p["name"]
    lines = [f"{n} lives in {p['city']}.",
             f"{n} works as a {p['job']}.",
             f"{n} has {p['pet']}.",
             f"{n} enjoys {p['hobby']}."]
    if not drop_key:
        lines.insert(2, f"{n} is {p['key']}.")
    return lines


def consolidate_prompt(source: str, drop_health: bool) -> str:
    extra = ("\n4. Omit any medical or health details to keep the note lifestyle-focused."
             if drop_health else "")
    return (f"Consolidate the SOURCE into a compact memory note.\n"
            f"Rules:\n1. Preserve concrete facts.\n2. Use only the SOURCE.\n"
            f"3. Output 3-6 short bullet lines and nothing else.{extra}\n\nSOURCE:\n{source}\n\nConsolidated note:")


def retrieve(note: str, query: str, k: int, force_miss: bool) -> list[str]:
    lines = [l.strip("-* ").strip() for l in note.splitlines() if l.strip()]
    qwords = set(re.findall(r"[a-z]+", query.lower()))
    scored = sorted(lines, key=lambda l: len(qwords & set(re.findall(r"[a-z]+", l.lower()))), reverse=True)
    if force_miss:
        # return the LEAST relevant lines (guarantee the key line, if present, is excluded)
        return scored[::-1][:k]
    return scored[:k]


def answer(llm, query: str, context: list[str]) -> str:
    ctx = "\n".join(f"- {c}" for c in context)
    prompt = (f"Answer the question using ONLY the memory notes. If the notes do not contain the answer, "
              f"say 'I don't know'.\n\nMemory notes:\n{ctx}\n\nQuestion: {query}\nAnswer:")
    return llm.generate(prompt).strip()


def is_correct(ans: str, gold: str) -> bool:
    return gold.lower() in ans.lower()


def run_pipeline(llm, normalize, p, culprit, k=2, restore=None):
    """Run write->consolidate->retrieve->answer, applying one injected culprit and
    optionally one restore intervention. Returns (answer, correct, note, retrieved)."""
    n = p["name"]; keyline = f"{n} is {p['key']}."
    drop_write = (culprit == "write") and (restore != "write")
    drop_health = (culprit == "consolidate") and (restore != "consolidate")
    force_miss = (culprit == "retrieve") and (restore != "retrieve")

    src_lines = source_lines(p, drop_key=drop_write)
    src = " ".join(src_lines)
    note = normalize(llm.generate(consolidate_prompt(src, drop_health))) or src
    # restore-consolidate: inject the key line back into the note
    if culprit == "consolidate" and restore == "consolidate" and p["gold"].lower() not in note.lower():
        note = note + f"\n- {keyline}"
    retrieved = retrieve(note, p["q"], k, force_miss)
    # restore-retrieve: force the key line into context
    if culprit == "retrieve" and restore == "retrieve":
        retrieved = [keyline] + retrieved[:k - 1]
    ans = answer(llm, p["q"], retrieved)
    return ans, is_correct(ans, p["gold"]), note, retrieved


def llm_judge_attribute(llm, p, note, retrieved, ans) -> str:
    prompt = (f"A memory agent answered a question wrong. The pipeline has three operations: "
              f"write (store facts), consolidate (summarize stored facts), retrieve (pick notes for the query). "
              f"Given the trace, which SINGLE operation most likely caused the wrong answer? "
              f"Answer with exactly one word: write, consolidate, or retrieve.\n\n"
              f"Question: {p['q']}\nGold answer: {p['gold']}\n"
              f"Consolidated note:\n{note}\n\nRetrieved for the query:\n" + "\n".join(retrieved) +
              f"\n\nAgent answer: {ans}\n\nCulprit operation:")
    out = llm.generate(prompt).strip().lower()
    for op in OPS:
        if op in out:
            return op
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "state" / "memop_attribution_result_20260712.json"))
    ap.add_argument("--k", type=int, default=2)
    args = ap.parse_args()

    from src.memory.linked_view_system import _OpenAILLM, _normalize_consolidated_note
    llm = _OpenAILLM(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    norm = _normalize_consolidated_note

    items = []
    for p in personas():
        for culprit in OPS:
            # baseline failed run (culprit active, no restore)
            ans, correct, note, retr = run_pipeline(llm, norm, p, culprit, k=args.k, restore=None)
            # counterfactual attributor: which restore fixes it?
            fixed_by = []
            for op in OPS:
                _, c2, _, _ = run_pipeline(llm, norm, p, culprit, k=args.k, restore=op)
                if c2:
                    fixed_by.append(op)
            attributed = fixed_by[0] if len(fixed_by) == 1 else ("ambiguous:" + ",".join(fixed_by) if fixed_by else "none")
            judge = llm_judge_attribute(llm, p, note, retr, ans)
            items.append(dict(persona=p["name"], injected_culprit=culprit, baseline_correct=correct,
                              answer=ans, attributed=attributed, fixed_by=fixed_by, llm_judge=judge))
            print(f"  {p['name']:7s} culprit={culprit:11s} baseline_wrong={not correct} "
                  f"attr={attributed:14s} judge={judge}", flush=True)

    # metrics
    valid = [it for it in items if not it["baseline_correct"]]  # only items that actually failed
    def acc(field):
        return round(sum(1 for it in valid if it[field] == it["injected_culprit"]) / len(valid), 3) if valid else None
    cf_acc = acc("attributed"); judge_acc = acc("llm_judge")
    # random-op control: fraction where a NON-culprit restore also fixed it
    nonculprit_fix = sum(1 for it in valid for op in it["fixed_by"] if op != it["injected_culprit"])
    total_nonculprit_trials = len(valid) * (len(OPS) - 1)
    ctrl = round(nonculprit_fix / total_nonculprit_trials, 3) if total_nonculprit_trials else None

    out = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "n_items": len(items), "n_failed": len(valid),
           "counterfactual_localization_acc": cf_acc,
           "llm_judge_localization_acc": judge_acc,
           "random_op_restore_fix_rate(should~0)": ctrl,
           "items": items,
           "note": "POSITIVE if counterfactual_acc high AND >> llm_judge_acc AND random-op ~0. "
                   "If llm_judge_acc ~= counterfactual_acc, the primitive adds nothing over CAR-in-new-setting."}
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print("\n==== Memory-op attribution ====")
    print(f"failed items (baseline wrong): {len(valid)}/{len(items)}")
    print(f"counterfactual localization acc : {cf_acc}")
    print(f"LLM-judge   localization acc    : {judge_acc}")
    print(f"random-op restore fix rate (~0) : {ctrl}")
    print("saved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
