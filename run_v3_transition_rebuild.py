from __future__ import annotations

import subprocess
import sys
from pathlib import Path


RUN_STEPS = [
    "run_v3_feasibility_gate.py",
    "run_v3_halumem_dataset_preflight.py",
    "run_v3_public_baseline_readiness.py",
    "run_v3_official_eval_runtime_audit.py",
    "run_v3_no_rewrite_policy_audit.py",
    "run_v3_no_rewrite_comparison.py",
    "run_v3_no_rewrite_statistics.py",
    "run_v3_no_rewrite_pareto.py",
    "run_v3_hygiene_audit.py",
    "run_v3_local_capability_matrix.py",
    "run_v3_local_evidence_packet.py",
    "run_v3_transition_status.py",
]


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    for step in RUN_STEPS:
        path = repo_root / step
        print(f"[v3-transition-rebuild] running {step}")
        subprocess.run([sys.executable, str(path)], cwd=str(repo_root), check=True)


if __name__ == "__main__":
    main()
