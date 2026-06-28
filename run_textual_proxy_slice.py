from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from pilot_core import (
    ABSTAIN,
    CLEANUP_ARCHITECTURES,
    REFUSE,
    CompactClaim,
    aggregate,
    answer_from_compact,
    build_retrieval_probe,
    estimate_cost,
    initial_compact,
    is_bad_claim,
    load_items,
    raw_answer,
    route_answer,
    scrub_claims,
)


ARCHITECTURES = ["summary_only", "tiered", "utility_calibrated", "scale_aware_unified"]
N_VALUES = [1, 2, 4, 8]
SEEDS = [11, 23, 47, 89, 131]
SLICE_IDS = [
    "halu_01",
    "halu_02",
    "halu_03",
    "halu_04",
    "conflict_01",
    "conflict_02",
    "conflict_03",
    "conflict_04",
    "unsafe_01",
    "unsafe_02",
    "unsafe_03",
    "unsafe_04",
    "benign_01",
    "benign_02",
    "benign_03",
    "benign_04",
]
TRACE_IDS = {
    "hallucination": "halu_03",
    "conflict": "conflict_02",
    "unsafe": "unsafe_04",
    "benign": "benign_04",
}
JSON_PATH = "outputs/textual_proxy_slice_results.json"
SUMMARY_PATH = "outputs/textual_proxy_slice_summary.md"
TRACE_PATH = "outputs/textual_proxy_slice_traces.md"


def rng_for(seed: int, item_id: str, pass_idx: int) -> random.Random:
    return random.Random(f"textual-proxy:{seed}:{item_id}:{pass_idx}")


def clone_claim(claim: CompactClaim, **changes: Any) -> CompactClaim:
    payload = {
        "field": claim.field,
        "value": claim.value,
        "supported": claim.supported,
        "unsafe": claim.unsafe,
        "confidence": claim.confidence,
        "current": claim.current,
        "provenance_complete": claim.provenance_complete,
        "conflict_state": claim.conflict_state,
    }
    payload.update(changes)
    return CompactClaim(**payload)


def select_slice(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    order = {item_id: idx for idx, item_id in enumerate(SLICE_IDS)}
    selected = [item for item in items if item["id"] in order]
    selected.sort(key=lambda item: order[item["id"]])
    if len(selected) != len(SLICE_IDS):
        missing = [item_id for item_id in SLICE_IDS if item_id not in {item["id"] for item in selected}]
        raise RuntimeError(f"Missing slice items: {missing}")
    return selected


def decay_claims(claims: list[CompactClaim], target_field: str, pass_idx: int) -> list[CompactClaim]:
    decayed = []
    for claim in claims:
        penalty = 0.05 if claim.field == target_field else 0.03
        confidence = max(0.35, claim.confidence - penalty)
        provenance_complete = claim.provenance_complete and pass_idx == 1 and claim.supported and claim.current
        decayed.append(
            clone_claim(
                claim,
                confidence=confidence,
                provenance_complete=provenance_complete,
            )
        )
    return decayed


def trim_context(claims: list[CompactClaim], target_field: str, pass_idx: int) -> list[CompactClaim]:
    target_claims = [claim for claim in claims if claim.field == target_field]
    context_claims = [claim for claim in claims if claim.field != target_field]
    keep = 2 if pass_idx <= 2 else 1
    context_claims = sorted(
        context_claims,
        key=lambda claim: (
            claim.unsafe,
            not claim.supported,
            claim.field,
            claim.value,
        ),
    )[:keep]
    return target_claims + context_claims


def render_target_snippet(claim: CompactClaim) -> str:
    field = claim.field.replace("_", " ")
    if claim.unsafe:
        return f"Suggested action mentioned: {claim.value}."
    if claim.conflict_state == "stale":
        return f"An earlier note lists {field} as {claim.value}."
    if claim.conflict_state == "merged":
        return f"Notes collapse {field} into {claim.value}."
    if not claim.supported:
        return f"Likely {field}: {claim.value}."
    if not claim.provenance_complete:
        return f"Current {field} appears to be {claim.value}."
    return f"Current {field} is {claim.value}."


def render_context_snippet(claim: CompactClaim) -> str:
    field = claim.field.replace("_", " ")
    if claim.unsafe:
        return f"{field}: risky suggestion retained"
    if not claim.supported:
        return f"{field}: maybe {claim.value}"
    if not claim.current:
        return f"{field}: prior value {claim.value}"
    return f"{field}: {claim.value}"


def render_note(item: dict[str, Any], claims: list[CompactClaim], pass_idx: int, rng: random.Random) -> str:
    target_field = item["query_field"]
    target_claims = [claim for claim in claims if claim.field == target_field]
    context_claims = [claim for claim in claims if claim.field != target_field][:2]

    opener = rng.choice(
        [
            f"Summary pass {pass_idx} for {item['subject']}.",
            f"Compressed memory note after pass {pass_idx} for {item['subject']}.",
        ]
    )
    parts = [opener]
    if context_claims:
        context_text = "; ".join(render_context_snippet(claim) for claim in context_claims)
        parts.append(f"Context kept: {context_text}.")

    if not target_claims:
        parts.append(
            rng.choice(
                [
                    f"The key {target_field.replace('_', ' ')} detail is not retained clearly.",
                    f"No reliable {target_field.replace('_', ' ')} detail remains in the note.",
                ]
            )
        )
    else:
        parts.extend(render_target_snippet(claim) for claim in target_claims)

    if item["family"] == "hallucination" and any(not claim.supported for claim in target_claims):
        parts.append("This looks inferred from nearby context rather than directly sourced.")
    if item["family"] == "conflict" and any(claim.conflict_state != "clean" for claim in target_claims):
        parts.append("Update history may be entangled with the current state.")
    if item["family"] == "benign" and not target_claims:
        parts.append("This looks like ordinary over-compression rather than a safety issue.")
    return " ".join(parts)


def conflict_values(item: dict[str, Any]) -> tuple[str, str]:
    target = item["query_field"]
    old_value = next(fact["value"] for fact in item["raw_facts"] if fact["field"] == target and not fact["current"])
    new_value = next(fact["value"] for fact in item["raw_facts"] if fact["field"] == target and fact["current"])
    return old_value, new_value


def consolidate_textual_proxy(
    item: dict[str, Any],
    n_passes: int,
    seed: int,
) -> tuple[list[CompactClaim], list[str]]:
    claims = initial_compact(item)
    note_history: list[str] = []
    target_field = item["query_field"]

    for pass_idx in range(1, n_passes + 1):
        rng = rng_for(seed, item["id"], pass_idx)
        claims = decay_claims(claims, target_field, pass_idx)

        if item["family"] == "hallucination":
            p_infer = min(0.10 + 0.09 * pass_idx, 0.66)
            if rng.random() < p_infer:
                invented_value = rng.choice(item["invention_candidates"])
                claims = [claim for claim in claims if claim.field != target_field]
                claims.append(
                    CompactClaim(
                        field=target_field,
                        value=invented_value,
                        supported=False,
                        unsafe=False,
                        confidence=min(0.38 + 0.08 * pass_idx, 0.80),
                        current=True,
                        provenance_complete=False,
                        conflict_state="unknown",
                    )
                )
        elif item["family"] == "conflict":
            old_value, new_value = conflict_values(item)
            context_claims = [claim for claim in claims if claim.field != target_field]
            r = rng.random()
            p_dual = min(0.18 + 0.04 * pass_idx, 0.34)
            p_stale = min(0.07 + 0.06 * pass_idx, 0.30)
            p_merge = min(0.08 + 0.06 * pass_idx, 0.30)
            if r < p_dual:
                claims = context_claims + [
                    CompactClaim(
                        field=target_field,
                        value=old_value,
                        supported=True,
                        unsafe=False,
                        confidence=max(0.46, 0.64 - 0.03 * pass_idx),
                        current=False,
                        provenance_complete=False,
                        conflict_state="stale",
                    ),
                    CompactClaim(
                        field=target_field,
                        value=new_value,
                        supported=True,
                        unsafe=False,
                        confidence=max(0.56, 0.79 - 0.03 * pass_idx),
                        current=True,
                        provenance_complete=False,
                        conflict_state="clean",
                    ),
                ]
            elif r < p_dual + p_stale:
                claims = context_claims + [
                    CompactClaim(
                        field=target_field,
                        value=old_value,
                        supported=True,
                        unsafe=False,
                        confidence=max(0.48, 0.68 - 0.03 * pass_idx),
                        current=False,
                        provenance_complete=False,
                        conflict_state="stale",
                    )
                ]
            elif r < p_dual + p_stale + p_merge:
                claims = context_claims + [
                    CompactClaim(
                        field=target_field,
                        value=f"{old_value} -> {new_value}",
                        supported=False,
                        unsafe=False,
                        confidence=min(0.48 + 0.05 * pass_idx, 0.74),
                        current=True,
                        provenance_complete=False,
                        conflict_state="merged",
                    )
                ]
            else:
                claims = context_claims + [
                    CompactClaim(
                        field=target_field,
                        value=new_value,
                        supported=True,
                        unsafe=False,
                        confidence=max(0.60, 0.82 - 0.03 * pass_idx),
                        current=True,
                        provenance_complete=pass_idx == 1,
                        conflict_state="clean",
                    )
                ]
        elif item["family"] == "unsafe":
            p_launder = min(0.18 + 0.08 * pass_idx, 0.78)
            if rng.random() < p_launder:
                claims = [claim for claim in claims if claim.field != target_field]
                claims.append(
                    CompactClaim(
                        field=target_field,
                        value=rng.choice(item["unsafe_paraphrases"]),
                        supported=False,
                        unsafe=True,
                        confidence=min(0.44 + 0.06 * pass_idx, 0.84),
                        current=True,
                        provenance_complete=False,
                        conflict_state="clean",
                    )
                )
        elif item["family"] == "benign":
            r = rng.random()
            p_drop = min(0.03 + 0.03 * pass_idx, 0.18)
            p_blur = min(0.08 + 0.05 * pass_idx, 0.34)
            if r < p_drop:
                claims = [claim for claim in claims if claim.field != target_field]
            elif r < p_drop + p_blur:
                claims = [claim for claim in claims if claim.field != target_field]
                claims.append(
                    CompactClaim(
                        field=target_field,
                        value=rng.choice(item["benign_simplifications"]),
                        supported=False,
                        unsafe=False,
                        confidence=min(0.50 + 0.05 * pass_idx, 0.78),
                        current=True,
                        provenance_complete=False,
                        conflict_state="unknown",
                    )
                )

        claims = trim_context(claims, target_field, pass_idx)
        note_history.append(render_note(item, claims, pass_idx, rng))

    return claims, note_history


def evaluate_textual_item(item: dict[str, Any], architecture: str, n_passes: int, seed: int) -> dict[str, Any]:
    latent_claims, note_history = consolidate_textual_proxy(item, n_passes, seed)
    latent_compact_answer, _ = answer_from_compact(item, latent_claims)
    claims = scrub_claims(latent_claims) if architecture in CLEANUP_ARCHITECTURES else latent_claims
    compact_answer, meta = answer_from_compact(item, claims)
    probe = None
    if architecture in CLEANUP_ARCHITECTURES:
        probe = build_retrieval_probe(item, latent_claims, seed + 503, n_passes)
    answer, escalated, route = route_answer(
        item,
        architecture,
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
    estimated_cost = estimate_cost(architecture, n_passes, escalated)

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
        "probe_status": None if architecture not in CLEANUP_ARCHITECTURES else probe.status,
        "probe_score": None if architecture not in CLEANUP_ARCHITECTURES else probe.score,
        "probe_raw_target_exists": None if architecture not in CLEANUP_ARCHITECTURES else probe.raw_target_exists,
        "probe_target_noise": None if architecture not in CLEANUP_ARCHITECTURES else probe.target_noise,
        "probe_history_conflict": None if architecture not in CLEANUP_ARCHITECTURES else probe.history_conflict,
        "benign_overcompression": benign_overcompression,
        "unsupported_answer": unsupported_answer,
        "unsafe_answer": unsafe_answer,
        "conflict_answer": conflict_answer,
        "propagation": propagation,
        "raw_escalated": escalated,
        "route": route,
        "estimated_cost": estimated_cost,
        "final_note": note_history[-1],
        "note_history": note_history,
        "claim_summary": [
            {
                "field": claim.field,
                "value": claim.value,
                "supported": claim.supported,
                "unsafe": claim.unsafe,
                "confidence": round(claim.confidence, 3),
                "current": claim.current,
                "provenance_complete": claim.provenance_complete,
                "conflict_state": claim.conflict_state,
            }
            for claim in claims
        ],
        "latent_claim_summary": [
            {
                "field": claim.field,
                "value": claim.value,
                "supported": claim.supported,
                "unsafe": claim.unsafe,
                "confidence": round(claim.confidence, 3),
                "current": claim.current,
                "provenance_complete": claim.provenance_complete,
                "conflict_state": claim.conflict_state,
            }
            for claim in latent_claims
        ],
    }


def slice_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    total = len(records)
    false_absent = [
        record
        for record in records
        if record["gold"] not in {ABSTAIN, REFUSE} and record["compact_answer"] == ABSTAIN and not record["raw_escalated"]
    ]
    false_present = [
        record
        for record in records
        if record["gold"] == ABSTAIN and record["raw_escalated"]
    ]
    note_missing = [record for record in records if "not retained clearly" in record["final_note"] or "No reliable" in record["final_note"]]
    return {
        "false_absent_rate": round(len(false_absent) / total, 3),
        "false_present_rate": round(len(false_present) / total, 3),
        "note_missing_rate": round(len(note_missing) / total, 3),
    }


def build_summary(results: dict[str, Any]) -> str:
    lines = [
        "# Textual Proxy Slice Summary",
        "",
        "这一轮不是再改 policy，而是把环境向前推一步：在 16 条高质量 slice 上，用一个更接近自由文本摘要 note 的 compactor proxy 测试 `scale_aware_unified`。",
        "",
        f"- slice items: {results['num_items']} (`4` per family)",
        f"- architectures: {', '.join(results['architectures'])}",
        f"- N: {results['n_values']}",
        "",
        "## Aggregate Readout",
        "",
    ]
    for architecture in results["architectures"]:
        lines.append(f"### {architecture}")
        lines.append("")
        lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | note_missing |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n in results["n_values"]:
            row = results["aggregate"][architecture][str(n)]
            metrics = results["slice_metrics"][architecture][str(n)]
            lines.append(
                f"| {n} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | {row['residual_bad_memory_rate']:.3f} | "
                f"{row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} | {metrics['false_absent_rate']:.3f} | "
                f"{metrics['false_present_rate']:.3f} | {metrics['note_missing_rate']:.3f} |"
            )
        lines.append("")
        lines.append("| family @ N=8 | accuracy | propagation | raw_escalation |")
        lines.append("|---|---:|---:|---:|")
        for family, metrics in results["aggregate"][architecture]["8"]["by_family"].items():
            lines.append(
                f"| {family} | {metrics['accuracy']:.3f} | {metrics['propagation_rate']:.3f} | {metrics['raw_escalation_rate']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Readout",
            "",
            "- 关键问题不是 textual proxy 会不会复制主实验数字，而是 `scale_aware_unified` 的方向性优势是否还活着。",
            "- 如果 `summary_only` 仍随 `N` 恶化，而 `scale_aware_unified` 仍能把 residual contamination 压到低位，同时避免 `tiered` 的高 raw fallback，那么说明主张开始跨环境稳定。",
            "- 如果优势在这个 slice 上消失，就说明前一轮的 unified story 还没有穿过 realism check。",
        ]
    )
    return "\n".join(lines) + "\n"


def build_traces(records: list[dict[str, Any]]) -> str:
    lines = [
        "# Textual Proxy Slice Traces",
        "",
        "这些 trace 用来检查 text-note 环境下的机制，不作为主表结论。",
        "",
    ]
    show_n = [1, 4, 8]
    for family, item_id in TRACE_IDS.items():
        lines.append(f"## {family}: {item_id}")
        lines.append("")
        for architecture in ARCHITECTURES:
            lines.append(f"### {architecture}")
            lines.append("")
            for n in show_n:
                record = next(
                    record
                    for record in records
                    if record["item_id"] == item_id
                    and record["architecture"] == architecture
                    and record["n_passes"] == n
                    and record["seed"] == SEEDS[0]
                )
                probe = "-" if record["probe_status"] is None else f"{record['probe_status']} / {record['probe_score']:.3f}"
                lines.append(
                    f"- N={n}: probe={probe}; compact={record['compact_answer']}; final={record['answer']}; "
                    f"route={record['route']}; raw={int(record['raw_escalated'])}"
                )
                lines.append(f"  note: {record['final_note']}")
            lines.append("")
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
            metric_table[architecture][str(n_passes)] = slice_metrics(records)
            route_counts[architecture][str(n_passes)] = dict(Counter(record["route"] for record in records))

    payload = {
        "description": "Focused textual-proxy slice for a more realistic summarization environment.",
        "slice_ids": SLICE_IDS,
        "architectures": ARCHITECTURES,
        "n_values": N_VALUES,
        "seeds": SEEDS,
        "num_items": len(items),
        "aggregate": aggregate_table,
        "slice_metrics": metric_table,
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
