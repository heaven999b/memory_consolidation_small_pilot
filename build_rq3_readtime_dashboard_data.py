#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "safety"
DEFAULT_STATE_DIR = PROJECT_ROOT / "state"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_items(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        rows.append(json.loads(raw))
    return rows


def _status_counts(jobs: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for job in jobs:
        counts[job.get("status") or "unknown"] += 1
    return dict(counts)


def _rate_to_pct(x: float) -> float:
    return round(x * 100.0, 1)


def build_snapshot(run_tag: str, output_dir: Path, state_dir: Path) -> dict[str, Any]:
    manifest_path = output_dir / f"{run_tag}_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest not found: {manifest_path}")
    manifest = _load_json(manifest_path)
    jobs = manifest["jobs"]

    status_counts = _status_counts(jobs)
    total_jobs = len(jobs)
    completed_jobs = status_counts.get("completed", 0)
    running_jobs = status_counts.get("running", 0)
    pending_jobs = status_counts.get("pending", 0)
    failed_jobs = status_counts.get("failed", 0)
    skipped_jobs = status_counts.get("skipped_existing", 0)

    condition_rows: list[dict[str, Any]] = []
    pair_rows: list[dict[str, Any]] = []
    conditions_by_job: dict[tuple[int, str, str], dict[int, dict[str, Any]]] = defaultdict(dict)
    items_by_job: dict[tuple[int, str, str], dict[int, dict[str, dict[str, Any]]]] = {}

    for job in jobs:
        report_path = Path(job["output_json"])
        items_path = Path(job["output_items_jsonl"])
        if not report_path.exists() or not items_path.exists():
            continue

        report = _load_json(report_path)
        item_rows = _read_items(items_path)
        key = (job["seed"], job["backend"], job["defense"])

        by_pass: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
        for row in item_rows:
            by_pass[int(row["passes"])][row["item_id"]] = row
        items_by_job[key] = dict(by_pass)

        for cond in report.get("conditions", []):
            metric = cond["payload_emission"]
            c = {
                "report_id": report["report_id"],
                "backend": job["backend"],
                "defense": job["defense"],
                "seed": job["seed"],
                "passes": cond["passes"],
                "n_items": cond["n_items"],
                "rate": metric["point"],
                "rate_pct": _rate_to_pct(metric["point"]),
                "k": metric["k"],
                "n": metric["n"],
                "lo": metric["lo"],
                "hi": metric["hi"],
                "lo_pct": _rate_to_pct(metric["lo"]),
                "hi_pct": _rate_to_pct(metric["hi"]),
                "generated_at": report.get("generated_at"),
            }
            condition_rows.append(c)
            conditions_by_job[key][int(cond["passes"])] = c

    for seed in manifest["config"]["seeds"]:
        for backend in manifest["config"]["backends"]:
            off_key = (seed, backend, "off")
            on_key = (seed, backend, "on")
            if off_key not in items_by_job or on_key not in items_by_job:
                continue
            off_passes = items_by_job[off_key]
            on_passes = items_by_job[on_key]
            shared_passes = sorted(set(off_passes) & set(on_passes))
            for p in shared_passes:
                off_rows = off_passes[p]
                on_rows = on_passes[p]
                ids = sorted(set(off_rows) & set(on_rows))
                if not ids:
                    continue
                better = 0
                worse = 0
                changed_examples: list[dict[str, Any]] = []
                for iid in ids:
                    off_emit = bool(off_rows[iid]["payload_emitted"])
                    on_emit = bool(on_rows[iid]["payload_emitted"])
                    if off_emit and not on_emit:
                        better += 1
                        if len(changed_examples) < 8:
                            changed_examples.append(
                                {
                                    "item_id": iid,
                                    "subject": off_rows[iid].get("subject", ""),
                                    "off_answer": off_rows[iid].get("answer_text", "")[:220],
                                    "on_answer": on_rows[iid].get("answer_text", "")[:220],
                                }
                            )
                    elif (not off_emit) and on_emit:
                        worse += 1
                off_rate = sum(1 for iid in ids if bool(off_rows[iid]["payload_emitted"])) / len(ids)
                on_rate = sum(1 for iid in ids if bool(on_rows[iid]["payload_emitted"])) / len(ids)
                pair_rows.append(
                    {
                        "seed": seed,
                        "backend": backend,
                        "passes": p,
                        "n_items": len(ids),
                        "off_rate": off_rate,
                        "off_rate_pct": _rate_to_pct(off_rate),
                        "on_rate": on_rate,
                        "on_rate_pct": _rate_to_pct(on_rate),
                        "delta": on_rate - off_rate,
                        "delta_pp": round((on_rate - off_rate) * 100.0, 1),
                        "better_flips": better,
                        "worse_flips": worse,
                        "examples": changed_examples,
                    }
                )

    aggregate_rows: list[dict[str, Any]] = []
    grouped_pairs: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in pair_rows:
        grouped_pairs[(row["backend"], row["passes"])].append(row)

    for (backend, passes), rows in sorted(grouped_pairs.items()):
        aggregate_rows.append(
            {
                "backend": backend,
                "passes": passes,
                "seeds_done": len(rows),
                "off_mean": mean(r["off_rate"] for r in rows),
                "off_mean_pct": _rate_to_pct(mean(r["off_rate"] for r in rows)),
                "on_mean": mean(r["on_rate"] for r in rows),
                "on_mean_pct": _rate_to_pct(mean(r["on_rate"] for r in rows)),
                "delta_mean": mean(r["delta"] for r in rows),
                "delta_mean_pp": round(mean(r["delta"] for r in rows) * 100.0, 1),
                "better_total": sum(r["better_flips"] for r in rows),
                "worse_total": sum(r["worse_flips"] for r in rows),
            }
        )

    pair_rows_sorted = sorted(pair_rows, key=lambda r: (r["delta_pp"], r["backend"], r["seed"], r["passes"]))
    best_pair = pair_rows_sorted[0] if pair_rows_sorted else None
    latest_completed = sorted(
        condition_rows,
        key=lambda r: (r.get("generated_at") or "", r["report_id"], r["passes"]),
        reverse=True,
    )[:8]

    job_cards = []
    for job in jobs:
        report_path = Path(job["output_json"])
        items_path = Path(job["output_items_jsonl"])
        job_cards.append(
            {
                "report_id": job["report_id"],
                "seed": job["seed"],
                "backend": job["backend"],
                "defense": job["defense"],
                "passes": job["passes"],
                "status": job["status"],
                "started_at": job.get("started_at"),
                "finished_at": job.get("finished_at"),
                "report_exists": report_path.exists(),
                "items_exists": items_path.exists(),
            }
        )

    return {
        "run_tag": run_tag,
        "snapshot_at": datetime.now().isoformat(timespec="seconds"),
        "manifest_path": str(manifest_path),
        "config": manifest["config"],
        "counts": {
            "total_jobs": total_jobs,
            "completed_jobs": completed_jobs,
            "running_jobs": running_jobs,
            "pending_jobs": pending_jobs,
            "failed_jobs": failed_jobs,
            "skipped_jobs": skipped_jobs,
            "completion_pct": round((completed_jobs + skipped_jobs) / total_jobs * 100.0, 1) if total_jobs else 0.0,
        },
        "aggregate_rows": aggregate_rows,
        "pair_rows": sorted(pair_rows, key=lambda r: (r["backend"], r["passes"], r["seed"])),
        "condition_rows": sorted(condition_rows, key=lambda r: (r["backend"], r["seed"], r["defense"], r["passes"])),
        "job_cards": job_cards,
        "best_pair": best_pair,
        "latest_completed": latest_completed,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Build dashboard data for the RQ3 read-time defense sweep.")
    p.add_argument("--run-tag", required=True)
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    args = p.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve()
    state_dir.mkdir(parents=True, exist_ok=True)

    snapshot = build_snapshot(args.run_tag, output_dir, state_dir)
    out_path = state_dir / f"{args.run_tag}_dashboard_data.json"
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"dashboard_data": str(out_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
