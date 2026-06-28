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


def run_script(base_dir: Path, script_name: str) -> None:
    subprocess.run([sys.executable, str(base_dir / script_name)], check=True)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    required_inputs = {
        "benchmark adapter layer": base_dir / ADAPTER_RESULTS,
        "minimal benchmark panel": base_dir / MINIMAL_RESULTS,
        "broader benchmark reviewer section": base_dir / BENCHMARK_SECTION_RESULTS,
    }
    missing = [label for label, path in required_inputs.items() if not path.exists()]
    if missing:
        raise RuntimeError(
            "Missing upstream benchmark artifacts: "
            + ", ".join(missing)
            + ". Refresh the external benchmark stack first."
        )

    run_script(base_dir, NATIVE_PRIMARY_BASE_SCRIPT)
    run_script(base_dir, PRIMARY_SURFACE_SCRIPT)
    run_script(base_dir, PROXY_BASE_SCRIPT)
    run_script(base_dir, PAPER_PACKET_SCRIPT)
    run_script(base_dir, VERIFY_NATIVE_PRIMARY_BASE_SCRIPT)
    run_script(base_dir, VERIFY_REVIEWER_SECTION_SCRIPT)
    run_script(base_dir, VERIFY_PRIMARY_SURFACE_SCRIPT)
    run_script(base_dir, VERIFY_PROXY_BASE_SCRIPT)
    run_script(base_dir, VERIFY_PAPER_PACKET_SCRIPT)
    print(
        "Benchmark-first entrypoint refreshed the proxy-base chain from "
        f"{required_inputs['broader benchmark reviewer section']}"
    )


if __name__ == "__main__":
    main()
