from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_public_baseline_readiness.json"
SUMMARY_PATH = "outputs/v3_public_baseline_readiness.md"
TIERMEM_VENV_PYTHON = "memory_consolidation_small_pilot/.venv_tiermem_v2/bin/python"

BASELINE_SPECS = [
    {
        "baseline_id": "mem0_memzero",
        "system_name": "Mem0",
        "official_script": "benchmarks/halumem/official_repo/eval/eval_memzero.py",
        "eval_frame": "memzero",
        "required_env": ["MEM0_API_KEY", "OPENAI_API_KEY"],
        "required_imports": ["mem0", "dotenv", "tenacity", "tqdm"],
        "dataset_path": "benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl",
        "dataset_source": "https://huggingface.co/datasets/IAAR-Shanghai/HaluMem",
        "runtime_kind": "cloud_api",
        "next_command": "python3 benchmarks/halumem/official_repo/eval/eval_memzero.py",
    },
    {
        "baseline_id": "zep",
        "system_name": "Zep",
        "official_script": "benchmarks/halumem/official_repo/eval/eval_zep.py",
        "eval_frame": "zep",
        "required_env": ["ZEP_API_KEY", "OPENAI_API_KEY"],
        "required_imports": ["zep_cloud", "dotenv", "tenacity", "tqdm"],
        "dataset_path": "benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl",
        "dataset_source": "https://huggingface.co/datasets/IAAR-Shanghai/HaluMem",
        "runtime_kind": "cloud_api",
        "next_command": "python3 benchmarks/halumem/official_repo/eval/eval_zep.py",
    },
    {
        "baseline_id": "memoryos_memos",
        "system_name": "MemoryOS / MemOS",
        "official_script": "benchmarks/halumem/official_repo/eval/eval_memos.py",
        "eval_frame": "memos",
        "required_env": ["MEMOS_URL", "MEMOS_KEY", "OPENAI_API_KEY"],
        "required_imports": ["requests", "dotenv", "tenacity", "tqdm"],
        "dataset_path": "benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl",
        "dataset_source": "https://huggingface.co/datasets/IAAR-Shanghai/HaluMem",
        "runtime_kind": "service_endpoint",
        "next_command": "python3 benchmarks/halumem/official_repo/eval/eval_memos.py",
    },
]


@dataclass
class BaselineReadiness:
    baseline_id: str
    system_name: str
    eval_frame: str
    official_script: str
    runtime_kind: str
    status: str
    dataset_present: bool
    dataset_source: str
    present_env: list[str]
    missing_env: list[str]
    present_imports: list[str]
    missing_imports: list[str]
    best_runtime_label: str
    runtime_missing_imports: dict[str, list[str]]
    blockers: list[str]
    next_action: str
    command_example: str


def module_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def runtime_python_candidates(repo_root: Path) -> list[tuple[str, Path]]:
    candidates = [("current_python", Path(sys.executable))]
    tiermem_python = repo_root / TIERMEM_VENV_PYTHON
    if tiermem_python.exists():
        candidates.append(("tiermem_venv", tiermem_python))
    return candidates


def check_imports_in_runtime(python_path: Path, module_names: list[str]) -> tuple[list[str], list[str]]:
    script = (
        "import importlib.util, json\n"
        f"mods = {module_names!r}\n"
        "present=[m for m in mods if importlib.util.find_spec(m) is not None]\n"
        "missing=[m for m in mods if m not in present]\n"
        "print(json.dumps({'present':present,'missing':missing}))\n"
    )
    completed = subprocess.run(
        [str(python_path), "-c", script],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return [], list(module_names)
    payload = json.loads(completed.stdout)
    return payload["present"], payload["missing"]


def assess_baseline(repo_root: Path, spec: dict[str, Any]) -> BaselineReadiness:
    script_exists = (repo_root / spec["official_script"]).exists()
    dataset_present = (repo_root / spec["dataset_path"]).exists()
    present_env = [name for name in spec["required_env"] if os.environ.get(name, "").strip()]
    missing_env = [name for name in spec["required_env"] if name not in present_env]

    runtime_results: dict[str, dict[str, list[str]]] = {}
    for label, python_path in runtime_python_candidates(repo_root):
        present, missing = check_imports_in_runtime(python_path, spec["required_imports"])
        runtime_results[label] = {"present": present, "missing": missing}

    best_runtime_label = min(runtime_results, key=lambda label: len(runtime_results[label]["missing"]))
    present_imports = runtime_results[best_runtime_label]["present"]
    missing_imports = runtime_results[best_runtime_label]["missing"]

    blockers: list[str] = []
    if not script_exists:
        blockers.append("official eval script missing")
    if not dataset_present:
        blockers.append(f"HaluMem-Medium.jsonl missing (official source: {spec['dataset_source']})")
    if missing_env:
        blockers.append(f"missing env vars: {missing_env}")
    if missing_imports:
        blockers.append(f"missing imports in best local runtime ({best_runtime_label}): {missing_imports}")

    if script_exists and dataset_present and not missing_env and not missing_imports:
        status = "ready"
    elif script_exists:
        status = "partial"
    else:
        status = "missing"

    next_action = "Run the official adapter on HaluMem-Medium and then score it via evaluation.py."
    if blockers:
        next_action = f"Unblock {spec['system_name']} by resolving: {', '.join(blockers)}."

    return BaselineReadiness(
        baseline_id=spec["baseline_id"],
        system_name=spec["system_name"],
        eval_frame=spec["eval_frame"],
        official_script=spec["official_script"],
        runtime_kind=spec["runtime_kind"],
        status=status,
        dataset_present=dataset_present,
        dataset_source=spec["dataset_source"],
        present_env=present_env,
        missing_env=missing_env,
        present_imports=present_imports,
        missing_imports=missing_imports,
        best_runtime_label=best_runtime_label,
        runtime_missing_imports={label: data["missing"] for label, data in runtime_results.items()},
        blockers=blockers or ["none recorded"],
        next_action=next_action,
        command_example=spec["next_command"],
    )


def build_payload(repo_root: Path) -> dict[str, Any]:
    rows = [assess_baseline(repo_root, spec) for spec in BASELINE_SPECS]
    ready = sum(1 for row in rows if row.status == "ready")
    partial = sum(1 for row in rows if row.status == "partial")
    overall_status = "ready" if ready == len(rows) else "partial" if (ready + partial) > 0 else "missing"
    return {
        "repo_root": ".",
        "description": "Local readiness audit for the real public memory-system baselines demanded by V3.",
        "overall_status": overall_status,
        "ready_count": ready,
        "partial_count": partial,
        "rows": [asdict(row) for row in rows],
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 Public Baseline Readiness",
        "",
        payload["description"],
        "",
        f"- overall status: `{payload['overall_status']}`",
        f"- ready adapters: `{payload['ready_count']}`",
        f"- partial adapters: `{payload['partial_count']}`",
        "",
        "| System | Frame | Status | Dataset | Best Runtime | Missing Env | Missing Imports |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in payload["rows"]:
        missing_env = ", ".join(row["missing_env"]) if row["missing_env"] else "none"
        missing_imports = ", ".join(row["missing_imports"]) if row["missing_imports"] else "none"
        lines.append(
            f"| {row['system_name']} | `{row['eval_frame']}` | `{row['status']}` | `{row['dataset_present']}` | `{row['best_runtime_label']}` | {missing_env} | {missing_imports} |"
        )
    lines.extend(["", "## Next Actions", ""])
    for row in payload["rows"]:
        lines.append(
            f"- {row['system_name']}: script=`{row['official_script']}`; runtime=`{row['best_runtime_label']}`; dataset_source=`{row['dataset_source']}`; next=`{row['command_example']}`; blocker=`{'; '.join(row['blockers'])}`"
        )
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-public-baselines] wrote {repo_root / JSON_PATH}")
    print(f"[v3-public-baselines] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
