# Expanded Benchmark Rigor Audit

这个 audit 不评估模型分数，只评估 expanded benchmark pool 本身是否足够严谨、分层是否标准、以及每一层能不能承担预期用途。

## Overall Verdict

- expanded_pool_standardized: `True`
- staged_run_ready: `True`
- full_paper_ready: `False`
- note: `Need full model-backed runs over the expanded pool and still lack official external conflict/unsafe families.`

## Layer Policy

| Layer | Count | Role | Verdict |
|---|---:|---|---|
| layer_0_reviewer_core | 32 | current_frozen_reviewer_table | solid_for_current_reporting |
| layer_1_expanded_official_pool | 159 | next_stage_benchmark_native_scale_up | staged_run_ready |
| layer_2_four_family_closure | 165 | four_family_primary_surface | coverage_complete_but_mixed_source_kind |

## Panel Rigor

| Panel | Selected | Source Total | Clean Candidate Pool | Runtime Projection | Key Strata |
|---|---:|---:|---:|---:|---|
| halumem_expanded_v1 | 19 | 20 | 19 | 19/19 | {'halumem_unsupported_designation_abstain': 19} |
| locomo_expanded_v1 | 80 | 1986 | 356 | 80/80 | {'locomo_absolute_temporal': 40, 'locomo_entity_or_attribute': 20, 'locomo_quantity_or_duration': 20} |
| longmemeval_expanded_v2 | 60 | 500 | 92 | 60/60 | {'longmemeval_single_session_assistant': 12, 'longmemeval_single_session_user': 48} |

## Stratum Verdicts

| Stratum | Count | Verdict | Use Note |
|---|---:|---|---|
| halumem_unsupported_designation_abstain | 19 | adequate | adequate for staged hallucination evaluation; still smaller than a final paper-scale family table would ideally want |
| locomo_absolute_temporal | 40 | solid | sufficient as a main staged benchmark stratum |
| locomo_entity_or_attribute | 20 | adequate | sufficient as a main staged benchmark stratum |
| locomo_quantity_or_duration | 20 | adequate | sufficient as a main staged benchmark stratum |
| longmemeval_single_session_assistant | 12 | adequate | good auxiliary stress/control stratum; too thin to headline alone |
| longmemeval_single_session_user | 48 | solid | sufficient as a main staged benchmark stratum |

## Findings

- The pool is now standardized enough to run staged benchmark experiments because the canonical levels are no longer the source dataset categories alone; they are the derived contract-based strata recorded in the expanded manifests.
- HaluMem is contract-pure but still relatively small at 19 items, so it is adequate for staged hallucination evaluation but not ideal as a lone paper-scale headline family.
- LoCoMo is the cleanest large stratum: 80 items, balanced across all 10 conversations, and split into explicit contract-derived strata rather than only relying on noisy source categories.
- LongMemEval user-facing recall is strong enough as a real stratum at 48 items, while the 12-item assistant-facing slice is best treated as an auxiliary control layer.
- The most important remaining structural limitation is not quality noise inside the pool; it is that official external benchmark coverage still stops at benign plus hallucination, while conflict and unsafe are only closed by local task extensions.

## Blocking Notes

- The LongMemEval assistant-facing stratum is only 12 items, so it should be treated as an auxiliary control slice rather than a standalone headline panel.
- The official expanded pool still covers benign plus hallucination only; conflict and unsafe remain manifest-backed local task extensions rather than official external benchmark panels.
- LoCoMo source categories are not stable enough to serve as the final paper taxonomy by themselves; the derived contract-based strata should be treated as the canonical levels.

