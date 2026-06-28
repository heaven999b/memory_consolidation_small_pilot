# Actual Hallucination Surrogate Split Summary

这一轮继续沿着 typed midpoint 往前走，但不再把 surrogate 放在一个桶里：把 identity-like surrogate 和 preference-style surrogate 拆开，测试高-N detector gain 到底主要靠哪一类在支撑。

- slice items: 8
- seeds: [11, 23]
- interventions: strong_anchor, typed_selective_anchor, identity_selective_anchor, preference_selective_anchor, soft_anchor
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

## typed_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.562 | 0.438 | 0.500 | 0.000 | 0.438 | 0.000 | 0.438 | 0.312 | 0.000 | 0.2071 |
| 8 | 0.562 | 0.438 | 0.625 | 0.000 | 0.438 | 0.000 | 0.312 | 0.375 | 0.062 | 0.3928 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.188 | 0.000 | 0.188 | 0.438 | 0.312 | 0.000 | 0.2071 |
| 8 | 1.000 | 0.000 | 0.000 | 0.062 | 0.000 | 0.062 | 0.312 | 0.375 | 0.062 | 0.3928 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.438 | 0.312 | 0.000 | 0.2071 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.312 | 0.375 | 0.062 | 0.3928 |

## identity_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.625 | 0.375 | 0.375 | 0.000 | 0.375 | 0.000 | 0.375 | 0.250 | 0.000 | 0.1881 |
| 8 | 0.625 | 0.375 | 0.500 | 0.000 | 0.375 | 0.000 | 0.438 | 0.250 | 0.000 | 0.3677 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.125 | 0.000 | 0.125 | 0.375 | 0.250 | 0.000 | 0.1881 |
| 8 | 1.000 | 0.000 | 0.000 | 0.062 | 0.000 | 0.062 | 0.438 | 0.250 | 0.000 | 0.3677 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.375 | 0.250 | 0.000 | 0.1881 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.438 | 0.250 | 0.000 | 0.3677 |

## preference_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.812 | 0.188 | 0.375 | 0.000 | 0.188 | 0.000 | 0.250 | 0.125 | 0.000 | 0.1982 |
| 8 | 0.812 | 0.188 | 0.312 | 0.000 | 0.188 | 0.000 | 0.250 | 0.125 | 0.000 | 0.3843 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.125 | 0.000 | 0.1982 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.125 | 0.000 | 0.3843 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.125 | 0.000 | 0.1982 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.125 | 0.000 | 0.3843 |

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

## Split Readout

- Unified clue survival at N=4: strong/typed/identity/preference/soft = `0.938` / `0.312` / `0.250` / `0.125` / `0.125`.
- Unified clue survival at N=8: strong/typed/identity/preference/soft = `0.938` / `0.375` / `0.250` / `0.125` / `0.125`.
- Typed detector gain at N=8: unified/note-aware false_present = `0.062`/`0.000`.
- Identity detector gain at N=8: unified/note-aware false_present = `0.062`/`0.000`.
- Preference detector gain at N=8: unified/note-aware false_present = `0.000`/`0.000`.
- Summary-only realism at N=8: strong/typed/identity/preference/soft = `0.062` / `0.562` / `0.625` / `0.812` / `0.875`.
- Seed-level note-aware non-loss under identity_selective_anchor: N=4 `2/2`, N=8 `2/2`.
- Seed-level note-aware non-loss under preference_selective_anchor: N=4 `2/2`, N=8 `2/2`.
