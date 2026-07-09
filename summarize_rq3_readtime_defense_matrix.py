#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "safety"
DEFAULT_STATE_DIR = PROJECT_ROOT / "state"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Summarize the large RQ3 read-time defense sweep."
    )
    p.add_argument("--run-tag", required=True)
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    return p


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_items(path: Path) -> dict[int, dict[str, bool]]:
    by_pass: dict[int, dict[str, bool]] = defaultdict(dict)
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        row = json.loads(raw)
        by_pass[int(row["passes"])][row["item_id"]] = bool(row["payload_emitted"])
    return dict(by_pass)


def main() -> int:
    args = _build_parser().parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve()
    state_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = output_dir / f"{args.run_tag}_manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifest not found: {manifest_path}")

    manifest = _load_json(manifest_path)
    jobs = manifest["jobs"]

    condition_rows: list[dict[str, Any]] = []
    paired_rows: list[dict[str, Any]] = []
    seed_grouped: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    pair_cache: dict[tuple[int, str, str], dict[int, dict[str, bool]]] = {}

    for job in jobs:
        if job["status"] != "completed":
            continue
        report_path = Path(job["output_json"])
        items_path = Path(job["output_items_jsonl"])
        if not report_path.exists() or not items_path.exists():
            continue
        report = _load_json(report_path)
        items_by_pass = _read_items(items_path)
        pair_cache[(job["seed"], job["backend"], job["defense"])] = items_by_pass
        for cond in report.get("conditions", []):
            metric = cond["payload_emission"]
            row = {
                "run_tag": args.run_tag,
                "report_id": report["report_id"],
                "seed": job["seed"],
                "backend": job["backend"],
                "defense": job["defense"],
                "passes": cond["passes"],
                "k": metric["k"],
                "n": metric["n"],
                "rate": metric["point"],
                "lo": metric["lo"],
                "hi": metric["hi"],
            }
            condition_rows.append(row)
            seed_grouped[(job["backend"], cond["passes"])].append(row)

    for seed in manifest["config"]["seeds"]:
        for backend in manifest["config"]["backends"]:
            off_key = (seed, backend, "off")
            on_key = (seed, backend, "on")
            if off_key not in pair_cache or on_key not in pair_cache:
                continue
            for passes, off_items in pair_cache[off_key].items():
                on_items = pair_cache[on_key].get(passes)
                if not on_items:
                    continue
                ids = sorted(set(off_items) & set(on_items))
                better = sum(1 for iid in ids if off_items[iid] and not on_items[iid])
                worse = sum(1 for iid in ids if (not off_items[iid]) and on_items[iid])
                stay_bad = sum(1 for iid in ids if off_items[iid] and on_items[iid])
                stay_good = sum(1 for iid in ids if (not off_items[iid]) and (not on_items[iid]))
                off_rate = sum(1 for iid in ids if off_items[iid]) / len(ids)
                on_rate = sum(1 for iid in ids if on_items[iid]) / len(ids)
                paired_rows.append(
                    {
                        "run_tag": args.run_tag,
                        "seed": seed,
                        "backend": backend,
                        "passes": passes,
                        "n_items": len(ids),
                        "off_rate": off_rate,
                        "on_rate": on_rate,
                        "delta_on_minus_off": on_rate - off_rate,
                        "better_flips": better,
                        "worse_flips": worse,
                        "stay_bad": stay_bad,
                        "stay_good": stay_good,
                    }
                )

    cond_csv = state_dir / f"{args.run_tag}_condition_summary.csv"
    pair_csv = state_dir / f"{args.run_tag}_paired_summary.csv"
    md_path = state_dir / f"{args.run_tag}_summary.md"

    with cond_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_tag",
                "report_id",
                "seed",
                "backend",
                "defense",
                "passes",
                "k",
                "n",
                "rate",
                "lo",
                "hi",
            ],
        )
        writer.writeheader()
        writer.writerows(condition_rows)

    with pair_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_tag",
                "seed",
                "backend",
                "passes",
                "n_items",
                "off_rate",
                "on_rate",
                "delta_on_minus_off",
                "better_flips",
                "worse_flips",
                "stay_bad",
                "stay_good",
            ],
        )
        writer.writeheader()
        writer.writerows(paired_rows)

    completed = sum(1 for job in jobs if job["status"] == "completed")
    pending = sum(1 for job in jobs if job["status"] not in {"completed", "skipped_existing"})
    skipped = sum(1 for job in jobs if job["status"] == "skipped_existing")

    lines = [
        f"# RQ3 Read-Time Defense Sweep Summary: {args.run_tag}",
        "",
        f"- manifest: `{manifest_path}`",
        f"- completed jobs: `{completed}`",
        f"- skipped existing: `{skipped}`",
        f"- unfinished jobs: `{pending}`",
        f"- condition csv: `{cond_csv}`",
        f"- paired csv: `{pair_csv}`",
        "",
        "## Aggregated by backend x pass",
        "",
        "| backend | pass | seeds_done | off mean | on mean | mean delta | total better flips | total worse flips |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    grouped_pairs: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in paired_rows:
        grouped_pairs[(row["backend"], row["passes"])].append(row)

    for key in sorted(grouped_pairs):
        backend, passes = key
        rows = grouped_pairs[key]
        lines.append(
            "| {backend} | {passes} | {n} | {off:.3f} | {on:.3f} | {delta:.3f} | {better} | {worse} |".format(
                backend=backend,
                passes=passes,
                n=len(rows),
                off=mean(r["off_rate"] for r in rows),
                on=mean(r["on_rate"] for r in rows),
                delta=mean(r["delta_on_minus_off"] for r in rows),
                better=sum(r["better_flips"] for r in rows),
                worse=sum(r["worse_flips"] for r in rows),
            )
        )

    lines.extend(
        [
            "",
            "## Per-seed paired comparison",
            "",
            "| seed | backend | pass | off rate | on rate | delta | better flips | worse flips |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in sorted(paired_rows, key=lambda x: (x["seed"], x["backend"], x["passes"])):
        lines.append(
            "| {seed} | {backend} | {passes} | {off:.3f} | {on:.3f} | {delta:.3f} | {better} | {worse} |".format(
                seed=row["seed"],
                backend=row["backend"],
                passes=row["passes"],
                off=row["off_rate"],
                on=row["on_rate"],
                delta=row["delta_on_minus_off"],
                better=row["better_flips"],
                worse=row["worse_flips"],
            )
        )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "condition_csv": str(cond_csv),
                "paired_csv": str(pair_csv),
                "summary_md": str(md_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
