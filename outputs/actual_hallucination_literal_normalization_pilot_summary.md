# Actual Hallucination Literal Normalization Pilot Summary

这一轮把 aligned-name note normalization 从 focused name-only branch 合回 broad literal branch：不改 literal compactor prompt，不改 detector，只在 executor 侧把 surviving aligned-name tentative clue 归一成标准三行 scaffold，检查 mixed code+name literal slice 会不会更干净、更稳定。

- slice items: 6
- seeds: [11]
- interventions: typed_selective_anchor, literal_identity_anchor, normalized_literal_identity_anchor, code_literal_anchor, name_literal_anchor
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

## Literal Normalization Readout

- Unified N=8 false_present: typed/literal/normalized/code/name = `0.500` / `0.500` / `0.500` / `0.167` / `0.333`.
- Note-aware N=8 false_present: typed/literal/normalized/code/name = `0.333` / `0.000` / `0.000` / `0.000` / `0.333`.
- Broad literal unified N=8 before normalization: code `signal=1/2, tent=0/2, raw=1/2, scaffold=2/2`, weak-name `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, strengthened-name `signal=2/2, tent=0/2, raw=2/2, scaffold=1/2`.
- Broad literal unified N=8 after normalization: code `signal=1/2, tent=0/2, raw=1/2, scaffold=2/2`, weak-name `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, strengthened-name `signal=2/2, tent=0/2, raw=2/2, scaffold=2/2`.
- Broad literal note-aware N=8 after normalization: strengthened-name `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Summary-only N=8 realism: literal/normalized = `0.333` / `0.333`.
