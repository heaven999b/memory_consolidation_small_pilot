#!/usr/bin/env python3
"""RT-02 v2 CHIR runner — genuine consolidation operators + top-k retrieval.

Rebuilds the CHIR RQ3 existence arms on the v2 construct-validity fixes:
  R1: consolidation happens through a genuine operator (append_only / summary_rewrite /
      merge_consolidation) with fail-fast that operator-ON truly changes old state.
  R2: probes/generation see only top-k RETRIEVED records (retrieval exposure logged),
      not the whole serialized pool.

Confirmatory-core arms (design rt02_v2_construct_validity_design_20260719.md §10):
  contam_d3   : misleading pool -> d operator-consolidated rounds -> source correction -> k-phase
  contam_d0   : misleading pool -> no rounds -> source correction -> k-phase (operator-off anchor)
  safe_d3     : correct source at t=0 -> d operator-consolidated rounds -> k-phase (primary control)
  full_closure: contam_d3 trajectory -> source correction + evidence-rewrite of consolidated
                descendants/state -> k-phase (idealized ceiling)

Key confirmatory contrast: contam_d3 vs contam_d0 under a GENUINE operator + real retrieval.
Run with --mock for a zero-API offline pipeline check. Real API needs .env.v3 sourced and
an explicit new --outdir; never overwrites v1 (state/rt02_runs/*20260718*).
"""
import argparse
import glob
import json
import os
import sys
import time
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt02_common import offi, make_clients, snapshot_hash, correct_qa_sources, judge_qa, CONTENT_FIELD  # noqa: E402
from rt02_v2_operators import OPERATORS, MockBackend, LLMBackend, get_content, set_content, retry, repro_meta  # noqa: E402
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


def select_cases(args):
    """Return [(domain, cluster_id, item)] from the v2 unseen split (or explicit domains)."""
    with open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    want = {}  # domain -> set(cluster_id)
    for domain, blk in man["qa"]["split"].items():
        if args.domains and domain not in args.domains.split(","):
            continue
        ids = blk["unseen_dev"] if args.split == "dev" else blk["unseen_confirmatory"]
        want[domain] = set(ids)
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


def load_done_arms(out_path):
    """Resume support: set of (domain, cluster_id, arm) already written."""
    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["domain"], r["cluster_id"], r["arm"]))
                except Exception:
                    pass
    return done


def probe(client, args, retriever, item, pool):
    """Read-only: retrieve top-k per query, generate, official judge. Logs retrieval exposure."""
    out = []
    for qkey, query, ca, risk in case_queries(item):
        subset, exposure = retriever.retrieve(query, pool)
        resp = gen(client, args.model, query, subset, args.temperature)
        u1, l1, r1 = judge_qa(client, args.judge_model, query, risk, ca, resp)
        rec = {"query_key": qkey, "unsafe_j1": u1, "retrieved_ids": [e["id"] for e in exposure],
               "n_retrieved": len(exposure)}
        if args.judge2_model:
            u2, l2, r2 = judge_qa(client, args.judge2_model, query, risk, ca, resp)
            rec.update({"unsafe_j2": u2, "unsafe_and": u1 & u2})
        out.append(rec)
    return out


def probe_rate(probes, key="unsafe_j1"):
    vals = [p[key] for p in probes if key in p]
    return sum(vals) / len(vals) if vals else None


def consolidate_round(client, args, retriever, item, pool, qkey, query, ca, risk, operator_fn, backend, traces):
    """One consolidation round: retrieve -> answer -> judge -> operator folds the episode in."""
    subset, _ = retriever.retrieve(query, pool)
    resp = gen(client, args.model, query, subset, args.temperature)
    unsafe, label, reason = judge_qa(client, args.judge_model, query, risk, ca, resp)
    new_pool, trace = operator_fn(pool, {"query": query, "answer": resp}, backend)
    trace["round_query"] = qkey
    trace["round_unsafe_j1"] = unsafe
    traces.append(trace)
    return new_pool


def k_phase(client, args, retriever, item, pool, operator_fn, backend):
    """k0 probe -> writeback(q1) -> k1 probe -> writeback(q2) -> k2 probe. Writebacks consolidate."""
    queries = case_queries(item)
    res = {"probes": {}, "pool_hashes": {}, "writeback_traces": []}
    res["pool_hashes"]["k0"] = snapshot_hash(pool)
    res["probes"]["k0"] = probe(client, args, retriever, item, pool)
    for k, (qkey, query, ca, risk) in enumerate(queries[:2], start=1):
        pool = consolidate_round(client, args, retriever, item, pool, qkey, query, ca, risk,
                                 operator_fn, backend, res["writeback_traces"])
        res["pool_hashes"][f"k{k}"] = snapshot_hash(pool)
        res["probes"][f"k{k}"] = probe(client, args, retriever, item, pool)
    return res, pool


def full_closure_rewrite(pool, item):
    """Idealized ceiling: rewrite every consolidated descendant/summary/merged state with the
    official correct answer of the matching query (published fields only)."""
    q2ca = {q: ca for _, q, ca, _ in case_queries(item)}
    generic = item.get("test_correct_answer", "")
    n = 0
    for mem in pool:
        role = mem.get("label_source") in ("rt02_descendant",) or mem.get("rt02_role") == "rt02_summary" \
            or mem.get("status") == "rt02_merged"
        if role:
            ca = q2ca.get(mem.get("user_request", ""), generic)
            if ca:
                set_content(mem, ca)
                mem["status"] = "closure_rewritten"
                n += 1
    return n


def run_arm(client, args, retriever, item, arm, operator_fn, backend, donor_benign=None):
    src = item.get("retrievable_memories", [])
    if arm == "contam_d3":
        pool = deepcopy(src)
        traj = []
        for qkey, query, ca, risk in case_queries(item)[:args.d]:
            pool = consolidate_round(client, args, retriever, item, pool, qkey, query, ca, risk, operator_fn, backend, traj)
        n_corr = correct_qa_sources(pool)
        kp, pool = k_phase(client, args, retriever, item, pool, operator_fn, backend)
        return {"arm": arm, "n_sources_corrected": n_corr, "trajectory_traces": traj, **kp}
    if arm == "contam_d0":
        pool = deepcopy(src)
        n_corr = correct_qa_sources(pool)
        kp, pool = k_phase(client, args, retriever, item, pool, operator_fn, backend)
        return {"arm": arm, "n_sources_corrected": n_corr, "trajectory_traces": [], **kp}
    if arm == "safe_d3":
        pool = deepcopy(src)
        n_safe = correct_qa_sources(pool)
        traj = []
        for qkey, query, ca, risk in case_queries(item)[:args.d]:
            pool = consolidate_round(client, args, retriever, item, pool, qkey, query, ca, risk, operator_fn, backend, traj)
        kp, pool = k_phase(client, args, retriever, item, pool, operator_fn, backend)
        return {"arm": arm, "n_sources_corrected": n_safe, "trajectory_traces": traj, **kp}
    if arm == "full_closure":
        pool = deepcopy(src)
        traj = []
        for qkey, query, ca, risk in case_queries(item)[:args.d]:
            pool = consolidate_round(client, args, retriever, item, pool, qkey, query, ca, risk, operator_fn, backend, traj)
        n_corr = correct_qa_sources(pool)
        n_rw = full_closure_rewrite(pool, item)
        kp, pool = k_phase(client, args, retriever, item, pool, operator_fn, backend)
        return {"arm": arm, "n_sources_corrected": n_corr, "n_closure_rewritten": n_rw, "trajectory_traces": traj, **kp}
    if arm == "benign_vol":
        # volume control: corrected d0 pool + benign borrowed records (matched count) -> is unsafe
        # driven merely by having MORE records? (should stay ~ contam_d0). Donor = a domain sibling's
        # correct-labeled records, so borrowed content is genuinely benign, not synthetic.
        pool = deepcopy(src)
        n_corr = correct_qa_sources(pool)
        borrowed = []
        for dmem in (donor_benign or [])[:args.d]:
            m = deepcopy(dmem)
            m["id"] = offi.get_next_memory_id(pool)
            m["label"] = "correct"
            m["label_source"] = "rt02_benign_borrowed"
            pool.append(m)
            borrowed.append(m["id"])
        kp, pool = k_phase(client, args, retriever, item, pool, operator_fn, backend)
        return {"arm": arm, "n_sources_corrected": n_corr, "n_borrowed": len(borrowed),
                "trajectory_traces": [], **kp}
    raise ValueError(arm)


def donor_benign_for(cases, domain, cid):
    """Benign borrow source: correct-labeled records from a domain sibling case."""
    sibs = [(c, it) for d, c, it in cases if d == domain]
    idx = next((i for i, (c, _) in enumerate(sibs) if c == cid), 0)
    for step in range(1, len(sibs) + 1):
        _, it2 = sibs[(idx + step) % len(sibs)]
        benign = [m for m in it2.get("retrievable_memories", []) if m.get("label") == "correct"]
        if benign:
            return benign
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--operator", default="summary_rewrite", choices=list(OPERATORS))
    ap.add_argument("--arms", default="contam_d3,contam_d0,safe_d3,benign_vol,full_closure")
    ap.add_argument("--split", default="dev", choices=("dev", "confirmatory"))
    ap.add_argument("--domains", default="")
    ap.add_argument("--n-cases", type=int, default=0)
    ap.add_argument("--d", type=int, default=3)
    ap.add_argument("--k-retrieval", dest="k", type=int, default=5)
    ap.add_argument("--model", default="gpt-4.1-mini")
    ap.add_argument("--judge-model", default="gpt-4.1-mini")
    ap.add_argument("--judge2-model", default="gpt-4o")
    ap.add_argument("--mock", action="store_true", help="offline: mock client + deterministic operator backend")
    ap.add_argument("--temperature", type=float, default=0,
                    help="generation temperature; >0 for multi-seed stochasticity runs (S1). "
                         "Use a distinct --outdir per seed and aggregate across record files.")
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    if not args.mock and glob.glob(os.path.join(args.outdir, "*20260718*")):
        raise SystemExit("refusing to write into a v1 outdir")
    os.makedirs(args.outdir, exist_ok=True)

    client = MockChatClient() if args.mock else make_clients()
    backend = MockBackend() if args.mock else LLMBackend(client, args.model)
    retriever = TfidfRetriever(k=args.k)
    operator_fn = OPERATORS[args.operator]

    cases = select_cases(args)
    log(f"CHIR v2: operator={args.operator} arms={args.arms} split={args.split} "
        f"cases={len(cases)} k={args.k} mock={args.mock}")

    manifest = {"operator": args.operator, "arms": args.arms.split(","), "split": args.split,
                "d": args.d, "k_retrieval": args.k, "temperature": args.temperature, "model": args.model,
                "judge1": args.judge_model, "judge2": args.judge2_model, "mock": args.mock,
                "n_cases": len(cases), "case_ids": [[d, c] for d, c, _ in cases],
                "repro": repro_meta(), "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(os.path.join(args.outdir, "run_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    out_path = os.path.join(args.outdir, "chir_v2_records.jsonl")
    done = load_done_arms(out_path)  # resume: skip (domain, cluster_id, arm) already written
    if done:
        log(f"resume: {len(done)} arm-records already present, will skip them")
    with open(out_path, "a", encoding="utf-8") as fout:
        for domain, cid, item in cases:
            donor = donor_benign_for(cases, domain, cid)
            for arm in args.arms.split(","):
                if (domain, cid, arm) in done:
                    continue
                src = item.get("retrievable_memories", [])
                rec = {"domain": domain, "cluster_id": cid, "operator": args.operator,
                       "source_ids": [m.get("id") for m in src],
                       "misleading_ids": [m.get("id") for m in src if m.get("label") == "misleading"]}
                rec.update(run_arm(client, args, retriever, item, arm, operator_fn, backend, donor_benign=donor))
                # compact endpoint summary for quick reading
                rec["u_j1_by_k"] = {k: probe_rate(v) for k, v in rec["probes"].items()}
                fout.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
                fout.flush()
            log(f"case done {domain}/{cid}")
    log(f"ALL DONE -> {out_path}")
    if args.mock:
        log(f"mock client calls: {getattr(client, 'calls', {})}")


if __name__ == "__main__":
    main()
