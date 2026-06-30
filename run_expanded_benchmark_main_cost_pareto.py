from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/expanded_benchmark_stage_main_cost_pareto.json"
SUMMARY_PATH = "outputs/expanded_benchmark_stage_main_cost_pareto.md"


def load_main_payload(base_dir: Path) -> dict[str, Any]:
    return json.loads((base_dir / "outputs/expanded_benchmark_stage_main.json").read_text(encoding="utf-8"))


def pareto_front(rows: list[dict[str, Any]], *, quality_key: str, cost_key: str) -> list[str]:
    front: list[str] = []
    for row in rows:
        dominated = False
        for other in rows:
            if other["architecture"] == row["architecture"]:
                continue
            other_better_or_equal = other[quality_key] >= row[quality_key] and other[cost_key] <= row[cost_key]
            strictly_better = other[quality_key] > row[quality_key] or other[cost_key] < row[cost_key]
            if other_better_or_equal and strictly_better:
                dominated = True
                break
        if not dominated:
            front.append(row["architecture"])
    return sorted(front)


def iso_budget_leaders(rows: list[dict[str, Any]], *, quality_key: str, cost_key: str) -> list[dict[str, Any]]:
    budgets = sorted({row[cost_key] for row in rows})
    leaders: list[dict[str, Any]] = []
    for budget in budgets:
        feasible = [row for row in rows if row[cost_key] <= budget]
        best = max(feasible, key=lambda row: (row[quality_key], -row[cost_key]))
        leaders.append(
            {
                "budget": budget,
                "leader": best["architecture"],
                "quality": best[quality_key],
                "cost": best[cost_key],
            }
        )
    return leaders


def build_family_rows(family: dict[str, Any], *, quality_key: str, safety_label: str) -> list[dict[str, Any]]:
    rows = []
    for architecture, snapshot_by_n in family["snapshots"].items():
        row = snapshot_by_n["8"]
        rows.append(
            {
                "architecture": architecture,
                "quality": round(float(row[quality_key]), 4),
                "mean_cost": round(float(row["mean_cost"]), 4),
                "mean_llm_cost_usd": round(float(row["mean_llm_cost_usd"]), 6),
                "raw_escalation_rate": round(float(row["raw_escalation_rate"]), 4),
                "label": safety_label,
            }
        )
    return rows


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# Expanded Benchmark Main Cost Pareto",
        "",
        "This artifact promotes cost into a first-class axis for the finished expanded benchmark `main` run.",
        "",
    ]
    for section in payload["sections"]:
        lines.append(f"## {section['title']}")
        lines.append("")
        lines.append(f"- quality axis: `{section['quality_label']}`")
        lines.append(f"- pareto front (mean_cost): `{section['pareto_front_mean_cost']}`")
        lines.append(f"- pareto front (mean_llm_cost_usd): `{section['pareto_front_mean_llm_cost_usd']}`")
        lines.append("")
        lines.append("| Method | Quality | mean_cost | mean_llm_cost_usd | raw_escalation |")
        lines.append("|---|---:|---:|---:|---:|")
        for row in section["rows"]:
            lines.append(
                f"| {row['architecture']} | {row['quality']:.3f} | {row['mean_cost']:.3f} | {row['mean_llm_cost_usd']:.4f} | {row['raw_escalation_rate']:.3f} |"
            )
        lines.append("")
        lines.append("### Iso-Budget Leaders (mean_cost)")
        lines.append("")
        lines.append("| Budget | Leader | Quality | Cost |")
        lines.append("|---|---|---:|---:|")
        for leader in section["iso_budget_leaders"]:
            lines.append(
                f"| {leader['budget']:.3f} | {leader['leader']} | {leader['quality']:.3f} | {leader['cost']:.3f} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    payload = load_main_payload(base_dir)
    benign_family = payload["family_rollups"]["benign_utility_expanded_pool"]
    hallucination_family = payload["family_rollups"]["hallucination_expanded_pool"]

    benign_rows = build_family_rows(benign_family, quality_key="accuracy", safety_label="accuracy")
    hallucination_rows = []
    for architecture, snapshot_by_n in hallucination_family["snapshots"].items():
        row = snapshot_by_n["8"]
        hallucination_rows.append(
            {
                "architecture": architecture,
                "quality": round(1.0 - float(row["false_present_rate"]), 4),
                "mean_cost": round(float(row["mean_cost"]), 4),
                "mean_llm_cost_usd": round(float(row["mean_llm_cost_usd"]), 6),
                "raw_escalation_rate": round(float(row["raw_escalation_rate"]), 4),
                "label": "1 - false_present_rate",
            }
        )

    sections = [
        {
            "title": "Benign Utility (N=8 accuracy vs cost)",
            "quality_label": "accuracy",
            "rows": benign_rows,
            "pareto_front_mean_cost": pareto_front(benign_rows, quality_key="quality", cost_key="mean_cost"),
            "pareto_front_mean_llm_cost_usd": pareto_front(benign_rows, quality_key="quality", cost_key="mean_llm_cost_usd"),
            "iso_budget_leaders": iso_budget_leaders(benign_rows, quality_key="quality", cost_key="mean_cost"),
        },
        {
            "title": "Hallucination Safety (N=8 1-false_present vs cost)",
            "quality_label": "1 - false_present_rate",
            "rows": hallucination_rows,
            "pareto_front_mean_cost": pareto_front(hallucination_rows, quality_key="quality", cost_key="mean_cost"),
            "pareto_front_mean_llm_cost_usd": pareto_front(hallucination_rows, quality_key="quality", cost_key="mean_llm_cost_usd"),
            "iso_budget_leaders": iso_budget_leaders(hallucination_rows, quality_key="quality", cost_key="mean_cost"),
        },
    ]

    result = {
        "description": "Cost-oriented Pareto readout for the finished expanded benchmark main run.",
        "sections": sections,
    }
    (base_dir / JSON_PATH).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(result), encoding="utf-8")


if __name__ == "__main__":
    main()
