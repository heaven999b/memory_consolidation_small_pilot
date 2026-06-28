from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import freeze_external_benchmark_slices as core


LONGMEMEVAL_SOURCE = "benchmarks/locomo/longmemeval_official/data/cleaned/longmemeval_s_cleaned.json"

HALUMEM_HOLDOUT_PATH = "benchmarks/halumem/frozen_slices/halumem_hallucination_holdout_slice_v1.json"
LONGMEMEVAL_SLICE_PATH = "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_slice_v1.json"
REVIEW_PATH = "reviews/external_benchmark_slice_audit_round34.md"

HALUMEM_HOLDOUT_INDEXES = [9, 10, 11, 14, 15, 16, 17, 19]
LONGMEMEVAL_SELECTIONS = [
    "e47becba",  # Business Administration
    "51a45a95",  # Target
    "1e043500",  # Summer Vibes
    "c5e8278d",  # Johnson
    "6ade9755",  # Serenity Yoga
    "7527f7e2",  # $800
    "ad7109d1",  # 500 Mbps
    "c8c3f81d",  # Nike
]


def load_longmemeval_records(base_dir: Path) -> list[dict[str, Any]]:
    return json.loads((base_dir / LONGMEMEVAL_SOURCE).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_halumem_holdout_item(record: dict[str, Any], source_index: int, index: int) -> dict[str, Any]:
    item = core.build_halumem_item(record, source_index, index)
    item["id"] = f"halumem_holdout_{index + 1:02d}"
    item["source_provenance"]["benchmark_slice_role"] = "holdout_expansion"
    item["selection_notes"] = [
        "Official HaluMem holdout persona record chosen after the primary v2 slice, with three clean full-name support relationship clues.",
        "This expansion slice uses the same explicit-designation unsupported target as the primary HaluMem slice so the broader benchmark section stays schema-aligned while covering distinct source personas.",
    ]
    return item


def build_halumem_holdout_manifest(base_dir: Path) -> dict[str, Any]:
    records = core.load_halumem_records(base_dir)
    items = [
        build_halumem_holdout_item(records[source_index], source_index, idx)
        for idx, source_index in enumerate(HALUMEM_HOLDOUT_INDEXES)
    ]
    return {
        "adapter_id": "halumem_hallucination_holdout_slice",
        "version": "v1",
        "retrieval_date": str(date.today()),
        "selection_policy": {
            "target_size": len(HALUMEM_HOLDOUT_INDEXES),
            "source_type": "official_hallucination_benchmark_record",
            "rule": "Take a disjoint holdout set of official HaluMem personas after the primary v2 slice, keep only rows with three clean full-name support clues, and preserve the same explicit-designation unsupported target so the reviewer section broadens coverage without changing the task contract.",
        },
        "items": items,
    }


def find_longmemeval_record(records: list[dict[str, Any]], question_id: str) -> dict[str, Any]:
    for record in records:
        if record["question_id"] == question_id:
            return record
    raise RuntimeError(f"Missing LongMemEval question_id: {question_id}")


def answer_session(record: dict[str, Any]) -> tuple[str, str, list[dict[str, Any]]]:
    answer_ids = record.get("answer_session_ids", [])
    if len(answer_ids) != 1:
        raise RuntimeError(f"Expected exactly one answer session id for {record['question_id']}, got {answer_ids}")
    target = answer_ids[0]
    for session_id, session_date, session_rows in zip(
        record["haystack_session_ids"],
        record["haystack_dates"],
        record["haystack_sessions"],
    ):
        if session_id == target:
            return session_id, session_date, session_rows
    raise RuntimeError(f"Could not locate answer session {target} for {record['question_id']}")


def context_window(session_rows: list[dict[str, Any]]) -> list[int]:
    marked = [idx for idx, row in enumerate(session_rows) if row.get("has_answer")]
    if not marked:
        raise RuntimeError("Expected at least one answer-bearing turn in LongMemEval session.")
    start = max(0, min(marked) - 2)
    end = min(len(session_rows), max(marked) + 3)
    return list(range(start, end))


def build_longmemeval_context(record: dict[str, Any]) -> tuple[str, str, list[str]]:
    session_id, session_date, session_rows = answer_session(record)
    indices = context_window(session_rows)
    messages = [
        f"[{session_id}] {session_rows[idx]['role']}: {session_rows[idx]['content']}"
        for idx in indices
    ]
    return session_id, session_date, messages


def build_longmemeval_item(record: dict[str, Any], index: int) -> dict[str, Any]:
    session_id, session_date, context_messages = build_longmemeval_context(record)
    raw_facts = [
        core.fact("benchmark_answer", str(record["answer"])),
        core.fact("question_type", record["question_type"]),
        core.fact("answer_session_id", session_id),
    ]
    for idx, message in enumerate(context_messages, start=1):
        raw_facts.append(core.fact(f"context_{idx}", message))

    return {
        "id": f"longmemeval_bench_{index + 1:02d}",
        "family": "benign",
        "subject": f"LongMemEval user {record['question_id']}",
        "query_text": record["question"],
        "query_field": "benchmark_answer",
        "gold_answer": str(record["answer"]),
        "criticality": "medium",
        "context_messages": context_messages,
        "raw_facts": raw_facts,
        "benign_simplifications": core.simplify_answer(str(record["answer"])),
        "utility_slice_type": "longmemeval_single_session_direct_qa",
        "source_provenance": {
            "benchmark_family": "LongMemEval",
            "source_file": LONGMEMEVAL_SOURCE,
            "question_id": record["question_id"],
            "question_type": record["question_type"],
            "question_date": record["question_date"],
            "answer_session_ids": record["answer_session_ids"],
            "answer_session_date": session_date,
        },
        "selection_notes": [
            "Official LongMemEval short-answer single-session user question with exactly one answer-bearing session id.",
            "The answer is stated explicitly inside the retained answer session window, so this slice broadens benign benchmark coverage without adding heavy temporal or multi-session reasoning load.",
        ],
    }


def build_longmemeval_manifest(base_dir: Path) -> dict[str, Any]:
    records = load_longmemeval_records(base_dir)
    items = [
        build_longmemeval_item(find_longmemeval_record(records, question_id), idx)
        for idx, question_id in enumerate(LONGMEMEVAL_SELECTIONS)
    ]
    return {
        "adapter_id": "longmemeval_benign_utility_slice",
        "version": "v1",
        "retrieval_date": str(date.today()),
        "selection_policy": {
            "target_size": len(LONGMEMEVAL_SELECTIONS),
            "source_type": "official_benign_qa_benchmark_record",
            "rule": "Choose official LongMemEval single-session-user questions with short explicit answers, exactly one answer-bearing session id, and a tight answer-session context window, so the broader benchmark section adds another benign utility benchmark without leaning on heavy temporal synthesis.",
        },
        "items": items,
    }


def build_review(halumem_holdout: dict[str, Any], longmemeval_manifest: dict[str, Any]) -> str:
    lines = [
        "# External Benchmark Slice Audit Round 34",
        "",
        "这一轮不是重做 core slices，而是给 benchmark-first surface 增加更宽的 reviewer-facing section：保持任务契约不变，但扩展到 disjoint HaluMem holdout 和一组更机械可判的 LongMemEval benign utility items。",
        "",
        "## HaluMem Holdout Slice",
        "",
        f"- adapter_id: `{halumem_holdout['adapter_id']}`",
        f"- item_count: `{len(halumem_holdout['items'])}`",
        "- audit rule: keep the same unsupported-target explicit-designation contract as the core HaluMem slice, but move to disjoint official personas with three clean full-name support clues.",
        "- target behavior: broader coverage of clue-adjacent false-present pressure without changing the abstain-correct semantics.",
        "",
    ]
    for item in halumem_holdout["items"]:
        lines.append(
            f"- `{item['id']}`: source_index `{item['source_provenance']['source_index']}`, subject `{item['subject']}`, support clues = `{', '.join(item['source_provenance']['support_relationships'])}`."
        )

    lines.extend(
        [
            "",
            "## LongMemEval Direct Benign Slice",
            "",
            f"- adapter_id: `{longmemeval_manifest['adapter_id']}`",
            f"- item_count: `{len(longmemeval_manifest['items'])}`",
            "- audit rule: only keep single-session user questions whose answer is explicitly stated inside one answer-bearing session window, with short concrete answers and no multi-session reasoning requirement.",
            "- target behavior: preserve answerability under compaction on a second benign benchmark family instead of overfitting the reviewer section to LoCoMo only.",
            "",
        ]
    )
    for item in longmemeval_manifest["items"]:
        provenance = item["source_provenance"]
        lines.append(
            f"- `{item['id']}`: `{provenance['question_id']}` `{item['query_text']}` => `{item['gold_answer']}`; answer session = `{provenance['answer_session_ids'][0]}`."
        )

    lines.extend(
        [
            "",
            "## Bottom Line",
            "",
            "- 扩展后的 reviewer section 现在不只是一条 HaluMem core slice 和一条 LoCoMo core slice。",
            "- HaluMem holdout 让 unsupported-target hallucination 压力更宽，LongMemEval direct slice 则让 benign utility benchmark 不再只靠 LoCoMo 单一家族。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    halumem_holdout = build_halumem_holdout_manifest(base_dir)
    longmemeval_manifest = build_longmemeval_manifest(base_dir)
    write_json(base_dir / HALUMEM_HOLDOUT_PATH, halumem_holdout)
    write_json(base_dir / LONGMEMEVAL_SLICE_PATH, longmemeval_manifest)
    (base_dir / REVIEW_PATH).write_text(build_review(halumem_holdout, longmemeval_manifest), encoding="utf-8")
    print(f"Wrote {base_dir / HALUMEM_HOLDOUT_PATH}")
    print(f"Wrote {base_dir / LONGMEMEVAL_SLICE_PATH}")
    print(f"Wrote {base_dir / REVIEW_PATH}")


if __name__ == "__main__":
    main()
