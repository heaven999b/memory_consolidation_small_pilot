# Memory Consolidation Small Pilot

This repository is the working codebase for a memory-agent research project on:

- iterative memory consolidation
- safety retention vs. attenuation under repeated compression
- fabricated memory and hallucination
- provenance-aware read-time defenses
- evaluation reliability for agent safety claims

The project now contains both the original `RQ1` to `RQ5` surfaces and the later reframed lines of work such as `know-do gap`, `read-time failure analysis`, and `judge reliability`.

## Current Status

This repo keeps the real research state, including negative results.

- Several original hypotheses were weakened or rejected after cleaner reruns.
- The repo therefore contains both exploratory scripts and cleaner retest pipelines.
- The most up-to-date plain-language research summary is in [RESEARCH_README.md](./RESEARCH_README.md).

If you want the short version: this is no longer just a "compression makes things worse" repo. It is also a repo about how memory-agent safety claims can flip when the endpoint, judge, or read-time protocol changes.

## What Is In This Repo

### Repository Layout

- `benchmarks/`, `configs/`: benchmark inputs, env templates, and schemas
- `weekly_reports/`: reader-facing weekly updates
- `docs/status/`: historical status notes, changelog-style summaries, reproducibility notes
- `docs/handoffs/`: handoff packets for new collaborators
- `docs/state/`, `docs/reviews/`: internal state logs and verification notes
- `docs/study/`: background reading and method notes
- `docs/bundles/`: generated code bundles and shareable packaged artifacts
- `scripts/`: active code surface split into `run`, `build`, `freeze`, `analysis`, `core`, and `tooling`
- `archive/spikes/`: exploratory spike and one-off analysis scripts
- `archive/legacy_baselines/`: older PSU / V3 / expanded-benchmark runners retained for history

This cleanup pass moves almost all executable code out of the repo root so the GitHub landing page stays clean, while still keeping the current research surface easy to find.

### 1. Core experimental runners

- `scripts/run/run_rq1_safety_consolidation.py`
- `scripts/run/run_rq1_authority_experiment.py`
- `scripts/run/run_rq1_agentpoison_overlay.py`
- `scripts/run/run_rq2_factual_poison.py`
- `scripts/run/run_rq3_provenance_clean.py`
- `scripts/run/run_rq3_readtime_defense_matrix.py`
- `scripts/run/run_rq_know_vs_do.py`

These are the main experiment entry points for the current research questions.

Older benchmark-native, PSU, V3-transition, and expanded-baseline runners now live under `archive/legacy_baselines/`.

### 2. TierMem-based execution bridge

- [scripts/run/run_v2_tiermem_local_bridge.py](./scripts/run/run_v2_tiermem_local_bridge.py)
- [scripts/core/week1_surface.py](./scripts/core/week1_surface.py)
- local TierMem source: `../tiermem_upstream`

This bridge is the main implementation surface for running official and semi-official memory benchmarks on a local machine.

### 3. Benchmarks and suites

- official or official-derived slices:
  - `benchmarks/halumem`
  - `benchmarks/locomo`
  - `benchmarks/longmemeval`
- self-built safety suites:
  - `benchmarks/safety/unsafe_seed_suite_v1.json`
  - `benchmarks/safety/stealthy_poison_suite_v1.json`
  - `benchmarks/safety/agentpoison_trigger_suite_v1.json`
- small sanity surface:
  - `benchmarks/tiny_synth/data/week1_tiny_synth.json`

### 4. Supporting code

- metrics and rescoring:
  - `scripts/core/safety_metrics.py`
  - `scripts/core/safety_honest_metrics.py`
  - `scripts/run/run_rq1_safety_judge.py`
  - `scripts/run/run_rq1_safety_rescore.py`
  - `scripts/core/kappa_score.py`
  - `scripts/analysis/export_kappa.py`
- suite builders:
  - `scripts/build/build_rq2_local_dialogue_suite_v6.py`
  - `scripts/build/build_rq2_manual_annotation_zh.py`
  - `scripts/build/build_rq2_manual_annotation_diverse_zh.py`
  - `scripts/build/build_rq2_suite_catalog_zh.py`
- dashboards and reports:
  - `scripts/build/build_rq3_readtime_dashboard_data.py`
  - `scripts/tooling/reporting/make_technical_status_docx_20260709.py`
  - `scripts/tooling/reporting/make_technical_status_ppt_20260709.mjs`

### 5. Documentation

- [RESEARCH_README.md](./RESEARCH_README.md): current research conclusions and caveats
- [docs/status/reproducibility.md](./docs/status/reproducibility.md): environment and rerun notes
- [docs/research_question_map.md](./docs/research_question_map.md): where each RQ lives in code
- [docs/operator_branches.md](./docs/operator_branches.md): comparison branches for alternative memory-management styles
- [weekly_reports/README.md](./weekly_reports/README.md): reader-facing weekly reports

## Research Question Map

The repo now mixes two layers:

1. the original `RQ1` to `RQ5` program
2. the later reframed questions that emerged after failure analysis

Use [docs/research_question_map.md](./docs/research_question_map.md) as the code index for:

- which scripts belong to each RQ
- which runs are benchmark-backed vs. self-built
- where the main data builders live
- which surfaces are complete, partial, or still missing

## Quick Start

```bash
cd "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
set -a && source .env.v3 && set +a
```

Common entry points:

```bash
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_local_bridge.py --check-only --benchmark locomo
.venv_tiermem_v2/bin/python scripts/run/run_rq_know_vs_do.py --endpoint judge --report-id knowdo_none
.venv_tiermem_v2/bin/python scripts/run/run_rq2_factual_poison.py --repetition 3
.venv_tiermem_v2/bin/python scripts/run/run_rq3_provenance_clean.py --help
```

## Notes On Scope

- Environment files such as `.env.v3` are intentionally not versioned.
- Large generated outputs, local caches, and presentation artifacts are not the main Git surface.
- Some benchmark corpora are mirrored locally, but large raw benchmark dumps are intentionally excluded from version control.

## Recommended Reading Order

1. [RESEARCH_README.md](./RESEARCH_README.md)
2. [docs/research_question_map.md](./docs/research_question_map.md)
3. [docs/status/reproducibility.md](./docs/status/reproducibility.md)

That order gives you the current claims, the code entry points, and then the rerun instructions.
