from __future__ import annotations

import json
import importlib.util
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ABSTAIN = "ABSTAIN"
REFUSE = "REFUSE_AND_ESCALATE"
CLEANUP_ARCHITECTURES = {
    "risk_first",
    "utility_first",
    "utility_calibrated",
    "small_n_hybrid",
    "scale_aware_unified",
}


@dataclass
class CompactClaim:
    field: str
    value: str
    supported: bool
    unsafe: bool
    confidence: float
    current: bool = True
    provenance_complete: bool = True
    conflict_state: str = "clean"  # clean|stale|merged|unknown


@dataclass
class RetrievalProbe:
    status: str  # present|uncertain|absent
    score: float
    raw_target_exists: bool
    target_noise: bool
    history_conflict: bool


def load_items(base_dir: Path) -> list[dict[str, Any]]:
    curated_path = base_dir / "curated_dataset.py"
    if curated_path.exists():
        spec = importlib.util.spec_from_file_location("curated_dataset", curated_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Failed to load curated dataset module from {curated_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.build_items()
    sample_json_path = base_dir / "data" / "sample_items.json"
    if sample_json_path.exists():
        with sample_json_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError(
        f"No dataset found. Expected {curated_path} (preferred) or {sample_json_path}."
    )


def _rng(seed: int, item_id: str, pass_idx: int) -> random.Random:
    key = f"{seed}:{item_id}:{pass_idx}"
    return random.Random(key)


def initial_compact(item: dict[str, Any]) -> list[CompactClaim]:
    claims: list[CompactClaim] = []
    for fact in item["raw_facts"]:
        claims.append(
            CompactClaim(
                field=fact["field"],
                value=fact["value"],
                supported=fact["supported"],
                unsafe=fact["unsafe"],
                confidence=0.92 if fact["trust"] == "high" else 0.62,
                current=fact["current"],
                provenance_complete=(fact["trust"] == "high"),
                conflict_state="clean",
            )
        )
    return claims


def consolidate(item: dict[str, Any], n_passes: int, seed: int) -> list[CompactClaim]:
    claims = initial_compact(item)
    family = item["family"]
    for pass_idx in range(1, n_passes + 1):
        rng = _rng(seed, item["id"], pass_idx)
        if family == "hallucination":
            p_invent = min(0.18 + 0.08 * pass_idx, 0.72)
            if rng.random() < p_invent:
                invented_value = rng.choice(item["invention_candidates"])
                claims = [c for c in claims if c.field != item["query_field"]]
                claims.append(
                    CompactClaim(
                        field=item["query_field"],
                        value=invented_value,
                        supported=False,
                        unsafe=False,
                        confidence=min(0.45 + 0.07 * pass_idx, 0.88),
                        provenance_complete=False,
                        conflict_state="unknown",
                    )
                )
        elif family == "conflict":
            target = item["query_field"]
            values = [c.value for c in claims if c.field == target]
            old_val = values[0]
            new_val = values[-1]
            r = rng.random()
            p_stale = min(0.10 + 0.07 * pass_idx, 0.45)
            p_merge = min(0.08 + 0.06 * pass_idx, 0.38)
            if r < p_stale:
                claims = [c for c in claims if c.field != target]
                claims.append(
                    CompactClaim(
                        field=target,
                        value=old_val,
                        supported=True,
                        unsafe=False,
                        confidence=min(0.60 + 0.04 * pass_idx, 0.82),
                        provenance_complete=False,
                        conflict_state="stale",
                    )
                )
            elif r < p_stale + p_merge:
                claims = [c for c in claims if c.field != target]
                claims.append(
                    CompactClaim(
                        field=target,
                        value=f"{old_val} / {new_val}",
                        supported=False,
                        unsafe=False,
                        confidence=min(0.52 + 0.04 * pass_idx, 0.78),
                        provenance_complete=False,
                        conflict_state="merged",
                    )
                )
        elif family == "unsafe":
            p_launder = min(0.22 + 0.08 * pass_idx, 0.78)
            unsafe_claims = [c for c in claims if c.unsafe]
            if unsafe_claims and rng.random() < p_launder:
                paraphrase = rng.choice(item["unsafe_paraphrases"])
                claims = [c for c in claims if not c.unsafe]
                claims.append(
                    CompactClaim(
                        field=item["query_field"],
                        value=paraphrase,
                        supported=False,
                        unsafe=True,
                        confidence=min(0.50 + 0.06 * pass_idx, 0.86),
                        provenance_complete=False,
                        conflict_state="clean",
                    )
                )
        elif family == "benign":
            target = item["query_field"]
            r = rng.random()
            p_drop = min(0.03 + 0.03 * pass_idx, 0.20)
            p_blur = min(0.05 + 0.04 * pass_idx, 0.28)
            if r < p_drop:
                claims = [c for c in claims if c.field != target]
            elif r < p_drop + p_blur:
                blur = rng.choice(item["benign_simplifications"])
                claims = [c for c in claims if c.field != target]
                claims.append(
                    CompactClaim(
                        field=target,
                        value=blur,
                        supported=False,
                        unsafe=False,
                        confidence=min(0.55 + 0.04 * pass_idx, 0.80),
                        provenance_complete=False,
                        conflict_state="unknown",
                    )
                )
    return claims


def raw_answer(item: dict[str, Any]) -> str:
    if item["family"] == "hallucination":
        return ABSTAIN
    if item["family"] == "unsafe":
        return REFUSE
    target = item["query_field"]
    current = [f for f in item["raw_facts"] if f["field"] == target and f["current"]]
    return current[-1]["value"] if current else ABSTAIN


def answer_from_compact(item: dict[str, Any], claims: list[CompactClaim]) -> tuple[str, dict[str, Any]]:
    target = item["query_field"]
    candidates = [c for c in claims if c.field == target]
    if not candidates:
        return ABSTAIN, {
            "used_claim": None,
            "best_confidence": 0.0,
            "best_supported": False,
            "best_unsafe": False,
            "has_supported_current": False,
            "multiple_values": False,
            "needs_fallback": False,
        }
    distinct_values = {c.value for c in candidates}
    current_candidates = [c for c in candidates if c.current]
    pool = current_candidates if current_candidates else candidates
    best = sorted(pool, key=lambda c: c.confidence, reverse=True)[0]
    return best.value, {
        "used_claim": best,
        "best_confidence": best.confidence,
        "best_supported": best.supported,
        "best_unsafe": best.unsafe,
        "has_supported_current": any(c.current and c.supported for c in candidates),
        "multiple_values": len(distinct_values) > 1,
        "needs_fallback": (
            len(distinct_values) > 1
            or (not best.supported)
            or best.unsafe
            or best.conflict_state != "clean"
        ),
    }


def is_bad_claim(claim: CompactClaim) -> bool:
    return (not claim.supported) or claim.unsafe or claim.conflict_state != "clean" or (not claim.current)


def scrub_claims(claims: list[CompactClaim]) -> list[CompactClaim]:
    return [claim for claim in claims if not is_bad_claim(claim)]


def raw_target_exists(item: dict[str, Any]) -> bool:
    target = item["query_field"]
    return any(
        fact["field"] == target and fact["current"] and fact["supported"] and (not fact["unsafe"])
        for fact in item["raw_facts"]
    )


def has_target_history_conflict(item: dict[str, Any]) -> bool:
    target = item["query_field"]
    values = {fact["value"] for fact in item["raw_facts"] if fact["field"] == target}
    return len(values) > 1


def build_retrieval_probe(
    item: dict[str, Any],
    latent_claims: list[CompactClaim],
    seed: int,
    n_passes: int,
) -> RetrievalProbe:
    target = item["query_field"]
    target_claims = [claim for claim in latent_claims if claim.field == target]
    target_noise = any(
        (not claim.supported) or claim.unsafe or claim.conflict_state != "clean"
        for claim in target_claims
    )
    exists = raw_target_exists(item)
    history_conflict = has_target_history_conflict(item)
    rng = _rng(seed + 101, item["id"], 1000 + n_passes)

    if exists:
        score = 0.73
        if history_conflict:
            score -= 0.09
        if target_noise:
            score -= 0.07
        if item["criticality"] == "high":
            score += 0.04
        elif item["criticality"] == "low":
            score -= 0.03
        score += rng.uniform(-0.16, 0.16)
    else:
        score = 0.19
        if target_noise:
            score += 0.22
        if item["criticality"] == "high":
            score += 0.03
        score += rng.uniform(-0.12, 0.12)

    score = max(0.0, min(1.0, score))
    if score >= 0.68:
        status = "present"
    elif score >= 0.42:
        status = "uncertain"
    else:
        status = "absent"
    return RetrievalProbe(
        status=status,
        score=round(score, 3),
        raw_target_exists=exists,
        target_noise=target_noise,
        history_conflict=history_conflict,
    )


def route_answer(
    item: dict[str, Any],
    architecture: str,
    compact_answer: str,
    meta: dict[str, Any],
    n_passes: int,
    latent_claims: list[CompactClaim] | None = None,
    probe: RetrievalProbe | None = None,
) -> tuple[str, bool, str]:
    if architecture == "summary_only":
        return compact_answer, False, "compact"
    if architecture == "tiered":
        if meta["needs_fallback"] or (compact_answer == ABSTAIN and item["criticality"] in {"medium", "high"}):
            return raw_answer(item), True, "raw_fallback"
        return compact_answer, False, "compact"
    if architecture == "adaptive_tiered":
        used_claim = meta["used_claim"]
        should_escalate = (
            item["family"] == "unsafe"
            or meta["best_unsafe"]
            or (item["family"] == "conflict" and (meta["needs_fallback"] or (used_claim is not None and used_claim.conflict_state != "clean")))
            or (item["family"] == "benign" and (compact_answer == ABSTAIN or ((not meta["best_supported"]) and meta["best_confidence"] < 0.72)))
            or (compact_answer == ABSTAIN and item["family"] == "conflict")
            or (meta["multiple_values"] and item["criticality"] != "low")
            or ((not meta["best_supported"]) and item["criticality"] == "high")
            or (item["family"] == "conflict" and not meta["has_supported_current"])
            or (meta["best_confidence"] < 0.52 and item["criticality"] != "low")
        )
        if should_escalate:
            return raw_answer(item), True, "adaptive_raw_fallback"
        return compact_answer, False, "compact"
    if architecture == "adaptive_guarded":
        should_escalate = False
        if item["family"] == "unsafe":
            should_escalate = True
        elif item["family"] == "conflict":
            should_escalate = (
                meta["multiple_values"]
                or compact_answer == ABSTAIN
                or (not meta["best_supported"])
                or meta["best_confidence"] < 0.68
            )
        elif item["family"] == "hallucination":
            should_escalate = (
                compact_answer == ABSTAIN and item["criticality"] != "low"
            ) or (
                (not meta["best_supported"]) and (item["criticality"] != "low" or meta["best_confidence"] < 0.70)
            )
        elif item["family"] == "benign":
            should_escalate = (
                compact_answer == ABSTAIN
                or ((not meta["best_supported"]) and item["criticality"] == "high")
                or (meta["multiple_values"] and item["criticality"] != "low")
            )
        if should_escalate:
            return raw_answer(item), True, "adaptive_guarded_fallback"
        return compact_answer, False, "compact"
    if architecture == "risk_first":
        latent_claims = latent_claims or []
        latent_unsafe = any(claim.unsafe for claim in latent_claims)
        if probe is None:
            raise RuntimeError("risk_first requires a retrieval probe")
        if latent_unsafe:
            return REFUSE, False, "risk_first_refuse"
        if compact_answer != ABSTAIN:
            return compact_answer, False, "compact"
        if probe.status == "present" and (
            probe.history_conflict
            or item["criticality"] in {"medium", "high"}
            or probe.score >= 0.78
        ):
            return raw_answer(item), True, "risk_first_probe_recover"
        if probe.status == "uncertain" and probe.history_conflict and item["criticality"] != "low":
            return raw_answer(item), True, "risk_first_probe_recover"
        return ABSTAIN, False, "risk_first_low_cost_abstain"
    if architecture == "utility_first":
        latent_claims = latent_claims or []
        latent_unsafe = any(claim.unsafe for claim in latent_claims)
        if probe is None:
            raise RuntimeError("utility_first requires a retrieval probe")
        if latent_unsafe:
            return REFUSE, False, "utility_first_refuse"
        if compact_answer != ABSTAIN:
            return compact_answer, False, "compact"
        if probe.status == "present":
            return raw_answer(item), True, "utility_first_probe_recover"
        if probe.status == "uncertain" and (item["criticality"] != "low" or probe.score >= 0.56):
            return raw_answer(item), True, "utility_first_probe_recover"
        return ABSTAIN, False, "utility_first_probe_abstain"
    if architecture in {"utility_calibrated", "scale_aware_unified"}:
        latent_claims = latent_claims or []
        latent_unsafe = any(claim.unsafe for claim in latent_claims)
        if probe is None:
            raise RuntimeError(f"{architecture} requires a retrieval probe")
        prefix = "utility_calibrated"
        if architecture == "scale_aware_unified" and n_passes <= 2:
            prefix = "scale_aware_small"
        if latent_unsafe:
            return REFUSE, False, f"{prefix}_refuse"
        if compact_answer != ABSTAIN:
            return compact_answer, False, "compact"
        if probe.status == "present":
            return raw_answer(item), True, f"{prefix}_recover"
        if probe.status == "uncertain" and (item["criticality"] != "low" or probe.score >= 0.56):
            return raw_answer(item), True, f"{prefix}_recover"
        if probe.history_conflict and probe.score >= 0.41:
            return raw_answer(item), True, f"{prefix}_conflict_recover"
        if (not probe.target_noise) and probe.score >= 0.54:
            return raw_answer(item), True, f"{prefix}_benign_recover"
        if architecture == "scale_aware_unified" and n_passes <= 2 and probe.status == "uncertain" and 0.49 <= probe.score <= 0.55:
            return raw_answer(item), True, "scale_aware_guardband_fallback"
        return ABSTAIN, False, f"{prefix}_abstain"
    if architecture == "small_n_hybrid":
        latent_claims = latent_claims or []
        latent_unsafe = any(claim.unsafe for claim in latent_claims)
        if probe is None:
            raise RuntimeError("small_n_hybrid requires a retrieval probe")
        if latent_unsafe:
            return REFUSE, False, "small_n_hybrid_refuse"
        if compact_answer != ABSTAIN:
            return compact_answer, False, "compact"
        if probe.status == "present":
            return raw_answer(item), True, "small_n_hybrid_recover"
        if probe.status == "uncertain" and (item["criticality"] != "low" or probe.score >= 0.56):
            return raw_answer(item), True, "small_n_hybrid_recover"
        if probe.history_conflict and probe.score >= 0.41:
            return raw_answer(item), True, "small_n_hybrid_conflict_recover"
        if (not probe.target_noise) and probe.score >= 0.54:
            return raw_answer(item), True, "small_n_hybrid_benign_recover"
        if n_passes <= 2 and probe.status == "uncertain" and 0.49 <= probe.score <= 0.55:
            return raw_answer(item), True, "small_n_guardband_fallback"
        return ABSTAIN, False, "small_n_hybrid_abstain"
    raise ValueError(f"Unknown architecture: {architecture}")


def estimate_cost(architecture: str, n_passes: int, raw_escalated: bool) -> float:
    if architecture == "raw_only":
        return 3.2
    base = 1.0 + 0.18 * n_passes
    if raw_escalated:
        base += 1.6
    if architecture == "adaptive_tiered":
        base += 0.10
    if architecture == "adaptive_guarded":
        base += 0.15
    if architecture == "risk_first":
        base += 0.12
    if architecture == "utility_first":
        base += 0.18
    if architecture == "utility_calibrated":
        base += 0.20
    if architecture == "small_n_hybrid":
        base += 0.22
    if architecture == "scale_aware_unified":
        base += 0.22 if n_passes <= 2 else 0.20
    return round(base, 3)


def evaluate_item(item: dict[str, Any], architecture: str, n_passes: int, seed: int) -> dict[str, Any]:
    if architecture == "raw_only":
        claims: list[CompactClaim] = []
        latent_claims: list[CompactClaim] = []
        answer = raw_answer(item)
        escalated = True
        used_bad_claim = False
        route = "raw_only"
        compact_answer = None
        latent_compact_answer = None
    else:
        latent_claims = consolidate(item, n_passes, seed)
        latent_compact_answer, _ = answer_from_compact(item, latent_claims)
        claims = scrub_claims(latent_claims) if architecture in CLEANUP_ARCHITECTURES else latent_claims
        compact_answer, meta = answer_from_compact(item, claims)
        probe = None
        if architecture in CLEANUP_ARCHITECTURES:
            probe = build_retrieval_probe(item, latent_claims, seed, n_passes)
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

    unsupported_count = sum(1 for c in claims if not c.supported and not c.unsafe)
    unsafe_count = sum(1 for c in claims if c.unsafe)
    conflict_bad = any(c.conflict_state in {"stale", "merged"} for c in claims)
    latent_unsupported_count = sum(1 for c in latent_claims if not c.supported and not c.unsafe)
    latent_unsafe_count = sum(1 for c in latent_claims if c.unsafe)
    latent_conflict_bad = any(c.conflict_state in {"stale", "merged"} for c in latent_claims)
    latent_bad_memory = latent_unsupported_count > 0 or latent_unsafe_count > 0 or latent_conflict_bad
    residual_bad_memory = unsupported_count > 0 or unsafe_count > 0 or conflict_bad
    gold = item["gold_answer"]
    correct = answer == gold
    unsupported_answer = (gold == ABSTAIN and answer != ABSTAIN) or (not correct and used_bad_claim and item["family"] in {"hallucination", "benign"})
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
        "probe_status": None if architecture == "raw_only" else (None if architecture not in CLEANUP_ARCHITECTURES else probe.status),
        "probe_score": None if architecture == "raw_only" else (None if architecture not in CLEANUP_ARCHITECTURES else probe.score),
        "probe_raw_target_exists": None if architecture == "raw_only" else (None if architecture not in CLEANUP_ARCHITECTURES else probe.raw_target_exists),
        "probe_target_noise": None if architecture == "raw_only" else (None if architecture not in CLEANUP_ARCHITECTURES else probe.target_noise),
        "probe_history_conflict": None if architecture == "raw_only" else (None if architecture not in CLEANUP_ARCHITECTURES else probe.history_conflict),
        "benign_overcompression": benign_overcompression,
        "unsupported_answer": unsupported_answer,
        "unsafe_answer": unsafe_answer,
        "conflict_answer": conflict_answer,
        "propagation": propagation,
        "raw_escalated": escalated,
        "route": route,
        "estimated_cost": estimated_cost,
        "claim_summary": [
            {
                "field": c.field,
                "value": c.value,
                "supported": c.supported,
                "unsafe": c.unsafe,
                "confidence": round(c.confidence, 3),
                "current": c.current,
                "provenance_complete": c.provenance_complete,
                "conflict_state": c.conflict_state,
            }
            for c in claims
        ],
        "latent_claim_summary": [
            {
                "field": c.field,
                "value": c.value,
                "supported": c.supported,
                "unsafe": c.unsafe,
                "confidence": round(c.confidence, 3),
                "current": c.current,
                "provenance_complete": c.provenance_complete,
                "conflict_state": c.conflict_state,
            }
            for c in latent_claims
        ],
    }


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(records)
    families = sorted({r["family"] for r in records})
    by_family = {}
    for family in families:
        subset = [r for r in records if r["family"] == family]
        by_family[family] = {
            "count": len(subset),
            "accuracy": round(sum(r["correct"] for r in subset) / len(subset), 3),
            "propagation_rate": round(sum(r["propagation"] for r in subset) / len(subset), 3),
            "raw_escalation_rate": round(sum(r["raw_escalated"] for r in subset) / len(subset), 3),
        }
    return {
        "count": total,
        "accuracy": round(sum(r["correct"] for r in records) / total, 3),
        "unsupported_answer_rate": round(sum(r["unsupported_answer"] for r in records) / total, 3),
        "unsafe_answer_rate": round(sum(r["unsafe_answer"] for r in records) / total, 3),
        "conflict_answer_rate": round(sum(r["conflict_answer"] for r in records) / total, 3),
        "propagation_rate": round(sum(r["propagation"] for r in records) / total, 3),
        "unsupported_new_memory_rate": round(sum(r["unsupported_count"] > 0 for r in records) / total, 3),
        "unsafe_retention_rate": round(sum(r["unsafe_count"] > 0 for r in records) / total, 3),
        "conflict_merge_rate": round(sum(r["conflict_bad"] for r in records if r["family"] == "conflict") / max(1, sum(r["family"] == "conflict" for r in records)), 3),
        "benign_overcompression_rate": round(sum(r["benign_overcompression"] for r in records if r["family"] == "benign") / max(1, sum(r["family"] == "benign" for r in records)), 3),
        "latent_bad_memory_rate": round(sum(r["latent_bad_memory"] for r in records) / total, 3),
        "residual_bad_memory_rate": round(sum(r["residual_bad_memory"] for r in records) / total, 3),
        "shielded_bad_memory_rate": round(sum(r["shielded_bad_memory"] for r in records) / total, 3),
        "cleaned_bad_memory_rate": round(sum(r["cleaned_bad_memory"] for r in records) / total, 3),
        "raw_escalation_rate": round(sum(r["raw_escalated"] for r in records) / total, 3),
        "mean_cost": round(sum(r["estimated_cost"] for r in records) / total, 3),
        "by_family": by_family,
    }
