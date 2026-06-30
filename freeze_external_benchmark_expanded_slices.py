from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

import freeze_external_benchmark_reviewer_slices as reviewer
import freeze_external_benchmark_slices as core


HALUMEM_EXPANDED_PATH = "benchmarks/halumem/frozen_slices/halumem_hallucination_expanded_v1.json"
LOCOMO_EXPANDED_PATH = "benchmarks/locomo/frozen_slices/locomo_benign_utility_expanded_v1.json"
LONGMEMEVAL_EXPANDED_PATH = "benchmarks/locomo/frozen_slices/longmemeval_benign_utility_expanded_v2.json"
REVIEW_PATH = "reviews/external_benchmark_expanded_dataset_audit_round35.md"

LOCOMO_PER_SAMPLE_CATEGORY_QUOTA = 4
LONGMEMEVAL_USER_TARGET = 48
LONGMEMEVAL_ASSISTANT_TARGET = 12

MONTH_WORDS = {
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
}
RELATIVE_TIME_WORDS = {
    "ago",
    "before",
    "after",
    "next",
    "last",
    "weekend",
    "yesterday",
    "today",
    "tomorrow",
}
QUESTION_PREFIX_SCORES = [
    ("what ", 3),
    ("where ", 3),
    ("who ", 3),
    ("when ", 3),
    ("which ", 2),
    ("how many ", 3),
    ("how much ", 3),
    ("how long ", 2),
    ("is ", 1),
    ("does ", 1),
    ("do ", 1),
]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_locomo_records(base_dir: Path) -> list[dict[str, Any]]:
    return core.load_locomo_records(base_dir)


def answer_text(value: Any) -> str:
    return str(value).strip()


def short_answer(answer: str, *, max_tokens: int, max_chars: int) -> bool:
    return 1 <= len(answer.split()) <= max_tokens and len(answer) <= max_chars


def prefix_score(question: str) -> int:
    lowered = question.lower().strip()
    for prefix, score in QUESTION_PREFIX_SCORES:
        if lowered.startswith(prefix):
            return score
    return 0


def is_absolute_temporal_answer(answer: str) -> bool:
    lowered = answer.lower().strip()
    if any(month in lowered for month in MONTH_WORDS):
        return True
    if re.fullmatch(r"\d{4}", lowered):
        return True
    if re.fullmatch(r"\d{1,2} [a-z]+ \d{4}", lowered):
        return True
    if re.fullmatch(r"[a-z]+,? \d{4}", lowered):
        return True
    if re.fullmatch(r"[a-z]+ \d{1,2}(st|nd|rd|th)?", lowered):
        return True
    return False


def evidence_complexity_band(evidence_ids: list[str]) -> str:
    if len(evidence_ids) <= 1:
        return "single_anchor"
    if len(evidence_ids) == 2:
        return "paired_anchor"
    return "multi_anchor"


def locomo_evaluation_stratum(question: str, answer: str) -> str:
    lowered = question.lower().strip()
    if is_absolute_temporal_answer(answer):
        return "locomo_absolute_temporal"
    if lowered.startswith("how many ") or lowered.startswith("how much ") or lowered.startswith("how long "):
        return "locomo_quantity_or_duration"
    return "locomo_entity_or_attribute"


def longmemeval_evaluation_stratum(question_type: str) -> str:
    if question_type == "single-session-user":
        return "longmemeval_single_session_user"
    return "longmemeval_single_session_assistant"


def longmemeval_complexity_band(question_type: str, context_messages: list[str], answer: str) -> str:
    if question_type == "single-session-assistant":
        return "assistant_trace_recall"
    if len(context_messages) <= 3 and len(answer.split()) <= 2:
        return "tight_literal_recall"
    return "session_window_recall"


def build_halumem_expanded_manifest(base_dir: Path) -> dict[str, Any]:
    records = core.load_halumem_records(base_dir)
    selected = [
        (source_index, record)
        for source_index, record in enumerate(records)
        if core.is_high_quality_halumem_record(record)
    ]
    items = []
    for index, (source_index, record) in enumerate(selected):
        item = core.build_halumem_item(record, source_index, index)
        item["id"] = f"halumem_expanded_{index + 1:02d}"
        item["evaluation_stratum"] = "halumem_unsupported_designation_abstain"
        item["complexity_band"] = "clean_three_clue_abstain"
        item["source_provenance"]["benchmark_slice_role"] = "expanded_quality_pool"
        item["selection_notes"] = [
            "Official HaluMem persona kept in the expanded pool because the support-clue surface is clean enough to support the same unsupported-target explicit-designation contract used by the smaller benchmark slices.",
            "This panel is meant to maximize official-source coverage without relaxing the abstain-correct semantics.",
        ]
        items.append(item)

    return {
        "adapter_id": "halumem_hallucination_expanded_slice",
        "version": "v1",
        "retrieval_date": str(date.today()),
        "selection_policy": {
            "target_size": len(items),
            "source_type": "official_hallucination_benchmark_record",
            "rule": "Keep every official HaluMem persona whose top support clues contain three clean full-name relationship anchors, then preserve the same unsupported explicit-designation query used by the benchmark-core slice.",
        },
        "items": items,
    }


def normalize_locomo_evidence_ids(evidence: list[Any]) -> list[str]:
    normalized: list[str] = []
    for raw in evidence:
        for part in str(raw).split(";"):
            value = part.strip()
            if value:
                normalized.append(value)
    return normalized


def locomo_answer_is_clean(answer: str) -> bool:
    lowered = answer.lower()
    if any(token in lowered for token in [" because ", " they ", " he ", " she ", " their "]):
        return False
    return True


def locomo_category_one_ok(question: str, answer: str) -> bool:
    lowered = question.lower()
    if any(
        token in lowered
        for token in ["why ", "how do", "how did", "likely", "both", "in common", "ideal", "should", "would"]
    ):
        return False
    return locomo_answer_is_clean(answer)


def locomo_category_two_ok(answer: str) -> bool:
    lowered = answer.lower()
    if any(token in lowered for token in RELATIVE_TIME_WORDS):
        return False
    if len(lowered.split()) > 5:
        return False
    if any(month in lowered for month in MONTH_WORDS):
        return True
    if re.fullmatch(r"\d{4}", lowered):
        return True
    if re.fullmatch(r"\d+ (day|days|month|months|year|years)", lowered):
        return True
    return False


def locomo_quality_score(question: str, answer: str, category: int) -> int:
    score = prefix_score(question)
    score += 1 if category == 1 else 2
    score -= max(0, len(answer.split()) - 3)
    if "," in answer:
        score -= 1
    if '"' in answer:
        score -= 1
    if " and " in answer.lower():
        score -= 1
    if re.search(r"\d", answer):
        score += 1
    return score


def locomo_candidate_rows(sample: dict[str, Any]) -> dict[int, list[dict[str, Any]]]:
    candidates: dict[int, list[dict[str, Any]]] = defaultdict(list)
    turn_map, _ = core.locomo_turn_index(sample)
    for qa_index, qa in enumerate(sample["qa"]):
        category = qa.get("category")
        if category not in {1, 2}:
            continue
        evidence_ids = normalize_locomo_evidence_ids(qa.get("evidence") or [])
        if not evidence_ids or not all(evidence_id in turn_map for evidence_id in evidence_ids):
            continue
        answer = answer_text(qa.get("answer"))
        if not short_answer(answer, max_tokens=8, max_chars=70):
            continue
        if category == 1 and not locomo_category_one_ok(qa["question"], answer):
            continue
        if category == 2 and not locomo_category_two_ok(answer):
            continue
        candidates[category].append(
            {
                "qa_index": qa_index,
                "question": qa["question"],
                "answer": answer,
                "category": category,
                "evidence_ids": evidence_ids,
                "score": locomo_quality_score(qa["question"], answer, category),
                "qa": qa,
            }
        )
    return candidates


def select_locomo_rows(samples: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for sample in sorted(samples, key=lambda row: row["sample_id"]):
        candidates = locomo_candidate_rows(sample)
        for category in (1, 2):
            rows = sorted(
                candidates[category],
                key=lambda row: (-row["score"], len(row["answer"].split()), row["question"], row["qa_index"]),
            )
            if len(rows) < LOCOMO_PER_SAMPLE_CATEGORY_QUOTA:
                raise RuntimeError(
                    f"LoCoMo sample {sample['sample_id']} category {category} only has {len(rows)} clean candidates."
                )
            selected.extend((sample, row) for row in rows[:LOCOMO_PER_SAMPLE_CATEGORY_QUOTA])
    return selected


def build_locomo_expanded_manifest(base_dir: Path) -> dict[str, Any]:
    samples = load_locomo_records(base_dir)
    selected = select_locomo_rows(samples)
    items = []
    for index, (sample, row) in enumerate(selected):
        qa = dict(row["qa"])
        qa["evidence"] = list(row["evidence_ids"])
        item = core.build_locomo_item(sample, qa, index)
        item["id"] = f"locomo_expanded_{index + 1:03d}"
        item["evaluation_stratum"] = locomo_evaluation_stratum(item["query_text"], item["gold_answer"])
        item["complexity_band"] = evidence_complexity_band(row["evidence_ids"])
        item["utility_slice_type"] = "locomo_balanced_direct_benchmark_qa"
        item["source_provenance"]["benchmark_slice_role"] = "expanded_quality_pool"
        item["source_provenance"]["question_index"] = row["qa_index"]
        item["source_provenance"]["selection_bucket"] = f"category_{row['category']}_balanced_topk"
        item["selection_notes"] = [
            "Official LoCoMo QA selected under a balanced per-conversation rule: keep the top clean category-1 direct factual items and top clean category-2 date/time items for each conversation.",
            "This expanded panel favors short explicit answers and valid evidence windows so the benchmark stays aligned with benign answer-retention rather than drifting into heavy inference or answer-normalization work.",
        ]
        items.append(item)

    return {
        "adapter_id": "locomo_benign_utility_expanded_slice",
        "version": "v1",
        "retrieval_date": str(date.today()),
        "selection_policy": {
            "target_size": len(items),
            "source_type": "official_benign_qa_benchmark_record",
            "rule": "For each LoCoMo conversation, keep four clean category-1 direct factual QA items and four clean category-2 explicit date/time QA items with valid evidence ids, short answers, and low normalization burden.",
            "per_sample_category_quota": LOCOMO_PER_SAMPLE_CATEGORY_QUOTA,
        },
        "items": items,
    }


def longmemeval_candidate_ok(record: dict[str, Any]) -> bool:
    if record.get("question_type") not in {"single-session-user", "single-session-assistant"}:
        return False
    if len(record.get("answer_session_ids", [])) != 1:
        return False
    answer = answer_text(record.get("answer"))
    if not short_answer(answer, max_tokens=8, max_chars=80):
        return False
    lowered = record.get("question", "").lower()
    if any(
        token in lowered
        for token in ["recommend", "resources", "summarize", "preference", "best way", "explain why", "opinion"]
    ):
        return False
    try:
        _, _, context_messages = reviewer.build_longmemeval_context(record)
    except RuntimeError:
        return False
    return 2 <= len(context_messages) <= 6


def longmemeval_quality_score(record: dict[str, Any]) -> int:
    score = prefix_score(record["question"])
    if record["question_type"] == "single-session-user":
        score += 2
    answer = answer_text(record["answer"])
    score -= max(0, len(answer.split()) - 3)
    if re.search(r"\d", answer):
        score += 1
    if len(answer.split()) <= 2:
        score += 1
    return score


def select_longmemeval_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if not longmemeval_candidate_ok(record):
            continue
        by_type[record["question_type"]].append(record)

    selected: list[dict[str, Any]] = []
    quotas = {
        "single-session-user": LONGMEMEVAL_USER_TARGET,
        "single-session-assistant": LONGMEMEVAL_ASSISTANT_TARGET,
    }
    for question_type, quota in quotas.items():
        rows = sorted(
            by_type[question_type],
            key=lambda row: (-longmemeval_quality_score(row), len(answer_text(row["answer"]).split()), row["question_id"]),
        )
        if len(rows) < quota:
            raise RuntimeError(
                f"LongMemEval question_type {question_type} only has {len(rows)} clean candidates for quota {quota}."
            )
        selected.extend(rows[:quota])
    return sorted(selected, key=lambda row: (row["question_type"], row["question_id"]))


def build_longmemeval_expanded_manifest(base_dir: Path) -> dict[str, Any]:
    records = reviewer.load_longmemeval_records(base_dir)
    selected = select_longmemeval_rows(records)
    items = []
    for index, record in enumerate(selected):
        item = reviewer.build_longmemeval_item(record, index)
        item["id"] = f"longmemeval_expanded_{index + 1:03d}"
        item["evaluation_stratum"] = longmemeval_evaluation_stratum(record["question_type"])
        item["complexity_band"] = longmemeval_complexity_band(
            record["question_type"],
            item["context_messages"],
            item["gold_answer"],
        )
        item["utility_slice_type"] = "longmemeval_balanced_single_session_direct_qa"
        item["source_provenance"]["benchmark_slice_role"] = "expanded_quality_pool"
        item["selection_notes"] = [
            "Official LongMemEval item with exactly one answer-bearing session id and a short direct answer that is explicitly supported inside a tight session window.",
            "The expanded panel keeps a mostly user-facing single-session contract, with a small assistant-facing tranche for coverage diversity, while avoiding recommendation or preference-heavy questions.",
        ]
        items.append(item)

    return {
        "adapter_id": "longmemeval_benign_utility_expanded_slice",
        "version": "v2",
        "retrieval_date": str(date.today()),
        "selection_policy": {
            "target_size": len(items),
            "source_type": "official_benign_qa_benchmark_record",
            "rule": "Keep clean LongMemEval single-session rows with exactly one answer-bearing session id, short direct answers, and a tight answer-session context window; allocate 48 user-facing items plus 12 assistant-facing items for coverage diversity without shifting to multi-session reasoning.",
            "single_session_user_target": LONGMEMEVAL_USER_TARGET,
            "single_session_assistant_target": LONGMEMEVAL_ASSISTANT_TARGET,
        },
        "items": items,
    }


def build_review(
    halumem_manifest: dict[str, Any],
    locomo_manifest: dict[str, Any],
    longmemeval_manifest: dict[str, Any],
) -> str:
    locomo_sample_counts: dict[str, int] = defaultdict(int)
    locomo_category_counts: dict[int, int] = defaultdict(int)
    for item in locomo_manifest["items"]:
        provenance = item["source_provenance"]
        locomo_sample_counts[provenance["sample_id"]] += 1
        locomo_category_counts[int(provenance["category"])] += 1

    longmemeval_type_counts: dict[str, int] = defaultdict(int)
    for item in longmemeval_manifest["items"]:
        longmemeval_type_counts[item["source_provenance"]["question_type"]] += 1

    total_items = (
        len(halumem_manifest["items"])
        + len(locomo_manifest["items"])
        + len(longmemeval_manifest["items"])
    )

    lines = [
        "# External Benchmark Expanded Dataset Audit Round 35",
        "",
        "这一轮不是继续停留在 32 条 reviewer section，而是正式构造下一阶段的大规模 official benchmark pool：保留现有任务契约，但把可追溯、可复现、可直接接入现有 compaction stack 的 benchmark items 扩到更大规模。",
        "",
        f"- total_official_items: `{total_items}`",
        f"- halumem_expanded: `{len(halumem_manifest['items'])}`",
        f"- locomo_expanded: `{len(locomo_manifest['items'])}`",
        f"- longmemeval_expanded: `{len(longmemeval_manifest['items'])}`",
        "",
        "## HaluMem Expanded",
        "",
        f"- adapter_id: `{halumem_manifest['adapter_id']}`",
        f"- item_count: `{len(halumem_manifest['items'])}`",
        "- rule: keep every official persona whose support-clue surface is clean enough for the same unsupported explicit-designation query used by the smaller HaluMem slices.",
        "- payoff: we move from a thin 8+8 hallucination reviewer section to almost the full verified local HaluMem pool without changing the abstain-correct task semantics.",
        "",
        "## LoCoMo Expanded",
        "",
        f"- adapter_id: `{locomo_manifest['adapter_id']}`",
        f"- item_count: `{len(locomo_manifest['items'])}`",
        f"- per_sample_counts: `{dict(sorted(locomo_sample_counts.items()))}`",
        f"- category_counts: `{dict(sorted(locomo_category_counts.items()))}`",
        "- rule: for each conversation, keep the top four clean category-1 direct factual QA items and top four clean category-2 explicit date/time QA items after evidence normalization and answer-form filtering.",
        "- payoff: the larger benign pool is now balanced across all 10 LoCoMo conversations instead of depending on a single tiny handpicked slice.",
        "",
        "## LongMemEval Expanded",
        "",
        f"- adapter_id: `{longmemeval_manifest['adapter_id']}`",
        f"- item_count: `{len(longmemeval_manifest['items'])}`",
        f"- question_type_counts: `{dict(sorted(longmemeval_type_counts.items()))}`",
        "- rule: keep only single-session rows with exactly one answer-bearing session id, short direct answers, and a tight answer-session context window; allocate most slots to user-facing recall questions and a smaller tranche to assistant-facing reminders.",
        "- payoff: we turn the previous 8-item LongMemEval add-on into a real second benign benchmark family with materially wider coverage.",
        "",
        "## Why Not Use Every Candidate",
        "",
        "- LoCoMo has many more raw QA rows, but a noticeable fraction are inference-heavy, relative-time-heavy, or use awkward evidence encodings; the expanded pool keeps only the subset that still matches our benign answer-retention contract.",
        "- LongMemEval also contains multi-session and temporal-reasoning items; those are valuable later, but they would currently blur the question of whether compaction alone preserves directly answerable local evidence.",
        "- The point of this pool is not maximum raw count at any cost; it is a larger, cleaner, benchmark-native dataset that can support the next baseline stage without collapsing into label-noise and answer-normalization noise.",
        "",
    ]

    halu_preview = halumem_manifest["items"][:3]
    locomo_preview = locomo_manifest["items"][:3]
    long_preview = longmemeval_manifest["items"][:3]

    lines.append("## Preview")
    lines.append("")
    lines.append("### HaluMem")
    lines.append("")
    for item in halu_preview:
        provenance = item["source_provenance"]
        lines.append(
            f"- `{item['id']}`: source_index `{provenance['source_index']}`, subject `{item['subject']}`, support clues = `{', '.join(provenance['support_relationships'])}`."
        )
    lines.append("")
    lines.append("### LoCoMo")
    lines.append("")
    for item in locomo_preview:
        provenance = item["source_provenance"]
        lines.append(
            f"- `{item['id']}`: `{provenance['sample_id']}` category `{provenance['category']}` => `{item['query_text']}` / `{item['gold_answer']}`."
        )
    lines.append("")
    lines.append("### LongMemEval")
    lines.append("")
    for item in long_preview:
        provenance = item["source_provenance"]
        lines.append(
            f"- `{item['id']}`: `{provenance['question_id']}` `{provenance['question_type']}` => `{item['query_text']}` / `{item['gold_answer']}`."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    halumem_manifest = build_halumem_expanded_manifest(base_dir)
    locomo_manifest = build_locomo_expanded_manifest(base_dir)
    longmemeval_manifest = build_longmemeval_expanded_manifest(base_dir)

    write_json(base_dir / HALUMEM_EXPANDED_PATH, halumem_manifest)
    write_json(base_dir / LOCOMO_EXPANDED_PATH, locomo_manifest)
    write_json(base_dir / LONGMEMEVAL_EXPANDED_PATH, longmemeval_manifest)
    (base_dir / REVIEW_PATH).write_text(
        build_review(halumem_manifest, locomo_manifest, longmemeval_manifest),
        encoding="utf-8",
    )

    print(f"Wrote {base_dir / HALUMEM_EXPANDED_PATH}")
    print(f"Wrote {base_dir / LOCOMO_EXPANDED_PATH}")
    print(f"Wrote {base_dir / LONGMEMEVAL_EXPANDED_PATH}")
    print(f"Wrote {base_dir / REVIEW_PATH}")


if __name__ == "__main__":
    main()
