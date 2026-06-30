# V3 Transition Status

Date: 2026-06-30

## Identity

- repo role: `V3 transition workspace`
- path decision: Path A locked: TierMem is the primary base and harness.
- legacy demotion: PSU and the prior proxy stack are retained as baselines plus appendix-style prior exploration.

## Completed Now

- tiermem_bridge_present: `True`
- v3_feasibility_gate_present: `True`
- v3_attack_suite_grounding_audit_present: `True`
- v3_halumem_dataset_preflight_present: `True`
- v3_public_baseline_readiness_present: `True`
- v3_official_eval_runtime_audit_present: `True`
- v3_no_rewrite_policy_audit_present: `True`
- v3_no_rewrite_comparison_present: `True`
- v3_no_rewrite_statistics_present: `True`
- v3_no_rewrite_pareto_present: `True`
- v3_local_capability_matrix_present: `True`
- v3_local_evidence_packet_present: `True`
- legacy_pilot_findings_present: `True`
- v3_alignment_checklist_present: `True`
- v3_hygiene_audit_present: `True`
- legacy_release_rebuild_retained: `True`
- v3_env_template_present: `True`
- official_eval_env_template_present: `True`
- official_eval_base_requirements_present: `True`

## Week-0 Gate

- tiermem_usable: `partial`
- halumem_usable: `partial`
- agentpoison_usable: `partial`
- mpbench_memevobench: `partial`
- citation_reality: `partial`
- license_compatibility: `partial`

## Execution Order

- e0_real_sanity_gate_passed: `False`
- e0_rule: `Do not treat defense comparisons as paper evidence before the real TierMem/HaluMem E0 sanity gate passes.`

## V3 Scaffolds Now

- public_baseline_readiness: `partial`
- agentpoison_grounding_status: `partial`
- memevobench_grounding_status: `partial`
- mpbench_grounding_status: `missing`
- halumem_dataset_status: `ready`
- halumem_expected_dataset_present: `True`
- halumem_candidate_count: `1`
- official_eval_runtime_status: `partial`
- official_eval_ready_runtime_count: `1`
- official_eval_venv_present: `False`
- no_rewrite_policy_scaffold: `partial`
- no_rewrite_n8_blocked_protected_case_rate: `0.9783`
- no_rewrite_comparison_present: `True`
- no_rewrite_comparison_items: `185`
- local_n_sweep_values: `[0, 1, 2, 4, 8, 16]`
- local_seed_values: `[11, 23]`
- local_architecture_count: `7`
- local_query_aware_fairness_surface_present: `True`
- local_no_rewrite_mechanism_surface_present: `True`
- no_rewrite_statistics_rows: `72`
- no_rewrite_surface_evidence_class: `synthetic_dry_run`
- no_rewrite_surface_paper_safe: `False`
- no_rewrite_pareto_sections: `2`
- local_evidence_packet_present: `True`
- local_capability_yes_count: `8`
- local_capability_partial_count: `4`
- tiermem_pre_api_smoke_supported: `True`

## Still Pending For Full V3

- e0_real_sanity_gate: `True`
- real_public_baselines_run: `False`
- query_blind_vs_query_aware_fairness_pair: `False`
- n_sweep_restored_to_0_1_2_4_8_16: `False`
- five_seed_statistics: `False`
- human_judge_kappa_reported: `False`
- multi_backbone_run: `False`
- full_conflict_unsafe_scale: `False`
- no_rewrite_tiermem_integration: `False`

## Pending Notes

- e0_real_sanity_gate: pending: TierMem and HaluMem are still not both running end-to-end with real credentials and real benchmark files
- real_public_baselines_run: pending: only readiness audit is complete locally
- halumem_medium_dataset_in_place: ready: preflight and canonical path are defined, and the final HaluMem-Medium.jsonl file is now present locally
- official_eval_runtime_scaffold: partial: templates and base requirements are present, but .venv_official_eval is not created yet
- query_blind_vs_query_aware_fairness_pair: partial: local proxy fairness surface exists; real TierMem/public-baseline path is pending
- n_sweep_restored_to_0_1_2_4_8_16: partial: restored on the synthetic local proxy/statistics surface only
- five_seed_statistics: pending: current local statistics use two seeds
- human_judge_kappa_reported: pending
- multi_backbone_run: pending
- full_conflict_unsafe_scale: partial: local extension panels exist; real benchmark-grade live runs are pending
- no_rewrite_tiermem_integration: pending: local policy scaffold exists but is not yet wired into the real TierMem path

## Interpretation

- The repo is no longer describing PSU as the final paper contribution.
- The V3 transition now has explicit feasibility, HaluMem dataset preflight, official-eval runtime scaffold audit, public-baseline readiness, synthetic no-rewrite dry-run, fairness-paired local comparison, paired statistics, Pareto, capability, hygiene, and legacy-migration documents.
- The local proxy surface now separates what query awareness explains from what the no-rewrite rule explains, but that decomposition is still synthetic and is not wired into the real TierMem path.
- E0 is still the controlling gate: defense-side dry-run artifacts should not be elevated above the not-yet-passed real sanity run.
- Full V3 completion still requires real public baseline execution, fairness-paired summary baselines, larger conflict/unsafe scale, human judge validation, and multi-backbone evidence.
