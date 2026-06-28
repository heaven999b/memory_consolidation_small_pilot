# Actual Hallucination Claim Reintegration Summary

这一轮把 bridge slice 再往外扩成 14-item mixed stress+literal reintegration，并且对 6 条 non-literal stress item 补上了 exact `literal_identity_anchor` live closure。对这些 stress-context item，`literal_identity_anchor` 直接使用 exact closure rows；`normalized_literal_identity_anchor` 和 `claim_normalized_literal_identity_anchor` 则复用同一批 exact rows，因为它们的额外 executor rewrite 只会作用在 aligned literal-overlap case 上，在当前 non-literal stress subset 上是 inert 的。换句话说，这个 artifact 不再依赖 mode-equivalent proxy。

- slice items: 14
- seeds: [11]
- mode: exact_stress_closure_reintegration
- interventions: typed_selective_anchor, literal_identity_anchor, normalized_literal_identity_anchor, claim_normalized_literal_identity_anchor
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [4, 8]
- proxy rows: 0/336

## Proxy Mapping

- `halu_02, halu_03, halu_04, halu_05, halu_08, halu_14`: `literal_identity_anchor` now comes from the exact closure artifact.
- On that same stress-context subset, `normalized_literal_identity_anchor` and `claim_normalized_literal_identity_anchor` reuse the exact literal rows as `contract_equivalent_exact`, because their extra aligned-name rewrite never fires there.

## typed_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.357 | 0.643 | 0.714 | 0.000 | 0.643 | 0.000 | 0.643 | 0.500 | 0.000 | 0.1983 |
| 8 | 0.357 | 0.643 | 0.714 | 0.000 | 0.643 | 0.000 | 0.500 | 0.571 | 0.071 | 0.3679 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.357 | 0.000 | 0.357 | 0.643 | 0.500 | 0.000 | 0.1983 |
| 8 | 1.000 | 0.000 | 0.000 | 0.286 | 0.000 | 0.286 | 0.500 | 0.571 | 0.071 | 0.3679 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.071 | 0.000 | 0.071 | 0.643 | 0.500 | 0.000 | 0.1983 |
| 8 | 1.000 | 0.000 | 0.000 | 0.143 | 0.000 | 0.143 | 0.500 | 0.571 | 0.071 | 0.3679 |

## literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.643 | 0.357 | 0.500 | 0.000 | 0.357 | 0.000 | 0.214 | 0.071 | 0.000 | 0.1960 |
| 8 | 0.643 | 0.357 | 0.429 | 0.000 | 0.357 | 0.000 | 0.357 | 0.071 | 0.071 | 0.3858 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.143 | 0.000 | 0.143 | 0.214 | 0.071 | 0.000 | 0.1960 |
| 8 | 1.000 | 0.000 | 0.000 | 0.214 | 0.000 | 0.214 | 0.357 | 0.071 | 0.071 | 0.3858 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.071 | 0.000 | 0.071 | 0.214 | 0.071 | 0.000 | 0.1960 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.357 | 0.071 | 0.071 | 0.3858 |

## normalized_literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.643 | 0.357 | 0.500 | 0.000 | 0.357 | 0.000 | 0.214 | 0.071 | 0.000 | 0.1960 |
| 8 | 0.643 | 0.357 | 0.429 | 0.000 | 0.357 | 0.000 | 0.357 | 0.071 | 0.071 | 0.3858 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.143 | 0.000 | 0.143 | 0.214 | 0.071 | 0.000 | 0.1960 |
| 8 | 1.000 | 0.000 | 0.000 | 0.214 | 0.000 | 0.214 | 0.357 | 0.071 | 0.071 | 0.3858 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.071 | 0.000 | 0.071 | 0.214 | 0.071 | 0.000 | 0.1960 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.357 | 0.071 | 0.071 | 0.3858 |

## claim_normalized_literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.643 | 0.357 | 0.500 | 0.000 | 0.357 | 0.000 | 0.214 | 0.143 | 0.000 | 0.1960 |
| 8 | 0.643 | 0.357 | 0.429 | 0.000 | 0.357 | 0.000 | 0.357 | 0.214 | 0.071 | 0.3858 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.143 | 0.000 | 0.143 | 0.214 | 0.143 | 0.000 | 0.1960 |
| 8 | 1.000 | 0.000 | 0.000 | 0.214 | 0.000 | 0.214 | 0.357 | 0.214 | 0.071 | 0.3858 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.071 | 0.000 | 0.071 | 0.214 | 0.143 | 0.000 | 0.1960 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.357 | 0.214 | 0.071 | 0.3858 |

## Claim Reintegration Readout

- Unified N=8 false_present: typed/literal/normalized/claim = `0.286` / `0.214` / `0.214` / `0.214`.
- Note-aware N=8 false_present: typed/literal/normalized/claim = `0.143` / `0.000` / `0.000` / `0.000`.
- Broad literal unified N=8 on relation items: literal `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, claim `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Broad literal unified N=8 on stress-context items: literal `signal=1/6, tent=1/6, raw=0/6, scaffold=5/6`, claim `signal=1/6, tent=1/6, raw=0/6, scaffold=5/6`.
- Broad literal unified N=8 on code items: literal `signal=1/2, tent=0/2, raw=1/2, scaffold=2/2`, claim `signal=1/2, tent=0/2, raw=1/2, scaffold=2/2`.
- Broad literal unified N=8 on weak-name items: literal `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`, claim `signal=0/2, tent=0/2, raw=0/2, scaffold=2/2`.
- Broad literal unified N=8 on strengthened-name items: literal `signal=2/2, tent=0/2, raw=2/2, scaffold=1/2`, normalized `signal=2/2, tent=0/2, raw=2/2, scaffold=2/2`, claim `signal=2/2, tent=2/2, raw=2/2, scaffold=2/2`.
- Summary-only N=8 realism: literal/normalized/claim = `0.643` / `0.643` / `0.643`.
