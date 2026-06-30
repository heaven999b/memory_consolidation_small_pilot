# Changelog

## v0.3.0-v3-transition - 2026-06-30

- Repositioned the repository as a **V3 transition workspace** instead of a PSU-final paper repo.
- Rewrote [README.md](./README.md) so TierMem is now the locked primary base and the older proxy stack is explicitly demoted to baseline + prior exploration.
- Added [feasibility_report.md](./feasibility_report.md) as the Week-0 V3 gate document required by the revised plan.
- Added [legacy_pilot_findings.md](./legacy_pilot_findings.md) to document exactly what transfers from the older 37-iteration pilot and what does not.
- Added [state/v3_alignment_master_checklist.md](./state/v3_alignment_master_checklist.md) to track which V3 requirements are already structurally satisfied and which are still experimental blockers.
- Added [run_v3_feasibility_gate.py](./run_v3_feasibility_gate.py), [run_v3_public_baseline_readiness.py](./run_v3_public_baseline_readiness.py), [run_v3_no_rewrite_policy_audit.py](./run_v3_no_rewrite_policy_audit.py), [run_v3_no_rewrite_comparison.py](./run_v3_no_rewrite_comparison.py), [run_v3_no_rewrite_statistics.py](./run_v3_no_rewrite_statistics.py), [run_v3_no_rewrite_pareto.py](./run_v3_no_rewrite_pareto.py), [run_v3_local_capability_matrix.py](./run_v3_local_capability_matrix.py), [run_v3_local_evidence_packet.py](./run_v3_local_evidence_packet.py), [run_v3_hygiene_audit.py](./run_v3_hygiene_audit.py), [run_v3_transition_status.py](./run_v3_transition_status.py), and [run_v3_transition_rebuild.py](./run_v3_transition_rebuild.py) so the V3 migration state can be regenerated from code rather than tracked only as ad hoc notes.
- Added [.env.v3.example](./.env.v3.example), [.env.official_eval.example](./.env.official_eval.example), and [requirements-official-eval-base.txt](./requirements-official-eval-base.txt) so the V3 path now has explicit local config scaffolds for the TierMem bridge and the mirrored HaluMem official eval path.
- Added [run_v3_halumem_dataset_preflight.py](./run_v3_halumem_dataset_preflight.py) plus [outputs/v3_halumem_dataset_preflight.md](./outputs/v3_halumem_dataset_preflight.md), so the canonical `HaluMem-Medium.jsonl` path, source URL, and absence/presence state are now checked explicitly.
- Added [run_v3_official_eval_runtime_audit.py](./run_v3_official_eval_runtime_audit.py) plus [outputs/v3_official_eval_runtime_audit.md](./outputs/v3_official_eval_runtime_audit.md), so the mirrored public-baseline path now has a dedicated runtime scaffold audit rather than only a coarse readiness note.
- Extended [run_v2_tiermem_local_bridge.py](./run_v2_tiermem_local_bridge.py) with `--pre-api-smoke`, so the bridge can now exercise dataset loading plus `LinkedViewSystem` init/reset without consuming live API budget.
- Added [v3_no_rewrite_policy.py](./v3_no_rewrite_policy.py) so the core V3 mechanism now exists as code rather than only as plan prose.
- Added [outputs/v3_no_rewrite_comparison.md](./outputs/v3_no_rewrite_comparison.md) so the V3 defended mechanism is now a directly comparable method surface over the expanded manifest-backed pool, not only a checklist or audit item.
- Added [outputs/v3_no_rewrite_statistics.md](./outputs/v3_no_rewrite_statistics.md), [outputs/v3_no_rewrite_pareto.md](./outputs/v3_no_rewrite_pareto.md), and [outputs/v3_local_evidence_packet.md](./outputs/v3_local_evidence_packet.md) so the local V3 evidence now includes paired significance, proxy cost tradeoffs, and a one-page status packet instead of only raw tables.
- Extended [.gitignore](./.gitignore) so `.venv_tiermem_v2/` stays out of version control.
- Updated [REPRODUCIBILITY.md](./REPRODUCIBILITY.md) so it now distinguishes the legacy pilot rebuild from the new V3 transition rebuild and documents the real TierMem bridge entrypoint.

## v0.2.0-idea-baseline-private - 2026-06-28

- Promoted the primary baseline surface from a local proxy presentation layer to a benchmark-native primary base.
- Froze a benchmark-first proxy base and benchmark-native primary base as reviewer-facing artifacts.
- Rebuilt the paper baseline packet so all `must` gates now pass.
- Left `paper_level_baseline_ready = false` because broader benchmark section scale is still only `32` frozen items.
- Demoted synthetic reference artifacts to explicit support-only status.
- Prepared the project for private GitHub publication by excluding raw mirrored benchmark corpora and local caches from version control.
- Added manifest-backed `conflict` / `unsafe` task-extension panels so the benchmark-native primary base now covers all four task families.
- Added pinned reproducibility files: `requirements.txt`, `environment.yml`, and `REPRODUCIBILITY.md`.
- Added `run_release_rebuild.py` so the current reviewer-facing release packet can be rebuilt from a single entrypoint with the intended multi-seed configuration.
- Formalized the best scaffold / hardening / carry-forward / note-aware lineage as `Provenance-Scaffolded Unified (PSU)`.
- Added `paper_strengthening_stats` and `paper_artifact_contract_report` so the repo now ships paired-bootstrap comparisons, slope readouts, per-pass artifact traces, provenance links, quarantine decisions, and stage attribution for the primary model-backed panels.
- Generalized `tiny_carry_forward_scaffold` from an unsafe-only preservation rule into a query-slot scaffold recovery rule that also protects benign/conflict target survival under repeated compression.
- Added `psu_recall_main_panel` so the recall-facing paper table now places `PSU` beside the baseline routing family and its nearest no-carry ablation on the same actual slice.
- Expanded the artifact contract so provenance coverage is now tracked through pass-level claim lineage, not only final retained claims; the audited primary model-backed panels now reach near-complete or complete provenance coverage.
- Hardened the model-backed execution path with summarizer attempt logging, timeout/error visibility, resume support, and partial progress checkpoints for the PSU carry-forward round.
- Promoted PSU to a stable multi-seed recall panel on `seed11,23`; at `N=8`, `PSU` now reaches `accuracy=1.000`, `history_loss=0.062`, and `raw_escalation=0.042` on the current paper-facing recall panel.
- Added `psu_paper_packet` and updated the release rebuild so the reviewer-facing packet now rebuilds the multi-seed PSU path rather than the old single-seed carry-forward stub.
- Added a larger official benchmark pool built from mirrored HaluMem, LoCoMo, and LongMemEval sources: the repo now freezes `159` benchmark-native items in expanded manifests, up from the current `32`-item reviewer section.
- Added `freeze_external_benchmark_expanded_slices.py` plus `outputs/expanded_benchmark_dataset_inventory.{json,md}` so the next-stage scale-up is documented, reproducible, and already validated against the benchmark-native runtime packet schema.
- Standardized the expanded pool into explicit contract-based strata and added `outputs/expanded_benchmark_rigor_audit.{json,md}` so the repo now records which layers are staging-ready, which strata are headline-worthy, and which slices should remain auxiliary.
- Added `run_expanded_benchmark_staged.py` and executed the first two staged artifacts: a fast `smoke` pass over `9` items and a broader `medium` pass over `18` items, both on the expanded official benchmark pool.
- Re-ran the expanded `medium` stage on `seed11,23`, patched the policy-refusal gate in `pilot_core.py`, and removed a benign over-refusal blocker: `scale_aware_unified` / `scale_aware_note_aware` now recover the previously failing `locomo_expanded_001/002` cases, hold `N=8` benign accuracy at `1.000`, and keep `N=8` hallucination false-present at `0.000` on the staged expanded pool.
