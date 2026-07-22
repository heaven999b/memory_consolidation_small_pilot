#!/usr/bin/env python3
"""RT-02 v2 Phase-0 manifest builder (READ-ONLY, no API).

Enumerates every MemEvoBench case USED by RT-02 v1 (CHIR qa/wf + RQ4, PairGain
qa/wf) and every official case AVAILABLE, then carves the completely-unseen
remainder into a stable v2 development / confirmatory split.

Output: state/rt02_v1_used_cases_manifest.json

Design: state/rt02_v2_construct_validity_design_20260719.md §1.
Rule: a case is "unseen" only if it was never touched by any v1 run. WF cluster_id
is non-unique (known v1 bug), so a WF row counts as USED if EITHER its absolute
row OR its cluster_id was touched -> conservative, never leaks a used case into v2.
"""
import glob
import hashlib
import json
import os
import re

ROOT = "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
MEMEVO = "/Users/yihaiwen/Documents/New project/memevobench_official"
QA_GLOB = os.path.join(MEMEVO, "memorybench", "QA", "*_memory_triplequery.json")
WF_JSON = os.path.join(MEMEVO, "memorybench", "Workflow", "workflow.json")

V1_RECORD_FILES = {
    "chir_qa": "state/rt02_runs/chir_qa_20260718/chir_qa_records.jsonl",
    "chir_wf": "state/rt02_runs/chir_wf_20260718/chir_wf_records.jsonl",
    "chir_rq4": "state/rt02_runs/chir_rq4_qa_20260718/chir_rq4_qa_records.jsonl",
    "pairgain_qa": "state/rt02_runs/pairgain_qa_20260718/pairgain_qa_records.jsonl",
    "pairgain_wf": "state/rt02_runs/pairgain_wf_20260718_v2/pairgain_wf_records.jsonl",
}

SPLIT_DEV_PCT = 35  # sha256 bucket < 35 -> dev, else confirmatory (biases toward confirmatory)


def load_jsonl(path):
    out = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        pass
    return out


def sha_bucket(key):
    return int(hashlib.sha256(key.encode("utf-8")).hexdigest(), 16) % 100


def official_qa():
    """{domain: sorted[cluster_id]}."""
    out = {}
    for path in sorted(glob.glob(QA_GLOB)):
        domain = os.path.basename(path).split("_memory_triplequery")[0]
        with open(path, encoding="utf-8") as f:
            items = json.load(f)
        out[domain] = sorted({it.get("cluster_id") for it in items if it.get("cluster_id") is not None},
                             key=lambda x: (str(type(x)), x))
    return out


def official_wf():
    """[{row, cluster_id, env}] indexed by absolute row in workflow.json."""
    rows = []
    if os.path.exists(WF_JSON):
        with open(WF_JSON, encoding="utf-8") as f:
            items = json.load(f)
        for i, it in enumerate(items):
            rows.append({"row": i, "cluster_id": it.get("cluster_id"),
                         "env": it.get("env") or it.get("environment") or it.get("scenario")})
    return rows


def collect_used():
    """Return (used_qa {domain:set(cluster)}, used_wf_rows set, used_wf_clusters set, key_report)."""
    used_qa, used_wf_rows, used_wf_clusters = {}, set(), set()
    report = {}
    for tag, rel in V1_RECORD_FILES.items():
        recs = load_jsonl(os.path.join(ROOT, rel))
        report[tag] = {"n_records": len(recs),
                       "keys_sample": sorted(recs[0].keys())[:12] if recs else []}
        for r in recs:
            domain = r.get("domain")
            cid = r.get("cluster_id")
            if "wf" in tag:
                if cid is not None:
                    used_wf_clusters.add(str(cid))
                ck = str(r.get("case_key", ""))
                m = re.match(r"wf_row_(\d+)_cluster_(.+)", ck)
                if m:
                    used_wf_rows.add(int(m.group(1)))
            else:
                if domain is not None and cid is not None:
                    used_qa.setdefault(domain, set()).add(cid)
    return used_qa, used_wf_rows, used_wf_clusters, report


def main():
    off_qa = official_qa()
    off_wf = official_wf()
    used_qa, used_wf_rows, used_wf_clusters, key_report = collect_used()

    # ---- QA unseen + split ----
    qa_split = {}
    qa_counts = {}
    for domain, clusters in off_qa.items():
        used = used_qa.get(domain, set())
        unseen = [c for c in clusters if c not in used]
        dev, conf = [], []
        for c in unseen:
            (dev if sha_bucket(f"qa|{domain}|{c}") < SPLIT_DEV_PCT else conf).append(c)
        qa_split[domain] = {"used": sorted(used, key=str), "unseen_dev": dev, "unseen_confirmatory": conf}
        qa_counts[domain] = {"official": len(clusters), "used": len(used),
                             "unseen": len(unseen), "dev": len(dev), "confirmatory": len(conf)}

    # ---- WF unseen + split (conservative: used if row OR cluster touched) ----
    wf_dev, wf_conf, wf_used = [], [], []
    for wrow in off_wf:
        row, cid = wrow["row"], str(wrow["cluster_id"])
        if row in used_wf_rows or cid in used_wf_clusters:
            wf_used.append(wrow)
        else:
            key = f"wf|{row}|{cid}"
            (wf_dev if sha_bucket(key) < SPLIT_DEV_PCT else wf_conf).append(wrow)

    manifest = {
        "generated": "2026-07-19",
        "design": "state/rt02_v2_construct_validity_design_20260719.md",
        "rule": "unseen QA case = cluster_id never used in that domain; unseen WF row = "
                "neither its absolute row nor its cluster_id ever touched (conservative, "
                "cluster_id non-unique). Split: sha256(key)%100 < 35 -> dev else confirmatory.",
        "split_dev_pct": SPLIT_DEV_PCT,
        "v1_record_key_report": key_report,
        "qa": {
            "counts": qa_counts,
            "totals": {
                "official": sum(v["official"] for v in qa_counts.values()),
                "used": sum(v["used"] for v in qa_counts.values()),
                "unseen": sum(v["unseen"] for v in qa_counts.values()),
                "dev": sum(v["dev"] for v in qa_counts.values()),
                "confirmatory": sum(v["confirmatory"] for v in qa_counts.values()),
            },
            "split": qa_split,
        },
        "wf": {
            "counts": {"official": len(off_wf), "used": len(wf_used),
                       "unseen": len(wf_dev) + len(wf_conf), "dev": len(wf_dev),
                       "confirmatory": len(wf_conf)},
            "used_rows": sorted(used_wf_rows), "used_clusters": sorted(used_wf_clusters),
            "unseen_dev": wf_dev, "unseen_confirmatory": wf_conf,
        },
    }

    out_path = os.path.join(ROOT, "state", "rt02_v1_used_cases_manifest.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, default=str)

    print("=== v1 record key report ===")
    for tag, rep in key_report.items():
        print(f"  {tag}: {rep['n_records']} records; keys={rep['keys_sample']}")
    print("=== QA totals ===", json.dumps(manifest["qa"]["totals"], ensure_ascii=False))
    for d, c in qa_counts.items():
        print(f"  {d}: official={c['official']} used={c['used']} unseen={c['unseen']} "
              f"(dev={c['dev']} conf={c['confirmatory']})")
    print("=== WF counts ===", json.dumps(manifest["wf"]["counts"], ensure_ascii=False))
    print(f"-> {out_path}")


if __name__ == "__main__":
    main()
