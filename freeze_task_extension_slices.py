from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pilot_core import load_items


SOURCE_MANIFEST_PATH = "benchmarks/task_extensions/SOURCE_MANIFEST.json"

TASK_EXTENSION_SPECS = [
    {
        "panel_id": "pilot_conflict_extension_v1",
        "manifest_path": "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v1.json",
        "version": "v1",
        "task_family": "conflict",
        "item_ids": [
            "conflict_01",
            "conflict_02",
            "conflict_03",
            "conflict_04",
        ],
        "selection_policy": (
            "Freeze the current-value conflict items that already participate in the actual recall slice "
            "so the benchmark-native primary base gains explicit manifest-backed conflict coverage."
        ),
        "selection_notes": [
            "Selected from the curated dataset because these items already anchor the real-model benign/conflict recall slice.",
            "Chosen to expose stale-value retention and merged-value corruption under repeated compaction.",
        ],
        "source_results": [
            "outputs/actual_recall_expansion_results.json",
        ],
    },
    {
        "panel_id": "pilot_unsafe_extension_v1",
        "manifest_path": "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v1.json",
        "version": "v1",
        "task_family": "unsafe",
        "item_ids": [
            "unsafe_01",
            "unsafe_04",
        ],
        "selection_policy": (
            "Freeze the refined unsafe refusal items that already participate in the carry-forward stress round "
            "so the benchmark-native primary base gains explicit manifest-backed unsafe coverage."
        ),
        "selection_notes": [
            "Selected from the curated dataset because these items already anchor the scaffold-refinement and carry-forward rounds.",
            "Chosen to expose blocked-action refusal retention rather than only benign history-loss behavior.",
        ],
        "source_results": [
            "outputs/actual_carry_forward_results.json",
            "outputs/actual_scaffold_refinement_results.json",
        ],
    },
]


def render_context_messages(item: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    for fact in item["raw_facts"]:
        state = "current" if fact["current"] else "stale"
        qualifiers = [state]
        if not fact["supported"]:
            qualifiers.append("unsupported")
        if fact["unsafe"]:
            qualifiers.append("unsafe")
        qualifier_text = ", ".join(qualifiers)
        messages.append(
            f"Memory fact for {item['subject']}: {fact['field']} = {fact['value']} ({qualifier_text}, trust={fact['trust']})."
        )
    return messages


def build_manifest_item(item: dict[str, Any], *, panel_id: str, task_family: str, selection_notes: list[str]) -> dict[str, Any]:
    manifest_item = {
        "id": item["id"],
        "family": item["family"],
        "subject": item["subject"],
        "query_text": item["query_text"],
        "query_field": item["query_field"],
        "gold_answer": item["gold_answer"],
        "criticality": item["criticality"],
        "context_messages": render_context_messages(item),
        "raw_facts": item["raw_facts"],
        "source_provenance": {
            "benchmark_family": "MemoryConsolidationPilot",
            "source_kind": "manifest_backed_task_extension",
            "source_dataset": "curated_dataset.py",
            "source_item_id": item["id"],
            "task_extension_family": task_family,
            "panel_id": panel_id,
        },
        "selection_notes": selection_notes,
    }
    if "unsafe_paraphrases" in item:
        manifest_item["unsafe_paraphrases"] = item["unsafe_paraphrases"]
    if "invention_candidates" in item:
        manifest_item["invention_candidates"] = item["invention_candidates"]
    return manifest_item


def write_source_manifest(base_dir: Path) -> None:
    payload = {
        "version": "v1",
        "source_kind": "manifest_backed_task_extensions",
        "description": (
            "Manifest-backed conflict and unsafe extension panels derived from the curated synthetic dataset "
            "so the benchmark-native primary base can cover all four task families."
        ),
        "local_source_paths": [
            "curated_dataset.py",
            "outputs/actual_recall_expansion_results.json",
            "outputs/actual_scaffold_refinement_results.json",
            "outputs/actual_carry_forward_results.json",
        ],
        "generated_manifests": [
            spec["manifest_path"] for spec in TASK_EXTENSION_SPECS
        ],
        "notes": [
            "These are not mirrored third-party benchmark files; they are frozen local task-extension manifests.",
            "They exist to make conflict and unsafe coverage explicit in the same manifest-backed primary-base structure used by the external benchmark panels.",
        ],
    }
    path = base_dir / SOURCE_MANIFEST_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_task_manifests(base_dir: Path) -> None:
    items = {item["id"]: item for item in load_items(base_dir)}
    for spec in TASK_EXTENSION_SPECS:
        manifest_items = []
        for item_id in spec["item_ids"]:
            item = items[item_id]
            manifest_items.append(
                build_manifest_item(
                    item,
                    panel_id=spec["panel_id"],
                    task_family=spec["task_family"],
                    selection_notes=spec["selection_notes"],
                )
            )
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
