from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/halumem_official_baseline_matrix_status.json"
SUMMARY_PATH = "outputs/halumem_official_baseline_matrix_status.md"

SYSTEM_SPECS = {
    "memzero": {
        "script": "eval_memzero.py",
        "frame": "memzero",
        "required_env": ["MEM0_API_KEY", "OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "RETRY_TIMES", "WAIT_TIME_LOWER", "WAIT_TIME_UPPER"],
        "required_packages": ["mem0", "openai", "tenacity", "dotenv", "tqdm"],
        "notes": "Single-stage run; then score with evaluation.py --frame memzero.",
    },
    "zep": {
        "script": "eval_zep.py",
        "frame": "zep",
        "required_env": ["ZEP_API_KEY", "OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "RETRY_TIMES", "WAIT_TIME_LOWER", "WAIT_TIME_UPPER"],
        "required_packages": ["zep_cloud", "openai", "tenacity", "dotenv", "tqdm"],
        "notes": "Two-stage run: first add, then search, then score with evaluation.py --frame zep.",
    },
    "memos": {
        "script": "eval_memos.py",
        "frame": "memos",
        "required_env": ["MEMOS_URL", "MEMOS_KEY", "OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "RETRY_TIMES", "WAIT_TIME_LOWER", "WAIT_TIME_UPPER"],
        "required_packages": ["requests", "openai", "tenacity", "dotenv", "tqdm"],
        "notes": "Single-stage run; then score with evaluation.py --frame memos.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Readiness and execution helper for official HaluMem memory-system baselines.")
    parser.add_argument("--systems", default="memzero,zep,memos", help="Comma-separated system list.")
    parser.add_argument("--execute", action="store_true", help="Reserved flag: execute ready systems via the official wrappers.")
    return parser.parse_args()


def package_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def env_present(name: str) -> bool:
    return bool(os.environ.get(name, "").strip())


def build_status_row(system: str, spec: dict[str, Any], eval_dir: Path) -> dict[str, Any]:
    missing_env = [name for name in spec["required_env"] if not env_present(name)]
    missing_packages = [name for name in spec["required_packages"] if not package_available(name)]
    script_path = eval_dir / spec["script"]
    return {
        "system": system,
        "frame": spec["frame"],
        "script": str(script_path),
        "script_exists": script_path.exists(),
        "required_env": spec["required_env"],
        "missing_env": missing_env,
        "required_packages": spec["required_packages"],
        "missing_packages": missing_packages,
        "ready": script_path.exists() and (not missing_env) and (not missing_packages),
        "notes": spec["notes"],
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# HaluMem Official Baseline Matrix Status",
        "",
        "This artifact turns A1 into an explicit execution surface: which official memory systems are wired in, what each one requires, and whether the current environment is ready to run them.",
        "",
        f"- eval_dir: `{payload['eval_dir']}`",
        "",
        "| System | Ready | Missing env | Missing packages | Script | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for row in payload["systems"]:
        missing_env = ", ".join(row["missing_env"]) if row["missing_env"] else "-"
        missing_packages = ", ".join(row["missing_packages"]) if row["missing_packages"] else "-"
        lines.append(
            f"| {row['system']} | {row['ready']} | {missing_env} | {missing_packages} | {Path(row['script']).name} | {row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            "- The next A1 step is to fill the missing env / package gaps for at least `memzero` and one of `zep` or `memos`, then run the official wrappers and score them through `evaluation.py`.",
            "- This repo now has a single status surface for that work instead of relying on manual README interpretation.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parent
    eval_dir = base_dir / "benchmarks/halumem/official_repo/eval"
    systems = [part.strip() for part in args.systems.split(",") if part.strip()]
    rows = [build_status_row(system, SYSTEM_SPECS[system], eval_dir) for system in systems]
    result = {
        "description": "Readiness status for official HaluMem memory-system baseline wrappers.",
        "eval_dir": str(eval_dir),
        "systems": rows,
        "execute_requested": args.execute,
    }
    (base_dir / JSON_PATH).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(result), encoding="utf-8")


if __name__ == "__main__":
    main()
