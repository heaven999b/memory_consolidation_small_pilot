from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable


JSON_PATH = "outputs/expanded_benchmark_stage_main_significance.json"
SUMMARY_PATH = "outputs/expanded_benchmark_stage_main_significance.md"
BOOTSTRAP_SAMPLES = 5000
BOOTSTRAP_SEED = 20260630


def load_main_payload(base_dir: Path) -> dict[str, Any]:
    return json.loads((base_dir / "outputs/expanded_benchmark_stage_main.json").read_text(encoding="utf-8"))


def select_records(records: list[dict[str, Any]], **filters: Any) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for record in records:
        keep = True
        for key, expected in filters.items():
            if record.get(key) != expected:
                keep = False
                break
        if keep:
            selected.append(record)
    return selected


def pair_records(
    baseline: list[dict[str, Any]],
    treatment: list[dict[str, Any]],
    key_fields: tuple[str, ...] = ("item_id", "seed"),
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    baseline_map = {tuple(record[field] for field in key_fields): record for record in baseline}
    treatment_map = {tuple(record[field] for field in key_fields): record for record in treatment}
    shared = sorted(set(baseline_map) & set(treatment_map))
    return [(baseline_map[key], treatment_map[key]) for key in shared]


def mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def bootstrap_ci(deltas: list[float], *, seed: int) -> dict[str, float]:
    if not deltas:
        return {"mean": 0.0, "ci_low": 0.0, "ci_high": 0.0}
    rng = __import__("random").Random(seed)
    estimates = []
    for _ in range(BOOTSTRAP_SAMPLES):
        sample = [deltas[rng.randrange(len(deltas))] for _ in range(len(deltas))]
        estimates.append(mean(sample))
    estimates.sort()
    low_idx = int(0.025 * len(estimates))
    high_idx = int(0.975 * len(estimates))
    return {
        "mean": round(mean(deltas), 4),
        "ci_low": round(estimates[low_idx], 4),
        "ci_high": round(estimates[min(high_idx, len(estimates) - 1)], 4),
    }


def binomial_cdf(k: int, n: int, p: float) -> float:
    total = 0.0
    for i in range(0, k + 1):
        total += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return total


def exact_mcnemar_pvalue(b01: int, b10: int) -> float:
    discordant = b01 + b10
    if discordant == 0:
        return 1.0
    tail = min(b01, b10)
    p_value = min(1.0, 2.0 * binomial_cdf(tail, discordant, 0.5))
    return round(p_value, 6)


def paired_test(
    baseline: list[dict[str, Any]],
    treatment: list[dict[str, Any]],
    favorable_fn: Callable[[dict[str, Any]], float],
    *,
    label: str,
    seed: int,
) -> dict[str, Any]:
    pairs = pair_records(baseline, treatment)
    deltas: list[float] = []
    baseline_values: list[float] = []
    treatment_values: list[float] = []
    treatment_win = 0
    baseline_win = 0
    ties = 0
    for base_record, treat_record in pairs:
        base_value = float(favorable_fn(base_record))
        treat_value = float(favorable_fn(treat_record))
        baseline_values.append(base_value)
        treatment_values.append(treat_value)
        deltas.append(treat_value - base_value)
        if treat_value > base_value:
            treatment_win += 1
        elif base_value > treat_value:
            baseline_win += 1
        else:
            ties += 1
    ci = bootstrap_ci(deltas, seed=seed)
    return {
        "label": label,
        "pair_count": len(pairs),
        "baseline_mean": round(mean(baseline_values), 4),
        "treatment_mean": round(mean(treatment_values), 4),
        "delta": ci["mean"],
        "ci_low": ci["ci_low"],
        "ci_high": ci["ci_high"],
        "treatment_win": treatment_win,
        "baseline_win": baseline_win,
        "ties": ties,
        "mcnemar_p": exact_mcnemar_pvalue(baseline_win, treatment_win),
    }


def pick_strongest_baseline(
    family: dict[str, Any],
    *,
    metric_key: str,
    maximize: bool,
) -> str:
    candidates = []
    for architecture, rows in family["snapshots"].items():
        if architecture == "psu":
            continue
        candidates.append((architecture, float(rows["8"][metric_key])))
    if maximize:
        return max(candidates, key=lambda row: row[1])[0]
    return min(candidates, key=lambda row: row[1])[0]


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# Expanded Benchmark Main Significance",
        "",
        "This artifact upgrades the finished expanded benchmark `main` run from a score table into paired significance tests at paper-facing scale.",
        "",
        f"- bootstrap samples: `{BOOTSTRAP_SAMPLES}`",
        f"- bootstrap seed: `{BOOTSTRAP_SEED}`",
        "",
        "## Main Tests",
        "",
        "| Comparison | Pairs | Baseline | PSU | Delta | 95% CI | Baseline-win | PSU-win | Ties | McNemar p |",
        "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for row in payload["comparisons"]:
        lines.append(
            f"| {row['label']} | {row['pair_count']} | {row['baseline_mean']:.3f} | {row['treatment_mean']:.3f} | "
            f"{row['delta']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
            f"{row['baseline_win']} | {row['treatment_win']} | {row['ties']} | {row['mcnemar_p']:.6f} |"
        )
    lines.extend(
        [
            "",
            "## Baseline Selection",
            "",
            f"- benign accuracy strongest baseline: `{payload['baseline_selection']['benign_accuracy']}`",
            f"- benign history-loss strongest baseline: `{payload['baseline_selection']['benign_history_loss']}`",
            f"- benign raw-escalation strongest baseline: `{payload['baseline_selection']['benign_raw_escalation']}`",
            f"- hallucination false-present strongest baseline: `{payload['baseline_selection']['hallucination_false_present']}`",
            f"- hallucination accuracy strongest baseline: `{payload['baseline_selection']['hallucination_accuracy']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    payload = load_main_payload(base_dir)
    benign_family = payload["family_rollups"]["benign_utility_expanded_pool"]
    hallucination_family = payload["family_rollups"]["hallucination_expanded_pool"]

    baseline_selection = {
        "benign_accuracy": pick_strongest_baseline(benign_family, metric_key="accuracy", maximize=True),
        "benign_history_loss": pick_strongest_baseline(benign_family, metric_key="history_loss_rate", maximize=False),
        "benign_raw_escalation": pick_strongest_baseline(benign_family, metric_key="raw_escalation_rate", maximize=False),
        "hallucination_false_present": pick_strongest_baseline(hallucination_family, metric_key="false_present_rate", maximize=False),
        "hallucination_accuracy": pick_strongest_baseline(hallucination_family, metric_key="accuracy", maximize=True),
    }

    benign_records = benign_family["records"]
    hallucination_records = hallucination_family["records"]
    comparisons = [
        paired_test(
            select_records(benign_records, architecture=baseline_selection["benign_accuracy"], n_passes=8),
            select_records(benign_records, architecture="psu", n_passes=8),
            lambda record: 1.0 if record["correct"] else 0.0,
            label=f"Benign N=8 accuracy: {baseline_selection['benign_accuracy']} -> PSU",
            seed=BOOTSTRAP_SEED + 1,
        ),
        paired_test(
            select_records(benign_records, architecture=baseline_selection["benign_history_loss"], n_passes=8),
            select_records(benign_records, architecture="psu", n_passes=8),
            lambda record: 1.0 if record["compact_answer"] != "ABSTAIN" else 0.0,
            label=f"Benign N=8 history retention: {baseline_selection['benign_history_loss']} -> PSU",
            seed=BOOTSTRAP_SEED + 2,
        ),
        paired_test(
            select_records(benign_records, architecture=baseline_selection["benign_raw_escalation"], n_passes=8),
            select_records(benign_records, architecture="psu", n_passes=8),
            lambda record: 1.0 if not record["raw_escalated"] else 0.0,
            label=f"Benign N=8 no-raw-escalation: {baseline_selection['benign_raw_escalation']} -> PSU",
            seed=BOOTSTRAP_SEED + 3,
        ),
        paired_test(
            select_records(hallucination_records, architecture=baseline_selection["hallucination_false_present"], n_passes=8),
            select_records(hallucination_records, architecture="psu", n_passes=8),
            lambda record: 1.0 if not record["raw_escalated"] else 0.0,
            label=f"Hallucination N=8 no-false-present: {baseline_selection['hallucination_false_present']} -> PSU",
            seed=BOOTSTRAP_SEED + 4,
        ),
        paired_test(
            select_records(hallucination_records, architecture=baseline_selection["hallucination_accuracy"], n_passes=8),
            select_records(hallucination_records, architecture="psu", n_passes=8),
            lambda record: 1.0 if record["correct"] else 0.0,
            label=f"Hallucination N=8 accuracy: {baseline_selection['hallucination_accuracy']} -> PSU",
            seed=BOOTSTRAP_SEED + 5,
        ),
    ]

    result = {
        "description": "Paired significance tests for the finished expanded benchmark main run.",
        "bootstrap_samples": BOOTSTRAP_SAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "baseline_selection": baseline_selection,
        "comparisons": comparisons,
    }
    (base_dir / JSON_PATH).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(result), encoding="utf-8")


if __name__ == "__main__":
    main()
