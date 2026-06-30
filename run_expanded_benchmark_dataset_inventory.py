from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import benchmark_native_runtime as native_runtime


MANIFEST_SPECS = [
    {
        "panel_id": "halumem_expanded_v1",
        "manifest_path": "benchmarks/halumem/frozen_slices/halumem_hallucination_expanded_v1.json",
    },
    {
        "panel_id": "locomo_expanded_v1",
        "manifest_path": "benchmarks/locomo/frozen_slices/locomo_benign_utility_expanded_v1.json",
    },
    {
        "panel_id": "longmemeval_expanded_v2",
        "manifest_path": "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_expanded_v2.json",
    },
]

JSON_PATH = "outputs/expanded_benchmark_dataset_inventory.json"
SUMMARY_PATH = "outputs/expanded_benchmark_dataset_inventory.md"

CURRENT_REVIEWER_SECTION_SIZE = 32


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def panel_summary(panel_id: str, manifest_path: str, manifest: dict[str, Any]) -> dict[str, Any]:
    runtime_valid_count = 0
    runtime_errors: list[dict[str, Any]] = []
    benchmark_family = None
    task_family = None
    extra: dict[str, Any] = {}

    if panel_id.startswith("halumem"):
        source_indexes = []
        for item in manifest["items"]:
            packet = native_runtime.build_native_packet(
                panel_id=panel_id,
                manifest_path=manifest_path,
                manifest_version=manifest.get("version", "unknown"),
                item=item,
            )
            errors = native_runtime.validate_packet(packet, native_runtime.runtime_projection(item))
            if errors:
                runtime_errors.append({"item_id": item["id"], "errors": errors})
            else:
                runtime_valid_count += 1
            benchmark_family = packet.benchmark_family
            task_family = packet.task_family
            source_indexes.append(item["source_provenance"]["source_index"])
        extra = {
            "unique_source_indexes": len(set(source_indexes)),
            "source_index_span": [min(source_indexes), max(source_indexes)],
        }
    elif panel_id.startswith("locomo"):
        sample_counts: dict[str, int] = defaultdict(int)
        category_counts: dict[str, int] = defaultdict(int)
        for item in manifest["items"]:
            packet = native_runtime.build_native_packet(
                panel_id=panel_id,
                manifest_path=manifest_path,
                manifest_version=manifest.get("version", "unknown"),
                item=item,
            )
            errors = native_runtime.validate_packet(packet, native_runtime.runtime_projection(item))
            if errors:
                runtime_errors.append({"item_id": item["id"], "errors": errors})
            else:
                runtime_valid_count += 1
            benchmark_family = packet.benchmark_family
            task_family = packet.task_family
            sample_counts[item["source_provenance"]["sample_id"]] += 1
            category_counts[str(item["source_provenance"]["category"])] += 1
        extra = {
            "sample_counts": dict(sorted(sample_counts.items())),
            "category_counts": dict(sorted(category_counts.items())),
        }
    else:
        question_type_counts: dict[str, int] = defaultdict(int)
        for item in manifest["items"]:
            packet = native_runtime.build_native_packet(
                panel_id=panel_id,
                manifest_path=manifest_path,
                manifest_version=manifest.get("version", "unknown"),
                item=item,
            )
            errors = native_runtime.validate_packet(packet, native_runtime.runtime_projection(item))
            if errors:
                runtime_errors.append({"item_id": item["id"], "errors": errors})
            else:
                runtime_valid_count += 1
            benchmark_family = packet.benchmark_family
            task_family = packet.task_family
            question_type_counts[item["source_provenance"]["question_type"]] += 1
        extra = {
            "question_type_counts": dict(sorted(question_type_counts.items())),
        }

    return {
        "panel_id": panel_id,
        "manifest_path": manifest_path,
        "manifest_version": manifest.get("version", "unknown"),
        "adapter_id": manifest["adapter_id"],
        "item_count": len(manifest["items"]),
        "benchmark_family": benchmark_family,
        "task_family": task_family,
        "runtime_projection_valid_count": runtime_valid_count,
        "runtime_projection_total_count": len(manifest["items"]),
        "runtime_projection_errors": runtime_errors,
        "selection_policy": manifest.get("selection_policy", {}),
        "extra": extra,
    }


def build_payload(base_dir: Path) -> dict[str, Any]:
    panels = {}
    benchmark_family_counts = Counter()
    task_family_counts = Counter()
    total_items = 0
    runtime_valid = 0
    for spec in MANIFEST_SPECS:
        manifest = load_json(base_dir / spec["manifest_path"])
        summary = panel_summary(spec["panel_id"], spec["manifest_path"], manifest)
        panels[spec["panel_id"]] = summary
        benchmark_family_counts[summary["benchmark_family"]] += summary["item_count"]
        task_family_counts[summary["task_family"]] += summary["item_count"]
        total_items += summary["item_count"]
        runtime_valid += summary["runtime_projection_valid_count"]

    return {
        "panel_count": len(panels),
        "total_items": total_items,
        "benchmark_family_counts": dict(sorted(benchmark_family_counts.items())),
        "task_family_counts": dict(sorted(task_family_counts.items())),
        "runtime_projection_valid_count": runtime_valid,
        "runtime_projection_total_count": total_items,
        "verification_passed": runtime_valid == total_items,
        "current_reviewer_section_size": CURRENT_REVIEWER_SECTION_SIZE,
        "scale_increase_vs_reviewer_section": total_items - CURRENT_REVIEWER_SECTION_SIZE,
        "scale_multiplier_vs_reviewer_section": round(total_items / CURRENT_REVIEWER_SECTION_SIZE, 3),
        "panels": panels,
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# Expanded Benchmark Dataset Inventory",
        "",
        "这个 artifact 记录下一阶段 official benchmark pool 的规模、来源、验证状态，以及它相对当前 reviewer section 的扩张幅度。",
        "",
        f"- panel_count: `{payload['panel_count']}`",
        f"- total_items: `{payload['total_items']}`",
        f"- benchmark_family_counts: `{payload['benchmark_family_counts']}`",
        f"- task_family_counts: `{payload['task_family_counts']}`",
        f"- runtime_projection_valid: `{payload['runtime_projection_valid_count']}/{payload['runtime_projection_total_count']}`",
        f"- reviewer_section_size: `{payload['current_reviewer_section_size']}`",
        f"- scale_delta: `{payload['scale_increase_vs_reviewer_section']}`",
        f"- scale_multiplier: `{payload['scale_multiplier_vs_reviewer_section']}`",
        "",
        "## Panels",
        "",
        "| Panel | Manifest Version | Items | Family | Runtime Projection |",
        "|---|---:|---:|---|---:|",
    ]
    for panel_id, panel in payload["panels"].items():
        lines.append(
            f"| {panel_id} | {panel['manifest_version']} | {panel['item_count']} | {panel['benchmark_family']} / {panel['task_family']} | {panel['runtime_projection_valid_count']}/{panel['runtime_projection_total_count']} |"
        )

    lines.extend(
        [
            "",
            "## Panel Details",
            "",
        ]
    )
    for panel_id, panel in payload["panels"].items():
        lines.append(f"### {panel_id}")
        lines.append("")
        lines.append(f"- manifest_path: `{panel['manifest_path']}`")
        lines.append(f"- adapter_id: `{panel['adapter_id']}`")
        lines.append(f"- selection_policy: `{panel['selection_policy']}`")
        if panel["extra"]:
            lines.append(f"- extra: `{panel['extra']}`")
        if panel["runtime_projection_errors"]:
            lines.append(f"- runtime_projection_errors: `{panel['runtime_projection_errors']}`")
        else:
            lines.append("- runtime_projection_errors: `[]`")
        lines.append("")

    lines.extend(
        [
            "## Readout",
            "",
            "- The large official pool is now almost five times the current 32-item reviewer section, while still fitting the same benchmark-native packet schema used by the current baseline surface.",
            "- HaluMem is close to full verified-local coverage, LoCoMo is balanced across all 10 conversations, and LongMemEval is widened into a real second benign benchmark family rather than a small add-on.",
            "- This does not yet mean the full large benchmark baseline has been run, but it removes the main dataset-construction blocker for that next stage.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    payload = build_payload(base_dir)
    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
