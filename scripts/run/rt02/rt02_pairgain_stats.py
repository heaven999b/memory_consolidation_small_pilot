#!/usr/bin/env python3
"""RT-02 PairGain MVP stats — RQ1 (conditional predictive power of G) + RQ2 (beyond TrustMem-style).

Run in .venv_tiermem_v2 (numpy/scipy/sklearn). Pre-registered analysis (design doc §2.4):
  rows: (case, t) transitions, t in {0,1,2}; outcome Y = A(t+1) (paired unsafe effect, judge1)
  models: current-only [A(t), D(t), D(t+1)] / trustmem-style [cov,pres,faith] / G-only / joint
  grouped 5-fold CV by case; metrics: held-out R^2, Spearman(pred, Y)
  key tests:
    RQ1: partial Spearman(G, Y | current) with case-bootstrap CI; sign stability over eps grid
    RQ2: joint minus trustmem-only CV gain; whole-curve permutation of G across cases (n=1000)
"""
import argparse
import json
import random
from collections import defaultdict

import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GroupKFold

PRIMARY_EPS = "0.05"


def load_jsonl(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def ckey(r):
    return (
        r.get("task", "qa"),
        r.get("domain"),
        str(r.get("case_key") or r.get("cluster_id")),
    )


def build_rows(records, nli_rows, eps=PRIMARY_EPS, gate="u_j1"):
    nli = {ckey(r): r for r in nli_rows}
    rows = []
    for rec in records:
        n = nli.get(ckey(rec))
        if not n:
            continue
        steps = rec["steps"]
        A = []
        for s in steps:
            um, up = s["minus_probe"].get(gate), s["plus_probe"].get(gate)
            A.append(None if um is None or up is None else um - up)
        D, G = n["D"], n["G"].get(eps, [])
        tm = {t["t"]: t for t in rec.get("trustmem_style", [])}
        for t in range(0, 3):
            if t + 1 >= len(A):
                continue
            need = [A[t], A[t + 1], D[t] if t < len(D) else None,
                    D[t + 1] if t + 1 < len(D) else None, G[t] if t < len(G) else None]
            if any(v is None for v in need):
                continue
            ts = tm.get(t + 1, {})
            cov, pre, fai = ts.get("coverage", -1), ts.get("preservation", -1), ts.get("faithfulness", -1)
            rows.append({
                "case": ckey(rec), "t": t, "task": rec.get("task", "qa"),
                "A_t": A[t], "D_t": D[t], "D_t1": D[t + 1], "G_t": G[t],
                "tm_cov": cov, "tm_pre": pre, "tm_fai": fai,
                "Y1": A[t + 1], "Y2": A[t + 2] if t + 2 < len(A) and A[t + 2] is not None else None,
            })
    return rows


FEATURE_SETS = {
    "current_only": ["A_t", "D_t", "D_t1"],
    "trustmem_only": ["tm_cov", "tm_pre", "tm_fai"],
    "g_only": ["G_t"],
    "joint": ["A_t", "D_t", "D_t1", "tm_cov", "tm_pre", "tm_fai", "G_t"],
}


def cv_scores(rows, features, y_key="Y1", n_splits=5, g_override=None):
    X = np.array([[r[f] for f in features] for r in rows], dtype=float)
    if g_override is not None and "G_t" in features:
        X[:, features.index("G_t")] = g_override
    y = np.array([r[y_key] for r in rows], dtype=float)
    # Python's built-in hash is process-randomized.  Stable integer group IDs
    # keep the registered grouped CV exactly reproducible across reruns.
    case_to_group = {case: idx for idx, case in enumerate(sorted({r["case"] for r in rows}))}
    groups = np.array([case_to_group[r["case"]] for r in rows])
    n_splits = min(n_splits, len(set(groups.tolist())))
    if n_splits < 2:
        return None
    preds = np.zeros_like(y)
    for tr, te in GroupKFold(n_splits=n_splits).split(X, y, groups):
        preds[te] = LinearRegression().fit(X[tr], y[tr]).predict(X[te])
    ss_res = float(np.sum((y - preds) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    rho = spearmanr(preds, y).statistic if len(set(preds.tolist())) > 1 else 0.0
    return {"cv_r2": 1 - ss_res / ss_tot if ss_tot > 0 else None,
            "spearman": None if rho is None or np.isnan(rho) else float(rho)}


def partial_spearman(rows, y_key="Y1"):
    controls = ["A_t", "D_t", "D_t1"]
    X = np.array([[r[f] for f in controls] for r in rows], dtype=float)
    g = np.array([r["G_t"] for r in rows], dtype=float)
    y = np.array([r[y_key] for r in rows], dtype=float)
    rg = g - LinearRegression().fit(X, g).predict(X)
    ry = y - LinearRegression().fit(X, y).predict(X)
    rho = spearmanr(rg, ry).statistic
    return None if rho is None or np.isnan(rho) else float(rho)


def bootstrap_partial(rows, y_key="Y1", n_boot=2000, seed=20260718):
    rng = random.Random(seed)
    by_case = defaultdict(list)
    for r in rows:
        by_case[r["case"]].append(r)
    cases = sorted(by_case)
    vals = []
    for _ in range(n_boot):
        sample = []
        for _ in cases:
            sample.extend(by_case[cases[rng.randrange(len(cases))]])
        if len(sample) >= 8:
            v = partial_spearman(sample, y_key)
            if v is not None:
                vals.append(v)
    if not vals:
        return None
    vals.sort()
    return {"rho": partial_spearman(rows, y_key), "ci_lo": vals[int(0.025 * len(vals))],
            "ci_hi": vals[int(0.975 * len(vals))], "n_boot": len(vals)}


def permutation_test(rows, records, nli_rows, n_perm=1000, seed=20260718, y_key="Y1"):
    """Whole-curve permutation: swap complete G curves across cases within task strata."""
    rng = random.Random(seed)
    base_joint = cv_scores(rows, FEATURE_SETS["joint"], y_key)
    base_cur = cv_scores(rows, FEATURE_SETS["current_only"], y_key)
    if not base_joint or not base_cur or base_joint["cv_r2"] is None:
        return None
    real_gain = base_joint["cv_r2"] - base_cur["cv_r2"]
    by_case_g = defaultdict(dict)
    for r in rows:
        by_case_g[r["case"]][r["t"]] = r["G_t"]
    tasks = defaultdict(list)
    for c in by_case_g:
        tasks[c[0]].append(c)
    for task in tasks:
        tasks[task].sort()
    count = 0
    gains = []
    for _ in range(n_perm):
        mapping = {}
        for task, cs in tasks.items():
            perm = cs[:]
            rng.shuffle(perm)
            mapping.update(dict(zip(cs, perm)))
        g_override = np.array([by_case_g[mapping[r["case"]]].get(r["t"], r["G_t"]) for r in rows])
        pj = cv_scores(rows, FEATURE_SETS["joint"], y_key, g_override=g_override)
        if pj and pj["cv_r2"] is not None:
            gain = pj["cv_r2"] - base_cur["cv_r2"]
            gains.append(gain)
            if gain >= real_gain:
                count += 1
    return {"real_gain_vs_current": real_gain, "perm_p": (count + 1) / (len(gains) + 1),
            "n_perm_effective": len(gains)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True, nargs="+")
    ap.add_argument("--nli", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    records = []
    for p in args.records:
        records.extend(load_jsonl(p))
    nli_rows = []
    for p in args.nli:
        nli_rows.extend(load_jsonl(p))

    out = {"eps_grid": {}, "primary": {}}
    for eps in ("0.01", "0.05", "0.1"):
        rows = build_rows(records, nli_rows, eps=eps)
        if len(rows) < 8:
            out["eps_grid"][eps] = {"error": f"too few rows: {len(rows)}"}
            continue
        ps = partial_spearman(rows)
        out["eps_grid"][eps] = {"n_rows": len(rows), "partial_spearman_G_Y1": ps}

    rows = build_rows(records, nli_rows, eps=PRIMARY_EPS)
    if len(rows) >= 8:
        pri = {"n_rows": len(rows), "n_cases": len({r['case'] for r in rows})}
        pri["models_Y1"] = {name: cv_scores(rows, feats, "Y1")
                            for name, feats in FEATURE_SETS.items()}
        rows2 = [r for r in rows if r.get("Y2") is not None]
        if len(rows2) >= 8:
            pri["models_Y2"] = {name: cv_scores(rows2, feats, "Y2")
                                for name, feats in FEATURE_SETS.items()}
        pri["partial_spearman_boot"] = bootstrap_partial(rows)
        pri["permutation"] = permutation_test(rows, records, nli_rows)
        out["primary"] = pri

        b = pri.get("partial_spearman_boot") or {}
        signs = [v.get("partial_spearman_G_Y1") for v in out["eps_grid"].values()
                 if isinstance(v, dict) and v.get("partial_spearman_G_Y1") is not None]
        sign_consistent = len(signs) > 0 and (all(s > 0 for s in signs) or all(s < 0 for s in signs))
        m = pri["models_Y1"]
        joint_beats_tm = (m["joint"] and m["trustmem_only"] and
                          m["joint"]["cv_r2"] is not None and m["trustmem_only"]["cv_r2"] is not None and
                          m["joint"]["cv_r2"] > m["trustmem_only"]["cv_r2"])
        perm = pri.get("permutation") or {}
        rq1_go = bool(b and b.get("ci_lo", -1) > 0 and sign_consistent)
        rq2_go = bool(joint_beats_tm and perm.get("perm_p", 1) < 0.05)
        out["verdict"] = {
            "rq1_go": rq1_go, "rq2_go": rq2_go,
            "overall": "GO" if (rq1_go and rq2_go) else ("PARTIAL" if rq1_go else "STOP"),
            "rule": "RQ1 Go iff partial Spearman(G,Y1|current) case-bootstrap CI>0 and eps-grid sign-consistent; "
                    "RQ2 Go iff joint beats trustmem-only held-out and permuted-G gain dies (p<0.05). "
                    "STOP -> PairGain headline dead (G is a current-state proxy).",
        }
    else:
        out["verdict"] = {"overall": "INSUFFICIENT_DATA", "n_rows": len(rows)}

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=float)
    print(json.dumps(out.get("verdict"), ensure_ascii=False, indent=2))
    if out.get("primary"):
        print(json.dumps({k: out["primary"][k] for k in ("models_Y1", "partial_spearman_boot", "permutation")
                          if k in out["primary"]}, ensure_ascii=False, indent=2, default=float))


if __name__ == "__main__":
    main()
