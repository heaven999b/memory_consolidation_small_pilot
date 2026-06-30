from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pilot_core
import v3_no_rewrite_policy as no_rewrite_policy


JSON_PATH = "outputs/v3_no_rewrite_comparison.json"
SUMMARY_PATH = "outputs/v3_no_rewrite_comparison.md"
N_VALUES = [0, 1, 2, 4, 8, 16]
SEEDS = [11, 23]
ARCHITECTURES = [
    "raw_only",
    "summary_only",
    "summary_query_aware",
    "summary_only_no_rewrite",
    "summary_query_aware_no_rewrite",
    "tiered",
    "tiered_no_rewrite",
]
MANIFEST_SPECS = [
    ("halumem_expanded_v1", "benchmarks/halumem/frozen_slices/halumem_hallucination_expanded_v1.json"),
    ("locomo_expanded_v1", "benchmarks/locomo/frozen_slices/locomo_benign_utility_expanded_v1.json"),
    ("longmemeval_expanded_v2", "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_expanded_v2.json"),
    ("pilot_conflict_extension_v2", "benchmarks/task_extensions/frozen_slices/conflict_task_extension_v2.json"),
    ("pilot_unsafe_extension_v2", "benchmarks/task_extensions/frozen_slices/unsafe_task_extension_v2.json"),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_items(repo_root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for panel_id, manifest_path in MANIFEST_SPECS:
        manifest = load_json(repo_root / manifest_path)
        for item in manifest["items"]:
            enriched = dict(item)
            enriched["panel_id"] = panel_id
            items.append(enriched)
    return items


def build_claims_from_dicts(claim_dicts: list[dict[str, Any]]) -> list[pilot_core.CompactClaim]:
    return [
        pilot_core.CompactClaim(
            field=claim["field"],
            value=claim["value"],
            supported=bool(claim["supported"]),
            unsafe=bool(claim["unsafe"]),
            confidence=float(claim["confidence"]),
            current=bool(claim.get("current", True)),
            provenance_complete=bool(claim.get("provenance_complete", True)),
            conflict_state=str(claim.get("conflict_state", "clean")),
        )
        for claim in claim_dicts
    ]


def query_aware_target_claims_from_raw(item: dict[str, Any]) -> list[pilot_core.CompactClaim]:
    target = item["query_field"].lower().strip().replace("_", " ")
    claims: list[pilot_core.CompactClaim] = []
    for fact in item.get("raw_facts", []):
        fact_field = str(fact.get("field", "")).lower().strip().replace("_", " ")
        if fact_field != target:
            continue
        if not bool(fact.get("current", False)):
            continue
        claims.append(
            pilot_core.CompactClaim(
                field=str(fact.get("field", "")),
                value=str(fact.get("value", "")),
                supported=bool(fact.get("supported", False)),
                unsafe=bool(fact.get("unsafe", False)),
                confidence=0.97 if bool(fact.get("supported", False)) else 0.78,
                current=True,
                provenance_complete=(str(fact.get("trust", "low")) == "high"),
                conflict_state="clean",
            )
        )
    return claims


def apply_query_aware(item: dict[str, Any], claims: list[pilot_core.CompactClaim]) -> list[pilot_core.CompactClaim]:
    target = item["query_field"].lower().strip().replace("_", " ")
    non_target_claims = [
        claim
        for claim in claims
        if claim.field.lower().strip().replace("_", " ") != target
    ]
    target_claims = query_aware_target_claims_from_raw(item)
    return non_target_claims + target_claims if target_claims else list(claims)


def apply_no_rewrite(item: dict[str, Any], latent_claims: list[pilot_core.CompactClaim]) -> tuple[list[pilot_core.CompactClaim], dict[str, Any]]:
    audit = no_rewrite_policy.audit_item(item, latent_claims)
    if not audit["protected"]:
        return list(latent_claims), audit

    target = item["query_field"].lower().strip().replace("_", " ")
    non_target_claims = [
        claim
        for claim in latent_claims
        if claim.field.lower().strip().replace("_", " ") != target
    ]
    replacement_claims = build_claims_from_dicts(no_rewrite_policy.build_replacement_claim_dicts(item, audit))
    return non_target_claims + replacement_claims, audit


def estimate_proxy_cost(architecture: str, base_architecture: str, n_passes: int, raw_escalated: bool) -> float:
    cost = pilot_core.estimate_cost(base_architecture, n_passes, raw_escalated)
    if "query_aware" in architecture:
        cost += 0.03
    if architecture.endswith("_no_rewrite"):
        cost += 0.05
    return round(cost, 3)


def family_metric_rows(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    family_rows: dict[str, dict[str, float]] = {}
    families = sorted({record["family"] for record in records})
    for family in families:
        subset = [record for record in records if record["family"] == family]
        family_rows[family] = {
            "accuracy": round(sum(record["correct"] for record in subset) / max(1, len(subset)), 3),
            "propagation_rate": round(sum(record["propagation"] for record in subset) / max(1, len(subset)), 3),
            "unsupported_answer_rate": round(sum(record["unsupported_answer"] for record in subset) / max(1, len(subset)), 3),
            "unsafe_answer_rate": round(sum(record["unsafe_answer"] for record in subset) / max(1, len(subset)), 3),
            "conflict_answer_rate": round(sum(record["conflict_answer"] for record in subset) / max(1, len(subset)), 3),
            "benign_overcompression_rate": round(sum(record["benign_overcompression"] for record in subset) / max(1, len(subset)), 3),
            "raw_escalation_rate": round(sum(record["raw_escalated"] for record in subset) / max(1, len(subset)), 3),
        }
    return family_rows


def evaluate_architecture(
    item: dict[str, Any],
    architecture: str,
    n_passes: int,
    seed: int,
) -> dict[str, Any]:
    if architecture == "raw_only":
        record = pilot_core.evaluate_item(item, "raw_only", n_passes, seed)
        record["protected_field"] = no_rewrite_policy.detect_protection_category(item) is not None
        record["no_rewrite_blocked_claim_count"] = 0
        record["no_rewrite_mode"] = "none"
        record["query_aware_mode"] = "none"
        return record

    base_architecture = architecture.removesuffix("_no_rewrite")
    if base_architecture == "summary_query_aware":
        base_architecture = "summary_only"
    latent_claims = pilot_core.consolidate(item, n_passes, seed)
    kept_claims = list(latent_claims)
    audit: dict[str, Any] | None = None
    no_rewrite_mode = "none"
    query_aware_mode = "none"

    if "query_aware" in architecture:
        kept_claims = apply_query_aware(item, kept_claims)
        query_aware_mode = "target_field_exact_preserve"

    if architecture.endswith("_no_rewrite"):
        kept_claims, audit = apply_no_rewrite(item, kept_claims)
        no_rewrite_mode = "protected_target_rewrite_block"
    elif base_architecture in pilot_core.CLEANUP_ARCHITECTURES:
        kept_claims = pilot_core.scrub_claims(latent_claims)

    compact_answer, meta = pilot_core.answer_from_compact(item, kept_claims)
    probe = None
    if base_architecture in pilot_core.CLEANUP_ARCHITECTURES:
        probe = pilot_core.build_retrieval_probe(item, kept_claims, seed, n_passes)
    answer, escalated, route = pilot_core.route_answer(
        item,
        base_architecture,
        compact_answer,
        meta,
        n_passes,
        latent_claims=kept_claims,
        probe=probe,
    )
    used_bad_claim = meta["used_claim"] is not None and pilot_core.is_bad_claim(meta["used_claim"])

    unsupported_count = sum(1 for claim in kept_claims if not claim.supported and not claim.unsafe)
    unsafe_count = sum(1 for claim in kept_claims if claim.unsafe)
    conflict_bad = any(claim.conflict_state in {"stale", "merged"} for claim in kept_claims)
    latent_unsupported_count = sum(1 for claim in latent_claims if not claim.supported and not claim.unsafe)
    latent_unsafe_count = sum(1 for claim in latent_claims if claim.unsafe)
    latent_conflict_bad = any(claim.conflict_state in {"stale", "merged"} for claim in latent_claims)
    latent_bad_memory = latent_unsupported_count > 0 or latent_unsafe_count > 0 or latent_conflict_bad
    residual_bad_memory = unsupported_count > 0 or unsafe_count > 0 or conflict_bad
    gold = item["gold_answer"]
    correct = answer == gold
    unsupported_answer = (gold == pilot_core.ABSTAIN and answer != pilot_core.ABSTAIN) or (
        (not correct) and used_bad_claim and item["family"] in {"hallucination", "benign"}
    )
    unsafe_answer = item["family"] == "unsafe" and answer != pilot_core.REFUSE
    conflict_answer = item["family"] == "conflict" and not correct
    benign_overcompression = item["family"] == "benign" and not correct
    propagation = unsupported_answer or unsafe_answer or (conflict_answer and used_bad_claim) or benign_overcompression
    shielded_bad_memory = latent_bad_memory and correct and escalated
    cleaned_bad_memory = latent_bad_memory and not residual_bad_memory

    record = {
        "item_id": item["id"],
        "panel_id": item["panel_id"],
        "family": item["family"],
        "architecture": architecture,
        "base_architecture": base_architecture,
        "n_passes": n_passes,
        "seed": seed,
        "latent_compact_answer": pilot_core.answer_from_compact(item, latent_claims)[0],
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
        "benign_overcompression": benign_overcompression,
        "unsupported_answer": unsupported_answer,
        "unsafe_answer": unsafe_answer,
        "conflict_answer": conflict_answer,
        "propagation": propagation,
        "raw_escalated": escalated,
        "route": route,
        "estimated_cost": estimate_proxy_cost(architecture, base_architecture, n_passes, escalated),
        "protected_field": (audit["protected"] if audit is not None else (no_rewrite_policy.detect_protection_category(item) is not None)),
        "no_rewrite_blocked_claim_count": 0 if audit is None else audit["blocked_claim_count"],
        "no_rewrite_allowed_claim_count": 0 if audit is None else audit["allowed_claim_count"],
        "no_rewrite_preserved_source_count": 0 if audit is None else audit["preserved_source_count"],
        "no_rewrite_mode": no_rewrite_mode,
        "no_rewrite_blocked_reasons": [] if audit is None else audit["blocked_reasons"],
        "query_aware_mode": query_aware_mode,
    }
    return record


def build_payload(repo_root: Path) -> dict[str, Any]:
    items = load_items(repo_root)
    records: list[dict[str, Any]] = []
    for item in items:
        for architecture in ARCHITECTURES:
            for n_passes in N_VALUES:
                for seed in SEEDS:
                    records.append(evaluate_architecture(item, architecture, n_passes, seed))

    grouped: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    by_arch_n: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    by_arch_n_family: dict[tuple[str, int, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_arch_n[(record["architecture"], record["n_passes"])].append(record)
        by_arch_n_family[(record["architecture"], record["n_passes"], record["family"])].append(record)

    for architecture in ARCHITECTURES:
        for n_passes in N_VALUES:
            subset = by_arch_n[(architecture, n_passes)]
            grouped[architecture][str(n_passes)] = {
                "overall": pilot_core.aggregate(subset),
                "by_family": family_metric_rows(subset),
                "protected_case_rate": round(
                    sum(record["protected_field"] for record in subset) / max(1, len(subset)),
                    3,
                ),
                "blocked_protected_case_rate": round(
                    sum(
                        1
                        for record in subset
                        if record["protected_field"] and record["no_rewrite_blocked_claim_count"] > 0
                    )
                    / max(1, sum(record["protected_field"] for record in subset)),
                    3,
                )
                if architecture.endswith("_no_rewrite")
                else None,
            }

    examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    no_rewrite_records = [record for record in records if record["architecture"] == "summary_only_no_rewrite" and record["n_passes"] == 8]
    for family in sorted({record["family"] for record in no_rewrite_records}):
        family_rows = [
            record
            for record in no_rewrite_records
            if record["family"] == family and record["no_rewrite_blocked_claim_count"] > 0
        ]
        family_rows.sort(key=lambda record: (-record["no_rewrite_blocked_claim_count"], record["item_id"], record["seed"]))
        for record in family_rows[:3]:
            examples[family].append(
                {
                    "item_id": record["item_id"],
                    "seed": record["seed"],
                    "compact_answer": record["compact_answer"],
                    "final_answer": record["answer"],
                    "blocked_reasons": record["no_rewrite_blocked_reasons"],
                }
            )

    return {
        "description": "Expanded-manifest local proxy comparison for V3 no-rewrite against summary-only and tiered baselines.",
        "n_values": N_VALUES,
        "seeds": SEEDS,
        "architectures": ARCHITECTURES,
        "item_count": len(items),
        "records": records,
        "snapshots": grouped,
        "examples": examples,
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 No-Rewrite Comparison",
        "",
        "This is a local proxy comparison over the expanded manifest-backed pool. It is not a real TierMem result table, but it does turn the V3 defended mechanism into a directly comparable method surface.",
        "",
        f"- items: `{payload['item_count']}`",
        f"- seeds: `{payload['seeds']}`",
        f"- depths: `{payload['n_values']}`",
        "",
    ]

    for family in ["hallucination", "conflict", "unsafe", "benign"]:
        lines.append(f"## {family}")
        lines.append("")
        if family == "hallucination":
            lines.append("| Method | N=0 acc | N=1 unsupported | N=8 unsupported | N=16 unsupported | N=16 acc |")
            lines.append("|---|---:|---:|---:|---:|---:|")
            for architecture in payload["architectures"]:
                n0 = payload["snapshots"][architecture]["0"]["by_family"][family]
                n1 = payload["snapshots"][architecture]["1"]["by_family"][family]
                n8 = payload["snapshots"][architecture]["8"]["by_family"][family]
                n16 = payload["snapshots"][architecture]["16"]["by_family"][family]
                lines.append(
                    f"| {architecture} | {n0['accuracy']:.3f} | {n1['unsupported_answer_rate']:.3f} | "
                    f"{n8['unsupported_answer_rate']:.3f} | {n16['unsupported_answer_rate']:.3f} | {n16['accuracy']:.3f} |"
                )
        elif family == "conflict":
            lines.append("| Method | N=0 acc | N=1 wrong_current | N=8 wrong_current | N=16 wrong_current | N=16 acc |")
            lines.append("|---|---:|---:|---:|---:|---:|")
            for architecture in payload["architectures"]:
                n0 = payload["snapshots"][architecture]["0"]["by_family"][family]
                n1 = payload["snapshots"][architecture]["1"]["by_family"][family]
                n8 = payload["snapshots"][architecture]["8"]["by_family"][family]
                n16 = payload["snapshots"][architecture]["16"]["by_family"][family]
                lines.append(
                    f"| {architecture} | {n0['accuracy']:.3f} | {n1['conflict_answer_rate']:.3f} | "
                    f"{n8['conflict_answer_rate']:.3f} | {n16['conflict_answer_rate']:.3f} | {n16['accuracy']:.3f} |"
                )
        elif family == "unsafe":
            lines.append("| Method | N=0 refuse_fail | N=1 refuse_fail | N=8 refuse_fail | N=16 refuse_fail | N=16 raw escalation |")
            lines.append("|---|---:|---:|---:|---:|---:|")
            for architecture in payload["architectures"]:
                n0 = payload["snapshots"][architecture]["0"]["by_family"][family]
                n1 = payload["snapshots"][architecture]["1"]["by_family"][family]
                n8 = payload["snapshots"][architecture]["8"]["by_family"][family]
                n16 = payload["snapshots"][architecture]["16"]["by_family"][family]
                lines.append(
                    f"| {architecture} | {n0['unsafe_answer_rate']:.3f} | {n1['unsafe_answer_rate']:.3f} | "
                    f"{n8['unsafe_answer_rate']:.3f} | {n16['unsafe_answer_rate']:.3f} | {n16['raw_escalation_rate']:.3f} |"
                )
        else:
            lines.append("| Method | N=0 acc | N=1 history_loss | N=8 history_loss | N=16 history_loss | N=16 acc |")
            lines.append("|---|---:|---:|---:|---:|---:|")
            for architecture in payload["architectures"]:
                n0 = payload["snapshots"][architecture]["0"]["by_family"][family]
                n1 = payload["snapshots"][architecture]["1"]["by_family"][family]
                n8 = payload["snapshots"][architecture]["8"]["by_family"][family]
                n16 = payload["snapshots"][architecture]["16"]["by_family"][family]
                lines.append(
                    f"| {architecture} | {n0['accuracy']:.3f} | {n1['benign_overcompression_rate']:.3f} | "
                    f"{n8['benign_overcompression_rate']:.3f} | {n16['benign_overcompression_rate']:.3f} | {n16['accuracy']:.3f} |"
                )
        lines.append("")

    lines.extend(
        [
            "## Protected-Field Control",
            "",
            "| Method | Query-Aware | No-Rewrite | N=1 protected rate | N=1 blocked protected | N=8 blocked protected | N=16 blocked protected |",
            "|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for architecture in payload["architectures"]:
        n1 = payload["snapshots"][architecture]["1"]
        n8 = payload["snapshots"][architecture]["8"]
        n16 = payload["snapshots"][architecture]["16"]
        n1_blocked = "-" if n1["blocked_protected_case_rate"] is None else f"{n1['blocked_protected_case_rate']:.3f}"
        n8_blocked = "-" if n8["blocked_protected_case_rate"] is None else f"{n8['blocked_protected_case_rate']:.3f}"
        n16_blocked = "-" if n16["blocked_protected_case_rate"] is None else f"{n16['blocked_protected_case_rate']:.3f}"
        lines.append(
            f"| {architecture} | {'yes' if 'query_aware' in architecture else 'no'} | {'yes' if architecture.endswith('_no_rewrite') else 'no'} | "
            f"{n1['protected_case_rate']:.3f} | {n1_blocked} | {n8_blocked} | {n16_blocked} |"
        )
    lines.extend(["", "## Example Blocked Cases", ""])
    for family, examples in sorted(payload["examples"].items()):
        lines.append(f"### {family}")
        lines.append("")
        for example in examples:
            lines.append(
                f"- `{example['item_id']}` seed=`{example['seed']}` blocked=`{example['blocked_reasons']}` compact=`{example['compact_answer']}` final=`{example['final_answer']}`"
            )
        lines.append("")

    lines.extend(
        [
            "## Readout",
            "",
            "- The purpose of this artifact is to compare the V3 mechanism as a method, not just as a checklist item.",
            "- If `summary_only_no_rewrite` and `tiered_no_rewrite` suppress hallucination / conflict / unsafe failures at high `N` while keeping benign utility reasonable, that is the right local signal before wiring the same rule into the real TierMem path.",
            "- This artifact should still be treated as a proxy surface until the real TierMem and public-baseline experiments are live.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-no-rewrite-compare] wrote {repo_root / JSON_PATH}")
    print(f"[v3-no-rewrite-compare] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
