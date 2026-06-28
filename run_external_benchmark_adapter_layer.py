from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/external_benchmark_adapter_layer.json"
SUMMARY_PATH = "outputs/external_benchmark_adapter_layer.md"
REVIEWER_SECTION_RESULTS = "outputs/external_benchmark_reviewer_section.json"


def benchmark_specs(base_dir: Path) -> list[dict[str, Any]]:
    return [
        {
            "adapter_id": "halumem_hallucination_slice",
            "benchmark_family": "HaluMem-style",
            "task_type": "hallucination_risk",
            "local_source_globs": [
                "benchmarks/halumem/official_repo/**/*",
            ],
            "source_manifest_path": "benchmarks/halumem/SOURCE_MANIFEST.json",
            "frozen_slice_manifest_glob": "benchmarks/halumem/frozen_slices/*.json",
            "canonical_record_schema": {
                "item_id": "str",
                "context_messages": "list[str]",
                "query_text": "str",
                "query_field": "str",
                "gold_answer": "str",
                "hallucination_risk_type": "str",
            },
            "required_fields": [
                "item_id",
                "context_messages",
                "query_text",
                "query_field",
                "gold_answer",
                "hallucination_risk_type",
            ],
            "frozen_slice_plan": {
                "target_size": 8,
                "selection_rule": "prefer unsupported-target or clue-adjacent items that can expose false_present under repeated compaction",
                "target_metrics": [
                    "false_present_rate",
                    "direct_unsupported_answer_rate",
                    "raw_escalation_rate",
                ],
            },
            "conversion_notes": [
                "Map benchmark examples into the project's compact-answer schema without introducing local synthetic facts.",
                "Preserve benchmark provenance fields so exact closure claims can be traced back to original benchmark ids.",
            ],
        },
        {
            "adapter_id": "locomo_benign_utility_slice",
            "benchmark_family": "LoCoMo/LongMemEval-style",
            "task_type": "benign_utility",
            "local_source_globs": [
                "benchmarks/locomo/locomo_official/**/*",
                "benchmarks/locomo/longmemeval_official/README.md",
                "benchmarks/locomo/longmemeval_official/LICENSE",
                "benchmarks/locomo/longmemeval_official/custom_history/*.py",
                "benchmarks/locomo/longmemeval_official/data/cleaned/longmemeval_oracle.json",
                "benchmarks/locomo/longmemeval_official/data/cleaned/longmemeval_s_cleaned.json",
            ],
            "source_manifest_path": "benchmarks/locomo/SOURCE_MANIFEST.json",
            "frozen_slice_manifest_glob": "benchmarks/locomo/frozen_slices/*.json",
            "canonical_record_schema": {
                "item_id": "str",
                "context_messages": "list[str]",
                "query_text": "str",
                "query_field": "str",
                "gold_answer": "str",
                "utility_slice_type": "str",
            },
            "required_fields": [
                "item_id",
                "context_messages",
                "query_text",
                "query_field",
                "gold_answer",
                "utility_slice_type",
            ],
            "frozen_slice_plan": {
                "target_size": 8,
                "selection_rule": "prefer answerable benign/conflict-like items that reveal history_loss and empty_note_then_abstain under deeper compaction",
                "target_metrics": [
                    "accuracy",
                    "history_loss_rate",
                    "empty_note_then_abstain_rate",
                    "raw_escalation_rate",
                ],
            },
            "conversion_notes": [
                "Keep raw benchmark wording intact and only normalize into the project's evaluation fields.",
                "Do not hand-author substitute facts when local benchmark data is absent; mark the adapter data-pending instead.",
            ],
        },
    ]


def local_matches(base_dir: Path, pattern: str) -> list[str]:
    return sorted(str(path.relative_to(base_dir)) for path in base_dir.glob(pattern) if path.is_file())


def local_matches_many(base_dir: Path, patterns: list[str]) -> list[str]:
    matches: set[str] = set()
    for pattern in patterns:
        matches.update(local_matches(base_dir, pattern))
    return sorted(matches)


def adapter_state(raw_data_ready: bool, slice_ready: bool) -> str:
    if slice_ready:
        return "slice_ready"
    if raw_data_ready:
        return "data_ready_slice_pending"
    return "adapter_ready_data_pending"


def build_payload(base_dir: Path) -> dict[str, Any]:
    adapters = []
    data_ready_count = 0
    source_manifest_count = 0
    slice_ready_count = 0
    for spec in benchmark_specs(base_dir):
        matches = local_matches_many(base_dir, spec["local_source_globs"])
        source_manifest_matches = local_matches(base_dir, spec["source_manifest_path"])
        slice_manifests = local_matches(base_dir, spec["frozen_slice_manifest_glob"])
        local_data_ready = len(matches) > 0
        source_manifest_present = len(source_manifest_matches) > 0
        slice_ready = len(slice_manifests) > 0
        if local_data_ready:
            data_ready_count += 1
        if source_manifest_present:
            source_manifest_count += 1
        if slice_ready:
            slice_ready_count += 1
        adapters.append(
            {
                **spec,
                "source_manifest_present": source_manifest_present,
                "local_match_count": len(matches),
                "local_match_examples": matches[:5],
                "slice_manifest_count": len(slice_manifests),
                "slice_manifest_examples": slice_manifests[:5],
                "raw_data_ready": local_data_ready,
                "slice_ready": slice_ready,
                "adapter_state": adapter_state(local_data_ready, slice_ready),
                "can_run_now": slice_ready,
            }
        )

    grounding_status = "gap"
    if adapters:
        grounding_status = "partial"
    if slice_ready_count == len(adapters) and adapters:
        grounding_status = "pass"

    reviewer_section_ready = (base_dir / REVIEWER_SECTION_RESULTS).exists()
    next_requirements = [
        "audit the official raw files into one frozen hallucination slice and one frozen benign-utility slice through the adapter schema",
        "write those frozen slice manifests under the declared frozen_slice_manifest_glob paths",
        "feed those frozen slices into the paper baseline packet as benchmark-grounded panels",
    ]
    if reviewer_section_ready and slice_ready_count == len(adapters) and adapters:
        next_requirements = [
            "replace the remaining local proxy-stack internals behind the benchmark-first primary surface so TierMem-style grounding can move from partial to pass",
            "carry the broader reviewer-facing benchmark section into more slice families and larger frozen coverage",
            "keep reducing how much the reviewer-facing story depends on synthetic reference artifacts rather than benchmark-native sections",
        ]
    elif slice_ready_count == len(adapters) and adapters:
        next_requirements = [
            "run the frozen external slices through the reviewer-facing benchmark baseline panel",
            "expand the first frozen slices beyond the minimal panel once the current benchmark-grounded packet is rebuilt",
            "replace the remaining local proxy-stack framing with a TierMem-style primary benchmark base",
        ]

    return {
        "description": "Frozen adapter layer for connecting reviewer-facing benchmark slices into the paper baseline packet.",
        "grounding_status": grounding_status,
        "adapter_ready_count": len(adapters),
        "source_manifest_count": source_manifest_count,
        "data_ready_count": data_ready_count,
        "slice_ready_count": slice_ready_count,
        "reviewer_section_ready": reviewer_section_ready,
        "adapters": adapters,
        "next_requirements": next_requirements,
    }


def build_summary(payload: dict[str, Any]) -> str:
    intro = (
        "这个 artifact 还不假装 benchmark grounding 已经完成。它冻结的是一层明确可运行的 adapter contract：至少有一条 HaluMem-style hallucination slice 和一条 LoCoMo/LongMemEval-style benign-utility slice 被接入同一套 schema、字段要求和冻结规则里。当前即使 benchmark 原始数据已经进 repo，只要还没有 frozen slice manifest，状态也只能停留在 data-ready / slice-pending，而不是伪装成已经跑完 benchmark。"
        if payload["grounding_status"] != "pass"
        else "这个 artifact 现在已经不只是 adapter contract 了：一条 HaluMem-style hallucination slice 和一条 LoCoMo/LongMemEval-style benign-utility slice 都已经以 frozen manifest 的形式落在本地，所以 external benchmark grounding 至少已经推进到 slice-ready。"
    )

    lines = [
        "# External Benchmark Adapter Layer",
        "",
        intro,
        "",
        f"- grounding_status: `{payload['grounding_status']}`",
        f"- adapters: `{payload['adapter_ready_count']}`",
        f"- source_manifest_count: `{payload['source_manifest_count']}`",
        f"- data_ready_count: `{payload['data_ready_count']}`",
        f"- slice_ready_count: `{payload['slice_ready_count']}`",
        f"- reviewer_section_ready: `{payload['reviewer_section_ready']}`",
        "",
    ]
    for adapter in payload["adapters"]:
        lines.extend(
            [
                f"## {adapter['adapter_id']}",
                "",
                f"- benchmark_family: `{adapter['benchmark_family']}`",
                f"- task_type: `{adapter['task_type']}`",
                f"- adapter_state: `{adapter['adapter_state']}`",
                f"- source_manifest_path: `{adapter['source_manifest_path']}`",
                f"- source_manifest_present: `{adapter['source_manifest_present']}`",
                f"- local_source_globs: `{'; '.join(adapter['local_source_globs'])}`",
                f"- local_match_count: `{adapter['local_match_count']}`",
                f"- frozen_slice_manifest_glob: `{adapter['frozen_slice_manifest_glob']}`",
                f"- slice_manifest_count: `{adapter['slice_manifest_count']}`",
                f"- frozen_target_size: `{adapter['frozen_slice_plan']['target_size']}`",
                f"- target_metrics: `{', '.join(adapter['frozen_slice_plan']['target_metrics'])}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Next Requirements",
            "",
            *[f"- {step}" for step in payload["next_requirements"]],
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
