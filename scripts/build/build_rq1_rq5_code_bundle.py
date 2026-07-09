#!/usr/bin/env python3
"""Build a compact handoff bundle for the RQ1-RQ5 code surface."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = PROJECT_ROOT / "dist"
BUNDLE_PATTERNS = [
    "README.md",
    "docs/research_question_map.md",
    "docs/operator_branches.md",
    "run_rq1_*.py",
    "run_rq2_*.py",
    "run_rq3_*.py",
    "run_rq_know_vs_do.py",
    "run_e1_*.py",
    "run_v2_tiermem_local_bridge.py",
    "run_v2_tiermem_micro_failure_mode_judge.py",
    "run_v2_tiermem_micro_n_sweep.py",
    "run_v2_tiermem_micro_slice.py",
    "week1_surface.py",
    "rq1_retest.py",
    "rq1_retest_n20.py",
    "rq1_relabel.py",
    "rq2_fixed.py",
    "analyze_rq2_tiermem_completed_pass.py",
    "rescore_rq2_selfbuilt_reports.py",
    "build_rq2_*.py",
    "build_rq3_*.py",
    "safety_metrics.py",
    "safety_honest_metrics.py",
    "safety_write_filter.py",
    "fix_toolkit.py",
    "stats_guardrails.py",
    "artifact_contract.py",
    "benchmark_native_runtime.py",
    "curated_dataset.py",
    "pilot_core.py",
    "configs/schemas/week1/*.json",
    "configs/rq2_selfbuilt_suite_*.json",
    "configs/week1/*.json",
    "benchmarks/safety/*.json",
    "benchmarks/safety/*.py",
    "benchmarks/tiny_synth/data/*.json",
    "benchmarks/halumem/official_repo/eval/llms.py",
]


def _collect_files() -> list[Path]:
    files: set[Path] = set()
    for pattern in BUNDLE_PATTERNS:
        for path in PROJECT_ROOT.glob(pattern):
            if path.is_file():
                files.add(path.resolve())
    return sorted(files)


def main() -> int:
    stamp = datetime.now().strftime("%Y%m%d")
    out_dir = DEFAULT_OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = out_dir / f"rq1_rq5_code_bundle_{stamp}.zip"
    manifest_path = out_dir / f"rq1_rq5_code_bundle_{stamp}_manifest.json"
    files = _collect_files()

    with ZipFile(bundle_path, "w", compression=ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, arcname=str(path.relative_to(PROJECT_ROOT)))

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(PROJECT_ROOT),
        "bundle_path": str(bundle_path),
        "n_files": len(files),
        "files": [str(path.relative_to(PROJECT_ROOT)) for path in files],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "bundle_zip": str(bundle_path),
        "manifest_json": str(manifest_path),
        "n_files": len(files),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
