from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any, Callable


JSON_PATH = "outputs/paper_strengthening_stats.json"
SUMMARY_PATH = "outputs/paper_strengthening_stats.md"
BOOTSTRAP_SAMPLES = 2000
BOOTSTRAP_SEED = 20260628


def load_json(base_dir: Path, relative_path: str) -> dict[str, Any]:
    return json.loads((base_dir / relative_path).read_text(encoding="utf-8"))


def select_records(records: list[dict[str, Any]], **filters: Any) -> list[dict[str, Any]]:
    selected = []
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
    rng = random.Random(seed)
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


def paired_binary_improvement(
    baseline: list[dict[str, Any]],
    treatment: list[dict[str, Any]],
    metric_fn: Callable[[dict[str, Any]], float],
    *,
    harmful_metric: bool,
    label: str,
    seed: int,
) -> dict[str, Any]:
    pairs = pair_records(baseline, treatment)
    deltas = []
    baseline_values = []
    treatment_values = []
    wins = 0
    losses = 0
    ties = 0
    for base_record, treat_record in pairs:
        base_value = float(metric_fn(base_record))
        treat_value = float(metric_fn(treat_record))
        baseline_values.append(base_value)
        treatment_values.append(treat_value)
        raw_delta = base_value - treat_value if harmful_metric else treat_value - base_value
        deltas.append(raw_delta)
        if raw_delta > 0:
            wins += 1
        elif raw_delta < 0:
            losses += 1
        else:
            ties += 1
    ci = bootstrap_ci(deltas, seed=seed)
    return {
        "label": label,
        "pair_count": len(pairs),
        "baseline_mean": round(mean(baseline_values), 4),
        "treatment_mean": round(mean(treatment_values), 4),
        "improvement_delta": ci["mean"],
        "ci_low": ci["ci_low"],
        "ci_high": ci["ci_high"],
        "wins": wins,
        "losses": losses,
        "ties": ties,
    }


def slope_from_points(points: list[tuple[float, float]]) -> float:
    if len(points) < 2:
        return 0.0
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in points)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if math.isclose(denominator, 0.0):
        return 0.0
    return round(numerator / denominator, 4)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    recall = load_json(base_dir, "outputs/actual_recall_expansion_results.json")
    stress = load_json(base_dir, "outputs/actual_hallucination_stress_results.json")
    persistence = load_json(base_dir, "outputs/actual_note_persistence_results.json")
    refinement = load_json(base_dir, "outputs/actual_scaffold_refinement_results.json")
    hardening = load_json(base_dir, "outputs/actual_placeholder_hardening_results.json")
    carry = load_json(base_dir, "outputs/actual_carry_forward_results.json")

    comparisons = []
    comparisons.append(
        paired_binary_improvement(
            select_records(recall["records"], architecture="summary_only", n_passes=8),
            select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8),
            lambda record: 1.0 if record["correct"] else 0.0,
            harmful_metric=False,
            label="Recall N=8 accuracy: summary_only -> scale_aware_note_aware",
            seed=BOOTSTRAP_SEED + 1,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(recall["records"], architecture="summary_only", n_passes=8, family="benign")
            + select_records(recall["records"], architecture="summary_only", n_passes=8, family="conflict"),
            select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8, family="benign")
            + select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8, family="conflict"),
            lambda record: 1.0 if record["compact_answer"] == "ABSTAIN" else 0.0,
            harmful_metric=True,
            label="Recall N=8 history loss: summary_only -> scale_aware_note_aware",
            seed=BOOTSTRAP_SEED + 2,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(stress["records"], architecture="scale_aware_unified", n_passes=1),
            select_records(stress["records"], architecture="scale_aware_note_aware", n_passes=1),
            lambda record: 1.0 if record["raw_escalated"] else 0.0,
            harmful_metric=True,
            label="Stress N=1 false-present: scale_aware_unified -> scale_aware_note_aware",
            seed=BOOTSTRAP_SEED + 3,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(stress["records"], architecture="scale_aware_unified", n_passes=8),
            select_records(stress["records"], architecture="scale_aware_note_aware", n_passes=8),
            lambda record: 1.0 if record["raw_escalated"] else 0.0,
            harmful_metric=True,
            label="Stress N=8 false-present: scale_aware_unified -> scale_aware_note_aware",
            seed=BOOTSTRAP_SEED + 4,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(persistence["records"], architecture="scale_aware_note_aware", intervention="baseline", n_passes=8, family="benign")
            + select_records(persistence["records"], architecture="scale_aware_note_aware", intervention="baseline", n_passes=8, family="conflict"),
            select_records(persistence["records"], architecture="scale_aware_note_aware", intervention="tiny_fixed_scaffold", n_passes=8, family="benign")
            + select_records(persistence["records"], architecture="scale_aware_note_aware", intervention="tiny_fixed_scaffold", n_passes=8, family="conflict"),
            lambda record: 1.0 if record["compact_answer"] == "ABSTAIN" else 0.0,
            harmful_metric=True,
            label="Note persistence N=8 history loss: baseline -> tiny_fixed_scaffold",
            seed=BOOTSTRAP_SEED + 5,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(refinement["records"], architecture="scale_aware_note_aware", intervention="tiny_fixed_scaffold", n_passes=8),
            select_records(refinement["records"], architecture="scale_aware_note_aware", intervention="tiny_refusal_scaffold", n_passes=8),
            lambda record: 1.0 if record["unsafe_answer"] else 0.0,
            harmful_metric=True,
            label="Scaffold refinement N=8 unsafe error: tiny_fixed_scaffold -> tiny_refusal_scaffold",
            seed=BOOTSTRAP_SEED + 6,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(hardening["records"], architecture="scale_aware_note_aware", intervention="tiny_refusal_scaffold", n_passes=8),
            select_records(hardening["records"], architecture="scale_aware_note_aware", intervention="tiny_placeholder_hardened_scaffold", n_passes=8),
            lambda record: 1.0 if record.get("placeholder_answer") else 0.0,
            harmful_metric=True,
            label="Placeholder hardening N=8 placeholder answer: tiny_refusal_scaffold -> tiny_placeholder_hardened_scaffold",
            seed=BOOTSTRAP_SEED + 7,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(carry["records"], architecture="scale_aware_note_aware", intervention="tiny_placeholder_hardened_scaffold", n_passes=8),
            select_records(carry["records"], architecture="scale_aware_note_aware", intervention="tiny_carry_forward_scaffold", n_passes=8),
            lambda record: 1.0 if record["unsafe_answer"] else 0.0,
            harmful_metric=True,
            label="Carry-forward N=8 unsafe error: tiny_placeholder_hardened_scaffold -> tiny_carry_forward_scaffold",
            seed=BOOTSTRAP_SEED + 8,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8),
            select_records(carry["records"], architecture="scale_aware_note_aware", intervention="tiny_carry_forward_scaffold", n_passes=8),
            lambda record: 1.0 if record["correct"] else 0.0,
            harmful_metric=False,
            label="Recall N=8 accuracy: scale_aware_note_aware -> PSU",
            seed=BOOTSTRAP_SEED + 9,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8, family="benign")
            + select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8, family="conflict"),
            select_records(carry["records"], architecture="scale_aware_note_aware", intervention="tiny_carry_forward_scaffold", n_passes=8, family="benign")
            + select_records(carry["records"], architecture="scale_aware_note_aware", intervention="tiny_carry_forward_scaffold", n_passes=8, family="conflict"),
            lambda record: 1.0 if record["compact_answer"] == "ABSTAIN" else 0.0,
            harmful_metric=True,
            label="Recall N=8 history loss: scale_aware_note_aware -> PSU",
            seed=BOOTSTRAP_SEED + 10,
        )
    )
    comparisons.append(
        paired_binary_improvement(
            select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8),
            select_records(carry["records"], architecture="scale_aware_note_aware", intervention="tiny_carry_forward_scaffold", n_passes=8),
            lambda record: 1.0 if record["raw_escalated"] else 0.0,
            harmful_metric=True,
            label="Recall N=8 raw escalation: scale_aware_note_aware -> PSU",
            seed=BOOTSTRAP_SEED + 11,
        )
    )

    slopes = {
        "summary_only_recall_history_loss_slope": slope_from_points(
            [
                (n, recall["recall_metrics"]["summary_only"][str(n)]["history_loss_rate"])
                for n in recall["n_values"]
            ]
        ),
        "scale_aware_note_aware_recall_history_loss_slope": slope_from_points(
            [
                (n, recall["recall_metrics"]["scale_aware_note_aware"][str(n)]["history_loss_rate"])
                for n in recall["n_values"]
            ]
        ),
        "psu_recall_history_loss_slope": slope_from_points(
            [
                (n, carry["carry_metrics"]["scale_aware_note_aware"]["tiny_carry_forward_scaffold"][str(n)]["history_loss_rate"])
                for n in carry["n_values"]
            ]
        ),
        "tiered_stress_false_present_slope": slope_from_points(
            [
                (n, stress["hallucination_metrics"]["tiered"][str(n)]["false_present_rate"])
                for n in stress["n_values"]
            ]
        ),
        "scale_aware_note_aware_stress_false_present_slope": slope_from_points(
            [
                (n, stress["hallucination_metrics"]["scale_aware_note_aware"][str(n)]["false_present_rate"])
                for n in stress["n_values"]
            ]
        ),
    }

    payload = {
        "bootstrap_samples": BOOTSTRAP_SAMPLES,
        "comparisons": comparisons,
        "slopes": slopes,
    }

    lines = [
        "# Paper Strengthening Stats",
        "",
        "这份工件补的是论文级统计层，不再只报单个 frozen table，而是对关键比较给出 paired bootstrap delta 和简单 slope 分析。",
        "",
        f"- bootstrap samples: {BOOTSTRAP_SAMPLES}",
        "",
        "## Paired Bootstrap",
        "",
        "| Comparison | Pairs | Baseline | Treatment | Improvement Delta | 95% CI | Wins | Losses | Ties |",
        "|---|---:|---:|---:|---:|---|---:|---:|---:|",
    ]
    for row in comparisons:
        lines.append(
            f"| {row['label']} | {row['pair_count']} | {row['baseline_mean']:.3f} | {row['treatment_mean']:.3f} | "
            f"{row['improvement_delta']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
            f"{row['wins']} | {row['losses']} | {row['ties']} |"
        )
    lines.extend(
        [
            "",
            "## Slope Readout",
            "",
            "| Metric | Slope |",
            "|---|---:|",
        ]
    )
    for key, value in slopes.items():
        lines.append(f"| {key} | {value:.4f} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Positive improvement delta means the treatment is better under the metric's intended direction.",
            "- Positive slope means the metric rises with `N`; for harmful metrics like `history_loss` or `false_present`, that is undesirable.",
        ]
    )

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
