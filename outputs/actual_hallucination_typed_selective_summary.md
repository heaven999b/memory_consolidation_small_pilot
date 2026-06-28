# Actual Hallucination Typed Selective Summary

这一轮不是再找一个新的中间态，而是把上一轮的 selective_anchor 做 typed semantics refinement：尽量保住 person/code-like surrogate，同时把 policy-window 和 schedule-like clue 压回 weak_context。

- slice items: 8
- seeds: [11, 23]
- interventions: strong_anchor, selective_anchor, typed_selective_anchor, soft_anchor
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

## selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.500 | 0.500 | 0.625 | 0.000 | 0.500 | 0.000 | 0.500 | 0.375 | 0.062 | 0.2090 |
| 8 | 0.438 | 0.562 | 0.688 | 0.000 | 0.562 | 0.000 | 0.438 | 0.375 | 0.125 | 0.4014 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.188 | 0.000 | 0.188 | 0.500 | 0.375 | 0.062 | 0.2090 |
| 8 | 0.938 | 0.062 | 0.000 | 0.062 | 0.062 | 0.062 | 0.438 | 0.375 | 0.125 | 0.4014 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.375 | 0.062 | 0.2090 |
| 8 | 0.938 | 0.062 | 0.000 | 0.000 | 0.062 | 0.000 | 0.438 | 0.375 | 0.125 | 0.4014 |

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

## Typed Readout

- Unified clue survival at N=4: strong/selective/typed/soft = `0.938` / `0.375` / `0.312` / `0.125`.
- Unified clue survival at N=8: strong/selective/typed/soft = `0.938` / `0.375` / `0.375` / `0.125`.
- Typed-anchor detector gain at N=4: unified/note-aware false_present = `0.188`/`0.000`.
- Typed-anchor detector gain at N=8: unified/note-aware false_present = `0.062`/`0.000`.
- Summary-only realism at N=4: strong/selective/typed accuracy = `0.062`/`0.500`/`0.562`.
- Summary-only realism at N=8: strong/selective/typed accuracy = `0.062`/`0.438`/`0.562`.
- Seed-level note-aware non-loss under typed_selective_anchor: N=4 `2/2`, N=8 `2/2`.
- Typed high-N accuracy vs prior selective: unified `1.000` vs `0.938`, note-aware `1.000` vs `0.938`.
