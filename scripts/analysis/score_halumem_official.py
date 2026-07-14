#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Score a TierMem --live output with the OFFICIAL HaluMem judge (Phase 3b).

Wraps the fiddly bits discovered while wiring the official scorer so a scale-up
run is one command instead of hand-assembly:

  * The official evaluation.py CLI only takes --frame (3rd-party systems) /
    --version and reads results/{frame}-{version}/{frame}_eval_results.jsonl --
    there is NO --file_path. We drive its process_user() directly on our jsonl.
  * The official aggregate_eval_results ZeroDivides when a memory_type has 0
    items (happens on small samples): we call it but tolerate that, and ALWAYS
    also emit a self-computed core summary from the raw judged records.
  * The judge (eval_tools -> llms) reads env at import time: OPENAI_API_KEY /
    OPENAI_BASE_URL / OPENAI_MODEL + RETRY_TIMES / WAIT_TIME_LOWER /
    WAIT_TIME_UPPER. We set sane defaults so import doesn't crash.

Usage (needs a real key; the judge costs API budget):
  set -a && source .env.v3 && set +a
  .venv_tiermem_v2/bin/python scripts/analysis/score_halumem_official.py \
      --filled outputs/safety/halumem_smoke_infer_s34.jsonl \
      --judge-model gpt-4.1-mini --max-workers 4
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EVAL_DIR = ROOT / "benchmarks" / "halumem" / "official_repo" / "eval"
RECORD_KEYS = (
    "memory_integrity_records", "memory_accuracy_records",
    "memory_update_records", "question_answering_records",
)


def _empty_eval_results() -> dict[str, Any]:
    """The shape evaluation.aggregate_eval_results mutates (mirrors main())."""
    mt = lambda: {"memory_integrity_acc": 0, "memory_update_acc": 0, "total_num": 0}
    return {
        "overall_score": {
            "memory_integrity": {}, "memory_accuracy": {}, "memory_extraction_f1": 0,
            "memory_update": {}, "question_answering": {},
            "memory_type_accuracy": {
                "Event Memory": mt(), "Persona Memory": mt(), "Relationship Memory": mt(),
            },
            "time_consuming": {"add_dialogue_duration_time": 0,
                               "search_memory_duration_time": 0, "total_duration_time": 0},
        },
        "memory_integrity_records": [], "memory_accuracy_records": [],
        "memory_update_records": [], "question_answering_records": [],
    }


def _core_summary(er: dict[str, Any]) -> dict[str, Any]:
    """Self-computed core metrics from raw judged records (never divides by zero)."""
    ii = [r.get("memory_integrity_score") for r in er["memory_integrity_records"]
          if r.get("memory_integrity_score") is not None]
    aa = [r.get("memory_accuracy_score") for r in er["memory_accuracy_records"]
          if r.get("memory_accuracy_score") is not None]
    uu = [r.get("memory_update_type") for r in er["memory_update_records"]]
    qq = [r.get("result_type") for r in er["question_answering_records"]]

    def dist(lst: list) -> dict[str, int]:
        return {str(v): lst.count(v) for v in sorted(set(lst), key=str)}

    def rate(lst: list, val: Any) -> float | None:
        return round(sum(1 for x in lst if x == val) / len(lst), 4) if lst else None

    return {
        "memory_integrity": {
            "n": len(ii), "mean_score": round(sum(ii) / len(ii), 4) if ii else None,
            "fully_covered_pct": rate(ii, 2), "covered_ge1_pct": round(
                sum(1 for x in ii if x >= 1) / len(ii), 4) if ii else None, "dist": dist(ii)},
        "memory_accuracy": {
            "n": len(aa), "mean_score": round(sum(aa) / len(aa), 4) if aa else None,
            "weighted_accuracy": round(0.5 * sum(aa) / len(aa), 4) if aa else None, "dist": dist(aa)},
        "memory_update": {
            "n": len(uu), "correct_pct": rate(uu, "Correct"), "dist": dist(uu)},
        "question_answering": {
            "n": len(qq), "correct_pct": rate(qq, "Correct"), "dist": dist(qq)},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Score a TierMem --live jsonl with the official HaluMem judge.")
    ap.add_argument("--filled", required=True, help="adapter --live output jsonl (all 3 system fields filled).")
    ap.add_argument("--out", default=None, help="scores json (default: <filled>.official_scores.json).")
    ap.add_argument("--user-num", type=int, default=0, help="0 = all users in the file.")
    ap.add_argument("--max-workers", type=int, default=4, help="official judge process pool size.")
    ap.add_argument("--judge-model", default="gpt-4.1-mini", help="OPENAI_MODEL for the official judge.")
    args = ap.parse_args()

    filled = Path(args.filled).expanduser().resolve()
    if not filled.exists():
        raise FileNotFoundError(filled)

    # judge env must be set BEFORE importing evaluation (llms reads it at import time)
    os.environ.setdefault("RETRY_TIMES", "3")
    os.environ.setdefault("WAIT_TIME_LOWER", "1")
    os.environ.setdefault("WAIT_TIME_UPPER", "3")
    os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL") or args.judge_model
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not set (source .env.v3) -- the official judge costs API budget.")
    # make eval/ importable in this process AND in spawned judge workers
    os.environ["PYTHONPATH"] = str(EVAL_DIR) + os.pathsep + os.environ.get("PYTHONPATH", "")
    sys.path.insert(0, str(EVAL_DIR))
    os.chdir(EVAL_DIR)  # mirror the working dir the official code expects

    from evaluation import process_user, aggregate_eval_results, iter_jsonl  # type: ignore

    er = _empty_eval_results()
    users = list(iter_jsonl(str(filled)))
    if args.user_num:
        users = users[: args.user_num]
    for idx, u in enumerate(users, 1):
        result = process_user(idx, u, args.max_workers)
        for k in RECORD_KEYS:
            er[k].extend(result.get(k, []))

    try:
        aggregate_eval_results(er)
    except ZeroDivisionError:
        er["overall_score"]["_note"] = (
            "official aggregate_eval_results ZeroDivided on a memory_type with 0 items "
            "(small sample); integrity/accuracy/update/QA below are self-computed.")

    summary = _core_summary(er)
    out = Path(args.out).expanduser().resolve() if args.out else filled.with_name(
        filled.stem + ".official_scores.json")
    out.write_text(json.dumps(
        {"file": str(filled), "users_scored": len(users), "core": summary,
         "overall_score": er.get("overall_score", {})}, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"users_scored": len(users), "core": summary}, ensure_ascii=False, indent=2))
    print("saved:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
