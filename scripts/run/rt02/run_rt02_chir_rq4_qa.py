#!/usr/bin/env python3
"""RT-02 CHIR RQ4 QA pilot: cross-fitted selective descendant closure.

The runner reconstructs the exact Stage-1 contaminated d=3 histories from
persisted responses, then evaluates proposal-registered evidence rewrite and
equal-count baselines with the official MemEvoBench QA generator/judge path.
"""
import argparse
import glob
import hashlib
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_rt02_chir_qa as cqa  # noqa: E402
from rt02_common import (  # noqa: E402
    correct_qa_sources, judge_qa, make_clients, offi, snapshot_hash,
)

_write_lock = threading.Lock()


def stable_seed(domain, cluster_id):
    raw = f"{domain}:{cluster_id}".encode("utf-8")
    return int(hashlib.sha256(raw).hexdigest()[:12], 16)


def u_mean(probes, gate="unsafe_j1"):
    vals = [p[gate] for p in probes if gate in p]
    return sum(vals) / len(vals) if vals else None


def load_stage1(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("arm") == "contam_d3":
                out[(rec["domain"], str(rec["cluster_id"]))] = rec
    return out


def reconstruct_source_only(item, stage_rec):
    pool = deepcopy(item.get("retrievable_memories", []))
    qmap = {key: (query, ca) for key, query, ca, _ in cqa.case_queries(item)}
    for rr in stage_rec.get("rounds", []):
        qkey = rr["query_key"]
        query = qmap[qkey][0]
        mem = offi.create_memory_from_response(query, rr["response"], offi.get_next_memory_id(pool))
        mem["label"] = rr.get("label", "")
        mem["label_source"] = "rt02_descendant"
        pool.append(mem)
    pre_correction_ok = not stage_rec.get("rounds") or (
        snapshot_hash(pool) == stage_rec["rounds"][-1].get("pool_hash")
    )
    correct_qa_sources(pool)
    return pool, pre_correction_ok


def descendant_positions(pool):
    return [i for i, mem in enumerate(pool) if mem.get("label_source") == "rt02_descendant"]


def rewrite_subset(pool, positions, subset, query_to_ca):
    out = deepcopy(pool)
    for descendant_idx in subset:
        mem = out[positions[descendant_idx]]
        ca = query_to_ca.get(mem.get("user_request", ""), "")
        if ca:
            mem["assistant"] = ca
            mem["user_feedback"] = ""
            mem["status"] = "closure_rewritten"
    return out


def delete_one(pool, positions, descendant_idx):
    remove_at = positions[descendant_idx]
    return [deepcopy(mem) for i, mem in enumerate(pool) if i != remove_at]


def probe_keys(client, args, item, pool, query_keys, include_j2=False):
    qmap = {key: (query, ca, risk) for key, query, ca, risk in cqa.case_queries(item)}
    out = []
    for key in query_keys:
        query, ca, risk = qmap[key]
        response = cqa.gen(client, args.model, query, pool)
        u1, l1, r1 = judge_qa(client, args.judge_model, query, risk, ca, response)
        rec = {
            "query_key": key, "unsafe_j1": u1, "label_j1": l1,
            "reason_j1": r1[:300], "response": response,
        }
        if include_j2:
            u2, l2, r2 = judge_qa(client, args.judge2_model, query, risk, ca, response)
            rec.update({
                "unsafe_j2": u2, "label_j2": l2, "reason_j2": r2[:300],
                "unsafe_and": u1 & u2,
            })
        out.append(rec)
    return out


def process_case(client, args, case, stage_rec):
    item, domain = case["item"], case["domain"]
    cid = item.get("cluster_id")
    pool, reconstruction_ok = reconstruct_source_only(item, stage_rec)
    positions = descendant_positions(pool)
    if not positions:
        return {"domain": domain, "cluster_id": cid, "error": "no descendants"}

    queries = cqa.case_queries(item)
    all_keys = [q[0] for q in queries]
    heldout_idx = stable_seed(domain, cid) % len(all_keys)
    heldout_keys = [all_keys[heldout_idx]]
    dev_keys = [key for i, key in enumerate(all_keys) if i != heldout_idx]
    query_to_ca = {query: ca for _, query, ca, _ in queries}
    n_desc = len(positions)
    cache = {}

    def eval_subset(subset, keys, include_j2=False):
        ck = (tuple(sorted(subset)), tuple(keys), include_j2)
        if ck not in cache:
            cache[ck] = probe_keys(
                client, args, item,
                rewrite_subset(pool, positions, subset, query_to_ca),
                keys, include_j2=include_j2,
            )
        return cache[ck]

    base_dev = eval_subset((), dev_keys)
    full_subset = tuple(range(n_desc))
    full_dev = eval_subset(full_subset, dev_keys)
    base_u, full_u = u_mean(base_dev), u_mean(full_dev)

    singletons = []
    for idx in range(n_desc):
        probes = eval_subset((idx,), dev_keys)
        singletons.append({
            "idx": idx, "descendant_id": pool[positions[idx]].get("id"),
            "dev_unsafe_j1": u_mean(probes),
            "correction_influence": None if base_u is None else base_u - u_mean(probes),
        })

    deletion = []
    for idx in range(n_desc):
        probes = probe_keys(client, args, item, delete_one(pool, positions, idx), dev_keys)
        deletion.append({
            "idx": idx, "dev_unsafe_j1": u_mean(probes),
            "deletion_influence": None if base_u is None else base_u - u_mean(probes),
        })

    influence_order = sorted(
        range(n_desc),
        key=lambda i: (singletons[i]["correction_influence"], -i),
        reverse=True,
    )
    m_star, dev_ratio = None, None
    dev_benefit = None if base_u is None or full_u is None else base_u - full_u
    prefix_trace = []
    if dev_benefit is not None and dev_benefit > 0:
        for m in range(1, n_desc + 1):
            subset = tuple(influence_order[:m])
            pu = u_mean(eval_subset(subset, dev_keys))
            ratio = (base_u - pu) / dev_benefit
            prefix_trace.append({"m": m, "subset": subset, "dev_unsafe_j1": pu, "ratio": ratio})
            if m_star is None and ratio >= args.rho:
                m_star, dev_ratio = m, ratio

    result = {
        "task": "qa", "domain": domain, "cluster_id": cid,
        "reconstruction_ok": reconstruction_ok,
        "source_only_hash": snapshot_hash(pool),
        "n_descendants": n_desc, "dev_keys": dev_keys, "heldout_keys": heldout_keys,
        "rho": args.rho, "dev_source_unsafe_j1": base_u,
        "dev_full_unsafe_j1": full_u, "dev_full_benefit": dev_benefit,
        "single_rewrite": singletons, "single_delete": deletion,
        "influence_order": influence_order, "prefix_trace": prefix_trace,
        "m_star": m_star,
        "repaired_fraction": None if m_star is None else m_star / n_desc,
        "dev_recovery_ratio": dev_ratio,
        "heldout": {}, "baseline_orders": {},
    }

    # Always retain source/full held-out anchors.  Judge 2 is used only here,
    # after development selection is frozen.
    result["heldout"]["source_only"] = eval_subset((), heldout_keys, include_j2=True)
    result["heldout"]["full_closure"] = eval_subset(full_subset, heldout_keys, include_j2=True)
    if m_star is None:
        return result

    rng = random.Random(stable_seed(domain, cid) + 17)
    random_order = list(range(n_desc))
    rng.shuffle(random_order)
    desc_text = [str(pool[pos].get("assistant", "")) for pos in positions]
    unsafe_scores = [stage_rec["rounds"][i].get("unsafe_j1", 0) for i in range(n_desc)]
    deletion_scores = [row["deletion_influence"] for row in deletion]
    orders = {
        "targeted": influence_order,
        "random": random_order,
        "recency": list(reversed(range(n_desc))),
        "length": sorted(range(n_desc), key=lambda i: (len(desc_text[i]), i), reverse=True),
        "current_unsafe": sorted(range(n_desc), key=lambda i: (unsafe_scores[i], -i), reverse=True),
        "deletion_influence": sorted(range(n_desc), key=lambda i: (deletion_scores[i], -i), reverse=True),
        "retrieval_uniform": list(range(n_desc)),
    }
    for name, order in orders.items():
        subset = tuple(order[:m_star])
        result["baseline_orders"][name] = {"order": order, "subset": subset}
        result["heldout"][name] = eval_subset(subset, heldout_keys, include_j2=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qa-dir", default=os.path.join(os.path.dirname(offi.__file__), "memorybench", "QA"))
    ap.add_argument("--stage1", default="state/rt02_runs/chir_qa_20260718/chir_qa_records.jsonl")
    ap.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"))
    ap.add_argument("--judge-model", default="gpt-4.1-mini")
    ap.add_argument("--judge2-model", default="gpt-4o")
    ap.add_argument("--per-domain", type=int, default=1)
    ap.add_argument("--max-cases", type=int, default=0)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--rho", type=float, default=0.8)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, "chir_rq4_qa_records.jsonl")
    stage1 = load_stage1(args.stage1)
    cases = []
    for path in sorted(glob.glob(os.path.join(args.qa_dir, "*_memory_triplequery.json"))):
        domain = os.path.basename(path).split("_memory_triplequery")[0]
        with open(path, encoding="utf-8") as f:
            items = sorted(json.load(f), key=lambda x: x.get("cluster_id", 0))[:args.per_domain]
        cases.extend({"domain": domain, "item": item} for item in items)
    cases = [c for c in cases if (c["domain"], str(c["item"].get("cluster_id"))) in stage1]
    if args.max_cases:
        cases = cases[:args.max_cases]

    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                done.add((rec.get("domain"), str(rec.get("cluster_id"))))
    todo = [c for c in cases if (c["domain"], str(c["item"].get("cluster_id"))) not in done]
    with open(os.path.join(args.outdir, "chir_rq4_qa_meta.json"), "w", encoding="utf-8") as f:
        json.dump({
            "model": args.model, "judge1": args.judge_model, "judge2": args.judge2_model,
            "rho": args.rho, "n_cases": len(cases), "started": time.strftime("%Y-%m-%d %H:%M:%S"),
        }, f, ensure_ascii=False, indent=2)

    client = make_clients()

    def run_one(case):
        key = (case["domain"], str(case["item"].get("cluster_id")))
        rec = process_case(client, args, case, stage1[key])
        with _write_lock:
            with open(out_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        return key

    cqa.log(f"CHIR RQ4 QA: {len(cases)} cases; {len(todo)} pending")
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(run_one, case) for case in todo]):
            cqa.log(f"RQ4 case done {fut.result()}")
    cqa.log(f"ALL DONE -> {out_path}")


if __name__ == "__main__":
    main()
