# External Benchmark Reviewer Section

这个 artifact 把 benchmark-first surface 从两条 starter panels 扩成了更宽的 reviewer-facing benchmark section：同一套 compaction stack 下，既有 core slices，也有 disjoint holdout / second-family expansion。

- seeds: `[11, 23]`
- architectures: `summary_only, tiered, scale_aware_unified, scale_aware_note_aware`
- N values: `[1, 8]`

## Family Rollups

### benign_utility_benchmark_section

- member_panels: `['locomo_core_v2', 'longmemeval_direct_v1']`
- num_items: `16`

| Method | N=1 acc | N=1 history_loss | N=8 acc | N=8 history_loss | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 1.000 | 0.000 | 0.469 | 0.438 | 0.000 |
| tiered | 1.000 | 0.000 | 0.906 | 0.438 | 0.438 |
| scale_aware_unified | 1.000 | 0.000 | 0.906 | 0.438 | 0.438 |
| scale_aware_note_aware | 1.000 | 0.000 | 0.906 | 0.438 | 0.438 |

#### Seed Stability (N=8)

| Method | accuracy by seed | history_loss by seed | history_loss span |
|---|---|---|---:|
| summary_only | 11:0.438, 23:0.500 | 11:0.500, 23:0.375 | 0.125 |
| tiered | 11:0.938, 23:0.875 | 11:0.500, 23:0.375 | 0.125 |
| scale_aware_unified | 11:0.938, 23:0.875 | 11:0.500, 23:0.375 | 0.125 |
| scale_aware_note_aware | 11:0.938, 23:0.875 | 11:0.500, 23:0.375 | 0.125 |

### hallucination_benchmark_section

- member_panels: `['halumem_core_v2', 'halumem_holdout_v1']`
- num_items: `16`

| Method | N=1 acc | N=1 false_present | N=8 acc | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.156 | 0.000 | 0.719 | 0.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 0.469 | 1.000 | 0.156 | 0.156 |
| scale_aware_note_aware | 1.000 | 0.125 | 1.000 | 0.094 | 0.094 |

#### Seed Stability (N=8)

| Method | accuracy by seed | false_present by seed | false_present span |
|---|---|---|---:|
| summary_only | 11:0.688, 23:0.750 | 11:0.000, 23:0.000 | 0.000 |
| tiered | 11:1.000, 23:1.000 | 11:1.000, 23:1.000 | 0.000 |
| scale_aware_unified | 11:1.000, 23:1.000 | 11:0.250, 23:0.062 | 0.188 |
| scale_aware_note_aware | 11:1.000, 23:1.000 | 11:0.188, 23:0.000 | 0.188 |

## Slice Coverage

| Panel | Family Rollup | Manifest Version | Items |
|---|---|---:|---:|
| halumem_core_v2 | hallucination_benchmark_section | v2 | 8 |
| halumem_holdout_v1 | hallucination_benchmark_section | v1 | 8 |
| locomo_core_v2 | benign_utility_benchmark_section | v2 | 8 |
| longmemeval_direct_v1 | benign_utility_benchmark_section | v1 | 8 |

## Readout

- HaluMem-style hallucination coverage is now broader than a single core slice because the reviewer section includes a disjoint holdout slice under the same unsupported-target contract.
- Benign utility coverage is now broader than LoCoMo alone because a direct-answer LongMemEval slice sits beside the LoCoMo core slice under the same answer-retention metrics.
- This still does not make the implementation fully TierMem-native, but it does make the benchmark-first surface materially less thin and less dependent on two starter slices.
