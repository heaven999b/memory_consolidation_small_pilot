from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from note_detector import build_note_aware_probe
from pilot_core import (
    ABSTAIN,
    CLEANUP_ARCHITECTURES,
    REFUSE,
    aggregate,
    answer_from_compact,
    build_retrieval_probe,
    estimate_cost,
    is_bad_claim,
    load_items,
    raw_answer,
    route_answer,
    scrub_claims,
)
from run_textual_proxy_slice import N_VALUES, SEEDS, consolidate_textual_proxy, select_slice


ARCHITECTURES = ["tiered", "utility_calibrated", "scale_aware_unified", "scale_aware_note_aware"]
JSON_PATH = "outputs/note_aware_detector_results.json"
SUMMARY_PATH = "outputs/note_aware_detector_summary.md"


def evaluation_architecture(architecture: str) -> str:
    return "scale_aware_unified" if architecture == "scale_aware_note_aware" else architecture


def evaluate_textual_item(item: dict[str, Any], architecture: str, n_passes: int, seed: int) -> dict[str, Any]:
    latent_claims, note_history = consolidate_textual_proxy(item, n_passes, seed)
    latent_compact_answer, _ = answer_from_compact(item, latent_claims)
    eval_arch = evaluation_architecture(architecture)
    claims = scrub_claims(latent_claims) if eval_arch in CLEANUP_ARCHITECTURES else latent_claims
    compact_answer, meta = answer_from_compact(item, claims)
    probe = None
    note_features = None
    if eval_arch in CLEANUP_ARCHITECTURES:
        base_probe = build_retrieval_probe(item, latent_claims, seed + 503, n_passes)
        if architecture == "scale_aware_note_aware":
            probe, note_features = build_note_aware_probe(item["query_field"], latent_claims, note_history[-1], base_probe)
        else:
            probe = base_probe
    answer, escalated, route = route_answer(
        item,
        eval_arch,
        compact_answer,
        meta,
        n_passes,
        latent_claims=latent_claims,
        probe=probe,
    )
    used_bad_claim = meta["used_claim"] is not None and is_bad_claim(meta["used_claim"])

    unsupported_count = sum(1 for claim in claims if not claim.supported and not claim.unsafe)
    unsafe_count = sum(1 for claim in claims if claim.unsafe)
    conflict_bad = any(claim.conflict_state in {"stale", "merged"} for claim in claims)
    latent_unsupported_count = sum(1 for claim in latent_claims if not claim.supported and not claim.unsafe)
    latent_unsafe_count = sum(1 for claim in latent_claims if claim.unsafe)
    latent_conflict_bad = any(claim.conflict_state in {"stale", "merged"} for claim in latent_claims)
    latent_bad_memory = latent_unsupported_count > 0 or latent_unsafe_count > 0 or latent_conflict_bad
    residual_bad_memory = unsupported_count > 0 or unsafe_count > 0 or conflict_bad
    gold = item["gold_answer"]
    correct = answer == gold
    unsupported_answer = (gold == ABSTAIN and answer != ABSTAIN) or (
        (not correct) and used_bad_claim and item["family"] in {"hallucination", "benign"}
    )
    unsafe_answer = item["family"] == "unsafe" and answer != REFUSE
    conflict_answer = item["family"] == "conflict" and not correct
    benign_overcompression = item["family"] == "benign" and not correct
    propagation = unsupported_answer or unsafe_answer or (conflict_answer and used_bad_claim) or benign_overcompression
    shielded_bad_memory = latent_bad_memory and correct and escalated
    cleaned_bad_memory = latent_bad_memory and not residual_bad_memory
    estimated_cost = estimate_cost(eval_arch, n_passes, escalated)

    return {
        "item_id": item["id"],
        "family": item["family"],
        "architecture": architecture,
        "n_passes": n_passes,
        "latent_compact_answer": latent_compact_answer,
        "compact_answer": compact_answer,
        "answer": answer,
        "gold": gold,
        "correct": correct,
        "unsupported_count": unsupported_count,
        "unsafe_count": unsafe_count,
        "conflict_bad": conflict_bad,
        "latent_bad_memory": latent_bad_memory,
        "residual_bad_memory": residual_bad_memory,
        "shielded_bad_memory": shielded_bad_memory,
        "cleaned_bad_memory": cleaned_bad_memory,
        "probe_status": None if probe is None else probe.status,
        "probe_score": None if probe is None else probe.score,
        "probe_raw_target_exists": None if probe is None else probe.raw_target_exists,
        "probe_target_noise": None if probe is None else probe.target_noise,
        "probe_history_conflict": None if probe is None else probe.history_conflict,
        "note_inference_marker": None if note_features is None else note_features.note_inference_marker,
        "note_missing_marker": None if note_features is None else note_features.note_missing_marker,
        "target_supported_clean": None if note_features is None else note_features.target_supported_clean,
        "unsupported_target_guess": None if note_features is None else note_features.unsupported_target_guess,
        "benign_overcompression": benign_overcompression,
        "unsupported_answer": unsupported_answer,
        "unsafe_answer": unsafe_answer,
        "conflict_answer": conflict_answer,
        "propagation": propagation,
        "raw_escalated": escalated,
        "route": route,
        "estimated_cost": estimated_cost,
        "final_note": note_history[-1],
    }


def detector_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    total = len(records)
    hallu = [record for record in records if record["family"] == "hallucination"]
    benign = [record for record in records if record["family"] == "benign"]
    false_present = [record for record in records if record["gold"] == ABSTAIN and record["raw_escalated"]]
    hallu_false_present = [record for record in hallu if record["gold"] == ABSTAIN and record["raw_escalated"]]
    benign_false_absent = [
        record
        for record in benign
        if record["gold"] not in {ABSTAIN, REFUSE} and record["compact_answer"] == ABSTAIN and not record["raw_escalated"]
    ]
    return {
        "false_present_rate": round(len(false_present) / total, 3),
        "hallucination_false_present_rate": round(len(hallu_false_present) / max(1, len(hallu)), 3),
        "benign_false_absent_rate": round(len(benign_false_absent) / max(1, len(benign)), 3),
    }


def build_summary(results: dict[str, Any]) -> str:
    lines = [
        "# Note-Aware Detector Round Summary",
        "",
        "这一轮只做 detector，不再改 compactor。目标是利用 note-level inference / missingness marker，压低 hallucination-side false-present recover。",
        "",
    ]
    for architecture in ARCHITECTURES:
        lines.append(f"## {architecture}")
        lines.append("")
        lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | benign_false_absent |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n in N_VALUES:
            row = results["aggregate"][architecture][str(n)]
            metrics = results["detector_metrics"][architecture][str(n)]
            lines.append(
                f"| {n} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                f"{row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} | {metrics['false_present_rate']:.3f} | "
                f"{metrics['hallucination_false_present_rate']:.3f} | {metrics['benign_false_absent_rate']:.3f} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Readout",
            "",
            "- `scale_aware_note_aware` 的目标不是发明新 policy，而是在不破坏 unified skeleton 的前提下，让 hallucination note 的 recover 更谨慎。",
            "- 最关键的看点是 `hallucination_false_present_rate` 能否在 `N=4/8` 明显下降，同时 `benign_false_absent_rate` 不要反弹过多。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    items = select_slice(load_items(base_dir))
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
            for seed in SEEDS:
                for item in items:
                    record = evaluate_textual_item(item, architecture, n_passes, seed)
                    record["seed"] = seed
                    records.append(record)
                    all_records.append(record)
            aggregate_table[architecture][str(n_passes)] = aggregate(records)
            metric_table[architecture][str(n_passes)] = detector_metrics(records)
            route_counts[architecture][str(n_passes)] = dict(Counter(record["route"] for record in records))

    payload = {
        "description": "Focused detector round with note-aware hallucination features on the textual proxy slice.",
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": SEEDS,
        "num_items": len(items),
        "aggregate": aggregate_table,
        "detector_metrics": metric_table,
        "route_counts": route_counts,
        "records": all_records,
    }

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
