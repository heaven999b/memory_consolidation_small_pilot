# Actual Hallucination Name Refinement Pilot Summary

这一轮不再继续扩数据，而是专门收紧 name-only scaffold：把 role-aligned 的人名重叠和 role-mismatched 的人名重叠显式分开，检查强化后的人名分支能否从 recoverable signal 更进一步走向 compact-stable clue。

- slice items: 6
- seeds: [11]
- interventions: typed_selective_anchor, literal_identity_anchor, name_literal_anchor, refined_name_literal_anchor
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [4, 8]

## typed_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.167 | 0.833 | 0.833 | 0.000 | 0.833 | 0.000 | 0.833 | 0.667 | 0.000 | 0.1998 |
| 8 | 0.167 | 0.833 | 0.833 | 0.000 | 0.833 | 0.000 | 0.667 | 0.667 | 0.000 | 0.3722 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.833 | 0.667 | 0.000 | 0.1998 |
| 8 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.667 | 0.667 | 0.000 | 0.3722 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.167 | 0.833 | 0.667 | 0.000 | 0.1998 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.667 | 0.667 | 0.000 | 0.3722 |

## literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.333 | 0.667 | 0.667 | 0.000 | 0.667 | 0.000 | 0.333 | 0.000 | 0.000 | 0.2347 |
| 8 | 0.333 | 0.667 | 0.667 | 0.000 | 0.667 | 0.000 | 0.667 | 0.000 | 0.000 | 0.4636 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.000 | 0.000 | 0.2347 |
| 8 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.667 | 0.000 | 0.000 | 0.4636 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.167 | 0.333 | 0.000 | 0.000 | 0.2347 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.667 | 0.000 | 0.000 | 0.4636 |

## name_literal_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.500 | 0.500 | 0.500 | 0.000 | 0.500 | 0.000 | 0.333 | 0.167 | 0.000 | 0.2087 |
| 8 | 0.500 | 0.500 | 0.500 | 0.000 | 0.500 | 0.000 | 0.333 | 0.333 | 0.000 | 0.3902 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.333 | 0.167 | 0.000 | 0.2087 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.333 | 0.000 | 0.3902 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.167 | 0.000 | 0.2087 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.333 | 0.000 | 0.3902 |

## refined_name_literal_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.667 | 0.333 | 0.333 | 0.000 | 0.333 | 0.000 | 0.000 | 0.333 | 0.000 | 0.2136 |
| 8 | 0.667 | 0.333 | 0.333 | 0.000 | 0.333 | 0.000 | 0.000 | 0.333 | 0.000 | 0.4208 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.2136 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.4208 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.2136 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.333 | 0.000 | 0.4208 |

## Name Refinement Readout

- Unified N=8 false_present: typed/literal/name/refined = `0.500` / `0.500` / `0.333` / `0.333`.
- Note-aware N=8 false_present: typed/literal/name/refined = `0.333` / `0.000` / `0.333` / `0.333`.
- Baseline name branch on unified N=8: weak-name `signal=1/2, tent=1/2, raw=0/2`, strengthened-name `signal=2/2, tent=1/2, raw=2/2`, code `signal=0/2, tent=0/2, raw=0/2`.
- Refined name branch on unified N=8: weak-name `signal=0/2, tent=0/2, raw=0/2`, strengthened-name `signal=2/2, tent=2/2, raw=2/2`, code `signal=0/2, tent=0/2, raw=0/2`.
- Summary-only N=8 realism: typed/literal/name/refined = `0.167` / `0.333` / `0.500` / `0.667`.
