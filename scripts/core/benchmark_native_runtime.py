from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


MANIFEST_SPECS = [
    {
        "panel_id": "halumem_core_v2",
        "manifest_path": "benchmarks/halumem/frozen_slices/halumem_hallucination_slice_v2.json",
    },
    {
        "panel_id": "halumem_holdout_v1",
        "manifest_path": "benchmarks/halumem/frozen_slices/halumem_hallucination_holdout_slice_v1.json",
    },
    {
        "panel_id": "locomo_core_v2",
        "manifest_path": "benchmarks/locomo/frozen_slices/locomo_benign_utility_slice_v2.json",
    },
    {
        "panel_id": "longmemeval_direct_v1",
        "manifest_path": "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_slice_v1.json",
    },
    {
        "panel_id": "pilot_conflict_extension_v1",
        "manifest_path": "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v1.json",
    },
    {
        "panel_id": "pilot_unsafe_extension_v1",
        "manifest_path": "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v1.json",
    },
]


@dataclass
class BenchmarkNativePacket:
    panel_id: str
    manifest_path: str
    manifest_version: str
    item_id: str
    benchmark_family: str
    task_family: str
    query_contract: str
    evidence_contract: str
    gold_behavior: str
    subject: str
    query_text: str
    query_field: str
    gold_answer: str
    criticality: str
    context_messages: list[str]
    source_provenance: dict[str, Any]
    selection_notes: list[str]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_projection(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item["id"],
        "family": item["family"],
        "subject": item["subject"],
        "query_text": item["query_text"],
        "query_field": item["query_field"],
        "gold_answer": item["gold_answer"],
        "criticality": item["criticality"],
        "context_messages": list(item["context_messages"]),
        "raw_facts": list(item["raw_facts"]),
        "source_provenance": dict(item["source_provenance"]),
    }


def infer_query_contract(item: dict[str, Any]) -> str:
    if item["family"] == "hallucination":
        return "unsupported_explicit_designation_query"
    if item["family"] == "conflict":
        return "current_value_resolution_query"
    if item["family"] == "unsafe":
        return "policy_blocked_action_query"
    benchmark_family = item.get("source_provenance", {}).get("benchmark_family")
    if benchmark_family == "LoCoMo":
        return "direct_evidence_grounded_benchmark_qa"
    if benchmark_family == "LongMemEval":
        return "single_session_direct_benchmark_qa"
    return "direct_supported_benchmark_qa"


def infer_evidence_contract(item: dict[str, Any]) -> str:
    if item["family"] == "hallucination":
        return "support_clue_adjacency_without_explicit_designation"
    if item["family"] == "conflict":
        return "stale_current_dual_fact_context"
    if item["family"] == "unsafe":
        return "policy_reason_and_blocked_action_context"
    benchmark_family = item.get("source_provenance", {}).get("benchmark_family")
    if benchmark_family == "LoCoMo":
        return "evidence_id_local_context_window"
    if benchmark_family == "LongMemEval":
        return "answer_session_context_window"
    return "direct_context_window"


def infer_gold_behavior(item: dict[str, Any]) -> str:
    if item["family"] == "hallucination":
        return "abstain_on_unsupported_target"
    if item["family"] == "conflict":
        return "return_current_supported_value"
    if item["family"] == "unsafe":
        return "refuse_and_escalate_on_blocked_action"
    return "return_supported_benchmark_answer"


def build_native_packet(
    *,
    panel_id: str,
    manifest_path: str,
    manifest_version: str,
    item: dict[str, Any],
) -> BenchmarkNativePacket:
    return BenchmarkNativePacket(
        panel_id=panel_id,
        manifest_path=manifest_path,
        manifest_version=manifest_version,
        item_id=item["id"],
        benchmark_family=item["source_provenance"]["benchmark_family"],
        task_family=item["family"],
        query_contract=infer_query_contract(item),
        evidence_contract=infer_evidence_contract(item),
        gold_behavior=infer_gold_behavior(item),
        subject=item["subject"],
        query_text=item["query_text"],
        query_field=item["query_field"],
        gold_answer=item["gold_answer"],
        criticality=item["criticality"],
        context_messages=list(item["context_messages"]),
        source_provenance=dict(item["source_provenance"]),
        selection_notes=list(item.get("selection_notes", [])),
    )


def validate_packet(packet: BenchmarkNativePacket, runtime_item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not packet.context_messages:
        errors.append("missing_context_messages")
    if not packet.query_text.strip():
        errors.append("missing_query_text")
    if not packet.query_field.strip():
        errors.append("missing_query_field")
    if packet.benchmark_family not in {"HaluMem", "LoCoMo", "LongMemEval", "MemoryConsolidationPilot"}:
        errors.append(f"unexpected_benchmark_family:{packet.benchmark_family}")
    if runtime_item["id"] != packet.item_id:
        errors.append("runtime_projection_id_mismatch")
    if runtime_item["query_field"] != packet.query_field:
        errors.append("runtime_projection_query_field_mismatch")
    if runtime_item["gold_answer"] != packet.gold_answer:
        errors.append("runtime_projection_gold_answer_mismatch")
    if len(runtime_item["raw_facts"]) == 0:
        errors.append("runtime_projection_missing_raw_facts")
    return errors


def load_native_panels(base_dir: Path) -> dict[str, dict[str, Any]]:
    payload: dict[str, dict[str, Any]] = {}
    for spec in MANIFEST_SPECS:
        manifest = load_json(base_dir / spec["manifest_path"])
        packets: list[BenchmarkNativePacket] = []
        audits: list[dict[str, Any]] = []
        for item in manifest["items"]:
            packet = build_native_packet(
                panel_id=spec["panel_id"],
                manifest_path=spec["manifest_path"],
                manifest_version=manifest.get("version", "unknown"),
                item=item,
            )
            runtime_item_dict = runtime_projection(item)
            errors = validate_packet(packet, runtime_item_dict)
            packets.append(packet)
            audits.append(
                {
                    "item_id": packet.item_id,
                    "errors": errors,
                    "runtime_projection_valid": len(errors) == 0,
                    "context_message_count": len(packet.context_messages),
                    "raw_fact_count": len(runtime_item_dict["raw_facts"]),
                }
            )
        payload[spec["panel_id"]] = {
            "manifest_path": spec["manifest_path"],
            "manifest_version": manifest.get("version", "unknown"),
            "packets": packets,
            "audits": audits,
        }
    return payload


def summarize_native_panels(native_panels: dict[str, dict[str, Any]]) -> dict[str, Any]:
    all_packets = [
        packet
        for panel in native_panels.values()
        for packet in panel["packets"]
    ]
    all_audits = [
        audit
        for panel in native_panels.values()
        for audit in panel["audits"]
    ]
    benchmark_family_counts = Counter(packet.benchmark_family for packet in all_packets)
    task_family_counts = Counter(packet.task_family for packet in all_packets)
    query_contract_counts = Counter(packet.query_contract for packet in all_packets)
    evidence_contract_counts = Counter(packet.evidence_contract for packet in all_packets)
    gold_behavior_counts = Counter(packet.gold_behavior for packet in all_packets)
    runtime_projection_valid = sum(1 for audit in all_audits if audit["runtime_projection_valid"])
    return {
        "panel_count": len(native_panels),
        "item_count": len(all_packets),
        "benchmark_families": sorted(benchmark_family_counts),
        "task_families": sorted(task_family_counts),
        "benchmark_family_counts": dict(benchmark_family_counts),
        "task_family_counts": dict(task_family_counts),
        "query_contract_counts": dict(query_contract_counts),
        "evidence_contract_counts": dict(evidence_contract_counts),
        "gold_behavior_counts": dict(gold_behavior_counts),
        "runtime_projection_valid_count": runtime_projection_valid,
        "runtime_projection_total_count": len(all_audits),
    }


def packet_to_dict(packet: BenchmarkNativePacket) -> dict[str, Any]:
    return asdict(packet)
