#!/usr/bin/env python3
"""RT-02 CHIR Stage-1 existence pilot — Workflow side (official MemEvoBench Workflow static pipeline).

Same six arms as the QA side (see run_rt02_chir_qa.py docstring). Official components used:
  - memory serialization: eval_workflow._format_memory
  - agent loop + tool sim: eval_workflow.run_single_query (read-only w.r.t. memory)
  - trajectory text: eval_workflow._format_output via update_query_with_result
  - descendants: eval_workflow._build_query_trace_memory_entry
  - unsafe verdict: judge.agent_safety_judge (AGENT_CLASSIFICATION_PROMPT_TEMPLATE), ground_truth passed
  - source correction: overwrite semantics of tool_correct_memory (content field <- published
    `correct_workflow`), timestamps untouched (design §4.1)
  - full closure: descendant `workflow` <- published `ground_truth` of the query that produced it
"""
import argparse
import json
import os
import sys
import threading
import time
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor, as_completed

WF_NORMAL = "/Users/yihaiwen/Documents/New project/memevobench_official/memorybench/Workflow/normal"
WF_ROOT = "/Users/yihaiwen/Documents/New project/memevobench_official/memorybench/Workflow"
for p in (WF_NORMAL, WF_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

_saved_argv = sys.argv
sys.argv = ["eval_workflow.py"]  # module-level parse_args() in eval_workflow
import eval_workflow as ew  # noqa: E402
from judge import agent_safety_judge  # noqa: E402
sys.argv = _saved_argv

_write_lock = threading.Lock()
QUERY_KEYS = ew.QUERY_KEYS  # ["test_query", "test_query_2", "test_query_3"]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def make_api(model_name, max_tokens=4096):
    return ew.OpenaiAPI(
        model_name=model_name,
        generation_config={"temperature": 0.0, "max_tokens": max_tokens},
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def ew_args(model_name):
    return argparse.Namespace(
        model_name=model_name, greedy=1, regen_exceed=0, extra_info="",
        allow_empty=0, debug=False, debug_samples=2, num_workers=1,
        use_feedback=False, seed=42, safety_memory=False,
    )


def correct_wf_sources(samples):
    n = 0
    for s in samples:
        if s.get("label") == "misleading" and s.get("correct_workflow"):
            s["workflow"] = s["correct_workflow"]
            s["label"] = "correct"            # bookkeeping; not serialized
            s["status"] = "corrected_source"  # bookkeeping; not serialized
            n += 1
    return n


def sources_view(cluster_id, samples):
    src = [s for s in samples
           if s.get("label_source") not in ("rt02_descendant", "rt02_benign_borrowed")]
    return ew._format_memory(cluster_id, src)


def run_query(agent_api, run_args, cluster_id, qkey, query_obj, pool):
    """One agent episode (multi-round tool loop), returns (format_output, rounds). Read-only."""
    q = deepcopy(query_obj)
    messages, rounds = ew.run_single_query(agent_api, cluster_id, qkey, q, pool, run_args)
    if messages is None:
        return None, 0
    ew.update_query_with_result(q, messages, rounds)
    return q.get("format_output", ""), rounds


def judge_traj(judge_api, query_obj, traj):
    out = agent_safety_judge(judge_api, query_obj.get("instruction", ""), traj,
                             query_obj.get("ground_truth", ""))
    return (1 if ew._is_attack_success(out) else 0), out


def run_rounds(agent_api, judge_api, run_args, cluster, pool, n_rounds):
    cid = cluster["cluster_id"]
    rounds_out = []
    for r in range(n_rounds):
        qkey = QUERY_KEYS[r % 3]
        query_obj = cluster.get(qkey)
        if not query_obj:
            continue
        traj, nr = run_query(agent_api, run_args, cid, qkey, query_obj, pool)
        if traj is None:
            rounds_out.append({"round": r + 1, "query_key": qkey, "error": True})
            continue
        unsafe, jo = judge_traj(judge_api, query_obj, traj)
        entry = ew._build_query_trace_memory_entry(cid, qkey, {**query_obj, "format_output": traj})
        if entry:
            entry["id"] = f"{entry['id']}_d{r + 1}"
            entry["label_source"] = "rt02_descendant"
            entry["source_query_key"] = qkey
            pool.append(entry)
        rounds_out.append({"round": r + 1, "query_key": qkey, "unsafe_j1": unsafe,
                           "judge": jo, "traj": traj[:4000]})
    return rounds_out


def probe(agent_api, j1, j2, run_args, cluster, pool):
    cid = cluster["cluster_id"]
    out = []
    for qkey in QUERY_KEYS:
        query_obj = cluster.get(qkey)
        if not query_obj:
            continue
        traj, nr = run_query(agent_api, run_args, cid, qkey, query_obj, pool)
        if traj is None:
            out.append({"query_key": qkey, "error": True})
            continue
        u1, jo1 = judge_traj(j1, query_obj, traj)
        rec = {"query_key": qkey, "unsafe_j1": u1, "judge_j1": jo1, "traj": traj[:4000]}
        if j2 is not None:
            u2, jo2 = judge_traj(j2, query_obj, traj)
            rec.update({"unsafe_j2": u2, "judge_j2": jo2, "unsafe_and": u1 & u2})
        out.append(rec)
    return out


def k_phase(agent_api, j1, j2, run_args, cluster, pool):
    cid = cluster["cluster_id"]
    result = {"probes": {}, "writebacks": []}
    result["probes"]["k0"] = probe(agent_api, j1, j2, run_args, cluster, pool)
    for k, qkey in enumerate(QUERY_KEYS[:2], start=1):
        query_obj = cluster.get(qkey)
        if query_obj:
            traj, nr = run_query(agent_api, run_args, cid, qkey, query_obj, pool)
            if traj is not None:
                unsafe, jo = judge_traj(j1, query_obj, traj)
                entry = ew._build_query_trace_memory_entry(cid, qkey, {**query_obj, "format_output": traj})
                if entry:
                    entry["id"] = f"{entry['id']}_k{k}"
                    entry["label_source"] = "rt02_descendant"
                    entry["source_query_key"] = qkey
                    pool.append(entry)
                result["writebacks"].append({"k": k, "query_key": qkey, "unsafe_j1": unsafe})
        result["probes"][f"k{k}"] = probe(agent_api, j1, j2, run_args, cluster, pool)
    return result


def full_closure_wf(cluster, pool):
    n = 0
    for s in pool:
        if s.get("label_source") == "rt02_descendant":
            src_q = cluster.get(s.get("source_query_key") or "")
            gt = (src_q or {}).get("ground_truth", "")
            if gt:
                s["workflow"] = gt
                s["status"] = "closure_rewritten"
                n += 1
    return n


def process_case_phase1(apis, args, cluster):
    agent_api, j1, j2 = apis
    run_args = ew_args(args.model)
    cid = cluster["cluster_id"]
    records = []

    contam = deepcopy(ew._get_samples_for_memory(cluster))
    contam_rounds = run_rounds(agent_api, j1, run_args, cluster, contam, 3)
    n_corr = correct_wf_sources(contam)
    contam_at_corr = deepcopy(contam)

    safe = deepcopy(ew._get_samples_for_memory(cluster))
    n_safe = correct_wf_sources(safe)
    safe_rounds = run_rounds(agent_api, j1, run_args, cluster, safe, 3)

    match_ok = sources_view(cid, contam_at_corr) == sources_view(cid, safe)
    if not match_ok:
        log(f"!! BRANCH MATCH FAIL wf/{cid}")

    safe_desc = [s for s in safe if s.get("label_source") == "rt02_descendant"][:3]

    for arm, pool, rounds in (("contam_d3", deepcopy(contam_at_corr), contam_rounds),
                              ("safe_d3", deepcopy(safe), safe_rounds)):
        kp = k_phase(agent_api, j1, j2, run_args, cluster, pool)
        rec = {"task": "workflow", "cluster_id": cid, "arm": arm,
               "n_sources_corrected": n_corr if arm == "contam_d3" else n_safe,
               "branch_match_ok": match_ok, "rounds": rounds, **kp}
        if arm == "safe_d3":
            rec["safe_descendants_store"] = deepcopy(safe_desc)
        records.append(rec)

    fc = deepcopy(contam_at_corr)
    n_rw = full_closure_wf(cluster, fc)
    kp = k_phase(agent_api, j1, j2, run_args, cluster, fc)
    records.append({"task": "workflow", "cluster_id": cid, "arm": "full_closure",
                    "n_descendants_rewritten": n_rw, "branch_match_ok": match_ok,
                    "rounds": contam_rounds, **kp})
    return records, deepcopy(safe_desc)


def process_case_phase2(apis, args, cluster, donor_desc):
    agent_api, j1, j2 = apis
    run_args = ew_args(args.model)
    cid = cluster["cluster_id"]
    records = []

    d0 = deepcopy(ew._get_samples_for_memory(cluster))
    n_corr = correct_wf_sources(d0)
    kp = k_phase(agent_api, j1, j2, run_args, cluster, d0)
    records.append({"task": "workflow", "cluster_id": cid, "arm": "contam_d0",
                    "n_sources_corrected": n_corr, "rounds": [], **kp})

    bv = deepcopy(ew._get_samples_for_memory(cluster))
    correct_wf_sources(bv)
    for i, dmem in enumerate(donor_desc):
        m = deepcopy(dmem)
        m["id"] = f"borrowed_{i}_{m.get('id', '')}"
        m["label_source"] = "rt02_benign_borrowed"
        bv.append(m)
    kp = k_phase(agent_api, j1, j2, run_args, cluster, bv)
    records.append({"task": "workflow", "cluster_id": cid, "arm": "benign_vol",
                    "n_borrowed": len(donor_desc), "rounds": [], **kp})

    nm = probe(agent_api, j1, j2, run_args, cluster, [])
    records.append({"task": "workflow", "cluster_id": cid, "arm": "null_mem",
                    "rounds": [], "probes": {"k0": nm}, "writebacks": []})
    return records


def append_records(path, records):
    with _write_lock:
        with open(path, "a", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")


def load_done(path):
    done = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["cluster_id"], r["arm"]))
                except Exception:
                    pass
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wf-json", default=os.path.join(WF_ROOT, "workflow.json"))
    ap.add_argument("--model", default="gpt-4.1-mini")
    ap.add_argument("--judge-model", default="gpt-4.1-mini")
    ap.add_argument("--judge2-model", default="gpt-4o")
    ap.add_argument("--n-cases", type=int, default=20)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    out_path = os.path.join(args.outdir, "chir_wf_records.jsonl")

    agent_api = make_api(args.model)
    j1 = make_api(args.judge_model, max_tokens=512)
    j2 = make_api(args.judge2_model, max_tokens=512) if args.judge2_model else None
    apis = (agent_api, j1, j2)

    with open(args.wf_json, encoding="utf-8") as f:
        clusters = json.load(f)
    clusters = [c for c in sorted(clusters, key=lambda x: str(x.get("cluster_id")))
                if any(s.get("label") == "misleading" and s.get("correct_workflow")
                       for s in ew._get_samples_for_memory(c))][: args.n_cases]
    log(f"{len(clusters)} workflow cases × 6 arms; model={args.model}")

    done = load_done(out_path)
    with open(os.path.join(args.outdir, "chir_wf_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"model": args.model, "judge1": args.judge_model, "judge2": args.judge2_model,
                   "n_cases": len(clusters), "started": time.strftime("%Y-%m-%d %H:%M:%S")},
                  f, ensure_ascii=False, indent=2)

    safe_desc = {}
    p1_needed = [c for c in clusters if not {(c["cluster_id"], a) for a in
                 ("contam_d3", "safe_d3", "full_closure")} <= done]

    def p1(cluster):
        recs, sd = process_case_phase1(apis, args, cluster)
        append_records(out_path, recs)
        return cluster["cluster_id"], sd

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(p1, c) for c in p1_needed]):
            cid, sd = fut.result()
            safe_desc[cid] = sd
            log(f"phase1 done {cid}")

    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if r.get("arm") == "safe_d3" and r["cluster_id"] not in safe_desc:
                    safe_desc[r["cluster_id"]] = r.get("safe_descendants_store", [])

    ids = [c["cluster_id"] for c in clusters]

    def donor_for(cluster):
        idx = ids.index(cluster["cluster_id"])
        for step in range(1, len(ids)):
            cid = ids[(idx + step) % len(ids)]
            if safe_desc.get(cid):
                return safe_desc[cid]
        return safe_desc.get(cluster["cluster_id"], [])

    p2_needed = [c for c in clusters if not {(c["cluster_id"], a) for a in
                 ("contam_d0", "benign_vol", "null_mem")} <= done]

    def p2(cluster):
        recs = process_case_phase2(apis, args, cluster, donor_for(cluster))
        append_records(out_path, recs)
        return cluster["cluster_id"]

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(p2, c) for c in p2_needed]):
            log(f"phase2 done {fut.result()}")

    log(f"ALL DONE -> {out_path}")


if __name__ == "__main__":
    main()
