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
| RQ1 | safety retention or amplification under consolidation | `run_rq1_safety_consolidation.py`, `run_rq1_safety_judge.py`, `run_rq1_safety_rescore.py`, `run_rq1_agentpoison_overlay.py`, `run_rq1_agentpoison_locomo.py`, `run_rq1_authority_experiment.py` | self-built safety suites in `benchmarks/safety/`, plus selected LoCoMo and AgentPoison-style overlays | active |
| RQ2 | fabricated memory or hallucination after consolidation | `run_rq2_factual_poison.py`, `rq2_fixed.py`, `analyze_rq2_tiermem_completed_pass.py`, `rescore_rq2_selfbuilt_reports.py` | official HaluMem-derived slices plus self-built local-dialogue suites in `configs/` | active |
| RQ3 | provenance-aware defenses | `run_rq3_provenance_clean.py`, `run_rq3_readtime_defense_matrix.py`, `extract_rq3_stubborn_partial_results.py`, `summarize_rq3_readtime_defense_matrix.py` | official-style question surfaces plus safety mini-suites in `benchmarks/safety/` | active |
| RQ4 | which consolidation operator is most fragile | `run_branch_comedy_control.py`, `run_branch_emem_control.py` | same RQ1 or RQ2 tasks reused under alternative operator-style controls | partial |
| RQ5 | where failure happens in the pipeline | `run_rq_know_vs_do.py`, `run_v2_tiermem_micro_failure_mode_judge.py`, `run_rq3_provenance_clean.py` | mixed: self-built policy or dialogue cases and read-time probes | active |

## Reframed Questions

These are not separate repos. They are additional layers inside the same workspace.

| Reframed line | Purpose | Main scripts |
| --- | --- | --- |
| know-do gap | distinguish knowing the rule from following the rule | `run_rq_know_vs_do.py` |
| factual resistance | test whether repeated memory pressure implants false beliefs | `run_rq2_factual_poison.py` |
| read-time defense | test whether provenance or trust controls help at answer time | `run_rq3_provenance_clean.py`, `run_rq3_readtime_defense_matrix.py` |
| evaluation reliability | check whether lexical endpoints disagree with judge-based scoring | `run_rq1_safety_rescore.py`, `kappa_score.py`, `export_kappa.py`, `fix_toolkit.py` |

## Official Benchmark Surfaces

These are the main benchmark-backed surfaces in the repo.

- `benchmarks/halumem`
- `benchmarks/locomo`
- `benchmarks/longmemeval`
- `run_v2_tiermem_local_bridge.py`
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

- `build_rq2_local_dialogue_suite_v6.py`
- `build_rq2_selfbuilt_packet.py`
- `build_rq2_suite_catalog_zh.py`
- `build_rq2_manual_annotation_zh.py`
- `build_rq2_manual_annotation_core_zh.py`
- `build_rq2_manual_annotation_diverse_zh.py`

## Framework And Shared Utilities

These files are not tied to a single RQ and support the whole repo.

- `run_v2_tiermem_local_bridge.py`
- `week1_surface.py`
- `pilot_core.py`
- `artifact_contract.py`
- `curated_dataset.py`
- `benchmark_native_runtime.py`
- `safety_metrics.py`
- `safety_honest_metrics.py`
- `safety_write_filter.py`
- `fix_toolkit.py`
- `kappa_score.py`
- `export_kappa.py`
- `gen_kappa_html.py`

## Report And Dashboard Generators

These are code files that generate research-facing artifacts.

- `build_rq3_readtime_dashboard_data.py`
- `watch_rq3_readtime_dashboard_data.py`
- `make_technical_status_docx_20260709.py`
- `make_speaker_cheatsheet_docx_20260709.py`
- `make_technical_status_ppt_20260709.mjs`
- `gen_report_ascii.py`
- `gen_report_full.py`
- `gen_research_report.py`
- `gen_paper.py`

## Suggested Entry Order For New Readers

1. `README.md`
2. `RESEARCH_README.md`
3. `run_v2_tiermem_local_bridge.py`
4. the `run_rq*.py` file for the question you care about
5. the matching config or benchmark directory

## Gaps To Keep In Mind

- `RQ4` is still partial rather than a full apples-to-apples operator family benchmark.
- Some older files remain as exploratory history and should not be read as final evidence.
- Many generated `state/` and `outputs/` artifacts are local analysis surfaces, while the files listed above are the main code surface.
