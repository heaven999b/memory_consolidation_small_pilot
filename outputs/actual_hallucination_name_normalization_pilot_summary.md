# Actual Hallucination Name Normalization Pilot Summary

这一轮固定上一轮的 refined name-only compactor，不再改 prompt 语义，而是在 executor 侧加入 aligned-name note normalization：当正确的 tentative aligned-name claim 还在时，把最终 note 归一成标准三行 scaffold，并显式补上 inference marker。

- slice items: 6
- seeds: [11]
- interventions: name_literal_anchor, refined_name_literal_anchor, normalized_refined_name_literal_anchor
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [4, 8]

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

## normalized_refined_name_literal_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.667 | 0.333 | 0.333 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.000 | 0.2136 |
| 8 | 0.667 | 0.333 | 0.333 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.000 | 0.4208 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.333 | 0.000 | 0.2136 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.333 | 0.000 | 0.4208 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.333 | 0.000 | 0.2136 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.333 | 0.000 | 0.4208 |

## Name Normalization Readout

- Unified N=8 false_present: baseline/refined/normalized = `0.333` / `0.333` / `0.333`.
- Note-aware N=8 false_present: baseline/refined/normalized = `0.333` / `0.333` / `0.000`.
- Refined unified N=8: weak-name `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, strengthened-name `signal=2/2, tent=2/2, raw=2/2, scaffold=1/2`, code `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Normalized unified N=8: weak-name `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, strengthened-name `signal=2/2, tent=2/2, raw=2/2, scaffold=2/2`, code `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Summary-only N=8 realism: baseline/refined/normalized = `0.500` / `0.667` / `0.667`.
