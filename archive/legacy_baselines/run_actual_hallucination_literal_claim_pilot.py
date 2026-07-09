from __future__ import annotations

import os

from deepseek_memory_summarizer import DeepSeekMemorySummarizer
import run_actual_hallucination_identity_micro_split_round as micro_base
import run_actual_hallucination_literal_normalization_pilot as norm_base
import run_actual_hallucination_literal_subsplit_pilot as literal_base


PILOT_IDS = literal_base.PILOT_IDS
PILOT_SEEDS = literal_base.PILOT_SEEDS

CODE_IDS = literal_base.CODE_IDS
WEAK_NAME_IDS = literal_base.WEAK_NAME_IDS
STRONG_NAME_IDS = literal_base.STRONG_NAME_IDS
NAME_IDS = literal_base.NAME_IDS
TRACE_IDS = literal_base.TRACE_IDS


def intervention_prompt(
    item: dict[str, object],
    pass_idx: int,
    seed: int,
    previous_note: str | None,
    previous_claims: list[micro_base.actual_base.CompactClaim] | None,
    intervention: str,
) -> str:
    if intervention in {"normalized_literal_identity_anchor", "claim_normalized_literal_identity_anchor"}:
        return literal_base.intervention_prompt(
            item,
            pass_idx,
            seed,
            previous_note,
            previous_claims,
            "literal_identity_anchor",
        )
    return literal_base.intervention_prompt(item, pass_idx, seed, previous_note, previous_claims, intervention)


def cache_key(intervention: str, item_id: str, seed: int, pass_idx: int) -> str:
    if intervention in {"normalized_literal_identity_anchor", "claim_normalized_literal_identity_anchor"}:
        return literal_base.cache_key("literal_identity_anchor", item_id, seed, pass_idx)
    return literal_base.cache_key(intervention, item_id, seed, pass_idx)


def claim_sensitive_literal_state(
    item: dict[str, object],
    current_note: str,
    normalized_claims: list[micro_base.actual_base.CompactClaim],
    intervention: str,
) -> tuple[str, list[micro_base.actual_base.CompactClaim]]:
    if intervention not in {"normalized_literal_identity_anchor", "claim_normalized_literal_identity_anchor"}:
        return current_note, normalized_claims

    current_note = norm_base.normalize_aligned_note(item, current_note, normalized_claims)
    if intervention != "claim_normalized_literal_identity_anchor":
        return current_note, normalized_claims

    support_value = norm_base.aligned_support_value(item)
    if support_value is None:
        return current_note, normalized_claims
    note_claim = micro_base.persistence_base.scaffold_query_claim(item, current_note)
    if note_claim is None or note_claim.value != support_value:
        return current_note, normalized_claims

    rewritten_claims = [claim for claim in normalized_claims if claim.field != item["query_field"]]
    rewritten_claims.append(note_claim)
    return current_note, rewritten_claims


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

        current_note, normalized_claims = claim_sensitive_literal_state(item, current_note, normalized_claims, intervention)

        if micro_base.persistence_base.should_carry_forward(item, structured_raw, normalized_claims, previous_claims, previous_note):
            carry_forward_events += 1
            current_note = previous_note or ""
            normalized_claims = list(previous_claims or [])

        current_note, normalized_claims = claim_sensitive_literal_state(item, current_note, normalized_claims, intervention)

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
        "# Actual Hallucination Literal Claim Pilot Summary",
        "",
        "这一轮不再继续做 note-only cleanup，而是对 broad literal branch 加一个 claim-sensitive executor follow-up：在 aligned-name role 对齐的情况下，把已经 canonical 的 broad literal scaffold 显式转成 tentative query claim，同时保持 mixed code+name literal slice 的 aggregate false-present 不回退。",
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
            "## Literal Claim Readout",
            "",
            f"- Unified N=8 false_present: literal/normalized/claim = `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['normalized_literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['claim_normalized_literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}`.",
            f"- Note-aware N=8 false_present: literal/normalized/claim = `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['claim_normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}`.",
            f"- Broad literal unified N=8 before note rewrite: strengthened-name `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`.",
            f"- Broad literal unified N=8 after note rewrite: strengthened-name `{_subset_counts(records, 'normalized_literal_identity_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`.",
            f"- Broad literal unified N=8 after claim-sensitive rewrite: strengthened-name `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, STRONG_NAME_IDS)}`.",
            f"- Broad literal note-aware N=8 after claim-sensitive rewrite: strengthened-name `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_note_aware', 8, STRONG_NAME_IDS)}`.",
            f"- Broad literal code/weak-name non-regression at unified N=8: code `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, CODE_IDS)}`, weak-name `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, WEAK_NAME_IDS)}`.",
            f"- Summary-only N=8 realism: normalized/claim = `{results['aggregate']['normalized_literal_identity_anchor']['summary_only']['8']['accuracy']:.3f}` / `{results['aggregate']['claim_normalized_literal_identity_anchor']['summary_only']['8']['accuracy']:.3f}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(results: dict[str, object]) -> str:
    seed = results["seeds"][0]
    records = results["records"]
    lines = [
        "# Actual Hallucination Literal Claim Traces",
        "",
        f"这些 trace 固定展示 seed `{seed}`，用来比较 {', '.join(results['interventions'])} 在 mixed literal slice 上的 claim surfacing 行为。",
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
        "code_literal_anchor",
        "name_literal_anchor",
    ]
    micro_base.JSON_PATH = "outputs/actual_hallucination_literal_claim_pilot_results.json"
    micro_base.SUMMARY_PATH = "outputs/actual_hallucination_literal_claim_pilot_summary.md"
    micro_base.TRACE_PATH = "outputs/actual_hallucination_literal_claim_pilot_traces.md"
    micro_base.TRACE_IDS = TRACE_IDS
    micro_base.identity_micro_mode = literal_base.literal_subsplit_mode
    micro_base.anchor_mode = literal_base.anchor_mode
    micro_base.selective_anchor_block = literal_base.selective_anchor_block
    micro_base.intervention_prompt = intervention_prompt
    micro_base.cache_key = cache_key
    micro_base.consolidate_model_backed = consolidate_model_backed
    micro_base.build_summary = build_summary
    micro_base.build_traces = build_traces
    micro_base.main()


if __name__ == "__main__":
    main()
