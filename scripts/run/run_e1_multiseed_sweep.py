#!/usr/bin/env python3
"""E1 multi-seed depth sweep launcher (with cost-estimating dry-run).

This is the *live* half of upgrading E1 from a single-seed pilot signal to a
statistically defensible result. It runs the HaluMem depth sweep across several
seeds, where -- because the reader decodes at temperature=0.0 -- each seed is a
reproducible random subsample of the evaluation QA (via the seeded slicing added
to ``run_v2_tiermem_micro_slice.py``). Between-seed variability then captures the
"which items did we happen to pick" uncertainty that the single-15/45-QA pilots
could not, and is consumed by ``run_e1_multiseed_statistics.py``.

Per seed the launcher: runs one micro-slice per consolidation depth, assembles a
per-seed sweep report, and runs the failure-mode judge on it. It therefore spends
real API budget when executed. Use ``--dry-run`` first to see the exact command
grid plus an API-cost / wall-clock estimate grounded in the cost telemetry of the
existing runs -- nothing is executed under ``--dry-run``.

Examples
--------
    # See the plan + cost estimate, run nothing:
    python3 run_e1_multiseed_sweep.py --dry-run

    # Actually launch (spends API budget); load the key first:
    set -a && source .env.v3 && set +a
    python3 run_e1_multiseed_sweep.py --seeds 11 23 47 89 131 --passes 0 1 2 4 8 16
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MICRO_RUNNER = PROJECT_ROOT / "run_v2_tiermem_micro_slice.py"
JUDGE_RUNNER = PROJECT_ROOT / "run_v2_tiermem_micro_failure_mode_judge.py"
STATS_RUNNER = PROJECT_ROOT / "run_e1_multiseed_statistics.py"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "v2_tiermem_micro"
MICRO_REPORTS = OUTPUT_DIR / "micro_reports"

# Default multi-seed set matches the legacy PSU seed family so results are
# comparable, extended to five seeds as the plan's ">=5 seeds" asks.
DEFAULT_SEEDS = [11, 23, 47, 89, 131]
DEFAULT_PASSES = [0, 1, 2, 4, 8, 16]

# gpt-4.1-mini approximate list price (USD per 1M tokens). Override via CLI.
DEFAULT_PRICE_IN = 0.40
DEFAULT_PRICE_OUT = 1.60


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Multi-seed E1 HaluMem depth sweep launcher.")
    p.add_argument("--benchmark", choices=["halumem", "locomo", "longmemeval"], default="halumem")
    p.add_argument("--route-mode", choices=["auto", "summary_only", "research_only"], default="summary_only")
    p.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS)
    p.add_argument("--passes", nargs="+", type=int, default=DEFAULT_PASSES)
    p.add_argument("--session-limit", type=int, default=1)
    p.add_argument("--qa-limit", type=int, default=15)
    p.add_argument("--session-pool", type=int, default=0,
                   help="If > session_limit, each seed draws sessions from this larger pool.")
    p.add_argument("--sample-qa", action=argparse.BooleanOptionalAction, default=True,
                   help="Seeded random QA subsample per session (default on; the point of multi-seed).")
    p.add_argument("--model", type=str, default="gpt-4.1-mini")
    p.add_argument("--consolidation-scope", choices=["auto", "all_pages", "qa_retrieved_pages"],
                   default="qa_retrieved_pages")
    p.add_argument("--consolidation-warmup-top-k", type=int, default=10)
    p.add_argument("--page-write-mode", choices=["raw", "infer"], default="infer")
    p.add_argument("--qa-max-workers", type=int, default=1,
                   help="Parallel workers for the QA/eval phase (passed through to the micro-slice).")
    p.add_argument("--write-max-workers", type=int, default=1,
                   help="Parallel workers for the memory-write phase (passed through to the micro-slice).")
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--max-research-iters", type=int, default=3)
    p.add_argument("--judge-model", type=str, default="gpt-4.1-mini")
    p.add_argument("--run-prefix", type=str, default=None)
    p.add_argument("--output-dir", type=str, default=str(OUTPUT_DIR))
    p.add_argument("--skip-existing", action="store_true")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the command grid and cost estimate; execute nothing.")
    p.add_argument("--price-in", type=float, default=DEFAULT_PRICE_IN, help="USD per 1M input tokens.")
    p.add_argument("--price-out", type=float, default=DEFAULT_PRICE_OUT, help="USD per 1M output tokens.")
    return p


def _observed_cost(route_mode: str, passes: int) -> Optional[dict[str, float]]:
    """Average the real cost telemetry of any existing micro_report matching
    this (route_mode, passes). Grounds the dry-run estimate in real runs."""
    calls, toks_in, toks_out, latency = [], [], [], []
    for path in MICRO_REPORTS.glob("*.json"):
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("route_mode") != route_mode:
            continue
        if int(d.get("consolidation_passes", -1)) != passes:
            continue
        overall = (d.get("cost_summary") or {}).get("overall") or {}
        if not overall:
            continue
        calls.append(float(overall.get("total_api_calls", 0) or 0))
        toks_in.append(float(overall.get("total_tokens_in", 0) or 0))
        toks_out.append(float(overall.get("total_tokens_out", 0) or 0))
        latency.append(float(overall.get("total_latency_sec", 0) or 0))
    if not calls:
        return None
    return {
        "api_calls": mean(calls),
        "tokens_in": mean(toks_in),
        "tokens_out": mean(toks_out),
        "latency_sec": mean(latency),
        "n_observed": len(calls),
    }


def _fallback_cost(passes: int) -> dict[str, float]:
    """Heuristic when no matching run exists: cost grows ~linearly with depth."""
    base_calls = 150.0
    return {
        "api_calls": base_calls * (1 + passes),
        "tokens_in": 430000.0 * (1 + passes),
        "tokens_out": 400.0 * (1 + max(1, passes)),
        "latency_sec": 70.0 * (1 + passes),
        "n_observed": 0,
    }


def _estimate(args: argparse.Namespace) -> dict[str, Any]:
    per_condition = []
    for passes in args.passes:
        obs = _observed_cost(args.route_mode, passes) or _fallback_cost(passes)
        per_condition.append({"passes": passes, **obs})
    n_seeds = len(args.seeds)
    tot_calls = sum(c["api_calls"] for c in per_condition) * n_seeds
    tot_in = sum(c["tokens_in"] for c in per_condition) * n_seeds
    tot_out = sum(c["tokens_out"] for c in per_condition) * n_seeds
    tot_latency = sum(c["latency_sec"] for c in per_condition) * n_seeds
    usd = tot_in / 1e6 * args.price_in + tot_out / 1e6 * args.price_out
    return {
        "per_condition": per_condition,
        "n_seeds": n_seeds,
        "n_conditions_total": len(args.passes) * n_seeds,
        "total_api_calls": tot_calls,
        "total_tokens_in": tot_in,
        "total_tokens_out": tot_out,
        "total_latency_sec_serial": tot_latency,
        "est_usd": usd,
    }


def _micro_cmd(args: argparse.Namespace, seed: int, passes: int, run_id: str,
               output_dir: Path) -> list[str]:
    cmd = [
        sys.executable, str(MICRO_RUNNER),
        "--benchmark", args.benchmark,
        "--session-limit", str(args.session_limit),
        "--qa-limit", str(args.qa_limit),
        "--model", args.model,
        "--run-id", run_id,
        "--output-dir", str(output_dir),
        "--route-mode", args.route_mode,
        "--consolidation-passes", str(passes),
        "--consolidation-scope", args.consolidation_scope,
        "--consolidation-warmup-top-k", str(args.consolidation_warmup_top_k),
        "--page-write-mode", args.page_write_mode,
        "--qa-max-workers", str(args.qa_max_workers),
        "--write-max-workers", str(args.write_max_workers),
        "--top-k", str(args.top_k),
        "--max-research-iters", str(args.max_research_iters),
        "--seed", str(seed),
    ]
    if args.sample_qa:
        cmd.append("--sample-qa")
    if args.session_pool:
        cmd.extend(["--session-pool", str(args.session_pool)])
    return cmd


def _run_seed(args: argparse.Namespace, seed: int, prefix: str, output_dir: Path) -> dict[str, Any]:
    """Execute all depths for one seed, assemble a sweep report, run the judge."""
    conditions: list[dict[str, Any]] = []
    for passes in args.passes:
        run_id = f"{prefix}_seed{seed}_{args.route_mode}_n{passes}"
        report_path = MICRO_REPORTS / f"{run_id}.json"
        if not (args.skip_existing and report_path.exists()):
            subprocess.run(_micro_cmd(args, seed, passes, run_id, output_dir), check=True, cwd=str(PROJECT_ROOT))
        conditions.append(json.loads(report_path.read_text(encoding="utf-8")))

    sweep_dir = output_dir / "sweep_reports"
    sweep_dir.mkdir(parents=True, exist_ok=True)
    sweep_id = f"{prefix}_seed{seed}"
    sweep_path = sweep_dir / f"{sweep_id}.json"
    sweep_path.write_text(json.dumps(
        {"sweep_id": sweep_id, "seed": seed, "generated_at": datetime.now().isoformat(),
         "conditions": conditions}, ensure_ascii=False, indent=2), encoding="utf-8")

    judge_id = f"{sweep_id}_judge"
    subprocess.run([
        sys.executable, str(JUDGE_RUNNER),
        "--sweep-report", str(sweep_path),
        "--report-id", judge_id,
        "--judge-model", args.judge_model,
        "--output-dir", str(output_dir / "judge_reports"),
    ], check=True, cwd=str(PROJECT_ROOT))
    judge_path = output_dir / "judge_reports" / f"{judge_id}.json"
    return {"seed": seed, "sweep_report": str(sweep_path), "judge_report": str(judge_path)}


def _print_dry_run(args: argparse.Namespace, prefix: str, est: dict[str, Any]) -> None:
    print(f"# DRY RUN -- nothing executed. prefix={prefix}")
    print(f"# benchmark={args.benchmark} route={args.route_mode} "
          f"seeds={args.seeds} passes={args.passes} "
          f"session_limit={args.session_limit} qa_limit={args.qa_limit} sample_qa={args.sample_qa}")
    print()
    print("Per-depth cost (averaged over matching existing runs; n_observed=0 => heuristic):")
    print("| N | est_api_calls | est_tokens_in | est_tokens_out | est_latency_sec | n_observed |")
    print("| ---: | ---: | ---: | ---: | ---: | ---: |")
    for c in est["per_condition"]:
        print(f"| {c['passes']} | {c['api_calls']:.0f} | {c['tokens_in']:.0f} | "
              f"{c['tokens_out']:.0f} | {c['latency_sec']:.0f} | {int(c['n_observed'])} |")
    print()
    print(f"Totals across {est['n_seeds']} seeds x {len(args.passes)} depths "
          f"= {est['n_conditions_total']} micro-runs + {est['n_seeds']} judge passes:")
    print(f"  ~{est['total_api_calls']:.0f} API calls, "
          f"~{est['total_tokens_in']/1e6:.2f}M in + {est['total_tokens_out']/1e6:.3f}M out tokens")
    print(f"  ~{est['total_latency_sec_serial']/60:.0f} min wall-clock if run serially "
          f"(parallelize with --max-workers inside the runner to cut this)")
    print(f"  ~${est['est_usd']:.2f} estimated (at ${args.price_in}/1M in, ${args.price_out}/1M out; "
          f"judge cost extra, roughly +15-25%)")
    print()
    print("Sample command that WOULD run (seed 0, N 0):")
    print("  " + " ".join(_micro_cmd(args, args.seeds[0], args.passes[0],
                                      f"{prefix}_seed{args.seeds[0]}_{args.route_mode}_n{args.passes[0]}",
                                      Path(args.output_dir).resolve())))
    print()
    print("After a real run, aggregate with:")
    print(f"  python3 {STATS_RUNNER.name} --manifest "
          f"{args.output_dir}/multiseed/{prefix}_manifest.json")


def main() -> int:
    args = _build_parser().parse_args()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = args.run_prefix or f"e1_multiseed_{args.benchmark}_{args.route_mode}_{stamp}"
    est = _estimate(args)

    if args.dry_run:
        _print_dry_run(args, prefix, est)
        return 0

    output_dir = Path(args.output_dir).expanduser().resolve()
    manifest_dir = output_dir / "multiseed"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    seed_entries = [_run_seed(args, seed, prefix, output_dir) for seed in args.seeds]

    manifest = {
        "prefix": prefix,
        "generated_at": datetime.now().isoformat(),
        "benchmark": args.benchmark,
        "route_mode": args.route_mode,
        "seeds": args.seeds,
        "passes": args.passes,
        "qa_limit": args.qa_limit,
        "session_limit": args.session_limit,
        "sample_qa": args.sample_qa,
        "estimate": est,
        "seed_entries": seed_entries,
    }
    manifest_path = manifest_dir / f"{prefix}_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"prefix": prefix, "manifest": str(manifest_path),
                      "seeds_run": len(seed_entries)}, ensure_ascii=False, indent=2))
    print(f"\nAggregate with: python3 {STATS_RUNNER.name} --manifest {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
