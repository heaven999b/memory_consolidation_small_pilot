#!/usr/bin/env python3
"""RT-02 v2 PairGain stats — does G predict the FUTURE held-out endpoint beyond current state?

This is the R4-fixed test: the outcome Y is the paired unsafe effect on the HELD-OUT endpoint
query (never written back), predicted from G(t) while controlling current state A(t),D(t),D(t+1).
v1 predicted A(t+1) on reused construction queries (leakage + autocorrelation); v2 predicts a
future the construction path never touched.

Inputs: pairgain_v2_records.jsonl (A series per step from the held-out endpoint) + an NLI file
from rt02_v2_nli.py (lineage-local D/G, frozen primary mode=source_only). Reuses the v1 stat
machinery (partial Spearman, grouped CV, case bootstrap). Offline, no API.

Verdict RQ1 GO iff partial Spearman(G, future-A | current) case-bootstrap CI>0, eps-grid sign
consistent, and joint beats current-only held-out. Design §10 / confirmatory config §5.
"""
import argparse
import json
import random
import sys
import os
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rt02_pairgain_stats import cv_scores, partial_spearman, bootstrap_partial  # noqa: E402

PRIMARY_EPS = "0.05"
FEATURE_SETS = {  # RQ2 salvage: G vs constructible/ calibrated baselines (not degenerate TrustMem)
    "current_only": ["A_t", "D_t", "D_t1"],
    "verifier_only": ["v_cov", "v_pre", "v_fai"],   # calibrated transition verifier (RQ2 baseline)
    "g_only": ["G_t"],
    "joint": ["A_t", "D_t", "D_t1", "G_t"],          # G over current-state (RQ1)
    "joint_all": ["A_t", "D_t", "D_t1", "v_cov", "v_pre", "v_fai", "G_t"],  # G over current + verifier (RQ2)
}


def load(paths):
    out = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
    return out


def build_rows(records, nli_rows, eps=PRIMARY_EPS, mode="source_only", horizon=1):
    """rows: (case, t). Y = A(t+horizon) on held-out endpoint. horizon>=1 => future."""
    nli = {(r["domain"], r["cluster_id"]): r for r in nli_rows if r.get("mode") == mode}
    rows = []
    for rec in records:
        key = (rec["domain"], rec["cluster_id"])
        n = nli.get(key)
        if not n:
            continue
        A = [s["endpoint"]["A_j1"] for s in rec["steps"]]
        D = n["D"]
        G = n["G"].get(eps, [])
        # verifier[k].t == transition k (step k-1 -> k); row t uses the transition into step t+1
        vmap = {v.get("t"): v for v in rec.get("verifier", [])}
        for t in range(len(A)):
            if t + horizon >= len(A) or t >= len(G) or t + 1 >= len(D):
                continue
            need = [A[t], A[t + horizon], D[t], D[t + 1], G[t]]
            if any(v is None for v in need):
                continue
            vf = vmap.get(t + 1, {})
            rows.append({"case": key, "t": t, "A_t": A[t], "D_t": D[t], "D_t1": D[t + 1],
                         "G_t": G[t], "Y1": A[t + horizon],
                         "v_cov": vf.get("coverage", -1), "v_pre": vf.get("preservation", -1),
                         "v_fai": vf.get("faithfulness", -1)})
    return rows


def verifier_has_variance(rows):
    """RQ2 guard: the calibrated verifier must have real variance, else the comparison is void."""
    import numpy as np
    for f in ("v_cov", "v_pre", "v_fai"):
        vals = [r[f] for r in rows if r[f] is not None and r[f] >= 0]
        if len(set(vals)) > 1 and np.std(vals) > 0.3:
            return True
    return False


def permutation_test(rows, n_perm=1000, seed=20260719):
    rng = random.Random(seed)
    base_j = cv_scores(rows, FEATURE_SETS["joint"], "Y1")
    base_c = cv_scores(rows, FEATURE_SETS["current_only"], "Y1")
    if not base_j or not base_c or base_j["cv_r2"] is None:
        return None
    real_gain = base_j["cv_r2"] - base_c["cv_r2"]
    by_case_g = defaultdict(dict)
    for r in rows:
        by_case_g[r["case"]][r["t"]] = r["G_t"]
    cases = sorted(by_case_g)
    count, gains = 0, []
    for _ in range(n_perm):
        perm = cases[:]
        rng.shuffle(perm)
        mapping = dict(zip(cases, perm))
        g_override = np.array([by_case_g[mapping[r["case"]]].get(r["t"], r["G_t"]) for r in rows])
        pj = cv_scores(rows, FEATURE_SETS["joint"], "Y1", g_override=g_override)
        if pj and pj["cv_r2"] is not None:
            gains.append(pj["cv_r2"] - base_c["cv_r2"])
            if gains[-1] >= real_gain:
                count += 1
    return {"real_gain_vs_current": real_gain, "perm_p": (count + 1) / (len(gains) + 1),
            "n_perm_effective": len(gains)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, nargs="+")
    ap.add_argument("--nli", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", default="source_only")
    ap.add_argument("--horizon", type=int, default=1, help=">=1 predicts a FUTURE held-out endpoint")
    args = ap.parse_args()

    records = load(args.records)
    nli_rows = load(args.nli)

    out = {"mode": args.mode, "horizon": args.horizon, "eps_grid": {}}
    for eps in ("0.01", "0.05", "0.1"):
        rows = build_rows(records, nli_rows, eps=eps, mode=args.mode, horizon=args.horizon)
        out["eps_grid"][eps] = {"n_rows": len(rows),
                                "partial_spearman_G_Y1": partial_spearman(rows) if len(rows) >= 8 else None}

    rows = build_rows(records, nli_rows, eps=PRIMARY_EPS, mode=args.mode, horizon=args.horizon)
    if len(rows) >= 8:
        models = {name: cv_scores(rows, feats, "Y1") for name, feats in FEATURE_SETS.items()}
        boot = bootstrap_partial(rows)
        perm = permutation_test(rows)
        signs = [v["partial_spearman_G_Y1"] for v in out["eps_grid"].values()
                 if v.get("partial_spearman_G_Y1") is not None]
        sign_consistent = bool(signs) and (all(s > 0 for s in signs) or all(s < 0 for s in signs))
        joint_beats_current = (models["joint"] and models["current_only"]
                               and models["joint"]["cv_r2"] is not None
                               and models["joint"]["cv_r2"] > models["current_only"]["cv_r2"])
        go = bool(boot and boot.get("ci_lo", -1) > 0 and sign_consistent and joint_beats_current)
        # RQ2 (salvaged): does G add value OVER a NON-DEGENERATE calibrated verifier?
        v_var = verifier_has_variance(rows)
        joint_all_beats_verifier = (models["joint_all"] and models["verifier_only"]
                                    and models["joint_all"]["cv_r2"] is not None
                                    and models["verifier_only"]["cv_r2"] is not None
                                    and models["joint_all"]["cv_r2"] > models["verifier_only"]["cv_r2"]
                                    and models["joint_all"]["cv_r2"] > models["joint"]["cv_r2"] - 1e-9)
        rq2_go = bool(v_var and joint_all_beats_verifier and go)
        out.update({"n_rows": len(rows), "n_cases": len({r["case"] for r in rows}),
                    "models_Y1": models, "partial_spearman_boot": boot, "permutation": perm,
                    "verdict": {"rq1_go": go,
                                "rq2_go": rq2_go,
                                "verifier_has_variance": v_var,
                                "rq1_rule": "GO iff partial Spearman(G,future-A|current) CI>0 AND eps-sign "
                                            "consistent AND joint>current-only held-out.",
                                "rq2_rule": "GO iff verifier has real variance (else void) AND joint_all "
                                            "(G+current+verifier) beats verifier-only AND RQ1 holds. Small n = descriptive.",
                                "note": "verifier is a CALIBRATED reimplementation baseline, not official TrustMem; "
                                        "if verifier_has_variance is False the RQ2 comparison is void (degenerate comparator)."}})
    else:
        out["verdict"] = {"rq1_go": None, "note": f"too few rows: {len(rows)}"}

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=float)
    print(json.dumps({k: out.get(k) for k in ("mode", "horizon", "n_rows", "n_cases",
                                              "partial_spearman_boot", "permutation", "verdict")},
                     ensure_ascii=False, indent=2, default=float))


if __name__ == "__main__":
    main()
