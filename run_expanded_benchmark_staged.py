from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

import run_actual_carry_forward_round as carry_base
import run_external_benchmark_reviewer_section as reviewer_section


DEFAULT_ARCHITECTURES = ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware", "psu"]
ARCHITECTURE_LIBRARY = {
    "summary_only": {
        "mode": "base",
        "architecture": "summary_only",
    },
    "tiered": {
        "mode": "base",
        "architecture": "tiered",
    },
    "scale_aware_unified": {
        "mode": "base",
        "architecture": "scale_aware_unified",
    },
    "scale_aware_note_aware": {
        "mode": "base",
        "architecture": "scale_aware_note_aware",
    },
    "psu": {
        "mode": "carry",
        "architecture": "scale_aware_note_aware",
        "intervention": "tiny_carry_forward_scaffold",
        "method_name": "Provenance-Scaffolded Unified",
    },
}
N_VALUES = reviewer_section.N_VALUES

STAGE_SPECS = {
    "smoke": {
        "description": "Fast contract sanity pass across every canonical expanded-pool stratum before broader staged execution.",
        "default_seeds": "11",
        "stratum_quotas": {
            "halumem_unsupported_designation_abstain": 2,
            "locomo_absolute_temporal": 2,
            "locomo_entity_or_attribute": 1,
            "locomo_quantity_or_duration": 1,
            "longmemeval_single_session_user": 2,
            "longmemeval_single_session_assistant": 1,
        },
    },
    "medium": {
        "description": "Broader staged pass that still stays well below the full expanded pool but is large enough to expose stability issues by stratum.",
        "default_seeds": "11,23",
        "stratum_quotas": {
            "halumem_unsupported_designation_abstain": 4,
            "locomo_absolute_temporal": 4,
            "locomo_entity_or_attribute": 2,
            "locomo_quantity_or_duration": 2,
            "longmemeval_single_session_user": 4,
            "longmemeval_single_session_assistant": 2,
        },
    },
    "large": {
        "description": "Larger staged pass with broader official-benchmark coverage and PSU included, meant to sit between medium validation and the full main run.",
        "default_seeds": "11",
        "stratum_quotas": {
            "halumem_unsupported_designation_abstain": 6,
            "locomo_absolute_temporal": 8,
            "locomo_entity_or_attribute": 4,
            "locomo_quantity_or_duration": 4,
            "longmemeval_single_session_user": 8,
            "longmemeval_single_session_assistant": 4,
        },
    },
    "main": {
        "description": "Full expanded official benchmark pool.",
        "default_seeds": "11,23",
        "stratum_quotas": None,
    },
}

JSON_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}.json"
SUMMARY_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}.md"
TRACE_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}_traces.md"


def selected_architectures() -> list[str]:
    architectures_env = os.environ.get("EXPANDED_BENCHMARK_ARCHITECTURES", "").strip()
    if not architectures_env:
        return list(DEFAULT_ARCHITECTURES)
    selected = [part.strip() for part in architectures_env.split(",") if part.strip()]
    unknown = [architecture for architecture in selected if architecture not in ARCHITECTURE_LIBRARY]
    if unknown:
        raise RuntimeError(f"Unknown expanded benchmark architectures: {unknown}. Expected subset of {sorted(ARCHITECTURE_LIBRARY)}.")
    return selected


def evaluate_record(
    item: dict[str, Any],
    architecture: str,
    n_passes: int,
    seed: int,
    summarizer: reviewer_section.DeepSeekMemorySummarizer,
) -> dict[str, Any]:
    spec = ARCHITECTURE_LIBRARY[architecture]
    if spec["mode"] == "base":
        record = reviewer_section.actual_base.evaluate_architecture(item, spec["architecture"], n_passes, seed, summarizer)
    elif spec["mode"] == "carry":
        record = carry_base.evaluate_architecture(
            item,
            spec["architecture"],
            n_passes,
            seed,
            spec["intervention"],
            summarizer,
        )
    else:
        raise RuntimeError(f"Unknown expanded benchmark architecture mode: {spec['mode']}")

    record["architecture"] = architecture
    if "intervention" in spec:
        record["benchmark_method_contract"] = spec["intervention"]
    if "method_name" in spec:
        record["benchmark_method_name"] = spec["method_name"]
    return record


def panel_specs() -> list[dict[str, Any]]:
    return [
        {
            "panel_id": "halumem_expanded_v1",
            "family_rollup": "hallucination_expanded_pool",
            "manifest_path": "benchmarks/halumem/frozen_slices/halumem_hallucination_expanded_v1.json",
            "prompt_version": "benchmark_halumem_v2",
            "cache_dir_name": "external_benchmark_halumem_cache",
            "metrics_fn": reviewer_section.hallucination_base.hallucination_metrics,
            "prompt_override": reviewer_section.hallucination_base.stress_pass_prompt,
            "focus_metric": "false_present_rate",
            "focus_label": "false_present",
        },
        {
            "panel_id": "locomo_expanded_v1",
            "family_rollup": "benign_utility_expanded_pool",
            "manifest_path": "benchmarks/locomo/frozen_slices/locomo_benign_utility_expanded_v1.json",
            "prompt_version": "benchmark_locomo_v2",
            "cache_dir_name": "external_benchmark_locomo_cache",
            "metrics_fn": reviewer_section.recall_base.recall_metrics,
            "prompt_override": None,
            "focus_metric": "history_loss_rate",
            "focus_label": "history_loss",
        },
        {
            "panel_id": "longmemeval_expanded_v2",
            "family_rollup": "benign_utility_expanded_pool",
            "manifest_path": "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_expanded_v2.json",
            "prompt_version": "benchmark_locomo_v2",
            "cache_dir_name": "external_benchmark_locomo_cache",
            "metrics_fn": reviewer_section.recall_base.recall_metrics,
            "prompt_override": None,
            "focus_metric": "history_loss_rate",
            "focus_label": "history_loss",
        },
    ]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def selected_stage() -> str:
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        stage = sys.argv[1].strip().lower()
    else:
        stage = os.environ.get("EXPANDED_BENCHMARK_STAGE", "smoke").strip().lower()
    if stage not in STAGE_SPECS:
        raise RuntimeError(f"Unknown stage `{stage}`. Expected one of {sorted(STAGE_SPECS)}.")
    return stage


def maybe_override_seeds_from_env(stage: str) -> None:
    seeds_env = os.environ.get("EXPANDED_BENCHMARK_SEEDS", "").strip()
    if seeds_env:
        os.environ["EXTERNAL_BENCHMARK_SECTION_SEEDS"] = seeds_env
        return
    if not os.environ.get("EXTERNAL_BENCHMARK_SECTION_SEEDS", "").strip():
        os.environ["EXTERNAL_BENCHMARK_SECTION_SEEDS"] = STAGE_SPECS[stage]["default_seeds"]


def select_items_for_stage(items: list[dict[str, Any]], stage: str) -> list[dict[str, Any]]:
    quotas = STAGE_SPECS[stage]["stratum_quotas"]
    if quotas is None:
        return list(items)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item["evaluation_stratum"]].append(item)

    selected: list[dict[str, Any]] = []
    for stratum, rows in grouped.items():
        quota = quotas.get(stratum)
        if quota is None:
            continue
        if len(rows) < quota:
            raise RuntimeError(f"Stage `{stage}` requires {quota} items for stratum `{stratum}`, but only found {len(rows)}.")
        selected.extend(rows[:quota])

    selected_ids = {item["id"] for item in selected}
    return [item for item in items if item["id"] in selected_ids]


def build_panel_selection_summary(selected_items: list[dict[str, Any]], total_items: int) -> dict[str, Any]:
    stratum_counts = Counter(item["evaluation_stratum"] for item in selected_items)
    complexity_counts = Counter(item.get("complexity_band", "missing") for item in selected_items)
    return {
        "selected_count": len(selected_items),
        "available_count": total_items,
        "selected_fraction": round(len(selected_items) / max(1, total_items), 3),
        "stratum_counts": dict(sorted(stratum_counts.items())),
        "complexity_counts": dict(sorted(complexity_counts.items())),
    }


def aggregate_family(
    *,
    panel_ids: list[str],
    panel_payloads: dict[str, dict[str, Any]],
    metrics_fn: Callable[[list[dict[str, Any]]], dict[str, float]],
    focus_metric: str,
    focus_label: str,
    seeds: list[int],
    architectures: list[str],
) -> dict[str, Any]:
    return reviewer_section.aggregate_family(
        panel_ids=panel_ids,
        panel_payloads=panel_payloads,
        metrics_fn=metrics_fn,
        focus_metric=focus_metric,
        focus_label=focus_label,
        seeds=seeds,
        architectures=architectures,
    )


def build_summary(payload: dict[str, Any]) -> str:
    architectures = payload["architectures"]
    lines = [
        f"# Expanded Benchmark Stage: {payload['stage']}",
        "",
        payload["stage_description"],
        "",
        f"- seeds: `{payload['seeds']}`",
        f"- architectures: `{', '.join(payload['architectures'])}`",
        f"- N values: `{payload['n_values']}`",
        f"- total selected items: `{payload['num_items']}`",
        "",
        "## Panel Coverage",
        "",
        "| Panel | Selected | Available | Selected Fraction | Strata |",
        "|---|---:|---:|---:|---|",
    ]
    for panel_id, panel in payload["slice_panels"].items():
        selection = panel["selection_summary"]
        lines.append(
            f"| {panel_id} | {selection['selected_count']} | {selection['available_count']} | {selection['selected_fraction']:.3f} | {selection['stratum_counts']} |"
        )

    lines.extend(
        [
            "",
            "## Family Rollups",
            "",
        ]
    )
    for family_key, family in payload["family_rollups"].items():
        lines.append(f"### {family_key}")
        lines.append("")
        lines.append(f"- member_panels: `{family['panel_ids']}`")
        lines.append(f"- num_items: `{family['num_items']}`")
        if family["focus_metric"] == "false_present_rate":
            lines.append("")
            lines.append("| Method | N=1 acc | N=1 false_present | N=8 acc | N=8 false_present | N=8 raw escalation |")
            lines.append("|---|---:|---:|---:|---:|---:|")
            for architecture in architectures:
                row1 = family["snapshots"][architecture]["1"]
                row8 = family["snapshots"][architecture]["8"]
                lines.append(
                    f"| {architecture} | {row1['accuracy']:.3f} | {row1['false_present_rate']:.3f} | "
                    f"{row8['accuracy']:.3f} | {row8['false_present_rate']:.3f} | {row8['raw_escalation_rate']:.3f} |"
                )
        else:
            lines.append("")
            lines.append("| Method | N=1 acc | N=1 history_loss | N=8 acc | N=8 history_loss | N=8 raw escalation |")
            lines.append("|---|---:|---:|---:|---:|---:|")
            for architecture in architectures:
                row1 = family["snapshots"][architecture]["1"]
                row8 = family["snapshots"][architecture]["8"]
                lines.append(
                    f"| {architecture} | {row1['accuracy']:.3f} | {row1['history_loss_rate']:.3f} | "
                    f"{row8['accuracy']:.3f} | {row8['history_loss_rate']:.3f} | {row8['raw_escalation_rate']:.3f} |"
                )
        lines.append("")
        lines.append("#### Seed Stability (N=8)")
        lines.append("")
        if family["focus_metric"] == "false_present_rate":
            lines.append("| Method | accuracy by seed | false_present by seed | false_present span |")
            lines.append("|---|---|---|---:|")
            for architecture in architectures:
                seed_rows = family["seed_snapshots"][architecture]["8"]
                values = [seed_rows[str(seed)]["false_present_rate"] for seed in payload["seeds"]]
                lines.append(
                    f"| {architecture} | {reviewer_section.seed_metric_string(seed_rows, payload['seeds'], 'accuracy')} | "
                    f"{reviewer_section.seed_metric_string(seed_rows, payload['seeds'], 'false_present_rate')} | {max(values) - min(values):.3f} |"
                )
        else:
            lines.append("| Method | accuracy by seed | history_loss by seed | history_loss span |")
            lines.append("|---|---|---|---:|")
            for architecture in architectures:
                seed_rows = family["seed_snapshots"][architecture]["8"]
                values = [seed_rows[str(seed)]["history_loss_rate"] for seed in payload["seeds"]]
                lines.append(
                    f"| {architecture} | {reviewer_section.seed_metric_string(seed_rows, payload['seeds'], 'accuracy')} | "
                    f"{reviewer_section.seed_metric_string(seed_rows, payload['seeds'], 'history_loss_rate')} | {max(values) - min(values):.3f} |"
                )
        lines.append("")

    lines.extend(
        [
            "## Readout",
            "",
            "- This staged artifact uses the expanded official benchmark pool rather than the older 32-item reviewer section, but it still preserves the same benchmark-native compaction stack and family-level metrics.",
            "- Smoke and medium stages should be interpreted as execution and stability checks over canonical strata, not as the final paper-facing benchmark table.",
            "- The right success condition for this artifact is structural stability across seeds and families; the right next step after a stable medium run is deciding whether to promote the full expanded main run.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(payload: dict[str, Any]) -> str:
    architectures = payload["architectures"]
    lines = [
        f"# Expanded Benchmark Stage Traces: {payload['stage']}",
        "",
        "这些 trace 用来快速确认 staged run 里的每个 expanded panel 真的进入了同一套 compaction stack。",
        "",
    ]
    for panel_id, panel in payload["slice_panels"].items():
        lines.append(f"## {panel_id}")
        lines.append("")
        trace_ids: list[str] = []
        seen_strata: set[str] = set()
        for item in panel["selected_items"]:
            stratum = item["evaluation_stratum"]
            if stratum in seen_strata:
                continue
            seen_strata.add(stratum)
            trace_ids.append(item["id"])
        for item_id in trace_ids:
            lines.append(f"### {item_id}")
            lines.append("")
            for architecture in architectures:
                lines.append(f"- `{architecture}`")
                for n_passes in N_VALUES:
                    record = next(
                        row
                        for row in panel["records"]
                        if row["item_id"] == item_id
                        and row["architecture"] == architecture
                        and row["n_passes"] == n_passes
                        and row["seed"] == payload["seeds"][0]
                    )
                    probe = "-" if record["probe_status"] is None else f"{record['probe_status']} / {record['probe_score']:.3f}"
                    carry = record.get("carry_forward_events")
                    carry_fragment = "" if carry is None else f"; carry={carry}"
                    lines.append(
                        f"  N={n_passes}: probe={probe}; compact={record['compact_answer']}; final={record['answer']}; "
                        f"route={record['route']}; raw={int(record['raw_escalated'])}{carry_fragment}; llm_cost=${record['llm_cost_usd']:.4f}"
                    )
                lines.append("")
    return "\n".join(lines) + "\n"


def build_stage_payload(stage: str, architectures: list[str] | None = None) -> dict[str, Any]:
    maybe_override_seeds_from_env(stage)
    base_dir = Path(__file__).resolve().parent
    specs = panel_specs()
    selected_methods = selected_architectures() if architectures is None else architectures

    slice_panels: dict[str, dict[str, Any]] = {}
    seeds: list[int] | None = None
    metrics_by_family: dict[str, Callable[[list[dict[str, Any]]], dict[str, float]]] = {}
    focus_by_family: dict[str, tuple[str, str]] = {}
    total_selected_items = 0
    overall_stratum_counts: Counter[str] = Counter()

    for spec in specs:
        manifest = load_json(base_dir / spec["manifest_path"])
        selected_items = select_items_for_stage(list(manifest["items"]), stage)
        selection_summary = build_panel_selection_summary(selected_items, len(manifest["items"]))
        overall_stratum_counts.update(item["evaluation_stratum"] for item in selected_items)
        snapshots, seed_snapshots, route_counts, records, panel_seeds = reviewer_section.evaluate_items(
            items=selected_items,
            prompt_version=spec["prompt_version"],
            cache_dir_name=spec["cache_dir_name"],
            metrics_fn=spec["metrics_fn"],
            prompt_override=spec["prompt_override"],
            architectures=selected_methods,
            record_evaluator=evaluate_record,
        )
        if seeds is None:
            seeds = panel_seeds
        elif seeds != panel_seeds:
            raise RuntimeError(f"Stage run seed mismatch: {seeds} vs {panel_seeds}")
        slice_panels[spec["panel_id"]] = {
            "panel_id": spec["panel_id"],
            "family_rollup": spec["family_rollup"],
            "slice_manifest_path": spec["manifest_path"],
            "slice_manifest_version": manifest.get("version"),
            "slice_ids": [item["id"] for item in selected_items],
            "num_items": len(selected_items),
            "selected_items": selected_items,
            "selection_summary": selection_summary,
            "snapshots": snapshots,
            "seed_snapshots": seed_snapshots,
            "route_counts": route_counts,
            "records": records,
            "focus_metric": spec["focus_metric"],
            "focus_label": spec["focus_label"],
        }
        total_selected_items += len(selected_items)
        metrics_by_family[spec["family_rollup"]] = spec["metrics_fn"]
        focus_by_family[spec["family_rollup"]] = (spec["focus_metric"], spec["focus_label"])

    assert seeds is not None

    stage_quotas = STAGE_SPECS[stage]["stratum_quotas"]
    if stage_quotas is not None:
        for stratum, quota in stage_quotas.items():
            observed = overall_stratum_counts.get(stratum, 0)
            if observed != quota:
                raise RuntimeError(
                    f"Stage `{stage}` expected {quota} selected items for stratum `{stratum}`, observed {observed}."
                )

    family_rollups: dict[str, Any] = {}
    for family_key in sorted(metrics_by_family.keys()):
        panel_ids = [spec["panel_id"] for spec in specs if spec["family_rollup"] == family_key]
        focus_metric, focus_label = focus_by_family[family_key]
        family_rollups[family_key] = aggregate_family(
            panel_ids=panel_ids,
            panel_payloads=slice_panels,
            metrics_fn=metrics_by_family[family_key],
            focus_metric=focus_metric,
            focus_label=focus_label,
            seeds=seeds,
            architectures=selected_methods,
        )

    return {
        "description": "Staged execution artifact over the expanded official benchmark pool.",
        "stage": stage,
        "stage_description": STAGE_SPECS[stage]["description"],
        "architectures": selected_methods,
        "n_values": N_VALUES,
        "seeds": seeds,
        "num_items": total_selected_items,
        "slice_panels": slice_panels,
        "family_rollups": family_rollups,
        "verdict": {
            "expanded_benchmark_stage_ready": True,
            "stage": stage,
            "note": f"Expanded benchmark stage `{stage}` executed over canonical expanded-pool strata.",
        },
    }


def write_stage_payload(base_dir: Path, payload: dict[str, Any]) -> tuple[Path, Path, Path]:
    stage = payload["stage"]
    json_path = base_dir / JSON_TEMPLATE.format(stage=stage)
    summary_path = base_dir / SUMMARY_TEMPLATE.format(stage=stage)
    trace_path = base_dir / TRACE_TEMPLATE.format(stage=stage)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_path.write_text(build_summary(payload), encoding="utf-8")
    trace_path.write_text(build_traces(payload), encoding="utf-8")
    return json_path, summary_path, trace_path


def main() -> None:
    stage = selected_stage()
    base_dir = Path(__file__).resolve().parent
    payload = build_stage_payload(stage)
    json_path, summary_path, trace_path = write_stage_payload(base_dir, payload)
    print(f"Wrote {json_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {trace_path}")


if __name__ == "__main__":
    main()
