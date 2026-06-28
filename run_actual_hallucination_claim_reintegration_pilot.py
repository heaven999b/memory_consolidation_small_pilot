from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import run_actual_hallucination_identity_micro_split_round as micro_base
import run_actual_hallucination_literal_normalization_pilot as norm_base
import run_actual_hallucination_literal_subsplit_pilot as literal_base
import run_actual_hallucination_robustness_round as robustness_base


PILOT_IDS = [
    "halu_01",
    "halu_02",
    "halu_03",
    "halu_04",
    "halu_05",
    "halu_08",
    "halu_12",
    "halu_14",
    "halu_15",
    "halu_16",
    "halu_17",
    "halu_18",
    "halu_19",
    "halu_20",
]
PILOT_SEEDS = [11]
ARCHITECTURES = ["summary_only", "scale_aware_unified", "scale_aware_note_aware"]
INTERVENTIONS = [
    "typed_selective_anchor",
    "literal_identity_anchor",
    "normalized_literal_identity_anchor",
    "claim_normalized_literal_identity_anchor",
]
N_VALUES = [4, 8]

RELATION_IDS = {"halu_01", "halu_12"}
STRESS_CONTEXT_IDS = {"halu_02", "halu_03", "halu_04", "halu_05", "halu_08", "halu_14"}
CODE_IDS = literal_base.CODE_IDS
WEAK_NAME_IDS = literal_base.WEAK_NAME_IDS
STRONG_NAME_IDS = literal_base.STRONG_NAME_IDS
LITERAL_IDS = CODE_IDS | WEAK_NAME_IDS | STRONG_NAME_IDS
PROXY_TYPED_EQ_IDS = {"halu_02", "halu_04", "halu_05", "halu_08", "halu_14"}
PROXY_IDENTITY_EQ_IDS = {"halu_03"}

TRACE_IDS = {
    "halu_01": "mentor-to-manager surrogate",
    "halu_03": "medical inference clue",
    "halu_05": "retention-exception frontier error",
    "halu_15": "code-overlap badge clue",
    "halu_19": "strengthened name-overlap sponsor clue",
    "halu_20": "strengthened name-overlap approver clue",
}

SURROGATE_SOURCE = "outputs/actual_hallucination_surrogate_split_results.json"
BRIDGE_SOURCE = "outputs/actual_hallucination_identity_claim_bridge_pilot_results.json"
LITERAL_SOURCE = "outputs/actual_hallucination_literal_claim_pilot_results.json"
EXACT_STRESS_SOURCE = "outputs/actual_hallucination_literal_identity_closure_results.json"
JSON_PATH = "outputs/actual_hallucination_claim_reintegration_pilot_results.json"
SUMMARY_PATH = "outputs/actual_hallucination_claim_reintegration_pilot_summary.md"
TRACE_PATH = "outputs/actual_hallucination_claim_reintegration_pilot_traces.md"

SOURCE_LABELS = {
    "surrogate": SURROGATE_SOURCE,
    "bridge": BRIDGE_SOURCE,
    "literal": LITERAL_SOURCE,
    "exact_closure": EXACT_STRESS_SOURCE,
}


def source_spec(intervention: str, item_id: str, exact_closure_available: bool) -> dict[str, str]:
    if intervention == "typed_selective_anchor":
        if item_id in LITERAL_IDS:
            return {
                "source_name": "literal",
                "source_intervention": "typed_selective_anchor",
                "proxy_status": "exact",
                "proxy_reason": "typed baseline on literal frontier is taken directly from the literal-claim pilot artifact",
            }
        return {
            "source_name": "surrogate",
            "source_intervention": "typed_selective_anchor",
            "proxy_status": "exact",
            "proxy_reason": "typed baseline on the non-literal stress slice is taken directly from the surrogate-split artifact",
        }

    if item_id in LITERAL_IDS:
        return {
            "source_name": "literal",
            "source_intervention": intervention,
            "proxy_status": "exact",
            "proxy_reason": "literal frontier rows are taken directly from the literal-claim pilot artifact",
        }

    if item_id in RELATION_IDS:
        return {
            "source_name": "bridge",
            "source_intervention": intervention,
            "proxy_status": "exact",
            "proxy_reason": "relation bridge rows are taken directly from the identity-claim bridge artifact",
        }

    if item_id in STRESS_CONTEXT_IDS and exact_closure_available:
        if intervention == "literal_identity_anchor":
            return {
                "source_name": "exact_closure",
                "source_intervention": "literal_identity_anchor",
                "proxy_status": "exact",
                "proxy_reason": "stress-context rows are taken directly from the exact literal-identity closure artifact",
            }
        return {
            "source_name": "exact_closure",
            "source_intervention": "literal_identity_anchor",
            "proxy_status": "contract_equivalent_exact",
            "proxy_reason": (
                "the normalized and claim-sensitive executor rewrites are inert on this non-literal stress subset, "
                "so the exact literal-identity closure rows are reused as contract-equivalent exact records"
            ),
        }

    if item_id in PROXY_TYPED_EQ_IDS:
        return {
            "source_name": "surrogate",
            "source_intervention": "typed_selective_anchor",
            "proxy_status": "mode_equivalent_proxy",
            "proxy_reason": (
                "on this item the literal-identity contract collapses to must_copy, weak_context, or policy_window_context, "
                "so the typed row is used as a mode-equivalent proxy without claiming a fresh model-backed literal run"
            ),
        }

    if item_id in PROXY_IDENTITY_EQ_IDS:
        return {
            "source_name": "surrogate",
            "source_intervention": "identity_selective_anchor",
            "proxy_status": "mode_equivalent_proxy",
            "proxy_reason": (
                "on this item literal-identity demotes the anchor to preference_context, so the identity-selective row is used "
                "as the closest mode-equivalent proxy"
            ),
        }

    raise RuntimeError(f"No source specification for intervention={intervention}, item_id={item_id}")


def load_payload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def index_records(records: list[dict[str, Any]]) -> dict[tuple[str, str, int, int, str], dict[str, Any]]:
    indexed: dict[tuple[str, str, int, int, str], dict[str, Any]] = {}
    for record in records:
        key = (
            record["intervention"],
            record["architecture"],
            int(record["n_passes"]),
            int(record["seed"]),
            record["item_id"],
        )
        indexed[key] = record
    return indexed


def build_records(
    surrogate_records: list[dict[str, Any]],
    bridge_records: list[dict[str, Any]],
    literal_records: list[dict[str, Any]],
    exact_closure_records: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    indices = {
        "surrogate": index_records(surrogate_records),
        "bridge": index_records(bridge_records),
        "literal": index_records(literal_records),
    }
    if exact_closure_records is not None:
        indices["exact_closure"] = index_records(exact_closure_records)
    stitched: list[dict[str, Any]] = []
    exact_closure_available = exact_closure_records is not None
    for intervention in INTERVENTIONS:
        for architecture in ARCHITECTURES:
            for n_passes in N_VALUES:
                for seed in PILOT_SEEDS:
                    for item_id in PILOT_IDS:
                        spec = source_spec(intervention, item_id, exact_closure_available)
                        key = (
                            spec["source_intervention"],
                            architecture,
                            n_passes,
                            seed,
                            item_id,
                        )
                        source_index = indices[spec["source_name"]]
                        if key not in source_index:
                            raise RuntimeError(f"Missing source record for {key} from {spec['source_name']}")
                        record = dict(source_index[key])
                        record["intervention"] = intervention
                        record["source_artifact"] = SOURCE_LABELS[spec["source_name"]]
                        record["source_intervention"] = spec["source_intervention"]
                        record["proxy_status"] = spec["proxy_status"]
                        record["proxy_reason"] = spec["proxy_reason"]
                        stitched.append(record)
    return stitched


def _subset_counts(
    records: list[dict[str, object]],
    intervention: str,
    architecture: str,
    n_passes: int,
    item_ids: set[str],
) -> str:
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
    proxy_rows = sum(1 for record in results["records"] if record["proxy_status"] == "mode_equivalent_proxy")
    exact_mode = results["mode"] == "exact_stress_closure_reintegration"
    intro = (
        "这一轮把 bridge slice 再往外扩成 14-item mixed stress+literal reintegration，并且对 6 条 non-literal stress item 补上了 exact "
        "`literal_identity_anchor` live closure。对这些 stress-context item，`literal_identity_anchor` 直接使用 exact closure rows；"
        "`normalized_literal_identity_anchor` 和 `claim_normalized_literal_identity_anchor` 则复用同一批 exact rows，因为它们的额外 executor rewrite "
        "只会作用在 aligned literal-overlap case 上，在当前 non-literal stress subset 上是 inert 的。换句话说，这个 artifact 不再依赖 mode-equivalent proxy。"
    ) if exact_mode else (
        "这一轮把 bridge slice 再往外扩成 14-item mixed stress+literal reintegration，但这里明确采用的是 proxy-expanded stitch，而不是伪装成完整新实验。"
        "原因是 wider stress slice 上有 6 个 non-literal item 没有现成的 `literal_identity_anchor` cache；其中 5 个 item 在该 contract 下只会落到 "
        "`must_copy` / `weak_context` / `policy_window_context`，因此用 typed row 作为 mode-equivalent proxy，另 1 个 `preference_context` item "
        "用 identity-selective row 作为 mode-equivalent proxy。literal frontier 与 relation bridge 仍然完全来自已验证 artifact。目标不是夸大结论，"
        "而是先看 claim-sensitive broad literal branch 在更宽 14-item slice 上是否还能保持同样的 non-regression 结构。"
    )
    lines = [
        "# Actual Hallucination Claim Reintegration Summary",
        "",
        intro,
        "",
        f"- slice items: {results['num_items']}",
        f"- seeds: {results['seeds']}",
        f"- mode: {results['mode']}",
        f"- interventions: {', '.join(results['interventions'])}",
        f"- architectures: {', '.join(results['architectures'])}",
        f"- N: {results['n_values']}",
        f"- proxy rows: {proxy_rows}/{len(results['records'])}",
        "",
        "## Proxy Mapping",
        "",
        *(
            [
                "- `halu_02, halu_03, halu_04, halu_05, halu_08, halu_14`: `literal_identity_anchor` now comes from the exact closure artifact.",
                "- On that same stress-context subset, `normalized_literal_identity_anchor` and `claim_normalized_literal_identity_anchor` reuse the exact literal rows as `contract_equivalent_exact`, because their extra aligned-name rewrite never fires there.",
            ]
            if exact_mode
            else [
                "- `halu_02, halu_04, halu_05, halu_08, halu_14`: use `typed_selective_anchor` rows as mode-equivalent proxy because the target branch collapses to `must_copy`, `weak_context`, or `policy_window_context`.",
                "- `halu_03`: use `identity_selective_anchor` rows as mode-equivalent proxy because the target branch demotes the clue to `preference_context` rather than a promotable surrogate.",
            ]
        ),
        "",
    ]
    for intervention in INTERVENTIONS:
        lines.append(f"## {intervention}")
        lines.append("")
        for architecture in ARCHITECTURES:
            lines.append(f"### {architecture}")
            lines.append("")
            lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
            for n in N_VALUES:
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
            "## Claim Reintegration Readout",
            "",
            f"- Unified N=8 false_present: typed/literal/normalized/claim = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['normalized_literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['claim_normalized_literal_identity_anchor']['scale_aware_unified']['8']['false_present_rate']:.3f}`.",
            f"- Note-aware N=8 false_present: typed/literal/normalized/claim = `{results['hallucination_metrics']['typed_selective_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}` / `{results['hallucination_metrics']['claim_normalized_literal_identity_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}`.",
            f"- Broad literal unified N=8 on relation items: literal `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, RELATION_IDS)}`, claim `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, RELATION_IDS)}`.",
            f"- Broad literal unified N=8 on stress-context items: literal `{_subset_counts(records, 'literal_identity_anchor', 'scale_aware_unified', 8, STRESS_CONTEXT_IDS)}`, claim `{_subset_counts(records, 'claim_normalized_literal_identity_anchor', 'scale_aware_unified', 8, STRESS_CONTEXT_IDS)}`.",
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
        "# Actual Hallucination Claim Reintegration Traces",
        "",
        f"这些 trace 固定展示 seed `{seed}`，用来比较 {', '.join(results['interventions'])} 在 14-item reintegration slice 上的 claim surfacing 行为。",
        "",
    ]
    for item_id, label in TRACE_IDS.items():
        item_records = [record for record in records if record["item_id"] == item_id and record["seed"] == seed]
        if not item_records:
            continue
        lines.append(f"## {item_id}: {label}")
        lines.append("")
        for intervention in INTERVENTIONS:
            lines.append(f"### {intervention}")
            lines.append("")
            for architecture in ARCHITECTURES:
                lines.append(f"#### {architecture}")
                lines.append("")
                for n in N_VALUES:
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
                        f"carry={record['carry_forward_events']}; llm_cost=${record['llm_cost_usd']:.4f}; "
                        f"source={record['source_intervention']} @ {Path(record['source_artifact']).name}; proxy={record['proxy_status']}"
                    )
                    lines.append(f"  note: {record['final_note']}")
                lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    surrogate_payload = load_payload(base_dir / SURROGATE_SOURCE)
    bridge_payload = load_payload(base_dir / BRIDGE_SOURCE)
    literal_payload = load_payload(base_dir / LITERAL_SOURCE)
    exact_closure_path = base_dir / EXACT_STRESS_SOURCE
    exact_closure_payload = load_payload(exact_closure_path) if exact_closure_path.exists() else None
    records = build_records(
        surrogate_payload["records"],
        bridge_payload["records"],
        literal_payload["records"],
        None if exact_closure_payload is None else exact_closure_payload["records"],
    )

    aggregate_table: dict[str, dict[str, dict[str, Any]]] = {}
    metric_table: dict[str, dict[str, dict[str, float]]] = {}
    route_counts: dict[str, dict[str, dict[str, int]]] = {}
    proxy_counts: dict[str, int] = dict(Counter(record["proxy_status"] for record in records))

    for intervention in INTERVENTIONS:
        aggregate_table[intervention] = {}
        metric_table[intervention] = {}
        route_counts[intervention] = {}
        for architecture in ARCHITECTURES:
            aggregate_table[intervention][architecture] = {}
            metric_table[intervention][architecture] = {}
            route_counts[intervention][architecture] = {}
            for n_passes in N_VALUES:
                subset = [
                    record
                    for record in records
                    if record["intervention"] == intervention
                    and record["architecture"] == architecture
                    and record["n_passes"] == n_passes
                ]
                aggregate_table[intervention][architecture][str(n_passes)] = micro_base.actual_base.aggregate(subset)
                metric_table[intervention][architecture][str(n_passes)] = robustness_base.hallucination_metrics(subset)
                route_counts[intervention][architecture][str(n_passes)] = dict(Counter(record["route"] for record in subset))

    payload = {
        "description": (
            "Reintegration of the wider actual hallucination stress slice plus the newer literal frontier. "
            "When the exact literal-identity closure artifact is present, the non-literal stress subset is rebuilt without proxy rows; "
            "otherwise the script falls back to the older proxy-expanded stitch."
        ),
        "mode": "exact_stress_closure_reintegration" if exact_closure_payload is not None else "proxy_expanded_stitch",
        "slice_ids": PILOT_IDS,
        "architectures": ARCHITECTURES,
        "interventions": INTERVENTIONS,
        "n_values": N_VALUES,
        "seeds": PILOT_SEEDS,
        "num_items": len(PILOT_IDS),
        "proxy_counts": proxy_counts,
        "source_artifacts": SOURCE_LABELS,
        "exact_closure_source_present": exact_closure_payload is not None,
        "aggregate": aggregate_table,
        "hallucination_metrics": metric_table,
        "route_counts": route_counts,
        "records": records,
    }

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    (base_dir / TRACE_PATH).write_text(build_traces(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")
    print(f"Wrote {base_dir / TRACE_PATH}")


if __name__ == "__main__":
    main()
