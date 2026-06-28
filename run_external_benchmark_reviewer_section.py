from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import run_actual_hallucination_stress_slice as hallucination_base
import run_actual_recall_expansion as recall_base
import run_actual_summarizer_slice as actual_base
from deepseek_memory_summarizer import DeepSeekMemorySummarizer


ARCHITECTURES = ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware"]
N_VALUES = [1, 8]
DEFAULT_SEEDS = [11, 23]

JSON_PATH = "outputs/external_benchmark_reviewer_section.json"
SUMMARY_PATH = "outputs/external_benchmark_reviewer_section.md"
TRACE_PATH = "outputs/external_benchmark_reviewer_section_traces.md"

DEFAULT_PASS_PROMPT = actual_base.pass_prompt


def panel_specs() -> list[dict[str, Any]]:
    return [
        {
            "panel_id": "halumem_core_v2",
            "family_rollup": "hallucination_benchmark_section",
            "manifest_path": "benchmarks/halumem/frozen_slices/halumem_hallucination_slice_v2.json",
            "prompt_version": "benchmark_halumem_v2",
            "cache_dir_name": "external_benchmark_halumem_cache",
            "metrics_fn": hallucination_base.hallucination_metrics,
            "prompt_override": hallucination_base.stress_pass_prompt,
            "focus_metric": "false_present_rate",
            "focus_label": "false_present",
        },
        {
            "panel_id": "halumem_holdout_v1",
            "family_rollup": "hallucination_benchmark_section",
            "manifest_path": "benchmarks/halumem/frozen_slices/halumem_hallucination_holdout_slice_v1.json",
            "prompt_version": "benchmark_halumem_v2",
            "cache_dir_name": "external_benchmark_halumem_cache",
            "metrics_fn": hallucination_base.hallucination_metrics,
            "prompt_override": hallucination_base.stress_pass_prompt,
            "focus_metric": "false_present_rate",
            "focus_label": "false_present",
        },
        {
            "panel_id": "locomo_core_v2",
            "family_rollup": "benign_utility_benchmark_section",
            "manifest_path": "benchmarks/locomo/frozen_slices/locomo_benign_utility_slice_v2.json",
            "prompt_version": "benchmark_locomo_v2",
            "cache_dir_name": "external_benchmark_locomo_cache",
            "metrics_fn": recall_base.recall_metrics,
            "prompt_override": None,
            "focus_metric": "history_loss_rate",
            "focus_label": "history_loss",
        },
        {
            "panel_id": "longmemeval_direct_v1",
            "family_rollup": "benign_utility_benchmark_section",
            "manifest_path": "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_slice_v1.json",
            "prompt_version": "benchmark_locomo_v2",
            "cache_dir_name": "external_benchmark_locomo_cache",
            "metrics_fn": recall_base.recall_metrics,
            "prompt_override": None,
            "focus_metric": "history_loss_rate",
            "focus_label": "history_loss",
        },
    ]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_seeds() -> list[int]:
    seeds_env = os.environ.get("EXTERNAL_BENCHMARK_SECTION_SEEDS")
    if not seeds_env:
        return list(DEFAULT_SEEDS)
    return [int(part.strip()) for part in seeds_env.split(",") if part.strip()]


def merge_snapshot(aggregate_row: dict[str, Any], metric_row: dict[str, float]) -> dict[str, Any]:
    row = dict(aggregate_row)
    row.update(metric_row)
    return row


def merged_snapshots(
    aggregate_table: dict[str, dict[str, dict[str, Any]]],
    metric_table: dict[str, dict[str, dict[str, float]]],
) -> dict[str, dict[str, dict[str, Any]]]:
    snapshots: dict[str, dict[str, dict[str, Any]]] = {}
    for architecture in ARCHITECTURES:
        snapshots[architecture] = {}
        for n_passes in N_VALUES:
            snapshots[architecture][str(n_passes)] = merge_snapshot(
                aggregate_table[architecture][str(n_passes)],
                metric_table[architecture][str(n_passes)],
            )
    return snapshots


def build_seed_snapshots(
    records: list[dict[str, Any]],
    seeds: list[int],
    metrics_fn: Callable[[list[dict[str, Any]]], dict[str, float]],
) -> dict[str, dict[str, Any]]:
    seed_snapshots: dict[str, dict[str, Any]] = {}
    for seed in seeds:
        seed_records = [record for record in records if record["seed"] == seed]
        seed_snapshots[str(seed)] = merge_snapshot(actual_base.aggregate(seed_records), metrics_fn(seed_records))
    return seed_snapshots


def evaluate_items(
    *,
    items: list[dict[str, Any]],
    prompt_version: str,
    cache_dir_name: str,
    metrics_fn: Callable[[list[dict[str, Any]]], dict[str, float]],
    prompt_override: Callable[[dict[str, Any], int, int, str | None, list[actual_base.CompactClaim] | None], str] | None,
) -> tuple[
    dict[str, dict[str, dict[str, Any]]],
    dict[str, dict[str, dict[str, dict[str, Any]]]],
    dict[str, dict[str, dict[str, int]]],
    list[dict[str, Any]],
    list[int],
]:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    summarizer = DeepSeekMemorySummarizer(output_dir / cache_dir_name)

    old_prompt_version = actual_base.PROMPT_VERSION
    old_pass_prompt = actual_base.pass_prompt
    actual_base.PROMPT_VERSION = prompt_version
    actual_base.pass_prompt = DEFAULT_PASS_PROMPT if prompt_override is None else prompt_override

    seeds = select_seeds()
    all_records: list[dict[str, Any]] = []
    aggregate_table: dict[str, dict[str, dict[str, Any]]] = {}
    metric_table: dict[str, dict[str, dict[str, float]]] = {}
    seed_snapshots: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
    route_counts: dict[str, dict[str, dict[str, int]]] = {}

    try:
        for architecture in ARCHITECTURES:
            aggregate_table[architecture] = {}
            metric_table[architecture] = {}
            seed_snapshots[architecture] = {}
            route_counts[architecture] = {}
            for n_passes in N_VALUES:
                records = []
                for seed in seeds:
                    for item in items:
                        record = actual_base.evaluate_architecture(item, architecture, n_passes, seed, summarizer)
                        record["seed"] = seed
                        records.append(record)
                        all_records.append(record)
                aggregate_table[architecture][str(n_passes)] = actual_base.aggregate(records)
                metric_table[architecture][str(n_passes)] = metrics_fn(records)
                seed_snapshots[architecture][str(n_passes)] = build_seed_snapshots(records, seeds, metrics_fn)
                route_counts[architecture][str(n_passes)] = dict(Counter(record["route"] for record in records))
    finally:
        actual_base.PROMPT_VERSION = old_prompt_version
        actual_base.pass_prompt = old_pass_prompt

    return merged_snapshots(aggregate_table, metric_table), seed_snapshots, route_counts, all_records, seeds


def aggregate_family(
    *,
    panel_ids: list[str],
    panel_payloads: dict[str, dict[str, Any]],
    metrics_fn: Callable[[list[dict[str, Any]]], dict[str, float]],
    focus_metric: str,
    focus_label: str,
    seeds: list[int],
) -> dict[str, Any]:
    all_records = [
        record
        for panel_id in panel_ids
        for record in panel_payloads[panel_id]["records"]
    ]
    snapshots: dict[str, dict[str, Any]] = {}
    seed_snapshots: dict[str, dict[str, Any]] = {}
    route_counts: dict[str, dict[str, dict[str, int]]] = {}
    for architecture in ARCHITECTURES:
        snapshots[architecture] = {}
        seed_snapshots[architecture] = {}
        route_counts[architecture] = {}
        for n_passes in N_VALUES:
            rows = [
                record for record in all_records
                if record["architecture"] == architecture and record["n_passes"] == n_passes
            ]
            snapshots[architecture][str(n_passes)] = merge_snapshot(actual_base.aggregate(rows), metrics_fn(rows))
            seed_snapshots[architecture][str(n_passes)] = build_seed_snapshots(rows, seeds, metrics_fn)
            route_counts[architecture][str(n_passes)] = dict(Counter(record["route"] for record in rows))
    return {
        "panel_ids": panel_ids,
        "num_items": sum(panel_payloads[panel_id]["num_items"] for panel_id in panel_ids),
        "slice_ids": [item_id for panel_id in panel_ids for item_id in panel_payloads[panel_id]["slice_ids"]],
        "focus_metric": focus_metric,
        "focus_label": focus_label,
        "snapshots": snapshots,
        "seed_snapshots": seed_snapshots,
        "route_counts": route_counts,
        "records": all_records,
    }


def seed_metric_string(seed_rows: dict[str, dict[str, Any]], seeds: list[int], metric_key: str) -> str:
    return ", ".join(f"{seed}:{seed_rows[str(seed)][metric_key]:.3f}" for seed in seeds)


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# External Benchmark Reviewer Section",
        "",
        "这个 artifact 把 benchmark-first surface 从两条 starter panels 扩成了更宽的 reviewer-facing benchmark section：同一套 compaction stack 下，既有 core slices，也有 disjoint holdout / second-family expansion。",
        "",
        f"- seeds: `{payload['seeds']}`",
        f"- architectures: `{', '.join(payload['architectures'])}`",
        f"- N values: `{payload['n_values']}`",
        "",
        "## Family Rollups",
        "",
    ]
    for family_key, family in payload["family_rollups"].items():
        lines.append(f"### {family_key}")
        lines.append("")
        lines.append(f"- member_panels: `{family['panel_ids']}`")
        lines.append(f"- num_items: `{family['num_items']}`")
        if family["focus_metric"] == "false_present_rate":
            lines.append("")
            lines.append("| Method | N=1 acc | N=1 false_present | N=8 acc | N=8 false_present | N=8 raw escalation |")
            lines.append("|---|---:|---:|---:|---:|---:|")
            for architecture in ARCHITECTURES:
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
            for architecture in ARCHITECTURES:
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
            for architecture in ARCHITECTURES:
                seed_rows = family["seed_snapshots"][architecture]["8"]
                values = [seed_rows[str(seed)]["false_present_rate"] for seed in payload["seeds"]]
                lines.append(
                    f"| {architecture} | {seed_metric_string(seed_rows, payload['seeds'], 'accuracy')} | "
                    f"{seed_metric_string(seed_rows, payload['seeds'], 'false_present_rate')} | {max(values) - min(values):.3f} |"
                )
        else:
            lines.append("| Method | accuracy by seed | history_loss by seed | history_loss span |")
            lines.append("|---|---|---|---:|")
            for architecture in ARCHITECTURES:
                seed_rows = family["seed_snapshots"][architecture]["8"]
                values = [seed_rows[str(seed)]["history_loss_rate"] for seed in payload["seeds"]]
                lines.append(
                    f"| {architecture} | {seed_metric_string(seed_rows, payload['seeds'], 'accuracy')} | "
                    f"{seed_metric_string(seed_rows, payload['seeds'], 'history_loss_rate')} | {max(values) - min(values):.3f} |"
                )
        lines.append("")

    lines.extend(
        [
            "## Slice Coverage",
            "",
            "| Panel | Family Rollup | Manifest Version | Items |",
            "|---|---|---:|---:|",
        ]
    )
    for panel_id, panel in payload["slice_panels"].items():
        lines.append(
            f"| {panel_id} | {panel['family_rollup']} | {panel['slice_manifest_version']} | {panel['num_items']} |"
        )

    lines.extend(
        [
            "",
            "## Readout",
            "",
            "- HaluMem-style hallucination coverage is now broader than a single core slice because the reviewer section includes a disjoint holdout slice under the same unsupported-target contract.",
            "- Benign utility coverage is now broader than LoCoMo alone because a direct-answer LongMemEval slice sits beside the LoCoMo core slice under the same answer-retention metrics.",
            "- This still does not make the implementation fully TierMem-native, but it does make the benchmark-first surface materially less thin and less dependent on two starter slices.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(payload: dict[str, Any]) -> str:
    lines = [
        "# External Benchmark Reviewer Section Traces",
        "",
        "这些 trace 用来快速确认 reviewer section 里的新增 slices 也真的进入了同一套 compaction stack。",
        "",
    ]
    for panel_id, panel in payload["slice_panels"].items():
        lines.append(f"## {panel_id}")
        lines.append("")
        if not panel["slice_ids"]:
            continue
        item_id = panel["slice_ids"][0]
        lines.append(f"### {item_id}")
        lines.append("")
        for architecture in ARCHITECTURES:
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
                lines.append(
                    f"  N={n_passes}: probe={probe}; compact={record['compact_answer']}; final={record['answer']}; "
                    f"route={record['route']}; raw={int(record['raw_escalated'])}; llm_cost=${record['llm_cost_usd']:.4f}"
                )
            lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    selected_panel_ids = set(
        part.strip() for part in os.environ.get("EXTERNAL_BENCHMARK_SECTION_PANELS", "").split(",") if part.strip()
    )
    specs = [spec for spec in panel_specs() if not selected_panel_ids or spec["panel_id"] in selected_panel_ids]
    if not specs:
        raise RuntimeError("No panel specs selected for the reviewer section.")

    slice_panels: dict[str, dict[str, Any]] = {}
    seeds: list[int] | None = None
    metrics_by_family: dict[str, Callable[[list[dict[str, Any]]], dict[str, float]]] = {}
    focus_by_family: dict[str, tuple[str, str]] = {}

    for spec in specs:
        manifest = load_json(base_dir / spec["manifest_path"])
        snapshots, seed_snapshots, route_counts, records, panel_seeds = evaluate_items(
            items=list(manifest["items"]),
            prompt_version=spec["prompt_version"],
            cache_dir_name=spec["cache_dir_name"],
            metrics_fn=spec["metrics_fn"],
            prompt_override=spec["prompt_override"],
        )
        if seeds is None:
            seeds = panel_seeds
        elif seeds != panel_seeds:
            raise RuntimeError(f"Reviewer section seed mismatch: {seeds} vs {panel_seeds}")
        slice_panels[spec["panel_id"]] = {
            "panel_id": spec["panel_id"],
            "family_rollup": spec["family_rollup"],
            "slice_manifest_path": spec["manifest_path"],
            "slice_manifest_version": manifest.get("version"),
            "slice_ids": [item["id"] for item in manifest["items"]],
            "num_items": len(manifest["items"]),
            "snapshots": snapshots,
            "seed_snapshots": seed_snapshots,
            "route_counts": route_counts,
            "records": records,
            "focus_metric": spec["focus_metric"],
            "focus_label": spec["focus_label"],
        }
        metrics_by_family[spec["family_rollup"]] = spec["metrics_fn"]
        focus_by_family[spec["family_rollup"]] = (spec["focus_metric"], spec["focus_label"])

    assert seeds is not None

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
        )

    payload = {
        "description": "Broader reviewer-facing benchmark section spanning core plus expansion slices across HaluMem, LoCoMo, and LongMemEval-style coverage.",
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": seeds,
        "slice_panels": slice_panels,
        "family_rollups": family_rollups,
        "verdict": {
            "benchmark_reviewer_section_ready": True,
            "note": "Core plus expansion benchmark slices now produce a broader reviewer-facing benchmark section rather than only the first minimal starter panel.",
        },
    }

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    (base_dir / TRACE_PATH).write_text(build_traces(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")
    print(f"Wrote {base_dir / TRACE_PATH}")


if __name__ == "__main__":
    main()
