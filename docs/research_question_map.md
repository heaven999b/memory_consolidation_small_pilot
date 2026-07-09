# Research Question Map

This file is the code-oriented map for the repository.

It answers four practical questions:

1. which files implement each research question
2. whether the surface uses official benchmark data, self-built data, or both
3. what the main entry script is
4. which parts are complete versus still exploratory

## Original RQ1 to RQ5

| RQ | Topic | Main scripts | Main data surface | Status |
| --- | --- | --- | --- | --- |
| RQ1 | safety retention or amplification under consolidation | `scripts/run/run_rq1_safety_consolidation.py`, `scripts/run/run_rq1_safety_judge.py`, `scripts/run/run_rq1_safety_rescore.py`, `scripts/run/run_rq1_agentpoison_overlay.py`, `scripts/run/run_rq1_agentpoison_locomo.py`, `scripts/run/run_rq1_authority_experiment.py` | self-built safety suites in `benchmarks/safety/`, plus selected LoCoMo and AgentPoison-style overlays | active |
| RQ2 | fabricated memory or hallucination after consolidation | `scripts/run/run_rq2_factual_poison.py`, `scripts/run/rq2_fixed.py`, `scripts/analysis/analyze_rq2_tiermem_completed_pass.py`, `scripts/analysis/rescore_rq2_selfbuilt_reports.py` | official HaluMem-derived slices plus self-built local-dialogue suites in `configs/` | active |
| RQ3 | provenance-aware defenses | `scripts/run/run_rq3_provenance_clean.py`, `scripts/run/run_rq3_readtime_defense_matrix.py`, `scripts/analysis/extract_rq3_stubborn_partial_results.py`, `scripts/analysis/summarize_rq3_readtime_defense_matrix.py` | official-style question surfaces plus safety mini-suites in `benchmarks/safety/` | active |
| RQ4 | which consolidation operator is most fragile | `scripts/run/run_branch_comedy_control.py`, `scripts/run/run_branch_emem_control.py` | same RQ1 or RQ2 tasks reused under alternative operator-style controls | partial |
| RQ5 | where failure happens in the pipeline | `scripts/run/run_rq_know_vs_do.py`, `scripts/run/run_v2_tiermem_micro_failure_mode_judge.py`, `scripts/run/run_rq3_provenance_clean.py` | mixed: self-built policy or dialogue cases and read-time probes | active |

## Reframed Questions

These are not separate repos. They are additional layers inside the same workspace.

| Reframed line | Purpose | Main scripts |
| --- | --- | --- |
| know-do gap | distinguish knowing the rule from following the rule | `scripts/run/run_rq_know_vs_do.py` |
| factual resistance | test whether repeated memory pressure implants false beliefs | `scripts/run/run_rq2_factual_poison.py` |
| read-time defense | test whether provenance or trust controls help at answer time | `scripts/run/run_rq3_provenance_clean.py`, `scripts/run/run_rq3_readtime_defense_matrix.py` |
| evaluation reliability | check whether lexical endpoints disagree with judge-based scoring | `scripts/run/run_rq1_safety_rescore.py`, `scripts/core/kappa_score.py`, `scripts/analysis/export_kappa.py`, `scripts/core/fix_toolkit.py` |

## Official Benchmark Surfaces

These are the main benchmark-backed surfaces in the repo.

- `benchmarks/halumem`
- `benchmarks/locomo`
- `benchmarks/longmemeval`
- `scripts/run/run_v2_tiermem_local_bridge.py`
- `benchmarks/halumem/official_repo/eval/llms.py`

Notes:

- HaluMem is used for the hallucination-style track.
- LoCoMo and LongMemEval are used for longer-context or memory retrieval surfaces.
- The TierMem bridge is the place where local execution, routing mode, page-write mode, and consolidation passes are wired together.

## Self-Built Surfaces

These are the main self-built code and dataset surfaces.

### Safety suites

- `benchmarks/safety/unsafe_seed_suite_v1.json`
- `benchmarks/safety/stealthy_poison_suite_v1.json`
- `benchmarks/safety/agentpoison_trigger_suite_v1.json`
- `benchmarks/safety/rq3_stubborn_failures_mini_suite_v1.json`

### RQ2 local-dialogue suites

- `configs/rq2_selfbuilt_suite_v3_domain_diverse.json`
- `configs/rq2_selfbuilt_suite_v4_domain_diverse_extra.json`
- `configs/rq2_selfbuilt_suite_v5_domain_diverse_local_dialogue.json`
- `configs/rq2_selfbuilt_suite_v6_domain_diverse_local_dialogue_100.json`

### Suite builders

- `scripts/build/build_rq2_local_dialogue_suite_v6.py`
- `scripts/build/build_rq2_selfbuilt_packet.py`
- `scripts/build/build_rq2_suite_catalog_zh.py`
- `scripts/build/build_rq2_manual_annotation_zh.py`
- `scripts/build/build_rq2_manual_annotation_core_zh.py`
- `scripts/build/build_rq2_manual_annotation_diverse_zh.py`

## Framework And Shared Utilities

These files are not tied to a single RQ and support the whole repo.

- `scripts/run/run_v2_tiermem_local_bridge.py`
- `scripts/core/week1_surface.py`
- `scripts/core/pilot_core.py`
- `scripts/core/artifact_contract.py`
- `scripts/core/curated_dataset.py`
- `scripts/core/benchmark_native_runtime.py`
- `scripts/core/safety_metrics.py`
- `scripts/core/safety_honest_metrics.py`
- `scripts/core/safety_write_filter.py`
- `scripts/core/fix_toolkit.py`
- `scripts/core/kappa_score.py`
- `scripts/analysis/export_kappa.py`
- `scripts/analysis/gen_kappa_html.py`

## Archived Legacy Surfaces

The repository keeps older benchmark-native, PSU, expanded-benchmark, and V3-transition runners under:

- `archive/legacy_baselines/`
- `archive/spikes/`

These are retained for continuity, but they are no longer the main entry surface for current RQ reporting.

## Report And Dashboard Generators

These are code files that generate research-facing artifacts.

- `scripts/build/build_rq3_readtime_dashboard_data.py`
- `scripts/watch/watch_rq3_readtime_dashboard_data.py`
- `scripts/tooling/reporting/make_technical_status_docx_20260709.py`
- `scripts/tooling/reporting/make_speaker_cheatsheet_docx_20260709.py`
- `scripts/tooling/reporting/make_technical_status_ppt_20260709.mjs`
- `scripts/tooling/reporting/gen_report_ascii.py`
- `scripts/tooling/reporting/gen_report_full.py`
- `scripts/tooling/reporting/gen_research_report.py`
- `scripts/tooling/reporting/gen_paper.py`

## Reader-Facing Weekly Reports

- `weekly_reports/README.md`
- `weekly_reports/week1/README.md`
- `weekly_reports/week1/week1_report_20260709_en.md`

These are short external-facing progress summaries rather than internal state logs.

## Round-Specific Viewing Guides

- `docs/HOW_TO_VIEW_ROUND_RESULTS_20260709.md`

This is the fastest “what file should I open and how should I read it?” guide for someone who did not participate in the run.

## Suggested Entry Order For New Readers

1. `README.md`
2. `RESEARCH_README.md`
3. `scripts/run/run_v2_tiermem_local_bridge.py`
4. the `scripts/run/run_rq*.py` file for the question you care about
5. the matching config or benchmark directory

## Gaps To Keep In Mind

- `RQ4` is still partial rather than a full apples-to-apples operator family benchmark.
- Some older files remain as exploratory history and should not be read as final evidence.
- Many generated `docs/state/` and `outputs/` artifacts are local analysis surfaces, while the files listed above are the main code surface.
