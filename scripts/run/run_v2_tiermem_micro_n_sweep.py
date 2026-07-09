#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MICRO_RUNNER = PROJECT_ROOT / "scripts" / "run" / "run_v2_tiermem_micro_slice.py"
DEFAULT_PAGE_SIZE = 4000
DEFAULT_PASSES = [0, 1, 2, 4, 8, 16]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a TierMem micro sweep over route mode and the full planned N grid."
    )
    parser.add_argument("--benchmark", choices=["locomo", "longmemeval", "halumem"], default="locomo")
    parser.add_argument("--session-limit", type=int, default=1)
    parser.add_argument("--qa-limit", type=int, default=5)
    parser.add_argument("--model", type=str, default="gpt-4.1-mini")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "outputs" / "v2_tiermem_micro"),
    )
    parser.add_argument(
        "--qdrant-path",
        type=str,
        default=str(PROJECT_ROOT / "outputs" / "tiermem_local_qdrant_micro"),
    )
    parser.add_argument("--max-workers", type=int, default=1)
    parser.add_argument("--write-max-workers", type=int, default=1)
    parser.add_argument("--qa-max-workers", type=int, default=1)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-research-iters", type=int, default=3)
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument(
        "--consolidation-scope",
        choices=["auto", "all_pages", "qa_retrieved_pages"],
        default="auto",
    )
    parser.add_argument("--consolidation-target-max-pages", type=int, default=0)
    parser.add_argument("--consolidation-warmup-top-k", type=int, default=0)
    parser.add_argument("--page-write-mode", choices=["raw", "infer"], default="raw")
    parser.add_argument("--abstain-on-unsupported", action="store_true")
    parser.add_argument("--router-threshold", type=float, default=0.5)
    parser.add_argument("--router-type", choices=["openai", "vllm", "llm"], default="openai")
    parser.add_argument("--router-model", type=str, default=None)
    parser.add_argument("--router-base-url", type=str, default=None)
    parser.add_argument("--router-api-key", type=str, default=None)
    parser.add_argument(
        "--route-modes",
        nargs="+",
        default=["summary_only", "research_only"],
        choices=["auto", "summary_only", "research_only"],
    )
    parser.add_argument("--passes", nargs="+", type=int, default=DEFAULT_PASSES)
    parser.add_argument("--run-prefix", type=str, default=None)
    parser.add_argument("--skip-existing", action="store_true")
    return parser


def _run_condition(args: argparse.Namespace, route_mode: str, passes: int, run_id: str) -> dict[str, Any]:
    output_dir = Path(args.output_dir).expanduser().resolve()
    report_path = output_dir / "micro_reports" / f"{run_id}.json"

    if args.skip_existing and report_path.exists():
        return json.loads(report_path.read_text(encoding="utf-8"))

    cmd = [
        sys.executable,
        str(MICRO_RUNNER),
        "--benchmark",
        args.benchmark,
        "--session-limit",
        str(args.session_limit),
        "--qa-limit",
        str(args.qa_limit),
        "--model",
        args.model,
        "--run-id",
        run_id,
        "--output-dir",
        str(output_dir),
        "--qdrant-path",
        str(Path(args.qdrant_path).expanduser().resolve()),
        "--max-workers",
        str(args.max_workers),
        "--write-max-workers",
        str(args.write_max_workers),
        "--qa-max-workers",
        str(args.qa_max_workers),
        "--top-k",
        str(args.top_k),
        "--max-research-iters",
        str(args.max_research_iters),
        "--page-size",
        str(args.page_size),
        "--consolidation-scope",
        args.consolidation_scope,
        "--consolidation-target-max-pages",
        str(args.consolidation_target_max_pages),
        "--consolidation-warmup-top-k",
        str(args.consolidation_warmup_top_k),
        "--page-write-mode",
        args.page_write_mode,
        "--router-threshold",
        str(args.router_threshold),
        "--router-type",
        args.router_type,
        "--route-mode",
        route_mode,
        "--consolidation-passes",
        str(passes),
    ]
    if args.abstain_on_unsupported:
        cmd.append("--abstain-on-unsupported")
    if args.router_model:
        cmd.extend(["--router-model", args.router_model])
    if args.router_base_url:
        cmd.extend(["--router-base-url", args.router_base_url])
    if args.router_api_key:
        cmd.extend(["--router-api-key", args.router_api_key])

    subprocess.run(cmd, check=True, cwd=str(PROJECT_ROOT))
    return json.loads(report_path.read_text(encoding="utf-8"))


def _write_sweep_report(output_dir: Path, sweep_id: str, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    report_dir = output_dir / "sweep_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / f"{sweep_id}.json"
    md_path = report_dir / f"{sweep_id}.md"

    payload = {
        "sweep_id": sweep_id,
        "generated_at": datetime.now().isoformat(),
        "conditions": rows,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# TierMem Micro N-Sweep: {sweep_id}",
        "",
        "| route_mode | passes | answered | F1 | BLEU1 | exact_ref | route_counts | overall_cost | run_id |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        overall_cost = ((row.get("cost_summary") or {}).get("overall") or {})
        lines.append(
            "| {route_mode} | {passes} | {answered} | {f1:.3f} | {bleu1:.3f} | {exact_ref:.3f} | `{route_counts}` | `{overall_cost}` | `{run_id}` |".format(
                route_mode=row.get("route_mode"),
                passes=row.get("consolidation_passes"),
                answered=row.get("answered"),
                f1=float(row.get("summary_f1", 0.0) or 0.0),
                bleu1=float(row.get("summary_bleu1", 0.0) or 0.0),
                exact_ref=float(row.get("mean_exact_match", 0.0) or 0.0),
                route_counts=row.get("route_counts"),
                overall_cost=overall_cost,
                run_id=row.get("run_id"),
            )
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    args = _build_parser().parse_args()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = args.run_prefix or f"micro_sweep_{args.benchmark}_{stamp}"

    rows: list[dict[str, Any]] = []
    for route_mode in args.route_modes:
        for passes in args.passes:
            run_id = f"{prefix}_{route_mode}_n{passes}"
            report = _run_condition(args, route_mode=route_mode, passes=passes, run_id=run_id)
            rows.append(report)

    output_dir = Path(args.output_dir).expanduser().resolve()
    json_path, md_path = _write_sweep_report(output_dir, prefix, rows)
    print(
        json.dumps(
            {
                "sweep_id": prefix,
                "conditions": len(rows),
                "report_json": str(json_path),
                "report_md": str(md_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
