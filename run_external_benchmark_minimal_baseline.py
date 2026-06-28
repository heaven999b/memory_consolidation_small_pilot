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
N_VALUES = [1, 4, 8]
DEFAULT_SEEDS = [11, 23]

HALUMEM_SLICE_PATH = "benchmarks/halumem/frozen_slices/halumem_hallucination_slice_v2.json"
LOCOMO_SLICE_PATH = "benchmarks/locomo/frozen_slices/locomo_benign_utility_slice_v2.json"

JSON_PATH = "outputs/external_benchmark_minimal_baseline.json"
SUMMARY_PATH = "outputs/external_benchmark_minimal_baseline.md"
TRACE_PATH = "outputs/external_benchmark_minimal_baseline_traces.md"

DEFAULT_PASS_PROMPT = actual_base.pass_prompt


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_seeds() -> list[int]:
    seeds_env = os.environ.get("EXTERNAL_BENCHMARK_SEEDS")
    if not seeds_env:
        return list(DEFAULT_SEEDS)
    return [int(part.strip()) for part in seeds_env.split(",") if part.strip()]


def maybe_limit(items: list[dict[str, Any]], env_var: str) -> list[dict[str, Any]]:
    limit = os.environ.get(env_var)
    if not limit:
        return items
    return items[: int(limit)]


def merge_snapshot(
    aggregate_row: dict[str, Any],
    metric_row: dict[str, float],
) -> dict[str, Any]:
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


def evaluate_panel(
    *,
    items: list[dict[str, Any]],
    prompt_version: str,
    cache_dir_name: str,
    metrics_fn: Callable[[list[dict[str, Any]]], dict[str, float]],
    prompt_override: Callable[[dict[str, Any], int, int, str | None, list[actual_base.CompactClaim] | None], str] | None = None,
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


def seed_metric_string(seed_rows: dict[str, dict[str, Any]], seeds: list[int], metric_key: str) -> str:
    return ", ".join(f"{seed}:{seed_rows[str(seed)][metric_key]:.3f}" for seed in seeds)


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# External Benchmark Minimal Baseline",
        "",
        "这个 artifact 把两条 frozen external benchmark slice 真正跑进现有 baseline trio / unified stack，而不是只停在 adapter-ready 状态。",
        "",
        f"- seeds: `{payload['seeds']}`",
        f"- architectures: `{', '.join(payload['architectures'])}`",
        f"- N values: `{payload['n_values']}`",
        "",
    ]
    for panel_name, panel in payload["benchmark_panels"].items():
        lines.append(f"## {panel_name}")
        lines.append("")
        lines.append(f"- slice_ids: `{panel['slice_ids']}`")
        lines.append(f"- slice_manifest_version: `{panel['slice_manifest_version']}`")
        lines.append(f"- num_items: `{panel['num_items']}`")
        if panel_name == "halumem_hallucination":
            lines.append("")
            lines.append("| Method | N=1 acc | N=1 false_present | N=1 raw escalation | N=8 acc | N=8 false_present | N=8 raw escalation |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|")
            for architecture in ARCHITECTURES:
                row1 = panel["snapshots"][architecture]["1"]
                row8 = panel["snapshots"][architecture]["8"]
                lines.append(
                    f"| {architecture} | {row1['accuracy']:.3f} | {row1['false_present_rate']:.3f} | {row1['raw_escalation_rate']:.3f} | "
                    f"{row8['accuracy']:.3f} | {row8['false_present_rate']:.3f} | {row8['raw_escalation_rate']:.3f} |"
                )
        else:
            lines.append("")
            lines.append("| Method | N=1 acc | N=1 history_loss | N=1 raw escalation | N=8 acc | N=8 history_loss | N=8 empty-note-abstain |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|")
            for architecture in ARCHITECTURES:
                row1 = panel["snapshots"][architecture]["1"]
                row8 = panel["snapshots"][architecture]["8"]
                lines.append(
                    f"| {architecture} | {row1['accuracy']:.3f} | {row1['history_loss_rate']:.3f} | {row1['raw_escalation_rate']:.3f} | "
                    f"{row8['accuracy']:.3f} | {row8['history_loss_rate']:.3f} | {row8['empty_note_then_abstain_rate']:.3f} |"
                )
        lines.append("")
        lines.append("### Seed Stability (N=8)")
        lines.append("")
        if panel_name == "halumem_hallucination":
            lines.append("| Method | accuracy by seed | false_present by seed | false_present span |")
            lines.append("|---|---|---|---:|")
            for architecture in ARCHITECTURES:
                seed_rows = panel["seed_snapshots"][architecture]["8"]
                values = [seed_rows[str(seed)]["false_present_rate"] for seed in payload["seeds"]]
                lines.append(
                    f"| {architecture} | {seed_metric_string(seed_rows, payload['seeds'], 'accuracy')} | "
                    f"{seed_metric_string(seed_rows, payload['seeds'], 'false_present_rate')} | {max(values) - min(values):.3f} |"
                )
        else:
            lines.append("| Method | accuracy by seed | history_loss by seed | history_loss span |")
            lines.append("|---|---|---|---:|")
            for architecture in ARCHITECTURES:
                seed_rows = panel["seed_snapshots"][architecture]["8"]
                values = [seed_rows[str(seed)]["history_loss_rate"] for seed in payload["seeds"]]
                lines.append(
                    f"| {architecture} | {seed_metric_string(seed_rows, payload['seeds'], 'accuracy')} | "
                    f"{seed_metric_string(seed_rows, payload['seeds'], 'history_loss_rate')} | {max(values) - min(values):.3f} |"
                )
        lines.append("")

    lines.extend(
        [
            "## Readout",
            "",
            "- HaluMem-style slice now measures benchmark-grounded unsupported-target false-present behavior under the real summarizer loop.",
            "- LoCoMo slice now measures benchmark-grounded benign answerability / history-loss behavior under the same compaction stack.",
            "- Multi-seed seed snapshots make it easier to tell whether the first benchmark readout is structurally stable or just a lucky single-seed slice.",
            "- This is still a minimal benchmark panel, not a full TierMem-style primary benchmark base, but it is materially stronger than an adapter-only placeholder.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(payload: dict[str, Any]) -> str:
    lines = [
        "# External Benchmark Minimal Baseline Traces",
        "",
        "这些 trace 用来快速检查 frozen benchmark slice 是否真的进入了现有 compaction / detector stack。",
        "",
    ]
    for panel_name, panel in payload["benchmark_panels"].items():
        lines.append(f"## {panel_name}")
        lines.append("")
        trace_ids = panel["slice_ids"][:2]
        for item_id in trace_ids:
            lines.append(f"### {item_id}")
            lines.append("")
            for architecture in ARCHITECTURES:
                lines.append(f"- `{architecture}`")
                for n_passes in [1, 8]:
                    record = next(
                        row
                        for row in panel["records"]
                        if row["item_id"] == item_id and row["architecture"] == architecture and row["n_passes"] == n_passes and row["seed"] == payload["seeds"][0]
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
    halumem_manifest = load_json(base_dir / HALUMEM_SLICE_PATH)
    locomo_manifest = load_json(base_dir / LOCOMO_SLICE_PATH)

    halumem_items = maybe_limit(list(halumem_manifest["items"]), "EXTERNAL_BENCHMARK_HALUMEM_LIMIT")
    locomo_items = maybe_limit(list(locomo_manifest["items"]), "EXTERNAL_BENCHMARK_LOCOMO_LIMIT")

    halu_snapshots, halu_seed_snapshots, halu_routes, halu_records, seeds = evaluate_panel(
        items=halumem_items,
        prompt_version="benchmark_halumem_v2",
        cache_dir_name="external_benchmark_halumem_cache",
        metrics_fn=hallucination_base.hallucination_metrics,
        prompt_override=hallucination_base.stress_pass_prompt,
    )
    locomo_snapshots, locomo_seed_snapshots, locomo_routes, locomo_records, _ = evaluate_panel(
        items=locomo_items,
        prompt_version="benchmark_locomo_v2",
        cache_dir_name="external_benchmark_locomo_cache",
        metrics_fn=recall_base.recall_metrics,
        prompt_override=None,
    )

    payload = {
        "description": "Minimal benchmark-grounded baseline panel over one frozen HaluMem-style hallucination slice and one frozen LoCoMo benign-utility slice.",
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": seeds,
        "benchmark_panels": {
            "halumem_hallucination": {
                "slice_manifest_path": HALUMEM_SLICE_PATH,
                "slice_manifest_version": halumem_manifest.get("version"),
                "slice_ids": [item["id"] for item in halumem_items],
                "num_items": len(halumem_items),
                "snapshots": halu_snapshots,
                "seed_snapshots": halu_seed_snapshots,
                "route_counts": halu_routes,
                "records": halu_records,
            },
            "locomo_benign_utility": {
                "slice_manifest_path": LOCOMO_SLICE_PATH,
                "slice_manifest_version": locomo_manifest.get("version"),
                "slice_ids": [item["id"] for item in locomo_items],
                "num_items": len(locomo_items),
                "snapshots": locomo_snapshots,
                "seed_snapshots": locomo_seed_snapshots,
                "route_counts": locomo_routes,
                "records": locomo_records,
            },
        },
        "verdict": {
            "minimal_benchmark_grounded_panel_ready": True,
            "note": "Both frozen external benchmark slices were executed through the model-backed compaction stack with multi-seed snapshots and produced reviewer-facing benchmark-grounded panel rows.",
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
