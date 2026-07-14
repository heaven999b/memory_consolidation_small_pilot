#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Memory-op attribution on REAL HaluMem failures (gap-1 differentiating kill-switch).

Tests the two claims that separate this from Causal Agent Replay (which attributes
to agent STEPS, is memory-agnostic, and cannot see evidence that consolidation dropped):
  (1) FAILURE-BUDGET: across NATURAL HaluMem failures, which memory op dominates
      (write-drop vs consolidate-drop vs retrieve-miss)? Hypothesis: consolidate.
  (2) RESTORE > JUDGE: the restore-one-op intervention (re-insert the provenance
      evidence a consolidation dropped) localizes culprits an LLM-judge (which only
      sees the trace, NOT the dropped evidence) misses.

Pipeline per user: write session dialogue -> per-session C^1 consolidation -> the
consolidated notes are the memory -> per answerable question, retrieve top-k lines
-> answer. Natural failure = gold answer not recovered.

Provenance = HaluMem question["evidence"][*]["memory_content"] (the gold supporting
memory). Op attribution via restore:
  restore-consolidate: add the evidence line to the memory (undo a consolidation drop) -> re-answer.
  restore-retrieve:    force the evidence line into the retrieved context -> re-answer.
  write assumed intact (evidence is drawn from the transcript by construction).
Attributed culprit = the op whose restore flips wrong->correct. Non-tautological:
the restore targets the OUTCOME (answer correctness), and a random-line restore control
must NOT fix it.

Live gpt-4.1-mini. Consolidation cache -> re-run cheap.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "core"))
TIERMEM = ROOT.parent / "tiermem_upstream"
sys.path.insert(0, str(TIERMEM))
HALU = ROOT / "benchmarks" / "halumem" / "official_repo" / "data" / "HaluMem-Medium.jsonl"


STOP = {"the", "and", "not", "for", "was", "her", "his", "she", "him", "are", "has",
        "have", "with", "that", "this", "what", "which", "user", "unknown", "provided",
        "did", "does", "how", "why", "who", "when", "where"}


def toks(s: str) -> set:
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def _cand_turns(user, sess_lim, evidence, topn):
    """Lexically prefilter dialogue turns most relevant to the evidence."""
    cand = []
    for s in user["sessions"][:sess_lim]:
        for t in s.get("dialogue", []):
            c = t.get("content", "")
            ov = max((len(toks(e) & toks(c)) / max(1, len(toks(e))) for e in evidence), default=0.0)
            if ov >= 0.2:
                cand.append((ov, c))
    return [c for _, c in sorted(cand, reverse=True)[:topn]]


def written_llm(llm, user, sess_lim, evidence) -> bool:
    """WRITE check (LLM semantic): is the gold evidence fact STATED or CLEARLY IMPLIED by the user
    anywhere in the conversation? Robust to paraphrase + multi-turn composite facts, unlike the
    lexical gate (too loose) or single-turn NLI (too strict, mislabels stated facts as write-drops)."""
    if not evidence:
        return True
    cand = _cand_turns(user, sess_lim, evidence, 12)
    if not cand:
        return False
    ctx = "\n".join(f"- {c}" for c in cand)
    fact = "; ".join(evidence)
    out = llm.generate(
        f"Conversation excerpts (user + assistant turns):\n{ctx}\n\n"
        f"Is the following fact STATED or CLEARLY IMPLIED anywhere in these excerpts? "
        f"Reply exactly one word: yes or no.\nFact: {fact}\nAnswer:").strip().lower()
    return out.startswith("y")


def consolidate_prompt(source: str) -> str:
    return (f"Consolidate the SOURCE conversation into a compact memory note for later question answering.\n"
            f"Rules:\n1. Preserve concrete names, dates, numbers, facts, preferences, and updates.\n"
            f"2. Use only the SOURCE.\n3. Output 4-8 short bullet lines and nothing else.\n\n"
            f"SOURCE:\n{source}\n\nConsolidated note:")


def note_lines(note: str) -> list[str]:
    return [l.strip("-*• ").strip() for l in note.splitlines() if l.strip()]


def retrieve(lines: list[str], query: str, k: int) -> list[str]:
    q = toks(query)
    return sorted(lines, key=lambda l: len(q & toks(l)), reverse=True)[:k]


def answer(llm, query: str, ctx: list[str]) -> str:
    c = "\n".join(f"- {x}" for x in ctx)
    return llm.generate(
        f"Answer the question using ONLY the memory notes. If the notes do not contain the answer, "
        f"say 'Unknown'.\n\nMemory notes:\n{c}\n\nQuestion: {query}\nAnswer:").strip()


FACT_TYPES = {"Basic Fact Recall", "Dynamic Update", "Multi-hop Inference", "Generalization & Application"}


def judge_correct(llm, question: str, gold: str, ans: str) -> bool:
    out = llm.generate(
        f"Judge whether the ANSWER is consistent with the GOLD answer to the question "
        f"(same fact/value; phrasing may differ; 'Unknown' is wrong if GOLD has a value). "
        f"Reply exactly one word: yes or no.\n\n"
        f"Question: {question}\nGOLD: {gold}\nANSWER: {ans}\nConsistent:").strip().lower()
    return out.startswith("y")


def build_memory(llm, norm, cache: Path, user, sess_lim) -> dict:
    key = user["uuid"]
    data = json.loads(cache.read_text()) if cache.exists() else {}
    if key in data:
        return data[key]
    notes = []
    for s in user["sessions"][:sess_lim]:
        dlg = " ".join(f'{t["role"]}: {t["content"]}' for t in s.get("dialogue", []))
        if not dlg.strip():
            continue
        note = norm(llm.generate(consolidate_prompt(dlg))) or dlg
        notes.append(note)
    data[key] = notes
    cache.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return notes


def gather_questions(user, sess_lim, max_q):
    qs = []
    for s in user["sessions"][:sess_lim]:
        for q in s.get("questions", []):
            ev = q.get("evidence") or []
            if (q.get("question_type") in FACT_TYPES and ev and q.get("answer")
                    and "unknown" not in q["answer"].lower()):
                qs.append(dict(question=q["question"], gold=q["answer"], qtype=q["question_type"],
                               evidence=[e["memory_content"] for e in ev if e.get("memory_content")]))
            if len(qs) >= max_q:
                return qs
    return qs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=3)
    ap.add_argument("--sessions", type=int, default=12)
    ap.add_argument("--max-q-per-user", type=int, default=25)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--cache", default=str(ROOT / "state" / "memop_halumem_notes_20260712.json"))
    ap.add_argument("--out", default=str(ROOT / "state" / "memop_halumem_result_20260712.json"))
    args = ap.parse_args()

    from src.memory.linked_view_system import _OpenAILLM, _normalize_consolidated_note
    llm = _OpenAILLM(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    norm = _normalize_consolidated_note
    from rq2_stage_extract import load_nli
    nli = load_nli(device=args.device)[0]  # DeBERTa-MNLI (CPU): 2nd, cross-family detector for write-check + correctness
    users = [json.loads(l) for l in HALU.read_text().splitlines()[:args.users]]

    items = []
    for u in users:
        notes = build_memory(llm, norm, Path(args.cache), u, args.sessions)
        mem_lines = [l for n in notes for l in note_lines(n)]
        qs = gather_questions(u, args.sessions, args.max_q_per_user)
        print(f"user {u['uuid'][:8]} mem_lines={len(mem_lines)} answerable_q={len(qs)}", flush=True)
        for qi, q in enumerate(qs):
            ev_lines = q["evidence"]
            distractor_ev = qs[(qi + 1) % len(qs)]["evidence"] if len(qs) > 1 else []
            base_ctx = retrieve(mem_lines, q["question"], args.k)
            ans = answer(llm, q["question"], base_ctx)
            ok = judge_correct(llm, q["question"], q["gold"], ans)
            nli_ok = nli([ans], [q["gold"]])[0][0] == "entailment"  # 2nd, cross-family correctness detector
            rec = dict(uuid=u["uuid"][:8], question=q["question"], gold=q["gold"], qtype=q.get("qtype"),
                       evidence=ev_lines, base_answer=ans, base_correct=ok, base_nli_correct=nli_ok)
            if not ok:
                # (1) WRITE branch (LLM semantic): is the fact stated/implied anywhere in the conversation?
                write_ok = written_llm(llm, u, args.sessions, ev_lines)
                # best store line = ORACLE retrieval from the EXISTING store (NO lexical gate; answer decides)
                store_match, best = None, 0.0
                for l in mem_lines:
                    ov = max((len(toks(e) & toks(l)) / max(1, len(toks(e))) for e in ev_lines), default=0.0)
                    if ov > best:
                        best, store_match = ov, l
                # (2) restore-RETRIEVE: best-effort retrieval from the EXISTING store (no injection, no threshold).
                # rr_ok is decided by whether the best store line actually answers -> a real counterfactual.
                rr_ctx = ([store_match] + [c for c in base_ctx if c != store_match])[:args.k] if store_match else base_ctx
                rr_ok = judge_correct(llm, q["question"], q["gold"], answer(llm, q["question"], rr_ctx))
                # restore-CONSOLIDATE: re-insert the TRUE evidence into the store, then retrieve.
                rc_ok = judge_correct(llm, q["question"], q["gold"],
                                      answer(llm, q["question"], retrieve(mem_lines + ev_lines, q["question"], args.k)))
                # (3) controls: random-line + DISTRACTOR-evidence (gold evidence of a DIFFERENT question).
                import hashlib
                ridx = int(hashlib.md5(q["question"].encode()).hexdigest(), 16) % max(1, len(mem_lines))
                rand_ok = judge_correct(llm, q["question"], q["gold"],
                                        answer(llm, q["question"], [mem_lines[ridx]] + base_ctx[:args.k - 1]))
                dist_ok = (judge_correct(llm, q["question"], q["gold"],
                                         answer(llm, q["question"], retrieve(mem_lines + distractor_ev, q["question"], args.k)))
                           if distractor_ev else False)
                in_memory = best >= 0.6  # kept only for threshold-sensitivity reporting
                # attribution (write first; specificity controls; then real rr/rc counterfactual):
                if not write_ok:
                    culprit = "write"                       # answer never coherently written -> not consolidation's fault
                elif rand_ok or dist_ok:
                    culprit = "nonspecific"                 # any/wrong evidence helps -> not causally specific
                elif rr_ok:
                    culprit = "retrieve"                    # evidence recoverable from existing store; retrieval missed it
                elif rc_ok:
                    culprit = "consolidate"                 # only re-inserting the TRUE evidence fixes -> consolidation dropped it
                else:
                    culprit = "unresolved"                  # answer-synthesis / multi-op / missing
                # COMPETENT trace-only judge baseline (told consolidation may have dropped the fact -> can say consolidate)
                jr = llm.generate(
                    f"A memory agent (pipeline: write -> consolidate/summarize memories -> retrieve -> answer) answered WRONG. "
                    f"The needed fact may have been DROPPED during consolidation/summarization, or it may be stored but not retrieved, "
                    f"or never written. Based on the trace, which SINGLE operation is most at fault? "
                    f"Reply one word: write, consolidate, or retrieve.\n"
                    f"Question: {q['question']}\nGold: {q['gold']}\nRetrieved notes shown to the agent:\n" +
                    "\n".join(base_ctx) + f"\nAgent answer: {ans}\nMost likely faulty operation:").strip().lower()
                judge = next((o for o in ("consolidate", "retrieve", "write") if o in jr), "unknown")
                rec.update(write_ok=write_ok, evidence_in_memory=in_memory, store_overlap=round(best, 3),
                           restore_consolidate_ok=rc_ok, restore_retrieve_ok=rr_ok,
                           random_restore_ok=rand_ok, distractor_restore_ok=dist_ok,
                           attributed=culprit, llm_judge=judge)
                print(f"  FAIL write={write_ok!s:5s} ov={best:.2f} rr={rr_ok!s:5s} rc={rc_ok!s:5s} "
                      f"rand={rand_ok!s:5s} dist={dist_ok!s:5s} attr={culprit:11s} judge={judge:11s} q='{q['question'][:34]}'", flush=True)
            items.append(rec)

    fails = [it for it in items if not it["base_correct"]]
    from collections import Counter
    nf = len(fails)
    budget = Counter(it.get("attributed") for it in fails)
    # well-posed subset: directly-stated-fact question types (op-attribution is meaningful there)
    FACT = {"Basic Fact Recall", "Dynamic Update"}
    fact_fails = [it for it in fails if it.get("qtype") in FACT]
    fact_budget = Counter(it.get("attributed") for it in fact_fails)
    # base failure rate by qtype (diagnoses whether the pipeline itself is the failure source)
    fail_rate_by_qtype = {}
    for qt in set(it.get("qtype") for it in items):
        tot = [it for it in items if it.get("qtype") == qt]
        fail_rate_by_qtype[qt] = f"{sum(1 for it in tot if not it['base_correct'])}/{len(tot)}"
    cons_fails = [it for it in fails if it.get("attributed") == "consolidate"]
    clean = [it for it in fails if it.get("attributed") in ("consolidate", "retrieve")]
    # honest headline: consolidate as share of ALL failures (not of the curated clean subset)
    cons_share_all = round(len(cons_fails) / nf, 3) if nf else None
    cons_share_clean = round(len(cons_fails) / len(clean), 3) if clean else None
    # threshold-sensitivity: how many consolidate culprits sit in the fragile 0.5-0.6 store-overlap band
    cons_borderline = sum(1 for it in cons_fails if 0.5 <= it.get("store_overlap", 0) < 0.6)
    disagree = sum(1 for it in fails if it.get("restore_consolidate_ok") != it.get("restore_retrieve_ok"))
    # controls: distractor-evidence must NOT fix consolidate culprits (gold-text non-triviality)
    dist_fix_on_cons = sum(1 for it in cons_fails if it.get("distractor_restore_ok"))
    # C3: competent trace-only judge recall on consolidate culprits + its overall label rate
    judge_cons = sum(1 for it in cons_fails if it["llm_judge"] == "consolidate")
    judge_dist = Counter(it["llm_judge"] for it in fails)
    # 2nd cross-family detector agreement: gpt-judge vs NLI on base correctness (single-detector red-line check)
    both = [it for it in items if "base_nli_correct" in it]
    gpt_nli_agree = sum(1 for it in both if bool(it["base_correct"]) == bool(it["base_nli_correct"]))
    nli_confirmed_fail = sum(1 for it in fails if not it.get("base_nli_correct", True))
    out = {"generated_at": datetime.now().isoformat(timespec="seconds"),
           "users": args.users, "sessions": args.sessions,
           "n_questions": len(items), "n_fail": nf,
           "failure_budget_of_ALL_failures": {k: f"{v} ({round(v/nf,3)})" for k, v in budget.items()},
           "fact_types_only_budget": {k: f"{v} ({round(v/max(1,len(fact_fails)),3)})" for k, v in fact_budget.items()},
           "fact_types_n_failures": len(fact_fails),
           "base_fail_rate_by_qtype": fail_rate_by_qtype,
           "consolidate_share_of_all_failures": cons_share_all,
           "consolidate_share_of_clean": cons_share_clean,
           "consolidate_culprits_in_fragile_0.5-0.6_band": f"{cons_borderline}/{len(cons_fails)}",
           "two_restores_disagree": f"{disagree}/{nf}",
           "distractor_restore_fixes_consolidate_culprits(should~0)": f"{dist_fix_on_cons}/{len(cons_fails)}",
           "llm_judge_label_dist": dict(judge_dist),
           "llm_judge_recall_on_consolidate": round(judge_cons / len(cons_fails), 3) if cons_fails else None,
           "llm_judge_consolidate_base_rate": round(judge_dist.get("consolidate", 0) / nf, 3) if nf else None,
           "gpt_vs_nli_correctness_agreement": round(gpt_nli_agree / len(both), 3) if both else None,
           "failures_also_confirmed_wrong_by_nli": f"{nli_confirmed_fail}/{nf}",
           "items": items}
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print("\n==== Memory-op attribution on REAL HaluMem (v3: write-branch + real counterfactual) ====")
    print(f"questions={len(items)} natural_failures={nf}")
    print(f"base fail rate by qtype: {fail_rate_by_qtype}")
    print(f"FULL BUDGET (share of ALL failures): {out['failure_budget_of_ALL_failures']}")
    print(f"FACT-TYPES-ONLY budget (well-posed, n={len(fact_fails)}): {out['fact_types_only_budget']}")
    print(f"consolidate = {cons_share_all} of ALL failures  ({cons_share_clean} of clean)")
    print(f"  fragile 0.5-0.6 store-overlap band: {cons_borderline}/{len(cons_fails)}")
    print(f"two restores disagree: {disagree}/{nf}")
    print(f"distractor-evidence fixes consolidate culprits (should~0): {dist_fix_on_cons}/{len(cons_fails)}")
    print(f"competent judge label dist: {dict(judge_dist)}  (consolidate base rate {out['llm_judge_consolidate_base_rate']})")
    print(f"  judge recall on consolidate culprits: {out['llm_judge_recall_on_consolidate']}")
    print(f"2nd detector (NLI) vs gpt-judge correctness agreement: {out['gpt_vs_nli_correctness_agreement']}  "
          f"(failures also NLI-confirmed wrong: {out['failures_also_confirmed_wrong_by_nli']})")
    print("saved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
