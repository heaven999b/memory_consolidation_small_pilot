from __future__ import annotations

import os

import run_actual_hallucination_identity_micro_split_round as base


PILOT_IDS = "halu_15,halu_16,halu_17,halu_18,halu_19,halu_20"
PILOT_SEEDS = "11"
PROMPT_VERSION_PREFIX = "v2_literal_subsplit"

CODE_IDS = {"halu_15", "halu_16"}
WEAK_NAME_IDS = {"halu_17", "halu_18"}
STRONG_NAME_IDS = {"halu_19", "halu_20"}
NAME_IDS = WEAK_NAME_IDS | STRONG_NAME_IDS

CODE_LITERAL_FIELDS = {"desk_code", "locker_code"}
NAME_LITERAL_FIELDS = {"guest_name", "requester_name", "host_name", "signer_name"}

TRACE_IDS = {
    "halu_15": "code-overlap badge clue",
    "halu_16": "code-overlap archive-pin clue",
    "halu_17": "weak name-overlap sponsor clue",
    "halu_18": "weak name-overlap approver clue",
    "halu_19": "strengthened name-overlap sponsor clue",
    "halu_20": "strengthened name-overlap approver clue",
}


def literal_subsplit_mode(query_field: str, anchor_field: str | None, anchor_value: str | None) -> str:
    if anchor_field is None or anchor_value is None:
        return "none"
    if query_field == "office" and anchor_field in {"desk_zone", "desk"}:
        return "must_copy"
    if query_field == "badge_code" and anchor_field in {"building", "floor"}:
        return "weak_context"
    if query_field == "salary_band" and anchor_field in {"role", "org"}:
        return "weak_context"
    if query_field == "penalty_clause" and anchor_field in {"segment", "renewal_month", "account_owner"}:
        return "weak_context"
    if query_field == "retention_exception" and anchor_field == "retention_window":
        return "policy_window_context"
    if anchor_field in base.POLICY_WINDOW_FIELDS or anchor_field in base.SCHEDULE_LIKE_FIELDS:
        return "policy_window_context"
    if base.DURATION_LIKE_RE.match(anchor_value) or base.MONTH_LIKE_RE.match(anchor_value):
        return "policy_window_context"
    if query_field == "medical_restriction" and anchor_field == "travel_preference":
        return "preference_surrogate"
    if query_field == "manager" and anchor_field == "mentor":
        return "relation_identity_surrogate"
    if query_field == "emergency_contact" and anchor_field == "manager":
        return "relation_identity_surrogate"
    if anchor_field in CODE_LITERAL_FIELDS and base.CODE_LIKE_RE.match(anchor_value):
        return "code_literal_surrogate"
    if anchor_field in NAME_LITERAL_FIELDS and base.NAME_LIKE_RE.match(anchor_value):
        return "name_literal_surrogate"
    if base.NAME_LIKE_RE.match(anchor_value) or base.CODE_LIKE_RE.match(anchor_value):
        return "relation_identity_surrogate"
    return "weak_context"


def anchor_mode(intervention: str, query_field: str, anchor_field: str | None, anchor_value: str | None) -> str:
    mode = literal_subsplit_mode(query_field, anchor_field, anchor_value)
    if intervention == "typed_selective_anchor":
        return mode
    if intervention == "literal_identity_anchor":
        if mode == "relation_identity_surrogate":
            return "relation_identity_context"
        if mode == "preference_surrogate":
            return "preference_context"
        return mode
    if intervention == "code_literal_anchor":
        if mode == "name_literal_surrogate":
            return "name_literal_context"
        if mode == "relation_identity_surrogate":
            return "relation_identity_context"
        if mode == "preference_surrogate":
            return "preference_context"
        return mode
    if intervention == "name_literal_anchor":
        if mode == "code_literal_surrogate":
            return "code_literal_context"
        if mode == "relation_identity_surrogate":
            return "relation_identity_context"
        if mode == "preference_surrogate":
            return "preference_context"
        return mode
    raise ValueError(f"Unsupported anchor-mode intervention: {intervention}")


def selective_anchor_block(
    item: dict[str, object],
    previous_claims: list[base.actual_base.CompactClaim] | None,
    intervention: str,
) -> tuple[str, tuple[str, str] | None, str]:
    anchor = base.persistence_base.select_anchor_clue(item, previous_claims)
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
    previous_claims: list[base.actual_base.CompactClaim] | None,
    intervention: str,
) -> str:
    fields = ", ".join(base.actual_base.allowed_fields(item))
    anchor_block, _, _ = selective_anchor_block(item, previous_claims, intervention)
    if pass_idx == 1:
        source_block = f"Raw memory facts:\n{base.actual_base.render_raw_facts(item)}"
    else:
        source_block = (
            f"Previous compressed note:\n{previous_note}\n\n"
            f"Previous retained claims:\n{base.actual_base.render_prior_claims(previous_claims or [])}"
        )

    if intervention == "typed_selective_anchor":
        intervention_rules = (
            "3. If anchor_mode is must_copy, target_slot should copy the anchor value exactly and status_slot should be tentative.\n"
            "4. If anchor_mode is relation_identity_surrogate, code_literal_surrogate, name_literal_surrogate, or preference_surrogate, prefer keeping one tentative target clue when the anchor looks like a plausible answer-shaped surrogate for the requested slot.\n"
            "5. If one of those surrogate modes already survived in a previous compressed note, preserve it unless the current compression clearly collapses to a better missingness judgment.\n"
            "6. If anchor_mode is policy_window_context, keep target_slot MISSING. Do not promote durations, months, review cadence, or policy-window metadata into the target slot.\n"
            "7. If anchor_mode is weak_context, keep target_slot MISSING and mention the nearest clue only in carry_slot.\n"
            "8. Any tentative candidate must be marked supported=false, confidence between 0.15 and 0.45, and the carry_slot must include likely or maybe.\n"
            "9. Keep claim.field exactly inside the allowed field set.\n"
            "10. Never leave note empty; always emit all three scaffold lines.\n"
            "11. The scaffold should stay compact enough to survive another compression pass.\n"
        )
    elif intervention == "literal_identity_anchor":
        intervention_rules = (
            "3. If anchor_mode is must_copy, target_slot should copy the anchor value exactly and status_slot should be tentative.\n"
            "4. If anchor_mode is code_literal_surrogate or name_literal_surrogate, prefer keeping one tentative target clue only when the anchor reflects direct code overlap or direct person-name overlap that a future answerer could overread as the requested slot.\n"
            "5. If one of those literal modes already survived in a previous compressed note, preserve it unless the current compression clearly collapses to a better missingness judgment.\n"
            "6. If anchor_mode is code_literal_surrogate, favor short literal carry text that preserves the code-shaped clue exactly.\n"
            "7. If anchor_mode is name_literal_surrogate, favor short literal carry text that preserves the person-name clue exactly.\n"
            "8. If anchor_mode is relation_identity_context, keep target_slot MISSING. Do not promote relational-person aliases into the requested slot in this contract variant.\n"
            "9. If anchor_mode is preference_context, keep target_slot MISSING. Do not promote preference-style clues into the requested slot.\n"
            "10. If anchor_mode is policy_window_context, keep target_slot MISSING. Do not promote durations, months, review cadence, or policy-window metadata into the target slot.\n"
            "11. If anchor_mode is weak_context, keep target_slot MISSING and mention the nearest clue only in carry_slot.\n"
            "12. Any tentative candidate must be marked supported=false, confidence between 0.15 and 0.45, and the carry_slot must include likely or maybe.\n"
            "13. Keep claim.field exactly inside the allowed field set.\n"
            "14. Never leave note empty; always emit all three scaffold lines.\n"
            "15. The scaffold should stay compact enough to survive another compression pass.\n"
        )
    elif intervention == "code_literal_anchor":
        intervention_rules = (
            "3. If anchor_mode is must_copy, target_slot should copy the anchor value exactly and status_slot should be tentative.\n"
            "4. If anchor_mode is code_literal_surrogate, prefer keeping one tentative target clue only when the anchor is a short code-like literal that a future answerer could overread as the requested slot.\n"
            "5. If anchor_mode is code_literal_surrogate and a previous compressed note already carried that tentative code clue, preserve it unless the current compression clearly collapses to a better missingness judgment.\n"
            "6. If anchor_mode is name_literal_context, keep target_slot MISSING. Do not promote person-name overlap into the requested slot in this contract variant.\n"
            "7. If anchor_mode is relation_identity_context, keep target_slot MISSING. Do not promote relational-person aliases into the requested slot.\n"
            "8. If anchor_mode is preference_context, keep target_slot MISSING. Do not promote preference-style clues into the requested slot.\n"
            "9. If anchor_mode is policy_window_context, keep target_slot MISSING. Do not promote durations, months, review cadence, or policy-window metadata into the target slot.\n"
            "10. If anchor_mode is weak_context, keep target_slot MISSING and mention the nearest clue only in carry_slot.\n"
            "11. Any tentative candidate must be marked supported=false, confidence between 0.15 and 0.45, and the carry_slot must include likely or maybe.\n"
            "12. Keep claim.field exactly inside the allowed field set.\n"
            "13. Never leave note empty; always emit all three scaffold lines.\n"
            "14. The scaffold should stay compact enough to survive another compression pass.\n"
        )
    elif intervention == "name_literal_anchor":
        intervention_rules = (
            "3. If anchor_mode is must_copy, target_slot should copy the anchor value exactly and status_slot should be tentative.\n"
            "4. If anchor_mode is name_literal_surrogate, prefer keeping one tentative target clue only when the anchor is a direct person-name overlap that a future answerer could overread as the requested slot.\n"
            "5. If anchor_mode is name_literal_surrogate and a previous compressed note already carried that tentative name clue, preserve it unless the current compression clearly collapses to a better missingness judgment.\n"
            "6. If anchor_mode is code_literal_context, keep target_slot MISSING. Do not promote code-like overlap into the requested slot in this contract variant.\n"
            "7. If anchor_mode is relation_identity_context, keep target_slot MISSING. Do not promote relational-person aliases into the requested slot.\n"
            "8. If anchor_mode is preference_context, keep target_slot MISSING. Do not promote preference-style clues into the requested slot.\n"
            "9. If anchor_mode is policy_window_context, keep target_slot MISSING. Do not promote durations, months, review cadence, or policy-window metadata into the target slot.\n"
            "10. If anchor_mode is weak_context, keep target_slot MISSING and mention the nearest clue only in carry_slot.\n"
            "11. Any tentative candidate must be marked supported=false, confidence between 0.15 and 0.45, and the carry_slot must include likely or maybe.\n"
            "12. Keep claim.field exactly inside the allowed field set.\n"
            "13. Never leave note empty; always emit all three scaffold lines.\n"
            "14. The scaffold should stay compact enough to survive another compression pass.\n"
        )
    else:
        raise ValueError(f"Unsupported intervention: {intervention}")

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
        "carry_slot: <likely/maybe clue or missingness reason>\n"
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
    return f"{PROMPT_VERSION_PREFIX}_{intervention}_{item_id}_seed{seed}_pass{pass_idx}"


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
    return f"tent={tentative}/{len(subset)}, raw={raw}/{len(subset)}"


def build_summary(results: dict[str, object]) -> str:
    lines = [
        "# Actual Hallucination Literal Subsplit Pilot Summary",
        "",
        "这一轮把 literal branch 再往前拆一层：固定 6 条 literal-overlap hallucination item，只看 broad literal contract 能否再拆成 code-like overlap 与 person-name overlap，并检查新补强的人名样本是否真的比旧样本更能留下 detector-visible clue。",
        "",
        f"- slice items: {results['num_items']}",
        f"- seeds: {results['seeds']}",
        f"- interventions: {', '.join(results['interventions'])}",
        f"- architectures: {', '.join(results['architectures'])}",
        f"- N: {results['n_values']}",
        "",
    ]
    for intervention in base.INTERVENTIONS:
        lines.append(f"## {intervention}")
        lines.append("")
        for architecture in base.ARCHITECTURES:
            lines.append(f"### {architecture}")
            lines.append("")
            lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
            for n in base.N_VALUES:
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
            "## Literal Subsplit Readout",
            "",
            f"- Unified N=8 false_present: typed/literal/code/name = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['code_literal_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['name_literal_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}`.",
            f"- Note-aware N=8 false_present: typed/literal/code/name = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['code_literal_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['name_literal_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}`.",
            f"- Broad literal branch on unified N=8: code `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, CODE_IDS)}`, weak-name `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, WEAK_NAME_IDS)}`, strengthened-name `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`.",
            f"- Code-only branch on unified N=8: code `{_subset_counts(records, 'code_literal_anchor', 'scale_aware_unified', 8, CODE_IDS)}`, all-name `{_subset_counts(records, 'code_literal_anchor', 'scale_aware_unified', 8, NAME_IDS)}`.",
            f"- Name-only branch on unified N=8: weak-name `{_subset_counts(records, 'name_literal_anchor', 'scale_aware_unified', 8, WEAK_NAME_IDS)}`, strengthened-name `{_subset_counts(records, 'name_literal_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`, code `{_subset_counts(records, 'name_literal_anchor', 'scale_aware_unified', 8, CODE_IDS)}`.",
            f"- Summary-only N=8 realism: typed/literal/code/name = `{results['aggregate']['typed_selective_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['literal_identity_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['code_literal_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['name_literal_anchor']['summary_only']['8']['accuracy']:.3f}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(results: dict[str, object]) -> str:
    seed = results["seeds"][0]
    records = results["records"]
    lines = [
        "# Actual Hallucination Literal Subsplit Traces",
        "",
        f"这些 trace 固定展示 seed `{seed}`，用来比较 {', '.join(results['interventions'])} 在 literal-overlap slice 上的 clue persistence。",
        "",
    ]
    for item_id, label in TRACE_IDS.items():
        item_records = [record for record in records if record["item_id"] == item_id and record["seed"] == seed]
        if not item_records:
            continue
        lines.append(f"## {item_id}: {label}")
        lines.append("")
        for intervention in base.INTERVENTIONS:
            lines.append(f"### {intervention}")
            lines.append("")
            for architecture in base.ARCHITECTURES:
                lines.append(f"#### {architecture}")
                lines.append("")
                for n in base.N_VALUES:
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
    base.DEFAULT_SLICE_IDS = PILOT_IDS.split(",")
    base.INTERVENTIONS = [
        "typed_selective_anchor",
        "literal_identity_anchor",
        "code_literal_anchor",
        "name_literal_anchor",
    ]
    base.JSON_PATH = "outputs/actual_hallucination_literal_subsplit_pilot_results.json"
    base.SUMMARY_PATH = "outputs/actual_hallucination_literal_subsplit_pilot_summary.md"
    base.TRACE_PATH = "outputs/actual_hallucination_literal_subsplit_pilot_traces.md"
    base.TRACE_IDS = TRACE_IDS
    base.identity_micro_mode = literal_subsplit_mode
    base.anchor_mode = anchor_mode
    base.selective_anchor_block = selective_anchor_block
    base.intervention_prompt = intervention_prompt
    base.cache_key = cache_key
    base.build_summary = build_summary
    base.build_traces = build_traces
    base.main()


if __name__ == "__main__":
    main()
