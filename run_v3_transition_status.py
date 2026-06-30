from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def file_exists(repo_root: Path, relative_path: str) -> bool:
    return (repo_root / relative_path).exists()


def build_payload(repo_root: Path) -> dict[str, Any]:
    release_snapshot = load_json(repo_root / "state" / "release_snapshot.json")
    feasibility = load_json(repo_root / "outputs" / "v3_feasibility_gate.json")
    attack_suite = load_json(repo_root / "outputs" / "v3_attack_suite_grounding_audit.json")
    halumem_preflight = load_json(repo_root / "outputs" / "v3_halumem_dataset_preflight.json")
    public_baselines = load_json(repo_root / "outputs" / "v3_public_baseline_readiness.json")
    official_eval_runtime = load_json(repo_root / "outputs" / "v3_official_eval_runtime_audit.json")
    no_rewrite = load_json(repo_root / "outputs" / "v3_no_rewrite_policy_audit.json")
    no_rewrite_comparison = load_json(repo_root / "outputs" / "v3_no_rewrite_comparison.json")
    no_rewrite_statistics = load_json(repo_root / "outputs" / "v3_no_rewrite_statistics.json")
    no_rewrite_surface_audit = load_json(repo_root / "outputs" / "v3_no_rewrite_surface_audit.json")
    no_rewrite_pareto = load_json(repo_root / "outputs" / "v3_no_rewrite_pareto.json")
    hygiene = load_json(repo_root / "outputs" / "v3_hygiene_audit.json")
    capability = load_json(repo_root / "outputs" / "v3_local_capability_matrix.json")
    local_packet = load_json(repo_root / "outputs" / "v3_local_evidence_packet.json")

    feasibility_map = {
        entry["name"]: entry["status"]
        for entry in feasibility.get("checks", [])
    }
    fairness_surface_present = any(
        row.get("comparison") == "Fairness: blind -> query-aware"
        for row in no_rewrite_statistics.get("rows", [])
    )
    mechanism_surface_present = any(
        row.get("comparison") == "Mechanism: query-aware -> no-rewrite"
        for row in no_rewrite_statistics.get("rows", [])
    )

    payload = {
        "generated_on": date.today().isoformat(),
        "current_identity": {
            "repo_role": "V3 transition workspace",
            "path_decision": "Path A locked: TierMem is the primary base and harness.",
            "legacy_demoted_to": "PSU and the prior proxy stack are retained as baselines plus appendix-style prior exploration.",
        },
        "completed_now": {
            "tiermem_bridge_present": file_exists(repo_root, "run_v2_tiermem_local_bridge.py"),
            "v3_feasibility_gate_present": file_exists(repo_root, "feasibility_report.md"),
            "v3_attack_suite_grounding_audit_present": file_exists(repo_root, "outputs/v3_attack_suite_grounding_audit.md"),
            "v3_halumem_dataset_preflight_present": file_exists(repo_root, "outputs/v3_halumem_dataset_preflight.md"),
            "v3_public_baseline_readiness_present": file_exists(repo_root, "outputs/v3_public_baseline_readiness.md"),
            "v3_official_eval_runtime_audit_present": file_exists(repo_root, "outputs/v3_official_eval_runtime_audit.md"),
            "v3_no_rewrite_policy_audit_present": file_exists(repo_root, "outputs/v3_no_rewrite_policy_audit.md"),
            "v3_no_rewrite_comparison_present": file_exists(repo_root, "outputs/v3_no_rewrite_comparison.md"),
            "v3_no_rewrite_statistics_present": file_exists(repo_root, "outputs/v3_no_rewrite_statistics.md"),
            "v3_no_rewrite_pareto_present": file_exists(repo_root, "outputs/v3_no_rewrite_pareto.md"),
            "v3_local_capability_matrix_present": file_exists(repo_root, "outputs/v3_local_capability_matrix.md"),
            "v3_local_evidence_packet_present": file_exists(repo_root, "outputs/v3_local_evidence_packet.md"),
            "legacy_pilot_findings_present": file_exists(repo_root, "legacy_pilot_findings.md"),
            "v3_alignment_checklist_present": file_exists(repo_root, "state/v3_alignment_master_checklist.md"),
            "v3_hygiene_audit_present": file_exists(repo_root, "outputs/v3_hygiene_audit.md"),
            "legacy_release_rebuild_retained": file_exists(repo_root, "run_release_rebuild.py"),
            "v3_env_template_present": file_exists(repo_root, ".env.v3.example"),
            "official_eval_env_template_present": file_exists(repo_root, ".env.official_eval.example"),
            "official_eval_base_requirements_present": file_exists(repo_root, "requirements-official-eval-base.txt"),
        },
        "week0_gate": {
            "tiermem_usable": feasibility_map.get("TierMem usable", "missing"),
            "halumem_usable": feasibility_map.get("HaluMem usable", "missing"),
            "agentpoison_usable": feasibility_map.get("AgentPoison usable", "missing"),
            "mpbench_memevobench": feasibility_map.get("MPBench / MemEvoBench availability", "missing"),
            "citation_reality": feasibility_map.get("Citation reality", "missing"),
            "license_compatibility": feasibility_map.get("License compatibility", "missing"),
        },
        "execution_order": {
            "e0_real_sanity_gate_passed": False,
            "e0_rule": "Do not treat defense comparisons as paper evidence before the real TierMem/HaluMem E0 sanity gate passes.",
        },
        "v3_scaffolds_now": {
            "public_baseline_readiness": public_baselines.get("overall_status", "missing"),
            "agentpoison_grounding_status": attack_suite.get("agentpoison", {}).get("status", "missing"),
            "memevobench_grounding_status": attack_suite.get("memevobench", {}).get("status", "missing"),
            "mpbench_grounding_status": attack_suite.get("mpbench", {}).get("status", "missing"),
            "halumem_dataset_status": halumem_preflight.get("status", "missing"),
            "halumem_expected_dataset_present": halumem_preflight.get("expected_present"),
            "halumem_candidate_count": halumem_preflight.get("candidate_count"),
            "official_eval_runtime_status": official_eval_runtime.get("status", "missing"),
            "official_eval_ready_runtime_count": official_eval_runtime.get("ready_runtime_count"),
            "official_eval_venv_present": official_eval_runtime.get("official_eval_venv_present"),
            "no_rewrite_policy_scaffold": "partial" if no_rewrite else "missing",
            "no_rewrite_n8_blocked_protected_case_rate": no_rewrite.get("overall", {}).get(
                "n8_blocked_protected_case_rate",
                None,
            ),
            "no_rewrite_comparison_present": bool(no_rewrite_comparison),
            "no_rewrite_comparison_items": no_rewrite_comparison.get("item_count"),
            "local_n_sweep_values": no_rewrite_comparison.get("n_values", []),
            "local_seed_values": no_rewrite_comparison.get("seeds", []),
            "local_architecture_count": len(no_rewrite_comparison.get("architectures", [])),
            "local_query_aware_fairness_surface_present": fairness_surface_present,
            "local_no_rewrite_mechanism_surface_present": mechanism_surface_present,
            "no_rewrite_statistics_rows": len(no_rewrite_statistics.get("rows", [])),
            "no_rewrite_surface_evidence_class": no_rewrite_surface_audit.get("evidence_class", "missing"),
            "no_rewrite_surface_paper_safe": no_rewrite_surface_audit.get("paper_safe"),
            "no_rewrite_pareto_sections": len(no_rewrite_pareto.get("sections", [])),
            "local_evidence_packet_present": bool(local_packet),
            "local_capability_yes_count": capability.get("counts", {}).get("yes"),
            "local_capability_partial_count": capability.get("counts", {}).get("partial"),
            "tiermem_pre_api_smoke_supported": file_exists(repo_root, "run_v2_tiermem_local_bridge.py"),
        },
        "still_pending_for_full_v3": {
            "e0_real_sanity_gate": True,
            "real_public_baselines_run": False,
            "query_blind_vs_query_aware_fairness_pair": False,
            "n_sweep_restored_to_0_1_2_4_8_16": False,
            "five_seed_statistics": False,
            "human_judge_kappa_reported": False,
            "multi_backbone_run": False,
            "full_conflict_unsafe_scale": False,
            "no_rewrite_tiermem_integration": False,
        },
        "full_v3_progress_notes": {
            "e0_real_sanity_gate": "pending: TierMem and HaluMem are still not both running end-to-end with real credentials and real benchmark files",
            "real_public_baselines_run": "pending: only readiness audit is complete locally",
            "halumem_medium_dataset_in_place": (
                "ready: preflight and canonical path are defined, and the final HaluMem-Medium.jsonl file is now present locally"
                if halumem_preflight.get("expected_present")
                else "partial: preflight and canonical path are defined, but the final HaluMem-Medium.jsonl file is still absent locally"
            ),
            "official_eval_runtime_scaffold": "partial: templates and base requirements are present, but .venv_official_eval is not created yet",
            "query_blind_vs_query_aware_fairness_pair": "partial: local proxy fairness surface exists; real TierMem/public-baseline path is pending",
            "n_sweep_restored_to_0_1_2_4_8_16": "partial: restored on the synthetic local proxy/statistics surface only",
            "five_seed_statistics": "pending: current local statistics use two seeds",
            "human_judge_kappa_reported": "pending",
            "multi_backbone_run": "pending",
            "full_conflict_unsafe_scale": "partial: local extension panels exist; real benchmark-grade live runs are pending",
            "no_rewrite_tiermem_integration": "pending: local policy scaffold exists but is not yet wired into the real TierMem path",
        },
        "legacy_release_snapshot": release_snapshot,
        "hygiene_summary": {
            "absolute_path_leak_files": len(hygiene.get("absolute_path_leaks", [])),
            "outputs_file_count": hygiene.get("outputs_inventory", {}).get("file_count"),
            "outputs_total_bytes": hygiene.get("outputs_inventory", {}).get("total_bytes"),
        },
    }
    return payload


def write_outputs(repo_root: Path, payload: dict[str, Any]) -> None:
    outputs_dir = repo_root / "outputs"
    state_dir = repo_root / "state"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    json_path = outputs_dir / "v3_transition_status.json"
    md_path = outputs_dir / "v3_transition_status.md"
    state_path = state_dir / "v3_transition_snapshot.json"

    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    json_path.write_text(text, encoding="utf-8")
    state_path.write_text(text, encoding="utf-8")

    completed = payload["completed_now"]
    pending = payload["still_pending_for_full_v3"]
    pending_notes = payload["full_v3_progress_notes"]
    week0 = payload["week0_gate"]
    scaffolds = payload["v3_scaffolds_now"]
    lines = [
        "# V3 Transition Status",
        "",
        f"Date: {payload['generated_on']}",
        "",
        "## Identity",
        "",
        f"- repo role: `{payload['current_identity']['repo_role']}`",
        f"- path decision: {payload['current_identity']['path_decision']}",
        f"- legacy demotion: {payload['current_identity']['legacy_demoted_to']}",
        "",
        "## Completed Now",
        "",
    ]
    for key, value in completed.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Week-0 Gate", ""])
    for key, value in week0.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Execution Order", ""])
    for key, value in payload["execution_order"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## V3 Scaffolds Now", ""])
    for key, value in scaffolds.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Still Pending For Full V3", ""])
    for key, value in pending.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Pending Notes", ""])
    for key, value in pending_notes.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The repo is no longer describing PSU as the final paper contribution.",
            "- The V3 transition now has explicit feasibility, HaluMem dataset preflight, official-eval runtime scaffold audit, public-baseline readiness, synthetic no-rewrite dry-run, fairness-paired local comparison, paired statistics, Pareto, capability, hygiene, and legacy-migration documents.",
            "- The local proxy surface now separates what query awareness explains from what the no-rewrite rule explains, but that decomposition is still synthetic and is not wired into the real TierMem path.",
            "- E0 is still the controlling gate: defense-side dry-run artifacts should not be elevated above the not-yet-passed real sanity run.",
            "- Full V3 completion still requires real public baseline execution, fairness-paired summary baselines, larger conflict/unsafe scale, human judge validation, and multi-backbone evidence.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[v3-transition] wrote {json_path}")
    print(f"[v3-transition] wrote {md_path}")
    print(f"[v3-transition] wrote {state_path}")


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    payload = build_payload(repo_root)
    write_outputs(repo_root, payload)


if __name__ == "__main__":
    main()
