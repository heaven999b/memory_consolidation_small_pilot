#!/usr/bin/env python3
"""E1 multi-seed statistics: between-seed CIs and seed-level paired tests.

Consumes the per-seed judge reports produced by ``run_e1_multiseed_sweep.py``
(one failure-mode judge report per seed) and reports, for each
(route_mode, consolidation depth N):

* the cross-seed mean of each failure-mode rate with a t-based 95% CI over
  seeds -- this is the interval the single-seed pilots could not give, because
  it captures the "which QA subset" variability that the seeded resampling
  injects; and
* seed-level paired tests of "N vs N=0": for each seed a delta is computed, and
  a one-sample t-test plus a sign test ask whether the depth effect is
  consistent across seeds. With >=5 seeds these can actually reach significance,
  unlike the item-level McNemar on a single 15-45 QA slice.

This module reuses the metric definitions in ``run_e1_hallucination_statistics``
so the point estimates are identical to the single-run layer.

Usage
-----
    python3 run_e1_multiseed_statistics.py --manifest outputs/v2_tiermem_micro/multiseed/<prefix>_manifest.json
    python3 run_e1_multiseed_statistics.py --judge-report a.json --judge-report b.json ... --self-test
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Optional

from scipy.stats import t as student_t, ttest_1samp, binomtest

from run_e1_hallucination_statistics import METRICS, load_family


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "v2_tiermem_micro" / "stats"
# The rates whose depth-trend is the E1 story.
FOCUS_METRICS = [
    "correct_rate",
    "unsupported_fabrication_on_unknown",
    "abstain_forgetting_on_factual",
    "fact_distortion_on_factual",
]


def _point_rate(items, metric_key: str) -> Optional[float]:
    num, den = METRICS[metric_key](items)
    return (num / den) if den else None


def _t_ci(values: list[float], alpha: float = 0.05) -> dict[str, Any]:
    n = len(values)
    m = mean(values) if n else float("nan")
    if n < 2:
        return {"mean": m, "sd": 0.0, "ci_low": float("nan"), "ci_high": float("nan"), "n": n}
    sd = pstdev(values) * math.sqrt(n / (n - 1))  # sample SD
    se = sd / math.sqrt(n)
    tcrit = float(student_t.ppf(1 - alpha / 2, df=n - 1))
    return {"mean": m, "sd": sd, "ci_low": m - tcrit * se, "ci_high": m + tcrit * se, "n": n}


def _collect_seed_rates(judge_reports: list[tuple[int, Path]]) -> dict[tuple, dict[str, dict[int, float]]]:
    """Return {(route, passes): {metric: {seed: rate}}}."""
    table: dict[tuple, dict[str, dict[int, float]]] = defaultdict(lambda: defaultdict(dict))
    for seed, path in judge_reports:
        _, conditions = load_family(path)
        for cond in conditions:
            key = (cond.route_mode, cond.passes)
            for metric_key in FOCUS_METRICS:
                r = _point_rate(cond.items, metric_key)
                if r is not None:
                    table[key][metric_key][seed] = r
    return table


def analyze(judge_reports: list[tuple[int, Path]]) -> dict[str, Any]:
    table = _collect_seed_rates(judge_reports)
    routes = sorted({k[0] for k in table}, key=lambda x: str(x))
    seeds = sorted({s for _, _ in judge_reports for s in [_]}) or [s for s, _ in judge_reports]
    seeds = sorted({s for s, _ in judge_reports})

    per_condition = []
    for (route, passes) in sorted(table, key=lambda k: (str(k[0]), k[1])):
        row: dict[str, Any] = {"route_mode": route, "consolidation_passes": passes, "metrics": {}}
        for metric_key in FOCUS_METRICS:
            per_seed = table[(route, passes)].get(metric_key, {})
            vals = [per_seed[s] for s in sorted(per_seed)]
            ci = _t_ci(vals)
            ci["per_seed"] = per_seed
            row["metrics"][metric_key] = ci
        per_condition.append(row)

    # Seed-level paired tests: for each route, each N>0, each metric, form the
    # per-seed delta (rate(N) - rate(0)) and test mean delta == 0.
    paired = []
    for route in routes:
        passes_here = sorted({p for (r, p) in table if r == route})
        if 0 not in passes_here:
            continue
        for passes in passes_here:
            if passes == 0:
                continue
            for metric_key in FOCUS_METRICS:
                base = table[(route, 0)].get(metric_key, {})
                other = table[(route, passes)].get(metric_key, {})
                shared = sorted(set(base) & set(other))
                deltas = [other[s] - base[s] for s in shared]
                if len(deltas) < 2:
                    continue
                mean_delta = mean(deltas)
                # one-sample t-test vs 0
                tt = ttest_1samp(deltas, 0.0)
                # sign test: how many deltas are negative (metric decreased)
                neg = sum(1 for d in deltas if d < 0)
                pos = sum(1 for d in deltas if d > 0)
                nonzero = neg + pos
                sign_p = float(binomtest(min(neg, pos), nonzero, 0.5).pvalue) if nonzero else 1.0
                paired.append({
                    "route_mode": route, "other_passes": passes, "metric": metric_key,
                    "n_seeds": len(deltas), "mean_delta": mean_delta,
                    "t_p_value": float(tt.pvalue), "neg_deltas": neg, "pos_deltas": pos,
                    "sign_p_value": sign_p, "deltas": deltas,
                })
    return {"seeds": seeds, "per_condition": per_condition, "paired_tests": paired}


def render_markdown(analysis: dict[str, Any]) -> str:
    seeds = analysis["seeds"]
    lines = [
        "# E1 multi-seed statistics: between-seed CI + seed-level paired tests",
        "",
        f"- generated_at: `{datetime.now().isoformat(timespec='seconds')}`",
        f"- seeds ({len(seeds)}): `{seeds}`",
        "- Each seed is a reproducible random QA subsample (reader is temperature=0.0), "
        "so the CI below captures evaluation-set variability -- the gap the single-seed "
        "pilots left open. Point rates equal the single-run layer's estimates.",
        "",
        "## Cross-seed mean rate [95% CI over seeds]",
        "",
        "| route | N | correct_rate | UF_on_unknown | AF_on_factual | FD_on_factual |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]

    def cell(m: dict[str, Any]) -> str:
        if m["n"] < 2 or math.isnan(m.get("ci_low", float("nan"))):
            return f"{m['mean']:.3f} (n={m['n']})" if not math.isnan(m["mean"]) else "n/a"
        return f"{m['mean']:.3f} [{m['ci_low']:.3f}, {m['ci_high']:.3f}]"

    for row in analysis["per_condition"]:
        m = row["metrics"]
        lines.append("| {route} | {n} | {cr} | {uf} | {af} | {fd} |".format(
            route=row["route_mode"], n=row["consolidation_passes"],
            cr=cell(m["correct_rate"]), uf=cell(m["unsupported_fabrication_on_unknown"]),
            af=cell(m["abstain_forgetting_on_factual"]), fd=cell(m["fact_distortion_on_factual"])))
    lines += ["", "## Seed-level paired tests (N vs N=0)", "",
              "| route | N | metric | seeds | mean_delta | t p | neg/pos | sign p | sig@0.05 |",
              "| --- | ---: | --- | ---: | ---: | ---: | :---: | ---: | :---: |"]
    for t in analysis["paired_tests"]:
        sig = "yes" if (t["t_p_value"] < 0.05 or t["sign_p_value"] < 0.05) else "no"
        lines.append("| {route} | {n} | {metric} | {ns} | {md:+.3f} | {tp:.4f} | {neg}/{pos} | {sp:.4f} | {sig} |".format(
            route=t["route_mode"], n=t["other_passes"], metric=t["metric"], ns=t["n_seeds"],
            md=t["mean_delta"], tp=t["t_p_value"], neg=t["neg_deltas"], pos=t["pos_deltas"],
            sp=t["sign_p_value"], sig=sig))
    lines += ["", "> `mean_delta` < 0 means the rate dropped as N increased. With >=5 seeds "
              "these tests can resolve a consistent depth effect that the single-slice "
              "item-level McNemar cannot.", ""]
    return "\n".join(lines) + "\n"


def _load_manifest(manifest_path: Path) -> list[tuple[int, Path]]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    out = []
    for entry in payload.get("seed_entries", []):
        out.append((int(entry["seed"]), Path(entry["judge_report"])))
    return out


def _self_test() -> None:
    """Validate the aggregation math on synthetic per-seed rates (no I/O)."""
    class FakeItem:
        def __init__(self, label, cls):
            self.judge_label, self.gold_answerability = label, cls
    # 3 fake seeds; UF_on_unknown drops from ~0.5 (N=0) to ~0.17 (N=1) consistently.
    vals_n0 = [0.50, 0.60, 0.40]
    vals_n1 = [0.17, 0.20, 0.10]
    ci0, ci1 = _t_ci(vals_n0), _t_ci(vals_n1)
    deltas = [b - a for a, b in zip(vals_n0, vals_n1)]
    tt = ttest_1samp(deltas, 0.0)
    assert abs(ci0["mean"] - 0.5) < 1e-9 and ci0["ci_low"] < ci0["mean"] < ci0["ci_high"]
    assert all(d < 0 for d in deltas) and tt.pvalue < 0.05, (deltas, tt.pvalue)
    print("[self-test] OK  "
          f"N0 mean={ci0['mean']:.3f} CI=[{ci0['ci_low']:.3f},{ci0['ci_high']:.3f}]  "
          f"N1 mean={ci1['mean']:.3f} CI=[{ci1['ci_low']:.3f},{ci1['ci_high']:.3f}]  "
          f"mean_delta={mean(deltas):+.3f} t_p={float(tt.pvalue):.4f}")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="E1 multi-seed cross-seed CI + paired tests.")
    p.add_argument("--manifest", type=str, default=None, help="Manifest from run_e1_multiseed_sweep.py.")
    p.add_argument("--judge-report", action="append", default=None,
                   help="Explicit per-seed judge report path (repeatable). Pair with --seed-labels.")
    p.add_argument("--seed-labels", nargs="+", type=int, default=None,
                   help="Seed label per --judge-report, in order.")
    p.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument("--report-id", type=str, default=None)
    p.add_argument("--self-test", action="store_true", help="Run the aggregation self-test and exit.")
    return p


def main() -> int:
    args = _build_parser().parse_args()
    if args.self_test:
        _self_test()
        return 0

    if args.manifest:
        judge_reports = _load_manifest(Path(args.manifest).expanduser())
    elif args.judge_report:
        labels = args.seed_labels or list(range(len(args.judge_report)))
        judge_reports = [(int(labels[i]), Path(p).expanduser()) for i, p in enumerate(args.judge_report)]
    else:
        raise SystemExit("provide --manifest or --judge-report ...")

    missing = [str(p) for _, p in judge_reports if not p.exists()]
    if missing:
        raise FileNotFoundError(f"judge reports not found: {missing}")

    analysis = analyze(judge_reports)
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    report_id = args.report_id or f"e1_multiseed_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    (output_dir / f"{report_id}.json").write_text(
        json.dumps({"report_id": report_id, "generated_at": datetime.now().isoformat(timespec="seconds"),
                    "sources": [str(p) for _, p in judge_reports], **analysis},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / f"{report_id}.md").write_text(render_markdown(analysis), encoding="utf-8")
    print(json.dumps({"report_id": report_id,
                      "report_md": str(output_dir / f"{report_id}.md"),
                      "n_seeds": len(judge_reports)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
