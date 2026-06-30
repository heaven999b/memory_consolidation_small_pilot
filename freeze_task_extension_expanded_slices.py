from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from freeze_task_extension_slices import build_manifest_item
from pilot_core import load_items


SOURCE_MANIFEST_PATH = "benchmarks/task_extensions/SOURCE_MANIFEST_expanded_v2.json"

TASK_EXTENSION_SPECS = [
    {
        "panel_id": "pilot_conflict_extension_v2",
        "manifest_path": "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v2.json",
        "version": "v2",
        "task_family": "conflict",
        "selection_policy": (
            "Freeze the full curated conflict family so the benchmark-native story is no longer carried by only four "
            "pilot examples and can support a dedicated conflict table."
        ),
        "selection_notes": [
            "Expanded from the curated synthetic dataset to cover the full conflict family rather than the earlier 4-item bridge slice.",
            "Chosen to test stale-value retention, merged-value corruption, and current-value recovery at a scale that can stand on its own table.",
        ],
        "source_results": [
            "outputs/actual_recall_expansion_results.json",
            "outputs/task_extension_expanded_family_results.json",
        ],
    },
    {
        "panel_id": "pilot_unsafe_extension_v2",
        "manifest_path": "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v2.json",
        "version": "v2",
        "task_family": "unsafe",
        "selection_policy": (
            "Freeze the full curated unsafe family so the blocked-action refusal story is no longer supported by only "
            "two examples and can support a dedicated unsafe table."
        ),
        "selection_notes": [
            "Expanded from the curated synthetic dataset to cover the full unsafe family rather than the earlier 2-item bridge slice.",
            "Chosen to test whether unsafe laundering and refusal retention survive repeated compaction across multiple policy scenarios.",
        ],
        "source_results": [
            "outputs/actual_carry_forward_results.json",
            "outputs/task_extension_expanded_family_results.json",
        ],
    },
]


def item_sort_key(item_id: str) -> tuple[str, int]:
    prefix, _, suffix = item_id.rpartition("_")
    try:
        return prefix, int(suffix)
    except ValueError:
        return prefix, 0


def write_source_manifest(base_dir: Path) -> None:
    payload = {
        "version": "v2",
        "source_kind": "manifest_backed_task_extensions",
        "description": (
            "Expanded manifest-backed conflict and unsafe extension panels derived from the curated synthetic dataset "
            "so the paper-facing benchmark can carry larger dedicated family tables."
        ),
        "local_source_paths": [
            "curated_dataset.py",
            "outputs/actual_recall_expansion_results.json",
            "outputs/actual_carry_forward_results.json",
            "outputs/task_extension_expanded_family_results.json",
        ],
        "generated_manifests": [spec["manifest_path"] for spec in TASK_EXTENSION_SPECS],
        "notes": [
            "These expanded manifests preserve the local pilot family source while moving beyond the tiny v1 bridge slices.",
            "They are meant for A3-style family-scale reporting rather than replacing the original small v1 compatibility panels.",
        ],
    }
    path = base_dir / SOURCE_MANIFEST_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_items_by_family(base_dir: Path) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in load_items(base_dir):
        grouped.setdefault(item["family"], []).append(item)
    for family_items in grouped.values():
        family_items.sort(key=lambda item: item_sort_key(item["id"]))
    return grouped


def write_task_manifests(base_dir: Path) -> None:
    items_by_family = build_items_by_family(base_dir)
    for spec in TASK_EXTENSION_SPECS:
        manifest_items = [
            build_manifest_item(
                item,
                panel_id=spec["panel_id"],
                task_family=spec["task_family"],
                selection_notes=spec["selection_notes"],
            )
            for item in items_by_family[spec["task_family"]]
        ]
        payload = {
            "adapter_id": spec["panel_id"],
            "version": spec["version"],
            "selection_policy": spec["selection_policy"],
            "task_family": spec["task_family"],
            "source_results": spec["source_results"],
            "items": manifest_items,
        }
        path = base_dir / spec["manifest_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {path}")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    write_source_manifest(base_dir)
    write_task_manifests(base_dir)
    print(f"Wrote {base_dir / SOURCE_MANIFEST_PATH}")


if __name__ == "__main__":
    main()
