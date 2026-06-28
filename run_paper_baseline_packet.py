from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


BASELINES = ["raw_only", "summary_only", "tiered"]
BEST_METHOD = "scale_aware_unified"
RECALL_METHODS = ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware"]
STRESS_METHODS = ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware"]

SMALL_RESULTS = "outputs/small_pilot_results.json"
RECALL_RESULTS = "outputs/actual_recall_expansion_results.json"
STRESS_RESULTS = "outputs/actual_hallucination_stress_results.json"
REINTEGRATION_RESULTS = "outputs/actual_hallucination_claim_reintegration_pilot_results.json"
BENCHMARK_ADAPTER_RESULTS = "outputs/external_benchmark_adapter_layer.json"
BENCHMARK_MINIMAL_RESULTS = "outputs/external_benchmark_minimal_baseline.json"
BENCHMARK_SECTION_RESULTS = "outputs/external_benchmark_reviewer_section.json"
PRIMARY_SURFACE_RESULTS = "outputs/tiermem_style_primary_surface.json"
PROXY_BASE_RESULTS = "outputs/benchmark_first_proxy_base.json"
NATIVE_PRIMARY_BASE_RESULTS = "outputs/benchmark_native_primary_base.json"

JSON_PATH = "outputs/paper_baseline_packet.json"
SUMMARY_PATH = "outputs/paper_baseline_packet.md"
CSV_PATH = "outputs/paper_baseline_panel.csv"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def requirement(
    key: str,
    title: str,
    status: str,
    evidence: str,
    level: str = "must",
) -> dict[str, str]:
    return {
        "key": key,
        "title": title,
        "status": status,
        "level": level,
        "evidence": evidence,
    }


def synthetic_snapshot(payload: dict[str, Any], architecture: str, n: int) -> dict[str, Any]:
    row = payload["aggregate"][architecture][str(n)]
    return {
        "architecture": architecture,
        "n": n,
        "accuracy": row["accuracy"],
        "propagation_rate": row["propagation_rate"],
        "residual_bad_memory_rate": row["residual_bad_memory_rate"],
        "raw_escalation_rate": row["raw_escalation_rate"],
        "mean_cost": row["mean_cost"],
        "unsupported_answer_rate": row["unsupported_answer_rate"],
        "unsafe_answer_rate": row["unsafe_answer_rate"],
        "conflict_answer_rate": row["conflict_answer_rate"],
    }


def actual_snapshot(payload: dict[str, Any], architecture: str, n: int) -> dict[str, Any]:
    row = payload["aggregate"][architecture][str(n)]
    out = {
        "architecture": architecture,
        "n": n,
        "accuracy": row["accuracy"],
        "propagation_rate": row["propagation_rate"],
        "residual_bad_memory_rate": row["residual_bad_memory_rate"],
        "raw_escalation_rate": row["raw_escalation_rate"],
    }
    if "recall_metrics" in payload:
        metrics = payload["recall_metrics"][architecture][str(n)]
        out.update(
            {
                "history_loss_rate": metrics["history_loss_rate"],
                "empty_note_then_abstain_rate": metrics["empty_note_then_abstain_rate"],
                "mean_llm_cost_usd": metrics["mean_llm_cost_usd"],
            }
        )
    if "hallucination_metrics" in payload:
        metrics = payload["hallucination_metrics"][architecture][str(n)]
        out.update(
            {
                "false_present_rate": metrics["false_present_rate"],
                "direct_unsupported_answer_rate": metrics["direct_unsupported_answer_rate"],
                "tentative_guess_note_rate": metrics["tentative_guess_note_rate"],
                "mean_llm_cost_usd": metrics["mean_llm_cost_usd"],
            }
        )
    return out


def build_packet(
    small: dict[str, Any],
    recall: dict[str, Any],
    stress: dict[str, Any],
    reintegration: dict[str, Any],
    benchmark_adapter: dict[str, Any] | None,
    benchmark_minimal: dict[str, Any] | None,
    benchmark_section: dict[str, Any] | None,
    primary_surface: dict[str, Any] | None,
    proxy_base: dict[str, Any] | None,
    native_primary_base: dict[str, Any] | None,
) -> dict[str, Any]:
    small_archs = set(small["architectures"])
    n_values = set(small["n_values"])
    small_summary_n8 = small["aggregate"]["summary_only"]["8"]
    small_tiered_n8 = small["aggregate"]["tiered"]["8"]
    small_unified_n8 = small["aggregate"][BEST_METHOD]["8"]
    recall_summary_n8 = recall["aggregate"]["summary_only"]["8"]
    recall_tiered_n8 = recall["aggregate"]["tiered"]["8"]
    recall_unified_n8 = recall["aggregate"][BEST_METHOD]["8"]
    recall_metrics_n8 = recall["recall_metrics"][BEST_METHOD]["8"]
    stress_summary_n1 = stress["aggregate"]["summary_only"]["1"]
    stress_tiered_n1 = stress["aggregate"]["tiered"]["1"]
    stress_note_n1 = stress["hallucination_metrics"]["scale_aware_note_aware"]["1"]
    reintegration_claim_unified_n8 = reintegration["hallucination_metrics"]["claim_normalized_literal_identity_anchor"]["scale_aware_unified"]["8"]
    reintegration_claim_note_n8 = reintegration["hallucination_metrics"]["claim_normalized_literal_identity_anchor"]["scale_aware_note_aware"]["8"]
    recall_seed_count = len(recall.get("seeds", []))
    stress_seed_count = len(stress.get("seeds", []))
    multi_seed_ready = recall_seed_count > 1 and stress_seed_count > 1
    benchmark_adapter_status = "gap" if benchmark_adapter is None else benchmark_adapter.get("grounding_status", "gap")
    benchmark_status = "gap"
    if benchmark_adapter_status != "gap":
        benchmark_status = "partial"
    if benchmark_adapter_status == "pass" and (benchmark_minimal is not None or benchmark_section is not None):
        benchmark_status = "pass"
    benchmark_section_ready = benchmark_section is not None and benchmark_section.get("verdict", {}).get("benchmark_reviewer_section_ready") is True
    primary_surface_status = "gap"
    if primary_surface is not None:
        primary_surface_status = primary_surface.get("primary_surface_status", {}).get("tiermem_style_primary_base_status", "gap")
    native_primary_ready = native_primary_base is not None and native_primary_base.get("verdict", {}).get("benchmark_native_primary_base_ready") is True
    exact_proxy_rows = reintegration.get("proxy_counts", {}).get("mode_equivalent_proxy", 0)
    exact_frontier_ready = reintegration.get("mode") == "exact_stress_closure_reintegration" and exact_proxy_rows == 0
    proxy_base_status = "gap"
    if benchmark_status == "pass" and primary_surface_status in {"partial", "pass"} and exact_frontier_ready:
        proxy_base_status = "partial"
    if proxy_base is not None:
        proxy_base_status = proxy_base.get("verdict", {}).get("benchmark_first_proxy_base_status", proxy_base_status)
    proxy_base_ready = proxy_base is not None and proxy_base.get("verdict", {}).get("benchmark_first_proxy_base_ready") is True
    broader_section_item_count = (
        0
        if benchmark_section is None
        else benchmark_section["family_rollups"]["hallucination_benchmark_section"]["num_items"]
        + benchmark_section["family_rollups"]["benign_utility_benchmark_section"]["num_items"]
    )
    broader_benchmark_scale_status = (
        "pass"
        if broader_section_item_count >= 48
        else "partial"
        if benchmark_section_ready
        else "gap"
    )
    synthetic_reference_demotion_status = (
        "pass"
        if native_primary_base is not None and native_primary_base.get("strengthening_status", {}).get("synthetic_reference_role") == "support_only"
        else "gap"
    )
    paper_level_ready = (
        multi_seed_ready
        and exact_frontier_ready
        and benchmark_status == "pass"
        and primary_surface_status == "pass"
        and broader_benchmark_scale_status == "pass"
    )

    if paper_level_ready:
        verdict_reason = (
            "the project now has a real closed-loop baseline trio, multi-seed model-backed sanity slices, an exact non-proxy stress-frontier closure, a broader reviewer-facing external benchmark section at usable scale, and a benchmark-native primary base, so the paper-level baseline gate is now satisfied."
        )
    elif multi_seed_ready and exact_frontier_ready and benchmark_status == "pass" and primary_surface_status == "pass" and benchmark_section_ready and proxy_base_ready and native_primary_ready:
        verdict_reason = (
            "the project now has a real closed-loop baseline trio, multi-seed model-backed sanity slices, an exact non-proxy stress-frontier closure, a broader reviewer-facing external benchmark section, a complete benchmark-first proxy base, and a benchmark-native primary base, "
            "but it still lacks larger-scale benchmark coverage before the baseline should be presented as paper-ready."
        )
    elif multi_seed_ready and exact_frontier_ready and benchmark_status == "pass" and primary_surface_status in {"partial", "pass"} and benchmark_section_ready and proxy_base_ready:
        verdict_reason = (
            "the project now has a real closed-loop baseline trio, multi-seed model-backed sanity slices, an exact non-proxy stress-frontier closure, a broader reviewer-facing external benchmark section, a benchmark-first primary surface, and a complete local benchmark-first proxy base, "
            "but it still lacks benchmark-native primary implementation grounding."
        )
    elif multi_seed_ready and exact_frontier_ready and benchmark_status == "pass" and primary_surface_status in {"partial", "pass"} and benchmark_section_ready:
        verdict_reason = (
            "the project now has a real closed-loop baseline trio, multi-seed model-backed sanity slices, an exact non-proxy stress-frontier closure, a broader reviewer-facing external benchmark section, and a benchmark-first primary surface, "
            "but it still lacks full TierMem-native implementation grounding."
        )
    elif multi_seed_ready and exact_frontier_ready and benchmark_status == "pass":
        verdict_reason = (
            "the project now has a real closed-loop baseline trio, multi-seed model-backed sanity slices, an exact non-proxy stress-frontier closure, and a minimal benchmark-grounded external panel, "
            "but it still lacks TierMem-style primary implementation grounding."
        )
    elif multi_seed_ready and exact_frontier_ready:
        verdict_reason = (
            "the project now has a real closed-loop baseline trio, multi-seed model-backed sanity slices, and an exact non-proxy stress-frontier closure, "
            "but it still lacks benchmark-grounded slice-ready external slices and TierMem-style primary implementation grounding."
        )
    else:
        verdict_reason = (
            "the project has a real closed-loop baseline trio and model-backed sanity slices, but it still lacks external benchmark slice grounding, TierMem-style primary grounding, a frozen multi-seed model-backed baseline panel, and an exact non-proxy stress-frontier closure."
        )

    requirements = [
        requirement(
            "closed_loop_baseline_trio",
            "Core baseline trio is frozen on the same sweep",
            "pass" if all(name in small_archs for name in BASELINES) else "gap",
            f"observed architectures include `{sorted(small_archs)}`.",
        ),
        requirement(
            "shared_depth_sweep",
            "Consolidation depth remains the primary variable",
            "pass" if {0, 1, 2, 4, 8}.issubset(n_values) else "gap",
            f"observed N values = `{small['n_values']}`.",
        ),
        requirement(
            "stagewise_failure_attribution",
            "Stage-wise failure attribution is visible",
            "pass"
            if {"unsupported_answer_rate", "unsafe_answer_rate", "conflict_answer_rate", "propagation_rate", "residual_bad_memory_rate"}.issubset(set(small_summary_n8.keys()))
            else "gap",
            "synthetic panel exposes answer-side and latent/residual failure rates in aggregate rows.",
        ),
        requirement(
            "utility_risk_cost_reporting",
            "Utility, risk, and cost are reported together",
            "pass"
            if {"accuracy", "propagation_rate", "raw_escalation_rate", "mean_cost"}.issubset(set(small_summary_n8.keys()))
            else "gap",
            "synthetic panel reports accuracy, propagation, raw escalation, and mean cost together.",
        ),
        requirement(
            "real_model_benign_conflict_sanity",
            "Real-model benign/conflict sanity slice exists",
            "pass",
            f"actual recall slice uses `{recall['num_items']}` items, seeds `{recall['seeds']}`, and exposes answerability-loss metrics such as `history_loss`.",
        ),
        requirement(
            "real_model_hallucination_sanity",
            "Real-model hallucination sanity slice exists",
            "pass",
            f"actual hallucination stress slice uses `{stress['num_items']}` items, seeds `{stress['seeds']}`, and exposes `false_present` / `direct_unsupported_answer`.",
        ),
        requirement(
            "multi_seed_model_backed_panel",
            "Frozen model-backed baseline panel is multi-seed",
            "pass" if multi_seed_ready else "partial",
            (
                f"actual recall seeds = `{recall['seeds']}`, actual stress seeds = `{stress['seeds']}`."
                if multi_seed_ready
                else "we have multi-seed model-backed follow-up artifacts elsewhere, but the current frozen recall/stress baseline panel is still single-seed."
            ),
        ),
        requirement(
            "primary_external_benchmark_grounding",
            "Primary baseline is grounded on an external benchmark slice",
            benchmark_status,
            (
                "current main baseline still uses curated synthetic items and audited local slices rather than a frozen HaluMem / LongMemEval / LoCoMo style benchmark subset."
                if benchmark_adapter is None
                else (
                    f"benchmark adapter layer status = `{benchmark_adapter.get('grounding_status')}`, "
                    f"data-ready adapters = `{benchmark_adapter.get('data_ready_count')}/{benchmark_adapter.get('adapter_ready_count')}`, "
                    f"slice-ready adapters = `{benchmark_adapter.get('slice_ready_count', 0)}/{benchmark_adapter.get('adapter_ready_count')}`, "
                    f"benchmark panel attached = `{benchmark_minimal is not None}`, "
                    f"broader reviewer section attached = `{benchmark_section_ready}`."
                )
            ),
        ),
        requirement(
            "tiermem_style_primary_base",
            "Primary implementation is grounded in a TierMem-style base rather than a local proxy stack",
            "pass" if native_primary_ready else primary_surface_status,
            (
                "the repo still presents itself as a pre-pilot proxy stack rather than a benchmark-grounded TierMem-style base implementation."
                if primary_surface is None
                else (
                    f"primary surface status = `{primary_surface_status}`, "
                    f"benchmark-first ready = `{primary_surface.get('primary_surface_status', {}).get('benchmark_first_surface_ready')}`, "
                    f"native primary base ready = `{native_primary_ready}`, "
                    f"full TierMem-native grounding = `{primary_surface.get('primary_surface_status', {}).get('full_tiermem_native_grounding')}`."
                )
            ),
        ),
        requirement(
            "benchmark_first_proxy_base_complete",
            "Benchmark-first proxy base is frozen end-to-end",
            proxy_base_status,
            (
                "the repo still lacks a frozen end-to-end benchmark-first proxy base artifact that ties benchmark grounding, primary surface, and exact frontier closure together."
                if proxy_base is None
                else (
                    f"proxy-base status = `{proxy_base_status}`, "
                    f"proxy-base ready = `{proxy_base.get('verdict', {}).get('benchmark_first_proxy_base_ready')}`, "
                    f"full TierMem-native grounding = `{proxy_base.get('verdict', {}).get('full_tiermem_native_grounding')}`."
                )
            ),
        ),
        requirement(
            "broader_benchmark_section_scale",
            "Broader benchmark reviewer section has enough scale for paper-facing use",
            broader_benchmark_scale_status,
            f"current broader benchmark section size = `{broader_section_item_count}` items across both family rollups.",
            level="should",
        ),
        requirement(
            "synthetic_reference_demotion",
            "Synthetic reference is explicitly demoted to support-only status",
            synthetic_reference_demotion_status,
            (
                "the repo still relies on synthetic reference artifacts without an explicit support-only role."
                if native_primary_base is None
                else f"native primary base marks synthetic reference role = `{native_primary_base.get('strengthening_status', {}).get('synthetic_reference_role')}`."
            ),
            level="should",
        ),
        requirement(
            "exact_non_proxy_frontier_closure",
            "Current stress frontier is closed without proxy rows",
            "pass" if exact_frontier_ready else "gap",
            f"current reintegration mode = `{reintegration.get('mode')}`, proxy rows = `{exact_proxy_rows}`.",
        ),
        requirement(
            "frozen_paper_baseline_packet",
            "Reviewer-facing paper baseline packet is frozen",
            "pass",
            "this artifact freezes the baseline trio, model-backed sanity slices, and explicit blockers in one place.",
        ),
    ]

    packet = {
        "description": "Reviewer-facing paper baseline packet for the iterative memory consolidation project.",
        "verdict": {
            "minimal_closed_loop_baseline_ready": True,
            "paper_level_baseline_ready": paper_level_ready,
            "reason": verdict_reason,
        },
        "requirements": requirements,
        "synthetic_core_panel": {
            "baseline_methods": BASELINES,
            "best_method": BEST_METHOD,
            "n_values": small["n_values"],
            "snapshots": {
                architecture: {
                    str(n): synthetic_snapshot(small, architecture, n) for n in small["n_values"]
                }
                for architecture in BASELINES + [BEST_METHOD]
            },
        },
        "model_backed_sanity": {
            "actual_recall_expansion": {
                "slice_ids": recall["slice_ids"],
                "seeds": recall["seeds"],
                "architectures": RECALL_METHODS,
                "n_values": recall["n_values"],
                "snapshots": {
                    architecture: {
                        str(n): actual_snapshot(recall, architecture, n) for n in recall["n_values"]
                    }
                    for architecture in RECALL_METHODS
                },
            },
            "actual_hallucination_stress": {
                "slice_ids": stress["slice_ids"],
                "seeds": stress["seeds"],
                "architectures": STRESS_METHODS,
                "n_values": stress["n_values"],
                "snapshots": {
                    architecture: {
                        str(n): actual_snapshot(stress, architecture, n) for n in stress["n_values"]
                    }
                    for architecture in STRESS_METHODS
                },
            },
        },
        "frontier_status": {
            "claim_reintegration_mode": reintegration.get("mode"),
            "claim_reintegration_proxy_rows": exact_proxy_rows,
            "claim_reintegration_total_rows": len(reintegration.get("records", [])),
            "claim_reintegration_unified_false_present_n8": reintegration_claim_unified_n8["false_present_rate"],
            "claim_reintegration_note_aware_false_present_n8": reintegration_claim_note_n8["false_present_rate"],
        },
        "benchmark_adapter": benchmark_adapter,
        "benchmark_grounded_panel": benchmark_minimal,
        "benchmark_reviewer_section": benchmark_section,
        "primary_surface": primary_surface,
        "benchmark_first_proxy_base": proxy_base,
        "benchmark_native_primary_base": native_primary_base,
        "headline_readout": {
            "synthetic_summary_only_n8": {
                "accuracy": small_summary_n8["accuracy"],
                "propagation_rate": small_summary_n8["propagation_rate"],
                "mean_cost": small_summary_n8["mean_cost"],
            },
            "synthetic_tiered_n8": {
                "accuracy": small_tiered_n8["accuracy"],
                "propagation_rate": small_tiered_n8["propagation_rate"],
                "raw_escalation_rate": small_tiered_n8["raw_escalation_rate"],
                "mean_cost": small_tiered_n8["mean_cost"],
            },
            "synthetic_best_method_n8": {
                "architecture": BEST_METHOD,
                "accuracy": small_unified_n8["accuracy"],
                "propagation_rate": small_unified_n8["propagation_rate"],
                "raw_escalation_rate": small_unified_n8["raw_escalation_rate"],
                "mean_cost": small_unified_n8["mean_cost"],
            },
            "actual_recall_n8": {
                "summary_only_accuracy": recall_summary_n8["accuracy"],
                "tiered_accuracy": recall_tiered_n8["accuracy"],
                "best_method_accuracy": recall_unified_n8["accuracy"],
                "best_method_history_loss": recall_metrics_n8["history_loss_rate"],
            },
            "actual_hallucination_n1": {
                "summary_only_propagation": stress_summary_n1["propagation_rate"],
                "tiered_false_present": stress["hallucination_metrics"]["tiered"]["1"]["false_present_rate"],
                "note_aware_false_present": stress_note_n1["false_present_rate"],
                "tiered_raw_escalation": stress_tiered_n1["raw_escalation_rate"],
            },
        },
        "recommended_next_actions": [
            *(
                []
                if benchmark_status == "pass"
                else [
                    "Populate the frozen benchmark adapter layer with real source files and freeze one runnable HaluMem-style slice plus one runnable LoCoMo/LongMemEval-style slice."
                ]
            ),
            (
                "Expand the broader reviewer-facing benchmark section to a larger frozen scale so the paper-level baseline gate can move from reviewer-credible to fully paper-ready."
                if native_primary_ready
                else "Replace the remaining local proxy-stack internals behind the new benchmark-first primary surface so `tiermem_style_primary_base` can move from partial to pass."
                if primary_surface_status in {"partial", "pass"}
                else "Replace the remaining local proxy-stack framing with a TierMem-style primary implementation surface that a reviewer would recognize as the main baseline."
            ),
            (
                "Further reduce how much reviewer-facing interpretation depends on synthetic-reference support artifacts."
                if native_primary_ready
                else "Carry the broader reviewer-facing benchmark section into more slice families and larger frozen coverage once the current benchmark-first proxy base is stable."
                if proxy_base_ready
                else "Carry the broader reviewer-facing benchmark section into more slice families and larger frozen coverage once the current core section is stable."
                if benchmark_section_ready
                else "Expand the benchmark-first primary surface beyond the first frozen HaluMem / LoCoMo slices and convert it into a broader reviewer-facing benchmark section."
                if benchmark_status == "pass"
                else "Once external slices are data-ready, rebuild the paper baseline packet so the benchmark-grounded panel sits beside the synthetic trio and the multi-seed sanity slices."
            ),
        ],
    }
    return packet


def write_csv(packet: dict[str, Any], path: Path) -> None:
    rows: list[dict[str, Any]] = []
    for architecture, n_rows in packet["synthetic_core_panel"]["snapshots"].items():
        for n, row in n_rows.items():
            rows.append(
                {
                    "panel": "synthetic_core",
                    "method": architecture,
                    "n": n,
                    "accuracy": row["accuracy"],
                    "propagation_rate": row["propagation_rate"],
                    "residual_bad_memory_rate": row["residual_bad_memory_rate"],
                    "raw_escalation_rate": row["raw_escalation_rate"],
                    "mean_cost_or_llm_cost": row["mean_cost"],
                    "history_loss_rate": "",
                    "false_present_rate": "",
                }
            )
    for panel_name, payload in packet["model_backed_sanity"].items():
        for architecture, n_rows in payload["snapshots"].items():
            for n, row in n_rows.items():
                rows.append(
                    {
                        "panel": panel_name,
                        "method": architecture,
                        "n": n,
                        "accuracy": row["accuracy"],
                        "propagation_rate": row["propagation_rate"],
                        "residual_bad_memory_rate": row["residual_bad_memory_rate"],
                        "raw_escalation_rate": row["raw_escalation_rate"],
                        "mean_cost_or_llm_cost": row.get("mean_llm_cost_usd", ""),
                        "history_loss_rate": row.get("history_loss_rate", ""),
                        "false_present_rate": row.get("false_present_rate", ""),
                    }
                )
    benchmark_panel = packet.get("benchmark_grounded_panel") or {}
    benchmark_section = packet.get("benchmark_reviewer_section") or {}
    for panel_name, payload in (benchmark_panel.get("benchmark_panels") or {}).items():
        for architecture, n_rows in payload["snapshots"].items():
            for n, row in n_rows.items():
                rows.append(
                    {
                        "panel": panel_name,
                        "method": architecture,
                        "n": n,
                        "accuracy": row["accuracy"],
                        "propagation_rate": row["propagation_rate"],
                        "residual_bad_memory_rate": row["residual_bad_memory_rate"],
                        "raw_escalation_rate": row["raw_escalation_rate"],
                        "mean_cost_or_llm_cost": row.get("mean_llm_cost_usd", ""),
                        "history_loss_rate": row.get("history_loss_rate", ""),
                        "false_present_rate": row.get("false_present_rate", ""),
                    }
                )
    for panel_name, payload in (benchmark_section.get("family_rollups") or {}).items():
        for architecture, n_rows in payload["snapshots"].items():
            for n, row in n_rows.items():
                rows.append(
                    {
                        "panel": panel_name,
                        "method": architecture,
                        "n": n,
                        "accuracy": row["accuracy"],
                        "propagation_rate": row["propagation_rate"],
                        "residual_bad_memory_rate": row["residual_bad_memory_rate"],
                        "raw_escalation_rate": row["raw_escalation_rate"],
                        "mean_cost_or_llm_cost": row.get("mean_llm_cost_usd", ""),
                        "history_loss_rate": row.get("history_loss_rate", ""),
                        "false_present_rate": row.get("false_present_rate", ""),
                    }
                )

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "panel",
                "method",
                "n",
                "accuracy",
                "propagation_rate",
                "residual_bad_memory_rate",
                "raw_escalation_rate",
                "mean_cost_or_llm_cost",
                "history_loss_rate",
                "false_present_rate",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def build_summary(packet: dict[str, Any]) -> str:
    lines = [
        "# Paper Baseline Packet",
        "",
        "这个 artifact 不假装我们已经有 benchmark-ready paper baseline。它做的事情是把 reviewer 真正在意的 baseline gate 冻结下来：哪些最小比较已经具备，哪些模型级 sanity 已经落地，哪些 blocker 仍然阻止我们把当前结果写成论文级 baseline。",
        "",
        "## Verdict",
        "",
        f"- minimal closed-loop baseline ready: `{packet['verdict']['minimal_closed_loop_baseline_ready']}`",
        f"- paper-level baseline ready: `{packet['verdict']['paper_level_baseline_ready']}`",
        f"- reason: {packet['verdict']['reason']}",
        "",
        "## Requirement Gate",
        "",
    ]
    for req in packet["requirements"]:
        lines.append(f"- `{req['status'].upper()}` {req['title']}: {req['evidence']}")

    lines.extend(
        [
            "",
            "## Synthetic Core Panel",
            "",
            "同一 `N`-sweep 上的 baseline trio 已经存在，因此 reviewer 至少能看到 clean closed-loop comparison，而不是一串无法对齐的局部 patch。",
            "",
            "| Method | N=0 acc | N=8 acc | N=8 propagation | N=8 residual | N=8 raw escalation | N=8 mean cost |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for architecture in BASELINES + [BEST_METHOD]:
        n0 = packet["synthetic_core_panel"]["snapshots"][architecture]["0"]
        n8 = packet["synthetic_core_panel"]["snapshots"][architecture]["8"]
        lines.append(
            f"| {architecture} | {n0['accuracy']:.3f} | {n8['accuracy']:.3f} | {n8['propagation_rate']:.3f} | "
            f"{n8['residual_bad_memory_rate']:.3f} | {n8['raw_escalation_rate']:.3f} | {n8['mean_cost']:.3f} |"
        )

    recall = packet["model_backed_sanity"]["actual_recall_expansion"]["snapshots"]
    stress = packet["model_backed_sanity"]["actual_hallucination_stress"]["snapshots"]
    lines.extend(
        [
            "",
            "## Model-Backed Sanity",
            "",
            "我们已经不只停在纯 proxy：real-model recall slice 和 real-model hallucination stress slice 都存在，所以 baseline story 至少有 model-backed sanity，而不是只有手写 compactor。",
            "",
            "### Actual Recall Expansion (N=8)",
            "",
            "| Method | accuracy | propagation | residual | raw escalation | history loss | empty-note-then-abstain | llm cost |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for architecture in RECALL_METHODS:
        row = recall[architecture]["8"]
        lines.append(
            f"| {architecture} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
            f"{row['raw_escalation_rate']:.3f} | {row['history_loss_rate']:.3f} | {row['empty_note_then_abstain_rate']:.3f} | {row['mean_llm_cost_usd']:.4f} |"
        )

    lines.extend(
        [
            "",
            "### Actual Hallucination Stress",
            "",
            "| Method | N=1 propagation | N=1 false_present | N=1 raw escalation | N=8 propagation | N=8 false_present | N=8 raw escalation |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for architecture in STRESS_METHODS:
        row1 = stress[architecture]["1"]
        row8 = stress[architecture]["8"]
        lines.append(
            f"| {architecture} | {row1['propagation_rate']:.3f} | {row1['false_present_rate']:.3f} | {row1['raw_escalation_rate']:.3f} | "
            f"{row8['propagation_rate']:.3f} | {row8['false_present_rate']:.3f} | {row8['raw_escalation_rate']:.3f} |"
        )

    frontier = packet["frontier_status"]
    benchmark_adapter = packet.get("benchmark_adapter")
    benchmark_panel = packet.get("benchmark_grounded_panel")
    benchmark_section = packet.get("benchmark_reviewer_section")
    primary_surface = packet.get("primary_surface") or {}
    proxy_base = packet.get("benchmark_first_proxy_base") or {}
    native_primary_base = packet.get("benchmark_native_primary_base") or {}
    benchmark_panels = {} if benchmark_panel is None else benchmark_panel.get("benchmark_panels", {})
    benchmark_family_rollups = {} if benchmark_section is None else benchmark_section.get("family_rollups", {})
    lines.extend(
        [
            "",
            "## Benchmark-First Primary Surface",
            "",
            f"- primary surface attached: `{bool(primary_surface)}`",
            f"- primary surface status: `{primary_surface.get('primary_surface_status', {}).get('tiermem_style_primary_base_status')}`",
            f"- primary surface note: `{primary_surface.get('primary_surface_status', {}).get('note')}`",
            "",
            "## Benchmark-First Proxy Base",
            "",
            f"- proxy base attached: `{bool(proxy_base)}`",
            f"- proxy base status: `{proxy_base.get('verdict', {}).get('benchmark_first_proxy_base_status')}`",
            f"- proxy base ready: `{proxy_base.get('verdict', {}).get('benchmark_first_proxy_base_ready')}`",
            f"- proxy base note: `{proxy_base.get('verdict', {}).get('note')}`",
            "",
            "## Benchmark-Native Primary Base",
            "",
            f"- native primary base attached: `{bool(native_primary_base)}`",
            f"- native primary base ready: `{native_primary_base.get('verdict', {}).get('benchmark_native_primary_base_ready')}`",
            f"- native primary base status: `{native_primary_base.get('verdict', {}).get('tiermem_style_primary_base_status')}`",
            f"- native primary base note: `{native_primary_base.get('verdict', {}).get('note')}`",
            "",
            "## Frontier Status",
            "",
            f"- current claim reintegration mode: `{frontier['claim_reintegration_mode']}`",
            f"- proxy rows in current reintegration artifact: `{frontier['claim_reintegration_proxy_rows']}/{frontier['claim_reintegration_total_rows']}`",
            f"- claim reintegration unified `N=8 false_present`: `{frontier['claim_reintegration_unified_false_present_n8']:.3f}`",
            f"- claim reintegration note-aware `N=8 false_present`: `{frontier['claim_reintegration_note_aware_false_present_n8']:.3f}`",
            "",
            "## Benchmark Adapter Status",
            "",
            f"- benchmark adapter grounding status: `{None if benchmark_adapter is None else benchmark_adapter.get('grounding_status')}`",
            f"- benchmark adapter data-ready count: `{0 if benchmark_adapter is None else benchmark_adapter.get('data_ready_count')}/{0 if benchmark_adapter is None else benchmark_adapter.get('adapter_ready_count')}`",
            f"- benchmark adapter slice-ready count: `{0 if benchmark_adapter is None else benchmark_adapter.get('slice_ready_count', 0)}/{0 if benchmark_adapter is None else benchmark_adapter.get('adapter_ready_count')}`",
            "",
            "## Benchmark-Grounded Panel",
            "",
            f"- benchmark panel attached: `{benchmark_panel is not None}`",
            f"- benchmark panel names: `{sorted(benchmark_panels.keys())}`",
            f"- broader reviewer section attached: `{benchmark_section is not None}`",
            f"- broader reviewer section families: `{sorted(benchmark_family_rollups.keys())}`",
            "",
            "## Why This Is Not Paper-Ready Yet",
            "",
            (
                "- 当前 external benchmark 已经不再只是 adapter 占位，而且 reviewer-facing benchmark section 也已经从 starter panel 扩成了更宽的 family rollups；但它还不是完整的大规模 benchmark section。"
                if benchmark_section is not None
                else (
                    "- 当前 external benchmark 已经不再只是 adapter 占位，而是有了最小 benchmark-grounded panel；但它还只是第一版 frozen slices。"
                    if benchmark_panel is not None
                    else "- 主 baseline 仍然还没有真正跑在 slice-ready external benchmark subset 上；当前虽然原始 benchmark 数据已进 repo，但还只是 adapter-backed / data-ready state。"
                )
            ),
            (
                "- 当前 repo 已经有 benchmark-first primary surface，而且 benchmark-native primary base 也已经补上；但 paper-facing benchmark coverage 还不够大。"
                if primary_surface and native_primary_base
                else "- 当前 repo 已经有 benchmark-first primary surface，但它还只是 presentation-layer partial，不是完整 TierMem-native benchmark base。"
                if primary_surface
                else "- 当前 repo 还是 local proxy stack，不是 reviewer 会默认接受的 TierMem-style benchmark base。"
            ),
            (
                "- 当前 benchmark-first proxy base 和 benchmark-native primary base 都已经补齐，所以接下来主要是扩 benchmark scale、继续压低 synthetic support 占比。"
                if proxy_base and native_primary_base
                else "- 当前 benchmark-first proxy base 已经补齐，所以 remaining blocker 不再是“proxy 没串起来”，而是“native implementation grounding 仍未完成”。"
                if proxy_base
                else "- 当前 benchmark-first proxy base 还没有被单独冻结成一份总工件，所以 proxy completion 这件事还不够显式。"
            ),
            (
                "- 即使 primary-base blocker 已经补掉，当前更大的任务仍然是把 benchmark section 扩到更接近 paper-facing 的规模。"
                if native_primary_base
                else "- 即使 multi-seed sanity、exact frontier closure、以及最小 benchmark panel 已经补上，它们也不能替代完整 TierMem-style primary base。"
            ),
            "",
            "## Next Required Actions",
            "",
        ]
    )
    for action in packet["recommended_next_actions"]:
        lines.append(f"- {action}")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    small = load_json(base_dir / SMALL_RESULTS)
    recall = load_json(base_dir / RECALL_RESULTS)
    stress = load_json(base_dir / STRESS_RESULTS)
    reintegration = load_json(base_dir / REINTEGRATION_RESULTS)
    benchmark_adapter_path = base_dir / BENCHMARK_ADAPTER_RESULTS
    benchmark_minimal_path = base_dir / BENCHMARK_MINIMAL_RESULTS
    benchmark_section_path = base_dir / BENCHMARK_SECTION_RESULTS
    primary_surface_path = base_dir / PRIMARY_SURFACE_RESULTS
    proxy_base_path = base_dir / PROXY_BASE_RESULTS
    native_primary_base_path = base_dir / NATIVE_PRIMARY_BASE_RESULTS
    benchmark_adapter = load_json(benchmark_adapter_path) if benchmark_adapter_path.exists() else None
    benchmark_minimal = load_json(benchmark_minimal_path) if benchmark_minimal_path.exists() else None
    benchmark_section = load_json(benchmark_section_path) if benchmark_section_path.exists() else None
    primary_surface = load_json(primary_surface_path) if primary_surface_path.exists() else None
    proxy_base = load_json(proxy_base_path) if proxy_base_path.exists() else None
    native_primary_base = load_json(native_primary_base_path) if native_primary_base_path.exists() else None

    packet = build_packet(
        small,
        recall,
        stress,
        reintegration,
        benchmark_adapter,
        benchmark_minimal,
        benchmark_section,
        primary_surface,
        proxy_base,
        native_primary_base,
    )
    (base_dir / JSON_PATH).write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(packet), encoding="utf-8")
    write_csv(packet, base_dir / CSV_PATH)
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")
    print(f"Wrote {base_dir / CSV_PATH}")


if __name__ == "__main__":
    main()
