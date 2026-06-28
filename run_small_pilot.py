from __future__ import annotations

import csv
import json
from pathlib import Path

from pilot_core import aggregate, evaluate_item, load_items


ARCHITECTURES = [
    "raw_only",
    "summary_only",
    "tiered",
    "adaptive_tiered",
    "adaptive_guarded",
    "risk_first",
    "utility_first",
    "utility_calibrated",
    "small_n_hybrid",
    "scale_aware_unified",
]
N_VALUES = [0, 1, 2, 4, 8]
SEEDS = [11, 23, 47, 89, 131]


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    items = load_items(base_dir)
    all_records = []
    aggregate_table: dict[str, dict[str, dict]] = {}

    for architecture in ARCHITECTURES:
        aggregate_table[architecture] = {}
        for n_passes in N_VALUES:
            records = []
            for seed in SEEDS:
                for item in items:
                    record = evaluate_item(item, architecture, n_passes, seed)
                    record["seed"] = seed
                    records.append(record)
                    all_records.append(record)
            aggregate_table[architecture][str(n_passes)] = aggregate(records)

    results = {
        "description": "Controlled synthetic pre-pilot for iterative memory consolidation.",
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": SEEDS,
        "num_items": len(items),
        "aggregate": aggregate_table,
        "records": all_records,
    }

    results_path = output_dir / "small_pilot_results.json"
    with results_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    summary_path = output_dir / "small_pilot_summary.md"
    summary_path.write_text(build_summary(results), encoding="utf-8")

    csv_path = output_dir / "aggregate_rows.csv"
    write_csv(results, csv_path)

    trace_path = output_dir / "exemplar_traces.md"
    trace_path.write_text(build_exemplar_traces(results), encoding="utf-8")

    print(f"Wrote {results_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {trace_path}")


def write_csv(results: dict, csv_path: Path) -> None:
    fieldnames = [
        "architecture",
        "n",
        "accuracy",
        "unsupported_answer_rate",
        "unsafe_answer_rate",
        "conflict_answer_rate",
        "propagation_rate",
        "unsupported_new_memory_rate",
        "unsafe_retention_rate",
        "conflict_merge_rate",
        "benign_overcompression_rate",
        "latent_bad_memory_rate",
        "residual_bad_memory_rate",
        "shielded_bad_memory_rate",
        "cleaned_bad_memory_rate",
        "raw_escalation_rate",
        "mean_cost",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for architecture in results["architectures"]:
            for n in results["n_values"]:
                row = results["aggregate"][architecture][str(n)]
                writer.writerow(
                    {
                        "architecture": architecture,
                        "n": n,
                        "accuracy": row["accuracy"],
                        "unsupported_answer_rate": row["unsupported_answer_rate"],
                        "unsafe_answer_rate": row["unsafe_answer_rate"],
                        "conflict_answer_rate": row["conflict_answer_rate"],
                        "propagation_rate": row["propagation_rate"],
                        "unsupported_new_memory_rate": row["unsupported_new_memory_rate"],
                        "unsafe_retention_rate": row["unsafe_retention_rate"],
                        "conflict_merge_rate": row["conflict_merge_rate"],
                        "benign_overcompression_rate": row["benign_overcompression_rate"],
                        "latent_bad_memory_rate": row["latent_bad_memory_rate"],
                        "residual_bad_memory_rate": row["residual_bad_memory_rate"],
                        "shielded_bad_memory_rate": row["shielded_bad_memory_rate"],
                        "cleaned_bad_memory_rate": row["cleaned_bad_memory_rate"],
                        "raw_escalation_rate": row["raw_escalation_rate"],
                        "mean_cost": row["mean_cost"],
                    }
                )


def build_summary(results: dict) -> str:
    lines = [
        "# Small Pilot Summary",
        "",
        "这是一个受控合成 pre-pilot，不是正式 benchmark 结论。",
        "",
        f"- items: {results['num_items']}",
        f"- seeds: {len(results['seeds'])}",
        f"- architectures: {', '.join(results['architectures'])}",
        f"- N: {results['n_values']}",
        "",
        "## Aggregate Readout",
        "",
    ]
    for architecture in results["architectures"]:
        lines.append(f"### {architecture}")
        lines.append("")
        lines.append("| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n in results["n_values"]:
            row = results["aggregate"][architecture][str(n)]
            lines.append(
                f"| {n} | {row['accuracy']:.3f} | {row['unsupported_answer_rate']:.3f} | "
                f"{row['unsafe_answer_rate']:.3f} | {row['conflict_answer_rate']:.3f} | {row['propagation_rate']:.3f} | "
                f"{row['unsupported_new_memory_rate']:.3f} | {row['unsafe_retention_rate']:.3f} | "
                f"{row['conflict_merge_rate']:.3f} | {row['benign_overcompression_rate']:.3f} | "
                f"{row['latent_bad_memory_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                f"{row['shielded_bad_memory_rate']:.3f} | {row['cleaned_bad_memory_rate']:.3f} | "
                f"{row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} |"
            )
        lines.append("")
        lines.append("Family breakdown:")
        lines.append("")
        lines.append("| family | accuracy | propagation | raw_escalation |")
        lines.append("|---|---:|---:|---:|")
        family_row = results["aggregate"][architecture][str(results["n_values"][-1])]["by_family"]
        for family, metrics in family_row.items():
            lines.append(
                f"| {family} | {metrics['accuracy']:.3f} | {metrics['propagation_rate']:.3f} | {metrics['raw_escalation_rate']:.3f} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Candidate Pareto Frontier",
            "",
        ]
    )
    frontier = compute_frontier(results)
    lines.append("| architecture | N | accuracy | propagation | mean_cost |")
    lines.append("|---|---:|---:|---:|---:|")
    for row in frontier:
        lines.append(
            f"| {row['architecture']} | {row['n']} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['mean_cost']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Matched-N Best Non-Raw Policy",
            "",
            "这个表只在相同 `N` 下比较非 `raw_only` 条件：先选最低 propagation，再选最高 accuracy、最低 residual contamination、最低 cost。",
            "",
        ]
    )
    matched_winners = compute_matched_n_winners(results)
    lines.append("| N | architecture | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for row in matched_winners:
        lines.append(
            f"| {row['n']} | {row['architecture']} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | "
            f"{row['residual_bad_memory_rate']:.3f} | {row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## What To Look For",
            "",
            "- `summary_only` 的 unsupported / unsafe / conflict 风险是否随 `N` 上升。",
            "- `tiered` 是否明显压低 propagation-to-answer，同时带来 raw escalation 成本。",
            "- `risk_first` / `utility_first` 能不能通过 scrub policy 把 latent contamination 变成更低的 residual contamination。",
            "- `utility_calibrated` 能不能通过 detector calibration 修补 `utility_first` 在低 N 的 recall miss，同时保留 cleanup policy 的低 residual contamination。",
            "- `scale_aware_unified` 能不能把 `small_n_hybrid` 的低-N 优势和 `utility_calibrated` 的高-N 优势拼成一个全 sweep 结构化策略。",
            "- `raw_only` 是否提供接近 risk floor 的上界。",
            "",
            "## Caveat",
            "",
            "这个结果只能说明当前实验 framing 和指标在小样本合成环境下是可运行的，不代表真实模型一定表现相同。",
        ]
    )
    return "\n".join(lines) + "\n"


def compute_frontier(results: dict) -> list[dict]:
    rows = []
    for architecture in results["architectures"]:
        for n in results["n_values"]:
            row = dict(results["aggregate"][architecture][str(n)])
            row["architecture"] = architecture
            row["n"] = n
            rows.append(row)

    def dominates(a: dict, b: dict) -> bool:
        return (
            a["accuracy"] >= b["accuracy"]
            and a["propagation_rate"] <= b["propagation_rate"]
            and a["mean_cost"] <= b["mean_cost"]
            and (
                a["accuracy"] > b["accuracy"]
                or a["propagation_rate"] < b["propagation_rate"]
                or a["mean_cost"] < b["mean_cost"]
            )
        )

    frontier = []
    for candidate in rows:
        if not any(dominates(other, candidate) for other in rows if other is not candidate):
            frontier.append(candidate)
    frontier.sort(key=lambda r: (r["propagation_rate"], r["mean_cost"], -r["accuracy"]))
    return frontier


def compute_matched_n_winners(results: dict) -> list[dict]:
    winners = []
    for n in results["n_values"]:
        rows = []
        for architecture in results["architectures"]:
            if architecture == "raw_only":
                continue
            row = dict(results["aggregate"][architecture][str(n)])
            row["architecture"] = architecture
            row["n"] = n
            rows.append(row)
        rows.sort(
            key=lambda r: (
                r["propagation_rate"],
                -r["accuracy"],
                r["residual_bad_memory_rate"],
                r["mean_cost"],
            )
        )
        winners.append(rows[0])
    return winners


def build_exemplar_traces(results: dict) -> str:
    families = ["hallucination", "conflict", "unsafe", "benign"]
    chosen_by_family: dict[str, str] = {}
    for family in families:
        candidates = [
            r for r in results["records"]
            if r["family"] == family and r["architecture"] == "summary_only" and r["n_passes"] == 8 and r["seed"] == results["seeds"][0]
        ]
        if candidates:
            candidates.sort(key=lambda r: (not r["propagation"], r["item_id"]))
            chosen_by_family[family] = candidates[0]["item_id"]

    lines = [
        "# Exemplar Traces",
        "",
        "这些 trace 用来辅助 review，不是主表。",
        "",
    ]
    show_architectures = [
        "summary_only",
        "tiered",
        "adaptive_tiered",
        "adaptive_guarded",
        "risk_first",
        "utility_first",
        "utility_calibrated",
        "small_n_hybrid",
        "scale_aware_unified",
    ]
    show_n = [0, 2, 8]
    for family in families:
        item_id = chosen_by_family.get(family)
        if not item_id:
            continue
        lines.append(f"## {family}: {item_id}")
        lines.append("")
        for architecture in show_architectures:
            lines.append(f"### {architecture}")
            lines.append("")
            lines.append("| N | probe | probe_score | latent_answer | compact_answer | final_answer | gold | correct | route | raw_escalated | cost |")
            lines.append("|---|---|---:|---|---|---|---|---:|---|---:|---:|")
            for n in show_n:
                record = next(
                    r for r in results["records"]
                    if r["item_id"] == item_id and r["architecture"] == architecture and r["n_passes"] == n and r["seed"] == results["seeds"][0]
                )
                probe_score = "-" if record["probe_score"] is None else f"{record['probe_score']:.3f}"
                lines.append(
                    f"| {n} | {record['probe_status'] or '-'} | "
                    f"{probe_score} | "
                    f"{record['latent_compact_answer']} | {record['compact_answer']} | {record['answer']} | {record['gold']} | "
                    f"{int(record['correct'])} | {record['route']} | {int(record['raw_escalated'])} | {record['estimated_cost']:.3f} |"
                )
            lines.append("")
            lines.append("Representative claims at highest N:")
            lines.append("")
            high_record = next(
                r for r in results["records"]
                if r["item_id"] == item_id and r["architecture"] == architecture and r["n_passes"] == show_n[-1] and r["seed"] == results["seeds"][0]
            )
            if high_record["probe_status"] is not None:
                lines.append(
                    f"Probe at highest N: status=`{high_record['probe_status']}`, score=`{high_record['probe_score']:.3f}`, "
                    f"raw_target_exists=`{int(high_record['probe_raw_target_exists'])}`, "
                    f"target_noise=`{int(high_record['probe_target_noise'])}`, "
                    f"history_conflict=`{int(high_record['probe_history_conflict'])}`."
                )
                lines.append("")
            lines.append("Latent compact claims:")
            lines.append("")
            lines.append("| field | value | supported | unsafe | conf | current | conflict |")
            lines.append("|---|---|---:|---:|---:|---:|---|")
            for claim in high_record["latent_claim_summary"]:
                lines.append(
                    f"| {claim['field']} | {claim['value']} | {int(claim['supported'])} | {int(claim['unsafe'])} | "
                    f"{claim['confidence']:.3f} | {int(claim['current'])} | {claim['conflict_state']} |"
                )
            lines.append("")
            lines.append("Post-policy claims:")
            lines.append("")
            lines.append("| field | value | supported | unsafe | conf | conflict |")
            lines.append("|---|---|---:|---:|---:|---|")
            for claim in high_record["claim_summary"]:
                lines.append(
                    f"| {claim['field']} | {claim['value']} | {int(claim['supported'])} | {int(claim['unsafe'])} | {claim['confidence']:.3f} | {claim['conflict_state']} |"
                )
            lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
