#!/usr/bin/env python3
"""RT-02 PairGain MVP — Workflow side. Correct/misleading synchronized branches, t=0..3.
Same protocol as run_rt02_pairgain_qa.py, on the official Workflow static pipeline."""
import argparse
import json
import os
import sys
import threading
import time
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_rt02_chir_wf as cw  # noqa: E402  (brings ew, judge, helpers; import is argv-safe)
from run_rt02_pairgain_qa import trustmem_style_score, probe_rates  # noqa: E402
from rt02_common import make_clients, snapshot_hash  # noqa: E402

_write_lock = threading.Lock()
ew = cw.ew
QUERY_KEYS = cw.QUERY_KEYS


def process_case(apis, raw_client, args, case, snap_dir):
    agent_api, j1, j2 = apis
    run_args = cw.ew_args(args.model)
    cluster = case["cluster"]
    cid = cluster["cluster_id"]
    case_key = case["case_key"]

    minus = deepcopy(ew._get_samples_for_memory(cluster))
    plus = deepcopy(ew._get_samples_for_memory(cluster))
    n_corr = cw.correct_wf_sources(plus)

    pairs = [{"m": s.get("workflow", ""), "c": s.get("correct_workflow", "")}
             for s in ew._get_samples_for_memory(cluster)
             if s.get("label") == "misleading" and s.get("correct_workflow")]

    rec = {"task": "workflow", "case_key": case_key, "cluster_id": cid,
           "n_sources_corrected": n_corr,
           "pairs": pairs, "steps": [], "trustmem_style": []}

    def snap(tag, pool):
        # MemEvoBench workflow.json can contain distinct cases with the same
        # official cluster_id.  case_key is the stable selected-row identity;
        # cluster_id remains untouched for calls into the official pipeline.
        path = os.path.join(snap_dir, f"{case_key}_{tag}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pool, f, ensure_ascii=False, default=str)
        return {"path": os.path.relpath(path, snap_dir), "hash": snapshot_hash(pool)}

    step0 = {"t": 0, "minus_snap": snap("minus_t0", minus), "plus_snap": snap("plus_t0", plus),
             "minus_probe": probe_rates(cw.probe(agent_api, j1, j2, run_args, cluster, minus)),
             "plus_probe": probe_rates(cw.probe(agent_api, j1, j2, run_args, cluster, plus))}
    rec["steps"].append(step0)

    for t in range(1, 4):
        qkey = QUERY_KEYS[(t - 1) % 3]
        query_obj = cluster.get(qkey)
        step = {"t": t, "query_key": qkey}
        pre_minus_view = ew._format_memory(cid, minus)
        for name, pool in (("minus", minus), ("plus", plus)):
            traj, nr = cw.run_query(agent_api, run_args, cid, qkey, query_obj, pool)
            if traj is None:
                step[f"{name}_round"] = {"error": True}
                continue
            unsafe, jo = cw.judge_traj(j1, query_obj, traj)
            entry = ew._build_query_trace_memory_entry(cid, qkey, {**query_obj, "format_output": traj})
            if entry:
                entry["id"] = f"{entry['id']}_t{t}"
                entry["label_source"] = "rt02_descendant"
                entry["source_query_key"] = qkey
                pool.append(entry)
            step[f"{name}_round"] = {"unsafe_j1": unsafe, "traj": traj[:4000]}
        post_minus_view = ew._format_memory(cid, minus)
        rec["trustmem_style"].append({"t": t, **trustmem_style_score(
            raw_client, args.judge_model, pre_minus_view,
            (query_obj or {}).get("instruction", ""),
            (step.get("minus_round") or {}).get("traj", ""), post_minus_view)})
        step["minus_snap"] = snap(f"minus_t{t}", minus)
        step["plus_snap"] = snap(f"plus_t{t}", plus)
        step["minus_probe"] = probe_rates(cw.probe(agent_api, j1, j2, run_args, cluster, minus))
        step["plus_probe"] = probe_rates(cw.probe(agent_api, j1, j2, run_args, cluster, plus))
        rec["steps"].append(step)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wf-json", default=os.path.join(cw.WF_ROOT, "workflow.json"))
    ap.add_argument("--model", default="gpt-4.1-mini")
    ap.add_argument("--judge-model", default="gpt-4.1-mini")
    ap.add_argument("--judge2-model", default="gpt-4o")
    ap.add_argument("--n-cases", type=int, default=30)
    ap.add_argument("--skip-first", type=int, default=20,
                    help="skip the first N clusters (avoid overlap with CHIR cases)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    snap_dir = os.path.join(args.outdir, "snapshots")
    os.makedirs(snap_dir, exist_ok=True)
    out_path = os.path.join(args.outdir, "pairgain_wf_records.jsonl")

    agent_api = cw.make_api(args.model)
    j1 = cw.make_api(args.judge_model, max_tokens=512)
    j2 = cw.make_api(args.judge2_model, max_tokens=512) if args.judge2_model else None
    raw_client = make_clients()

    with open(args.wf_json, encoding="utf-8") as f:
        clusters = json.load(f)
    clusters = [c for c in sorted(clusters, key=lambda x: str(x.get("cluster_id")))
                if any(s.get("label") == "misleading" and s.get("correct_workflow")
                       for s in ew._get_samples_for_memory(c))]
    selected = clusters[args.skip_first: args.skip_first + args.n_cases]
    cases = [
        {
            "cluster": cluster,
            "case_key": f"wf_row_{args.skip_first + offset:04d}_cluster_{cluster['cluster_id']}",
        }
        for offset, cluster in enumerate(selected)
    ]
    cw.log(f"PairGain WF: {len(cases)} cases; model={args.model}")

    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    done.add(rec.get("case_key") or str(rec["cluster_id"]))
                except Exception:
                    pass
    todo = [case for case in cases if case["case_key"] not in done]

    with open(os.path.join(args.outdir, "pairgain_wf_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"model": args.model, "judge1": args.judge_model, "judge2": args.judge2_model,
                   "n_cases": len(cases), "case_key_version": 2,
                   "started": time.strftime("%Y-%m-%d %H:%M:%S")},
                  f, ensure_ascii=False, indent=2)

    def run_one(case):
        rec = process_case((agent_api, j1, j2), raw_client, args, case, snap_dir)
        with _write_lock:
            with open(out_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        return case["case_key"]

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(run_one, case) for case in todo]):
            cw.log(f"case done {fut.result()}")
    cw.log(f"ALL DONE -> {out_path}")


if __name__ == "__main__":
    main()
