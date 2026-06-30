from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_local_capability_matrix.json"
SUMMARY_PATH = "outputs/v3_local_capability_matrix.md"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def profile_ready(prefix: str) -> bool:
    return all(os.environ.get(name, "").strip() for name in [f"{prefix}_API_KEY", f"{prefix}_BASE_URL", f"{prefix}_MODEL"])


def build_rows(repo_root: Path) -> list[dict[str, Any]]:
    feasibility = load_json(repo_root / "outputs" / "v3_feasibility_gate.json")
    halumem_preflight = load_json(repo_root / "outputs" / "v3_halumem_dataset_preflight.json")
    public_baselines = load_json(repo_root / "outputs" / "v3_public_baseline_readiness.json")
    official_eval_runtime = load_json(repo_root / "outputs" / "v3_official_eval_runtime_audit.json")
    no_rewrite = load_json(repo_root / "outputs" / "v3_no_rewrite_policy_audit.json")

    feasibility_map = {entry["name"]: entry for entry in feasibility.get("checks", [])}
    public_rows = public_baselines.get("rows", [])
    any_public_ready = any(row.get("status") == "ready" for row in public_rows)
    all_public_partial_or_better = all(row.get("status") in {"ready", "partial"} for row in public_rows) if public_rows else False
    blocked_rate_n8 = no_rewrite.get("overall", {}).get("n8_blocked_protected_case_rate", 0.0)
    public_blockers = {
        row.get("system_name", "unknown"): "; ".join(row.get("blockers", []))
        for row in public_rows
    }
    halumem_blocker = (
        "dataset is already present"
        if halumem_preflight.get("expected_present")
        else "canonical HaluMem-Medium.jsonl file is still missing"
    )
    official_eval_blocker = (
        "none"
        if official_eval_runtime.get("official_eval_venv_present")
        else "scaffold exists, but .venv_official_eval has not been created yet"
    )

    gpt_ready = profile_ready("GPT_OPENAI")
    qwen_ready = profile_ready("QWEN_OPENAI")
    llama_ready = profile_ready("LLAMA_OPENAI")

    return [
        {
            "task": "V3 transition rebuild",
            "can_do_on_mac": "yes",
            "status": "ready",
            "blocker": "none",
            "next_command": "python3 run_v3_transition_rebuild.py",
        },
        {
            "task": "TierMem tiny sanity run",
            "can_do_on_mac": "partial",
            "status": feasibility_map.get("TierMem usable", {}).get("status", "missing"),
            "blocker": (
                "; ".join(feasibility_map.get("TierMem usable", {}).get("blockers", ["unknown"]))
                if feasibility_map
                else "unknown"
            ),
            "next_command": ".venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --benchmark locomo --limit 2",
        },
        {
            "task": "Official public baseline setup audit",
            "can_do_on_mac": "yes",
            "status": public_baselines.get("overall_status", "missing"),
            "blocker": "none" if all_public_partial_or_better else "official harness files are incomplete",
            "next_command": "python3 run_v3_public_baseline_readiness.py",
        },
        {
            "task": "HaluMem dataset preflight",
            "can_do_on_mac": "yes",
            "status": halumem_preflight.get("status", "missing"),
            "blocker": halumem_blocker,
            "next_command": "python3 run_v3_halumem_dataset_preflight.py",
        },
        {
            "task": "Official eval runtime scaffold",
            "can_do_on_mac": "yes",
            "status": official_eval_runtime.get("status", "missing"),
            "blocker": official_eval_blocker,
            "next_command": "python3 run_v3_official_eval_runtime_audit.py",
        },
        {
            "task": "Official public baseline live runs",
            "can_do_on_mac": "partial" if public_rows else "no",
            "status": "ready" if any_public_ready else public_baselines.get("overall_status", "missing"),
            "blocker": (
                f"Mem0: {public_blockers.get('Mem0', 'unknown')} | "
                f"Zep: {public_blockers.get('Zep', 'unknown')} | "
                f"MemOS: {public_blockers.get('MemoryOS / MemOS', 'unknown')}"
            ),
            "next_command": "python3 benchmarks/halumem/official_repo/eval/eval_memzero.py",
        },
        {
            "task": "Safety-critical no-rewrite dry-run audit",
            "can_do_on_mac": "yes",
            "status": "ready" if no_rewrite else "missing",
            "blocker": "none" if no_rewrite else "audit has not been generated yet",
            "next_command": "python3 run_v3_no_rewrite_policy_audit.py",
        },
        {
            "task": "Legacy support analyses for V3 appendix",
            "can_do_on_mac": "yes",
            "status": "ready",
            "blocker": "none",
            "next_command": "python3 run_expanded_benchmark_main_cost_pareto.py && python3 run_expanded_benchmark_main_probe_sweep.py && python3 run_expanded_benchmark_main_significance.py",
        },
        {
            "task": "TierMem pre-API smoke",
            "can_do_on_mac": "yes",
            "status": "ready",
            "blocker": "none",
            "next_command": ".venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --pre-api-smoke --benchmark locomo",
        },
        {
            "task": "Legacy multi-backbone profile runs",
            "can_do_on_mac": "partial",
            "status": "ready" if any([gpt_ready, qwen_ready, llama_ready]) else "partial",
            "blocker": (
                f"configured profiles: gpt={gpt_ready}, qwen={qwen_ready}, llama={llama_ready}; deepseek_cli={shutil.which('deepseek') is not None}"
            ),
            "next_command": "python3 run_expanded_benchmark_backbone_profile.py main gpt_openai_profile",
        },
        {
            "task": "AgentPoison attack suite grounding",
            "can_do_on_mac": "no",
            "status": feasibility_map.get("AgentPoison usable", {}).get("status", "missing"),
            "blocker": ", ".join(feasibility_map.get("AgentPoison usable", {}).get("blockers", ["local repo absent"])) if feasibility_map else "local repo absent",
            "next_command": "Clone AgentPoison before claiming the safety attack suite is executable.",
        },
        {
            "task": "V3 defended-method maturity",
            "can_do_on_mac": "yes",
            "status": "partial",
            "blocker": f"local no-rewrite scaffold exists, but it is still a dry-run surface; current N=8 blocked protected rate = {blocked_rate_n8}",
            "next_command": "Wire the no-rewrite rule into the real TierMem path after the tiny bridge sanity run succeeds.",
        },
    ]


def build_payload(repo_root: Path) -> dict[str, Any]:
    rows = build_rows(repo_root)
    return {
        "repo_root": ".",
        "description": "Local capability matrix for what this Mac can execute now under the V3 migration plan.",
        "rows": rows,
        "counts": {
            "yes": sum(1 for row in rows if row["can_do_on_mac"] == "yes"),
            "partial": sum(1 for row in rows if row["can_do_on_mac"] == "partial"),
            "no": sum(1 for row in rows if row["can_do_on_mac"] == "no"),
        },
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 Local Capability Matrix",
        "",
        payload["description"],
        "",
        f"- fully doable now: `{payload['counts']['yes']}`",
        f"- partially doable now: `{payload['counts']['partial']}`",
        f"- blocked locally: `{payload['counts']['no']}`",
        "",
        "| Task | Can Do | Status | Blocker | Next Command |",
        "|---|---|---|---|---|",
    ]
    for row in payload["rows"]:
        blocker = str(row["blocker"]).replace("|", "\\|")
        next_command = str(row["next_command"]).replace("|", "\\|")
        lines.append(
            f"| {row['task']} | `{row['can_do_on_mac']}` | `{row['status']}` | {blocker} | `{next_command}` |"
        )
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-capability] wrote {repo_root / JSON_PATH}")
    print(f"[v3-capability] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
