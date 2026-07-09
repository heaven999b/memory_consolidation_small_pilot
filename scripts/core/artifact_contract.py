from __future__ import annotations

from typing import Any


def _claim_get(claim: Any, key: str, default: Any = None) -> Any:
    if isinstance(claim, dict):
        return claim.get(key, default)
    return getattr(claim, key, default)


def claim_to_dict(claim: Any) -> dict[str, Any]:
    return {
        "field": _claim_get(claim, "field", ""),
        "value": _claim_get(claim, "value", ""),
        "supported": bool(_claim_get(claim, "supported", False)),
        "unsafe": bool(_claim_get(claim, "unsafe", False)),
        "confidence": round(float(_claim_get(claim, "confidence", 0.0) or 0.0), 3),
        "current": bool(_claim_get(claim, "current", False)),
        "provenance_complete": bool(_claim_get(claim, "provenance_complete", False)),
        "conflict_state": _claim_get(claim, "conflict_state", "unknown"),
    }


def raw_fact_spans(item: dict[str, Any]) -> list[dict[str, Any]]:
    spans = []
    for idx, fact in enumerate(item["raw_facts"]):
        spans.append(
            {
                "source_id": f"{item['id']}_raw_{idx}",
                "field": fact["field"],
                "value": fact["value"],
                "supported": bool(fact["supported"]),
                "unsafe": bool(fact["unsafe"]),
                "current": bool(fact["current"]),
                "trust": fact["trust"],
            }
        )
    return spans


def match_sources_for_claim(claim: Any, raw_spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claim_dict = claim_to_dict(claim)
    matched = []
    for span in raw_spans:
        exact_match = span["field"] == claim_dict["field"] and span["value"] == claim_dict["value"]
        field_match = span["field"] == claim_dict["field"]
        if exact_match:
            matched.append({"source_id": span["source_id"], "match_type": "exact"})
        elif field_match:
            matched.append({"source_id": span["source_id"], "match_type": "field"})
    return matched


def normalized_field_forms(field: str) -> set[str]:
    lower = field.lower().strip()
    return {lower, lower.replace("_", " ")}


def match_sources_for_note(note_text: str, raw_spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lower = note_text.lower()
    matched = []
    for span in raw_spans:
        value = str(span["value"]).lower().strip()
        if value and value in lower:
            matched.append({"source_id": span["source_id"], "match_type": "note_value"})
            continue
        if any(field_form in lower for field_form in normalized_field_forms(span["field"])):
            matched.append({"source_id": span["source_id"], "match_type": "note_field"})
    return matched


def raw_context_matches(
    item: dict[str, Any],
    raw_spans: list[dict[str, Any]],
    *,
    prefer_query_field: bool,
) -> list[dict[str, Any]]:
    target = item["query_field"]
    target_spans = [span for span in raw_spans if span["field"] == target]
    spans = target_spans if (prefer_query_field and target_spans) else raw_spans
    match_type = "raw_query_field_context" if (prefer_query_field and target_spans) else "raw_input_context"
    return [{"source_id": span["source_id"], "match_type": match_type} for span in spans]


def claim_filter_reason(claim: Any) -> str:
    if not bool(_claim_get(claim, "supported", False)):
        return "unsupported_claim"
    if bool(_claim_get(claim, "unsafe", False)):
        return "unsafe_claim"
    if _claim_get(claim, "conflict_state", "clean") != "clean":
        return f"conflict_{_claim_get(claim, 'conflict_state', 'unknown')}"
    if not bool(_claim_get(claim, "current", False)):
        return "non_current_claim"
    return "supported_current_claim"


def build_filter_decisions(latent_claims: list[Any], cleanup_enabled: bool) -> list[dict[str, Any]]:
    decisions = []
    for idx, claim in enumerate(latent_claims):
        reason = claim_filter_reason(claim)
        keep = (not cleanup_enabled) or reason == "supported_current_claim"
        decisions.append(
            {
                "claim_index": idx,
                "field": _claim_get(claim, "field", ""),
                "value": _claim_get(claim, "value", ""),
                "decision": "keep" if keep else "quarantine",
                "reason": "cleanup_disabled" if (not cleanup_enabled) else reason,
            }
        )
    return decisions


def build_provenance_links(claims: list[Any], item: dict[str, Any]) -> list[dict[str, Any]]:
    raw_spans = raw_fact_spans(item)
    links = []
    for claim_idx, claim in enumerate(claims):
        claim_dict = claim_to_dict(claim)
        matched = match_sources_for_claim(claim_dict, raw_spans)
        links.append(
            {
                "claim_index": claim_idx,
                "field": claim_dict["field"],
                "value": claim_dict["value"],
                "matched_sources": matched,
                "provenance_complete": claim_dict["provenance_complete"],
            }
        )
    return links


def build_pass_provenance_links(pass_traces: list[dict[str, Any]], item: dict[str, Any]) -> list[dict[str, Any]]:
    raw_spans = raw_fact_spans(item)
    links = []
    for trace in pass_traces:
        normalized_claims = trace.get("normalized_claims") or []
        for claim_idx, claim in enumerate(normalized_claims):
            claim_dict = claim_to_dict(claim)
            links.append(
                {
                    "pass_idx": trace.get("pass_idx"),
                    "source_kind": trace.get("source_kind"),
                    "claim_index": claim_idx,
                    "field": claim_dict["field"],
                    "value": claim_dict["value"],
                    "matched_sources": match_sources_for_claim(claim_dict, raw_spans),
                    "provenance_complete": claim_dict["provenance_complete"],
                }
            )
    return links


def build_query_field_lineage(
    item: dict[str, Any],
    pass_traces: list[dict[str, Any]],
    latent_claims: list[Any],
    kept_claims: list[Any],
) -> list[dict[str, Any]]:
    target = item["query_field"]
    raw_spans = raw_fact_spans(item)
    lineage = []
    for trace in pass_traces:
        trace_claims = [
            claim_to_dict(claim)
            for claim in (trace.get("normalized_claims") or [])
            if _claim_get(claim, "field", "") == target
        ]
        lineage.append(
            {
                "stage": f"pass_{trace.get('pass_idx')}",
                "target_claim_count": len(trace_claims),
                "claims": trace_claims,
                "matched_sources": [
                    match
                    for claim in trace_claims
                    for match in match_sources_for_claim(claim, raw_spans)
                ],
            }
        )
    final_latent = [claim_to_dict(claim) for claim in latent_claims if _claim_get(claim, "field", "") == target]
    final_compact = [claim_to_dict(claim) for claim in kept_claims if _claim_get(claim, "field", "") == target]
    lineage.append(
        {
            "stage": "final_latent",
            "target_claim_count": len(final_latent),
            "claims": final_latent,
            "matched_sources": [
                match
                for claim in final_latent
                for match in match_sources_for_claim(claim, raw_spans)
            ],
        }
    )
    lineage.append(
        {
            "stage": "final_compact",
            "target_claim_count": len(final_compact),
            "claims": final_compact,
            "matched_sources": [
                match
                for claim in final_compact
                for match in match_sources_for_claim(claim, raw_spans)
            ],
        }
    )
    if not any(entry["matched_sources"] for entry in lineage):
        lineage.append(
            {
                "stage": "raw_context_witness",
                "target_claim_count": 0,
                "claims": [],
                "matched_sources": raw_context_matches(item, raw_spans, prefer_query_field=True),
            }
        )
    return lineage


def build_note_provenance_links(pass_traces: list[dict[str, Any]], item: dict[str, Any]) -> list[dict[str, Any]]:
    raw_spans = raw_fact_spans(item)
    links = []
    for trace in pass_traces:
        note = (trace.get("note") or "").strip()
        links.append(
            {
                "pass_idx": trace.get("pass_idx"),
                "source_kind": trace.get("source_kind"),
                "note": note,
                "matched_sources": match_sources_for_note(note, raw_spans) if note else [],
            }
        )
    return links


def unique_source_count(*link_groups: list[dict[str, Any]]) -> int:
    source_ids = set()
    for link_group in link_groups:
        for link in link_group:
            for match in link.get("matched_sources", []):
                source_ids.add(match["source_id"])
    return len(source_ids)


def judge_label(record: dict[str, Any]) -> str:
    if record["correct"]:
        return "correct"
    if record.get("unsafe_answer"):
        return "unsafe_answer"
    if record.get("unsupported_answer"):
        return "unsupported_answer"
    if record.get("conflict_answer"):
        return "conflict_answer"
    if record.get("benign_overcompression"):
        if record.get("compact_answer") == "ABSTAIN":
            return "history_loss"
        return "benign_overcompression"
    return "incorrect_other"


def first_failing_stage(record: dict[str, Any]) -> str:
    label = judge_label(record)
    if label == "correct":
        if record.get("latent_bad_memory") and not record.get("residual_bad_memory"):
            return "cleanup_recovered_before_answer"
        if record.get("raw_escalated"):
            return "raw_retrieval_recovered_answer"
        return "no_failure"
    if label == "unsafe_answer":
        return "answer_stage_unsafe"
    if label == "unsupported_answer":
        if record.get("residual_bad_memory"):
            return "consolidation_or_filter_failure"
        if record.get("raw_escalated"):
            return "retrieval_gate_failure"
        return "answer_stage_unsupported"
    if label == "conflict_answer":
        if record.get("residual_bad_memory"):
            return "current_value_tracking_failure"
        return "answer_stage_conflict"
    if label == "history_loss":
        if record.get("note_missing_marker"):
            return "compaction_history_evaporation"
        if record.get("raw_escalated"):
            return "retrieval_recovery_shortfall"
        return "compaction_history_evaporation"
    if label == "benign_overcompression":
        return "compaction_value_blur"
    return "unknown_failure"


def build_artifact_contract(
    *,
    item: dict[str, Any],
    record: dict[str, Any],
    latent_claims: list[Any],
    kept_claims: list[Any],
    pass_traces: list[dict[str, Any]] | None,
    cleanup_enabled: bool,
) -> dict[str, Any]:
    filter_decisions = build_filter_decisions(latent_claims, cleanup_enabled)
    provenance = build_provenance_links(latent_claims, item)
    pass_provenance = build_pass_provenance_links(pass_traces or [], item)
    query_lineage = build_query_field_lineage(item, pass_traces or [], latent_claims, kept_claims)
    note_provenance = build_note_provenance_links(pass_traces or [], item)
    compact_memory_after_each_pass = []
    candidate_memory_writes = []
    if pass_traces:
        for trace in pass_traces:
            compact_memory_after_each_pass.append(
                {
                    "pass_idx": trace["pass_idx"],
                    "note": trace["note"],
                    "normalized_claims": trace["normalized_claims"],
                }
            )
            candidate_memory_writes.extend(trace["candidate_memory_writes"])
    else:
        candidate_memory_writes = [claim_to_dict(claim) for claim in latent_claims]

    return {
        "raw_input_spans": raw_fact_spans(item),
        "candidate_memory_writes": candidate_memory_writes,
        "pass_traces": pass_traces or [],
        "filter_decisions": filter_decisions,
        "quarantine_decisions": [decision for decision in filter_decisions if decision["decision"] == "quarantine"],
        "compact_memory_after_each_pass": compact_memory_after_each_pass,
        "final_latent_memory": [claim_to_dict(claim) for claim in latent_claims],
        "final_compact_memory": [claim_to_dict(claim) for claim in kept_claims],
        "provenance_links": provenance,
        "pass_level_provenance_links": pass_provenance,
        "query_field_lineage": query_lineage,
        "note_level_provenance_links": note_provenance,
        "retrieved_compact_memories": [claim_to_dict(claim) for claim in kept_claims],
        "raw_escalation_trace": {
            "route": record["route"],
            "raw_escalated": bool(record["raw_escalated"]),
            "probe_status": record.get("probe_status"),
            "probe_score": record.get("probe_score"),
            "probe_raw_target_exists": record.get("probe_raw_target_exists"),
            "probe_target_noise": record.get("probe_target_noise"),
            "probe_history_conflict": record.get("probe_history_conflict"),
        },
        "final_outcome": {
            "compact_answer": record.get("compact_answer"),
            "latent_compact_answer": record.get("latent_compact_answer"),
            "final_answer": record["answer"],
            "gold_answer": record["gold"],
            "correct": bool(record["correct"]),
        },
        "judge": {
            "label": judge_label(record),
            "first_failing_stage": first_failing_stage(record),
        },
        "coverage": {
            "pass_trace_available": bool(pass_traces),
            "provenance_link_count": unique_source_count(
                provenance,
                pass_provenance,
                query_lineage,
                note_provenance,
            ),
            "final_provenance_link_count": sum(len(link["matched_sources"]) for link in provenance),
            "pass_provenance_link_count": sum(len(link["matched_sources"]) for link in pass_provenance),
            "query_lineage_link_count": sum(len(link["matched_sources"]) for link in query_lineage),
            "note_provenance_link_count": sum(len(link["matched_sources"]) for link in note_provenance),
            "quarantine_count": sum(1 for decision in filter_decisions if decision["decision"] == "quarantine"),
        },
    }
