# Modification Log Summary

## V3 Transition Pass: `2026-06-30`

- Reframed the repo as a **V3 transition workspace** rather than a PSU-final paper repo.
- Rewrote [README.md](./README.md) so TierMem is the locked primary base and PSU is explicitly demoted to a legacy baseline.
- Added [feasibility_report.md](./feasibility_report.md) plus [run_v3_feasibility_gate.py](./run_v3_feasibility_gate.py); the repo now has a first-class Week-0 gate document instead of only scattered notes.
- Added [legacy_pilot_findings.md](./legacy_pilot_findings.md) so the benchmark loaders, metric lineage, artifact infra, and failure-mode taxonomy are explicitly carried forward while tuned PSU win numbers are explicitly retired as final evidence.
- Added [state/v3_alignment_master_checklist.md](./state/v3_alignment_master_checklist.md) so V3 structural progress and still-pending experimental blockers are tracked in one place.
- Added [run_v3_public_baseline_readiness.py](./run_v3_public_baseline_readiness.py) plus [outputs/v3_public_baseline_readiness.md](./outputs/v3_public_baseline_readiness.md), so the demanded Mem0 / Zep / MemOS comparison surface now has a concrete local readiness audit instead of being only a TODO line.
- Added [.env.v3.example](./.env.v3.example), [.env.official_eval.example](./.env.official_eval.example), and [requirements-official-eval-base.txt](./requirements-official-eval-base.txt), so the V3 path now has explicit config scaffolds for the TierMem bridge and the mirrored HaluMem official eval runtime.
- Added [run_v3_halumem_dataset_preflight.py](./run_v3_halumem_dataset_preflight.py) plus [outputs/v3_halumem_dataset_preflight.md](./outputs/v3_halumem_dataset_preflight.md), so the canonical `HaluMem-Medium.jsonl` path and official Hugging Face source are now checked directly instead of being buried in prose.
- Added [run_v3_official_eval_runtime_audit.py](./run_v3_official_eval_runtime_audit.py) plus [outputs/v3_official_eval_runtime_audit.md](./outputs/v3_official_eval_runtime_audit.md), so the HaluMem official eval path now has a dedicated runtime audit that separates common imports, baseline-specific imports, and dataset blockers.
- Extended [run_v2_tiermem_local_bridge.py](./run_v2_tiermem_local_bridge.py) with `--pre-api-smoke`, so the TierMem path can now exercise dataset-loader plus `LinkedViewSystem` init/reset before spending real API budget.
- Added [v3_no_rewrite_policy.py](./v3_no_rewrite_policy.py) plus [run_v3_no_rewrite_policy_audit.py](./run_v3_no_rewrite_policy_audit.py), so the V3 defended mechanism now exists as code and a local dry-run artifact instead of only as plan wording.
- Added [run_v3_no_rewrite_comparison.py](./run_v3_no_rewrite_comparison.py) plus [outputs/v3_no_rewrite_comparison.md](./outputs/v3_no_rewrite_comparison.md), so the V3 defended mechanism is now compared directly against `summary_only` / `tiered` over the expanded manifest-backed pool rather than only audited in isolation.
- Added a fairness-paired `summary_query_aware` comparison surface, plus [run_v3_no_rewrite_statistics.py](./run_v3_no_rewrite_statistics.py) and [run_v3_no_rewrite_pareto.py](./run_v3_no_rewrite_pareto.py), so the local V3 evidence now shows what query awareness alone buys, what the `no-rewrite` mechanism adds beyond that, and what the proxy cost tradeoff looks like.
- Added [run_v3_local_evidence_packet.py](./run_v3_local_evidence_packet.py) plus [outputs/v3_local_evidence_packet.md](./outputs/v3_local_evidence_packet.md), so the repo now has a compact one-page local evidence packet rather than only a growing pile of intermediate artifacts.
- Added [run_v3_local_capability_matrix.py](./run_v3_local_capability_matrix.py) plus [outputs/v3_local_capability_matrix.md](./outputs/v3_local_capability_matrix.md), so the repo now explicitly says which V3 steps this Mac can execute now and which remain blocked by data, credentials, or missing upstream artifacts.
- Added [run_v3_hygiene_audit.py](./run_v3_hygiene_audit.py) and [outputs/v3_hygiene_audit.md](./outputs/v3_hygiene_audit.md) so absolute-path leaks and the current outputs-surface size are now auditable.
- Added [run_v3_transition_status.py](./run_v3_transition_status.py), [outputs/v3_transition_status.md](./outputs/v3_transition_status.md), and [state/v3_transition_snapshot.json](./state/v3_transition_snapshot.json) so the repo's V3 identity and remaining blockers are serialized.
- Added [run_v3_transition_rebuild.py](./run_v3_transition_rebuild.py) as a one-command refresh path for the full V3 status surface, including feasibility, public-baseline readiness, no-rewrite dry-run, capability, hygiene, and transition snapshots.

## Release Snapshot: `v0.2.0-idea-baseline-private`

- Promoted the primary baseline surface from a local proxy presentation layer to a benchmark-native primary base.
- Froze both a benchmark-first proxy base and a benchmark-native primary base as reviewer-facing artifacts.
- Rebuilt the paper baseline packet so all current `must` gates pass except the scale-related paper-level gate.
- Explicitly demoted synthetic-reference artifacts to support-only status in the main reviewer sequence.
- Prepared the repository for private GitHub publication by excluding raw mirrored benchmark corpora and local cache directories from version control.

## Maintenance Pass: `2026-06-28`

- Added a stable helper alias `build_curated_dataset()` in [curated_dataset.py](./curated_dataset.py) so quick audits and external scripts can inspect the 58-item synthetic dataset without guessing the builder name.
- Added [REPO_REVIEW_AND_TABLE_ANALYSIS.md](./REPO_REVIEW_AND_TABLE_ANALYSIS.md) to summarize remaining issues, reviewer-facing weaknesses, and the meaning of the current tables.
- Updated [README.md](./README.md) so the release snapshot section also points to the simple modification log and the new review-and-analysis report.
- Added frozen manifest-backed task extensions for `conflict` and `unsafe`, plus [run_task_extension_section.py](./run_task_extension_section.py), so task-family coverage no longer stops at `benign` / `hallucination`.
- Added [requirements.txt](./requirements.txt), [environment.yml](./environment.yml), and [REPRODUCIBILITY.md](./REPRODUCIBILITY.md) so the release environment is explicitly pinned.
- Added [run_release_rebuild.py](./run_release_rebuild.py) so the reviewer-facing packet can be rebuilt from one entrypoint with the intended multi-seed configuration preserved.
- Added [outputs/provenance_scaffolded_method_report.md](./outputs/provenance_scaffolded_method_report.md) so the current best scaffold / provenance / note-aware chain is no longer just a sequence of rounds, but a formal method object (`PSU`).
- Added [outputs/paper_strengthening_stats.md](./outputs/paper_strengthening_stats.md) so key reviewer-facing comparisons now have paired-bootstrap deltas and `metric-vs-N` slope readouts instead of only point estimates.
- Added [outputs/paper_artifact_contract_report.md](./outputs/paper_artifact_contract_report.md) plus [outputs/paper_artifact_contract_records.json](./outputs/paper_artifact_contract_records.json) so the primary model-backed panels now expose per-pass traces, provenance coverage, quarantine signals, and first-failing-stage attribution.
- Generalized [run_actual_carry_forward_round.py](./run_actual_carry_forward_round.py) so `tiny_carry_forward_scaffold` now preserves previously grounded query slots on benign/conflict collapse cases rather than only unsafe refusal scaffolds.
- Added [outputs/psu_recall_main_panel.md](./outputs/psu_recall_main_panel.md) so the baseline routing family, the no-carry PSU ablation, and final PSU now appear in one recall-facing paper table.
- Hardened [deepseek_memory_summarizer.py](./deepseek_memory_summarizer.py) and [run_actual_carry_forward_round.py](./run_actual_carry_forward_round.py) with attempt logs, timeout/error visibility, subset smoke controls, and resume/progress checkpoints so cold-cache multi-seed runs no longer fail silently.
- Rebuilt PSU on `seed11,23`; the current [outputs/psu_recall_main_panel.md](./outputs/psu_recall_main_panel.md) now shows `N=8` `PSU` at `accuracy=1.000`, `history_loss=0.062`, and `raw_escalation=0.042`.
- Expanded [artifact_contract.py](./artifact_contract.py) again with raw-context witness links for empty-output collapse cases; current audited coverage is now `1.000` / `0.986` / `0.938` / `1.000` across `actual_summarizer_slice`, `actual_recall_expansion`, `actual_hallucination_stress`, and `actual_carry_forward`.
- Added [outputs/psu_paper_packet.md](./outputs/psu_paper_packet.md) so the method definition, multi-seed PSU main panel, paired deltas, artifact coverage, and current 32-item benchmark section scale are visible in one paper-facing packet.
- Added [freeze_external_benchmark_expanded_slices.py](./freeze_external_benchmark_expanded_slices.py) so the mirrored official benchmark corpora now freeze into a larger next-stage pool rather than only the current 32-item reviewer section.
- Added [outputs/expanded_benchmark_dataset_inventory.md](./outputs/expanded_benchmark_dataset_inventory.md) plus [outputs/expanded_benchmark_dataset_inventory.json](./outputs/expanded_benchmark_dataset_inventory.json); the current expanded pool is `159` items total (`19` HaluMem, `80` LoCoMo, `60` LongMemEval) and passes runtime projection validation `159/159`.
- Updated the expanded manifests to carry explicit `evaluation_stratum` / `complexity_band` metadata and added [outputs/expanded_benchmark_rigor_audit.md](./outputs/expanded_benchmark_rigor_audit.md), which now says the pool is standardized and staged-run ready, but not yet final-paper ready.
- Added [run_expanded_benchmark_staged.py](./run_expanded_benchmark_staged.py) and actually ran [outputs/expanded_benchmark_stage_smoke.md](./outputs/expanded_benchmark_stage_smoke.md) plus [outputs/expanded_benchmark_stage_medium.md](./outputs/expanded_benchmark_stage_medium.md), so the expanded official pool is no longer only “ready to run” in principle.
- Re-ran [outputs/expanded_benchmark_stage_medium.md](./outputs/expanded_benchmark_stage_medium.md) on `seed11,23`, patched [pilot_core.py](./pilot_core.py) so only the `unsafe` task family hard-triggers policy refusal, and added [outputs/expanded_benchmark_stage_medium_analysis.md](./outputs/expanded_benchmark_stage_medium_analysis.md); the immediate effect is that `scale_aware_unified` / `scale_aware_note_aware` no longer over-refuse on the two previously failing benign LoCoMo cases and now hold staged benign `N=8` accuracy at `1.000` while keeping staged hallucination false-present at `0.000`.

## One-Line Interpretation

- This repo is now cleanly versioned and reviewer-credible for idea reporting.
- It is not yet paper-ready mainly because the full large benchmark baseline still has to be run, but the old dataset-construction blocker is now much smaller: the repo already freezes a `159`-item official benchmark pool and the remaining gap is pushing the real evaluation pipeline across it cleanly.
