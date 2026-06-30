from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


JSON_PATH = "outputs/psu_recall_main_panel.json"
SUMMARY_PATH = "outputs/psu_recall_main_panel.md"


def load_json(base_dir: Path, relative_path: str) -> dict[str, Any]:
    return json.loads((base_dir / relative_path).read_text(encoding="utf-8"))


def select_records(records: list[dict[str, Any]], **filters: Any) -> list[dict[str, Any]]:
    selected = []
    for record in records:
        keep = True
        for key, expected in filters.items():
            if record.get(key) != expected:
                keep = False
                break
        if keep:
            selected.append(record)
    return selected


def recall_panel_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    total = len(records)
    bc = [record for record in records if record["family"] in {"benign", "conflict"}]
    unsafe = [record for record in records if record["family"] == "unsafe"]
    hallucination = [record for record in records if record["family"] == "hallucination"]
    history_loss = [record for record in bc if record["compact_answer"] == "ABSTAIN"]
    empty_note_then_abstain = [
        record for record in bc if (not record["final_note"].strip()) and record["answer"] == "ABSTAIN"
    ]
    benign_conflict_errors = [record for record in bc if not record["correct"]]
    unsafe_errors = [record for record in unsafe if not record["correct"]]
    placeholder_answers = [record for record in hallucination if record.get("placeholder_answer")]
    carry_records = [record for record in records if record.get("carry_forward_events", 0) > 0]
    return {
        "count": total,
        "accuracy": round(sum(record["correct"] for record in records) / max(1, total), 3),
        "propagation": round(sum(record["propagation"] for record in records) / max(1, total), 3),
        "raw_escalation": round(sum(record["raw_escalated"] for record in records) / max(1, total), 3),
        "history_loss": round(len(history_loss) / max(1, len(bc)), 3),
        "empty_note_then_abstain": round(len(empty_note_then_abstain) / max(1, len(bc)), 3),
        "benign_conflict_error": round(len(benign_conflict_errors) / max(1, len(bc)), 3),
        "unsafe_error": round(len(unsafe_errors) / max(1, len(unsafe)), 3),
        "hallucination_placeholder": round(len(placeholder_answers) / max(1, len(hallucination)), 3),
        "carry_forward_record": round(len(carry_records) / max(1, total), 3),
        "mean_llm_cost_usd": round(sum(record.get("llm_cost_usd", 0.0) for record in records) / max(1, total), 6),
    }


def pair_records(
    baseline: list[dict[str, Any]],
    treatment: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    baseline_map = {(record["item_id"], record["seed"]): record for record in baseline}
    treatment_map = {(record["item_id"], record["seed"]): record for record in treatment}
    shared = sorted(set(baseline_map) & set(treatment_map))
    return [(baseline_map[key], treatment_map[key]) for key in shared]


def paired_delta(
    baseline: list[dict[str, Any]],
    treatment: list[dict[str, Any]],
    metric_fn: Callable[[dict[str, Any]], float],
    *,
    harmful_metric: bool,
) -> dict[str, Any]:
    pairs = pair_records(baseline, treatment)
    deltas = []
    wins = 0
    losses = 0
    for base_record, treat_record in pairs:
        base_value = float(metric_fn(base_record))
        treat_value = float(metric_fn(treat_record))
        delta = base_value - treat_value if harmful_metric else treat_value - base_value
        deltas.append(delta)
        if delta > 0:
            wins += 1
        elif delta < 0:
            losses += 1
    mean_delta = round(sum(deltas) / max(1, len(deltas)), 4)
    return {
        "pair_count": len(pairs),
        "mean_delta": mean_delta,
        "wins": wins,
        "losses": losses,
        "ties": max(0, len(pairs) - wins - losses),
    }


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    recall = load_json(base_dir, "outputs/actual_recall_expansion_results.json")
    carry = load_json(base_dir, "outputs/actual_carry_forward_results.json")

    method_specs = [
        ("summary_only", "summary_only", None),
        ("tiered", "tiered", None),
        ("scale_aware_unified", "scale_aware_unified", None),
        ("scale_aware_note_aware", "scale_aware_note_aware", None),
        ("psu_no_carry", "scale_aware_note_aware", "tiny_placeholder_hardened_scaffold"),
        ("psu", "scale_aware_note_aware", "tiny_carry_forward_scaffold"),
    ]

    panel_rows: dict[str, list[dict[str, Any]]] = {}
    for n_passes in [4, 8]:
        rows = []
        for label, architecture, intervention in method_specs:
            if intervention is None:
                records = select_records(recall["records"], architecture=architecture, n_passes=n_passes)
            else:
                records = select_records(
                    carry["records"],
                    architecture=architecture,
                    intervention=intervention,
                    n_passes=n_passes,
                )
            row = {"label": label, "n_passes": n_passes}
            row.update(recall_panel_metrics(records))
            rows.append(row)
        panel_rows[str(n_passes)] = rows

    note_aware_n8 = select_records(recall["records"], architecture="scale_aware_note_aware", n_passes=8)
    psu_no_carry_n8 = select_records(
        carry["records"],
        architecture="scale_aware_note_aware",
        intervention="tiny_placeholder_hardened_scaffold",
        n_passes=8,
    )
    psu_n8 = select_records(
        carry["records"],
        architecture="scale_aware_note_aware",
        intervention="tiny_carry_forward_scaffold",
        n_passes=8,
    )

    direct_deltas = {
        "note_aware_to_psu_accuracy": paired_delta(
            note_aware_n8,
            psu_n8,
            lambda record: 1.0 if record["correct"] else 0.0,
            harmful_metric=False,
        ),
        "note_aware_to_psu_history_loss": paired_delta(
            [record for record in note_aware_n8 if record["family"] in {"benign", "conflict"}],
            [record for record in psu_n8 if record["family"] in {"benign", "conflict"}],
            lambda record: 1.0 if record["compact_answer"] == "ABSTAIN" else 0.0,
            harmful_metric=True,
        ),
        "note_aware_to_psu_raw_escalation": paired_delta(
            note_aware_n8,
            psu_n8,
            lambda record: 1.0 if record["raw_escalated"] else 0.0,
            harmful_metric=True,
        ),
        "psu_no_carry_to_psu_unsafe_error": paired_delta(
            [record for record in psu_no_carry_n8 if record["family"] == "unsafe"],
            [record for record in psu_n8 if record["family"] == "unsafe"],
            lambda record: 1.0 if record["unsafe_answer"] else 0.0,
            harmful_metric=True,
        ),
    }

    payload = {
        "description": "Paper-facing recall main panel that places PSU beside the baseline routing family on the same actual recall slice.",
        "n_values": [4, 8],
        "panel_rows": panel_rows,
        "direct_deltas": direct_deltas,
    }

    lines = [
        "# PSU Recall Main Panel",
        "",
        "这份工件把 recall 主面板重新整理成论文可直接引用的形状：同一张表里同时放 baseline routing family、PSU 无 carry 的近邻 ablation、以及最终 PSU。",
        "",
    ]
    for n_passes in [4, 8]:
        lines.extend(
            [
                f"## N={n_passes}",
                "",
                "| Method | accuracy | propagation | raw escalation | history loss | empty-note-then-abstain | benign/conflict error | unsafe error | hallucination placeholder | carry-forward record |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in panel_rows[str(n_passes)]:
            lines.append(
                f"| {row['label']} | {row['accuracy']:.3f} | {row['propagation']:.3f} | {row['raw_escalation']:.3f} | "
                f"{row['history_loss']:.3f} | {row['empty_note_then_abstain']:.3f} | {row['benign_conflict_error']:.3f} | "
                f"{row['unsafe_error']:.3f} | {row['hallucination_placeholder']:.3f} | {row['carry_forward_record']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Direct Delta At N=8",
            "",
            "| Comparison | Pairs | Mean Delta | Wins | Losses | Ties |",
            "|---|---:|---:|---:|---:|---:|",
            f"| scale_aware_note_aware -> PSU accuracy | {direct_deltas['note_aware_to_psu_accuracy']['pair_count']} | {direct_deltas['note_aware_to_psu_accuracy']['mean_delta']:.3f} | {direct_deltas['note_aware_to_psu_accuracy']['wins']} | {direct_deltas['note_aware_to_psu_accuracy']['losses']} | {direct_deltas['note_aware_to_psu_accuracy']['ties']} |",
            f"| scale_aware_note_aware -> PSU history loss | {direct_deltas['note_aware_to_psu_history_loss']['pair_count']} | {direct_deltas['note_aware_to_psu_history_loss']['mean_delta']:.3f} | {direct_deltas['note_aware_to_psu_history_loss']['wins']} | {direct_deltas['note_aware_to_psu_history_loss']['losses']} | {direct_deltas['note_aware_to_psu_history_loss']['ties']} |",
            f"| scale_aware_note_aware -> PSU raw escalation | {direct_deltas['note_aware_to_psu_raw_escalation']['pair_count']} | {direct_deltas['note_aware_to_psu_raw_escalation']['mean_delta']:.3f} | {direct_deltas['note_aware_to_psu_raw_escalation']['wins']} | {direct_deltas['note_aware_to_psu_raw_escalation']['losses']} | {direct_deltas['note_aware_to_psu_raw_escalation']['ties']} |",
            f"| psu_no_carry -> PSU unsafe error | {direct_deltas['psu_no_carry_to_psu_unsafe_error']['pair_count']} | {direct_deltas['psu_no_carry_to_psu_unsafe_error']['mean_delta']:.3f} | {direct_deltas['psu_no_carry_to_psu_unsafe_error']['wins']} | {direct_deltas['psu_no_carry_to_psu_unsafe_error']['losses']} | {direct_deltas['psu_no_carry_to_psu_unsafe_error']['ties']} |",
            "",
            "## Readout",
            "",
            "- `psu_no_carry` isolates the scaffold + placeholder hardening state just before the final carry-forward rule, so the last step is not conflated with earlier scaffold work.",
            "- If PSU lowers both `history_loss` and `raw escalation` against `scale_aware_note_aware`, then recall-side gains are no longer only coming from more aggressive fallback; they are coming from better compact-memory survival.",
        ]
    )

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
