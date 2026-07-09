#!/usr/bin/env python3
"""Offline rescoring for existing self-built RQ2 report JSONs.

Use this after improving the answer classifier so we can correct old runs
without paying API cost again.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_rq2_factual_poison import classify_answer, load_suite, summarize_rows


def rescore_report(path: Path) -> Path:
    report = json.loads(path.read_text(encoding="utf-8"))
    suite = {item["id"]: item for item in load_suite(report.get("suite_version", "v2"))}

    rescored_rows = []
    by_pass: dict[int, list[dict]] = {}
    for row in report.get("rows", []):
        item = dict(suite[row["base_id"]])
        item["query_mode"] = row["query_mode"]
        label = classify_answer(row.get("answer", ""), item)
        new_row = dict(row)
        new_row["label"] = label
        new_row["states_false"] = label == "FALSE_BELIEF"
        new_row["states_true"] = label == "TRUE"
        rescored_rows.append(new_row)
        by_pass.setdefault(int(new_row["passes"]), []).append(new_row)

    report["rows"] = rescored_rows
    report["conditions"] = [{"passes": n, **summarize_rows(rows)} for n, rows in sorted(by_pass.items())]

    out_path = path.with_name(path.stem + "_rescored.json")
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--reports", nargs="+", required=True)
    args = p.parse_args()
    outs = [str(rescore_report(Path(r).expanduser().resolve())) for r in args.reports]
    print(json.dumps({"rescored_reports": outs}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
