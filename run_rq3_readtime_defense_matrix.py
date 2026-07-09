#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent
RQ3_SCRIPT = PROJECT_ROOT / "run_rq3_provenance_clean.py"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "safety"
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env.v3"
DEFAULT_SEEDS = [11, 17, 23, 29, 31]
DEFAULT_TIERMEM_PASSES = [0, 1, 2, 4, 8, 16]
DEFENSE_MODE_TO_CONDITION = {
    "on": "defense_priority_rule",
    "priority_rule": "defense_priority_rule",
    "source_trust": "defense_source_trust",
    "uncertainty_gate": "defense_uncertainty_gate",
    "conservative_compaction": "defense_conservative_compaction",
    "full_method": "defense_full_method",
}


def _parse_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        raise FileNotFoundError(f"env file not found: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        env[key] = value
    return env


@dataclass
class Job:
    report_id: str
    seed: int
    backend: str
    defense: str
    passes: list[int]
    output_json: str
    output_items_jsonl: str
    cmd: list[str]
    status: str = "pending"
    started_at: str | None = None
    finished_at: str | None = None
    returncode: int | None = None


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Batch launcher for the large RQ3 read-time defense sweep."
    )
    p.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument("--run-tag", default="rq3_readtime_large_20260708")
    p.add_argument("--model", default="gpt-4.1-mini")
    p.add_argument("--suite", default=None, help="Optional safety suite path.")
    p.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS)
    p.add_argument(
        "--backends",
        nargs="+",
        choices=["prompt_only", "tiermem"],
        default=["prompt_only", "tiermem"],
    )
    p.add_argument(
        "--defense-modes",
        nargs="+",
        choices=sorted(DEFENSE_MODE_TO_CONDITION),
        default=["priority_rule", "source_trust", "uncertainty_gate", "conservative_compaction", "full_method"],
    )
    p.add_argument("--tiermem-passes", nargs="+", type=int, default=DEFAULT_TIERMEM_PASSES)
    p.add_argument("--route-mode", choices=["auto", "summary_only", "research_only"], default="summary_only")
    p.add_argument("--item-limit", type=int, default=0)
    p.add_argument("--one-variant", action="store_true")
    p.add_argument("--judge-model", default=None)
    p.add_argument("--skip-existing", action="store_true")
    p.add_argument("--continue-on-error", action="store_true")
    p.add_argument("--max-jobs", type=int, default=0, help="Run only the first K jobs (0 = all).")
    p.add_argument("--dry-run", action="store_true")
    return p


def _backend_label(backend: str) -> str:
    return "po" if backend == "prompt_only" else "tm"


def _build_jobs(args: argparse.Namespace, output_dir: Path) -> list[Job]:
    jobs: list[Job] = []
    for seed in args.seeds:
        for backend in args.backends:
            passes = [0] if backend == "prompt_only" else list(args.tiermem_passes)
            for defense in args.defense_modes:
                condition_id = DEFENSE_MODE_TO_CONDITION[defense]
                report_id = f"{args.run_tag}_{_backend_label(backend)}_{defense}_seed{seed}"
                report_json = output_dir / f"{report_id}.json"
                report_items = output_dir / f"{report_id}_items.jsonl"
                cmd = [
                    sys.executable,
                    str(RQ3_SCRIPT),
                    "--backends",
                    backend,
                    "--conditions",
                    "policy_only",
                    "conflict_baseline",
                    condition_id,
                    "poison_only",
                    "--query-mode",
                    "neutral",
                    "--seed",
                    str(seed),
                    "--model",
                    args.model,
                    "--judge-model",
                    args.judge_model or args.model,
                    "--route-mode",
                    args.route_mode,
                    "--report-id",
                    report_id,
                    "--output-dir",
                    str(output_dir),
                ]
                if args.suite:
                    cmd.extend(["--suite", args.suite])
                if args.item_limit:
                    cmd.extend(["--item-limit", str(args.item_limit)])
                if args.one_variant:
                    cmd.append("--one-variant")
                if backend == "tiermem":
                    cmd.extend(["--passes", *[str(x) for x in passes]])
                jobs.append(
                    Job(
                        report_id=report_id,
                        seed=seed,
                        backend=backend,
                        defense=defense,
                        passes=passes,
                        output_json=str(report_json),
                        output_items_jsonl=str(report_items),
                        cmd=cmd,
                    )
                )
    if args.max_jobs > 0:
        jobs = jobs[: args.max_jobs]
    return jobs


def _write_manifest(path: Path, args: argparse.Namespace, jobs: list[Job]) -> None:
    payload: dict[str, Any] = {
        "run_tag": args.run_tag,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "config": {
            "model": args.model,
            "judge_model": args.judge_model or args.model,
            "suite": args.suite,
            "seeds": args.seeds,
            "backends": args.backends,
            "defense_modes": args.defense_modes,
            "tiermem_passes": args.tiermem_passes,
            "route_mode": args.route_mode,
            "item_limit": args.item_limit,
            "one_variant": args.one_variant,
            "skip_existing": args.skip_existing,
        },
        "jobs": [asdict(job) for job in jobs],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    args = _build_parser().parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    merged_env = os.environ.copy()
    if args.env_file:
        merged_env.update(_parse_env_file(Path(args.env_file).expanduser().resolve()))
    if not merged_env.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is missing. Use --env-file or export it first.")

    jobs = _build_jobs(args, output_dir)
    manifest_path = output_dir / f"{args.run_tag}_manifest.json"
    _write_manifest(manifest_path, args, jobs)

    if args.dry_run:
        print(json.dumps({"manifest": str(manifest_path), "jobs": [asdict(j) for j in jobs]}, ensure_ascii=False, indent=2))
        return 0

    print(f"[rq3-matrix] manifest: {manifest_path}")
    for idx, job in enumerate(jobs, start=1):
        output_json = Path(job.output_json)
        if args.skip_existing and output_json.exists():
            job.status = "skipped_existing"
            job.finished_at = datetime.now().isoformat(timespec="seconds")
            print(f"[rq3-matrix] {idx}/{len(jobs)} skip {job.report_id}")
            _write_manifest(manifest_path, args, jobs)
            continue

        job.status = "running"
        job.started_at = datetime.now().isoformat(timespec="seconds")
        _write_manifest(manifest_path, args, jobs)
        print(
            f"[rq3-matrix] {idx}/{len(jobs)} start {job.report_id} "
            f"(backend={job.backend} defense={job.defense} seed={job.seed})"
        )
        proc = subprocess.run(job.cmd, cwd=str(PROJECT_ROOT), env=merged_env)
        job.returncode = proc.returncode
        job.finished_at = datetime.now().isoformat(timespec="seconds")
        if proc.returncode == 0 and output_json.exists():
            job.status = "completed"
            print(f"[rq3-matrix] done {job.report_id}")
        else:
            job.status = "failed"
            print(f"[rq3-matrix] failed {job.report_id} rc={proc.returncode}")
            _write_manifest(manifest_path, args, jobs)
            if not args.continue_on_error:
                return proc.returncode
        _write_manifest(manifest_path, args, jobs)

    print(json.dumps({"run_tag": args.run_tag, "manifest": str(manifest_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
