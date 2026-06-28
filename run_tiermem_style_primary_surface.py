from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SMALL_RESULTS = "outputs/small_pilot_results.json"
RECALL_RESULTS = "outputs/actual_recall_expansion_results.json"
STRESS_RESULTS = "outputs/actual_hallucination_stress_results.json"
REINTEGRATION_RESULTS = "outputs/actual_hallucination_claim_reintegration_pilot_results.json"
BENCHMARK_ADAPTER_RESULTS = "outputs/external_benchmark_adapter_layer.json"
BENCHMARK_MINIMAL_RESULTS = "outputs/external_benchmark_minimal_baseline.json"
BENCHMARK_SECTION_RESULTS = "outputs/external_benchmark_reviewer_section.json"
BENCHMARK_NATIVE_PRIMARY_BASE_RESULTS = "outputs/benchmark_native_primary_base.json"

JSON_PATH = "outputs/tiermem_style_primary_surface.json"
SUMMARY_PATH = "outputs/tiermem_style_primary_surface.md"
BENCHMARK_FIRST_ENTRYPOINT = "run_benchmark_first_primary_entrypoint.py"
BENCHMARK_FIRST_PROXY_BASE = "outputs/benchmark_first_proxy_base.json"

ARCHITECTURES = ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware"]
BASELINE_TRIO = ["raw_only", "summary_only", "tiered"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_load_json(path: Path) -> dict[str, Any] | None:
    return load_json(path) if path.exists() else None


def summarize_row(row: dict[str, Any], *keys: str) -> dict[str, Any]:
    summary = {"accuracy": row["accuracy"]}
    for key in keys:
        if key in row:
            summary[key] = row[key]
    return summary


def benchmark_panel_summary(panel: dict[str, Any], focus_metric: str) -> dict[str, Any]:
    seed_snapshots = panel.get("seed_snapshots", {})
    return {
        "slice_manifest_path": panel.get("slice_manifest_path"),
        "slice_manifest_version": panel.get("slice_manifest_version"),
        "slice_ids": panel.get("slice_ids", []),
        "num_items": panel["num_items"],
        "n1_rows": {
            architecture: summarize_row(
                panel["snapshots"][architecture]["1"],
                "propagation_rate",
                "residual_bad_memory_rate",
                "raw_escalation_rate",
                focus_metric,
            )
            for architecture in ARCHITECTURES
        },
        "n8_rows": {
            architecture: summarize_row(
                panel["snapshots"][architecture]["8"],
                "propagation_rate",
                "residual_bad_memory_rate",
                "raw_escalation_rate",
                focus_metric,
            )
            for architecture in ARCHITECTURES
        },
        "seed_focus_metric_n8": {
            architecture: {
                seed: {
                    "accuracy": seed_row["accuracy"],
                    focus_metric: seed_row[focus_metric],
                    "raw_escalation_rate": seed_row["raw_escalation_rate"],
                }
                for seed, seed_row in seed_snapshots.get(architecture, {}).get("8", {}).items()
            }
            for architecture in ARCHITECTURES
        },
    }


def benchmark_core_from_section(section: dict[str, Any], benchmark_grounding_status: str) -> dict[str, Any]:
    family_rollups = section.get("family_rollups", {})
    return {
        "source_path": BENCHMARK_SECTION_RESULTS,
        "source_kind": "broader_reviewer_section",
        "adapter_grounding_status": benchmark_grounding_status,
        "panel_names": sorted(family_rollups.keys()),
        "slice_panel_names": sorted(section.get("slice_panels", {}).keys()),
        "panels": {
            "hallucination_benchmark_section": benchmark_panel_summary(
                family_rollups["hallucination_benchmark_section"],
                "false_present_rate",
            ),
            "benign_utility_benchmark_section": benchmark_panel_summary(
                family_rollups["benign_utility_benchmark_section"],
                "history_loss_rate",
            ),
        },
    }


def benchmark_core_from_minimal(minimal: dict[str, Any], benchmark_grounding_status: str) -> dict[str, Any]:
    benchmark_panels = minimal.get("benchmark_panels", {})
    return {
        "source_path": BENCHMARK_MINIMAL_RESULTS,
        "source_kind": "minimal_starter_panel",
        "adapter_grounding_status": benchmark_grounding_status,
        "panel_names": sorted(benchmark_panels.keys()),
        "slice_panel_names": sorted(benchmark_panels.keys()),
        "panels": {
            "halumem_hallucination": benchmark_panel_summary(benchmark_panels["halumem_hallucination"], "false_present_rate"),
            "locomo_benign_utility": benchmark_panel_summary(benchmark_panels["locomo_benign_utility"], "history_loss_rate"),
        },
    }


def recall_summary(recall: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_path": RECALL_RESULTS,
        "slice_ids": recall["slice_ids"],
        "seeds": recall["seeds"],
        "n8_rows": {
            architecture: summarize_row(
                recall["aggregate"][architecture]["8"],
                "propagation_rate",
                "residual_bad_memory_rate",
                "raw_escalation_rate",
            )
            | {
                "history_loss_rate": recall["recall_metrics"][architecture]["8"]["history_loss_rate"],
                "empty_note_then_abstain_rate": recall["recall_metrics"][architecture]["8"]["empty_note_then_abstain_rate"],
            }
            for architecture in ARCHITECTURES
        },
    }


def stress_summary(stress: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_path": STRESS_RESULTS,
        "slice_ids": stress["slice_ids"],
        "seeds": stress["seeds"],
        "n1_rows": {
            architecture: summarize_row(
                stress["aggregate"][architecture]["1"],
                "propagation_rate",
                "residual_bad_memory_rate",
                "raw_escalation_rate",
            )
            | {
                "false_present_rate": stress["hallucination_metrics"][architecture]["1"]["false_present_rate"],
            }
            for architecture in ARCHITECTURES
        },
        "n8_rows": {
            architecture: summarize_row(
                stress["aggregate"][architecture]["8"],
                "propagation_rate",
                "residual_bad_memory_rate",
                "raw_escalation_rate",
            )
            | {
                "false_present_rate": stress["hallucination_metrics"][architecture]["8"]["false_present_rate"],
            }
            for architecture in ARCHITECTURES
        },
    }


def synthetic_reference(small: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_path": SMALL_RESULTS,
        "baseline_methods": BASELINE_TRIO,
        "n8_rows": {
            architecture: summarize_row(
                small["aggregate"][architecture]["8"],
                "propagation_rate",
                "residual_bad_memory_rate",
                "raw_escalation_rate",
                "mean_cost",
            )
            for architecture in BASELINE_TRIO + ["scale_aware_unified"]
        },
    }


def build_payload(
    small: dict[str, Any],
    recall: dict[str, Any],
    stress: dict[str, Any],
    reintegration: dict[str, Any],
    benchmark_adapter: dict[str, Any] | None,
    benchmark_minimal: dict[str, Any] | None,
    benchmark_section: dict[str, Any] | None,
    benchmark_native_primary_base: dict[str, Any] | None,
) -> dict[str, Any]:
    benchmark_grounding_status = "gap" if benchmark_adapter is None else benchmark_adapter.get("grounding_status", "gap")
    section_ready = benchmark_section is not None and benchmark_section.get("verdict", {}).get("benchmark_reviewer_section_ready") is True
    minimal_ready = benchmark_minimal is not None and benchmark_minimal.get("verdict", {}).get("minimal_benchmark_grounded_panel_ready") is True
    benchmark_ready = section_ready or minimal_ready
    native_primary_ready = benchmark_native_primary_base is not None and benchmark_native_primary_base.get("verdict", {}).get("benchmark_native_primary_base_ready") is True
    native_primary_status = benchmark_native_primary_base.get("verdict", {}).get("tiermem_style_primary_base_status", "partial") if benchmark_native_primary_base is not None else "gap"
    full_native_grounding = benchmark_native_primary_base.get("verdict", {}).get("full_tiermem_native_grounding", False) if benchmark_native_primary_base is not None else False
    primary_status = (
        "pass"
        if native_primary_ready
        else "partial"
        if benchmark_ready and benchmark_grounding_status == "pass"
        else "gap"
    )
    exact_proxy_rows = reintegration.get("proxy_counts", {}).get("mode_equivalent_proxy", 0)
    exact_frontier_ready = reintegration.get("mode") == "exact_stress_closure_reintegration" and exact_proxy_rows == 0
    entrypoint_ready = section_ready and (Path(__file__).resolve().parent / BENCHMARK_FIRST_ENTRYPOINT).exists()
    proxy_base_complete = (
        benchmark_grounding_status == "pass"
        and minimal_ready
        and section_ready
        and entrypoint_ready
        and exact_frontier_ready
        and primary_status in {"partial", "pass"}
    )
    benchmark_core = (
        benchmark_core_from_section(benchmark_section, benchmark_grounding_status)
        if section_ready
        else benchmark_core_from_minimal(benchmark_minimal, benchmark_grounding_status)
        if minimal_ready
        else {
            "source_path": BENCHMARK_SECTION_RESULTS if benchmark_section is not None else BENCHMARK_MINIMAL_RESULTS,
            "source_kind": "missing",
            "adapter_grounding_status": benchmark_grounding_status,
            "panel_names": [],
            "slice_panel_names": [],
            "panels": {},
        }
    )

    return {
        "description": "Benchmark-first primary surface that presents the reviewer-facing external benchmark section as the main entrypoint.",
        "primary_surface_status": {
            "benchmark_first_surface_ready": primary_status in {"partial", "pass"},
            "tiermem_style_primary_base_status": primary_status,
            "full_tiermem_native_grounding": full_native_grounding,
            "benchmark_source_kind": benchmark_core["source_kind"],
            "benchmark_first_entrypoint_path": BENCHMARK_FIRST_ENTRYPOINT,
            "benchmark_first_entrypoint_ready": entrypoint_ready,
            "benchmark_first_proxy_base_path": BENCHMARK_FIRST_PROXY_BASE,
            "benchmark_first_proxy_base_complete": proxy_base_complete,
            "benchmark_native_primary_base_path": BENCHMARK_NATIVE_PRIMARY_BASE_RESULTS,
            "benchmark_native_primary_base_ready": native_primary_ready,
            "benchmark_native_primary_base_status": native_primary_status,
            "exact_non_proxy_frontier_ready": exact_frontier_ready,
            "note": (
                "The repo now exposes a benchmark-native primary base over frozen benchmark manifests, so the reviewer-facing primary baseline is no longer just a local proxy surface; the remaining gap is that this is still not a literal full TierMem reproduction or a final large-scale paper section."
                if native_primary_ready
                else "The repo now exposes a complete local benchmark-first proxy base backed by a broader reviewer-facing benchmark section, a benchmark-first entrypoint, and an exact non-proxy frontier closure, but the implementation underneath is still a local proxy-stack partial rather than a full TierMem-native benchmark base."
                if proxy_base_complete
                else "The repo now exposes a benchmark-first primary surface backed by a broader reviewer-facing benchmark section plus a benchmark-first entrypoint, but the implementation underneath is still a local proxy-stack partial rather than a full TierMem-native benchmark base."
                if primary_status == "partial" and section_ready
                else "The repo now exposes a benchmark-first primary surface with real frozen HaluMem and LoCoMo panels, but the implementation underneath is still a local proxy-stack partial rather than a full TierMem-native benchmark base."
                if primary_status == "partial"
                else "The repo still lacks a benchmark-first primary surface backed by runnable frozen external benchmark panels."
            ),
        },
        "reviewer_sequence": [
            "Start with the benchmark-native primary base rather than the synthetic proxy trio."
            if native_primary_ready
            else "Start with the benchmark-grounded reviewer section rather than the synthetic proxy trio.",
            "Use the model-backed sanity slices as realism support for answerability-loss and hallucination-side behavior.",
            "Treat the synthetic core panel as a control-plane reference, not the primary source of evidence.",
        ],
        "benchmark_grounded_core": benchmark_core,
        "model_backed_support": {
            "actual_recall_expansion": recall_summary(recall),
            "actual_hallucination_stress": stress_summary(stress),
        },
        "synthetic_reference": synthetic_reference(small),
        "frontier_reference": {
            "source_path": REINTEGRATION_RESULTS,
            "mode": reintegration.get("mode"),
            "proxy_rows": reintegration.get("proxy_counts", {}).get("mode_equivalent_proxy", 0),
            "total_rows": len(reintegration.get("records", [])),
            "claim_reintegration_unified_false_present_n8": reintegration["hallucination_metrics"]["claim_normalized_literal_identity_anchor"]["scale_aware_unified"]["8"]["false_present_rate"],
            "claim_reintegration_note_aware_false_present_n8": reintegration["hallucination_metrics"]["claim_normalized_literal_identity_anchor"]["scale_aware_note_aware"]["8"]["false_present_rate"],
        },
    }


def build_summary(payload: dict[str, Any]) -> str:
    status = payload["primary_surface_status"]
    benchmark_core = payload["benchmark_grounded_core"]
    recall = payload["model_backed_support"]["actual_recall_expansion"]["n8_rows"]
    stress = payload["model_backed_support"]["actual_hallucination_stress"]
    synthetic = payload["synthetic_reference"]["n8_rows"]

    lines = [
        "# TierMem-Style Primary Surface",
        "",
        "这个 artifact 的目标不是宣称我们已经变成完整 TierMem-native base，而是把 reviewer 应该先看到的 benchmark-grounded panel 放到最前面，把 synthetic / proxy 结果降成支撑层。",
        "",
        "## Status",
        "",
        f"- benchmark-first surface ready: `{status['benchmark_first_surface_ready']}`",
        f"- tiermem-style primary base status: `{status['tiermem_style_primary_base_status']}`",
        f"- full TierMem-native grounding: `{status['full_tiermem_native_grounding']}`",
        f"- benchmark source kind: `{status['benchmark_source_kind']}`",
        f"- benchmark-first entrypoint: `{status['benchmark_first_entrypoint_path']}`",
        f"- benchmark-first entrypoint ready: `{status['benchmark_first_entrypoint_ready']}`",
        f"- benchmark-first proxy base path: `{status['benchmark_first_proxy_base_path']}`",
        f"- benchmark-first proxy base complete: `{status['benchmark_first_proxy_base_complete']}`",
        f"- benchmark-native primary base path: `{status['benchmark_native_primary_base_path']}`",
        f"- benchmark-native primary base ready: `{status['benchmark_native_primary_base_ready']}`",
        f"- benchmark-native primary base status: `{status['benchmark_native_primary_base_status']}`",
        f"- exact non-proxy frontier ready: `{status['exact_non_proxy_frontier_ready']}`",
        f"- note: {status['note']}",
        "",
        "## Benchmark-Grounded Core",
        "",
        f"- source path: `{benchmark_core['source_path']}`",
        f"- source kind: `{benchmark_core['source_kind']}`",
        f"- adapter grounding status: `{benchmark_core['adapter_grounding_status']}`",
        f"- panel names: `{benchmark_core['panel_names']}`",
        f"- slice panel names: `{benchmark_core['slice_panel_names']}`",
        "",
    ]

    if benchmark_core["panels"]:
        halu_key = "hallucination_benchmark_section" if "hallucination_benchmark_section" in benchmark_core["panels"] else "halumem_hallucination"
        benign_key = "benign_utility_benchmark_section" if "benign_utility_benchmark_section" in benchmark_core["panels"] else "locomo_benign_utility"
        halu = benchmark_core["panels"][halu_key]["n8_rows"]
        locomo = benchmark_core["panels"][benign_key]["n8_rows"]
        lines.extend(
            [
                "### HaluMem-Style Hallucination Section (N=8)",
                "",
                "| Method | accuracy | propagation | raw escalation | false_present |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for architecture in ARCHITECTURES:
            row = halu[architecture]
            lines.append(
                f"| {architecture} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['raw_escalation_rate']:.3f} | {row['false_present_rate']:.3f} |"
            )
        lines.extend(
            [
                "",
                "### Benign Utility Section (N=8)",
                "",
                "| Method | accuracy | propagation | raw escalation | history_loss |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for architecture in ARCHITECTURES:
            row = locomo[architecture]
            lines.append(
                f"| {architecture} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['raw_escalation_rate']:.3f} | {row['history_loss_rate']:.3f} |"
            )
        lines.extend(
            [
                "",
                "## Model-Backed Support",
                "",
                "### Actual Recall Expansion (N=8)",
                "",
                "| Method | accuracy | propagation | raw escalation | history_loss |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for architecture in ARCHITECTURES:
            row = recall[architecture]
            lines.append(
                f"| {architecture} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['raw_escalation_rate']:.3f} | {row['history_loss_rate']:.3f} |"
            )
        lines.extend(
            [
                "",
                "### Actual Hallucination Stress",
                "",
                "| Method | N=1 accuracy | N=1 false_present | N=8 accuracy | N=8 false_present |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for architecture in ARCHITECTURES:
            row1 = stress["n1_rows"][architecture]
            row8 = stress["n8_rows"][architecture]
            lines.append(
                f"| {architecture} | {row1['accuracy']:.3f} | {row1['false_present_rate']:.3f} | {row8['accuracy']:.3f} | {row8['false_present_rate']:.3f} |"
            )

    lines.extend(
        [
            "",
            "## Synthetic Reference",
            "",
            "| Method | N=8 accuracy | N=8 propagation | N=8 raw escalation | N=8 mean cost |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for architecture in BASELINE_TRIO + ["scale_aware_unified"]:
        row = synthetic[architecture]
        lines.append(
            f"| {architecture} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} |"
        )

    frontier = payload["frontier_reference"]
    readiness_header = "## Why This Is Still Not Paper-Ready" if status["tiermem_style_primary_base_status"] == "pass" else "## Why This Is Still Partial"
    lines.extend(
        [
            "",
            readiness_header,
            "",
            (
                "- 现在主表面已经进入 benchmark-native primary base 阶段：主 baseline 显式吃 frozen benchmark manifests、query contract 和 evidence contract，而不是只靠 local proxy surface。"
                if status["tiermem_style_primary_base_status"] == "pass"
                else "- 现在主表面已经不是半截 proxy 了：benchmark-first local proxy base 已经补齐，而且已经吃上更宽的 reviewer-facing benchmark section；但它还不是完整、系统性的 benchmark-native 主实现。"
                if status["benchmark_first_proxy_base_complete"]
                else "- 现在主表面已经 benchmark-first，而且已经吃上更宽的 reviewer-facing benchmark section；但它还不是完整、系统性的 benchmark-native 主实现。"
                if benchmark_core["source_kind"] == "broader_reviewer_section"
                else "- 现在主表面已经 benchmark-first，但它还只覆盖第一批 frozen HaluMem / LoCoMo slices，不是更广的 benchmark section。"
            ),
            (
                "- blocker 已经从 must-fix 变成补强：接下来要继续扩更大 benchmark section，并进一步降低 reviewer-facing 解释对 synthetic support 的依赖。"
                if status["tiermem_style_primary_base_status"] == "pass"
                else "- 当前 benchmark-first proxy base 已经能独立成一个 reviewer-facing baseline artifact，但 implementation grounding 仍主要来自本 repo 的 local proxy stack。"
                if status["benchmark_first_proxy_base_complete"]
                else "- 当前 implementation grounding 仍主要来自本 repo 的 local proxy stack，因此这个 surface 还是 presentation-layer partial，不是完整 TierMem-native base。"
            ),
            f"- 当前 frontier 虽然已经是 `{frontier['mode']}`，且 proxy rows = `{frontier['proxy_rows']}/{frontier['total_rows']}`，这说明 stress-closure 已经去 proxy 化；现在如果还要继续推进，重点就不是补 proxy，而是扩 benchmark coverage 和收紧 paper-facing证据结构。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    small = load_json(base_dir / SMALL_RESULTS)
    recall = load_json(base_dir / RECALL_RESULTS)
    stress = load_json(base_dir / STRESS_RESULTS)
    reintegration = load_json(base_dir / REINTEGRATION_RESULTS)
    benchmark_adapter = maybe_load_json(base_dir / BENCHMARK_ADAPTER_RESULTS)
    benchmark_minimal = maybe_load_json(base_dir / BENCHMARK_MINIMAL_RESULTS)
    benchmark_section = maybe_load_json(base_dir / BENCHMARK_SECTION_RESULTS)
    benchmark_native_primary_base = maybe_load_json(base_dir / BENCHMARK_NATIVE_PRIMARY_BASE_RESULTS)

    payload = build_payload(
        small,
        recall,
        stress,
        reintegration,
        benchmark_adapter,
        benchmark_minimal,
        benchmark_section,
        benchmark_native_primary_base,
    )
    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
