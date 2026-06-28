# Actual Hallucination Robustness Summary

这一轮把 actual hallucination persistence 推到 robustness 检验：既扩 seed，也把强 anchor contract 和 softer anchor contract 放在同一真实 stress slice 上对照。

- slice items: 8
- seeds: [11, 23]
- interventions: strong_anchor, soft_anchor
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [4, 8]

## strong_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.062 | 0.938 | 0.938 | 0.000 | 0.938 | 0.000 | 0.875 | 0.938 | 0.125 | 0.1941 |
| 8 | 0.062 | 0.938 | 0.938 | 0.000 | 0.938 | 0.000 | 0.938 | 0.938 | 0.250 | 0.4061 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.312 | 0.000 | 0.312 | 0.875 | 0.938 | 0.125 | 0.1941 |
| 8 | 1.000 | 0.000 | 0.000 | 0.188 | 0.000 | 0.188 | 0.938 | 0.938 | 0.250 | 0.4061 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.875 | 0.938 | 0.125 | 0.1941 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.938 | 0.938 | 0.250 | 0.4061 |

## soft_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.875 | 0.125 | 0.125 | 0.000 | 0.125 | 0.000 | 0.188 | 0.125 | 0.000 | 0.1840 |
| 8 | 0.875 | 0.125 | 0.188 | 0.000 | 0.125 | 0.000 | 0.312 | 0.125 | 0.000 | 0.3504 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.188 | 0.125 | 0.000 | 0.1840 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.312 | 0.125 | 0.000 | 0.3504 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.188 | 0.125 | 0.000 | 0.1840 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.312 | 0.125 | 0.000 | 0.3504 |

## Robustness Readout

- Strong vs soft clue survival at unified N=4: tentative_target_claim = `0.938` vs `0.125`.
- Strong vs soft clue survival at unified N=8: tentative_target_claim = `0.938` vs `0.125`.
- Strong-anchor detector gain at N=4: unified/note-aware false_present = `0.312`/`0.000`.
- Strong-anchor detector gain at N=8: unified/note-aware false_present = `0.188`/`0.000`.
- Seed-level note-aware non-loss under strong_anchor: N=4 `2/2`, N=8 `2/2`.
