#!/usr/bin/env python3
"""Build a small diverse manual audit set for self-built RQ2."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_rq2_manual_annotation_zh as base

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = PROJECT_ROOT / "state"

OUTPUT_HTML = STATE_DIR / "rq2_manual_annotation_diverse_zh.html"
OUTPUT_CSV = STATE_DIR / "rq2_manual_annotation_diverse_zh.csv"
OUTPUT_JSON = STATE_DIR / "rq2_manual_annotation_diverse_zh.json"
TARGET_DIVERSE_ROWS = 36


def _norm(text: str) -> str:
    text = (text or "").strip().lower().replace("-", " ")
    return re.sub(r"\s+", " ", text)


def _representatives(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row["base_id"], row["query_mode"], row["auto_label"], _norm(row["answer"]))
        groups[key].append(row)

    reps: list[dict[str, str]] = []
    for key, members in groups.items():
        members = sorted(
            members,
            key=lambda row: (
                int(row["passes"]),
                int(row["seed"]),
                row["report_id"],
            ),
        )
        chosen = dict(members[0])
        chosen["duplicate_count"] = str(len(members))
        chosen["covered_conditions"] = ", ".join(
            f"seed={row['seed']}/N={row['passes']}" for row in members
        )
        chosen["_norm_answer"] = key[3]
        reps.append(chosen)
    return reps


def _rarity_reason(rep: dict[str, str], count: int, exact_match: bool) -> str:
    reasons: list[str] = []
    if count == 1:
        reasons.append("这是只出现过一次的罕见答案形态")
    elif count == 2:
        reasons.append("这是只出现过两次的少见答案形态")
    if not exact_match:
        reasons.append("它不是最标准的答案写法，能帮助检查终点判定是否会被措辞变化带偏")
    if rep["auto_label"] == "FALSE_BELIEF":
        reasons.append("它代表模型明确站到了错误传言一边")
    else:
        reasons.append("它代表模型在容易混淆的条件下仍然站在正确答案一边")
    return "；".join(reasons)


def build_diverse_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    reps = _representatives(rows)
    key_counts = Counter((rep["base_id"], rep["query_mode"], rep["auto_label"], rep["_norm_answer"]) for rep in reps)
    rep_counts = Counter(rep["_norm_answer"] for rep in reps)

    by_base: dict[str, list[dict[str, str]]] = defaultdict(list)
    for rep in reps:
        by_base[rep["base_id"]].append(rep)

    selected: list[dict[str, str]] = []

    def rank(rep: dict[str, str]) -> tuple[int, int, int, int, int, str]:
        norm_answer = rep["_norm_answer"]
        exact_match = norm_answer in {_norm(rep["true_v_zh"]), _norm(rep["false_v_zh"]), _norm(rep["true_v"]), _norm(rep["false_v"])}
        rarity = rep_counts[norm_answer]
        return (
            0 if rep["auto_label"] == "FALSE_BELIEF" else 1,
            0 if not exact_match else 1,
            rarity,
            int(rep["duplicate_count"]),
            int(rep["passes"]),
            rep["query_mode"],
        )

    # Base coverage: one strongest representative per base fact.
    for base_id, group in sorted(by_base.items()):
        best = sorted(group, key=rank)[0]
        selected.append(best)

    chosen_ids = {row["uid"] for row in selected}

    # Add a second representative for bases that have both correct and false-belief outcomes.
    for base_id, group in sorted(by_base.items()):
        labels = {row["auto_label"] for row in group}
        if labels != {"TRUE", "FALSE_BELIEF"}:
            continue
        current = next(row for row in selected if row["base_id"] == base_id)
        target = "TRUE" if current["auto_label"] == "FALSE_BELIEF" else "FALSE_BELIEF"
        candidates = [row for row in group if row["auto_label"] == target and row["uid"] not in chosen_ids]
        if not candidates:
            continue
        best = sorted(candidates, key=rank)[0]
        selected.append(best)
        chosen_ids.add(best["uid"])

    # Keep the set readable, but no longer squeeze it down to the old 18-row cap.
    if len(selected) > TARGET_DIVERSE_ROWS:
        selected = sorted(selected, key=lambda rep: (rank(rep), rep["family"], rep["base_id"]))[:TARGET_DIVERSE_ROWS]

    # Sort for a readable audit flow.
    selected = sorted(
        selected,
        key=lambda row: (
            row["family"],
            row["base_id"],
            row["query_mode"],
            row["auto_label"],
            int(row["passes"]),
            int(row["seed"]),
        ),
    )

    for idx, row in enumerate(selected, start=1):
        norm_answer = row["_norm_answer"]
        exact_match = norm_answer in {
            _norm(row["true_v_zh"]),
            _norm(row["false_v_zh"]),
            _norm(row["true_v"]),
            _norm(row["false_v"]),
        }
        row["index"] = str(idx)
        row["selection_reason_zh"] = _rarity_reason(row, rep_counts[norm_answer], exact_match)
        row.pop("_norm_answer", None)
    return selected


def write_csv(rows: list[dict[str, str]], output_csv: Path | None = None) -> None:
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
        "selection_reason_zh",
        "human_label",
        "notes",
        "report_id",
    ]
    target = output_csv or OUTPUT_CSV
    with target.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-annotation", default=str(base.INPUT_ANNOTATION))
    ap.add_argument("--output-html", default=str(OUTPUT_HTML))
    ap.add_argument("--output-csv", default=str(OUTPUT_CSV))
    ap.add_argument("--output-json", default=str(OUTPUT_JSON))
    return ap


def main() -> None:
    args = _parser().parse_args()
    input_annotation = Path(args.input_annotation).expanduser().resolve()
    output_html = Path(args.output_html).expanduser().resolve()
    output_csv = Path(args.output_csv).expanduser().resolve()
    output_json = Path(args.output_json).expanduser().resolve()

    full_rows = base.build_rows(input_annotation)
    diverse_rows = build_diverse_rows(full_rows)
    output_json.write_text(json.dumps(diverse_rows, ensure_ascii=False, indent=2))
    write_csv(diverse_rows, output_csv)
    html = base.build_html(
        diverse_rows,
        page_title="RQ2 中文多样性审稿台",
        page_subtitle=(
            "这里不是全量样本，也不是普通去重版，而是保留更多不同翻车类型、不同答案形态、"
            "不同结果方向的多样性样本。它比旧版 18 条更大，目标是让你能看见更多变化，同时又不至于被重复题淹没。"
        ),
    )
    output_html.write_text(html)
    print(f"full_rows={len(full_rows)}")
    print(f"diverse_rows={len(diverse_rows)}")
    print(f"Wrote {output_html}")
    print(f"Wrote {output_csv}")
    print(f"Wrote {output_json}")


if __name__ == "__main__":
    main()
