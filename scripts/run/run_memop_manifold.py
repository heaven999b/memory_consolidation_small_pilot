#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Closed-loop kill-switch: does the MANIFOLD signal (continuous evidence-preservation
distance) beat the brittle LLM membership checks for op-attribution, and does
provenance-guided REPAIR help the end task? On the ground-truth benchmark (known culprit
+ confident-wrong), head-to-head on the SAME items.

Manifold attribution: embed the gold evidence e; measure its answer-preserving similarity
at each stage of the provenance trajectory:
  sim_write = max cos(e, dialogue-turn)   (write-drop -> e removed from dialogue -> low)
  sim_store = max cos(e, store-line)       (consolidate-drop -> e not in store -> low)
  sim_retr  = max cos(e, retrieved-line)   (retrieve-miss -> e excluded from context -> low)
The evidence's trajectory departs the answer-preserving manifold at the op with the LARGEST
DROP: d_write=1-sim_write, d_cons=sim_write-sim_store, d_retr=sim_store-sim_retr.
culprit = argmax drop. Continuous, no LLM yes/no -> should beat the brittle checks (55% ceiling).

REPAIR (the method leg): re-inject the gold evidence into the answer context (provenance-guided)
vs re-inject the DISTRACTOR (control). If evidence-repair fixes and distractor doesn't, the
diagnose->repair loop closes.

Embeddings: OpenAI text-embedding-3-small (cached). Reuses the ground-truth injection.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, sys
from datetime import datetime
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "core"))
sys.path.insert(0, str(ROOT / "scripts" / "run"))
TIERMEM = ROOT.parent / "tiermem_upstream"
sys.path.insert(0, str(TIERMEM))
HALU = ROOT / "benchmarks" / "halumem" / "official_repo" / "data" / "HaluMem-Medium.jsonl"

from run_memop_halumem import toks, note_lines, retrieve, answer, judge_correct, build_memory, gather_questions
from run_memop_groundtruth import (build_state, make_distractor, all_turn_texts, written_llm_turns,
                                   store_supports, evidence_line)

_EMB_CACHE: dict[str, list] = {}


def get_emb(client, texts):
    out, todo = {}, []
    for t in texts:
        h = hashlib.md5(t.encode()).hexdigest()
        if h in _EMB_CACHE:
            out[t] = _EMB_CACHE[h]
        else:
            todo.append(t)
    for i in range(0, len(todo), 128):
        batch = [t[:8000] or " " for t in todo[i:i + 128]]
        r = client.embeddings.create(model="text-embedding-3-small", input=batch)
        for t, d in zip(todo[i:i + 128], r.data):
            _EMB_CACHE[hashlib.md5(t.encode()).hexdigest()] = d.embedding
            out[t] = d.embedding
    return out


def cos(a, b):
    s = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return s / (na * nb + 1e-9)


def max_sim(embs, e_emb, lines):
    if not lines:
        return 0.0
    return max(cos(e_emb, embs[l]) for l in lines if l in embs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=6)
    ap.add_argument("--sessions", type=int, default=12)
    ap.add_argument("--max-q-per-user", type=int, default=12)
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--cache", default=str(ROOT / "state" / "memop_halumem_notes_20260712.json"))
    ap.add_argument("--out", default=str(ROOT / "state" / "memop_manifold_20260712.json"))
    args = ap.parse_args()

    from src.memory.linked_view_system import _OpenAILLM, _normalize_consolidated_note
    from openai import OpenAI
    llm = _OpenAILLM(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL") or None)
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
                if ev_store_line is not None:
                    base_ctx = [c for c in base_ctx if c != ev_store_line][:args.k]
                ans = answer(llm, q["question"], base_ctx)
                if judge_correct(llm, q["question"], q["gold"], ans):
                    continue
                cw = ("i don't know" not in ans.lower() and "unknown" not in ans.lower() and "not" not in ans.lower()[:8])
                dlg = all_turn_texts(u, args.sessions, drop_evidence=ev if culprit == "write_drop" else None)
                dlg_cand = sorted(dlg, key=lambda c: len(set().union(*[toks(e) for e in ev]) & toks(c)), reverse=True)[:8]
                # ---- (A) brittle LLM-check attribution (current method) ----
                write_ok = written_llm_turns(llm, dlg, ev)
                store_has = store_supports(llm, store, ev)
                llm_attr = "write_drop" if not write_ok else ("retrieve_miss" if store_has else "consolidate_drop")
                # ---- (B) MANIFOLD attribution (continuous embedding trajectory) ----
                ev_text = evidence_line(ev)
                texts = [ev_text] + dlg_cand + store + base_ctx
                embs = get_emb(client, list(dict.fromkeys(texts)))
                e_emb = embs[ev_text]
                sim_w = max_sim(embs, e_emb, dlg_cand)
                sim_s = max_sim(embs, e_emb, store)
                sim_r = max_sim(embs, e_emb, base_ctx)
                drops = {"write_drop": 1.0 - sim_w, "consolidate_drop": max(0.0, sim_w - sim_s),
                         "retrieve_miss": max(0.0, sim_s - sim_r)}
                man_attr = max(drops, key=drops.get)
                # ---- (C) trace-only judge ----
                jr = llm.generate(
                    f"A memory agent (write->consolidate->retrieve->answer) answered WRONG. The fact may have been "
                    f"never written, dropped in consolidation, or not retrieved. Which SINGLE step? one word: "
                    f"write/consolidate/retrieve.\nQuestion: {q['question']}\nGold: {q['gold']}\nRetrieved:\n" +
                    "\n".join(base_ctx) + f"\nAnswer: {ans}\nStep:").strip().lower()
                judge = {"write": "write_drop", "consolidate": "consolidate_drop", "retrieve": "retrieve_miss"}.get(
                    next((o for o in ("consolidate", "retrieve", "write") if o in jr), ""), "unknown")
                # ---- (D) REPAIR: provenance-guided (true evidence) vs distractor control ----
                rep_ev = judge_correct(llm, q["question"], q["gold"], answer(llm, q["question"], [ev_text] + base_ctx[:args.k - 1]))
                rep_ctrl = judge_correct(llm, q["question"], q["gold"], answer(llm, q["question"], [distractor] + base_ctx[:args.k - 1]))
                items.append(dict(uuid=u["uuid"][:8], injected=culprit, cw=cw,
                                  write_ok=write_ok, store_has=store_has,
                                  sim_w=round(sim_w, 3), sim_s=round(sim_s, 3), sim_r=round(sim_r, 3),
                                  llm_attr=llm_attr, man_attr=man_attr, judge=judge,
                                  llm_ok=llm_attr == culprit, man_ok=man_attr == culprit, judge_ok=judge == culprit,
                                  repair_evidence_ok=rep_ev, repair_distractor_ok=rep_ctrl))
                print(f"  inj={culprit:16s} sims(w/s/r)={sim_w:.2f}/{sim_s:.2f}/{sim_r:.2f} "
                      f"MAN={man_attr:16s}{'OK' if man_attr==culprit else 'XX'} LLM={llm_attr:16s}{'ok' if llm_attr==culprit else 'xx'} "
                      f"J={judge}", flush=True)

    n = len(items); cw = [it for it in items if it["cw"]]
    def acc(sel, f): return round(sum(1 for it in sel if it[f]) / len(sel), 3) if sel else None
    out = {"generated_at": datetime.now().isoformat(timespec="seconds"), "n": n, "n_cw": len(cw),
           "MANIFOLD_acc": acc(items, "man_ok"), "MANIFOLD_acc_cw": acc(cw, "man_ok"),
           "LLMcheck_acc": acc(items, "llm_ok"), "LLMcheck_acc_cw": acc(cw, "llm_ok"),
           "judge_acc": acc(items, "judge_ok"), "judge_acc_cw": acc(cw, "judge_ok"),
           "per_op_manifold": {op: acc([it for it in items if it["injected"] == op], "man_ok") for op in OPS},
           "per_op_llmcheck": {op: acc([it for it in items if it["injected"] == op], "llm_ok") for op in OPS},
           "repair_evidence_fix_rate": acc(items, "repair_evidence_ok"),
           "repair_distractor_fix_rate(control,should_low)": acc(items, "repair_distractor_ok"),
           "items": items}
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print("\n==== CLOSED-LOOP kill-switch: manifold vs brittle checks vs judge ====")
    print(f"n={n}  confident-wrong={len(cw)}")
    print(f"ATTRIBUTION acc:   MANIFOLD={out['MANIFOLD_acc']} (cw {out['MANIFOLD_acc_cw']})  |  "
          f"LLM-check={out['LLMcheck_acc']} (cw {out['LLMcheck_acc_cw']})  |  judge={out['judge_acc']} (cw {out['judge_acc_cw']})")
    print(f"per-op MANIFOLD: {out['per_op_manifold']}")
    print(f"per-op LLM-check: {out['per_op_llmcheck']}")
    print(f"REPAIR: provenance(true evidence) fixes {out['repair_evidence_fix_rate']}  vs  distractor control {out['repair_distractor_fix_rate(control,should_low)']}")
    print("saved:", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
