from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_official_eval_runtime_audit.json"
SUMMARY_PATH = "outputs/v3_official_eval_runtime_audit.md"

COMMON_IMPORTS = ["openai", "dotenv", "tenacity", "tqdm", "requests"]
BASELINE_IMPORTS = {
    "mem0_memzero": ["mem0"],
    "zep": ["zep_cloud"],
    "memos": [],
}


def rel(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def runtime_candidates(repo_root: Path) -> list[tuple[str, Path]]:
    return [
        ("current_python", Path(sys.executable)),
        ("tiermem_venv", repo_root / ".venv_tiermem_v2" / "bin" / "python"),
        ("official_eval_venv", repo_root / ".venv_official_eval" / "bin" / "python"),
    ]


def check_imports(python_path: Path, modules: list[str]) -> tuple[list[str], list[str]]:
    if not python_path.exists():
        return [], modules
    script = (
        "import importlib.util, json\n"
        f"mods = {modules!r}\n"
        "present=[m for m in mods if importlib.util.find_spec(m) is not None]\n"
        "missing=[m for m in mods if m not in present]\n"
        "print(json.dumps({'present': present, 'missing': missing}))\n"
    )
    completed = subprocess.run(
        [str(python_path), "-c", script],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return [], modules
    payload = json.loads(completed.stdout)
    return payload["present"], payload["missing"]


def build_payload(repo_root: Path) -> dict[str, Any]:
    dataset_preflight = {}
    dataset_preflight_path = repo_root / "outputs" / "v3_halumem_dataset_preflight.json"
    if dataset_preflight_path.exists():
        dataset_preflight = json.loads(dataset_preflight_path.read_text(encoding="utf-8"))

    rows = []
    for label, python_path in runtime_candidates(repo_root):
        common_present, common_missing = check_imports(python_path, COMMON_IMPORTS)
        baseline_missing = {
            baseline: check_imports(python_path, imports)[1]
            for baseline, imports in BASELINE_IMPORTS.items()
        }
        rows.append(
            {
                "runtime": label,
                "python_path": rel(repo_root, python_path),
                "exists": python_path.exists(),
                "common_present": common_present,
                "common_missing": common_missing,
                "baseline_missing": baseline_missing,
            }
        )

    env_templates = {
        ".env.v3.example": (repo_root / ".env.v3.example").exists(),
        ".env.official_eval.example": (repo_root / ".env.official_eval.example").exists(),
        "benchmarks/halumem/official_repo/eval/.env-example": (
            repo_root / "benchmarks" / "halumem" / "official_repo" / "eval" / ".env-example"
        ).exists(),
    }
    requirements_present = (repo_root / "requirements-official-eval-base.txt").exists()
    ready_runtimes = sum(
        1
        for row in rows
        if row["exists"] and not row["common_missing"]
    )
    venv_present = any(row["runtime"] == "official_eval_venv" and row["exists"] for row in rows)
    status = "ready" if venv_present and ready_runtimes > 0 else "partial"

    return {
        "repo_root": ".",
        "description": "Scaffold/runtime audit for the mirrored HaluMem official evaluation path, excluding live API execution.",
        "status": status,
        "env_templates": env_templates,
        "base_requirements_present": requirements_present,
        "rows": rows,
        "ready_runtime_count": ready_runtimes,
        "official_eval_venv_present": venv_present,
        "dataset_expected_present": dataset_preflight.get("expected_present"),
        "dataset_expected_path": dataset_preflight.get("expected_path"),
        "next_commands": [
            "python3 -m venv .venv_official_eval",
            ".venv_official_eval/bin/pip install -r requirements-official-eval-base.txt",
            "Populate .env.official_eval using the chosen system's keys and endpoints.",
            "Install the selected system SDK after choosing a concrete baseline (for example, Mem0 or Zep).",
        ],
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 Official Eval Runtime Audit",
        "",
        payload["description"],
        "",
        f"- status: `{payload['status']}`",
        f"- official eval venv present: `{payload['official_eval_venv_present']}`",
        f"- ready runtime count: `{payload['ready_runtime_count']}`",
        f"- base requirements present: `{payload['base_requirements_present']}`",
        f"- HaluMem expected dataset present: `{payload['dataset_expected_present']}`",
        f"- HaluMem expected dataset path: `{payload['dataset_expected_path']}`",
        "",
        "## Env Templates",
        "",
    ]
    for key, value in payload["env_templates"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Runtime Matrix",
            "",
            "| Runtime | Exists | Common Missing | Mem0 Missing | Zep Missing | MemOS Missing |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in payload["rows"]:
        common_missing = ", ".join(row["common_missing"]) if row["common_missing"] else "none"
        mem0_missing = ", ".join(row["baseline_missing"]["mem0_memzero"]) if row["baseline_missing"]["mem0_memzero"] else "none"
        zep_missing = ", ".join(row["baseline_missing"]["zep"]) if row["baseline_missing"]["zep"] else "none"
        memos_missing = ", ".join(row["baseline_missing"]["memos"]) if row["baseline_missing"]["memos"] else "none"
        lines.append(
            f"| `{row['runtime']}` | `{row['exists']}` | {common_missing} | {mem0_missing} | {zep_missing} | {memos_missing} |"
        )
    lines.extend(["", "## Next Commands", ""])
    for cmd in payload["next_commands"]:
        lines.append(f"- `{cmd}`")
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload) + "\n", encoding="utf-8")
    print(f"[v3-official-eval-audit] wrote {repo_root / JSON_PATH}")
    print(f"[v3-official-eval-audit] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
