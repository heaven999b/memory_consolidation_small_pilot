from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import freeze_task_extension_expanded_slices as expanded_freeze
from pilot_core import load_items


V1_CONFLICT_MANIFEST = "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v1.json"
V1_UNSAFE_MANIFEST = "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v1.json"
V2_CONFLICT_MANIFEST = "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v2.json"
V2_UNSAFE_MANIFEST = "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v2.json"

UNIFIED_RESULTS = "outputs/task_extension_expanded_family_results.json"
RECALL_RESULTS = "outputs/actual_recall_expansion_results.json"
CARRY_RESULTS = "outputs/actual_carry_forward_results.json"

JSON_PATH = "outputs/task_extension_expanded_status.json"
SUMMARY_PATH = "outputs/task_extension_expanded_status.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_ids(path: Path) -> list[str]:
    return [item["id"] for item in load_json(path)["items"]]


def covered_ids_from_records(path: Path, *, family: str) -> set[str]:
    if not path.exists():
        return set()
    payload = load_json(path)
    records = payload.get("records", [])
    return {record["item_id"] for record in records if record.get("family") == family}


def build_family_status(
    *,
    family: str,
    v1_ids: list[str],
    v2_ids: list[str],
    unified_ids: set[str],
    fallback_ids: set[str],
    source_label: str,
) -> dict[str, Any]:
    covered_ids = sorted(unified_ids or fallback_ids, key=expanded_freeze.item_sort_key)
    covered_set = set(covered_ids)
    missing_ids = sorted([item_id for item_id in v2_ids if item_id not in covered_set], key=expanded_freeze.item_sort_key)
    return {
        "family": family,
        "v1_count": len(v1_ids),
        "v2_count": len(v2_ids),
        "growth": len(v2_ids) - len(v1_ids),
        "coverage_source": source_label,
        "covered_count": len([item_id for item_id in v2_ids if item_id in covered_set]),
        "missing_count": len(missing_ids),
        "ready_for_family_table": len(missing_ids) == 0,
        "covered_ids": covered_ids,
        "missing_ids": missing_ids,
    }


def build_payload(base_dir: Path) -> dict[str, Any]:
    curated_counts = Counter(item["family"] for item in load_items(base_dir))

    v1_conflict_ids = manifest_ids(base_dir / V1_CONFLICT_MANIFEST)
    v1_unsafe_ids = manifest_ids(base_dir / V1_UNSAFE_MANIFEST)
    v2_conflict_ids = manifest_ids(base_dir / V2_CONFLICT_MANIFEST)
    v2_unsafe_ids = manifest_ids(base_dir / V2_UNSAFE_MANIFEST)

    unified_path = base_dir / UNIFIED_RESULTS
    unified_conflict_ids = covered_ids_from_records(unified_path, family="conflict")
    unified_unsafe_ids = covered_ids_from_records(unified_path, family="unsafe")

    conflict_status = build_family_status(
        family="conflict",
        v1_ids=v1_conflict_ids,
        v2_ids=v2_conflict_ids,
        unified_ids=unified_conflict_ids,
        fallback_ids=covered_ids_from_records(base_dir / RECALL_RESULTS, family="conflict"),
        source_label=UNIFIED_RESULTS if unified_conflict_ids else RECALL_RESULTS,
    )
    unsafe_status = build_family_status(
        family="unsafe",
        v1_ids=v1_unsafe_ids,
        v2_ids=v2_unsafe_ids,
        unified_ids=unified_unsafe_ids,
        fallback_ids=covered_ids_from_records(base_dir / CARRY_RESULTS, family="unsafe"),
        source_label=UNIFIED_RESULTS if unified_unsafe_ids else CARRY_RESULTS,
    )

    ready = conflict_status["ready_for_family_table"] and unsafe_status["ready_for_family_table"]
    return {
        "description": "A3 status surface for scaled manifest-backed conflict/unsafe families.",
        "verdict": {
            "expanded_task_extension_ready": ready,
            "note": (
                "Both expanded task families have full model-backed coverage and can stand as dedicated family tables."
                if ready
                else "Expanded task-family manifests now exist, but at least one family still lacks full model-backed coverage."
            ),
        },
        "curated_dataset_counts": dict(sorted(curated_counts.items())),
        "manifests": {
            "conflict_v1_path": V1_CONFLICT_MANIFEST,
            "unsafe_v1_path": V1_UNSAFE_MANIFEST,
            "conflict_v2_path": V2_CONFLICT_MANIFEST,
            "unsafe_v2_path": V2_UNSAFE_MANIFEST,
        },
        "family_status": {
            "conflict": conflict_status,
            "unsafe": unsafe_status,
        },
    }


def build_summary(payload: dict[str, Any]) -> str:
    conflict = payload["family_status"]["conflict"]
    unsafe = payload["family_status"]["unsafe"]
    lines = [
        "# Expanded Task Extension Status",
        "",
        "This artifact turns A3 into an explicit status surface: how much larger the dedicated `conflict` / `unsafe` families can be, and how much model-backed coverage is still missing.",
        "",
        f"- ready: `{payload['verdict']['expanded_task_extension_ready']}`",
        f"- curated dataset counts: `{payload['curated_dataset_counts']}`",
        "",
        "| Family | v1 count | v2 count | growth | covered now | missing now | coverage source | ready |",
        "|---|---:|---:|---:|---:|---:|---|---|",
        f"| conflict | {conflict['v1_count']} | {conflict['v2_count']} | {conflict['growth']} | {conflict['covered_count']} | {conflict['missing_count']} | {conflict['coverage_source']} | {conflict['ready_for_family_table']} |",
        f"| unsafe | {unsafe['v1_count']} | {unsafe['v2_count']} | {unsafe['growth']} | {unsafe['covered_count']} | {unsafe['missing_count']} | {unsafe['coverage_source']} | {unsafe['ready_for_family_table']} |",
        "",
        "## Missing Coverage",
        "",
        f"- conflict missing ids: `{conflict['missing_ids']}`",
        f"- unsafe missing ids: `{unsafe['missing_ids']}`",
        "",
        "## Readout",
        "",
        "- The blocking issue is no longer data definition: expanded manifests exist for both families.",
        "- The remaining gap is model-backed execution coverage over the new v2 item ids.",
        "- Once the missing ids are run, these families can move from 'supporting slice' into dedicated benchmark tables.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    expanded_freeze.write_source_manifest(base_dir)
    expanded_freeze.write_task_manifests(base_dir)

    payload = build_payload(base_dir)
    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
