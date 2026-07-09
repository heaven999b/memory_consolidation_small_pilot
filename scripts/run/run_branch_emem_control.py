#!/usr/bin/env python3
"""Launch the E-mem-style anti-compression branch against an existing RQ harness.

This branch disables pre-answer consolidation, answers from the raw/research path,
and turns off summary write-back. It is an anti-compression control, not a literal
multi-agent reproduction of E-mem.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TASK_TO_SCRIPT = {
    "rq1_safety": PROJECT_ROOT / "run_rq1_safety_consolidation.py",
    "rq1_authority": PROJECT_ROOT / "run_rq1_authority_experiment.py",
    "rq1_agentpoison": PROJECT_ROOT / "run_rq1_agentpoison_overlay.py",
    "rq2_selfbuilt": PROJECT_ROOT / "run_rq2_factual_poison.py",
}

FORBIDDEN_FLAGS = {
    "--backend",
    "--passes",
    "--route-mode",
    "--page-write-mode",
    "--consolidation-prompt-style",
    "--write-facts-to-database",
    "--abstain-on-unsupported",
}


def _has_flag(forwarded: list[str], flag: str) -> bool:
    return any(tok == flag or tok.startswith(f"{flag}=") for tok in forwarded)


def _reject_overrides(forwarded: list[str]) -> None:
    bad = sorted(flag for flag in FORBIDDEN_FLAGS if _has_flag(forwarded, flag))
    if bad:
        raise SystemExit(
            "E-mem branch locks the following flags and they cannot be overridden here: "
            + ", ".join(bad)
        )


def _build_defaults(task: str) -> list[str]:
    output_dir = PROJECT_ROOT / "outputs" / "operator_branches" / "emem_style" / task
    defaults = [
        "--passes", "0",
        "--route-mode", "research_only",
        "--page-write-mode", "raw",
        "--write-facts-to-database", "off",
        "--abstain-on-unsupported",
        "--output-dir", str(output_dir),
    ]
    if task in {"rq1_safety", "rq1_authority", "rq2_selfbuilt"}:
        defaults = ["--backend", "tiermem"] + defaults
    return defaults


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run an E-mem-style anti-compression control branch against an existing RQ harness."
    )
    parser.add_argument("--task", choices=sorted(TASK_TO_SCRIPT), required=True)
    parser.add_argument("--print-only", action="store_true",
                        help="Print the resolved command instead of executing it.")
    parser.add_argument("--python-bin", default=sys.executable)
    args, forwarded = parser.parse_known_args()
    _reject_overrides(forwarded)

    cmd = [args.python_bin, str(TASK_TO_SCRIPT[args.task]), *_build_defaults(args.task), *forwarded]
    print(json.dumps({
        "branch": "emem_style",
        "task": args.task,
        "script": str(TASK_TO_SCRIPT[args.task]),
        "command": cmd,
    }, ensure_ascii=False, indent=2))
    if args.print_only:
        return 0
    subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
