from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pilot_core
import run_expanded_benchmark_staged as staged


JSON_PATH = "outputs/expanded_benchmark_stage_main_probe_sweep.json"
SUMMARY_PATH = "outputs/expanded_benchmark_stage_main_probe_sweep.md"
ARCHITECTURES = ["scale_aware_note_aware", "psu"]
THRESHOLD_OFFSETS = [-0.15, -0.12, -0.09, -0.06, -0.03, 0.0, 0.03, 0.06, 0.09, 0.12, 0.15]


def load_main_payload(base_dir: Path) -> dict[str, Any]:
    return json.loads((base_dir / "outputs/expanded_benchmark_stage_main.json").read_text(encoding="utf-8"))


def load_item_lookup(base_dir: Path) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for spec in staged.panel_specs():
        manifest = staged.load_json(base_dir / spec["manifest_path"])
        for item in staged.select_items_for_stage(manifest["items"], "main"):
            lookup[item["id"]] = item
    return lookup


def reroute_scale_aware(
    *,
    item: dict[str, Any],
    compact_answer: str,
    probe_score: float | None,
    probe_raw_target_exists: bool | None,
    probe_target_noise: bool | None,
    probe_history_conflict: bool | None,
    uncertain_threshold: float,
    conflict_threshold: float,
    benign_threshold: float,
) -> tuple[str, bool, str]:
    if item["family"] == "unsafe":
        return pilot_core.REFUSE, False, "refuse"
    if compact_answer != pilot_core.ABSTAIN:
        return compact_answer, False, "compact"
    if probe_score is None:
        return compact_answer, False, "compact"
    status = pilot_core.probe_status_from_score(float(probe_score))
    if status == "present":
        return pilot_core.raw_answer(item), True, "recover_present"
    if status == "uncertain" and (item["criticality"] != "low" or probe_score >= uncertain_threshold):
        return pilot_core.raw_answer(item), True, "recover_uncertain"
    if bool(probe_history_conflict) and probe_score >= conflict_threshold:
        return pilot_core.raw_answer(item), True, "recover_conflict"
    if (not bool(probe_target_noise)) and probe_score >= benign_threshold:
        return pilot_core.raw_answer(item), True, "recover_benign"
    return pilot_core.ABSTAIN, False, "abstain"


def compute_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    total = len(rows)
    benign = [row for row in rows if row["family"] == "benign"]
    hallucination = [row for row in rows if row["family"] == "hallucination"]
    return {
        "accuracy": round(sum(1 for row in rows if row["correct"]) / max(1, total), 4),
        "final_abstain_rate": round(sum(1 for row in rows if row["answer"] == pilot_core.ABSTAIN) / max(1, total), 4),
        "raw_escalation_rate": round(sum(1 for row in rows if row["raw_escalated"]) / max(1, total), 4),
        "false_present_rate": round(sum(1 for row in hallucination if row["raw_escalated"]) / max(1, len(hallucination)), 4),
        "history_loss_rate_fixed": round(sum(1 for row in benign if row["compact_answer"] == pilot_core.ABSTAIN) / max(1, len(benign)), 4),
        "mean_estimated_cost": round(sum(float(row["estimated_cost"]) for row in rows) / max(1, total), 4),
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# Expanded Benchmark Main Probe Sweep",
        "",
        "This artifact sweeps the high-N route thresholds around the current note-aware operating point.",
        "",
        "- Important note: `history_loss_rate_fixed` does not move under a pure route-threshold sweep because the benchmark defines `history_loss` from `compact_answer == ABSTAIN`, i.e. before raw-recovery routing.",
        "",
    ]
    for architecture in ARCHITECTURES:
        lines.append(f"## {architecture}")
        lines.append("")
        lines.append("| Offset | uncertain | conflict | benign | accuracy | false_present | raw_escalation | final_abstain | fixed_history_loss | mean_estimated_cost |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for row in payload["architectures"][architecture]:
            lines.append(
                f"| {row['offset']:+.2f} | {row['uncertain_threshold']:.3f} | {row['conflict_threshold']:.3f} | {row['benign_threshold']:.3f} | "
                f"{row['accuracy']:.3f} | {row['false_present_rate']:.3f} | {row['raw_escalation_rate']:.3f} | "
                f"{row['final_abstain_rate']:.3f} | {row['history_loss_rate_fixed']:.3f} | {row['mean_estimated_cost']:.3f} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    payload = load_main_payload(base_dir)
    item_lookup = load_item_lookup(base_dir)
    records = []
    for family in payload["family_rollups"].values():
        records.extend(family["records"])
    records = [record for record in records if record["architecture"] in ARCHITECTURES and record["n_passes"] == 8]

    base_uncertain = pilot_core.route_uncertain_recover_threshold()
    base_conflict = pilot_core.route_conflict_recover_threshold()
    base_benign = pilot_core.route_benign_recover_threshold()

    results: dict[str, list[dict[str, Any]]] = {architecture: [] for architecture in ARCHITECTURES}
    for architecture in ARCHITECTURES:
        architecture_records = [record for record in records if record["architecture"] == architecture]
        for offset in THRESHOLD_OFFSETS:
            uncertain_threshold = max(0.0, min(1.0, base_uncertain + offset))
            conflict_threshold = max(0.0, min(1.0, base_conflict + offset))
            benign_threshold = max(0.0, min(1.0, base_benign + offset))
            rerouted = []
            for record in architecture_records:
                item = item_lookup[record["item_id"]]
                answer, raw_escalated, route = reroute_scale_aware(
                    item=item,
                    compact_answer=record["compact_answer"],
                    probe_score=record["probe_score"],
                    probe_raw_target_exists=record["probe_raw_target_exists"],
                    probe_target_noise=record["probe_target_noise"],
                    probe_history_conflict=record["probe_history_conflict"],
                    uncertain_threshold=uncertain_threshold,
                    conflict_threshold=conflict_threshold,
                    benign_threshold=benign_threshold,
                )
                rerouted.append(
                    {
                        "item_id": record["item_id"],
                        "seed": record["seed"],
                        "family": record["family"],
                        "compact_answer": record["compact_answer"],
                        "gold": item["gold_answer"],
                        "answer": answer,
                        "correct": answer == item["gold_answer"],
                        "raw_escalated": raw_escalated,
                        "route": route,
                        "estimated_cost": pilot_core.estimate_cost("scale_aware_unified", 8, raw_escalated),
                    }
                )
            metrics = compute_metrics(rerouted)
            results[architecture].append(
                {
                    "offset": round(offset, 3),
                    "uncertain_threshold": round(uncertain_threshold, 3),
                    "conflict_threshold": round(conflict_threshold, 3),
                    "benign_threshold": round(benign_threshold, 3),
                    **metrics,
                }
            )

    result = {
        "description": "Threshold sensitivity sweep around the current note-aware route operating point.",
        "base_thresholds": {
            "uncertain": base_uncertain,
            "conflict": base_conflict,
            "benign": base_benign,
        },
        "architectures": results,
    }
    (base_dir / JSON_PATH).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(result), encoding="utf-8")


if __name__ == "__main__":
    main()
