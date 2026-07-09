#!/usr/bin/env python3
"""Build a deduplicated Chinese audit set for self-built RQ2 manual review."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

import build_rq2_manual_annotation_zh as base

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = PROJECT_ROOT / "state"

OUTPUT_HTML = STATE_DIR / "rq2_manual_annotation_core_zh.html"
OUTPUT_CSV = STATE_DIR / "rq2_manual_annotation_core_zh.csv"
OUTPUT_JSON = STATE_DIR / "rq2_manual_annotation_core_zh.json"


def _norm_answer(text: str) -> str:
    text = (text or "").strip().lower().replace("-", " ")
    return re.sub(r"\s+", " ", text)


def dedup_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    buckets: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row["base_id"], row["query_mode"], row["auto_label"], _norm_answer(row["answer"]))
        buckets[key].append(row)

    reduced: list[dict[str, str]] = []
    for _, members in sorted(buckets.items()):
        members = sorted(
            members,
            key=lambda row: (
                row["family"],
                row["base_id"],
                row["query_mode"],
                int(row["passes"]),
                int(row["seed"]),
            ),
        )
        chosen = dict(members[0])
        chosen["duplicate_count"] = str(len(members))
        chosen["covered_conditions"] = ", ".join(
            f"seed={row['seed']}/N={row['passes']}" for row in members
        )
        reduced.append(chosen)

    for idx, row in enumerate(reduced, start=1):
        row["index"] = str(idx)
    return reduced


def write_csv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "index",
        "uid",
        "family_zh",
        "seed",
        "passes",
        "base_id",
        "title_zh",
        "query_mode_zh",
        "question_zh",
        "true_v_zh",
        "false_v_zh",
        "answer",
        "auto_label_zh",
        "duplicate_count",
        "covered_conditions",
        "human_label",
        "notes",
        "report_id",
    ]
    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def main() -> None:
    full_rows = base.build_rows()
    core_rows = dedup_rows(full_rows)
    OUTPUT_JSON.write_text(base.json.dumps(core_rows, ensure_ascii=False, indent=2))
    write_csv(core_rows)
    html = base.build_html(
        core_rows,
        page_title="RQ2 中文去重审稿台",
        page_subtitle=(
            "这里不是全量 144 条，而是去重后的人工审稿集。"
            "重复答案只保留一个代表样本，避免你越标越像在刷同一题。"
            "只有想跳题时，才展开下面的题目列表。"
        ),
    )
    OUTPUT_HTML.write_text(html)
    print(f"full_rows={len(full_rows)}")
    print(f"core_rows={len(core_rows)}")
    print(f"Wrote {OUTPUT_HTML}")
    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
