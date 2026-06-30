from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/paper_artifact_contract_report.json"
SUMMARY_PATH = "outputs/paper_artifact_contract_report.md"
DATASET_PATH = "outputs/paper_artifact_contract_records.json"


PANELS = [
    ("actual_summarizer_slice", "outputs/actual_summarizer_slice_results.json"),
    ("actual_recall_expansion", "outputs/actual_recall_expansion_results.json"),
    ("actual_hallucination_stress", "outputs/actual_hallucination_stress_results.json"),
    ("actual_carry_forward", "outputs/actual_carry_forward_results.json"),
]


def load_json(base_dir: Path, relative_path: str) -> dict[str, Any]:
    return json.loads((base_dir / relative_path).read_text(encoding="utf-8"))


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    report: dict[str, Any] = {"panels": {}}
    normalized_records = []

    for panel_name, relative_path in PANELS:
        payload = load_json(base_dir, relative_path)
        records = payload["records"]
        pass_trace_count = 0
        provenance_count = 0
        quarantine_count = 0
        stage_attr_count = 0
        panel_records = []

        for record in records:
            artifact = record.get("artifact_contract") or {}
            coverage = artifact.get("coverage") or {}
            judge = artifact.get("judge") or {}
            if coverage.get("pass_trace_available"):
                pass_trace_count += 1
            if coverage.get("provenance_link_count", 0) > 0:
                provenance_count += 1
            if coverage.get("quarantine_count", 0) > 0:
                quarantine_count += 1
            if judge.get("first_failing_stage"):
                stage_attr_count += 1
            panel_records.append(
                {
                    "panel": panel_name,
                    "item_id": record["item_id"],
                    "architecture": record["architecture"],
                    "n_passes": record["n_passes"],
                    "seed": record["seed"],
                    "judge_label": record.get("judge_label"),
                    "first_failing_stage": record.get("first_failing_stage"),
                    "raw_escalated": record["raw_escalated"],
                    "route": record["route"],
                    "artifact_contract": artifact,
                }
            )

        normalized_records.extend(panel_records)
        report["panels"][panel_name] = {
            "record_count": len(records),
            "pass_trace_coverage": round(pass_trace_count / max(1, len(records)), 3),
            "provenance_link_coverage": round(provenance_count / max(1, len(records)), 3),
            "quarantine_signal_coverage": round(quarantine_count / max(1, len(records)), 3),
            "stage_attribution_coverage": round(stage_attr_count / max(1, len(records)), 3),
        }

    (base_dir / JSON_PATH).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / DATASET_PATH).write_text(json.dumps(normalized_records, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Paper Artifact Contract Report",
        "",
        "这份工件检查 primary model-backed panel 是否已经具备 reviewer 需要的 item-level artifact contract，而不只是最终汇总表。",
        "",
        "| Panel | Records | Pass Trace Coverage | Provenance Coverage | Quarantine Coverage | Stage Attribution Coverage |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for panel_name, row in report["panels"].items():
        lines.append(
            f"| {panel_name} | {row['record_count']} | {row['pass_trace_coverage']:.3f} | "
            f"{row['provenance_link_coverage']:.3f} | {row['quarantine_signal_coverage']:.3f} | "
            f"{row['stage_attribution_coverage']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Readout",
            "",
            "- `pass_trace_coverage` checks whether we kept per-pass compact memory history rather than only the final note.",
            "- `provenance_link_coverage` checks whether each record exposes at least one raw-span linkage in final retained memory, pass-level claim lineage, note lineage, or an explicit raw-context witness when the model collapsed to empty output.",
            "- `quarantine_signal_coverage` checks whether cleanup architectures expose explicit claim filtering or quarantine decisions.",
            "- `stage_attribution_coverage` checks whether every record can be routed to a first failing stage instead of only a final correctness flag.",
        ]
    )

    (base_dir / SUMMARY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / DATASET_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
