#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GROUND-TRUTH memory-op attribution benchmark (the path to a validated result).

The natural-HaluMem decomposition can't be validated (no which-op ground truth) and
its consolidate/retrieve split is a restore-priority tie-break. This harness MANUFACTURES
ground truth on REAL HaluMem traces + forces CONFIDENT-WRONG answers (the regime the
clean-oracle abstention test didn't cover), so we can MEASURE whether the restore
attributor recovers the KNOWN culprit op and beats the trace-only LLM-judge.

Per real (persona, answerable QA, evidence, gold):
  - synthesize a DISTRACTOR memory line asserting a plausible WRONG answer (LLM) so the
    agent answers confidently-wrong (not "I don't know") when the true evidence is absent.
  - inject exactly ONE known culprit op:
      write_drop      : evidence absent from BOTH the raw dialogue (write-check turns) and the store.
      consolidate_drop: evidence in the raw dialogue but NOT in the store (dropped in summarisation).
      retrieve_miss   : evidence IN the store but base retrieval excludes it.
  - run the restore attributor (write_ok via LLM over the (edited) dialogue; rr=best-effort
    store-only retrieval; rc=re-insert true evidence) + random/distractor controls + LLM-judge.
Ground truth = the injected op. Report per-op localization accuracy, confident-wrong subset,
restore-vs-judge, controls. This is the truth-validated result the natural pilot could not give.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from datetime import datetime
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "core"))
sys.path.insert(0, str(ROOT / "scripts" / "run"))
TIERMEM = ROOT.parent / "tiermem_upstream"
sys.path.insert(0, str(TIERMEM))
HALU = ROOT / "benchmarks" / "halumem" / "official_repo" / "data" / "HaluMem-Medium.jsonl"

from run_memop_halumem import (toks, note_lines, retrieve, answer, judge_correct,
                               build_memory, gather_questions, _cand_turns)


def all_turn_texts(user, sess_lim, drop_evidence=None):
    """Raw dialogue turn texts; optionally drop turns that lexically state the evidence (= write-drop)."""
    out = []
    for s in user["sessions"][:sess_lim]:
        for t in s.get("dialogue", []):
            c = t.get("content", "")
            if drop_evidence:
                ov = max((len(toks(e) & toks(c)) / max(1, len(toks(e))) for e in drop_evidence), default=0.0)
                if ov >= 0.5:
                    continue  # remove the turn that states the fact -> simulate never-written
            out.append(c)
    return out


def written_llm_turns(llm, turns, evidence) -> bool:
    if not evidence:
        return True
    q = set().union(*[toks(e) for e in evidence])
    cand = sorted(turns, key=lambda c: len(q & toks(c)), reverse=True)[:12]
    cand = [c for c in cand if len(q & toks(c)) > 0]
    if not cand:
        return False
    ctx = "\n".join(f"- {c}" for c in cand)
    out = llm.generate(
        f"Conversation excerpts:\n{ctx}\n\nIs the following fact STATED or CLEARLY IMPLIED anywhere "
        f"in these excerpts? Reply exactly one word: yes or no.\nFact: {'; '.join(evidence)}\nAnswer:").strip().lower()
    return out.startswith("y")


def store_supports(llm, store_lines, evidence) -> bool:
    """STRICT store-membership: do the notes support the SPECIFIC fact (its value), not just the topic,
    and NOT a different/conflicting value? Rejects the injected distractor (which asserts a wrong value)."""
    if not evidence:
        return False
    q = set().union(*[toks(e) for e in evidence])
    cand = [l for l in sorted(store_lines, key=lambda l: len(q & toks(l)), reverse=True)[:10] if len(q & toks(l)) > 0]
    if not cand:
        return False
    ctx = "\n".join(f"- {c}" for c in cand)
    out = llm.generate(
        f"Memory notes:\n{ctx}\n\nDo these notes SUPPORT the following specific fact (the exact value/claim, "
        f"not merely the topic)? Answer 'no' if the notes only mention the topic or assert a DIFFERENT/conflicting "
        f"value. Reply exactly one word: yes or no.\nFact: {'; '.join(evidence)}\nAnswer:").strip().lower()
    return out.startswith("y")


def make_distractor(llm, question, gold) -> str:
    return llm.generate(
        f"Write ONE short first-person memory note (a single line, as if stored from a past chat) that would "
        f"make someone answer the question with a PLAUSIBLE but WRONG value. The TRUE answer is '{gold}' — your "
        f"note MUST assert a different, wrong value, and must NOT contain the true value.\n"
        f"Question: {question}\nNote:").strip().strip("-* ").splitlines()[0][:200]


def evidence_line(evidence):
    return "; ".join(evidence)


def paraphrase_evidence(llm, evidence) -> str:
    """A consolidation-style paraphrase of the evidence (what a real store would hold), NOT verbatim,
    so the store-membership check is tested realistically (not on the injected verbatim string)."""
    return llm.generate(
        f"Rewrite this fact as ONE short third-person memory note in different words (same meaning, "
        f"do not copy the wording):\nFact: {'; '.join(evidence)}\nNote:").strip().strip("-* ").splitlines()[0][:200]


def build_state(llm, mem_lines, ev, distractor, culprit):
    """Return (store_lines, force_retrieve_miss). store excludes the real evidence; retrieve_miss
    injects a PARAPHRASED (realistic, not verbatim) evidence note so membership isn't trivially lexical."""
    base = [l for l in mem_lines if max((len(toks(e) & toks(l)) / max(1, len(toks(e))) for e in ev), default=0) < 0.5]
    store = base + [distractor]
    if culprit == "retrieve_miss":
        para = paraphrase_evidence(llm, ev)   # evidence (paraphrased) IS in store; retrieval forced to miss it
        return store + [para], para
    return store, None   # write_drop / consolidate_drop: evidence NOT in store


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=6)
    ap.add_argument("--sessions", type=int, default=12)
    ap.add_argument("--max-q-per-user", type=int, default=12)
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--cache", default=str(ROOT / "state" / "memop_halumem_notes_20260712.json"))
    ap.add_argument("--out", default=str(ROOT / "state" / "memop_groundtruth_20260712.json"))
    args = ap.parse_args()

    from src.memory.linked_view_system import _OpenAILLM, _normalize_consolidated_note
    llm = _OpenAILLM(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    norm = _normalize_consolidated_note
    users = [json.loads(l) for l in HALU.read_text().splitlines()[:args.users]]
    OPS = ["write_drop", "consolidate_drop", "retrieve_miss"]

    items = []
    for u in users:
        notes = build_memory(llm, norm, Path(args.cache), u, args.sessions)
        mem_lines = [l for n in notes for l in note_lines(n)]
        qs = gather_questions(u, args.sessions, args.max_q_per_user)
        print(f"user {u['uuid'][:8]} q={len(qs)}", flush=True)
        for q in qs:
            ev = q["evidence"]
            if not ev:
                continue
            distractor = make_distractor(llm, q["question"], q["gold"])
            for culprit in OPS:
                store, ev_store_line = build_state(llm, mem_lines, ev, distractor, culprit)
                base_ctx = retrieve(store, q["question"], args.k)
                if ev_store_line is not None:   # retrieve-miss: force the (paraphrased) evidence out of context
                    base_ctx = [c for c in base_ctx if c != ev_store_line][:args.k]
                ans = answer(llm, q["question"], base_ctx)
                if judge_correct(llm, q["question"], q["gold"], ans):
                    continue  # injection didn't induce a failure; skip
                confident_wrong = ("i don't know" not in ans.lower() and "unknown" not in ans.lower()
                                   and "not" not in ans.lower()[:8])
                # ---- PROVENANCE MEMBERSHIP checks (robust to the distractor; the primary signal) ----
                # write_ok: is the fact stated in the (edited-for-write-drop) raw dialogue?
                turns = all_turn_texts(u, args.sessions, drop_evidence=ev if culprit == "write_drop" else None)
                write_ok = written_llm_turns(llm, turns, ev)
                # store_has: STRICT membership — does the store support the SPECIFIC value (rejects the distractor)?
                store_has = store_supports(llm, store, ev)
                best_ov = round(max((max((len(toks(e) & toks(l)) / max(1, len(toks(e))) for e in ev), default=0) for l in store), default=0), 2)
                # ---- restore signals (reported as confirmation; unreliable under a distractor) ----
                rc_ok = judge_correct(llm, q["question"], q["gold"], answer(llm, q["question"], [evidence_line(ev)] + base_ctx[:args.k - 1]))
                rr_ok = (judge_correct(llm, q["question"], q["gold"],
                                       answer(llm, q["question"], ([ev_store_line] + base_ctx)[:args.k]))
                         if ev_store_line is not None else False)
                import hashlib
                ridx = int(hashlib.md5(q["question"].encode()).hexdigest(), 16) % max(1, len(store))
                rand_ok = judge_correct(llm, q["question"], q["gold"], answer(llm, q["question"], [store[ridx]] + base_ctx[:args.k - 1]))
                # ---- MEMBERSHIP-based attribution (primary): where does the evidence first go missing? ----
                if not write_ok:
                    attributed = "write_drop"          # fact never written
                elif store_has:
                    attributed = "retrieve_miss"       # fact in store, retrieval missed it
                else:
                    attributed = "consolidate_drop"    # written but not in store -> dropped in consolidation
                # trace-only judge (sees base_ctx + answer, NOT the dropped evidence)
                jr = llm.generate(
                    f"A memory agent (write -> consolidate/summarize -> retrieve -> answer) answered WRONG. "
                    f"The needed fact may have been never written, dropped in consolidation, or not retrieved. "
                    f"Which SINGLE step is at fault? Reply one word: write, consolidate, or retrieve.\n"
                    f"Question: {q['question']}\nGold: {q['gold']}\nRetrieved notes:\n" + "\n".join(base_ctx) +
                    f"\nAgent answer: {ans}\nFaulty step:").strip().lower()
                judge = next((o for o in ("consolidate", "retrieve", "write") if o in jr), "unknown")
                judge_op = {"write": "write_drop", "consolidate": "consolidate_drop", "retrieve": "retrieve_miss"}.get(judge, "unknown")
                items.append(dict(uuid=u["uuid"][:8], q=q["question"], gold=q["gold"], injected=culprit,
                                  answer=ans, confident_wrong=confident_wrong, write_ok=write_ok, store_has=store_has,
                                  rr_ok=rr_ok, rc_ok=rc_ok, rand_ok=rand_ok, best_ov=best_ov,
                                  attributed=attributed, judge=judge_op,
                                  attr_correct=(attributed == culprit), judge_correct_=(judge_op == culprit)))
                print(f"  inj={culprit:16s} cw={confident_wrong!s:5s} wok={write_ok!s:5s} shas={store_has!s:5s} "
                      f"attr={attributed:16s} judge={judge_op:12s} {'OK' if attributed==culprit else 'XX'}", flush=True)

    n = len(items)
    cw = [it for it in items if it["confident_wrong"]]
    def acc(sel, field): return round(sum(1 for it in sel if it[field]) / len(sel), 3) if sel else None
    per_op = {op: {"n": sum(1 for it in items if it["injected"] == op),
                   "attr_acc": acc([it for it in items if it["injected"] == op], "attr_correct"),
                   "judge_acc": acc([it for it in items if it["injected"] == op], "judge_correct_")}
              for op in OPS}
    out = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "n_injected_failures": n, "n_confident_wrong": len(cw),
           "attributor_localization_acc": acc(items, "attr_correct"),
           "attributor_acc_on_confident_wrong": acc(cw, "attr_correct"),
           "llm_judge_localization_acc": acc(items, "judge_correct_"),
           "llm_judge_acc_on_confident_wrong": acc(cw, "judge_correct_"),
           "per_op": per_op,
           "confusion_attributed_by_injected": {op: dict(Counter(it["attributed"] for it in items if it["injected"] == op)) for op in OPS},
           "nonspecific_rate": round(sum(1 for it in items if it["attributed"] == "nonspecific") / max(1, n), 3),
           "items": items}
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print("\n==== GROUND-TRUTH memory-op attribution (known culprit on real traces) ====")
    print(f"injected failures={n}  confident-wrong={len(cw)}")
    print(f"ATTRIBUTOR localization acc: all={out['attributor_localization_acc']}  confident-wrong={out['attributor_acc_on_confident_wrong']}")
    print(f"LLM-JUDGE   localization acc: all={out['llm_judge_localization_acc']}  confident-wrong={out['llm_judge_acc_on_confident_wrong']}")
    print(f"per-op: {json.dumps(per_op)}")
    print(f"confusion: {out['confusion_attributed_by_injected']}")
    print("saved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
