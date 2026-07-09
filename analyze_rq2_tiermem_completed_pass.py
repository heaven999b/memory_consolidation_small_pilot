#!/usr/bin/env python3
"""Analyze a completed TierMem pass for the RQ2 factual-poison suite."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_rq2_factual_poison import (
    FactPoisonBackend,
    build_probes,
    classify_answer,
    load_suite,
    summarize_rows,
)

class _Reader(FactPoisonBackend):
    pass


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite-version", choices=["v1", "v2", "v3", "v4", "v5", "v6"], required=True)
    ap.add_argument("--repetition", type=int, required=True)
    ap.add_argument("--query-modes", nargs="+", required=True)
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--page-store-dir", required=True)
    ap.add_argument("--passes", type=int, required=True)
    ap.add_argument("--output-json", default=None)
    return ap


def main() -> int:
    args = _parser().parse_args()
    base_items = load_suite(args.suite_version)
    probes = build_probes(base_items, args.repetition, args.query_modes)

    reader = object.__new__(_Reader)
    extracted = reader._extract(
        Path(args.run_root).resolve(),
        Path(args.page_store_dir).resolve(),
        probes,
    )

    rows = []
    for probe in probes:
        out = extracted[probe["id"]]
        label = classify_answer(out["answer_text"], probe)
        rows.append({
            "id": probe["id"],
            "base_id": probe["base_id"],
            "family": probe["family"],
            "thing": probe["thing"],
            "query_mode": probe["query_mode"],
            "passes": args.passes,
            "true_v": probe["true_v"],
            "false_v": probe["false_v"],
            "answer": out["answer_text"][:200],
            "label": label,
            "states_false": label == "FALSE_BELIEF",
            "states_true": label == "TRUE",
            "consolidated_text": out["consolidated_text"],
        })

    summary = summarize_rows(rows)
    payload = {
        "passes": args.passes,
        "n_base_items": len(base_items),
        "n_probes": len(probes),
        "summary": summary,
        "false_rows": [
            {
                "base_id": row["base_id"],
                "family": row["family"],
                "query_mode": row["query_mode"],
                "answer": row["answer"],
            }
            for row in rows
            if row["label"] == "FALSE_BELIEF"
        ],
    }
    if args.output_json:
        Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
