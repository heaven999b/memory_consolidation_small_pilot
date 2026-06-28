from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/small_pilot_results.json"
SUMMARY_PATH = "outputs/scale_aware_unified_summary.md"
JSON_PATH = "outputs/scale_aware_unified_results.json"
COMPARE_ARCHITECTURES = ["tiered", "utility_calibrated", "small_n_hybrid", "scale_aware_unified"]


def build_summary(results: dict) -> str:
    lines = [
        "# Scale-Aware Unified Summary",
        "",
        "这一轮是结构化统一实验：把 `small_n_hybrid` 的 `N<=2` 行为和 `utility_calibrated` 的 `N>=4` 行为合并成一个全 sweep policy。",
        "",
    ]
    for architecture in COMPARE_ARCHITECTURES:
        lines.append(f"## {architecture}")
        lines.append("")
        lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for n in results["n_values"]:
            row = results["aggregate"][architecture][str(n)]
            lines.append(
                f"| {n} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                f"{row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Unified Readout",
            "",
            "- `scale_aware_unified` 应该在 `N<=2` 近似 `small_n_hybrid`，在 `N>=4` 近似 `utility_calibrated`。",
            "- 关键问题不是它能否“发明新优势”，而是它能否无缝保留两边已知最强的局部解。",
            "",
            "## Matched-N Unified Comparison",
            "",
            "| N | tiered | utility_calibrated | small_n_hybrid | scale_aware_unified |",
            "|---|---|---|---|---|",
        ]
    )
    for n in results["n_values"]:
        cells = []
        for architecture in COMPARE_ARCHITECTURES:
            row = results["aggregate"][architecture][str(n)]
            cells.append(f"{row['accuracy']:.3f}/{row['propagation_rate']:.3f}/{row['raw_escalation_rate']:.3f}")
        lines.append(f"| {n} | {' | '.join(cells)} |")
    lines.extend(
        [
            "",
            "每个单元格格式：`accuracy / propagation / raw_escalation`。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    payload = {
        "n_values": results["n_values"],
        "aggregate": {
            architecture: {
                str(n): results["aggregate"][architecture][str(n)]
                for n in results["n_values"]
            }
            for architecture in COMPARE_ARCHITECTURES
        },
    }
    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
