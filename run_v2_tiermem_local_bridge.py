#!/usr/bin/env python3
"""
Bridge local benchmark mirrors to the real TierMem upstream stack.

This script is intentionally V2-first:
- uses the cloned TierMem upstream implementation
- points TierMem dataset loaders at local benchmark mirrors in this repo
- prefers local-path Qdrant mode so a Mac can run a minimal sanity baseline
- performs readiness checks before attempting a real run
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Dict, Iterable, List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
TIERMEM_ROOT = WORKSPACE_ROOT / "tiermem_upstream"
LOCAL_MEM0_DIR = PROJECT_ROOT / "outputs" / "tiermem_local_mem0"


@dataclass(frozen=True)
class BenchmarkSpec:
    cli_name: str
    upstream_module: str
    upstream_benchmark_name: str
    default_data_path: Path
    split: str
    notes: str


BENCHMARK_SPECS: Dict[str, BenchmarkSpec] = {
    "locomo": BenchmarkSpec(
        cli_name="locomo",
        upstream_module="core.datasets.locomo",
        upstream_benchmark_name="locomo",
        default_data_path=PROJECT_ROOT / "benchmarks" / "locomo" / "locomo_official" / "data" / "locomo10.json",
        split="test",
        notes="Local LoCoMo mirror is already present and matches TierMem's expected structure after path override.",
    ),
    "longmemeval": BenchmarkSpec(
        cli_name="longmemeval",
        upstream_module="core.datasets.longmemeval",
        upstream_benchmark_name="longmemeval_chunk_500",
        default_data_path=PROJECT_ROOT
        / "benchmarks"
        / "locomo"
        / "longmemeval_official"
        / "data"
        / "cleaned"
        / "longmemeval_s_cleaned.json",
        split="test",
        notes="Local LongMemEval-S cleaned mirror is already present and large enough for a real small-scale sanity pass.",
    ),
    "halumem": BenchmarkSpec(
        cli_name="halumem",
        upstream_module="core.datasets.halumem",
        upstream_benchmark_name="halumem",
        default_data_path=PROJECT_ROOT
        / "benchmarks"
        / "halumem"
        / "official_repo"
        / "data"
        / "HaluMem-Medium.jsonl",
        split="Medium",
        notes="TierMem's HaluMem loader is wired to the canonical local HaluMem-Medium.jsonl path.",
    ),
}


REQUIRED_MODULES: Tuple[str, ...] = (
    "openai",
    "qdrant_client",
    "json_repair",
    "tqdm",
    "pydantic",
    "requests",
    "sqlalchemy",
    "tenacity",
    "tiktoken",
)

OPTIONAL_MODULES: Tuple[str, ...] = (
    "sentence_transformers",
    "fastembed",
    "tantivy",
)


def _module_status(module_names: Iterable[str]) -> List[Tuple[str, bool, str]]:
    rows: List[Tuple[str, bool, str]] = []
    for name in module_names:
        try:
            mod = importlib.import_module(name)
            mod_path = getattr(mod, "__file__", "built-in")
            rows.append((name, True, str(mod_path)))
        except Exception as exc:  # pragma: no cover - diagnostic path
            rows.append((name, False, f"{type(exc).__name__}: {exc}"))
    return rows


def _format_module_rows(rows: List[Tuple[str, bool, str]]) -> List[str]:
    return [
        f"  - {name}: {'OK' if ok else 'MISSING'} ({detail})"
        for name, ok, detail in rows
    ]


def _env_status() -> Dict[str, bool]:
    return {
        "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
        "OPENAI_BASE_URL": bool(os.getenv("OPENAI_BASE_URL")),
        "OPENAI_MODEL": bool(os.getenv("OPENAI_MODEL")),
        "QDRANT_HOST": bool(os.getenv("QDRANT_HOST")),
        "QDRANT_PORT": bool(os.getenv("QDRANT_PORT")),
    }


def _spec_for(name: str) -> BenchmarkSpec:
    try:
        return BENCHMARK_SPECS[name]
    except KeyError as exc:
        raise SystemExit(f"Unknown benchmark: {name}") from exc


def _resolve_data_path(args: argparse.Namespace, spec: BenchmarkSpec) -> Path:
    if args.data_path:
        return Path(args.data_path).expanduser().resolve()
    return spec.default_data_path.resolve()


def _take_first_session(dataset_module: ModuleType, spec: BenchmarkSpec) -> tuple[bool, str]:
    sessions = dataset_module.iter_sessions(split=spec.split, limit=1)
    first = next(iter(sessions), None)
    if first is None:
        return False, "no sessions returned"
    if isinstance(first, dict):
        session_keys = sorted(first.keys())
        session_id = str(first.get("session_id") or first.get("id") or "unknown")
        return True, f"session_id={session_id}; keys={session_keys}"
    return True, f"sample_type={type(first).__name__}"


def _dataset_loader_preflight(spec: BenchmarkSpec, data_path: Path) -> tuple[bool, str]:
    try:
        dataset_module = _import_dataset_module(spec)
        _patch_dataset_module(dataset_module, data_path)
        return _take_first_session(dataset_module, spec)
    except Exception as exc:  # pragma: no cover - diagnostic path
        return False, f"{type(exc).__name__}: {exc}"


def _print_readiness(args: argparse.Namespace) -> int:
    print("=" * 72)
    print("TierMem V2 Local Bridge Readiness")
    print("=" * 72)
    print(f"Interpreter: {sys.executable}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"TierMem upstream: {TIERMEM_ROOT}")
    print(f"TierMem upstream exists: {TIERMEM_ROOT.exists()}")
    print()

    env_rows = _env_status()
    print("Environment variables")
    for key, present in env_rows.items():
        print(f"  - {key}: {'SET' if present else 'MISSING'}")
    print()

    required_rows = _module_status(REQUIRED_MODULES)
    optional_rows = _module_status(OPTIONAL_MODULES)

    print("Required Python modules")
    for line in _format_module_rows(required_rows):
        print(line)
    print()

    print("Optional Python modules")
    for line in _format_module_rows(optional_rows):
        print(line)
    print()

    targets = [args.benchmark] if args.benchmark else list(BENCHMARK_SPECS.keys())
    print("Benchmark data")
    for name in targets:
        spec = _spec_for(name)
        data_path = _resolve_data_path(args, spec) if args.benchmark == name else spec.default_data_path.resolve()
        exists = data_path.exists()
        size = data_path.stat().st_size if exists and data_path.is_file() else 0
        print(f"  - {name}: {'READY' if exists else 'MISSING'}")
        print(f"    path: {data_path}")
        if exists:
            print(f"    size_bytes: {size}")
            required_missing = [module for module, ok, _detail in required_rows if not ok]
            if TIERMEM_ROOT.exists() and not required_missing:
                ok, detail = _dataset_loader_preflight(spec, data_path)
                print(f"    dataset_loader_preflight: {'OK' if ok else 'FAIL'} ({detail})")
        print(f"    note: {spec.notes}")
    print()

    required_missing = [name for name, ok, _detail in required_rows if not ok]
    target_name = args.benchmark or "locomo"
    target_spec = _spec_for(target_name)
    target_data_path = _resolve_data_path(args, target_spec)
    target_data_ready = target_data_path.exists()
    openai_ready = env_rows["OPENAI_API_KEY"]

    if required_missing or not openai_ready or not target_data_ready or not TIERMEM_ROOT.exists():
        print("Readiness verdict: NOT RUNNABLE YET")
        if required_missing:
            print(f"  missing required modules: {', '.join(required_missing)}")
        if not openai_ready:
            print("  missing required env var: OPENAI_API_KEY")
        if not target_data_ready:
            print(f"  missing benchmark data for {target_name}: {target_data_path}")
        if not TIERMEM_ROOT.exists():
            print(f"  missing TierMem clone: {TIERMEM_ROOT}")
        return 1

    print("Readiness verdict: READY FOR A MINIMAL LOCAL SANITY RUN")
    return 0


def _ensure_tiermem_import_path() -> None:
    if not TIERMEM_ROOT.exists():
        raise FileNotFoundError(f"TierMem upstream repo not found: {TIERMEM_ROOT}")
    LOCAL_MEM0_DIR.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MEM0_DIR", str(LOCAL_MEM0_DIR))
    os.environ.setdefault("MEM0_TELEMETRY", "False")
    tiermem_root_str = str(TIERMEM_ROOT)
    if tiermem_root_str not in sys.path:
        sys.path.insert(0, tiermem_root_str)


def _import_dataset_module(spec: BenchmarkSpec) -> ModuleType:
    _ensure_tiermem_import_path()
    return importlib.import_module(spec.upstream_module)


def _patch_dataset_module(dataset_module: ModuleType, data_path: Path) -> None:
    if dataset_module.__name__.endswith("longmemeval") and hasattr(dataset_module, "TIKTOKEN_AVAILABLE"):
        # The upstream LongMemEval loader tries to fetch tokenizer files on first use.
        # For a local bridge sanity pass we prefer the built-in char-count fallback.
        dataset_module.TIKTOKEN_AVAILABLE = False  # type: ignore[attr-defined]

    original_iter_sessions = dataset_module.iter_sessions

    def patched_iter_sessions(split: str = "test", limit: Optional[int] = None):
        return original_iter_sessions(data_path=str(data_path), split=split, limit=limit)

    dataset_module.iter_sessions = patched_iter_sessions  # type: ignore[attr-defined]


def _router_config(args: argparse.Namespace) -> Dict[str, object]:
    router_type = args.router_type
    cfg: Dict[str, object] = {"type": router_type}
    if router_type == "openai":
        cfg["model"] = args.router_model or args.model
        if args.router_api_key:
            cfg["api_key"] = args.router_api_key
        if args.router_base_url:
            cfg["base_url"] = args.router_base_url
    elif router_type == "vllm":
        cfg["model"] = args.router_model or "Qwen3-0.6B"
        cfg["base_url"] = args.router_base_url or "http://localhost:8000/v1"
        cfg["api_key"] = args.router_api_key or "vllm-api-key"
        cfg["is_thinking_model"] = True
    return cfg


def _build_lv_cfg(
    args: argparse.Namespace,
    spec: BenchmarkSpec,
    collection_name: str,
    qdrant_path: Path,
) -> Dict[str, object]:
    return {
        "benchmark_name": spec.upstream_benchmark_name,
        "write_facts_to_database": True,
        "mem0_config": {
            "backend": "mem0",
            "llm": {
                "provider": "openai",
                "config": {
                    "model": args.model,
                },
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "path": str(qdrant_path),
                    "collection_name": collection_name,
                    "on_disk": True,
                },
            },
        },
        "memory_system_model": args.model,
        "router_config": _router_config(args),
        "use_query_rewriter": False,
        "use_dual_retrieval": False,
        "rewriter_guide_update_freq": 10,
        "router_threshold": args.router_threshold,
        "top_k": args.top_k,
        "max_research_iters": args.max_research_iters,
        "page_size": args.page_size,
        "use_reranker": False,
    }


def _pre_api_smoke(args: argparse.Namespace) -> int:
    spec = _spec_for(args.benchmark)
    data_path = _resolve_data_path(args, spec)

    if not data_path.exists():
        print(f"Missing benchmark data: {data_path}")
        return 1

    required_rows = _module_status(REQUIRED_MODULES)
    required_missing = [name for name, ok, _detail in required_rows if not ok]
    if required_missing:
        print("Cannot run pre-api smoke yet. Missing required modules:")
        for name in required_missing:
            print(f"  - {name}")
        return 1

    _ensure_tiermem_import_path()
    dataset_module = _import_dataset_module(spec)
    _patch_dataset_module(dataset_module, data_path)
    ok, detail = _take_first_session(dataset_module, spec)
    if not ok:
        print(f"Dataset loader preflight failed: {detail}")
        return 1

    placeholder_used = False
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "pre_api_smoke_placeholder"
        placeholder_used = True
    os.environ.setdefault("OPENAI_MODEL", args.model)

    from src.memory.linked_view_system import LinkedViewSystem

    run_id = args.run_id or f"v2_pre_api_{spec.cli_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    collection_name = f"tiermem_v2_pre_api_{spec.cli_name}_{run_id}".replace("-", "_")
    qdrant_path = Path(args.qdrant_path).expanduser().resolve()
    qdrant_path.mkdir(parents=True, exist_ok=True)

    lv_cfg = _build_lv_cfg(args, spec, collection_name, qdrant_path)
    try:
        system = LinkedViewSystem(lv_cfg)
        system.reset(f"pre_api_smoke_{spec.cli_name}")
    except Exception as exc:
        print("Pre-API smoke failed during system init/reset.")
        print(f"  error: {type(exc).__name__}: {exc}")
        return 1

    print("=" * 72)
    print("TierMem V2 pre-API smoke succeeded")
    print("=" * 72)
    print(f"benchmark: {spec.cli_name}")
    print(f"dataset_loader_preflight: {detail}")
    print(f"placeholder_openai_key_used: {placeholder_used}")
    print(f"qdrant_path: {qdrant_path}")
    print(f"collection_name: {collection_name}")
    return 0


def _run_bridge(args: argparse.Namespace) -> int:
    spec = _spec_for(args.benchmark)
    data_path = _resolve_data_path(args, spec)

    if not data_path.exists():
        print(f"Missing benchmark data: {data_path}")
        return 1

    required_rows = _module_status(REQUIRED_MODULES)
    required_missing = [name for name, ok, _detail in required_rows if not ok]
    if required_missing:
        print("Cannot run yet. Missing required modules:")
        for name in required_missing:
            print(f"  - {name}")
        return 1

    if not os.getenv("OPENAI_API_KEY"):
        print("Cannot run yet. OPENAI_API_KEY is missing.")
        return 1

    _ensure_tiermem_import_path()

    from core.runner.run_benchmark_multi import run_benchmark_multi
    from src.memory.linked_view_system import LinkedViewSystem

    dataset_module = _import_dataset_module(spec)
    _patch_dataset_module(dataset_module, data_path)

    run_id = args.run_id or f"v2_{spec.cli_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    collection_name = f"tiermem_v2_{spec.cli_name}_{run_id}".replace("-", "_")
    qdrant_path = Path(args.qdrant_path).expanduser().resolve()
    qdrant_path.mkdir(parents=True, exist_ok=True)

    lv_cfg = _build_lv_cfg(args, spec, collection_name, qdrant_path)
    system = LinkedViewSystem(lv_cfg)

    summary = run_benchmark_multi(
        system=system,
        dataset_module=dataset_module,
        benchmark_name=spec.upstream_benchmark_name,
        run_id=run_id,
        config={
            "model_name": args.model,
            "split": spec.split,
        },
        output_dir=str(Path(args.output_dir).expanduser().resolve()),
        limit=args.limit,
        max_workers=args.max_workers,
        executor_type="thread",
        system_config=lv_cfg,
        qa_max_workers=args.qa_max_workers,
        write_max_workers=args.write_max_workers,
        load_only=False,
    )

    print("=" * 72)
    print("TierMem V2 local bridge run complete")
    print("=" * 72)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run readiness checks or launch a V2-first TierMem local sanity run."
    )
    parser.add_argument(
        "--benchmark",
        choices=sorted(BENCHMARK_SPECS.keys()),
        default="locomo",
        help="Benchmark target for readiness/run mode.",
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default=None,
        help="Optional explicit benchmark data path override.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only print readiness diagnostics without attempting a run.",
    )
    parser.add_argument(
        "--pre-api-smoke",
        action="store_true",
        help="Run dataset-loader plus LinkedViewSystem init/reset without a real benchmark pass.",
    )
    parser.add_argument("--limit", type=int, default=2, help="Session limit for a sanity run.")
    parser.add_argument("--model", type=str, default="gpt-4.1-mini", help="TierMem model name.")
    parser.add_argument("--run-id", type=str, default=None, help="Optional run id override.")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "outputs" / "v2_tiermem"),
        help="Output directory for bridge runs.",
    )
    parser.add_argument(
        "--qdrant-path",
        type=str,
        default=str(PROJECT_ROOT / "outputs" / "tiermem_local_qdrant"),
        help="Local-path Qdrant store used for the minimal Mac baseline.",
    )
    parser.add_argument("--max-workers", type=int, default=1, help="Session-level concurrency.")
    parser.add_argument("--write-max-workers", type=int, default=1, help="Per-session write concurrency.")
    parser.add_argument("--qa-max-workers", type=int, default=1, help="Per-session QA concurrency.")
    parser.add_argument("--top-k", type=int, default=5, help="TierMem retrieval top-k.")
    parser.add_argument("--max-research-iters", type=int, default=3, help="TierMem max research iterations.")
    parser.add_argument("--page-size", type=int, default=100, help="TierMem page size.")
    parser.add_argument("--router-threshold", type=float, default=0.5, help="Router threshold.")
    parser.add_argument(
        "--router-type",
        choices=["openai", "vllm", "llm"],
        default="openai",
        help="Router backend for the real TierMem stack.",
    )
    parser.add_argument("--router-model", type=str, default=None, help="Optional router model override.")
    parser.add_argument("--router-base-url", type=str, default=None, help="Optional router base URL.")
    parser.add_argument("--router-api-key", type=str, default=None, help="Optional router API key.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.check_only:
        return _print_readiness(args)
    if args.pre_api_smoke:
        return _pre_api_smoke(args)
    return _run_bridge(args)


if __name__ == "__main__":
    raise SystemExit(main())
