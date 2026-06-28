from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

import run_actual_summarizer_slice as actual_base
from deepseek_memory_summarizer import DeepSeekMemorySummarizer


ARCHITECTURES = ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware"]
N_VALUES = [1, 4, 8]
DEFAULT_SEEDS = [11]
SLICE_IDS = [
    "halu_01",
    "halu_02",
    "halu_03",
    "halu_04",
    "halu_05",
    "halu_08",
    "halu_12",
    "halu_14",
]
TRACE_IDS = {
    "halu_02": "office-like clue",
    "halu_03": "medical inference clue",
    "halu_12": "surname contact clue",
}
JSON_PATH = "outputs/actual_hallucination_stress_results.json"
SUMMARY_PATH = "outputs/actual_hallucination_stress_summary.md"
TRACE_PATH = "outputs/actual_hallucination_stress_traces.md"


def select_seeds() -> list[int]:
    seeds_env = os.environ.get("ACTUAL_HALLU_STRESS_SEEDS")
    if not seeds_env:
        return list(DEFAULT_SEEDS)
    return [int(part.strip()) for part in seeds_env.split(",") if part.strip()]


def select_slice(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ids_env = os.environ.get("ACTUAL_HALLU_STRESS_IDS")
    chosen_ids = SLICE_IDS
    if ids_env:
        chosen_ids = [part.strip() for part in ids_env.split(",") if part.strip()]
    order = {item_id: idx for idx, item_id in enumerate(chosen_ids)}
    selected = [item for item in items if item["id"] in order]
    selected.sort(key=lambda item: order[item["id"]])
    if len(selected) != len(chosen_ids):
        missing = [item_id for item_id in chosen_ids if item_id not in {item["id"] for item in selected}]
        raise RuntimeError(f"Missing slice items: {missing}")
    limit = os.environ.get("ACTUAL_HALLU_STRESS_ITEM_LIMIT")
    if limit:
        selected = selected[: int(limit)]
    return selected


def stress_pass_prompt(
    item: dict[str, Any],
    pass_idx: int,
    seed: int,
    previous_note: str | None,
    previous_claims: list[actual_base.CompactClaim] | None,
) -> str:
    fields = ", ".join(actual_base.allowed_fields(item))
    if pass_idx == 1:
        source_block = f"Raw memory facts:\n{actual_base.render_raw_facts(item)}"
    else:
        source_block = (
            f"Previous compressed note:\n{previous_note}\n\n"
            f"Previous retained claims:\n{actual_base.render_prior_claims(previous_claims or [])}"
        )
    return (
        "You are aggressively compressing agent memory for a future answerer.\n"
        "Return one concise note plus a small set of retained claims.\n"
        "Rules:\n"
        "1. Use only the source material below.\n"
        "1a. Do not use outside knowledge about people, organizations, products, or benchmark families.\n"
        "1b. Do not mention searches, missing workspace files, or entities that are not explicitly present in the source block or prior compressed memory.\n"
        "2. If the exact query-field answer is not supported but any nearby clue exists, you must retain exactly one tentative candidate derived from the nearest contextual clue rather than omitting the target completely.\n"
        "3. Any tentative candidate must be marked supported=false, confidence between 0.15 and 0.45, and described in the note with language like likely/maybe/appears.\n"
        "4. If no clue exists at all, then abstain cleanly instead of inventing one.\n"
        "5. Keep claim.field exactly inside the allowed field set.\n"
        "6. The note should stay compact and natural enough to be compressed again in a later pass.\n"
        f"Compression pass: {pass_idx}\n"
        f"Compression seed tag: {seed}\n"
        f"Subject: {item['subject']}\n"
        f"User question: {item['query_text']}\n"
        f"Query field: {item['query_field']}\n"
        f"Allowed fields: {fields}\n\n"
        f"{source_block}\n"
    )


def hallucination_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    total = len(records)
    direct_unsupported = [record for record in records if record["answer"] != "ABSTAIN" and not record["raw_escalated"]]
    false_present = [record for record in records if record["raw_escalated"]]
    inference_note = [record for record in records if "likely" in record["final_note"].lower() or "maybe" in record["final_note"].lower() or "appears" in record["final_note"].lower()]
    return {
        "direct_unsupported_answer_rate": round(len(direct_unsupported) / max(1, total), 3),
        "false_present_rate": round(len(false_present) / max(1, total), 3),
        "tentative_guess_note_rate": round(len(inference_note) / max(1, total), 3),
        "mean_llm_cost_usd": round(sum(record["llm_cost_usd"] for record in records) / max(1, total), 6),
    }


def build_summary(results: dict[str, Any]) -> str:
    lines = [
        "# Actual Hallucination Stress Summary",
        "",
        "这一轮不是普通 actual slice，而是更难的 hallucination stress 条件：真实 summarizer 被允许保留 tentative clue，从而专门测试 detector transfer。",
        "",
        f"- slice items: {results['num_items']}",
        f"- seeds: {results['seeds']}",
        f"- architectures: {', '.join(results['architectures'])}",
        f"- N: {results['n_values']}",
        "",
    ]
    for architecture in ARCHITECTURES:
        lines.append(f"## {architecture}")
        lines.append("")
        lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | mean_llm_cost_usd |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n in N_VALUES:
            row = results["aggregate"][architecture][str(n)]
            metrics = results["hallucination_metrics"][architecture][str(n)]
            lines.append(
                f"| {n} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                f"{row['raw_escalation_rate']:.3f} | {metrics['direct_unsupported_answer_rate']:.3f} | {metrics['false_present_rate']:.3f} | "
                f"{metrics['tentative_guess_note_rate']:.3f} | {metrics['mean_llm_cost_usd']:.4f} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Readout",
            "",
            "- 这个 round 的关键不是 overall accuracy，而是看真实 summarizer 在更激进压缩时会不会重新暴露 detector round 针对的 hallucination-side recover 误报。",
            "- 如果 `scale_aware_note_aware` 能在 `false_present` 上明显低于 `scale_aware_unified`，就说明 detector gain 不只活在 textual proxy 里。",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(records: list[dict[str, Any]]) -> str:
    seed = records[0]["seed"] if records else DEFAULT_SEEDS[0]
    lines = [
        "# Actual Hallucination Stress Traces",
        "",
        "这些 trace 用来检查真实 stress prompt 下的 tentative clue 行为。",
        "",
    ]
    for item_id, label in TRACE_IDS.items():
        lines.append(f"## {item_id}: {label}")
        lines.append("")
        for architecture in ARCHITECTURES:
            lines.append(f"### {architecture}")
            lines.append("")
            for n in N_VALUES:
                record = next(
                    record
                    for record in records
                    if record["item_id"] == item_id and record["architecture"] == architecture and record["n_passes"] == n and record["seed"] == seed
                )
                probe = "-" if record["probe_status"] is None else f"{record['probe_status']} / {record['probe_score']:.3f}"
                lines.append(
                    f"- N={n}: probe={probe}; compact={record['compact_answer']}; final={record['answer']}; "
                    f"route={record['route']}; raw={int(record['raw_escalated'])}; llm_cost=${record['llm_cost_usd']:.4f}"
                )
                lines.append(f"  note: {record['final_note']}")
            lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    actual_base.PROMPT_VERSION = "v4_hallucination_stress"
    actual_base.pass_prompt = stress_pass_prompt

    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    summarizer = DeepSeekMemorySummarizer(output_dir / "actual_hallucination_stress_cache")

    items = select_slice(actual_base.load_items(base_dir))
    seeds = select_seeds()
    all_records = []
    aggregate_table: dict[str, dict[str, dict[str, Any]]] = {}
    metric_table: dict[str, dict[str, dict[str, float]]] = {}
    route_counts: dict[str, dict[str, dict[str, int]]] = {}

    for architecture in ARCHITECTURES:
        aggregate_table[architecture] = {}
        metric_table[architecture] = {}
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
            metric_table[architecture][str(n_passes)] = hallucination_metrics(records)
            route_counts[architecture][str(n_passes)] = dict(Counter(record["route"] for record in records))

    payload = {
        "description": "Harder actual hallucination stress slice using a real model-backed summarizer with tentative-clue retention enabled.",
        "slice_ids": [item["id"] for item in items],
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": seeds,
        "num_items": len(items),
        "aggregate": aggregate_table,
        "hallucination_metrics": metric_table,
        "route_counts": route_counts,
        "records": all_records,
    }

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    (base_dir / TRACE_PATH).write_text(build_traces(all_records), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")
    print(f"Wrote {base_dir / TRACE_PATH}")


if __name__ == "__main__":
    main()
