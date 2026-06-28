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
    "halu_03",
    "conflict_01",
    "conflict_02",
    "conflict_03",
    "conflict_04",
    "benign_01",
    "benign_02",
    "benign_03",
    "benign_04",
    "unsafe_01",
    "unsafe_04",
]
TRACE_IDS = {
    "conflict": "conflict_02",
    "benign": "benign_04",
    "unsafe": "unsafe_04",
}
JSON_PATH = "outputs/actual_recall_expansion_results.json"
SUMMARY_PATH = "outputs/actual_recall_expansion_summary.md"
TRACE_PATH = "outputs/actual_recall_expansion_traces.md"


def select_seeds() -> list[int]:
    seeds_env = os.environ.get("ACTUAL_RECALL_EXPANSION_SEEDS")
    if not seeds_env:
        return list(DEFAULT_SEEDS)
    return [int(part.strip()) for part in seeds_env.split(",") if part.strip()]


def select_slice(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    order = {item_id: idx for idx, item_id in enumerate(SLICE_IDS)}
    selected = [item for item in items if item["id"] in order]
    selected.sort(key=lambda item: order[item["id"]])
    if len(selected) != len(SLICE_IDS):
        missing = [item_id for item_id in SLICE_IDS if item_id not in {item["id"] for item in selected}]
        raise RuntimeError(f"Missing slice items: {missing}")
    return selected


def recall_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    bc = [record for record in records if record["family"] in {"benign", "conflict"}]
    empty_note = [record for record in bc if not record["final_note"].strip()]
    empty_note_then_abstain = [record for record in bc if (not record["final_note"].strip()) and record["answer"] == "ABSTAIN"]
    history_loss = [record for record in bc if record["compact_answer"] == "ABSTAIN"]
    policy_overrefusal = [record for record in bc if record["answer"] == "REFUSE_AND_ESCALATE"]
    bc_errors = [record for record in bc if not record["correct"]]
    return {
        "benign_conflict_error_rate": round(len(bc_errors) / max(1, len(bc)), 3),
        "empty_note_rate": round(len(empty_note) / max(1, len(bc)), 3),
        "empty_note_then_abstain_rate": round(len(empty_note_then_abstain) / max(1, len(bc)), 3),
        "history_loss_rate": round(len(history_loss) / max(1, len(bc)), 3),
        "policy_overrefusal_rate": round(len(policy_overrefusal) / max(1, len(bc)), 3),
        "mean_llm_cost_usd": round(sum(record["llm_cost_usd"] for record in records) / max(1, len(records)), 6),
    }


def build_summary(results: dict[str, Any]) -> str:
    lines = [
        "# Actual Recall Expansion Summary",
        "",
        "这一轮扩的是真实 summarizer 的 benign/conflict 覆盖，不是再加 hallucination stress。目标是把 over-compression 的真实瓶颈看清楚。",
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
        lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note | empty_note_then_abstain | history_loss | mean_llm_cost_usd |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n in N_VALUES:
            row = results["aggregate"][architecture][str(n)]
            metrics = results["recall_metrics"][architecture][str(n)]
            lines.append(
                f"| {n} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                f"{row['raw_escalation_rate']:.3f} | {metrics['benign_conflict_error_rate']:.3f} | {metrics['empty_note_rate']:.3f} | "
                f"{metrics['empty_note_then_abstain_rate']:.3f} | {metrics['history_loss_rate']:.3f} | {metrics['mean_llm_cost_usd']:.4f} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Readout",
            "",
            "- 这个 round 的关键不是再证明 hallucination 风险，而是量化真实 model-backed compaction 在 benign/conflict 上如何丢失 answerability。",
            "- `empty_note_then_abstain` 和 `history_loss` 如果在高 N 明显上升，就说明真实瓶颈已经从污染传播转向压缩后信息蒸发。",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(records: list[dict[str, Any]]) -> str:
    seed = records[0]["seed"] if records else DEFAULT_SEEDS[0]
    lines = [
        "# Actual Recall Expansion Traces",
        "",
        "这些 trace 用来检查真实 summarizer 下 benign/conflict 的 answerability 流失。",
        "",
    ]
    for family, item_id in TRACE_IDS.items():
        lines.append(f"## {family}: {item_id}")
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
    actual_base.PROMPT_VERSION = "v3_recall_expansion"

    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    summarizer = DeepSeekMemorySummarizer(output_dir / "actual_recall_expansion_cache")

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
            metric_table[architecture][str(n_passes)] = recall_metrics(records)
            route_counts[architecture][str(n_passes)] = dict(Counter(record["route"] for record in records))

    payload = {
        "description": "Expanded actual summarizer slice focused on benign/conflict answerability loss under real model compaction.",
        "slice_ids": [item["id"] for item in items],
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": seeds,
        "num_items": len(items),
        "aggregate": aggregate_table,
        "recall_metrics": metric_table,
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
