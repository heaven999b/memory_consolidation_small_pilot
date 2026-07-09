from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ADAPTER_RESULTS = "outputs/external_benchmark_adapter_layer.json"
MINIMAL_RESULTS = "outputs/external_benchmark_minimal_baseline.json"
BENCHMARK_SECTION_RESULTS = "outputs/external_benchmark_reviewer_section.json"
NATIVE_PRIMARY_BASE_SCRIPT = "run_benchmark_native_primary_base.py"
PRIMARY_SURFACE_SCRIPT = "run_tiermem_style_primary_surface.py"
PROXY_BASE_SCRIPT = "run_benchmark_first_proxy_base.py"
PAPER_PACKET_SCRIPT = "run_paper_baseline_packet.py"
VERIFY_NATIVE_PRIMARY_BASE_SCRIPT = "verify_benchmark_native_primary_base.py"
VERIFY_REVIEWER_SECTION_SCRIPT = "verify_external_benchmark_reviewer_section.py"
VERIFY_PRIMARY_SURFACE_SCRIPT = "verify_tiermem_style_primary_surface.py"
VERIFY_PROXY_BASE_SCRIPT = "verify_benchmark_first_proxy_base.py"
VERIFY_PAPER_PACKET_SCRIPT = "verify_paper_baseline_packet.py"

LEGACY_SUBDIRS = [
    "benchmark",
    "support",
    "verify",
]


def resolve_script(repo_root: Path, legacy_dir: Path, script_name: str) -> Path:
    legacy_path = legacy_dir / script_name
    if legacy_path.exists():
        return legacy_path
    for subdir in LEGACY_SUBDIRS:
        nested_path = legacy_dir / subdir / script_name
        if nested_path.exists():
            return nested_path
    return repo_root / script_name


def run_script(repo_root: Path, legacy_dir: Path, script_name: str) -> None:
    subprocess.run([sys.executable, str(resolve_script(repo_root, legacy_dir, script_name))], cwd=str(repo_root), check=True)


def main() -> None:
    legacy_dir = Path(__file__).resolve().parent
    repo_root = legacy_dir.parents[1]
    required_inputs = {
        "benchmark adapter layer": repo_root / ADAPTER_RESULTS,
        "minimal benchmark panel": repo_root / MINIMAL_RESULTS,
        "broader benchmark reviewer section": repo_root / BENCHMARK_SECTION_RESULTS,
    }
    missing = [label for label, path in required_inputs.items() if not path.exists()]
    if missing:
        raise RuntimeError(
            "Missing upstream benchmark artifacts: "
            + ", ".join(missing)
            + ". Refresh the external benchmark stack first."
        )

    run_script(repo_root, legacy_dir, NATIVE_PRIMARY_BASE_SCRIPT)
    run_script(repo_root, legacy_dir, PRIMARY_SURFACE_SCRIPT)
    run_script(repo_root, legacy_dir, PROXY_BASE_SCRIPT)
    run_script(repo_root, legacy_dir, PAPER_PACKET_SCRIPT)
    run_script(repo_root, legacy_dir, VERIFY_NATIVE_PRIMARY_BASE_SCRIPT)
    run_script(repo_root, legacy_dir, VERIFY_REVIEWER_SECTION_SCRIPT)
    run_script(repo_root, legacy_dir, VERIFY_PRIMARY_SURFACE_SCRIPT)
    run_script(repo_root, legacy_dir, VERIFY_PROXY_BASE_SCRIPT)
    run_script(repo_root, legacy_dir, VERIFY_PAPER_PACKET_SCRIPT)
    print(
        "Benchmark-first entrypoint refreshed the proxy-base chain from "
        f"{required_inputs['broader benchmark reviewer section']}"
    )


if __name__ == "__main__":
    main()
