from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class CheckResult:
    name: str
    status: str
    pass_condition: str
    current_state: str
    evidence: list[str]
    blockers: list[str]
    next_action: str


def run_command(cmd: list[str], cwd: Path) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except Exception as exc:
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
        }


def find_repo(workspace_root: Path, patterns: list[str]) -> Path | None:
    for child in workspace_root.iterdir():
        if not child.is_dir():
            continue
        lowered = child.name.lower()
        if any(pattern in lowered for pattern in patterns):
            return child
    return None


def bridge_check(repo_root: Path, benchmark: str) -> dict[str, Any]:
    python_path = repo_root / ".venv_tiermem_v2" / "bin" / "python"
    script_path = repo_root / "run_v2_tiermem_local_bridge.py"
    if not python_path.exists() or not script_path.exists():
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": "bridge runtime missing",
        }
    return run_command(
        [str(python_path), str(script_path), "--check-only", "--benchmark", benchmark],
        cwd=repo_root,
    )


def parse_bridge_readiness(result: dict[str, Any]) -> dict[str, Any]:
    stdout = result.get("stdout", "")
    missing_env = "missing required env var: OPENAI_API_KEY" in stdout
    missing_modules = "missing required modules:" in stdout
    missing_data = "missing benchmark data for" in stdout
    ready = "Readiness verdict: READY FOR A MINIMAL LOCAL SANITY RUN" in stdout
    preflight_line = None
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if line.startswith("dataset_loader_preflight:"):
            preflight_line = line
            break
    return {
        "ready": ready,
        "missing_openai_key": missing_env,
        "missing_modules": missing_modules,
        "missing_data": missing_data,
        "env_only_blocked": missing_env and not missing_modules and not missing_data,
        "dataset_loader_preflight": preflight_line,
    }


def load_license_first_line(path: Path) -> str | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line:
                return line
    return None


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def build_checks(repo_root: Path) -> list[CheckResult]:
    workspace_root = repo_root.parent
    tiermem_root = workspace_root / "tiermem_upstream"
    halumem_root = repo_root / "benchmarks" / "halumem" / "official_repo"
    longmemeval_root = repo_root / "benchmarks" / "locomo" / "longmemeval_official"
    agentpoison_root = find_repo(workspace_root, ["agentpoison"])
    mpbench_root = find_repo(workspace_root, ["mpbench"])
    memevobench_root = find_repo(workspace_root, ["memevobench"])

    locomo_bridge = bridge_check(repo_root, "locomo")
    longmemeval_bridge = bridge_check(repo_root, "longmemeval")
    halumem_bridge = bridge_check(repo_root, "halumem")
    locomo_bridge_state = parse_bridge_readiness(locomo_bridge)
    longmemeval_bridge_state = parse_bridge_readiness(longmemeval_bridge)
    halumem_bridge_state = parse_bridge_readiness(halumem_bridge)

    halumem_medium = halumem_root / "data" / "HaluMem-Medium.jsonl"
    tiermem_license = load_license_first_line(tiermem_root / "LICENSE")
    longmemeval_license = load_license_first_line(longmemeval_root / "LICENSE")
    halumem_readme = read_text(halumem_root / "README.md")
    halumem_hf_link = "https://huggingface.co/datasets/IAAR-Shanghai/HaluMem"
    halumem_license_badge = "CC-BY-NC-ND-4.0" if "CC-BY-NC-ND-4.0" in halumem_readme else None

    checks: list[CheckResult] = []

    tiermem_blockers: list[str] = []
    if not tiermem_root.exists():
        tiermem_blockers.append("tiermem_upstream clone is missing")
    if locomo_bridge_state["env_only_blocked"]:
        tiermem_blockers.append("LoCoMo tiny sanity run is blocked only by OPENAI_API_KEY")
    elif locomo_bridge["returncode"] != 0:
        tiermem_blockers.append("LoCoMo bridge has additional unresolved runtime issues")
    if longmemeval_bridge_state["env_only_blocked"]:
        tiermem_blockers.append("LongMemEval tiny sanity run is blocked only by OPENAI_API_KEY")
    elif longmemeval_bridge["returncode"] != 0:
        tiermem_blockers.append("LongMemEval bridge has additional unresolved runtime issues")
    checks.append(
        CheckResult(
            name="TierMem usable",
            status="partial" if tiermem_root.exists() else "fail",
            pass_condition="Clone TierMem and run one supported eval end-to-end with the real raw tier, provenance links, and router present in code.",
            current_state=(
                "TierMem is cloned locally and the dedicated .venv_tiermem_v2 runtime passes local import/data preflight for both LoCoMo and LongMemEval. The remaining blocker for a real tiny run is OPENAI_API_KEY."
                if tiermem_root.exists()
                else "TierMem is not present locally."
            ),
            evidence=[
                "repo: ../tiermem_upstream",
                f"license: {tiermem_license or 'missing'}",
                f"locomo bridge returncode={locomo_bridge['returncode']}",
                f"longmemeval bridge returncode={longmemeval_bridge['returncode']}",
                f"locomo env_only_blocked={locomo_bridge_state['env_only_blocked']}",
                f"longmemeval env_only_blocked={longmemeval_bridge_state['env_only_blocked']}",
                f"locomo {locomo_bridge_state['dataset_loader_preflight'] or 'dataset_loader_preflight: unavailable'}",
                f"longmemeval {longmemeval_bridge_state['dataset_loader_preflight'] or 'dataset_loader_preflight: unavailable'}",
            ],
            blockers=tiermem_blockers or ["none recorded"],
            next_action="Set OPENAI_API_KEY and run a tiny bridge sanity pass on LoCoMo, then LongMemEval.",
        )
    )

    halumem_blockers: list[str] = []
    if not halumem_root.exists():
        halumem_blockers.append("mirrored HaluMem repo is missing")
    if not halumem_medium.exists():
        halumem_blockers.append("final HaluMem-Medium.jsonl is not mirrored locally; source is the official Hugging Face dataset")
    if halumem_bridge_state["missing_openai_key"]:
        halumem_blockers.append("HaluMem bridge also needs OPENAI_API_KEY once the Medium file is present")
    elif halumem_bridge["returncode"] != 0:
        halumem_blockers.append("HaluMem bridge check is not runnable end-to-end yet")
    checks.append(
        CheckResult(
            name="HaluMem usable",
            status="partial" if halumem_root.exists() else "fail",
            pass_condition="Load the official HaluMem data and run one official Medium eval end-to-end.",
            current_state=(
                "The mirrored HaluMem repo and eval helpers are present, and the official README points to the Hugging Face release. The remaining local gap is the missing HaluMem-Medium.jsonl file expected by both TierMem and the official eval scripts."
                if halumem_root.exists()
                else "The local HaluMem mirror is missing."
            ),
            evidence=[
                "repo: benchmarks/halumem/official_repo",
                f"final_medium_present: {halumem_medium.exists()}",
                f"bridge returncode={halumem_bridge['returncode']}",
                f"dataset_source: {halumem_hf_link}",
                f"license_badge_in_readme: {halumem_license_badge or 'not found'}",
            ],
            blockers=halumem_blockers or ["none recorded"],
            next_action="Download HaluMem-Medium from the official Hugging Face dataset, place it under benchmarks/halumem/official_repo/data/, and rerun the bridge check with a real API key.",
        )
    )

    checks.append(
        CheckResult(
            name="AgentPoison usable",
            status="paper_only" if agentpoison_root is None else "partial",
            pass_condition="Clone AgentPoison and generate at least one usable trigger/query poisoning overlay.",
            current_state=(
                "No local AgentPoison repo was found in the workspace."
                if agentpoison_root is None
                else "A local AgentPoison-like repo exists, but it has not yet been audited by this workspace."
            ),
            evidence=[f"local_repo: {'../' + agentpoison_root.name if agentpoison_root else 'not found'}"],
            blockers=["local AgentPoison artifacts are absent"],
            next_action="Clone AgentPoison and confirm trigger generation before claiming the safety attack suite is executable.",
        )
    )

    checks.append(
        CheckResult(
            name="MPBench / MemEvoBench availability",
            status="paper_only",
            pass_condition="Confirm whether MPBench and MemEvoBench release runnable code plus data, not only papers.",
            current_state="Neither MPBench nor MemEvoBench local repos were found in the workspace, so they should still be treated as taxonomy references only.",
            evidence=[
                f"mpbench_repo: {'../' + mpbench_root.name if mpbench_root else 'not found'}",
                f"memevobench_repo: {'../' + memevobench_root.name if memevobench_root else 'not found'}",
            ],
            blockers=["artifact availability is still unverified locally"],
            next_action="Keep them out of promised experiments until real public artifacts are confirmed.",
        )
    )

    citation_blockers: list[str] = []
    if agentpoison_root is None:
        citation_blockers.append("recent safety benchmark repos are not yet verified locally")
    if not halumem_medium.exists():
        citation_blockers.append("HaluMem final dataset packaging remains incomplete locally")
    checks.append(
        CheckResult(
            name="Citation reality",
            status="partial",
            pass_condition="Every cited paper ID, repo URL, and benchmark artifact must resolve to a real accessible object before release.",
            current_state="TierMem, HaluMem, and LongMemEval are grounded by local repos or mirrors, but the more recent safety-side citations are still only plan references in this workspace.",
            evidence=[
                f"tiermem_repo: {tiermem_root.exists()}",
                f"halumem_repo: {halumem_root.exists()}",
                f"longmemeval_repo: {longmemeval_root.exists()}",
                f"agentpoison_repo: {agentpoison_root or 'not found'}",
            ],
            blockers=citation_blockers or ["none recorded"],
            next_action="Do a fresh citation-and-license pass before any public release or paper submission.",
        )
    )

    license_blockers: list[str] = []
    if tiermem_license is None:
        license_blockers.append("TierMem license not found")
    if longmemeval_license is None:
        license_blockers.append("LongMemEval license not found")
    if halumem_license_badge is None and not (halumem_root / "LICENSE").exists():
        license_blockers.append("HaluMem local mirror has no obvious standalone license signal")
    checks.append(
        CheckResult(
            name="License compatibility",
            status="partial",
            pass_condition="All reused repos must have a verified license compatible with the intended public release plan.",
            current_state="TierMem and LongMemEval expose local license files. HaluMem's mirrored root does not ship a standalone LICENSE file, but its README advertises CC-BY-NC-ND-4.0, so the remaining task is to verify and document that signal cleanly before release.",
            evidence=[
                f"tiermem_license: {tiermem_license or 'missing'}",
                f"longmemeval_license: {longmemeval_license or 'missing'}",
                f"halumem_license_present: {(halumem_root / 'LICENSE').exists()}",
                f"halumem_license_badge: {halumem_license_badge or 'not found'}",
            ],
            blockers=license_blockers or ["none recorded"],
            next_action="Verify the exact licenses of all mirrored benchmark repos before packaging a public release.",
        )
    )

    return checks


def write_report(repo_root: Path, checks: list[CheckResult]) -> None:
    output_json = repo_root / "outputs" / "v3_feasibility_gate.json"
    report_md = repo_root / "feasibility_report.md"
    output_json.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_on": date.today().isoformat(),
        "repo_root": ".",
        "checks": [asdict(check) for check in checks],
    }
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Feasibility Report",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This is the Week-0 V3 feasibility gate. It records what is already locally grounded, what only partially runs, and what remains paper-only in the current workspace.",
        "",
        "| Check | Status | Pass Condition | Current State |",
        "|---|---|---|---|",
    ]
    for check in checks:
        lines.append(
            f"| {check.name} | `{check.status}` | {check.pass_condition} | {check.current_state} |"
        )
    lines.append("")
    lines.append("## Details")
    lines.append("")
    for check in checks:
        lines.append(f"### {check.name}")
        lines.append("")
        lines.append(f"- status: `{check.status}`")
        lines.append(f"- pass condition: {check.pass_condition}")
        lines.append(f"- current state: {check.current_state}")
        lines.append("- evidence:")
        lines.extend([f"  - {item}" for item in check.evidence])
        lines.append("- blockers:")
        lines.extend([f"  - {item}" for item in check.blockers])
        lines.append(f"- next action: {check.next_action}")
        lines.append("")
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    checks = build_checks(repo_root)
    write_report(repo_root, checks)
    print(f"[v3-feasibility] wrote {repo_root / 'feasibility_report.md'}")
    print(f"[v3-feasibility] wrote {repo_root / 'outputs' / 'v3_feasibility_gate.json'}")


if __name__ == "__main__":
    main()
