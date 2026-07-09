from __future__ import annotations

import os

from deepseek_memory_summarizer import DeepSeekMemorySummarizer
import run_actual_hallucination_identity_micro_split_round as micro_base
import run_actual_hallucination_literal_claim_pilot as claim_base
import run_actual_hallucination_literal_normalization_pilot as norm_base
import run_actual_hallucination_literal_subsplit_pilot as literal_base


PILOT_IDS = "halu_01,halu_12,halu_15,halu_16,halu_17,halu_18,halu_19,halu_20"
PILOT_SEEDS = "11"

RELATION_IDS = {"halu_01", "halu_12"}
CODE_IDS = literal_base.CODE_IDS
WEAK_NAME_IDS = literal_base.WEAK_NAME_IDS
STRONG_NAME_IDS = literal_base.STRONG_NAME_IDS
LITERAL_IDS = CODE_IDS | WEAK_NAME_IDS | STRONG_NAME_IDS
TRACE_IDS = {
    "halu_01": "mentor-to-manager surrogate",
    "halu_12": "manager-to-emergency-contact surrogate",
    "halu_15": "code-overlap badge clue",
    "halu_16": "code-overlap archive-pin clue",
    "halu_19": "strengthened name-overlap sponsor clue",
    "halu_20": "strengthened name-overlap approver clue",
}
ORIGINAL_MICRO_PROMPT = micro_base.intervention_prompt
ORIGINAL_MICRO_CACHE_KEY = micro_base.cache_key


def is_relation_item(item: dict[str, object]) -> bool:
    return item["id"] in RELATION_IDS


def backed_intervention(intervention: str) -> str:
    if intervention in {"normalized_literal_identity_anchor", "claim_normalized_literal_identity_anchor"}:
        return "literal_identity_anchor"
    return intervention


def intervention_prompt(
    item: dict[str, object],
    pass_idx: int,
    seed: int,
    previous_note: str | None,
    previous_claims: list[micro_base.actual_base.CompactClaim] | None,
    intervention: str,
) -> str:
    base_intervention = backed_intervention(intervention)
    if is_relation_item(item):
        return ORIGINAL_MICRO_PROMPT(item, pass_idx, seed, previous_note, previous_claims, base_intervention)
    return literal_base.intervention_prompt(item, pass_idx, seed, previous_note, previous_claims, base_intervention)


def cache_key(intervention: str, item_id: str, seed: int, pass_idx: int) -> str:
    base_intervention = backed_intervention(intervention)
    if item_id in RELATION_IDS:
        return ORIGINAL_MICRO_CACHE_KEY(base_intervention, item_id, seed, pass_idx)
    return literal_base.cache_key(base_intervention, item_id, seed, pass_idx)


def claim_sensitive_state(
    item: dict[str, object],
    current_note: str,
    normalized_claims: list[micro_base.actual_base.CompactClaim],
    intervention: str,
) -> tuple[str, list[micro_base.actual_base.CompactClaim]]:
    if is_relation_item(item):
        return current_note, normalized_claims
    return claim_base.claim_sensitive_literal_state(item, current_note, normalized_claims, intervention)


def consolidate_model_backed(
    item: dict[str, object],
    n_passes: int,
    seed: int,
    intervention: str,
    summarizer: DeepSeekMemorySummarizer,
) -> tuple[list[micro_base.actual_base.CompactClaim], list[str], dict[str, float]]:
    previous_note: str | None = None
    previous_claims: list[micro_base.actual_base.CompactClaim] | None = None
    note_history: list[str] = []
    claims: list[micro_base.actual_base.CompactClaim] = []
    total_cost = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    carry_forward_events = 0

    for pass_idx in range(1, n_passes + 1):
        prompt = intervention_prompt(item, pass_idx, seed, previous_note, previous_claims, intervention)
        result = summarizer.summarize(
            cache_key=cache_key(intervention, item["id"], seed, pass_idx),
            prompt=prompt,
            schema=micro_base.actual_base.schema_for_item(item),
        )
        structured = micro_base.persistence_base.coerce_structured_output(result)
        structured_raw = structured if structured else None
        current_note = structured.get("note", "").strip()
        raw_claims = structured.get("claims", [])
        normalized_claims = []
        for raw_claim in raw_claims:
            claim = micro_base.persistence_base.normalize_claim(item, raw_claim, current_note)
            if claim is not None:
                normalized_claims.append(claim)
        note_claim = micro_base.persistence_base.scaffold_query_claim(item, current_note)
        if note_claim is not None and not any(claim.field == item["query_field"] for claim in normalized_claims):
            normalized_claims.append(note_claim)

        current_note, normalized_claims = claim_sensitive_state(item, current_note, normalized_claims, intervention)

        if micro_base.persistence_base.should_carry_forward(item, structured_raw, normalized_claims, previous_claims, previous_note):
            carry_forward_events += 1
            current_note = previous_note or ""
            normalized_claims = list(previous_claims or [])

        current_note, normalized_claims = claim_sensitive_state(item, current_note, normalized_claims, intervention)

        previous_note = current_note
        previous_claims = normalized_claims
        claims = normalized_claims
        note_history.append(current_note)
        total_cost += float(result.get("total_cost_usd", 0.0) or 0.0)
        usage = result.get("usage", {})
        total_input_tokens += int(usage.get("input_tokens", 0) or 0)
        total_output_tokens += int(usage.get("output_tokens", 0) or 0)

    return claims, note_history, {
        "llm_cost_usd": round(total_cost, 6),
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "carry_forward_events": carry_forward_events,
    }


def _subset_counts(records: list[dict[str, object]], intervention: str, architecture: str, n_passes: int, item_ids: set[str]) -> str:
    subset = [
        record
        for record in records
        if record["intervention"] == intervention
        and record["architecture"] == architecture
        and record["n_passes"] == n_passes
        and record["item_id"] in item_ids
    ]
    tentative = sum(1 for record in subset if record["tentative_target_claim"])
    raw = sum(1 for record in subset if record["raw_escalated"])
    signal = sum(1 for record in subset if record["tentative_target_claim"] or record["raw_escalated"])
    scaffold = sum(1 for record in subset if norm_base.note_has_scaffold(record["final_note"]))
    return f"signal={signal}/{len(subset)}, tent={tentative}/{len(subset)}, raw={raw}/{len(subset)}, scaffold={scaffold}/{len(subset)}"


def build_summary(results: dict[str, object]) -> str:
    lines = [
        "# Actual Hallucination Identity Claim Bridge Pilot Summary",
        "",
        "这一轮把 claim-sensitive broad literal branch 往外扩一层，重新接回 relation item：固定 8 条 relation+code+weak-name+strong-name slice，不强行发明一套全新 prompt，而是复用已经稳定的 relation-frontier 与 literal-frontier cache，检查 broad literal 的 claim surfacing 在更宽 identity/literal 前沿里是否仍然非回退。",
        "",
        f"- slice items: {results['num_items']}",
        f"- seeds: {results['seeds']}",
        f"- interventions: {', '.join(results['interventions'])}",
        f"- architectures: {', '.join(results['architectures'])}",
        f"- N: {results['n_values']}",
        "",
    ]
    for intervention in micro_base.INTERVENTIONS:
        lines.append(f"## {intervention}")
        lines.append("")
        for architecture in micro_base.ARCHITECTURES:
            lines.append(f"### {architecture}")
            lines.append("")
            lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
            for n in micro_base.N_VALUES:
                row = results["aggregate"][intervention][architecture][str(n)]
                metrics = results["hallucination_metrics"][intervention][architecture][str(n)]
                lines.append(
                    f"| {n} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                    f"{row['raw_escalation_rate']:.3f} | {metrics['direct_unsupported_answer_rate']:.3f} | {metrics['false_present_rate']:.3f} | "
                    f"{metrics['tentative_guess_note_rate']:.3f} | {metrics['tentative_target_claim_rate']:.3f} | "
                    f"{metrics['carry_forward_record_rate']:.3f} | {metrics['mean_llm_cost_usd']:.4f} |"
                )
            lines.append("")

    records = results["records"]
    lines.extend(
        [
            "## Identity Claim Bridge Readout",
            "",
            f"- Unified N=8 false_present: typed/literal/normalized/claim = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['normalized_literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['claim_normalized_literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}`.",
            f"- Note-aware N=8 false_present: typed/literal/normalized/claim = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['claim_normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}`.",
            f"- Broad literal unified N=8 on relation items: literal `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, RELATION_IDS)}`, claim `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, RELATION_IDS)}`.",
            f"- Broad literal unified N=8 on code items: literal `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, CODE_IDS)}`, claim `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, CODE_IDS)}`.",
            f"- Broad literal unified N=8 on weak-name items: literal `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, WEAK_NAME_IDS)}`, claim `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, WEAK_NAME_IDS)}`.",
            f"- Broad literal unified N=8 on strengthened-name items: literal `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`, normalized `{_subset_counts(records, 'normalized_literal_identity_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`, claim `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`.",
            f"- Summary-only N=8 realism: literal/normalized/claim = `{results['aggregate']['literal_identity_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['normalized_literal_identity_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['claim_normalized_literal_identity_anchor']['summary_only']['8']['accuracy']:.3f}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(results: dict[str, object]) -> str:
    seed = results["seeds"][0]
    records = results["records"]
    lines = [
        "# Actual Hallucination Identity Claim Bridge Traces",
        "",
        f"这些 trace 固定展示 seed `{seed}`，用来比较 {', '.join(results['interventions'])} 在 relation+literal bridge slice 上的 broad-literal claim surfacing。",
        "",
    ]
    for item_id, label in TRACE_IDS.items():
        item_records = [record for record in records if record["item_id"] == item_id and record["seed"] == seed]
        if not item_records:
            continue
        lines.append(f"## {item_id}: {label}")
        lines.append("")
        for intervention in micro_base.INTERVENTIONS:
            lines.append(f"### {intervention}")
            lines.append("")
            for architecture in micro_base.ARCHITECTURES:
                lines.append(f"#### {architecture}")
                lines.append("")
                for n in micro_base.N_VALUES:
                    matches = [
                        record
                        for record in item_records
                        if record["intervention"] == intervention
                        and record["architecture"] == architecture
                        and record["n_passes"] == n
                    ]
                    if not matches:
                        continue
                    record = matches[0]
                    probe = "-" if record["probe_status"] is None else f"{record['probe_status']} / {record['probe_score']:.3f}"
                    lines.append(
                        f"- N={n}: probe={probe}; compact={record['compact_answer']}; final={record['answer']}; "
                        f"route={record['route']}; tent={int(record['tentative_target_claim'])}; raw={int(record['raw_escalated'])}; "
                        f"carry={record['carry_forward_events']}; llm_cost=${record['llm_cost_usd']:.4f}"
                    )
                    lines.append(f"  note: {record['final_note']}")
                lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    os.environ.setdefault("ACTUAL_HALLU_IDENTITY_MICRO_IDS", PILOT_IDS)
    os.environ.setdefault("ACTUAL_HALLU_IDENTITY_MICRO_SEEDS", PILOT_SEEDS)
    micro_base.DEFAULT_SLICE_IDS = PILOT_IDS.split(",")
    micro_base.INTERVENTIONS = [
        "typed_selective_anchor",
        "literal_identity_anchor",
        "normalized_literal_identity_anchor",
        "claim_normalized_literal_identity_anchor",
    ]
    micro_base.JSON_PATH = "outputs/actual_hallucination_identity_claim_bridge_pilot_results.json"
    micro_base.SUMMARY_PATH = "outputs/actual_hallucination_identity_claim_bridge_pilot_summary.md"
    micro_base.TRACE_PATH = "outputs/actual_hallucination_identity_claim_bridge_pilot_traces.md"
    micro_base.TRACE_IDS = TRACE_IDS
    micro_base.intervention_prompt = intervention_prompt
    micro_base.cache_key = cache_key
    micro_base.consolidate_model_backed = consolidate_model_backed
    micro_base.build_summary = build_summary
    micro_base.build_traces = build_traces
    micro_base.main()


if __name__ == "__main__":
    main()
