#!/usr/bin/env python3
"""RT-02 shared utilities: official-module import, source correction, snapshots, judges, stats.

Design contract (state/rt02_baseline_design_20260718.md):
- All unsafe verdicts come from the OFFICIAL MemEvoBench judge prompts, never custom rubrics.
- Correction text = published fields only (QA: memory's `correct_answer`; WF: `correct_workflow`).
- Correction keeps `timestamp`/`id` unchanged so serialized prompts stay byte-identical with the
  safe-history branch (deviation from tool_correct_memory's timestamp refresh, declared in design §4.1).
"""
import hashlib
import json
import os
import random
import sys
from copy import deepcopy

MEMEVO_ROOT = "/Users/yihaiwen/Documents/New project/memevobench_official"
if MEMEVO_ROOT not in sys.path:
    sys.path.insert(0, MEMEVO_ROOT)

import iterative_memory_triplequery_test as offi  # noqa: E402  (official QA pipeline, unmodified semantics)

# type -> content field carrying the memory's main text (mirrors offi.get_memory_content)
CONTENT_FIELD = {
    "knowledge": "content",
    "conversation": "assistant",
    "note": "note",
    "forum": "post",
}


def make_clients():
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY not set — source .env.v3 first")
    return OpenAI(api_key=api_key, base_url=base_url)


def snapshot_hash(memories):
    return hashlib.sha256(
        json.dumps(memories, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]


def prompt_view(memories):
    """Exactly what the model sees (official serialization)."""
    return offi.format_memories_for_prompt(memories)


def correct_qa_sources(memories):
    """Source correction on a QA memory pool, official published text only.

    Replaces each label=='misleading' record's content field with its published
    `correct_answer`. id/timestamp untouched -> prompt serialization byte-identical
    to a safe-history pool built the same way at t=0.
    Returns number of records corrected.
    """
    n = 0
    for mem in memories:
        if mem.get("label") == "misleading" and mem.get("correct_answer"):
            field = CONTENT_FIELD.get((mem.get("type") or "").lower())
            if not field:
                continue
            mem[field] = mem["correct_answer"]
            mem["label"] = "correct"          # bookkeeping; not serialized into prompt
            mem["status"] = "corrected_source"  # bookkeeping; not serialized into prompt
            n += 1
    return n


def full_closure_qa(memories, query_to_correct_answer):
    """Evidence-rewrite every generated descendant with the published test_correct_answer
    of the query that produced it. Published fields only; deterministic."""
    n = 0
    for mem in memories:
        if mem.get("type") == "conversation" and mem.get("label_source") == "rt02_descendant":
            ca = query_to_correct_answer.get(mem.get("user_request", ""))
            if ca:
                mem["assistant"] = ca
                mem["status"] = "closure_rewritten"
                mem["user_feedback"] = ""
                n += 1
    return n


def judge_qa(client, judge_model, query, risk_type, correct_answer, response):
    """Official QA judge (JUDGE_RESPONSE_PROMPT). Returns (unsafe:int, label, reason)."""
    label, reason = offi.judge_response_correctness(
        client, judge_model, query, risk_type, correct_answer, response, temperature=0
    )
    return (1 if label == "misleading" else 0), label, reason


def paired_bootstrap_ci(case_deltas, n_boot=10000, seed=20260718):
    """Percentile bootstrap CI for the mean of per-case paired deltas."""
    rng = random.Random(seed)
    vals = list(case_deltas)
    if not vals:
        return None
    n = len(vals)
    means = []
    for _ in range(n_boot):
        s = [vals[rng.randrange(n)] for _ in range(n)]
        means.append(sum(s) / n)
    means.sort()
    return {
        "mean": sum(vals) / n,
        "ci_lo": means[int(0.025 * n_boot)],
        "ci_hi": means[int(0.975 * n_boot)],
        "n_cases": n,
    }
