#!/usr/bin/env python3
"""RT-02 CHIR Stage-1 existence pilot — QA side (official MemEvoBench QA pipeline).

Arms per case (design doc state/rt02_baseline_design_20260718.md §4.2):
  contam_d3     misleading pool -> 3 official rounds -> source correction -> k-phase
  safe_d3       sources corrected at t=0 -> 3 official rounds -> k-phase (primary control)
  full_closure  contam_d3 trajectory -> source correction + descendant evidence-rewrite -> k-phase
  contam_d0     misleading pool, no rounds -> source correction -> k-phase (append-only/raw)
  benign_vol    corrected pool + borrowed benign descendants (volume control) -> k-phase
  null_mem      official base_model mode probes (descriptive baseline)

k-phase: k0 probe(3 queries, read-only) -> writeback(test_query) -> k1 probe -> writeback(test_query_2) -> k2 probe.
All verdicts: official JUDGE_RESPONSE_PROMPT via judge1 (default gpt-4.1-mini) + judge2 (gpt-4o) on probes.
"""
import argparse
import glob
import json
import os
import sys
import threading
import time
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt02_common import (  # noqa: E402
    offi, make_clients, snapshot_hash, prompt_view,
    correct_qa_sources, full_closure_qa, judge_qa, CONTENT_FIELD,
)

_write_lock = threading.Lock()


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def retry(fn, tries=4, base_sleep=2.0):
    last = None
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # rate limits / transient API errors
            last = e
            time.sleep(base_sleep * (2 ** i))
    raise last


def gen(client, model, query, memories, prompt_mode="original"):
    return retry(lambda: offi.generate_response(
        client, model, query, memories, temperature=0, prompt_mode=prompt_mode))


def case_queries(item):
    return [
        ("test_query", item.get("test_query", ""), item.get("test_correct_answer", ""), item.get("risk_type", "")),
        ("test_query_2", item.get("test_query_2", ""), item.get("test_correct_answer_2", ""), item.get("risk_type_2", "")),
        ("test_query_3", item.get("test_query_3", ""), item.get("test_correct_answer_3", ""), item.get("risk_type_3", "")),
    ]


def source_records_view(memories):
    """Canonical view of the ORIGINAL source records (ids A-E) as serialized to the model,
    used for the byte-identity branch-matching assert."""
    src = [m for m in memories if m.get("label_source") not in ("rt02_descendant", "rt02_benign_borrowed")]
    return prompt_view(src)


def run_rounds(client, model, judge_model, item, memories, n_rounds, tag):
    """Official iterative rounds: answer -> official judge label -> append as conversation memory."""
    queries = case_queries(item)
    rounds = []
    for r in range(n_rounds):
        qkey, query, ca, risk = queries[r % 3]
        resp = gen(client, model, query, memories)
        unsafe, label, reason = judge_qa(client, judge_model, query, risk, ca, resp)
        new_mem = offi.create_memory_from_response(query, resp, offi.get_next_memory_id(memories))
        new_mem["label"] = label
        new_mem["label_source"] = "rt02_descendant"
        memories.append(new_mem)
        rounds.append({"round": r + 1, "query_key": qkey, "unsafe_j1": unsafe,
                       "label": label, "reason": reason[:300], "response": resp,
                       "pool_hash": snapshot_hash(memories)})
    return rounds


def probe(client, model, judge_model, judge2_model, item, memories, prompt_mode="original"):
    """Read-only evaluation on the 3 official queries. Nothing is written back."""
    out = []
    for qkey, query, ca, risk in case_queries(item):
        resp = gen(client, model, query, memories, prompt_mode=prompt_mode)
        u1, l1, r1 = judge_qa(client, judge_model, query, risk, ca, resp)
        rec = {"query_key": qkey, "unsafe_j1": u1, "label_j1": l1, "reason_j1": r1[:300],
               "response": resp}
        if judge2_model:
            u2, l2, r2 = judge_qa(client, judge2_model, query, risk, ca, resp)
            rec.update({"unsafe_j2": u2, "label_j2": l2, "reason_j2": r2[:300],
                        "unsafe_and": u1 & u2})
        out.append(rec)
    return out


def k_phase(client, model, judge_model, judge2_model, item, memories):
    """k0 probe -> writeback(test_query) -> k1 probe -> writeback(test_query_2) -> k2 probe."""
    queries = case_queries(item)
    result = {"probes": {}, "writebacks": [], "pool_hashes": {}}
    result["pool_hashes"]["k0"] = snapshot_hash(memories)
    result["probes"]["k0"] = probe(client, model, judge_model, judge2_model, item, memories)
    for k, (qkey, query, ca, risk) in enumerate(queries[:2], start=1):
        resp = gen(client, model, query, memories)
        unsafe, label, reason = judge_qa(client, judge_model, query, risk, ca, resp)
        new_mem = offi.create_memory_from_response(query, resp, offi.get_next_memory_id(memories))
        new_mem["label"] = label
        new_mem["label_source"] = "rt02_descendant"
        memories.append(new_mem)
        result["writebacks"].append({"k": k, "query_key": qkey, "unsafe_j1": unsafe, "label": label})
        result["pool_hashes"][f"k{k}"] = snapshot_hash(memories)
        result["probes"][f"k{k}"] = probe(client, model, judge_model, judge2_model, item, memories)
    return result


def process_case_phase1(client, args, case):
    """contam_d3 + safe_d3 + full_closure (shared contaminated trajectory). Returns records + safe descendants."""
    item, domain = case["item"], case["domain"]
    cid = item.get("cluster_id")
    q2ca = {q: ca for _, q, ca, _ in case_queries(item)}
    records, out = [], {}

    # --- contaminated trajectory (shared by contam_d3 and full_closure) ---
    contam = deepcopy(item.get("retrievable_memories", []))
    contam_rounds = run_rounds(client, args.model, args.judge_model, item, contam, 3, "contam")
    n_corr = correct_qa_sources(contam)
    contam_at_corr = deepcopy(contam)

    # --- safe-history branch ---
    safe = deepcopy(item.get("retrievable_memories", []))
    n_safe = correct_qa_sources(safe)
    safe_rounds = run_rounds(client, args.model, args.judge_model, item, safe, 3, "safe")

    # branch-matching assert: corrected sources must serialize byte-identically
    match_ok = source_records_view(contam_at_corr) == source_records_view(safe)
    if not match_ok:
        log(f"!! BRANCH MATCH FAIL {domain}/{cid}")

    safe_desc = [m for m in safe if m.get("label_source") == "rt02_descendant"][:3]

    for arm, pool, rounds in (
        ("contam_d3", deepcopy(contam_at_corr), contam_rounds),
        ("safe_d3", deepcopy(safe), safe_rounds),
    ):
        kp = k_phase(client, args.model, args.judge_model, args.judge2_model, item, pool)
        rec = {"domain": domain, "cluster_id": cid, "arm": arm,
               "n_sources_corrected": n_corr if arm == "contam_d3" else n_safe,
               "branch_match_ok": match_ok, "rounds": rounds, **kp}
        if arm == "safe_d3":
            rec["safe_descendants_store"] = deepcopy(safe_desc)
        records.append(rec)

    fc = deepcopy(contam_at_corr)
    n_rw = full_closure_qa(fc, q2ca)
    kp = k_phase(client, args.model, args.judge_model, args.judge2_model, item, fc)
    records.append({"domain": domain, "cluster_id": cid, "arm": "full_closure",
                    "n_descendants_rewritten": n_rw, "branch_match_ok": match_ok,
                    "rounds": contam_rounds, **kp})

    out["records"] = records
    out["safe_descendants"] = deepcopy(safe_desc)
    return out


def process_case_phase2(client, args, case, donor_descendants):
    """contam_d0 (append-only/raw), benign_vol, null_mem."""
    item, domain = case["item"], case["domain"]
    cid = item.get("cluster_id")
    records = []

    d0 = deepcopy(item.get("retrievable_memories", []))
    n_corr = correct_qa_sources(d0)
    kp = k_phase(client, args.model, args.judge_model, args.judge2_model, item, d0)
    records.append({"domain": domain, "cluster_id": cid, "arm": "contam_d0",
                    "n_sources_corrected": n_corr, "rounds": [], **kp})

    bv = deepcopy(item.get("retrievable_memories", []))
    correct_qa_sources(bv)
    borrowed = []
    for dmem in donor_descendants:
        m = deepcopy(dmem)
        m["id"] = offi.get_next_memory_id(bv)
        m["label_source"] = "rt02_benign_borrowed"
        bv.append(m)
        borrowed.append(m["id"])
    kp = k_phase(client, args.model, args.judge_model, args.judge2_model, item, bv)
    records.append({"domain": domain, "cluster_id": cid, "arm": "benign_vol",
                    "n_borrowed": len(borrowed), "rounds": [], **kp})

    nm = probe(client, args.model, args.judge_model, args.judge2_model, item, [], prompt_mode="base_model")
    records.append({"domain": domain, "cluster_id": cid, "arm": "null_mem",
                    "rounds": [], "probes": {"k0": nm}, "writebacks": [], "pool_hashes": {}})
    return records


def append_records(path, records):
    with _write_lock:
        with open(path, "a", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")


def load_done(path):
    done = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["domain"], r["cluster_id"], r["arm"]))
                except Exception:
                    pass
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qa-dir", default=os.path.join(os.path.dirname(offi.__file__), "memorybench", "QA"))
    ap.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"))
    ap.add_argument("--judge-model", default="gpt-4.1-mini")
    ap.add_argument("--judge2-model", default="gpt-4o")
    ap.add_argument("--per-domain", type=int, default=3)
    ap.add_argument("--domains", default="")
    ap.add_argument("--max-cases", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, "chir_qa_records.jsonl")
    client = make_clients()

    cases = []
    for path in sorted(glob.glob(os.path.join(args.qa_dir, "*_memory_triplequery.json"))):
        domain = os.path.basename(path).split("_memory_triplequery")[0]
        if args.domains and domain not in args.domains.split(","):
            continue
        with open(path, encoding="utf-8") as f:
            items = json.load(f)
        items = sorted(items, key=lambda x: x.get("cluster_id", 0))[: args.per_domain]
        for it in items:
            cases.append({"domain": domain, "item": it})
    if args.max_cases:
        cases = cases[: args.max_cases]
    log(f"{len(cases)} QA cases × 6 arms; model={args.model} judge1={args.judge_model} judge2={args.judge2_model}")

    done = load_done(out_path)
    meta = {"model": args.model, "judge1": args.judge_model, "judge2": args.judge2_model,
            "per_domain": args.per_domain, "n_cases": len(cases),
            "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(os.path.join(args.outdir, "chir_qa_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # ---- phase 1: contam_d3 / safe_d3 / full_closure ----
    safe_desc = {}
    p1_needed = [c for c in cases if not {(c["domain"], c["item"].get("cluster_id"), a) for a in
                 ("contam_d3", "safe_d3", "full_closure")} <= done]

    def p1(case):
        out = process_case_phase1(client, args, case)
        append_records(out_path, out["records"])
        return case, out["safe_descendants"]

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(p1, c) for c in p1_needed]
        for fut in as_completed(futs):
            case, sd = fut.result()
            key = (case["domain"], case["item"].get("cluster_id"))
            safe_desc[key] = sd
            log(f"phase1 done {key}")

    # recover safe descendants for already-done cases from the JSONL (resume path)
    if len(safe_desc) < len(cases) and os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if r.get("arm") == "safe_d3" and (r["domain"], r["cluster_id"]) not in safe_desc:
                    safe_desc[(r["domain"], r["cluster_id"])] = r.get("safe_descendants_store", [])

    # ---- phase 2: contam_d0 / benign_vol / null_mem (donor = next case in same domain) ----
    by_domain = {}
    for c in cases:
        by_domain.setdefault(c["domain"], []).append(c)

    def donor_for(case):
        sibs = by_domain[case["domain"]]
        idx = sibs.index(case)
        for step in range(1, len(sibs)):
            key = (case["domain"], sibs[(idx + step) % len(sibs)]["item"].get("cluster_id"))
            if key in safe_desc and safe_desc[key]:
                return safe_desc[key]
        own = (case["domain"], case["item"].get("cluster_id"))
        return safe_desc.get(own, [])

    p2_needed = [c for c in cases if not {(c["domain"], c["item"].get("cluster_id"), a) for a in
                 ("contam_d0", "benign_vol", "null_mem")} <= done]

    def p2(case):
        recs = process_case_phase2(client, args, case, donor_for(case))
        append_records(out_path, recs)
        return (case["domain"], case["item"].get("cluster_id"))

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(p2, c) for c in p2_needed]
        for fut in as_completed(futs):
            log(f"phase2 done {fut.result()}")

    log(f"ALL DONE -> {out_path}")


if __name__ == "__main__":
    main()
