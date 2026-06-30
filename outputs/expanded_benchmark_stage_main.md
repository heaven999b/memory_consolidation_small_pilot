# Expanded Benchmark Stage: main

Full expanded official benchmark pool.

- seeds: `[11, 23]`
- architectures: `summary_only, tiered, scale_aware_unified, scale_aware_note_aware, psu`
- N values: `[1, 8]`
- total selected items: `159`

## Panel Coverage

| Panel | Selected | Available | Selected Fraction | Strata |
|---|---:|---:|---:|---|
| halumem_expanded_v1 | 19 | 19 | 1.000 | {'halumem_unsupported_designation_abstain': 19} |
| locomo_expanded_v1 | 80 | 80 | 1.000 | {'locomo_absolute_temporal': 40, 'locomo_entity_or_attribute': 20, 'locomo_quantity_or_duration': 20} |
| longmemeval_expanded_v2 | 60 | 60 | 1.000 | {'longmemeval_single_session_assistant': 12, 'longmemeval_single_session_user': 48} |

## Family Rollups

### benign_utility_expanded_pool

- member_panels: `['locomo_expanded_v1', 'longmemeval_expanded_v2']`
- num_items: `140`

| Method | N=1 acc | N=1 history_loss | N=8 acc | N=8 history_loss | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.954 | 0.032 | 0.314 | 0.554 | 0.000 |
| tiered | 0.986 | 0.032 | 0.946 | 0.554 | 0.650 |
| scale_aware_unified | 0.986 | 0.071 | 0.946 | 0.650 | 0.650 |
| scale_aware_note_aware | 0.986 | 0.071 | 0.946 | 0.650 | 0.650 |
| psu | 0.993 | 0.039 | 0.986 | 0.071 | 0.071 |

#### Seed Stability (N=8)

| Method | accuracy by seed | history_loss by seed | history_loss span |
|---|---|---|---:|
| summary_only | 11:0.300, 23:0.329 | 11:0.557, 23:0.550 | 0.007 |
| tiered | 11:0.943, 23:0.950 | 11:0.557, 23:0.550 | 0.007 |
| scale_aware_unified | 11:0.943, 23:0.950 | 11:0.650, 23:0.650 | 0.000 |
| scale_aware_note_aware | 11:0.943, 23:0.950 | 11:0.650, 23:0.650 | 0.000 |
| psu | 11:0.979, 23:0.993 | 11:0.071, 23:0.071 | 0.000 |

### hallucination_expanded_pool

- member_panels: `['halumem_expanded_v1']`
- num_items: `19`

| Method | N=1 acc | N=1 false_present | N=8 acc | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.237 | 0.000 | 0.895 | 0.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 0.526 | 1.000 | 0.079 | 0.079 |
| scale_aware_note_aware | 1.000 | 0.289 | 1.000 | 0.053 | 0.053 |
| psu | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |

#### Seed Stability (N=8)

| Method | accuracy by seed | false_present by seed | false_present span |
|---|---|---|---:|
| summary_only | 11:0.947, 23:0.842 | 11:0.000, 23:0.000 | 0.000 |
| tiered | 11:1.000, 23:1.000 | 11:1.000, 23:1.000 | 0.000 |
| scale_aware_unified | 11:1.000, 23:1.000 | 11:0.053, 23:0.105 | 0.052 |
| scale_aware_note_aware | 11:1.000, 23:1.000 | 11:0.053, 23:0.053 | 0.000 |
| psu | 11:1.000, 23:1.000 | 11:0.000, 23:0.000 | 0.000 |

## Readout

- This staged artifact uses the expanded official benchmark pool rather than the older 32-item reviewer section, but it still preserves the same benchmark-native compaction stack and family-level metrics.
- Smoke and medium stages should be interpreted as execution and stability checks over canonical strata, not as the final paper-facing benchmark table.
- The right success condition for this artifact is structural stability across seeds and families; the right next step after a stable medium run is deciding whether to promote the full expanded main run.
