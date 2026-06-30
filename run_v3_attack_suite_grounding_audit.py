from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_attack_suite_grounding_audit.json"
SUMMARY_PATH = "outputs/v3_attack_suite_grounding_audit.md"


def find_repo(workspace_root: Path, patterns: list[str]) -> Path | None:
    for child in workspace_root.iterdir():
        if not child.is_dir():
            continue
        lowered = child.name.lower()
        if any(pattern in lowered for pattern in patterns):
            return child
    return None


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def license_first_line(path: Path) -> str | None:
    if not path.exists():
        return None
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if line:
            return line
    return None


def build_payload(repo_root: Path) -> dict[str, Any]:
    workspace_root = repo_root.parent
    agentpoison_root = find_repo(workspace_root, ["agentpoison"])
    mpbench_root = find_repo(workspace_root, ["mpbench"])
    memevobench_root = find_repo(workspace_root, ["memevobench"])

    agentpoison_readme = read_text(agentpoison_root / "README.md") if agentpoison_root else ""
    memevobench_readme = read_text(memevobench_root / "README.md") if memevobench_root else ""

    return {
        "description": "Local grounding audit for safety-side benchmark and attack-suite repositories.",
        "agentpoison": {
            "status": "partial" if agentpoison_root else "missing",
            "repo": str(agentpoison_root) if agentpoison_root else None,
            "license": license_first_line(agentpoison_root / "LICENSE") if agentpoison_root else None,
            "has_environment_yml": bool(agentpoison_root and (agentpoison_root / "environment.yml").exists()),
            "has_trigger_optimization": bool(agentpoison_root and (agentpoison_root / "algo" / "trigger_optimization.py").exists()),
            "has_scripts_dir": bool(agentpoison_root and (agentpoison_root / "scripts").exists()),
            "requires_external_dataset_download": "drive.google.com" in agentpoison_readme,
            "readme_mentions_openai_or_remote_models": ("OpenAI" in agentpoison_readme or "Replicate" in agentpoison_readme),
            "next_action": (
                "Create a minimal local artifact audit and generate one tiny trigger/query overlay."
                if agentpoison_root
                else "Clone the official AgentPoison repository."
            ),
        },
        "mpbench": {
            "status": "missing" if mpbench_root is None else "partial",
            "repo": str(mpbench_root) if mpbench_root else None,
            "next_action": (
                "Search for the official runnable MPBench artifact."
                if mpbench_root is None
                else "Inspect whether the local MPBench-like repo actually corresponds to the intended benchmark."
            ),
        },
        "memevobench": {
            "status": "partial" if memevobench_root else "missing",
            "repo": str(memevobench_root) if memevobench_root else None,
            "license": license_first_line(memevobench_root / "LICENSE") if memevobench_root else None,
            "has_readme": bool(memevobench_root and (memevobench_root / "README.md").exists()),
            "has_evaluation_dir": bool(memevobench_root and (memevobench_root / "evaluation").exists()),
            "has_memorybench_dir": bool(memevobench_root and (memevobench_root / "memorybench").exists()),
            "mentions_workflow_json": "workflow.json" in memevobench_readme,
            "mentions_openai_key": "OPENAI_API_KEY" in memevobench_readme,
            "mentions_judge_key": "JUDGE_API_KEY" in memevobench_readme,
            "next_action": (
                "Inspect one QA-style command and one workflow-style command on a tiny local slice."
                if memevobench_root
                else "Clone the MemEvoBench repository."
            ),
        },
        "overall_conclusion": (
            "AgentPoison and MemEvoBench are now locally grounded at the repository level, but neither attack-suite path is yet counted as executed evidence. "
            "MPBench remains unresolved."
        ),
    }


def build_summary(payload: dict[str, Any]) -> str:
    agentpoison = payload["agentpoison"]
    mpbench = payload["mpbench"]
    memevobench = payload["memevobench"]
    lines = [
        "# V3 Attack Suite Grounding Audit",
        "",
        payload["description"],
        "",
        "## Status",
        "",
        f"- AgentPoison: `{agentpoison['status']}`",
        f"- MPBench: `{mpbench['status']}`",
        f"- MemEvoBench: `{memevobench['status']}`",
        "",
        "## AgentPoison",
        "",
        f"- repo: `{agentpoison['repo']}`",
        f"- license: `{agentpoison['license']}`",
        f"- has_environment_yml: `{agentpoison['has_environment_yml']}`",
        f"- has_trigger_optimization: `{agentpoison['has_trigger_optimization']}`",
        f"- has_scripts_dir: `{agentpoison['has_scripts_dir']}`",
        f"- requires_external_dataset_download: `{agentpoison['requires_external_dataset_download']}`",
        f"- readme_mentions_openai_or_remote_models: `{agentpoison['readme_mentions_openai_or_remote_models']}`",
        f"- next_action: {agentpoison['next_action']}",
        "",
        "## MPBench",
        "",
        f"- repo: `{mpbench['repo']}`",
        f"- next_action: {mpbench['next_action']}",
        "",
        "## MemEvoBench",
        "",
        f"- repo: `{memevobench['repo']}`",
        f"- license: `{memevobench['license']}`",
        f"- has_readme: `{memevobench['has_readme']}`",
        f"- has_evaluation_dir: `{memevobench['has_evaluation_dir']}`",
        f"- has_memorybench_dir: `{memevobench['has_memorybench_dir']}`",
        f"- mentions_workflow_json: `{memevobench['mentions_workflow_json']}`",
        f"- mentions_openai_key: `{memevobench['mentions_openai_key']}`",
        f"- mentions_judge_key: `{memevobench['mentions_judge_key']}`",
        f"- next_action: {memevobench['next_action']}",
        "",
        "## Conclusion",
        "",
        payload["overall_conclusion"],
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-attack-suite-audit] wrote {repo_root / JSON_PATH}")
    print(f"[v3-attack-suite-audit] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
