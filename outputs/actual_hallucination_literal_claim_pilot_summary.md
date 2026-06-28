# Actual Hallucination Literal Claim Pilot Summary

这一轮不再继续做 note-only cleanup，而是对 broad literal branch 加一个 claim-sensitive executor follow-up：在 aligned-name role 对齐的情况下，把已经 canonical 的 broad literal scaffold 显式转成 tentative query claim，同时保持 mixed code+name literal slice 的 aggregate false-present 不回退。

- slice items: 6
- seeds: [11]
- interventions: typed_selective_anchor, literal_identity_anchor, normalized_literal_identity_anchor, claim_normalized_literal_identity_anchor, code_literal_anchor, name_literal_anchor
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

## normalized_literal_identity_anchor

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

## claim_normalized_literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.333 | 0.667 | 0.667 | 0.000 | 0.667 | 0.000 | 0.333 | 0.167 | 0.000 | 0.2347 |
| 8 | 0.333 | 0.667 | 0.667 | 0.000 | 0.667 | 0.000 | 0.667 | 0.333 | 0.000 | 0.4636 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.167 | 0.000 | 0.2347 |
| 8 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.667 | 0.333 | 0.000 | 0.4636 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.167 | 0.333 | 0.167 | 0.000 | 0.2347 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.667 | 0.333 | 0.000 | 0.4636 |

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

## Literal Claim Readout

- Unified N=8 false_present: literal/normalized/claim = `0.500` / `0.500` / `0.500`.
- Note-aware N=8 false_present: literal/normalized/claim = `0.000` / `0.000` / `0.000`.
- Broad literal unified N=8 before note rewrite: strengthened-name `signal=2/2, tent=0/2, raw=2/2, scaffold=1/2`.
- Broad literal unified N=8 after note rewrite: strengthened-name `signal=2/2, tent=0/2, raw=2/2, scaffold=2/2`.
- Broad literal unified N=8 after claim-sensitive rewrite: strengthened-name `signal=2/2, tent=2/2, raw=2/2, scaffold=2/2`.
- Broad literal note-aware N=8 after claim-sensitive rewrite: strengthened-name `signal=2/2, tent=2/2, raw=0/2, scaffold=2/2`.
- Broad literal code/weak-name non-regression at unified N=8: code `signal=1/2, tent=0/2, raw=1/2, scaffold=2/2`, weak-name `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Summary-only N=8 realism: normalized/claim = `0.333` / `0.333`.
