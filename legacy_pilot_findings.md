# Legacy Pilot Findings

Date: 2026-06-30

This document records how the earlier `psu`-centered pilot transfers into the V3 TierMem path.

## Directly reusable assets

### Benchmark integration

These are still valuable and should move forward into the V3 path:

- mirrored HaluMem assets under `benchmarks/halumem/`
- mirrored LoCoMo assets under `benchmarks/locomo/`
- mirrored LongMemEval assets under `benchmarks/locomo/longmemeval_official/`
- frozen benchmark slices and source manifests
- benchmark-facing runtime scaffolding:
  - [benchmark_native_runtime.py](./benchmark_native_runtime.py)
  - [run_external_benchmark_adapter_layer.py](./run_external_benchmark_adapter_layer.py)
  - [run_external_benchmark_minimal_baseline.py](./run_external_benchmark_minimal_baseline.py)
  - [run_external_benchmark_reviewer_section.py](./run_external_benchmark_reviewer_section.py)

### Metric and artifact infrastructure

These should be migrated rather than rewritten:

- metric lineage:
  - `propagation`
  - `false_present`
  - `history_loss`
  - `raw_escalation`
- artifact pattern:
  - `run_*` + `verify_*`
  - per-item JSON/JSONL traces
  - monitor HTML / JSON
  - packet-style markdown summaries
- benchmark expansion tooling:
  - [freeze_external_benchmark_expanded_slices.py](./freeze_external_benchmark_expanded_slices.py)
  - [run_expanded_benchmark_dataset_inventory.py](./run_expanded_benchmark_dataset_inventory.py)
  - [run_expanded_benchmark_rigor_audit.py](./run_expanded_benchmark_rigor_audit.py)
  - [run_expanded_benchmark_staged.py](./run_expanded_benchmark_staged.py)

### Failure-mode knowledge

The many local refinement rounds remain useful as **design evidence**, not result evidence.

They already tell us where iterative compaction tends to fail:

- literal overlap collapse
- name normalization drift
- carry-forward failure
- placeholder collapse
- unsupported designation fabrication
- over-refusal on benign items
- unsafe retention and laundering

That taxonomy should migrate into the V3 appendix and defense motivation section.

## Re-cast assets

### PSU

`PSU` should be kept as:

- a strong **legacy baseline**
- a heuristic-only comparison point with:
  - scaffolded compaction
  - carry-forward hardening
  - note-aware routing
  - no true provenance mechanism

It should **not** remain the paper's claimed contribution.

### Expanded benchmark panel work

The expanded benchmark staging work is still worth keeping because it proves:

- the repo can freeze and audit larger benchmark pools
- the monitor / cache / packet infrastructure scales beyond toy slices

But its interpretation changes:

- it is migration support for V3
- not final held-out evidence for the new paper claim

## Retired as main evidence

The following should not be treated as final paper evidence anymore:

- PSU's in-sample headline wins
- any result obtained after repeated micro-round tuning on fixed small slices
- `scale_aware_unified` as a paper-facing method
- DeepSeek-only proxy conclusions

## Practical migration rule

When deciding whether to keep something from the earlier pilot, use this rule:

- keep it if it helps:
  - load data
  - score outputs
  - serialize traces
  - audit benchmark quality
  - explain failure modes
- demote it if it is:
  - a tuned result
  - a locally composite method
  - a proxy-only conclusion

## Bottom line

The legacy pilot is not dead work.

Its correct V3 role is:

- **asset bank**
- **baseline bank**
- **failure-taxonomy appendix**

Its incorrect V3 role would be:

- final method
- final benchmark evidence
- final causal claim
