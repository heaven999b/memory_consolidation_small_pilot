#!/usr/bin/env python3
"""Phase 4a: produce a de-duplicated, ready-to-label RQ2 annotation sheet.

Why: the existing ``state/rq2_manual_annotation_*_zh.csv`` sheets contain many
near-duplicate probes (same base scenario x query mode x question, differing only
by seed / consolidation pass). Labelling all of them would inflate the effective
independent n and bias Cohen's kappa. This tool collapses each unique probe to a
single row, records how many raw rows it represents, and leaves ``human_label``
empty for the human annotator.

Offline, zero API. After a human fills ``human_label`` in the *_dedup.csv, run
``scripts/core/kappa_score.py`` to get kappa (auto_label vs human_label).

Usage:
    python3 scripts/build/build_rq2_clean_annotation_sheet.py
    python3 scripts/build/build_rq2_clean_annotation_sheet.py --inputs a.csv b.csv
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"
DEFAULT_INPUTS = [
    STATE / "rq2_manual_annotation_core_zh.csv",
    STATE / "rq2_manual_annotation_diverse_zh.csv",
    STATE / "rq2_manual_annotation_v4_tiermem_diverse_zh.csv",
]
# One probe = one scenario asked one way. Seed/passes are NOT part of the key,
# so re-asks of the same probe collapse into a single annotation unit.
DEDUP_KEY = ("base_id", "query_mode_zh", "question_zh")


def _key(row: dict) -> tuple:
    return tuple((row.get(k, "") or "").strip() for k in DEDUP_KEY)


def dedup_file(path: Path) -> tuple[list[dict], list[str], int, int]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        return [], [], 0, 0
    fields = list(rows[0].keys())
    if "dedup_group_size" not in fields:
        fields = fields + ["dedup_group_size"]
    seen: dict[tuple, dict] = {}
    for row in rows:
        k = _key(row)
        if k not in seen:
            r = dict(row)
            r["dedup_group_size"] = 1
            r["human_label"] = ""  # ensure blank for the annotator
            seen[k] = r
        else:
            seen[k]["dedup_group_size"] = int(seen[k]["dedup_group_size"]) + 1
    return list(seen.values()), fields, len(rows), len(seen)


def main() -> int:
    ap = argparse.ArgumentParser(description="Dedup RQ2 annotation sheets for clean human labelling.")
    ap.add_argument("--inputs", nargs="*", default=[str(p) for p in DEFAULT_INPUTS])
    ap.add_argument("--suffix", default="_dedup")
    args = ap.parse_args()

    total_before = total_after = 0
    for raw in args.inputs:
        path = Path(raw).expanduser()
        if not path.exists():
            print(f"  skip (missing): {path}")
            continue
        deduped, fields, n_before, n_after = dedup_file(path)
        if not deduped:
            print(f"  skip (empty): {path}")
            continue
        out = path.with_name(path.stem + args.suffix + path.suffix)
        with out.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(deduped)
        total_before += n_before
        total_after += n_after
        print(f"  {path.name}: {n_before} -> {n_after} unique  ({n_before - n_after} near-dups removed)  -> {out.name}")

    print(f"\nTOTAL: {total_before} raw rows -> {total_after} unique probes to label "
          f"({total_before - total_after} redundant rows removed).")
    print("Next: a human fills `human_label` in the *_dedup.csv, then run scripts/core/kappa_score.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
