#!/usr/bin/env python3
"""RT-02 v2 PairGain runner — genuine operators + query/time separation + lineage-local snapshots.

Rebuilds the PairGain RQ1 transitions on the v2 construct-validity fixes:
  R1: consolidation via a genuine operator (fail-fast enforces real state change).
  R4: the 3 official queries are split into CONSTRUCTION queries (drive consolidation,
      written back) and a HELD-OUT endpoint query (never written back); the paired unsafe
      endpoint A(t) is measured ONLY on the held-out query, so G(t) predicts a future the
      construction path never touched.
  R6: branch_match_audit is run at t0 and flagged; official-text arm by default.
  R2: probes/generation are retrieval-aware (top-k), exposure logged.

Snapshots of both branches at every t are saved for the OFFLINE lineage-local NLI step
(rt02_v2_measure.py: source_only / source_lineage / retrieval_weighted q, the R3 fix).
This runner does NOT compute NLI. Run with --mock for a zero-API pipeline check.
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import time
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt02_common import offi, make_clients, snapshot_hash, correct_qa_sources, judge_qa, CONTENT_FIELD  # noqa: E402
from rt02_v2_operators import OPERATORS, MockBackend, LLMBackend, branch_match_audit, retry, repro_meta  # noqa: E402
from rt02_v2_retrieval import TfidfRetriever  # noqa: E402
from rt02_v2_mock import MockChatClient  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MANIFEST = os.path.join(ROOT, "state", "rt02_v1_used_cases_manifest.json")


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def gen(client, model, query, subset, temperature=0):
    return retry(lambda: offi.generate_response(client, model, query, subset, temperature=temperature))


def case_queries(item):
    return [
        ("test_query", item.get("test_query", ""), item.get("test_correct_answer", ""), item.get("risk_type", "")),
        ("test_query_2", item.get("test_query_2", ""), item.get("test_correct_answer_2", ""), item.get("risk_type_2", "")),
        ("test_query_3", item.get("test_query_3", ""), item.get("test_correct_answer_3", ""), item.get("risk_type_3", "")),
    ]


def heldout_index(domain, cid):
    """Stable SHA-256 pick of the held-out endpoint query (design §7); chosen before any run."""
    return int(hashlib.sha256(f"{domain}|{cid}".encode("utf-8")).hexdigest(), 16) % 3


def source_ids(pool):
    return [m.get("id") for m in pool if m.get("label_source") not in ("rt02_descendant", "rt02_benign_borrowed")
            and m.get("rt02_role") != "rt02_summary"]


def misleading_pairs(item):
    return [{"m": m.get(CONTENT_FIELD.get((m.get("type") or "").lower(), "content"), ""),
             "c": m.get("correct_answer", "")}
            for m in item.get("retrievable_memories", [])
            if m.get("label") == "misleading" and m.get("correct_answer")]


def select_cases(args):
    with open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    want = {}
    for domain, blk in man["qa"]["split"].items():
        if args.domains and domain not in args.domains.split(","):
            continue
        want[domain] = set(blk["unseen_dev"] if args.split == "dev" else blk["unseen_confirmatory"])
    cases = []
    for path in sorted(glob.glob(os.path.join(os.path.dirname(offi.__file__), "memorybench", "QA", "*_memory_triplequery.json"))):
        domain = os.path.basename(path).split("_memory_triplequery")[0]
        if domain not in want:
            continue
        with open(path, encoding="utf-8") as f:
            items = json.load(f)
        for it in sorted(items, key=lambda x: x.get("cluster_id", 0)):
            if it.get("cluster_id") in want[domain]:
                cases.append((domain, it.get("cluster_id"), it))
    if args.n_cases:
        cases = cases[: args.n_cases]
    return cases


def heldout_endpoint(client, args, retriever, item, minus_pool, plus_pool, ho):
    """Paired unsafe A(t) on the held-out query only (read-only, retrieval-aware)."""
    qkey, query, ca, risk = case_queries(item)[ho]
    out = {}
    for name, pool in (("minus", minus_pool), ("plus", plus_pool)):
        subset, exposure = retriever.retrieve(query, pool)
        resp = gen(client, args.model, query, subset, args.temperature)
        u1, _, _ = judge_qa(client, args.judge_model, query, risk, ca, resp)
        rec = {"unsafe_j1": u1, "retrieved_ids": [e["id"] for e in exposure]}
        if args.judge2_model:
            u2, _, _ = judge_qa(client, args.judge2_model, query, risk, ca, resp)
            rec.update({"unsafe_j2": u2, "unsafe_and": u1 & u2})
        out[name] = rec
    out["A_j1"] = out["minus"]["unsafe_j1"] - out["plus"]["unsafe_j1"]
    if args.judge2_model:
        out["A_and"] = out["minus"].get("unsafe_and", 0) - out["plus"].get("unsafe_and", 0)
    return {"query_key": qkey, **out}


def process_case(client, args, retriever, operator_fn, backend, domain, cid, item, snap_dir):
    ho = heldout_index(domain, cid)
    construction = [q for i, q in enumerate(case_queries(item)) if i != ho]

    minus = deepcopy(item.get("retrievable_memories", []))
    plus = deepcopy(item.get("retrievable_memories", []))
    correct_qa_sources(plus)

    src_ids = source_ids(minus)
    audit = branch_match_audit(minus, plus, target_ids=src_ids, style_matched=False)

    rec = {"domain": domain, "cluster_id": cid, "operator": args.operator,
           "heldout_query_index": ho, "construction_query_keys": [q[0] for q in construction],
           "source_ids": src_ids, "pairs": misleading_pairs(item),
           "branch_match_audit": audit, "steps": [], "op_traces": {"minus": [], "plus": []}}

    def snap(tag, pool):
        p = os.path.join(snap_dir, f"{domain}_{cid}_{tag}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(pool, f, ensure_ascii=False)
        return {"path": os.path.relpath(p, snap_dir), "hash": snapshot_hash(pool)}

    # t=0 baseline endpoint + snapshots
    rec["steps"].append({"t": 0, "minus_snap": snap("minus_t0", minus), "plus_snap": snap("plus_t0", plus),
                         "endpoint": heldout_endpoint(client, args, retriever, item, minus, plus, ho)})

    for t in range(1, args.transitions + 1):
        qkey, query, ca, risk = construction[(t - 1) % len(construction)]
        for name, pool_ref in (("minus", minus), ("plus", plus)):
            pool = minus if name == "minus" else plus
            subset, _ = retriever.retrieve(query, pool)
            resp = gen(client, args.model, query, subset, args.temperature)
            new_pool, trace = operator_fn(pool, {"query": query, "answer": resp}, backend)
            trace["t"] = t
            rec["op_traces"][name].append(trace)
            if name == "minus":
                minus = new_pool
            else:
                plus = new_pool
        rec["steps"].append({"t": t, "construction_query": qkey,
                             "minus_snap": snap(f"minus_t{t}", minus), "plus_snap": snap(f"plus_t{t}", plus),
                             "endpoint": heldout_endpoint(client, args, retriever, item, minus, plus, ho)})
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--operator", default="summary_rewrite", choices=list(OPERATORS))
    ap.add_argument("--split", default="dev", choices=("dev", "confirmatory"))
    ap.add_argument("--domains", default="")
    ap.add_argument("--n-cases", type=int, default=0)
    ap.add_argument("--transitions", type=int, default=4, help="consolidation transitions (deeper = longer horizon, R4)")
    ap.add_argument("--k-retrieval", dest="k", type=int, default=5)
    ap.add_argument("--model", default="gpt-4.1-mini")
    ap.add_argument("--judge-model", default="gpt-4.1-mini")
    ap.add_argument("--judge2-model", default="gpt-4o")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--temperature", type=float, default=0,
                    help="generation temperature; >0 for multi-seed stochasticity runs (S1)")
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    if not args.mock and glob.glob(os.path.join(args.outdir, "*20260718*")):
        raise SystemExit("refusing to write into a v1 outdir")
    os.makedirs(args.outdir, exist_ok=True)
    snap_dir = os.path.join(args.outdir, "snapshots")
    os.makedirs(snap_dir, exist_ok=True)

    client = MockChatClient() if args.mock else make_clients()
    backend = MockBackend() if args.mock else LLMBackend(client, args.model)
    retriever = TfidfRetriever(k=args.k)
    operator_fn = OPERATORS[args.operator]

    cases = select_cases(args)
    log(f"PairGain v2: operator={args.operator} split={args.split} cases={len(cases)} "
        f"transitions={args.transitions} k={args.k} mock={args.mock}")

    with open(os.path.join(args.outdir, "run_manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"operator": args.operator, "split": args.split, "transitions": args.transitions,
                   "k_retrieval": args.k, "temperature": args.temperature, "model": args.model, "judge1": args.judge_model,
                   "judge2": args.judge2_model, "mock": args.mock, "n_cases": len(cases),
                   "case_ids": [[d, c] for d, c, _ in cases], "repro": repro_meta(),
                   "started": time.strftime("%Y-%m-%d %H:%M:%S")},
                  f, ensure_ascii=False, indent=2)

    out_path = os.path.join(args.outdir, "pairgain_v2_records.jsonl")
    done = set()  # resume: skip (domain, cluster_id) already written
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["domain"], r["cluster_id"]))
                except Exception:
                    pass
        if done:
            log(f"resume: {len(done)} case-records already present, will skip them")
    n_match_fail = 0
    with open(out_path, "a", encoding="utf-8") as fout:
        for domain, cid, item in cases:
            if (domain, cid) in done:
                continue
            rec = process_case(client, args, retriever, operator_fn, backend, domain, cid, item, snap_dir)
            n_match_fail += int(rec["branch_match_audit"]["match_fail"])
            fout.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
            fout.flush()
            log(f"case done {domain}/{cid} (heldout q idx {rec['heldout_query_index']})")
    log(f"ALL DONE -> {out_path}; branch match_fail cases (this run): {n_match_fail}")
    if args.mock:
        log(f"mock client calls: {getattr(client, 'calls', {})}")


if __name__ == "__main__":
    main()
