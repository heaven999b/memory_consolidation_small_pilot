# Expanded Benchmark Stage: medium

Broader staged pass that still stays well below the full expanded pool but is large enough to expose stability issues by stratum.

- seeds: `[11, 23]`
- architectures: `summary_only, tiered, scale_aware_unified, scale_aware_note_aware`
- N values: `[1, 8]`
- total selected items: `18`

## Panel Coverage

| Panel | Selected | Available | Selected Fraction | Strata |
|---|---:|---:|---:|---|
| halumem_expanded_v1 | 4 | 19 | 0.211 | {'halumem_unsupported_designation_abstain': 4} |
| locomo_expanded_v1 | 8 | 80 | 0.100 | {'locomo_absolute_temporal': 4, 'locomo_entity_or_attribute': 2, 'locomo_quantity_or_duration': 2} |
| longmemeval_expanded_v2 | 6 | 60 | 0.100 | {'longmemeval_single_session_assistant': 2, 'longmemeval_single_session_user': 4} |

## Family Rollups

### benign_utility_expanded_pool

- member_panels: `['locomo_expanded_v1', 'longmemeval_expanded_v2']`
- num_items: `14`

| Method | N=1 acc | N=1 history_loss | N=8 acc | N=8 history_loss | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.964 | 0.036 | 0.464 | 0.357 | 0.000 |
| tiered | 1.000 | 0.036 | 1.000 | 0.357 | 0.536 |
| scale_aware_unified | 1.000 | 0.036 | 1.000 | 0.536 | 0.536 |
| scale_aware_note_aware | 1.000 | 0.036 | 1.000 | 0.536 | 0.536 |

#### Seed Stability (N=8)

| Method | accuracy by seed | history_loss by seed | history_loss span |
|---|---|---|---:|
| summary_only | 11:0.500, 23:0.429 | 11:0.357, 23:0.357 | 0.000 |
| tiered | 11:1.000, 23:1.000 | 11:0.357, 23:0.357 | 0.000 |
| scale_aware_unified | 11:1.000, 23:1.000 | 11:0.500, 23:0.571 | 0.071 |
| scale_aware_note_aware | 11:1.000, 23:1.000 | 11:0.500, 23:0.571 | 0.071 |

### hallucination_expanded_pool

- member_panels: `['halumem_expanded_v1']`
- num_items: `4`

| Method | N=1 acc | N=1 false_present | N=8 acc | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.250 | 0.000 | 1.000 | 0.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 0.625 | 1.000 | 0.000 | 0.000 |
| scale_aware_note_aware | 1.000 | 0.625 | 1.000 | 0.000 | 0.000 |

#### Seed Stability (N=8)

| Method | accuracy by seed | false_present by seed | false_present span |
|---|---|---|---:|
| summary_only | 11:1.000, 23:1.000 | 11:0.000, 23:0.000 | 0.000 |
| tiered | 11:1.000, 23:1.000 | 11:1.000, 23:1.000 | 0.000 |
| scale_aware_unified | 11:1.000, 23:1.000 | 11:0.000, 23:0.000 | 0.000 |
| scale_aware_note_aware | 11:1.000, 23:1.000 | 11:0.000, 23:0.000 | 0.000 |

## Readout

- This staged artifact uses the expanded official benchmark pool rather than the older 32-item reviewer section, but it still preserves the same benchmark-native compaction stack and family-level metrics.
- Smoke and medium stages should be interpreted as execution and stability checks over canonical strata, not as the final paper-facing benchmark table.
- The right success condition for this artifact is structural stability across seeds and families; the right next step after a stable medium run is deciding whether to promote the full expanded main run.
