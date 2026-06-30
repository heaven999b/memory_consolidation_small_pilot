from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_no_rewrite_pareto.json"
SUMMARY_PATH = "outputs/v3_no_rewrite_pareto.md"
N_VALUES = [8, 16]


def load_payload(repo_root: Path) -> dict[str, Any]:
    return json.loads((repo_root / "outputs" / "v3_no_rewrite_comparison.json").read_text(encoding="utf-8"))


def mean_cost(records: list[dict[str, Any]]) -> float:
    return round(sum(float(record["estimated_cost"]) for record in records) / max(1, len(records)), 3)


def subset(payload: dict[str, Any], architecture: str, n_passes: int) -> list[dict[str, Any]]:
    return [
        record
        for record in payload["records"]
        if record["architecture"] == architecture and record["n_passes"] == n_passes
    ]


def pareto_front(rows: list[dict[str, Any]], quality_key: str, cost_key: str = "mean_cost") -> list[str]:
    front: list[str] = []
    for row in rows:
        dominated = False
        for other in rows:
            if other["architecture"] == row["architecture"]:
                continue
            better_or_equal = other[quality_key] >= row[quality_key] and other[cost_key] <= row[cost_key]
            strictly_better = other[quality_key] > row[quality_key] or other[cost_key] < row[cost_key]
            if better_or_equal and strictly_better:
                dominated = True
                break
        if not dominated:
            front.append(row["architecture"])
    return sorted(front)


def build_payload(repo_root: Path) -> dict[str, Any]:
    comparison = load_payload(repo_root)
    sections: list[dict[str, Any]] = []
    for n_passes in N_VALUES:
        benign_rows: list[dict[str, Any]] = []
        safety_rows: list[dict[str, Any]] = []
        for architecture in comparison["architectures"]:
            subset_records = subset(comparison, architecture, n_passes)
            snapshot = comparison["snapshots"][architecture][str(n_passes)]
            benign = snapshot["by_family"]["benign"]
            hallucination = snapshot["by_family"]["hallucination"]
            conflict = snapshot["by_family"]["conflict"]
            unsafe = snapshot["by_family"]["unsafe"]
            safety_quality = round(
                1.0
                - (
                    hallucination["unsupported_answer_rate"]
                    + conflict["conflict_answer_rate"]
                    + unsafe["unsafe_answer_rate"]
                )
                / 3.0,
                3,
            )
            mean_cost_value = mean_cost(subset_records)
            benign_rows.append(
                {
                    "architecture": architecture,
                    "quality": benign["accuracy"],
                    "mean_cost": mean_cost_value,
                    "history_loss": benign["benign_overcompression_rate"],
                }
            )
            safety_rows.append(
                {
                    "architecture": architecture,
                    "quality": safety_quality,
                    "mean_cost": mean_cost_value,
                    "hallucination_risk": hallucination["unsupported_answer_rate"],
                    "conflict_risk": conflict["conflict_answer_rate"],
                    "unsafe_risk": unsafe["unsafe_answer_rate"],
                }
            )
        sections.append(
            {
                "n_passes": n_passes,
                "benign_rows": benign_rows,
                "benign_front": pareto_front(benign_rows, "quality"),
                "safety_rows": safety_rows,
                "safety_front": pareto_front(safety_rows, "quality"),
            }
        )
    return {
        "description": "Proxy cost/utility and cost/safety Pareto readout for the V3 no-rewrite comparison surface.",
        "sections": sections,
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 No-Rewrite Pareto",
        "",
        payload["description"],
        "",
    ]
    for section in payload["sections"]:
        lines.append(f"## N={section['n_passes']}")
        lines.append("")
        lines.append(f"- benign Pareto front: `{section['benign_front']}`")
        lines.append(f"- safety Pareto front: `{section['safety_front']}`")
        lines.append("")
        lines.append("### Benign Accuracy vs Cost")
        lines.append("")
        lines.append("| Method | Accuracy | mean_cost | history_loss |")
        lines.append("|---|---:|---:|---:|")
        for row in section["benign_rows"]:
            lines.append(
                f"| {row['architecture']} | {row['quality']:.3f} | {row['mean_cost']:.3f} | {row['history_loss']:.3f} |"
            )
        lines.append("")
        lines.append("### Safety Score vs Cost")
        lines.append("")
        lines.append("| Method | Safety Score | mean_cost | hallucination_risk | conflict_risk | unsafe_risk |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for row in section["safety_rows"]:
            lines.append(
                f"| {row['architecture']} | {row['quality']:.3f} | {row['mean_cost']:.3f} | "
                f"{row['hallucination_risk']:.3f} | {row['conflict_risk']:.3f} | {row['unsafe_risk']:.3f} |"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-no-rewrite-pareto] wrote {repo_root / JSON_PATH}")
    print(f"[v3-no-rewrite-pareto] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()

