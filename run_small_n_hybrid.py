from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from pilot_core import aggregate, evaluate_item, load_items


ARCHITECTURES = ["tiered", "utility_calibrated", "small_n_hybrid"]
N_VALUES = [1, 2]
SEEDS = [11, 23, 47, 89, 131]


def calibration_metrics(records: list[dict]) -> dict[str, float]:
    total = len(records)
    false_absent = [
        r for r in records
        if r["gold"] not in {"ABSTAIN", "REFUSE_AND_ESCALATE"} and r["compact_answer"] == "ABSTAIN" and not r["raw_escalated"]
    ]
    false_present = [
        r for r in records
        if r["gold"] == "ABSTAIN" and r["raw_escalated"]
    ]
    guardband = [r for r in records if r["route"] == "small_n_guardband_fallback"]
    return {
        "false_absent_rate": round(len(false_absent) / total, 3),
        "false_present_rate": round(len(false_present) / total, 3),
        "guardband_rate": round(len(guardband) / total, 3),
    }


def build_summary(results: dict) -> str:
    lines = [
        "# Small-N Hybrid Summary",
        "",
        "这一轮是一个 focused experiment：只看 `N in {1, 2}`，测试是否能在小 N 区间借用 tiered-style shield 修补 cleanup policy 的窄带 miss。",
        "",
    ]
    for architecture in ARCHITECTURES:
        lines.append(f"## {architecture}")
        lines.append("")
        lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | guardband |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n in N_VALUES:
            row = results["aggregate"][architecture][str(n)]
            calib = results["calibration"][architecture][str(n)]
            lines.append(
                f"| {n} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                f"{row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} | {calib['false_absent_rate']:.3f} | "
                f"{calib['false_present_rate']:.3f} | {calib['guardband_rate']:.3f} |"
            )
        lines.append("")
        lines.append("| family @ N=2 | accuracy | propagation | raw_escalation |")
        lines.append("|---|---:|---:|---:|")
        for family, metrics in results["aggregate"][architecture]["2"]["by_family"].items():
            lines.append(
                f"| {family} | {metrics['accuracy']:.3f} | {metrics['propagation_rate']:.3f} | {metrics['raw_escalation_rate']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Headline Comparison",
            "",
            "- `small_n_hybrid` should be judged only on `N=1/2`; it is not intended as a new high-`N` global policy.",
            "- The key question is whether it can match `tiered`'s perfect small-`N` shielding while keeping cleanup-style zero residual contamination and much lower raw escalation.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    items = load_items(base_dir)
    all_records = []
    aggregate_table: dict[str, dict[str, dict]] = {}
    calibration_table: dict[str, dict[str, dict]] = {}
    route_counts: dict[str, dict[str, dict[str, int]]] = {}

    for architecture in ARCHITECTURES:
        aggregate_table[architecture] = {}
        calibration_table[architecture] = {}
        route_counts[architecture] = {}
        for n_passes in N_VALUES:
            records = []
            for seed in SEEDS:
                for item in items:
                    record = evaluate_item(item, architecture, n_passes, seed)
                    record["seed"] = seed
                    records.append(record)
                    all_records.append(record)
            aggregate_table[architecture][str(n_passes)] = aggregate(records)
            calibration_table[architecture][str(n_passes)] = calibration_metrics(records)
            route_counts[architecture][str(n_passes)] = dict(Counter(r["route"] for r in records))

    payload = {
        "description": "Focused N=1/2 experiment for a narrow guardband small-N hybrid policy.",
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": SEEDS,
        "num_items": len(items),
        "aggregate": aggregate_table,
        "calibration": calibration_table,
        "route_counts": route_counts,
        "records": all_records,
    }

    json_path = output_dir / "small_n_hybrid_results.json"
    summary_path = output_dir / "small_n_hybrid_summary.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_path.write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
