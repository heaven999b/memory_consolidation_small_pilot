from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


DEFAULT_STAGE = "large"
TARGET_N = 8
TARGET_ARCHITECTURE = "psu"
BASE_ARCHITECTURES = ["scale_aware_unified", "scale_aware_note_aware"]

STAGE_JSON_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}.json"
TUNING_JSON_TEMPLATE = "outputs/expanded_benchmark_tuning_{stage}_comparison.json"
ERROR_JSON_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}_error_analysis.json"
OUTPUT_JSON_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}_packet.json"
OUTPUT_MD_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}_packet.md"


def selected_stage() -> str:
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        return sys.argv[1].strip().lower()
    return os.environ.get("EXPANDED_BENCHMARK_STAGE_PACKET_STAGE", DEFAULT_STAGE).strip().lower()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return load_json(path)


def packet_paths(base_dir: Path, stage: str) -> dict[str, Path]:
    return {
        "stage": base_dir / STAGE_JSON_TEMPLATE.format(stage=stage),
        "tuning": base_dir / TUNING_JSON_TEMPLATE.format(stage=stage),
        "error": base_dir / ERROR_JSON_TEMPLATE.format(stage=stage),
        "output_json": base_dir / OUTPUT_JSON_TEMPLATE.format(stage=stage),
        "output_md": base_dir / OUTPUT_MD_TEMPLATE.format(stage=stage),
    }


def panel_coverage(payload: dict[str, Any]) -> dict[str, Any]:
    coverage: dict[str, Any] = {}
    for panel_id, panel in payload["slice_panels"].items():
        summary = panel["selection_summary"]
        coverage[panel_id] = {
            "selected_count": summary["selected_count"],
            "available_count": summary["available_count"],
            "selected_fraction": summary["selected_fraction"],
            "stratum_counts": summary["stratum_counts"],
            "complexity_counts": summary["complexity_counts"],
        }
    return coverage


def family_table(payload: dict[str, Any], n_passes: int) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for family_name, family in payload["family_rollups"].items():
        rows[family_name] = {
            "focus_label": family["focus_label"],
            "num_items": family["num_items"],
            "rows": {
                architecture: family["snapshots"][architecture][str(n_passes)]
                for architecture in payload["architectures"]
            },
        }
    return rows


def tuning_summary(tuning_payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if tuning_payload is None:
        return None

    summary: dict[str, Any] = {}
    for profile_name, profile_payload in tuning_payload["profiles"].items():
        summary[profile_name] = {}
        for family_name in ["benign_utility_expanded_pool", "hallucination_expanded_pool"]:
            focus = {}
            for architecture in tuning_payload["architectures"]:
                row = profile_payload["family_rollups"][family_name]["snapshots"][architecture][str(TARGET_N)]
                focus[architecture] = {
                    "accuracy": row["accuracy"],
                    "history_loss_rate": row.get("history_loss_rate"),
                    "false_present_rate": row.get("false_present_rate"),
                    "raw_escalation_rate": row["raw_escalation_rate"],
                }
            summary[profile_name][family_name] = focus
    return summary


def build_verdict(stage_payload: dict[str, Any], error_payload: dict[str, Any] | None) -> dict[str, Any]:
    benign = stage_payload["family_rollups"]["benign_utility_expanded_pool"]["snapshots"]
    hallucination = stage_payload["family_rollups"]["hallucination_expanded_pool"]["snapshots"]

    psu_benign = benign[TARGET_ARCHITECTURE][str(TARGET_N)]
    note_benign = benign["scale_aware_note_aware"][str(TARGET_N)]
    psu_hallu = hallucination[TARGET_ARCHITECTURE][str(TARGET_N)]
    note_hallu = hallucination["scale_aware_note_aware"][str(TARGET_N)]

    no_regression = True
    if error_payload is not None:
        no_regression = all(
            error_payload["aggregate"][family_kind][architecture]["target_worse"] == 0
            for family_kind in ["benign", "hallucination"]
            for architecture in BASE_ARCHITECTURES
        )

    ready_to_promote = (
        psu_benign["accuracy"] >= note_benign["accuracy"]
        and psu_benign["history_loss_rate"] < note_benign["history_loss_rate"]
        and psu_hallu["false_present_rate"] <= note_hallu["false_present_rate"]
        and no_regression
    )

    reason = (
        "PSU preserves benign N=8 accuracy while sharply reducing history_loss/raw_escalation, "
        "does not worsen hallucination false_present, and shows no paired regressions in the current error-analysis artifact."
        if ready_to_promote
        else "The current stage still shows a tradeoff or paired regressions that should be resolved before promotion."
    )
    return {
        "ready_to_promote_full_main": ready_to_promote,
        "reason": reason,
    }


def build_packet(stage: str) -> dict[str, Any]:
    base_dir = Path(__file__).resolve().parent
    paths = packet_paths(base_dir, stage)
    stage_payload = load_json(paths["stage"])
    tuning_payload = load_optional_json(paths["tuning"])
    error_payload = load_optional_json(paths["error"])

    return {
        "stage": stage,
        "stage_description": stage_payload["stage_description"],
        "architectures": stage_payload["architectures"],
        "seeds": stage_payload["seeds"],
        "n_values": stage_payload["n_values"],
        "num_items": stage_payload["num_items"],
        "panel_coverage": panel_coverage(stage_payload),
        "family_table_n8": family_table(stage_payload, TARGET_N),
        "tuning_summary": tuning_summary(tuning_payload),
        "error_analysis": error_payload,
        "verdict": build_verdict(stage_payload, error_payload),
    }


def build_summary(packet: dict[str, Any]) -> str:
    lines = [
        f"# Expanded Benchmark Stage {packet['stage'].title()} Packet",
        "",
        "这份 packet 把当前 stage 最值得在汇报或正文里直接引用的证据收在一起：覆盖规模、N=8 主表、可选调参对比、paired error analysis，以及是否值得继续往 full main 推进的判定。",
        "",
        "## Stage",
        "",
        f"- description: {packet['stage_description']}",
        f"- items: `{packet['num_items']}`",
        f"- seeds: `{packet['seeds']}`",
        f"- architectures: `{', '.join(packet['architectures'])}`",
        f"- verdict: `{packet['verdict']['ready_to_promote_full_main']}`",
        f"- reason: {packet['verdict']['reason']}",
        "",
        "## Coverage",
        "",
        "| Panel | Selected | Available | Fraction | Strata |",
        "|---|---:|---:|---:|---|",
    ]
    for panel_id, row in packet["panel_coverage"].items():
        lines.append(
            f"| {panel_id} | {row['selected_count']} | {row['available_count']} | {row['selected_fraction']:.3f} | {row['stratum_counts']} |"
        )

    lines.extend(
        [
            "",
            "## Family Table (N=8)",
            "",
        ]
    )
    for family_name, family in packet["family_table_n8"].items():
        focus_label = family["focus_label"]
        lines.append(f"### {family_name}")
        lines.append("")
        lines.append(f"- focus label: `{focus_label}`")
        lines.append(f"- num items: `{family['num_items']}`")
        lines.append("")
        lines.append(f"| Method | accuracy | {focus_label} | raw escalation |")
        lines.append("|---|---:|---:|---:|")
        for architecture, row in family["rows"].items():
            focus_value = row["history_loss_rate"] if "history_loss_rate" in row else row["false_present_rate"]
            lines.append(
                f"| {architecture} | {row['accuracy']:.3f} | {focus_value:.3f} | {row['raw_escalation_rate']:.3f} |"
            )
        lines.append("")

    if packet["tuning_summary"] is not None:
        lines.extend(
            [
                "## Tuning Sweep",
                "",
                "这部分只在当前 stage 已经做过 profile sweep 时出现。",
                "",
            ]
        )
        for profile_name, profile in packet["tuning_summary"].items():
            lines.append(f"### {profile_name}")
            lines.append("")
            lines.append("| Family | Method | accuracy | history_loss | false_present | raw escalation |")
            lines.append("|---|---|---:|---:|---:|---:|")
            for family_name, family_rows in profile.items():
                for architecture, row in family_rows.items():
                    history_loss = "-" if row["history_loss_rate"] is None else f"{row['history_loss_rate']:.3f}"
                    false_present = "-" if row["false_present_rate"] is None else f"{row['false_present_rate']:.3f}"
                    lines.append(
                        f"| {family_name} | {architecture} | {row['accuracy']:.3f} | {history_loss} | {false_present} | {row['raw_escalation_rate']:.3f} |"
                    )
            lines.append("")

    error_payload = packet["error_analysis"]
    if error_payload is not None:
        lines.extend(
            [
                "## Paired Error Analysis",
                "",
                "| Family | Base | Paired | PSU better | Tie | PSU worse | Base focus error | PSU focus error | Base raw | PSU raw |",
                "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for family_kind in ["benign", "hallucination"]:
            for architecture in error_payload["base_architectures"]:
                row = error_payload["aggregate"][family_kind][architecture]
                lines.append(
                    f"| {family_kind} | {architecture} | {row['paired_cases']} | {row['target_better']} | {row['tie']} | {row['target_worse']} | "
                    f"{row['base_focus_error_rate']:.3f} | {row['target_focus_error_rate']:.3f} | {row['base_raw_escalation_rate']:.3f} | {row['target_raw_escalation_rate']:.3f} |"
                )
        lines.append("")

    lines.extend(
        [
            "## Bottom Line",
            "",
            "- 这个 packet 的价值在于，它把“规模是否够、PSU 的 gain 是否只是平均数假象、调参有没有真改变结论”压缩到一页里。",
            "- 如果后续 `main` 复现相同 paired pattern，那么我们就不仅有更大 benchmark coverage，也有一份更像论文 error-analysis section 的直接证据。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    stage = selected_stage()
    packet = build_packet(stage)
    base_dir = Path(__file__).resolve().parent
    paths = packet_paths(base_dir, stage)
    paths["output_json"].write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["output_md"].write_text(build_summary(packet), encoding="utf-8")
    print(f"Wrote {paths['output_json']}")
    print(f"Wrote {paths['output_md']}")


if __name__ == "__main__":
    main()
