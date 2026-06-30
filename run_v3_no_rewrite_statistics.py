from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_no_rewrite_statistics.json"
SUMMARY_PATH = "outputs/v3_no_rewrite_statistics.md"
BOOTSTRAP_SAMPLES = 4000
BOOTSTRAP_SEED = 20260630
COMPARISONS = [
    ("summary_only", "summary_query_aware", "Fairness: blind -> query-aware"),
    ("summary_query_aware", "summary_only_no_rewrite", "Mechanism: query-aware -> no-rewrite"),
    ("summary_only", "summary_only_no_rewrite", "Main: blind -> no-rewrite"),
]
FAMILY_METRICS = {
    "hallucination": ("unsupported_answer", "Unsupported answer"),
    "conflict": ("conflict_answer", "Wrong current answer"),
    "unsafe": ("unsafe_answer", "Unsafe answer"),
    "benign": ("correct", "Accuracy"),
}


def load_payload(repo_root: Path) -> dict[str, Any]:
    return json.loads((repo_root / "outputs" / "v3_no_rewrite_comparison.json").read_text(encoding="utf-8"))


def available_n_values(payload: dict[str, Any]) -> list[int]:
    explicit = payload.get("n_values")
    if isinstance(explicit, list) and explicit:
        return [int(value) for value in explicit]
    return sorted({int(record["n_passes"]) for record in payload.get("records", [])})


def pair_records(
    records: list[dict[str, Any]],
    architecture_a: str,
    architecture_b: str,
    family: str,
    n_passes: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    left = {
        (record["item_id"], record["seed"]): record
        for record in records
        if record["architecture"] == architecture_a and record["family"] == family and record["n_passes"] == n_passes
    }
    right = {
        (record["item_id"], record["seed"]): record
        for record in records
        if record["architecture"] == architecture_b and record["family"] == family and record["n_passes"] == n_passes
    }
    shared = sorted(set(left) & set(right))
    return [(left[key], right[key]) for key in shared]


def mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def bootstrap_ci(deltas: list[float], seed: int) -> dict[str, float]:
    if not deltas:
        return {"delta": 0.0, "ci_low": 0.0, "ci_high": 0.0}
    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(BOOTSTRAP_SAMPLES):
        sample = [deltas[rng.randrange(len(deltas))] for _ in range(len(deltas))]
        estimates.append(mean(sample))
    estimates.sort()
    return {
        "delta": round(mean(deltas), 4),
        "ci_low": round(estimates[int(0.025 * len(estimates))], 4),
        "ci_high": round(estimates[min(int(0.975 * len(estimates)), len(estimates) - 1)], 4),
    }


def binomial_cdf(k: int, n: int, p: float) -> float:
    total = 0.0
    for i in range(k + 1):
        total += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return total


def exact_mcnemar_p(b01: int, b10: int) -> float:
    discordant = b01 + b10
    if discordant == 0:
        return 1.0
    tail = min(b01, b10)
    return round(min(1.0, 2.0 * binomial_cdf(tail, discordant, 0.5)), 6)


def evaluate_binary_pairs(
    pairs: list[tuple[dict[str, Any], dict[str, Any]]],
    metric_key: str,
    *,
    positive_is_good: bool,
    seed: int,
) -> dict[str, Any]:
    left_values: list[float] = []
    right_values: list[float] = []
    deltas: list[float] = []
    left_win = 0
    right_win = 0
    ties = 0
    for left, right in pairs:
        left_value = 1.0 if bool(left[metric_key]) else 0.0
        right_value = 1.0 if bool(right[metric_key]) else 0.0
        left_values.append(left_value)
        right_values.append(right_value)
        deltas.append(right_value - left_value)
        if right_value > left_value:
            right_win += 1
        elif left_value > right_value:
            left_win += 1
        else:
            ties += 1
    ci = bootstrap_ci(deltas, seed)
    return {
        "pair_count": len(pairs),
        "left_mean": round(mean(left_values), 4),
        "right_mean": round(mean(right_values), 4),
        "delta": ci["delta"],
        "ci_low": ci["ci_low"],
        "ci_high": ci["ci_high"],
        "left_win": left_win,
        "right_win": right_win,
        "ties": ties,
        "mcnemar_p": exact_mcnemar_p(left_win, right_win),
        "positive_is_good": positive_is_good,
    }


def build_payload(repo_root: Path) -> dict[str, Any]:
    payload = load_payload(repo_root)
    records = payload["records"]
    n_values = available_n_values(payload)
    rows: list[dict[str, Any]] = []
    seed_offset = 0
    for left_arch, right_arch, label in COMPARISONS:
        for family, (metric_key, metric_label) in FAMILY_METRICS.items():
            for n_passes in n_values:
                pairs = pair_records(records, left_arch, right_arch, family, n_passes)
                positive_is_good = family == "benign"
                stats = evaluate_binary_pairs(
                    pairs,
                    metric_key,
                    positive_is_good=positive_is_good,
                    seed=BOOTSTRAP_SEED + seed_offset,
                )
                rows.append(
                    {
                        "comparison": label,
                        "left_architecture": left_arch,
                        "right_architecture": right_arch,
                        "family": family,
                        "metric_key": metric_key,
                        "metric_label": metric_label,
                        "n_passes": n_passes,
                        **stats,
                    }
                )
                seed_offset += 1
    return {
        "description": "Paired synthetic dry-run statistics for the V3 no-rewrite comparison surface.",
        "evidence_class": payload.get("evidence_class", "synthetic_dry_run"),
        "surface_runtime": payload.get("surface_runtime", "legacy_compaction_simulator"),
        "bootstrap_samples": BOOTSTRAP_SAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "n_values": n_values,
        "rows": rows,
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 No-Rewrite Statistics",
        "",
        payload["description"],
        "",
        f"- evidence class: `{payload.get('evidence_class', 'unknown')}`",
        f"- runtime: `{payload.get('surface_runtime', 'unknown')}`",
        f"- bootstrap samples: `{payload['bootstrap_samples']}`",
        f"- bootstrap seed: `{payload['bootstrap_seed']}`",
        f"- depths: `{payload.get('n_values', [])}`",
        "",
        "Warning: this table is a synthetic dry-run over the legacy compaction simulator.",
        "Zero-width confidence intervals or exact `0.000` / `+/-1.000` deltas here should not be interpreted as real-model stochastic evidence.",
        "",
        "| Comparison | Family | N | Left | Right | Delta | 95% CI | Left-win | Right-win | Ties | McNemar p |",
        "|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| {row['comparison']} | {row['family']} | {row['n_passes']} | {row['left_mean']:.3f} | {row['right_mean']:.3f} | "
            f"{row['delta']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | {row['left_win']} | {row['right_win']} | "
            f"{row['ties']} | {row['mcnemar_p']:.6f} |"
        )
    lines.append("")
    lines.append("Interpretation note: `benign` uses accuracy, while the other families use failure endpoints, so negative deltas on risk families are improvements.")
    lines.append("Paper-safety note: do not mix this synthetic table with real TierMem or official public-baseline result tables.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-no-rewrite-stats] wrote {repo_root / JSON_PATH}")
    print(f"[v3-no-rewrite-stats] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
