# Actual Hallucination Literal Subsplit Pilot Summary

这一轮把 literal branch 再往前拆一层：固定 6 条 literal-overlap hallucination item，只看 broad literal contract 能否再拆成 code-like overlap 与 person-name overlap，并检查新补强的人名样本是否真的比旧样本更能留下 detector-visible clue。

- slice items: 6
- seeds: [11]
- interventions: typed_selective_anchor, literal_identity_anchor, code_literal_anchor, name_literal_anchor
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

## code_literal_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.667 | 0.333 | 0.500 | 0.000 | 0.333 | 0.000 | 0.333 | 0.167 | 0.000 | 0.2110 |
| 8 | 0.667 | 0.333 | 0.667 | 0.000 | 0.333 | 0.000 | 0.333 | 0.167 | 0.000 | 0.4192 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.167 | 0.000 | 0.2110 |
| 8 | 1.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.167 | 0.333 | 0.167 | 0.000 | 0.4192 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.167 | 0.000 | 0.2110 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.167 | 0.000 | 0.4192 |

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

## Literal Subsplit Readout

- Unified N=8 false_present: typed/literal/code/name = `0.500` / `0.500` / `0.167` / `0.333`.
- Note-aware N=8 false_present: typed/literal/code/name = `0.333` / `0.000` / `0.000` / `0.333`.
- Broad literal branch on unified N=8: code `tent=0/2, raw=1/2`, weak-name `tent=0/2, raw=0/2`, strengthened-name `tent=0/2, raw=2/2`.
- Code-only branch on unified N=8: code `tent=1/2, raw=1/2`, all-name `tent=0/4, raw=0/4`.
- Name-only branch on unified N=8: weak-name `tent=1/2, raw=0/2`, strengthened-name `tent=1/2, raw=2/2`, code `tent=0/2, raw=0/2`.
- Summary-only N=8 realism: typed/literal/code/name = `0.167` / `0.333` / `0.667` / `0.500`.
