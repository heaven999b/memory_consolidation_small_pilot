from __future__ import annotations

import os

import run_actual_hallucination_identity_micro_split_round as micro_base
import run_actual_hallucination_literal_subsplit_pilot as literal_base


PILOT_IDS = literal_base.PILOT_IDS
PILOT_SEEDS = literal_base.PILOT_SEEDS
PROMPT_VERSION_PREFIX = "v3_name_refinement"

CODE_IDS = literal_base.CODE_IDS
WEAK_NAME_IDS = literal_base.WEAK_NAME_IDS
STRONG_NAME_IDS = literal_base.STRONG_NAME_IDS
NAME_IDS = literal_base.NAME_IDS
TRACE_IDS = literal_base.TRACE_IDS

ALIGNED_NAME_PAIRS = {
    ("sponsoring_employee", "host_name"),
    ("approver_name", "signer_name"),
}
ANTI_ROLE_NAME_PAIRS = {
    ("sponsoring_employee", "guest_name"),
    ("sponsoring_employee", "visitor_name"),
    ("approver_name", "requester_name"),
}


def name_refinement_mode(query_field: str, anchor_field: str | None, anchor_value: str | None) -> str:
    base_mode = literal_base.literal_subsplit_mode(query_field, anchor_field, anchor_value)
    if base_mode != "name_literal_surrogate" or anchor_field is None:
        return base_mode
    pair = (query_field, anchor_field)
    if pair in ALIGNED_NAME_PAIRS:
        return "aligned_name_literal_surrogate"
    if pair in ANTI_ROLE_NAME_PAIRS:
        return "anti_role_name_context"
    return "generic_name_literal_context"


def anchor_mode(intervention: str, query_field: str, anchor_field: str | None, anchor_value: str | None) -> str:
    if intervention != "refined_name_literal_anchor":
        return literal_base.anchor_mode(intervention, query_field, anchor_field, anchor_value)
    mode = name_refinement_mode(query_field, anchor_field, anchor_value)
    if mode == "code_literal_surrogate":
        return "code_literal_context"
    if mode == "relation_identity_surrogate":
        return "relation_identity_context"
    if mode == "preference_surrogate":
        return "preference_context"
    return mode


def selective_anchor_block(
    item: dict[str, object],
    previous_claims: list[micro_base.actual_base.CompactClaim] | None,
    intervention: str,
) -> tuple[str, tuple[str, str] | None, str]:
    anchor = micro_base.persistence_base.select_anchor_clue(item, previous_claims)
    if anchor is None:
        return "Anchor guide:\n- none\n", None, "none"
    mode = anchor_mode(intervention, item["query_field"], anchor[0], anchor[1])
    return (
        f"Anchor guide:\n- nearest clue {anchor[0]}:{anchor[1]}\n- anchor_mode: {mode}\n",
        anchor,
        mode,
    )


def intervention_prompt(
    item: dict[str, object],
    pass_idx: int,
    seed: int,
    previous_note: str | None,
    previous_claims: list[micro_base.actual_base.CompactClaim] | None,
    intervention: str,
) -> str:
    if intervention != "refined_name_literal_anchor":
        return literal_base.intervention_prompt(item, pass_idx, seed, previous_note, previous_claims, intervention)

    fields = ", ".join(micro_base.actual_base.allowed_fields(item))
    anchor_block, _, _ = selective_anchor_block(item, previous_claims, intervention)
    if pass_idx == 1:
        source_block = f"Raw memory facts:\n{micro_base.actual_base.render_raw_facts(item)}"
    else:
        source_block = (
            f"Previous compressed note:\n{previous_note}\n\n"
            f"Previous retained claims:\n{micro_base.actual_base.render_prior_claims(previous_claims or [])}"
        )

    intervention_rules = (
        "3. The note must always use these exact prefixes, in this exact order: `target_slot:`, `status_slot:`, `carry_slot:`. Do not shorten them, rename them, or replace them with prose.\n"
        "4. If anchor_mode is aligned_name_literal_surrogate, target_slot must copy the anchor value exactly and status_slot must be tentative.\n"
        "5. If anchor_mode is aligned_name_literal_surrogate and a previous compressed note already carried that same tentative target clue, preserve the same target_slot line unless the current compression clearly supports a stronger missingness judgment.\n"
        "6. If anchor_mode is aligned_name_literal_surrogate, the carry_slot must mention the role-alignment reason in compact form, such as host-may-sponsor or signer-may-approve.\n"
        "7. If anchor_mode is anti_role_name_context, target_slot must be MISSING and status_slot must be missing. Do not promote the anchor value into the requested slot. Explicitly describe the role mismatch in carry_slot.\n"
        "8. If anchor_mode is anti_role_name_context and a previous compressed note carried a tentative target clue derived from that mismatched name, delete that tentative clue rather than carrying it forward.\n"
        "9. If anchor_mode is generic_name_literal_context, code_literal_context, relation_identity_context, preference_context, policy_window_context, or weak_context, keep target_slot MISSING and mention the clue only as context in carry_slot.\n"
        "10. When target_slot is tentative, keep exactly one tentative claim for the query field with supported=false and confidence between 0.15 and 0.45.\n"
        "11. When target_slot is MISSING, do not invent a query-field claim; keep any retained claims on non-query fields only if they are directly supported by the source.\n"
        "12. The note must stay compact enough to survive another compression pass.\n"
        "13. Never leave the note empty, even if the source is unchanged.\n"
    )
    return (
        "You are aggressively compressing agent memory for a future answerer.\n"
        "Return one concise note plus a small set of retained claims.\n"
        "Rules:\n"
        "1. Use only the source material below.\n"
        "1a. Do not use outside knowledge about people, organizations, products, or benchmark families.\n"
        "1b. Do not mention searches, missing workspace files, or entities not explicitly present in the source block or prior compressed memory.\n"
        "2. Format the note as exactly three short lines:\n"
        f"target_slot: {item['query_field']} => <tentative candidate or MISSING>\n"
        "status_slot: <tentative|missing>\n"
        "carry_slot: <compact role clue or missingness reason>\n"
        f"{intervention_rules}"
        f"Compression pass: {pass_idx}\n"
        f"Compression seed tag: {seed}\n"
        f"Contract variant: {intervention}\n"
        f"Subject: {item['subject']}\n"
        f"User question: {item['query_text']}\n"
        f"Query field: {item['query_field']}\n"
        f"Allowed fields: {fields}\n\n"
        f"{anchor_block}\n"
        f"{source_block}\n"
    )


def cache_key(intervention: str, item_id: str, seed: int, pass_idx: int) -> str:
    if intervention == "refined_name_literal_anchor":
        return f"{PROMPT_VERSION_PREFIX}_{intervention}_{item_id}_seed{seed}_pass{pass_idx}"
    return literal_base.cache_key(intervention, item_id, seed, pass_idx)


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
    return f"signal={signal}/{len(subset)}, tent={tentative}/{len(subset)}, raw={raw}/{len(subset)}"


def build_summary(results: dict[str, object]) -> str:
    lines = [
        "# Actual Hallucination Name Refinement Pilot Summary",
        "",
        "这一轮不再继续扩数据，而是专门收紧 name-only scaffold：把 role-aligned 的人名重叠和 role-mismatched 的人名重叠显式分开，检查强化后的人名分支能否从 recoverable signal 更进一步走向 compact-stable clue。",
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
            "## Name Refinement Readout",
            "",
            f"- Unified N=8 false_present: typed/literal/name/refined = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['name_literal_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['refined_name_literal_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}`.",
            f"- Note-aware N=8 false_present: typed/literal/name/refined = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['name_literal_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['refined_name_literal_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}`.",
            f"- Baseline name branch on unified N=8: weak-name `{_subset_counts(records, 'name_literal_anchor', 'scale_aware_unified', 8, WEAK_NAME_IDS)}`, strengthened-name `{_subset_counts(records, 'name_literal_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`, code `{_subset_counts(records, 'name_literal_anchor', 'scale_aware_unified', 8, CODE_IDS)}`.",
            f"- Refined name branch on unified N=8: weak-name `{_subset_counts(records, 'refined_name_literal_anchor', 'scale_aware_unified', 8, WEAK_NAME_IDS)}`, strengthened-name `{_subset_counts(records, 'refined_name_literal_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`, code `{_subset_counts(records, 'refined_name_literal_anchor', 'scale_aware_unified', 8, CODE_IDS)}`.",
            f"- Summary-only N=8 realism: typed/literal/name/refined = `{results['aggregate']['typed_selective_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['literal_identity_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['name_literal_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['refined_name_literal_anchor']['summary_only']['8']['accuracy']:.3f}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(results: dict[str, object]) -> str:
    seed = results["seeds"][0]
    records = results["records"]
    lines = [
        "# Actual Hallucination Name Refinement Traces",
        "",
        f"这些 trace 固定展示 seed `{seed}`，用来比较 {', '.join(results['interventions'])} 在 name-overlap frontier 上的 clue persistence。",
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
                        f"route={record['route']}; raw={int(record['raw_escalated'])}; carry={record['carry_forward_events']}; llm_cost=${record['llm_cost_usd']:.4f}"
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
        "name_literal_anchor",
        "refined_name_literal_anchor",
    ]
    micro_base.JSON_PATH = "outputs/actual_hallucination_name_refinement_pilot_results.json"
    micro_base.SUMMARY_PATH = "outputs/actual_hallucination_name_refinement_pilot_summary.md"
    micro_base.TRACE_PATH = "outputs/actual_hallucination_name_refinement_pilot_traces.md"
    micro_base.TRACE_IDS = TRACE_IDS
    micro_base.identity_micro_mode = name_refinement_mode
    micro_base.anchor_mode = anchor_mode
    micro_base.selective_anchor_block = selective_anchor_block
    micro_base.intervention_prompt = intervention_prompt
    micro_base.cache_key = cache_key
    micro_base.build_summary = build_summary
    micro_base.build_traces = build_traces
    micro_base.main()


if __name__ == "__main__":
    main()
