# Memory Consolidation Small Pilot

Current repository identity: `v0.3.0-v3-transition`

This repo is no longer framed as "the PSU paper repo." It is now a **V3 transition workspace** whose job is to move the project onto the execution-locked, TierMem-based path defined in `02_revised_plan_v3.md`.

## V3 Path Decision

The project has now locked **Path A**:

- **TierMem is the primary implementation base and evaluation harness.**
- The earlier self-built stack (`psu`, `scale_aware_unified`, the many micro-round fixes) is retained only as:
  - a **legacy baseline family**
  - a **prior-exploration appendix surface**
- The main contribution is no longer "PSU beats local baselines."
- The main contribution is now the narrower V3 claim:
  - **safety-critical fields should not be freely rewritten during iterative consolidation, and this must be enforced and tested inside a provenance-aware TierMem-style pipeline under repeated `C^N` compression and adversarial updates.**

## What This Repo Now Contains

### 1. V3 first-class transition documents

- [feasibility_report.md](./feasibility_report.md)
  - Week-0 feasibility gate required by V3
- [legacy_pilot_findings.md](./legacy_pilot_findings.md)
  - exact mapping of which legacy assets transfer and which do not
- [state/reviewer_blockers_clean.md](./state/reviewer_blockers_clean.md)
  - current clean blocker list and execution order
- [state/v3_alignment_master_checklist.md](./state/v3_alignment_master_checklist.md)
  - current V3 checklist with done / partial / pending status
- [outputs/v3_transition_status.md](./outputs/v3_transition_status.md)
  - current transition snapshot
- [outputs/v3_public_baseline_readiness.md](./outputs/v3_public_baseline_readiness.md)
  - local readiness audit for the official Mem0 / Zep / MemOS comparison surface
- [outputs/v3_attack_suite_grounding_audit.md](./outputs/v3_attack_suite_grounding_audit.md)
  - local grounding audit for AgentPoison / MPBench / MemEvoBench
- [outputs/v3_halumem_dataset_preflight.md](./outputs/v3_halumem_dataset_preflight.md)
  - canonical-path audit for `HaluMem-Medium.jsonl`
- [outputs/v3_official_eval_runtime_audit.md](./outputs/v3_official_eval_runtime_audit.md)
  - scaffold/runtime audit for the mirrored HaluMem official eval path
- [outputs/v3_no_rewrite_policy_audit.md](./outputs/v3_no_rewrite_policy_audit.md)
  - local synthetic dry-run instantiation of the V3 safety-critical no-rewrite rule
- [outputs/v3_no_rewrite_comparison.md](./outputs/v3_no_rewrite_comparison.md)
  - synthetic dry-run comparison table for `no-rewrite` versus `summary_only` / `tiered`
- [outputs/v3_no_rewrite_statistics.md](./outputs/v3_no_rewrite_statistics.md)
  - paired synthetic dry-run significance readout for blind vs query-aware vs no-rewrite
- [outputs/v3_no_rewrite_surface_audit.md](./outputs/v3_no_rewrite_surface_audit.md)
  - explicit audit showing why the no-rewrite surface must stay separate from real benchmark evidence
- [outputs/v3_no_rewrite_pareto.md](./outputs/v3_no_rewrite_pareto.md)
  - synthetic proxy cost/utility and cost/safety Pareto readout
- [outputs/v3_local_capability_matrix.md](./outputs/v3_local_capability_matrix.md)
  - what this Mac can execute now, what is blocked, and the next command for each V3 task
- [outputs/v3_local_evidence_packet.md](./outputs/v3_local_evidence_packet.md)
  - one-page local synthetic packet for the current V3 transition state
- [outputs/v3_hygiene_audit.md](./outputs/v3_hygiene_audit.md)
  - current absolute-path leak and outputs-surface audit

### 2. Real TierMem bridge work

- cloned TierMem upstream repo:
  - `../tiermem_upstream`
- local bridge script:
  - [run_v2_tiermem_local_bridge.py](./run_v2_tiermem_local_bridge.py)
- dedicated local environment:
  - `.venv_tiermem_v2/`
- official eval scaffold files:
  - `.env.v3.example`
  - `.env.official_eval.example`
  - `requirements-official-eval-base.txt`

This bridge is important because it already does three non-trivial V3 migration tasks:

- rewires TierMem dataset loaders to local benchmark mirrors
- uses local-path Qdrant mode instead of assuming an external Qdrant service
- redirects `mem0` local state into repo outputs instead of relying on `~/.mem0`

## Current Week-0 Gate Status

The current local state is:

- `TierMem usable`: `partial`
  - real code is cloned and the bridge runtime exists
  - LoCoMo and LongMemEval are now blocked mainly by `OPENAI_API_KEY`, not by missing code
- `HaluMem usable`: `partial`
  - local mirror and eval helpers exist
  - final `HaluMem-Medium.jsonl` expected by the TierMem loader is still missing
- `AgentPoison usable`: `paper_only`
  - not yet cloned locally
- `MPBench / MemEvoBench`: `paper_only`
  - not yet grounded by local artifacts

So the repo has moved from "local proxy-only baseline work" to "TierMem migration in progress," but it has **not** yet completed the full V3 experimental program.

Most importantly, the real `E0` sanity gate is still **not passed**. Any current `no-rewrite` artifacts must therefore be read as synthetic dry-run scaffolding, not as paper-grade defense evidence.

## What Transfers From The Legacy Pilot

The old repo work is not thrown away. It transfers in four high-value buckets:

- benchmark integration
  - mirrored HaluMem / LoCoMo / LongMemEval assets
  - frozen benchmark slices
  - benchmark-facing adapters and manifests
- metrics
  - `propagation`, `false_present`, `history_loss`, `raw_escalation`
- artifact infrastructure
  - `run_*` + `verify_*`
  - JSONL traces
  - monitors
  - packet-style markdown outputs
- failure-mode taxonomy
  - the many micro-rounds now serve as prior exploration and design motivation

What does **not** transfer as paper evidence:

- PSU headline win numbers from tuned in-sample small panels
- `scale_aware_unified` as a main system
- any claim that a DeepSeek-only tuned proxy stack is the final method

## Legacy Surface Still Present

The earlier reviewer-facing packet is still kept in this repo because it remains useful as a legacy baseline surface:

- [run_release_rebuild.py](./run_release_rebuild.py)
- [state/release_snapshot.json](./state/release_snapshot.json)
- [outputs/psu_paper_packet.md](./outputs/psu_paper_packet.md)

But these are now explicitly **legacy**:

- they show what the prior pilot already built
- they do **not** define the V3 paper contribution
- they should be read as migration assets and baselines, not the final system

## New V3 Entry Points

### V3 transition refresh

```bash
python3 run_v3_transition_rebuild.py
```

This rebuilds:

- `feasibility_report.md`
- `outputs/v3_feasibility_gate.json`
- `outputs/v3_halumem_dataset_preflight.{json,md}`
- `outputs/v3_public_baseline_readiness.{json,md}`
- `outputs/v3_official_eval_runtime_audit.{json,md}`
- `outputs/v3_no_rewrite_policy_audit.{json,md}`
- `outputs/v3_no_rewrite_comparison.{json,md}`
- `outputs/v3_no_rewrite_statistics.{json,md}`
- `outputs/v3_no_rewrite_surface_audit.{json,md}`
- `outputs/v3_no_rewrite_pareto.{json,md}`
- `outputs/v3_hygiene_audit.{json,md}`
- `outputs/v3_local_capability_matrix.{json,md}`
- `outputs/v3_local_evidence_packet.{json,md}`
- `outputs/v3_transition_status.{json,md}`
- `state/v3_transition_snapshot.json`

### Real TierMem local readiness

```bash
.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --check-only --benchmark locomo
```

### TierMem pre-API smoke

```bash
.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --pre-api-smoke --benchmark locomo
```

This exercises dataset-loader plus `LinkedViewSystem` init/reset without running a live benchmark pass.

### Tiny real TierMem sanity run

```bash
.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --benchmark locomo --limit 2
```

This last command still requires a valid `OPENAI_API_KEY`.

### Official public baseline readiness

```bash
python3 run_v3_public_baseline_readiness.py
```

### HaluMem dataset preflight

```bash
python3 run_v3_halumem_dataset_preflight.py
```

### Official eval runtime audit

```bash
python3 run_v3_official_eval_runtime_audit.py
```

### No-rewrite policy dry-run

```bash
python3 run_v3_no_rewrite_policy_audit.py
```

This is a synthetic dry-run over the legacy simulator, not a real TierMem benchmark.

### No-rewrite comparison table

```bash
python3 run_v3_no_rewrite_comparison.py
```

This is a synthetic dry-run comparison surface.

### No-rewrite statistics

```bash
python3 run_v3_no_rewrite_statistics.py
```

This now reports the full synthetic `N` sweep present in the local comparison surface.

### No-rewrite surface audit

```bash
python3 run_v3_no_rewrite_surface_audit.py
```

### No-rewrite Pareto

```bash
python3 run_v3_no_rewrite_pareto.py
```

## What Is Still Missing For Full V3

The following items are still pending:

- run real public memory-system baselines
  - Mem0 / Zep / MemoryOS on official harnesses
- pass the real `E0` sanity gate first
- restore the full `N` sweep on the real final-path runs
- expand conflict / unsafe into real family-scale tables
- add ≥5 seeds with proper statistics
- add human judge validation with Cohen's `kappa`
- add multi-backbone robustness
- finish TierMem integration of the safety-critical-field no-rewrite mechanism

## Repository Scope

This repo should now be interpreted as:

- a **V3 migration workspace**
- a **TierMem bridge and audit surface**
- a **legacy pilot asset bank**

It should **not** be interpreted anymore as:

- a finished PSU paper repo
- a fully complete TierMem reproduction
- a final paper-ready benchmark result release

## Related Files

- [REPRODUCIBILITY.md](./REPRODUCIBILITY.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [MODIFICATION_LOG_SUMMARY.md](./MODIFICATION_LOG_SUMMARY.md)
- [state/rebuttal_gap_closure_plan.md](./state/rebuttal_gap_closure_plan.md)
