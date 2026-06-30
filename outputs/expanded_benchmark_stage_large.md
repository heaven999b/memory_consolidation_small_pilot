# Expanded Benchmark Stage: large

Larger staged pass with broader official-benchmark coverage and PSU included, meant to sit between medium validation and the full main run.

- seeds: `[11]`
- architectures: `summary_only, tiered, scale_aware_unified, scale_aware_note_aware, psu`
- N values: `[1, 8]`
- total selected items: `34`

## Panel Coverage

| Panel | Selected | Available | Selected Fraction | Strata |
|---|---:|---:|---:|---|
| halumem_expanded_v1 | 6 | 19 | 0.316 | {'halumem_unsupported_designation_abstain': 6} |
| locomo_expanded_v1 | 16 | 80 | 0.200 | {'locomo_absolute_temporal': 8, 'locomo_entity_or_attribute': 4, 'locomo_quantity_or_duration': 4} |
| longmemeval_expanded_v2 | 12 | 60 | 0.200 | {'longmemeval_single_session_assistant': 4, 'longmemeval_single_session_user': 8} |

## Family Rollups

### benign_utility_expanded_pool

- member_panels: `['locomo_expanded_v1', 'longmemeval_expanded_v2']`
- num_items: `28`

| Method | N=1 acc | N=1 history_loss | N=8 acc | N=8 history_loss | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.929 | 0.071 | 0.357 | 0.464 | 0.000 |
| tiered | 1.000 | 0.071 | 0.964 | 0.464 | 0.607 |
| scale_aware_unified | 1.000 | 0.107 | 0.964 | 0.607 | 0.607 |
| scale_aware_note_aware | 1.000 | 0.107 | 0.964 | 0.607 | 0.607 |
| psu | 1.000 | 0.036 | 0.964 | 0.036 | 0.036 |

#### Seed Stability (N=8)

| Method | accuracy by seed | history_loss by seed | history_loss span |
|---|---|---|---:|
| summary_only | 11:0.357 | 11:0.464 | 0.000 |
| tiered | 11:0.964 | 11:0.464 | 0.000 |
| scale_aware_unified | 11:0.964 | 11:0.607 | 0.000 |
| scale_aware_note_aware | 11:0.964 | 11:0.607 | 0.000 |
| psu | 11:0.964 | 11:0.036 | 0.000 |

### hallucination_expanded_pool

- member_panels: `['halumem_expanded_v1']`
- num_items: `6`

| Method | N=1 acc | N=1 false_present | N=8 acc | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.167 | 0.000 | 0.833 | 0.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 0.667 | 1.000 | 0.167 | 0.167 |
| scale_aware_note_aware | 1.000 | 0.500 | 1.000 | 0.167 | 0.167 |
| psu | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |

#### Seed Stability (N=8)

| Method | accuracy by seed | false_present by seed | false_present span |
|---|---|---|---:|
| summary_only | 11:0.833 | 11:0.000 | 0.000 |
| tiered | 11:1.000 | 11:1.000 | 0.000 |
| scale_aware_unified | 11:1.000 | 11:0.167 | 0.000 |
| scale_aware_note_aware | 11:1.000 | 11:0.167 | 0.000 |
| psu | 11:1.000 | 11:0.000 | 0.000 |

## Readout

- This staged artifact uses the expanded official benchmark pool rather than the older 32-item reviewer section, but it still preserves the same benchmark-native compaction stack and family-level metrics.
- Smoke and medium stages should be interpreted as execution and stability checks over canonical strata, not as the final paper-facing benchmark table.
- The right success condition for this artifact is structural stability across seeds and families; the right next step after a stable medium run is deciding whether to promote the full expanded main run.
