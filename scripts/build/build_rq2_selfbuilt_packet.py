#!/usr/bin/env python3
"""Build a paper-facing packet for the self-built RQ2 line.

Inputs:
  - one or more report JSONs produced by run_rq2_factual_poison.py

Outputs:
  - markdown summary table
  - csv with all tiermem rows for manual annotation
  - csv with item-level behaviour patterns across depth / seed
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "state"


def load_reports(paths: list[str]) -> list[dict[str, Any]]:
    reports = []
    for path_str in paths:
        path = Path(path_str).expanduser().resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["_path"] = str(path)
        reports.append(payload)
    return reports


def row_contains(answer: str, needle: str) -> bool:
    return needle.lower() in (answer or "").lower()


def classify_pattern(labels_by_depth: dict[int, list[str]]) -> str:
    depth_keys = sorted(labels_by_depth)
    collapsed = {k: ("FALSE_BELIEF" if "FALSE_BELIEF" in v else "non_false") for k, v in labels_by_depth.items()}
    ordered = [collapsed[k] for k in depth_keys]
    if ordered and all(v == "FALSE_BELIEF" for v in ordered):
        return "always_false"
    if ordered and all(v == "non_false" for v in ordered):
        return "always_non_false"
    if len(ordered) >= 2 and ordered[0] == "non_false" and any(v == "FALSE_BELIEF" for v in ordered[1:]):
        return "turns_false_after_consolidation"
    if len(ordered) >= 2 and ordered[0] == "FALSE_BELIEF" and any(v == "non_false" for v in ordered[1:]):
        return "recovers_after_consolidation"
    return "mixed"


def build_tables(reports: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    summary_rows: list[dict[str, Any]] = []
    annotation_rows: list[dict[str, Any]] = []
    pattern_rows: list[dict[str, Any]] = []

    tiermem_reports = [r for r in reports if r.get("backend") == "tiermem"]
    prompt_reports = [r for r in reports if r.get("backend") == "prompt_only"]

    for report in sorted(tiermem_reports, key=lambda r: (",".join(r.get("families", [])), r.get("seed", 0), str(r.get("report_id", "")))):
        family = ",".join(report.get("families") or []) or "mixed"
        for cond in report.get("conditions", []):
            fb = cond["false_belief_rate"]
            summary_rows.append({
                "line": "selfbuilt_tiermem",
                "family": family,
                "seed": report.get("seed"),
                "passes": cond["passes"],
                "n_probes": cond["n_probes"],
                "n_base_items": cond["n_base_items"],
                "false_belief_k": fb["k"],
                "false_belief_n": fb["n"],
                "false_belief_rate": round(fb["point"], 3),
                "report_id": report["report_id"],
            })
        for row in report.get("rows", []):
            answer = row.get("answer", "")
            annotation_rows.append({
                "report_id": report["report_id"],
                "family": row.get("family", family),
                "seed": report.get("seed"),
                "passes": row.get("passes"),
                "base_id": row.get("base_id"),
                "query_mode": row.get("query_mode"),
                "auto_label": row.get("label"),
                "true_v": row.get("true_v"),
                "false_v": row.get("false_v"),
                "answer": answer,
                "mentions_true_value": row_contains(answer, row.get("true_v", "")),
                "mentions_false_value": row_contains(answer, row.get("false_v", "")),
                "human_label": "",
                "notes": "",
            })

    for report in sorted(prompt_reports, key=lambda r: (r.get("repetition", 0), str(r.get("report_id", "")))):
        for cond in report.get("conditions", []):
            fb = cond["false_belief_rate"]
            summary_rows.append({
                "line": "selfbuilt_prompt_only",
                "family": "all_v2",
                "seed": report.get("seed"),
                "passes": cond["passes"],
                "n_probes": cond["n_probes"],
                "n_base_items": cond["n_base_items"],
                "false_belief_k": fb["k"],
                "false_belief_n": fb["n"],
                "false_belief_rate": round(fb["point"], 3),
                "report_id": report["report_id"],
            })

    grouped: dict[tuple[str, str, int | None], dict[int, list[str]]] = defaultdict(lambda: defaultdict(list))
    mode_grouped: dict[tuple[str, str, int | None], set[str]] = defaultdict(set)
    for report in tiermem_reports:
        family = ",".join(report.get("families") or []) or "mixed"
        seed = report.get("seed")
        for row in report.get("rows", []):
            key = (family, row.get("base_id"), seed)
            grouped[key][int(row.get("passes", 0))].append(row.get("label", "OTHER"))
            mode_grouped[key].add(row.get("query_mode", ""))
    for (family, base_id, seed), labels_by_depth in sorted(grouped.items()):
        pattern_rows.append({
            "family": family,
            "base_id": base_id,
            "seed": seed,
            "depths_seen": ",".join(str(k) for k in sorted(labels_by_depth)),
            "query_modes": ",".join(sorted(mode_grouped[(family, base_id, seed)])),
            "pattern": classify_pattern(labels_by_depth),
            **{f"N{k}": "|".join(labels_by_depth[k]) for k in sorted(labels_by_depth)},
        })
    return summary_rows, annotation_rows, pattern_rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, summary_rows: list[dict[str, Any]], pattern_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# RQ2 自建版汇总包",
        "",
        "这份包只对应 **自建版**，不和官方 benchmark 线混写。",
        "",
        "## 1. 汇总表",
        "",
        "| line | family | seed | passes | false belief | n_probes | report_id |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary_rows:
        lines.append(
            f"| {row['line']} | {row['family']} | {row['seed']} | {row['passes']} | "
            f"{row['false_belief_k']}/{row['false_belief_n']} = {row['false_belief_rate']:.3f} | "
            f"{row['n_probes']} | `{row['report_id']}` |"
        )
    lines.extend([
        "",
        "## 2. 逐题模式表",
        "",
        "| family | base_id | seed | depths | pattern | details |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in pattern_rows:
        details = ", ".join(f"{k}={v}" for k, v in row.items() if k.startswith("N"))
        lines.append(
            f"| {row['family']} | {row['base_id']} | {row['seed']} | {row['depths_seen']} | "
            f"{row['pattern']} | {details} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--reports", nargs="+", required=True)
    p.add_argument("--output-prefix", default="rq2_selfbuilt_packet_20260707")
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = p.parse_args()

    reports = load_reports(args.reports)
    summary_rows, annotation_rows, pattern_rows = build_tables(reports)
    out_dir = Path(args.output_dir).expanduser().resolve()
    prefix = args.output_prefix

    write_markdown(out_dir / f"{prefix}.md", summary_rows, pattern_rows)
    write_csv(out_dir / f"{prefix}_summary.csv", summary_rows)
    write_csv(out_dir / f"{prefix}_annotation.csv", annotation_rows)
    write_csv(out_dir / f"{prefix}_patterns.csv", pattern_rows)

    print(json.dumps({
        "markdown": str(out_dir / f"{prefix}.md"),
        "summary_csv": str(out_dir / f"{prefix}_summary.csv"),
        "annotation_csv": str(out_dir / f"{prefix}_annotation.csv"),
        "patterns_csv": str(out_dir / f"{prefix}_patterns.csv"),
        "n_reports": len(reports),
        "n_annotation_rows": len(annotation_rows),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
