#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
TIERMEM_ROOT = WORKSPACE_ROOT / "tiermem_upstream"
LOCAL_MEM0_DIR = PROJECT_ROOT / "outputs" / "tiermem_local_mem0_micro"
DEFAULT_PAGE_SIZE = 4000


def _ensure_imports() -> None:
    LOCAL_MEM0_DIR.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MEM0_DIR", str(LOCAL_MEM0_DIR))
    os.environ.setdefault("MEM0_TELEMETRY", "False")
    project_root_str = str(PROJECT_ROOT)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    tiermem_root_str = str(TIERMEM_ROOT)
    if tiermem_root_str not in sys.path:
        sys.path.insert(0, tiermem_root_str)


_ensure_imports()

from run_v2_tiermem_local_bridge import (  # noqa: E402
    _build_lv_cfg,
    _import_dataset_module,
    _patch_dataset_module,
    _spec_for,
)
from week1_surface import add_week1_architecture_arg, resolve_week1_runtime


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a tiny live TierMem micro-slice with a limited number of sessions and QA pairs."
    )
    add_week1_architecture_arg(parser)
    parser.add_argument("--benchmark", choices=["locomo", "longmemeval", "halumem", "tiny_synth"], default="locomo")
    parser.add_argument("--session-limit", type=int, default=1)
    parser.add_argument("--qa-limit", type=int, default=5)
    parser.add_argument("--model", type=str, default="gpt-4.1-mini")
    parser.add_argument("--run-id", type=str, default=None)
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
    parser.add_argument("--route-mode", choices=["auto", "summary_only", "research_only"], default="auto")
    parser.add_argument("--consolidation-passes", type=int, default=0)
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
    # Seeded evaluation-set subsampling. The reader runs at temperature=0.0
    # (deterministic decoding), so the meaningful per-seed variance source is
    # *which* sessions / QA are drawn, not LLM sampling noise. When --seed is set
    # together with --sample-qa / --session-pool, the slice is a reproducible
    # random subset instead of the default head-truncation, giving genuine
    # between-seed variability for multi-seed statistics. Defaults preserve the
    # original deterministic behaviour exactly.
    parser.add_argument("--seed", type=int, default=None,
                        help="RNG seed for evaluation-set subsampling (None = deterministic head slice).")
    parser.add_argument("--sample-qa", action="store_true",
                        help="Randomly sample qa_limit QA per session under --seed instead of head-truncating.")
    parser.add_argument("--session-pool", type=int, default=0,
                        help="If > session_limit and --seed set, draw session_limit sessions from this larger pool.")
    return parser


def _slice_sessions(
    dataset_module: ModuleType,
    split: str,
    session_limit: int,
    qa_limit: int,
    seed: int | None = None,
    sample_qa: bool = False,
    session_pool: int = 0,
) -> list[dict[str, Any]]:
    import random

    rng = random.Random(seed) if seed is not None else None
    # When resampling sessions we need a pool larger than session_limit to draw
    # from; otherwise iterate exactly session_limit (original behaviour).
    resample_sessions = rng is not None and session_pool and session_pool > session_limit
    iter_limit = session_pool if resample_sessions else session_limit

    pool: list[dict[str, Any]] = list(dataset_module.iter_sessions(split=split, limit=iter_limit))
    if resample_sessions:
        chosen = rng.sample(pool, min(session_limit, len(pool)))
    else:
        chosen = pool[:session_limit]

    sessions: list[dict[str, Any]] = []
    for idx, session in enumerate(chosen, start=1):
        copied = dict(session)
        qa_pairs = list(copied.get("qa_pairs", []))
        if rng is not None and sample_qa and len(qa_pairs) > qa_limit:
            selected_qa = rng.sample(qa_pairs, qa_limit)
        else:
            selected_qa = qa_pairs[:qa_limit]
        copied["qa_pairs"] = selected_qa
        copied["micro_slice_meta"] = {
            "session_rank": idx,
            "qa_limit": qa_limit,
            "original_qa_count": len(qa_pairs),
            "sliced_qa_count": len(copied["qa_pairs"]),
            "seed": seed,
            "sample_qa": bool(rng is not None and sample_qa),
            "resampled_sessions": resample_sessions,
        }
        sessions.append(copied)
    return sessions


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _iter_session_qa_logs(run_root: Path) -> Iterable[Path]:
    sessions_dir = run_root / "sessions"
    if not sessions_dir.exists():
        return []
    return sorted(sessions_dir.glob("*_qa.jsonl"))


def _iter_session_write_logs(run_root: Path) -> Iterable[Path]:
    sessions_dir = run_root / "sessions"
    if not sessions_dir.exists():
        return []
    return sorted(sessions_dir.glob("*_write.jsonl"))


def _build_micro_report(
    run_root: Path,
    benchmark: str,
    run_id: str,
    qa_limit: int,
    architecture: str | None,
    route_mode: str,
    consolidation_passes: int,
    consolidation_scope: str,
    consolidation_target_max_pages: int,
    page_write_mode: str,
    abstain_on_unsupported: bool,
    seed: int | None = None,
    sample_qa: bool = False,
) -> dict[str, Any]:
    qa_rows: list[dict[str, Any]] = []
    for qa_path in _iter_session_qa_logs(run_root):
        qa_rows.extend(_read_jsonl(qa_path))
    write_rows: list[dict[str, Any]] = []
    for write_path in _iter_session_write_logs(run_root):
        write_rows.extend(_read_jsonl(write_path))
    summary_path = run_root / "summary.json"
    summary_payload = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}

    answered = len(qa_rows)
    total_score = sum(float(row.get("score", 0.0) or 0.0) for row in qa_rows)
    route_counts = Counter(
        ((row.get("mechanism_trace") or {}).get("route") or "UNKNOWN")
        for row in qa_rows
    )
    avg_total_latency_ms = (
        sum(float((row.get("cost_metrics") or {}).get("online_total_latency_ms", 0.0) or 0.0) for row in qa_rows) / answered
        if answered
        else 0.0
    )
    avg_tokens_in = (
        sum(float((row.get("cost_metrics") or {}).get("online_tokens_in", 0.0) or 0.0) for row in qa_rows) / answered
        if answered
        else 0.0
    )
    avg_tokens_out = (
        sum(float((row.get("cost_metrics") or {}).get("online_tokens_out", 0.0) or 0.0) for row in qa_rows) / answered
        if answered
        else 0.0
    )
    sample_failures = [
        {
            "query_id": row.get("query_id"),
            "question": row.get("question"),
            "ground_truth": row.get("ground_truth"),
            "model_response": row.get("model_response"),
            "route": (row.get("mechanism_trace") or {}).get("route"),
        }
        for row in qa_rows
        if float(row.get("score", 0.0) or 0.0) == 0.0
    ][:3]
    selected_page_ids = {
        str((row.get("storage_stats") or {}).get("page_id") or "")
        for row in write_rows
        if (row.get("storage_stats") or {}).get("stage") == "consolidation_pass"
        and str((row.get("storage_stats") or {}).get("page_id") or "")
    }
    qa_page_ids = {
        str(hit.get("page_id") or "")
        for row in qa_rows
        for hit in ((row.get("mechanism_trace") or {}).get("hits_summary") or [])
        if str(hit.get("page_id") or "")
    }
    overlap_page_ids = selected_page_ids & qa_page_ids
    selection_row = next(
        (
            row
            for row in write_rows
            if (row.get("storage_stats") or {}).get("stage") == "consolidation_target_selection"
        ),
        None,
    )
    selection_stats = dict((selection_row or {}).get("storage_stats") or {})
    selection_cost = dict((selection_row or {}).get("cost_metrics") or {})
    overlap_metrics = {
        "selected_unique_pages": len(selected_page_ids),
        "qa_unique_pages": len(qa_page_ids),
        "overlap_unique_pages": len(overlap_page_ids),
        "overlap_ratio_on_qa_pages": (len(overlap_page_ids) / len(qa_page_ids)) if qa_page_ids else 0.0,
        "overlap_ratio_on_selected_pages": (len(overlap_page_ids) / len(selected_page_ids)) if selected_page_ids else 0.0,
        "qa_only_pages": max(0, len(qa_page_ids - selected_page_ids)),
        "selected_only_pages": max(0, len(selected_page_ids - qa_page_ids)),
    }

    return {
        "benchmark": benchmark,
        "run_id": run_id,
        "qa_limit": qa_limit,
        "architecture": architecture or "manual_runtime",
        "route_mode": route_mode,
        "consolidation_passes": consolidation_passes,
        "consolidation_scope": consolidation_scope,
        "consolidation_target_max_pages": consolidation_target_max_pages,
        "page_write_mode": page_write_mode,
        "abstain_on_unsupported": abstain_on_unsupported,
        "seed": seed,
        "sample_qa": sample_qa,
        "answered": answered,
        "mean_exact_match": (total_score / answered) if answered else 0.0,
        "route_counts": dict(route_counts),
        "avg_online_total_latency_ms": avg_total_latency_ms,
        "avg_online_tokens_in": avg_tokens_in,
        "avg_online_tokens_out": avg_tokens_out,
        "summary_metrics": summary_payload.get("metrics", {}),
        "summary_f1": float((summary_payload.get("metrics", {}) or {}).get("f1", 0.0) or 0.0),
        "summary_bleu1": float((summary_payload.get("metrics", {}) or {}).get("bleu1", 0.0) or 0.0),
        "cost_summary": summary_payload.get("cost_summary", {}),
        "consolidation_selection": selection_stats,
        "consolidation_selection_cost": selection_cost,
        "consolidation_overlap": overlap_metrics,
        "sample_failures": sample_failures,
        "run_root": str(run_root),
    }


def _write_report(report_dir: Path, report: dict[str, Any]) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / f"{report['run_id']}.json"
    md_path = report_dir / f"{report['run_id']}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# TierMem Micro Slice Report: {report['run_id']}",
        "",
        f"- benchmark: `{report['benchmark']}`",
        f"- architecture: `{report['architecture']}`",
        f"- route_mode: `{report['route_mode']}`",
        f"- consolidation_passes: `{report['consolidation_passes']}`",
        f"- consolidation_scope: `{report['consolidation_scope']}`",
        f"- consolidation_target_max_pages: `{report['consolidation_target_max_pages']}`",
        f"- page_write_mode: `{report['page_write_mode']}`",
        f"- abstain_on_unsupported: `{report['abstain_on_unsupported']}`",
        f"- answered: `{report['answered']}`",
        f"- summary_f1: `{report['summary_f1']:.3f}`",
        f"- summary_bleu1: `{report['summary_bleu1']:.3f}`",
        f"- mean_exact_match_reference: `{report['mean_exact_match']:.3f}`",
        f"- route_counts: `{report['route_counts']}`",
        f"- avg_online_total_latency_ms: `{report['avg_online_total_latency_ms']:.1f}`",
        f"- avg_online_tokens_in: `{report['avg_online_tokens_in']:.1f}`",
        f"- avg_online_tokens_out: `{report['avg_online_tokens_out']:.1f}`",
        f"- consolidation_selection: `{report.get('consolidation_selection', {})}`",
        f"- consolidation_overlap: `{report.get('consolidation_overlap', {})}`",
        f"- summary_metrics: `{report['summary_metrics']}`",
        f"- overall_cost: `{(report.get('cost_summary') or {}).get('overall', {})}`",
        f"- memory_write_cost: `{(report.get('cost_summary') or {}).get('memory_write', {})}`",
        f"- run_root: `{report['run_root']}`",
        "",
        "## Sample Failures",
        "",
    ]
    failures = report.get("sample_failures") or []
    if not failures:
        lines.append("- none")
    else:
        for failure in failures:
            lines.append(
                f"- `{failure['query_id']}` | q=`{failure['question']}` | gold=`{failure['ground_truth']}` | "
                f"route=`{failure['route']}` | response=`{(failure['model_response'] or '')[:180]}`"
            )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    args = _build_parser().parse_args()
    runtime = resolve_week1_runtime(args)
    spec = _spec_for(args.benchmark)
    dataset_module = _import_dataset_module(spec)
    _patch_dataset_module(dataset_module, spec.default_data_path)

    sessions = _slice_sessions(
        dataset_module=dataset_module,
        split=spec.split,
        session_limit=args.session_limit,
        qa_limit=args.qa_limit,
        seed=args.seed,
        sample_qa=args.sample_qa,
        session_pool=args.session_pool,
    )
    if not sessions:
        raise RuntimeError(f"No sessions loaded for benchmark={args.benchmark}.")

    class MicroDatasetModule:
        @staticmethod
        def iter_sessions(split: str = spec.split, limit: int | None = None):
            del split, limit
            yield from sessions

    run_id = args.run_id or (
        f"micro_{args.benchmark}_s{args.session_limit}_q{args.qa_limit}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    qdrant_path = Path(args.qdrant_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    collection_name = f"tiermem_micro_{args.benchmark}_{run_id}".replace("-", "_")

    lv_cfg = _build_lv_cfg(args, spec, collection_name, qdrant_path)
    lv_cfg["page_store_dir"] = str(output_dir / "page_store" / run_id)

    from src.memory.linked_view_system import LinkedViewSystem
    from core.runner.run_benchmark_multi import run_benchmark_multi

    system = LinkedViewSystem(lv_cfg)
    summary = run_benchmark_multi(
        system=system,
        dataset_module=MicroDatasetModule,
        benchmark_name=spec.upstream_benchmark_name,
        run_id=run_id,
        config={
            "model_name": args.model,
            "split": spec.split,
            "architecture": runtime["architecture"] or "manual_runtime",
            "engine_route_mode": runtime["route_mode"],
            "page_write_mode": runtime["page_write_mode"],
            "max_research_iters": runtime["max_research_iters"],
            "consolidation_passes": args.consolidation_passes,
        },
        output_dir=str(output_dir),
        limit=len(sessions),
        max_workers=args.max_workers,
        executor_type="thread",
        system_config=lv_cfg,
        qa_max_workers=args.qa_max_workers,
        write_max_workers=args.write_max_workers,
        load_only=False,
    )

    run_root = output_dir / args.benchmark / system.get_system_name() / run_id
    report = _build_micro_report(
        run_root=run_root,
        benchmark=args.benchmark,
        run_id=run_id,
        qa_limit=args.qa_limit,
        architecture=runtime["architecture"],
        route_mode=runtime["route_mode"],
        consolidation_passes=args.consolidation_passes,
        consolidation_scope=args.consolidation_scope,
        consolidation_target_max_pages=args.consolidation_target_max_pages,
        page_write_mode=runtime["page_write_mode"],
        abstain_on_unsupported=args.abstain_on_unsupported,
        seed=args.seed,
        sample_qa=args.sample_qa,
    )
    json_path, md_path = _write_report(output_dir / "micro_reports", report)

    payload = {
        "summary": summary,
        "micro_report": report,
        "report_json": str(json_path),
        "report_md": str(md_path),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
