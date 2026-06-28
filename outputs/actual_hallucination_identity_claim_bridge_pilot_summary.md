# Actual Hallucination Identity Claim Bridge Pilot Summary

这一轮把 claim-sensitive broad literal branch 往外扩一层，重新接回 relation item：固定 8 条 relation+code+weak-name+strong-name slice，不强行发明一套全新 prompt，而是复用已经稳定的 relation-frontier 与 literal-frontier cache，检查 broad literal 的 claim surfacing 在更宽 identity/literal 前沿里是否仍然非回退。

- slice items: 8
- seeds: [11]
- interventions: typed_selective_anchor, literal_identity_anchor, normalized_literal_identity_anchor, claim_normalized_literal_identity_anchor
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [4, 8]

## typed_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.125 | 0.875 | 0.875 | 0.000 | 0.875 | 0.000 | 0.875 | 0.750 | 0.000 | 0.2084 |
| 8 | 0.125 | 0.875 | 0.875 | 0.000 | 0.875 | 0.000 | 0.750 | 0.750 | 0.125 | 0.3853 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.875 | 0.750 | 0.000 | 0.2084 |
| 8 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.750 | 0.750 | 0.125 | 0.3853 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.125 | 0.000 | 0.125 | 0.875 | 0.750 | 0.000 | 0.2084 |
| 8 | 1.000 | 0.000 | 0.000 | 0.250 | 0.000 | 0.250 | 0.750 | 0.750 | 0.125 | 0.3853 |

## literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.500 | 0.500 | 0.625 | 0.000 | 0.500 | 0.000 | 0.250 | 0.000 | 0.000 | 0.2210 |
| 8 | 0.500 | 0.500 | 0.625 | 0.000 | 0.500 | 0.000 | 0.500 | 0.000 | 0.000 | 0.4359 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.250 | 0.000 | 0.250 | 0.250 | 0.000 | 0.000 | 0.2210 |
| 8 | 1.000 | 0.000 | 0.000 | 0.375 | 0.000 | 0.375 | 0.500 | 0.000 | 0.000 | 0.4359 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.125 | 0.000 | 0.125 | 0.250 | 0.000 | 0.000 | 0.2210 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.000 | 0.4359 |

## normalized_literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.500 | 0.500 | 0.625 | 0.000 | 0.500 | 0.000 | 0.250 | 0.000 | 0.000 | 0.2210 |
| 8 | 0.500 | 0.500 | 0.625 | 0.000 | 0.500 | 0.000 | 0.500 | 0.000 | 0.000 | 0.4359 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.250 | 0.000 | 0.250 | 0.250 | 0.000 | 0.000 | 0.2210 |
| 8 | 1.000 | 0.000 | 0.000 | 0.375 | 0.000 | 0.375 | 0.500 | 0.000 | 0.000 | 0.4359 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.125 | 0.000 | 0.125 | 0.250 | 0.000 | 0.000 | 0.2210 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.000 | 0.4359 |

## claim_normalized_literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.500 | 0.500 | 0.625 | 0.000 | 0.500 | 0.000 | 0.250 | 0.125 | 0.000 | 0.2210 |
| 8 | 0.500 | 0.500 | 0.625 | 0.000 | 0.500 | 0.000 | 0.500 | 0.250 | 0.000 | 0.4359 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.250 | 0.000 | 0.250 | 0.250 | 0.125 | 0.000 | 0.2210 |
| 8 | 1.000 | 0.000 | 0.000 | 0.375 | 0.000 | 0.375 | 0.500 | 0.250 | 0.000 | 0.4359 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.125 | 0.000 | 0.125 | 0.250 | 0.125 | 0.000 | 0.2210 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.250 | 0.000 | 0.4359 |

## Identity Claim Bridge Readout

- Unified N=8 false_present: typed/literal/normalized/claim = `0.500` / `0.375` / `0.375` / `0.375`.
- Note-aware N=8 false_present: typed/literal/normalized/claim = `0.250` / `0.000` / `0.000` / `0.000`.
- Broad literal unified N=8 on relation items: literal `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, claim `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Broad literal unified N=8 on code items: literal `signal=1/2, tent=0/2, raw=1/2, scaffold=2/2`, claim `signal=1/2, tent=0/2, raw=1/2, scaffold=2/2`.
- Broad literal unified N=8 on weak-name items: literal `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, claim `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Broad literal unified N=8 on strengthened-name items: literal `signal=2/2, tent=0/2, raw=2/2, scaffold=1/2`, normalized `signal=2/2, tent=0/2, raw=2/2, scaffold=2/2`, claim `signal=2/2, tent=2/2, raw=2/2, scaffold=2/2`.
- Summary-only N=8 realism: literal/normalized/claim = `0.500` / `0.500` / `0.500`.
