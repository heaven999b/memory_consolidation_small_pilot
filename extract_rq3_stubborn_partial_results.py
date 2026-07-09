#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import safety_honest_metrics as hm


def _base_id(item_id: str) -> str:
    if item_id.endswith("a") or item_id.endswith("b"):
        return item_id[:-1]
    return item_id


def _load_items(suite_path: Path, one_variant: bool) -> list[dict[str, Any]]:
    items = json.loads(suite_path.read_text(encoding="utf-8"))["items"]
    if not one_variant:
        return items
    seen: set[str] = set()
    kept: list[dict[str, Any]] = []
    for item in items:
        base = _base_id(item["id"])
        if base in seen:
            continue
        seen.add(base)
        kept.append(item)
    return kept


def _load_answer(qa_path: Path) -> dict[str, Any]:
    lines = [line for line in qa_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"empty qa file: {qa_path}")
    return json.loads(lines[0])


def _cell_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    unsafe = sum(1 for row in rows if row["unsafe_lexical"])
    return {
        "n_rows": total,
        "unsafe_k": unsafe,
        "unsafe_rate": (unsafe / total) if total else None,
    }


def _group_summary(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[str(row[key])].append(row)
    out = []
    for value, bucket in sorted(buckets.items()):
        total = len(bucket)
        unsafe = sum(1 for row in bucket if row["unsafe_lexical"])
        out.append({
            key: value,
            "n_rows": total,
            "unsafe_k": unsafe,
            "unsafe_rate": unsafe / total if total else None,
        })
    return out


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['report_id']}",
        "",
        f"- generated_at: `{report['generated_at']}`",
        f"- suite_path: `{report['suite_path']}`",
        f"- one_variant: `{report['one_variant']}`",
        f"- note: `{report['note']}`",
        "",
        "## Cell Summary",
        "",
        "| condition | N | unsafe | unsafe rate |",
        "| --- | ---: | ---: | ---: |",
    ]
    for cell in report["cell_summaries"]:
        rate = "n/a" if cell["unsafe_rate"] is None else f"{cell['unsafe_rate']:.3f}"
        lines.append(f"| {cell['condition_id']} / N={cell['passes']} | {cell['n_rows']} | {cell['unsafe_k']} | {rate} |")

    lines += [
        "",
        "## Query Family",
        "",
        "| condition | N | query family | unsafe | unsafe rate |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for group in report["query_family_summaries"]:
        rate = "n/a" if group["unsafe_rate"] is None else f"{group['unsafe_rate']:.3f}"
        lines.append(
            f"| {group['condition_id']} | {group['passes']} | {group['query_family']} | {group['unsafe_k']} | {rate} |"
        )

    lines += [
        "",
        "## Scenario",
        "",
        "| condition | N | scenario | unsafe | unsafe rate |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for group in report["scenario_summaries"]:
        rate = "n/a" if group["unsafe_rate"] is None else f"{group['unsafe_rate']:.3f}"
        lines.append(
            f"| {group['condition_id']} | {group['passes']} | {group['source_base_id']} | {group['unsafe_k']} | {rate} |"
        )

    lines += [
        "",
        "## Sample Unsafe Answers",
        "",
    ]
    for row in report["sample_unsafe_rows"]:
        lines += [
            f"### {row['condition_id']} / N={row['passes']} / {row['item_id']}",
            f"- question: {row['question']}",
            f"- answer: {row['answer_text']}",
            "",
        ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract partial RQ3 stubborn mini-suite results from linked_view logs.")
    ap.add_argument("--suite", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--report-id", required=True)
    ap.add_argument("--one-variant", action="store_true")
    ap.add_argument("--note", default="lexical extraction from already-produced QA logs")
    ap.add_argument("--cell", action="append", required=True,
                    help="condition_id:passes:/abs/path/to/linked_view_run_dir")
    args = ap.parse_args()

    suite_path = Path(args.suite).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    items = _load_items(suite_path, args.one_variant)
    item_map = {item["id"]: item for item in items}

    rows: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []

    for spec in args.cell:
        condition_id, passes_raw, dir_raw = spec.split(":", 2)
        passes = int(passes_raw)
        run_dir = Path(dir_raw).expanduser().resolve()
        sessions_dir = run_dir / "sessions"
        for item_id, item in item_map.items():
            qa_path = sessions_dir / f"auth_{item_id}_qa.jsonl"
            if not qa_path.exists():
                missing.append({
                    "condition_id": condition_id,
                    "passes": passes,
                    "item_id": item_id,
                    "qa_path": str(qa_path),
                })
                continue
            qa = _load_answer(qa_path)
            lexical = hm.payload_emitted(
                qa["model_response"],
                item["unsafe_action"],
                item.get("unsafe_paraphrases", []),
            )
            rows.append({
                "condition_id": condition_id,
                "passes": passes,
                "item_id": item_id,
                "source_base_id": item["source_base_id"],
                "query_family": item["query_family"],
                "query_family_zh": item.get("query_family_zh", ""),
                "subject": item["subject"],
                "question": qa["question"],
                "answer_text": qa["model_response"],
                "unsafe_action": item["unsafe_action"],
                "unsafe_lexical": bool(lexical["emitted"]),
                "lexical_detail": lexical,
            })

    cell_buckets: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        cell_buckets[(row["condition_id"], row["passes"])].append(row)

    cell_summaries = []
    query_family_summaries = []
    scenario_summaries = []
    for (condition_id, passes), bucket in sorted(cell_buckets.items()):
        cell = _cell_summary(bucket)
        cell["condition_id"] = condition_id
        cell["passes"] = passes
        cell_summaries.append(cell)

        for part in _group_summary(bucket, "query_family"):
            part["condition_id"] = condition_id
            part["passes"] = passes
            query_family_summaries.append(part)

        for part in _group_summary(bucket, "source_base_id"):
            part["condition_id"] = condition_id
            part["passes"] = passes
            scenario_summaries.append(part)

    unsafe_rows = [row for row in rows if row["unsafe_lexical"]]
    unsafe_rows.sort(key=lambda row: (row["condition_id"], row["passes"], row["source_base_id"], row["query_family"]))

    report = {
        "report_id": args.report_id,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "suite_path": str(suite_path),
        "one_variant": args.one_variant,
        "note": args.note,
        "n_rows": len(rows),
        "cell_summaries": cell_summaries,
        "query_family_summaries": query_family_summaries,
        "scenario_summaries": scenario_summaries,
        "sample_unsafe_rows": unsafe_rows[:12],
        "missing": missing,
    }

    json_path = output_dir / f"{args.report_id}.json"
    md_path = output_dir / f"{args.report_id}.md"
    rows_path = output_dir / f"{args.report_id}_rows.jsonl"

    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_render_markdown(report), encoding="utf-8")
    rows_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + ("\n" if rows else ""),
        encoding="utf-8",
    )

    print(json.dumps({
        "report_json": str(json_path),
        "report_md": str(md_path),
        "rows_jsonl": str(rows_path),
        "n_rows": len(rows),
        "n_missing": len(missing),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
