from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/psu_paper_packet.json"
SUMMARY_PATH = "outputs/psu_paper_packet.md"


def load_json(base_dir: Path, relative_path: str) -> dict[str, Any]:
    return json.loads((base_dir / relative_path).read_text(encoding="utf-8"))


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    method_report = load_json(base_dir, "outputs/provenance_scaffolded_method_report.json")
    recall_panel = load_json(base_dir, "outputs/psu_recall_main_panel.json")
    stats = load_json(base_dir, "outputs/paper_strengthening_stats.json")
    artifact = load_json(base_dir, "outputs/paper_artifact_contract_report.json")
    benchmark = load_json(base_dir, "outputs/external_benchmark_reviewer_section.json")

    comparisons = {row["label"]: row for row in stats["comparisons"]}
    payload = {
        "method_spec": method_report["method_spec"],
        "psu_recall_panel_n8": recall_panel["panel_rows"]["8"],
        "key_deltas": {
            "note_aware_to_psu_accuracy": comparisons["Recall N=8 accuracy: scale_aware_note_aware -> PSU"],
            "note_aware_to_psu_history_loss": comparisons["Recall N=8 history loss: scale_aware_note_aware -> PSU"],
            "note_aware_to_psu_raw_escalation": comparisons["Recall N=8 raw escalation: scale_aware_note_aware -> PSU"],
        },
        "artifact_contract": artifact["panels"],
        "benchmark_section": {
            "seeds": benchmark["seeds"],
            "family_rollups": {
                family: {
                    "num_items": row["num_items"],
                    "panel_ids": row["panel_ids"],
                }
                for family, row in benchmark["family_rollups"].items()
            },
        },
    }

    lines = [
        "# PSU Paper Packet",
        "",
        "这份 packet 把当前最接近论文正文会直接引用的 PSU 证据收在一起：方法定义、主 recall 表、关键 paired-delta、artifact contract 覆盖、以及更大 benchmark section 的当前规模。",
        "",
        "## Method",
        "",
        f"- name: `{payload['method_spec']['name']}`",
        f"- short name: `{payload['method_spec']['short_name']}`",
        f"- routing architecture: `{payload['method_spec']['routing_architecture']}`",
        f"- compaction contract: `{payload['method_spec']['compaction_contract']}`",
        "",
        "## Recall Main Panel (N=8)",
        "",
        "| Method | accuracy | propagation | raw escalation | history loss | benign/conflict error | unsafe error | carry-forward record |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["psu_recall_panel_n8"]:
        lines.append(
            f"| {row['label']} | {row['accuracy']:.3f} | {row['propagation']:.3f} | {row['raw_escalation']:.3f} | "
            f"{row['history_loss']:.3f} | {row['benign_conflict_error']:.3f} | {row['unsafe_error']:.3f} | {row['carry_forward_record']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Key Paired Deltas",
            "",
            "| Comparison | Pairs | Baseline | Treatment | Improvement Delta | 95% CI |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for label, row in payload["key_deltas"].items():
        pretty = {
            "note_aware_to_psu_accuracy": "scale_aware_note_aware -> PSU accuracy",
            "note_aware_to_psu_history_loss": "scale_aware_note_aware -> PSU history_loss",
            "note_aware_to_psu_raw_escalation": "scale_aware_note_aware -> PSU raw_escalation",
        }[label]
        lines.append(
            f"| {pretty} | {row['pair_count']} | {row['baseline_mean']:.3f} | {row['treatment_mean']:.3f} | "
            f"{row['improvement_delta']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] |"
        )

    lines.extend(
        [
            "",
            "## Artifact Contract Coverage",
            "",
            "| Panel | Records | Pass Trace | Provenance | Quarantine | Stage Attribution |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for panel_name, row in payload["artifact_contract"].items():
        lines.append(
            f"| {panel_name} | {row['record_count']} | {row['pass_trace_coverage']:.3f} | {row['provenance_link_coverage']:.3f} | "
            f"{row['quarantine_signal_coverage']:.3f} | {row['stage_attribution_coverage']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Benchmark Section Scale",
            "",
            f"- seeds: `{payload['benchmark_section']['seeds']}`",
        ]
    )
    for family, row in payload["benchmark_section"]["family_rollups"].items():
        lines.append(f"- {family}: `{row['num_items']}` items from `{row['panel_ids']}`")

    lines.extend(
        [
            "",
            "## Bottom Line",
            "",
            "- PSU is now supported by a stable multi-seed recall main panel rather than only a single-seed pilot.",
            "- The strongest gain is not just final accuracy; it is the collapse of high-N `history_loss` and `raw_escalation`, which is exactly the mechanism the method claims to improve.",
            "- The current benchmark-first reviewer section is broader than the initial minimal baseline, but it is still a 32-item frozen section rather than a full paper-scale benchmark sweep.",
        ]
    )

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
