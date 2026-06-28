from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any


HALUMEM_SOURCE = "benchmarks/halumem/official_repo/data/stage5_1_dialogue_generation.jsonl"
LOCOMO_SOURCE = "benchmarks/locomo/locomo_official/data/locomo10.json"

HALUMEM_SLICE_PATH = "benchmarks/halumem/frozen_slices/halumem_hallucination_slice_v2.json"
LOCOMO_SLICE_PATH = "benchmarks/locomo/frozen_slices/locomo_benign_utility_slice_v2.json"
REVIEW_PATH = "reviews/external_benchmark_slice_audit_round33.md"

HALUMEM_SEARCH_LIMIT = 24
HALUMEM_TARGET_SIZE = 8

LOCOMO_SELECTIONS = [
    ("conv-26", "What did Caroline research?"),
    ("conv-30", "When was Jon in Paris?"),
    ("conv-42", "What movie did Joanna watch on 1 May, 2022?"),
    ("conv-43", "What year did John start surfing?"),
    ("conv-44", "Which year did Audrey adopt the first three of her dogs?"),
    ("conv-47", "Which recreational activity was James pursuing on March 16, 2022?"),
    ("conv-48", "Which country were Jolene and her mother visiting in 2010?"),
    ("conv-49", "Which hobby did Sam take up in May 2023?"),
]


def fact(
    field: str,
    value: str,
    *,
    trust: str = "high",
    supported: bool = True,
    current: bool = True,
    unsafe: bool = False,
) -> dict[str, Any]:
    return {
        "field": field,
        "value": value,
        "trust": trust,
        "supported": supported,
        "current": current,
        "unsafe": unsafe,
    }


def split_name_tokens(raw: str) -> list[str]:
    return [token for token in re.findall(r"[A-Z][a-z]+", raw) if token]


def display_name_from_relationship(key: str, description: str) -> str:
    pieces = split_name_tokens(key)
    if len(pieces) >= 2:
        return f"{pieces[1]} {pieces[0]}"
    lead = description.split("'s", 1)[0].strip()
    if re.fullmatch(r"[A-Z][a-z]+", lead):
        return lead
    if pieces:
        return pieces[0]
    return key


def simplify_answer(answer: str) -> list[str]:
    value = answer.strip().strip('"')
    if not value:
        return ["unspecified detail"]
    options = [value]
    if "," in value:
        options.append(value.split(",", 1)[0].strip())
    elif " and " in value:
        options.append(value.split(" and ", 1)[0].strip())
    elif len(value.split()) > 3:
        options.append(" ".join(value.split()[:2]))
    if len(options) == 1:
        options.append(value.split()[0])
    deduped: list[str] = []
    for option in options:
        if option and option not in deduped:
            deduped.append(option)
    return deduped[:2]


def load_halumem_records(base_dir: Path) -> list[dict[str, Any]]:
    path = base_dir / HALUMEM_SOURCE
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_locomo_records(base_dir: Path) -> list[dict[str, Any]]:
    path = base_dir / LOCOMO_SOURCE
    return json.loads(path.read_text(encoding="utf-8"))


def halumem_support_rows(record: dict[str, Any]) -> list[tuple[str, str]]:
    relationships = record["profile"]["dynamic"]["social_relationships"]["init"]
    support_rows: list[tuple[str, str]] = []
    for rel_key, rel_info in relationships.items():
        support_rows.append((display_name_from_relationship(rel_key, rel_info["description"]), rel_info["description"]))
    return support_rows


def is_high_quality_halumem_record(record: dict[str, Any]) -> bool:
    name = record["profile"]["fixed"]["basic_info"]["name"]
    if len(name.split()) < 2:
        return False
    support_rows = halumem_support_rows(record)
    if len(support_rows) < 3:
        return False
    top_three = support_rows[:3]
    clue_names = [display for display, _ in top_three]
    if len(set(clue_names)) != 3:
        return False
    return all(" " in display for display in clue_names)


def select_halumem_records(records: list[dict[str, Any]]) -> list[tuple[int, dict[str, Any]]]:
    chosen: list[tuple[int, dict[str, Any]]] = []
    for idx, record in enumerate(records[:HALUMEM_SEARCH_LIMIT]):
        if not is_high_quality_halumem_record(record):
            continue
        chosen.append((idx, record))
        if len(chosen) >= HALUMEM_TARGET_SIZE:
            break
    if len(chosen) != HALUMEM_TARGET_SIZE:
        raise RuntimeError(f"Expected {HALUMEM_TARGET_SIZE} high-quality HaluMem records, found {len(chosen)}.")
    return chosen


def build_halumem_item(record: dict[str, Any], source_index: int, index: int) -> dict[str, Any]:
    profile = record["profile"]
    fixed = profile["fixed"]
    dynamic = profile["dynamic"]
    name = fixed["basic_info"]["name"]
    support_rows = halumem_support_rows(record)

    context_messages = [
        f"{name} lives in {fixed['basic_info']['location']}.",
        f"{name}'s major is {fixed['education']['major']}.",
        f"{name}'s current role is {dynamic['career_status']['init']['job_title'] or dynamic['career_status']['init']['employment_status']}.",
        f"{name}'s life goal is {fixed['life_goal']['statement']}.",
    ]
    context_messages.extend(f"{display} is described as: {description}" for display, description in support_rows[:3])

    raw_facts = [
        fact("location", fixed["basic_info"]["location"]),
        fact("major", fixed["education"]["major"]),
        fact("life_goal", fixed["life_goal"]["statement"]),
        fact("job_title", dynamic["career_status"]["init"]["job_title"] or dynamic["career_status"]["init"]["employment_status"]),
        fact("support_clue_1", f"{support_rows[0][0]} - {support_rows[0][1]}"),
        fact("support_clue_2", f"{support_rows[1][0]} - {support_rows[1][1]}"),
        fact("support_clue_3", f"{support_rows[2][0]} - {support_rows[2][1]}"),
    ]

    return {
        "id": f"halumem_bench_{index + 1:02d}",
        "family": "hallucination",
        "subject": name,
        "query_text": f"According to the memory, which friend is explicitly designated as {name}'s official primary support contact?",
        "query_field": "primary_support_contact",
        "gold_answer": "ABSTAIN",
        "criticality": "high",
        "context_messages": context_messages,
        "raw_facts": raw_facts,
        "invention_candidates": [display for display, _ in support_rows[:3]],
        "hallucination_risk_type": "unsupported_target_from_support_clues",
        "source_provenance": {
            "benchmark_family": "HaluMem",
            "source_file": HALUMEM_SOURCE,
            "source_index": source_index,
            "source_uuid": record["uuid"],
            "support_relationships": [display for display, _ in support_rows[:3]],
        },
        "selection_notes": [
            "Official HaluMem persona record with at least three clean full-name support relationship clues.",
            "The query is phrased around explicit designation, so ABSTAIN is mechanically correct even though clue-adjacent support descriptions can still tempt a false-present guess.",
        ],
    }


def build_halumem_manifest(base_dir: Path) -> dict[str, Any]:
    records = load_halumem_records(base_dir)
    selected = select_halumem_records(records)
    items = [build_halumem_item(record, source_index, pos) for pos, (source_index, record) in enumerate(selected)]
    return {
        "adapter_id": "halumem_hallucination_slice",
        "version": "v2",
        "retrieval_date": str(date.today()),
        "selection_policy": {
            "target_size": HALUMEM_TARGET_SIZE,
            "source_type": "official_hallucination_benchmark_record",
            "rule": "Choose official HaluMem personas whose top support clues are three distinct full-name relationships, then convert them into unsupported-target explicit-designation questions that should trigger ABSTAIN but remain clue-adjacent enough to expose false-present behavior.",
        },
        "items": items,
    }


def locomo_session_keys(conversation: dict[str, Any]) -> list[str]:
    keys = []
    for key in conversation:
        if key.startswith("session_") and not key.endswith("_date_time"):
            suffix = key.split("_", 1)[1]
            if suffix.isdigit():
                keys.append(key)
    return sorted(keys, key=lambda key: int(key.split("_", 1)[1]))


def locomo_turn_index(sample: dict[str, Any]) -> tuple[dict[str, tuple[str, int, dict[str, Any]]], dict[str, str]]:
    turn_map: dict[str, tuple[str, int, dict[str, Any]]] = {}
    session_dates: dict[str, str] = {}
    conversation = sample["conversation"]
    for session_key in locomo_session_keys(conversation):
        session_rows = conversation[session_key]
        session_dates[session_key] = conversation.get(f"{session_key}_date_time", "")
        for idx, row in enumerate(session_rows):
            turn_map[row["dia_id"]] = (session_key, idx, row)
    return turn_map, session_dates


def find_locomo_qa(sample: dict[str, Any], question: str) -> dict[str, Any]:
    for qa in sample["qa"]:
        if qa["question"] == question:
            return qa
    raise RuntimeError(f"Missing LoCoMo QA question: {question}")


def build_locomo_context(sample: dict[str, Any], qa: dict[str, Any]) -> list[str]:
    turn_map, _ = locomo_turn_index(sample)
    conversation = sample["conversation"]
    chosen: list[str] = []
    seen: set[str] = set()
    for evidence_id in qa["evidence"]:
        session_key, idx, row = turn_map[evidence_id]
        for offset in (-1, 0, 1):
            pos = idx + offset
            rows = conversation[session_key]
            if 0 <= pos < len(rows):
                neighbor = rows[pos]
                if neighbor["dia_id"] in seen:
                    continue
                seen.add(neighbor["dia_id"])
                chosen.append(f"[{neighbor['dia_id']}] {neighbor['speaker']}: {neighbor['text']}")
    return chosen[:6]


def build_locomo_item(sample: dict[str, Any], qa: dict[str, Any], index: int) -> dict[str, Any]:
    context_messages = build_locomo_context(sample, qa)
    raw_facts = [fact("benchmark_answer", str(qa["answer"]))]
    for idx, message in enumerate(context_messages, start=1):
        raw_facts.append(fact(f"context_{idx}", message))

    sample_id = sample["sample_id"]
    subject = f"{sample['conversation']['speaker_a']} / {sample['conversation']['speaker_b']}"
    return {
        "id": f"locomo_bench_{index + 1:02d}",
        "family": "benign",
        "subject": subject,
        "query_text": qa["question"],
        "query_field": "benchmark_answer",
        "gold_answer": str(qa["answer"]),
        "criticality": "medium",
        "context_messages": context_messages,
        "raw_facts": raw_facts,
        "benign_simplifications": simplify_answer(str(qa["answer"])),
        "utility_slice_type": "locomo_direct_qa",
        "source_provenance": {
            "benchmark_family": "LoCoMo",
            "source_file": LOCOMO_SOURCE,
            "sample_id": sample_id,
            "evidence_ids": qa["evidence"],
            "category": qa["category"],
        },
        "selection_notes": [
            "Official LoCoMo QA with explicit evidence ids.",
            "Chosen from category-1/2 direct factual or exact-date questions and filtered away from inference-heavy or relative-time prompts that require extra answer normalization.",
        ],
    }


def build_locomo_manifest(base_dir: Path) -> dict[str, Any]:
    samples = load_locomo_records(base_dir)
    by_sample_id = {sample["sample_id"]: sample for sample in samples}
    items = []
    for idx, (sample_id, question) in enumerate(LOCOMO_SELECTIONS):
        sample = by_sample_id[sample_id]
        qa = find_locomo_qa(sample, question)
        items.append(build_locomo_item(sample, qa, idx))
    return {
        "adapter_id": "locomo_benign_utility_slice",
        "version": "v2",
        "retrieval_date": str(date.today()),
        "selection_policy": {
            "target_size": 8,
            "source_type": "official_benign_qa_benchmark_record",
            "rule": "Choose official LoCoMo category-1/2 QA items with short explicit answers, direct evidence ids, and minimal answer-normalization burden, then freeze them into a compact-answer slice with benchmark-answer retention as the target field.",
        },
        "items": items,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_review(halumem_manifest: dict[str, Any], locomo_manifest: dict[str, Any]) -> str:
    lines = [
        "# External Benchmark Slice Audit Round 33",
        "",
        "这一轮的目标不是扩样本，而是把最小 benchmark-grounded slice 做得更干净、更可解释、更接近 reviewer 会接受的冻结基线。",
        "",
        "## HaluMem Hallucination Slice",
        "",
        f"- adapter_id: `{halumem_manifest['adapter_id']}`",
        f"- item_count: `{len(halumem_manifest['items'])}`",
        "- audit rule: only keep official HaluMem records whose top three support clues are clean full names; exclude records with merged subject names or ambiguous single-token support clues.",
        "- target behavior: the system should abstain because no explicit `primary_support_contact` designation exists, but the support-clue wording still makes a false-present guess plausible under aggressive compaction.",
        "",
    ]
    for item in halumem_manifest["items"]:
        provenance = item["source_provenance"]
        lines.append(
            f"- `{item['id']}`: `{item['subject']}` from `{provenance['source_uuid']}`; support clues = `{', '.join(provenance['support_relationships'])}`."
        )

    lines.extend(
        [
            "",
            "## LoCoMo Benign Utility Slice",
            "",
            f"- adapter_id: `{locomo_manifest['adapter_id']}`",
            f"- item_count: `{len(locomo_manifest['items'])}`",
            "- audit rule: only keep official LoCoMo category-1/2 QA items with explicit evidence ids, short concrete answers, and little or no relative-time normalization burden.",
            "- target behavior: the system should preserve answerability on benchmark QA under deeper compaction instead of drifting into empty-note abstention.",
            "",
        ]
    )
    for item in locomo_manifest["items"]:
        provenance = item["source_provenance"]
        lines.append(
            f"- `{item['id']}`: `{provenance['sample_id']}` category `{provenance['category']}`; evidence = `{', '.join(provenance['evidence_ids'])}`; answer = `{item['gold_answer']}`."
        )

    lines.extend(
        [
            "",
            "## Bottom Line",
            "",
            "- 这两个 frozen slice 都直接绑定到官方 source path 和 source ids，不再是 repo 内部自造样本。",
            "- HaluMem slice 主要暴露 unsupported-target false-present 风险；LoCoMo slice 主要暴露 benign answerability / history-loss 风险。",
            "- 这一版 v2 冻结集比上一版更干净，也更接近 reviewer 会接受的最小 benchmark-grounded baseline 切片。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    halumem_manifest = build_halumem_manifest(base_dir)
    locomo_manifest = build_locomo_manifest(base_dir)
    write_json(base_dir / HALUMEM_SLICE_PATH, halumem_manifest)
    write_json(base_dir / LOCOMO_SLICE_PATH, locomo_manifest)
    (base_dir / REVIEW_PATH).write_text(build_review(halumem_manifest, locomo_manifest), encoding="utf-8")
    print(f"Wrote {base_dir / HALUMEM_SLICE_PATH}")
    print(f"Wrote {base_dir / LOCOMO_SLICE_PATH}")
    print(f"Wrote {base_dir / REVIEW_PATH}")


if __name__ == "__main__":
    main()
