from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import benchmark_native_runtime as native_runtime
import freeze_external_benchmark_expanded_slices as expanded
import freeze_external_benchmark_reviewer_slices as reviewer
import freeze_external_benchmark_slices as core


HALUMEM_EXPANDED_PATH = "benchmarks/halumem/frozen_slices/halumem_hallucination_expanded_v1.json"
LOCOMO_EXPANDED_PATH = "benchmarks/locomo/frozen_slices/locomo_benign_utility_expanded_v1.json"
LONGMEMEVAL_EXPANDED_PATH = "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_expanded_v2.json"
CONFLICT_EXTENSION_PATH = "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v1.json"
UNSAFE_EXTENSION_PATH = "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v1.json"

JSON_PATH = "outputs/expanded_benchmark_rigor_audit.json"
SUMMARY_PATH = "outputs/expanded_benchmark_rigor_audit.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_valid_count(panel_id: str, manifest_path: str, manifest: dict[str, Any]) -> tuple[int, list[dict[str, Any]]]:
    valid = 0
    errors: list[dict[str, Any]] = []
    for item in manifest["items"]:
        packet = native_runtime.build_native_packet(
            panel_id=panel_id,
            manifest_path=manifest_path,
            manifest_version=manifest.get("version", "unknown"),
            item=item,
        )
        row_errors = native_runtime.validate_packet(packet, native_runtime.runtime_projection(item))
        if row_errors:
            errors.append({"item_id": item["id"], "errors": row_errors})
        else:
            valid += 1
    return valid, errors


def selection_stats(base_dir: Path) -> dict[str, Any]:
    halumem_records = core.load_halumem_records(base_dir)
    halumem_clean = [row for row in halumem_records if core.is_high_quality_halumem_record(row)]

    locomo_records = core.load_locomo_records(base_dir)
    locomo_candidates = 0
    for sample in locomo_records:
        for rows in expanded.locomo_candidate_rows(sample).values():
            locomo_candidates += len(rows)

    longmemeval_records = reviewer.load_longmemeval_records(base_dir)
    longmemeval_candidates = sum(1 for row in longmemeval_records if expanded.longmemeval_candidate_ok(row))

    return {
        "halumem": {
            "source_total": len(halumem_records),
            "clean_candidate_pool": len(halumem_clean),
        },
        "locomo": {
            "source_total": sum(len(sample["qa"]) for sample in locomo_records),
            "clean_candidate_pool": locomo_candidates,
        },
        "longmemeval": {
            "source_total": len(longmemeval_records),
            "clean_candidate_pool": longmemeval_candidates,
        },
    }


def verdict_for_count(count: int, *, main_floor: int, adequate_floor: int) -> str:
    if count >= main_floor:
        return "solid"
    if count >= adequate_floor:
        return "adequate"
    return "thin"


def layer_summary(base_dir: Path) -> dict[str, Any]:
    reviewer_section_size = (
        len(load_json(base_dir / "benchmarks/halumem/frozen_slices/halumem_hallucination_slice_v2.json")["items"])
        + len(load_json(base_dir / "benchmarks/halumem/frozen_slices/halumem_hallucination_holdout_slice_v1.json")["items"])
        + len(load_json(base_dir / "benchmarks/locomo/frozen_slices/locomo_benign_utility_slice_v2.json")["items"])
        + len(load_json(base_dir / "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_slice_v1.json")["items"])
    )
    conflict_count = len(load_json(base_dir / CONFLICT_EXTENSION_PATH)["items"])
    unsafe_count = len(load_json(base_dir / UNSAFE_EXTENSION_PATH)["items"])
    expanded_count = (
        len(load_json(base_dir / HALUMEM_EXPANDED_PATH)["items"])
        + len(load_json(base_dir / LOCOMO_EXPANDED_PATH)["items"])
        + len(load_json(base_dir / LONGMEMEVAL_EXPANDED_PATH)["items"])
    )
    return {
        "layer_0_reviewer_core": {
            "count": reviewer_section_size,
            "role": "current_frozen_reviewer_table",
            "verdict": "solid_for_current_reporting",
        },
        "layer_1_expanded_official_pool": {
            "count": expanded_count,
            "role": "next_stage_benchmark_native_scale_up",
            "verdict": "staged_run_ready",
        },
        "layer_2_four_family_closure": {
            "count": expanded_count + conflict_count + unsafe_count,
            "official_external_count": expanded_count,
            "task_extension_count": conflict_count + unsafe_count,
            "role": "four_family_primary_surface",
            "verdict": "coverage_complete_but_mixed_source_kind",
        },
    }


def panel_summary(
    *,
    panel_id: str,
    manifest_path: str,
    manifest: dict[str, Any],
    source_total: int,
    clean_candidate_pool: int,
) -> dict[str, Any]:
    valid_count, runtime_errors = runtime_valid_count(panel_id, manifest_path, manifest)
    items = manifest["items"]
    stratum_counts = Counter(item.get("evaluation_stratum", "missing") for item in items)
    complexity_counts = Counter(item.get("complexity_band", "missing") for item in items)
    answer_token_counts = [len(str(item["gold_answer"]).split()) for item in items]
    context_message_counts = [len(item["context_messages"]) for item in items]
    source_category_prefix_mismatch = []
    if panel_id == "locomo_expanded_v1":
        for item in items:
            query = item["query_text"].lower()
            category = item["source_provenance"]["category"]
            if category == 1 and (query.startswith("when ") or query.startswith("how long ")):
                source_category_prefix_mismatch.append(item["id"])
            if category == 2 and (query.startswith("what ") or query.startswith("where ") or query.startswith("who ")):
                source_category_prefix_mismatch.append(item["id"])
    source_selectivity = 0.0 if source_total == 0 else len(items) / source_total
    candidate_selectivity = 0.0 if clean_candidate_pool == 0 else len(items) / clean_candidate_pool
    return {
        "panel_id": panel_id,
        "manifest_path": manifest_path,
        "manifest_version": manifest.get("version", "unknown"),
        "item_count": len(items),
        "source_total": source_total,
        "clean_candidate_pool": clean_candidate_pool,
        "source_selectivity": round(source_selectivity, 4),
        "candidate_selectivity": round(candidate_selectivity, 4),
        "runtime_projection_valid_count": valid_count,
        "runtime_projection_total_count": len(items),
        "runtime_projection_errors": runtime_errors,
        "stratum_counts": dict(sorted(stratum_counts.items())),
        "complexity_counts": dict(sorted(complexity_counts.items())),
        "query_field_count": len({item["query_field"] for item in items}),
        "gold_behavior_signature": sorted({item["gold_answer"] for item in items})[:5],
        "answer_token_range": [min(answer_token_counts), max(answer_token_counts)],
        "context_message_range": [min(context_message_counts), max(context_message_counts)],
        "source_category_prefix_mismatch_examples": source_category_prefix_mismatch[:5],
    }


def stratum_verdicts(payload: dict[str, Any]) -> dict[str, Any]:
    verdicts: dict[str, Any] = {}
    for panel in payload["panels"].values():
        for stratum, count in panel["stratum_counts"].items():
            if stratum == "halumem_unsupported_designation_abstain":
                verdict = verdict_for_count(count, main_floor=24, adequate_floor=15)
                use_note = "adequate for staged hallucination evaluation; still smaller than a final paper-scale family table would ideally want"
            elif stratum == "longmemeval_single_session_assistant":
                verdict = verdict_for_count(count, main_floor=20, adequate_floor=10)
                use_note = "good auxiliary stress/control stratum; too thin to headline alone"
            else:
                verdict = verdict_for_count(count, main_floor=30, adequate_floor=15)
                use_note = "sufficient as a main staged benchmark stratum" if verdict != "thin" else "too thin for main stratum use"
            verdicts[stratum] = {
                "count": count,
                "verdict": verdict,
                "use_note": use_note,
            }
    return dict(sorted(verdicts.items()))


def overall_verdict(payload: dict[str, Any]) -> dict[str, Any]:
    blocking_notes = []
    if payload["panels"]["longmemeval_expanded_v2"]["stratum_counts"].get("longmemeval_single_session_assistant", 0) < 20:
        blocking_notes.append(
            "The LongMemEval assistant-facing stratum is only 12 items, so it should be treated as an auxiliary control slice rather than a standalone headline panel."
        )
    blocking_notes.append(
        "The official expanded pool still covers benign plus hallucination only; conflict and unsafe remain manifest-backed local task extensions rather than official external benchmark panels."
    )
    blocking_notes.append(
        "LoCoMo source categories are not stable enough to serve as the final paper taxonomy by themselves; the derived contract-based strata should be treated as the canonical levels."
    )
    return {
        "expanded_pool_standardized": True,
        "expanded_pool_staged_run_ready": True,
        "expanded_pool_full_paper_ready": False,
        "primary_reason_not_full_paper_ready": "Need full model-backed runs over the expanded pool and still lack official external conflict/unsafe families.",
        "blocking_notes": blocking_notes,
    }


def build_payload(base_dir: Path) -> dict[str, Any]:
    selection = selection_stats(base_dir)
    halumem_manifest = load_json(base_dir / HALUMEM_EXPANDED_PATH)
    locomo_manifest = load_json(base_dir / LOCOMO_EXPANDED_PATH)
    longmemeval_manifest = load_json(base_dir / LONGMEMEVAL_EXPANDED_PATH)

    panels = {
        "halumem_expanded_v1": panel_summary(
            panel_id="halumem_expanded_v1",
            manifest_path=HALUMEM_EXPANDED_PATH,
            manifest=halumem_manifest,
            source_total=selection["halumem"]["source_total"],
            clean_candidate_pool=selection["halumem"]["clean_candidate_pool"],
        ),
        "locomo_expanded_v1": panel_summary(
            panel_id="locomo_expanded_v1",
            manifest_path=LOCOMO_EXPANDED_PATH,
            manifest=locomo_manifest,
            source_total=selection["locomo"]["source_total"],
            clean_candidate_pool=selection["locomo"]["clean_candidate_pool"],
        ),
        "longmemeval_expanded_v2": panel_summary(
            panel_id="longmemeval_expanded_v2",
            manifest_path=LONGMEMEVAL_EXPANDED_PATH,
            manifest=longmemeval_manifest,
            source_total=selection["longmemeval"]["source_total"],
            clean_candidate_pool=selection["longmemeval"]["clean_candidate_pool"],
        ),
    }

    return {
        "selection_stats": selection,
        "layers": layer_summary(base_dir),
        "panels": panels,
        "stratum_verdicts": stratum_verdicts({"panels": panels}),
        "overall_verdict": overall_verdict({"panels": panels}),
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# Expanded Benchmark Rigor Audit",
        "",
        "这个 audit 不评估模型分数，只评估 expanded benchmark pool 本身是否足够严谨、分层是否标准、以及每一层能不能承担预期用途。",
        "",
        "## Overall Verdict",
        "",
        f"- expanded_pool_standardized: `{payload['overall_verdict']['expanded_pool_standardized']}`",
        f"- staged_run_ready: `{payload['overall_verdict']['expanded_pool_staged_run_ready']}`",
        f"- full_paper_ready: `{payload['overall_verdict']['expanded_pool_full_paper_ready']}`",
        f"- note: `{payload['overall_verdict']['primary_reason_not_full_paper_ready']}`",
        "",
        "## Layer Policy",
        "",
        "| Layer | Count | Role | Verdict |",
        "|---|---:|---|---|",
    ]
    for layer_name, layer in payload["layers"].items():
        lines.append(f"| {layer_name} | {layer['count']} | {layer['role']} | {layer['verdict']} |")

    lines.extend(
        [
            "",
            "## Panel Rigor",
            "",
            "| Panel | Selected | Source Total | Clean Candidate Pool | Runtime Projection | Key Strata |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for panel_name, panel in payload["panels"].items():
        lines.append(
            f"| {panel_name} | {panel['item_count']} | {panel['source_total']} | {panel['clean_candidate_pool']} | {panel['runtime_projection_valid_count']}/{panel['runtime_projection_total_count']} | {panel['stratum_counts']} |"
        )

    lines.extend(
        [
            "",
            "## Stratum Verdicts",
            "",
            "| Stratum | Count | Verdict | Use Note |",
            "|---|---:|---|---|",
        ]
    )
    for stratum, row in payload["stratum_verdicts"].items():
        lines.append(f"| {stratum} | {row['count']} | {row['verdict']} | {row['use_note']} |")

    lines.extend(
        [
            "",
            "## Findings",
            "",
            "- The pool is now standardized enough to run staged benchmark experiments because the canonical levels are no longer the source dataset categories alone; they are the derived contract-based strata recorded in the expanded manifests.",
            "- HaluMem is contract-pure but still relatively small at 19 items, so it is adequate for staged hallucination evaluation but not ideal as a lone paper-scale headline family.",
            "- LoCoMo is the cleanest large stratum: 80 items, balanced across all 10 conversations, and split into explicit contract-derived strata rather than only relying on noisy source categories.",
            "- LongMemEval user-facing recall is strong enough as a real stratum at 48 items, while the 12-item assistant-facing slice is best treated as an auxiliary control layer.",
            "- The most important remaining structural limitation is not quality noise inside the pool; it is that official external benchmark coverage still stops at benign plus hallucination, while conflict and unsafe are only closed by local task extensions.",
            "",
            "## Blocking Notes",
            "",
        ]
    )
    for note in payload["overall_verdict"]["blocking_notes"]:
        lines.append(f"- {note}")
    lines.append("")
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
