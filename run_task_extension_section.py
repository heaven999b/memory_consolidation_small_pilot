from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import run_actual_summarizer_slice as actual_base


CONFLICT_MANIFEST = "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v1.json"
UNSAFE_MANIFEST = "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v1.json"
RECALL_RESULTS = "outputs/actual_recall_expansion_results.json"
CARRY_RESULTS = "outputs/actual_carry_forward_results.json"

JSON_PATH = "outputs/task_extension_section.json"
SUMMARY_PATH = "outputs/task_extension_section.md"
TRACE_PATH = "outputs/task_extension_section_traces.md"

UNSAFE_INTERVENTION = "tiny_carry_forward_scaffold"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def conflict_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    history_loss = [record for record in records if record["compact_answer"] == actual_base.ABSTAIN]
    supported_target = [record for record in records if record.get("supported_current_target_present")]
    return {
        "conflict_error_rate": round(sum(1 for record in records if record["conflict_answer"]) / max(1, len(records)), 3),
        "history_loss_rate": round(len(history_loss) / max(1, len(records)), 3),
        "supported_current_target_rate": round(len(supported_target) / max(1, len(records)), 3),
        "mean_llm_cost_usd": round(sum(record["llm_cost_usd"] for record in records) / max(1, len(records)), 6),
    }


def unsafe_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    carry_records = [record for record in records if record.get("carry_forward_events", 0) > 0]
    return {
        "unsafe_error_rate": round(sum(1 for record in records if record["unsafe_answer"]) / max(1, len(records)), 3),
        "carry_forward_record_rate": round(len(carry_records) / max(1, len(records)), 3),
        "mean_carry_forward_events": round(sum(record.get("carry_forward_events", 0) for record in records) / max(1, len(records)), 3),
        "mean_llm_cost_usd": round(sum(record["llm_cost_usd"] for record in records) / max(1, len(records)), 6),
    }


def build_conflict_panel(manifest: dict[str, Any], recall: dict[str, Any]) -> dict[str, Any]:
    slice_ids = [item["id"] for item in manifest["items"]]
    records = [record for record in recall["records"] if record["item_id"] in slice_ids]
    architectures = recall["architectures"]
    n_values = recall["n_values"]

    snapshots: dict[str, dict[str, dict[str, Any]]] = {}
    for architecture in architectures:
        snapshots[architecture] = {}
        for n_passes in n_values:
            rows = [
                record
                for record in records
                if record["architecture"] == architecture and record["n_passes"] == n_passes
            ]
            snapshots[architecture][str(n_passes)] = actual_base.aggregate(rows) | conflict_metrics(rows)

    return {
        "manifest_path": CONFLICT_MANIFEST,
        "manifest_version": manifest.get("version", "unknown"),
        "task_family": "conflict",
        "source_result_path": RECALL_RESULTS,
        "slice_ids": slice_ids,
        "num_items": len(slice_ids),
        "architectures": architectures,
        "n_values": n_values,
        "focus_metric": "conflict_error_rate",
        "snapshots": snapshots,
    }


def build_unsafe_panel(manifest: dict[str, Any], carry: dict[str, Any]) -> dict[str, Any]:
    slice_ids = [item["id"] for item in manifest["items"]]
    records = [
        record
        for record in carry["records"]
        if record["item_id"] in slice_ids and record["intervention"] == UNSAFE_INTERVENTION
    ]
    architectures = carry["architectures"]
    n_values = carry["n_values"]

    snapshots: dict[str, dict[str, dict[str, Any]]] = {}
    for architecture in architectures:
        snapshots[architecture] = {}
        for n_passes in n_values:
            rows = [
                record
                for record in records
                if record["architecture"] == architecture and record["n_passes"] == n_passes
            ]
            snapshots[architecture][str(n_passes)] = actual_base.aggregate(rows) | unsafe_metrics(rows)

    return {
        "manifest_path": UNSAFE_MANIFEST,
        "manifest_version": manifest.get("version", "unknown"),
        "task_family": "unsafe",
        "source_result_path": CARRY_RESULTS,
        "source_intervention": UNSAFE_INTERVENTION,
        "slice_ids": slice_ids,
        "num_items": len(slice_ids),
        "architectures": architectures,
        "n_values": n_values,
        "focus_metric": "unsafe_error_rate",
        "snapshots": snapshots,
    }


def build_payload(conflict_manifest: dict[str, Any], unsafe_manifest: dict[str, Any], recall: dict[str, Any], carry: dict[str, Any]) -> dict[str, Any]:
    conflict_panel = build_conflict_panel(conflict_manifest, recall)
    unsafe_panel = build_unsafe_panel(unsafe_manifest, carry)
    task_families = sorted({conflict_panel["task_family"], unsafe_panel["task_family"]})
    ready = all(
        [
            conflict_panel["num_items"] > 0,
            unsafe_panel["num_items"] > 0,
            bool(conflict_panel["snapshots"]),
            bool(unsafe_panel["snapshots"]),
        ]
    )
    return {
        "description": "Manifest-backed conflict and unsafe task extension section attached to the benchmark-native primary base.",
        "verdict": {
            "task_extension_section_ready": ready,
            "note": (
                "The repo now freezes manifest-backed conflict and unsafe extension panels, so the benchmark-native primary base covers all four task families rather than only benign and hallucination."
                if ready
                else "The repo has started to attach manifest-backed conflict and unsafe task extensions, but one of the extension panels is still incomplete."
            ),
        },
        "extension_summary": {
            "panel_count": 2,
            "item_count": conflict_panel["num_items"] + unsafe_panel["num_items"],
            "task_families": task_families,
            "manifest_backed": True,
        },
        "task_extension_panels": {
            "conflict_manifest_backed_extension": conflict_panel,
            "unsafe_manifest_backed_extension": unsafe_panel,
        },
        "performance_bridge": {
            "conflict_extension_n8": {
                architecture: {
                    "accuracy": conflict_panel["snapshots"][architecture]["8"]["accuracy"],
                    "conflict_error_rate": conflict_panel["snapshots"][architecture]["8"]["conflict_error_rate"],
                    "history_loss_rate": conflict_panel["snapshots"][architecture]["8"]["history_loss_rate"],
                    "raw_escalation_rate": conflict_panel["snapshots"][architecture]["8"]["raw_escalation_rate"],
                }
                for architecture in conflict_panel["architectures"]
                if "8" in conflict_panel["snapshots"][architecture]
            },
            "unsafe_extension_n8": {
                architecture: {
                    "accuracy": unsafe_panel["snapshots"][architecture]["8"]["accuracy"],
                    "unsafe_error_rate": unsafe_panel["snapshots"][architecture]["8"]["unsafe_error_rate"],
                    "carry_forward_record_rate": unsafe_panel["snapshots"][architecture]["8"]["carry_forward_record_rate"],
                    "raw_escalation_rate": unsafe_panel["snapshots"][architecture]["8"]["raw_escalation_rate"],
                }
                for architecture in unsafe_panel["architectures"]
                if "8" in unsafe_panel["snapshots"][architecture]
            },
        },
        "source_artifacts": {
            "conflict_manifest_path": CONFLICT_MANIFEST,
            "unsafe_manifest_path": UNSAFE_MANIFEST,
            "conflict_result_path": RECALL_RESULTS,
            "unsafe_result_path": CARRY_RESULTS,
            "unsafe_result_intervention": UNSAFE_INTERVENTION,
        },
    }


def build_summary(payload: dict[str, Any]) -> str:
    conflict_panel = payload["task_extension_panels"]["conflict_manifest_backed_extension"]
    unsafe_panel = payload["task_extension_panels"]["unsafe_manifest_backed_extension"]
    lines = [
        "# Task Extension Section",
        "",
        "这个 artifact 不替代外部 benchmark reviewer section。它补的是另一类缺口：把 `conflict` 和 `unsafe` 也冻结成 manifest-backed task extensions，让 benchmark-native primary base 覆盖完整四个任务 family。",
        "",
        f"- ready: `{payload['verdict']['task_extension_section_ready']}`",
        f"- panel count: `{payload['extension_summary']['panel_count']}`",
        f"- item count: `{payload['extension_summary']['item_count']}`",
        f"- task families: `{payload['extension_summary']['task_families']}`",
        "",
        "## Conflict Extension (N=8)",
        "",
        "| Method | accuracy | conflict_error | history_loss | raw escalation |",
        "|---|---:|---:|---:|---:|",
    ]
    for architecture in conflict_panel["architectures"]:
        row = conflict_panel["snapshots"][architecture]["8"]
        lines.append(
            f"| {architecture} | {row['accuracy']:.3f} | {row['conflict_error_rate']:.3f} | {row['history_loss_rate']:.3f} | {row['raw_escalation_rate']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Unsafe Extension (N=8)",
            "",
            "| Method | accuracy | unsafe_error | carry_forward_record | raw escalation |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for architecture in unsafe_panel["architectures"]:
        row = unsafe_panel["snapshots"][architecture]["8"]
        lines.append(
            f"| {architecture} | {row['accuracy']:.3f} | {row['unsafe_error_rate']:.3f} | {row['carry_forward_record_rate']:.3f} | {row['raw_escalation_rate']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Readout",
            "",
            "- `conflict` 现在不再只是散落在 recall slice 里的 supporting evidence，而是有了 manifest-backed extension panel。",
            "- `unsafe` 现在也不再只是单轮 scaffold 调参结果，而是有了 manifest-backed extension panel，并明确绑定到 carry-forward refusal winner。",
            "- 这一步补掉的不是 benchmark scale，而是任务 family 覆盖缺口。",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(payload: dict[str, Any]) -> str:
    conflict_panel = payload["task_extension_panels"]["conflict_manifest_backed_extension"]
    unsafe_panel = payload["task_extension_panels"]["unsafe_manifest_backed_extension"]
    lines = [
        "# Task Extension Section Traces",
        "",
        f"- conflict slice ids: `{conflict_panel['slice_ids']}`",
        f"- unsafe slice ids: `{unsafe_panel['slice_ids']}`",
        "",
    ]
    for architecture in conflict_panel["architectures"]:
        row = conflict_panel["snapshots"][architecture]["8"]
        lines.append(
            f"- conflict N=8 {architecture}: acc={row['accuracy']:.3f}, conflict_error={row['conflict_error_rate']:.3f}, history_loss={row['history_loss_rate']:.3f}, raw={row['raw_escalation_rate']:.3f}"
        )
    lines.append("")
    for architecture in unsafe_panel["architectures"]:
        row = unsafe_panel["snapshots"][architecture]["8"]
        lines.append(
            f"- unsafe N=8 {architecture}: acc={row['accuracy']:.3f}, unsafe_error={row['unsafe_error_rate']:.3f}, carry_forward_record={row['carry_forward_record_rate']:.3f}, raw={row['raw_escalation_rate']:.3f}"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    conflict_manifest = load_json(base_dir / CONFLICT_MANIFEST)
    unsafe_manifest = load_json(base_dir / UNSAFE_MANIFEST)
    recall = load_json(base_dir / RECALL_RESULTS)
    carry = load_json(base_dir / CARRY_RESULTS)

    payload = build_payload(conflict_manifest, unsafe_manifest, recall, carry)
    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    (base_dir / TRACE_PATH).write_text(build_traces(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")
    print(f"Wrote {base_dir / TRACE_PATH}")


if __name__ == "__main__":
    main()
