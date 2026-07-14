#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ2 dataset builder: stratified four-family question-type sampling for HaluMem.

Stops the head-truncation (run_v2_tiermem_micro_slice.py --session-limit/--qa-limit)
that systematically dropped hard question types (multi-hop / temporal / conflict).
Builds per-family candidate pools across ALL sessions and samples a quota per
family, so RQ2 covers the benchmark's real question-type mix instead of only easy
single-hop short-answer + abstention.

Family map (HaluMem question_type -> RQ2 family), verified against the golden mix
(Medium, 3467 QA): single_hop=Basic Fact Recall(746) multi_hop=Multi-hop Inference(198)
temporal_update=Dynamic Update(180) conflict=Memory Conflict(769) abstention=Memory
Boundary(828, gold=Unknown/evidence empty). Held out of the main test:
Generalization & Application(746) -- kept out to avoid judge-subjective contamination.

`stratified_slice` is deterministic under --seed and reusable both from the runner
(on loader qa_pairs) and from this file's offline --dry preview (on golden jsonl).
"""
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
HELD_OUT = "Generalization & Application"


def _is_abstention(qa: dict[str, Any]) -> bool:
    """Memory Boundary positive: gold says unknown / not provided, evidence empty."""
    if qa.get("question_type") != "Memory Boundary":
        return False
    gt = str(qa.get("ground_truth") or qa.get("answer") or "").strip().lower()
    ev = qa.get("evidence") or []
    return (not ev) and (gt.startswith("unknown") or "not provided" in gt)


FAMILIES: dict[str, Callable[[dict[str, Any]], bool]] = {
    "single_hop":      lambda q: q.get("question_type") == "Basic Fact Recall",
    "multi_hop":       lambda q: q.get("question_type") == "Multi-hop Inference",
    "temporal_update": lambda q: q.get("question_type") == "Dynamic Update",
    "conflict":        lambda q: q.get("question_type") == "Memory Conflict",
    "abstention":      _is_abstention,
}

# Phase-2 minimal-compliant default (~120 QA; multi_hop/temporal are scarce ~10/user).
DEFAULT_QUOTA = {"single_hop": 30, "multi_hop": 30, "temporal_update": 30,
                 "conflict": 15, "abstention": 15}


def parse_quota(spec: str | None) -> dict[str, int]:
    if not spec:
        return dict(DEFAULT_QUOTA)
    out: dict[str, int] = {}
    for part in spec.split(","):
        k, _, v = part.strip().partition("=")
        k = k.strip()
        if k in FAMILIES and v.strip().lstrip("-").isdigit():
            out[k] = int(v)
    return out or dict(DEFAULT_QUOTA)


def stratified_slice(sessions: list[dict[str, Any]], quota: dict[str, int],
                     seed: int | None, families: dict[str, Callable] = FAMILIES,
                     ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return (sessions with only the chosen qa_pairs, report). Deterministic under seed.

    Each chosen qa gets an `rq2_family` tag. A qa is assigned to the FIRST matching
    family (order = quota insertion order), so families stay disjoint.
    """
    rng = random.Random(seed)
    buckets: dict[str, list[tuple[int, dict]]] = {fam: [] for fam in quota}
    for si, sess in enumerate(sessions):
        for qa in sess.get("qa_pairs", []) or []:
            for fam in quota:
                if families[fam](qa):
                    buckets[fam].append((si, qa))
                    break
    chosen: dict[int, list[dict]] = defaultdict(list)
    report: dict[str, Any] = {}
    for fam, n in quota.items():
        cands = buckets.get(fam, [])
        pick = list(cands) if (n <= 0 or n >= len(cands)) else rng.sample(cands, n)
        report[fam] = {"available": len(cands), "picked": len(pick),
                       "short": max(0, n - len(cands))}
        for si, qa in pick:
            qa2 = dict(qa)
            qa2["rq2_family"] = fam
            chosen[si].append(qa2)
    out: list[dict[str, Any]] = []
    for si, sess in enumerate(sessions):
        if si in chosen:
            c = dict(sess)
            c["qa_pairs"] = chosen[si]
            out.append(c)
    report["_sessions_touched"] = len(out)
    report["_total_qa"] = sum(len(v) for v in chosen.values())
    return out, report


def _golden_as_sessions(split: str = "Medium", pool: int = 0) -> list[dict[str, Any]]:
    """OFFLINE: load golden jsonl into loader-shaped sessions (one per user) for --dry.

    Uses the same qa fields the loader emits (question_type/evidence/ground_truth),
    so the family logic tested here matches the runtime path exactly.
    """
    p = ROOT / "benchmarks" / "halumem" / "official_repo" / "data" / f"HaluMem-{split}.jsonl"
    sessions: list[dict[str, Any]] = []
    with p.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            if pool and i >= pool:
                break
            line = line.strip()
            if not line:
                continue
            u = json.loads(line)
            qa_pairs = []
            for s in u.get("sessions", []):
                for q in s.get("questions", []) or []:
                    qa_pairs.append({
                        "question": q.get("question", ""),
                        "ground_truth": q.get("answer", ""),
                        "question_type": q.get("question_type", ""),
                        "evidence": q.get("evidence", []),
                    })
            sessions.append({"session_id": u.get("uuid"), "qa_pairs": qa_pairs})
    return sessions


def main() -> int:
    ap = argparse.ArgumentParser(description="RQ2 four-family stratified sampler (offline dry preview).")
    ap.add_argument("--split", default="Medium")
    ap.add_argument("--pool", type=int, default=0, help="0 = all users.")
    ap.add_argument("--family-quota", default=None, help="e.g. single_hop=30,multi_hop=30,conflict=15,...")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--dry", action="store_true", help="OFFLINE: report per-family availability/picked; no LLM.")
    ap.add_argument("--show", type=int, default=0, help="print N sample questions per family.")
    args = ap.parse_args()

    quota = parse_quota(args.family_quota)
    sessions = _golden_as_sessions(args.split, args.pool)
    sliced, report = stratified_slice(sessions, quota, args.seed)
    print(json.dumps({"quota": quota, "report": report}, ensure_ascii=False, indent=2))

    if args.show:
        seen: dict[str, int] = defaultdict(int)
        for sess in sliced:
            for qa in sess["qa_pairs"]:
                fam = qa["rq2_family"]
                if seen[fam] < args.show:
                    seen[fam] += 1
                    print(f"  [{fam}] {str(qa.get('question',''))[:70]!r} -> {str(qa.get('ground_truth',''))[:40]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
