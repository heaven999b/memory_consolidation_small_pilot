# Expanded Benchmark Stage: smoke

Fast contract sanity pass across every canonical expanded-pool stratum before broader staged execution.

- seeds: `[11]`
- architectures: `summary_only, tiered, scale_aware_unified, scale_aware_note_aware, psu`
- N values: `[1, 8]`
- total selected items: `9`

## Panel Coverage

| Panel | Selected | Available | Selected Fraction | Strata |
|---|---:|---:|---:|---|
| halumem_expanded_v1 | 2 | 19 | 0.105 | {'halumem_unsupported_designation_abstain': 2} |
| locomo_expanded_v1 | 4 | 80 | 0.050 | {'locomo_absolute_temporal': 2, 'locomo_entity_or_attribute': 1, 'locomo_quantity_or_duration': 1} |
| longmemeval_expanded_v2 | 3 | 60 | 0.050 | {'longmemeval_single_session_assistant': 1, 'longmemeval_single_session_user': 2} |

## Family Rollups

### benign_utility_expanded_pool

- member_panels: `['locomo_expanded_v1', 'longmemeval_expanded_v2']`
- num_items: `7`

| Method | N=1 acc | N=1 history_loss | N=8 acc | N=8 history_loss | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 1.000 | 0.000 | 0.714 | 0.143 | 0.000 |
| tiered | 1.000 | 0.000 | 1.000 | 0.143 | 0.286 |
| scale_aware_unified | 1.000 | 0.000 | 1.000 | 0.286 | 0.286 |
| scale_aware_note_aware | 1.000 | 0.000 | 1.000 | 0.286 | 0.286 |
| psu | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |

#### Seed Stability (N=8)

| Method | accuracy by seed | history_loss by seed | history_loss span |
|---|---|---|---:|
| summary_only | 11:0.714 | 11:0.143 | 0.000 |
| tiered | 11:1.000 | 11:0.143 | 0.000 |
| scale_aware_unified | 11:1.000 | 11:0.286 | 0.000 |
| scale_aware_note_aware | 11:1.000 | 11:0.286 | 0.000 |
| psu | 11:1.000 | 11:0.000 | 0.000 |

### hallucination_expanded_pool

- member_panels: `['halumem_expanded_v1']`
- num_items: `2`

| Method | N=1 acc | N=1 false_present | N=8 acc | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| scale_aware_note_aware | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| psu | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |

#### Seed Stability (N=8)

| Method | accuracy by seed | false_present by seed | false_present span |
|---|---|---|---:|
| summary_only | 11:1.000 | 11:0.000 | 0.000 |
| tiered | 11:1.000 | 11:1.000 | 0.000 |
| scale_aware_unified | 11:1.000 | 11:0.000 | 0.000 |
| scale_aware_note_aware | 11:1.000 | 11:0.000 | 0.000 |
| psu | 11:1.000 | 11:0.000 | 0.000 |

## Readout

- This staged artifact uses the expanded official benchmark pool rather than the older 32-item reviewer section, but it still preserves the same benchmark-native compaction stack and family-level metrics.
- Smoke and medium stages should be interpreted as execution and stability checks over canonical strata, not as the final paper-facing benchmark table.
- The right success condition for this artifact is structural stability across seeds and families; the right next step after a stable medium run is deciding whether to promote the full expanded main run.
