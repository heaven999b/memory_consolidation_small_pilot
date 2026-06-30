from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


RUN_STEPS = [
    ("freeze_task_extension_slices.py", {}),
    ("run_actual_summarizer_slice.py", {}),
    ("run_actual_recall_expansion.py", {"ACTUAL_RECALL_EXPANSION_SEEDS": "11,23"}),
    ("run_actual_hallucination_stress_slice.py", {"ACTUAL_HALLU_STRESS_SEEDS": "11,23"}),
    ("run_actual_hallucination_claim_reintegration_pilot.py", {}),
    ("run_actual_note_persistence_round.py", {}),
    ("run_actual_scaffold_refinement_round.py", {}),
    ("run_actual_placeholder_hardening_round.py", {}),
    ("run_actual_carry_forward_round.py", {"ACTUAL_CARRY_FORWARD_SEEDS": "11,23", "ACTUAL_CARRY_FORWARD_ARCHITECTURES": "scale_aware_note_aware"}),
    ("run_psu_recall_main_panel.py", {}),
    ("run_provenance_scaffolded_method_report.py", {}),
    ("run_paper_strengthening_stats.py", {}),
    ("run_artifact_contract_audit.py", {}),
    ("run_psu_paper_packet.py", {}),
    ("run_external_benchmark_adapter_layer.py", {}),
    ("run_external_benchmark_minimal_baseline.py", {}),
    ("run_external_benchmark_reviewer_section.py", {}),
    ("run_task_extension_section.py", {}),
    ("run_benchmark_native_primary_base.py", {}),
    ("run_tiermem_style_primary_surface.py", {}),
    ("run_benchmark_first_proxy_base.py", {}),
    ("run_paper_baseline_packet.py", {}),
]

VERIFY_STEPS = [
    "verify_task_extension_section.py",
    "verify_benchmark_native_primary_base.py",
    "verify_paper_baseline_packet.py",
    "verify_paper_strengthening_artifacts.py",
]


def run_step(base_dir: Path, step: str, extra_env: dict[str, str] | None = None) -> None:
    path = base_dir / step
    print(f"[release-rebuild] running {step}")
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    subprocess.run([sys.executable, str(path)], cwd=str(base_dir), check=True, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild the reviewer-facing release packet in dependency order.")
    parser.add_argument("--skip-verify", action="store_true", help="Skip the verification scripts after rebuilding outputs.")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    for step, extra_env in RUN_STEPS:
        run_step(base_dir, step, extra_env)
    if not args.skip_verify:
        for step in VERIFY_STEPS:
            run_step(base_dir, step)


if __name__ == "__main__":
    main()
