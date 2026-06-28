# Actual Note Persistence Summary

这一轮固定真实 recall slice 和 routing skeleton，只替换 note 形式，测试 query-field scaffold 能否降低高 N 的 answerability evaporation。

- slice items: 12
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- interventions: baseline, target_field_anchor, tiny_fixed_scaffold
- N: [4, 8]

## summary_only

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note_then_abstain | history_loss | target_claim | supported_target | mean_note_tokens | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 4 | 0.500 | 0.333 | 0.250 | 0.000 | 0.500 | 0.125 | 0.500 | 0.500 | 0.500 | 19.25 | 0.1451 |
| baseline | 8 | 0.083 | 0.583 | 0.250 | 0.000 | 1.000 | 0.125 | 1.000 | 0.000 | 0.000 | 24.62 | 0.2637 |
| target_field_anchor | 4 | 0.250 | 0.417 | 0.083 | 0.000 | 0.875 | 0.750 | 0.875 | 0.125 | 0.125 | 2.75 | 0.1663 |
| target_field_anchor | 8 | 0.167 | 0.500 | 0.000 | 0.000 | 1.000 | 0.375 | 1.000 | 0.000 | 0.000 | 18.62 | 0.2901 |
| tiny_fixed_scaffold | 4 | 0.750 | 0.167 | 0.167 | 0.000 | 0.125 | 0.000 | 0.125 | 0.875 | 0.875 | 11.88 | 0.1743 |
| tiny_fixed_scaffold | 8 | 0.417 | 0.333 | 0.083 | 0.000 | 0.625 | 0.125 | 0.625 | 0.375 | 0.375 | 13.00 | 0.3145 |

## scale_aware_unified

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note_then_abstain | history_loss | target_claim | supported_target | mean_note_tokens | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 4 | 0.917 | 0.083 | 0.000 | 0.417 | 0.000 | 0.000 | 0.500 | 0.500 | 0.500 | 19.25 | 0.1451 |
| baseline | 8 | 0.917 | 0.083 | 0.000 | 0.667 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 24.62 | 0.2637 |
| target_field_anchor | 4 | 0.917 | 0.083 | 0.000 | 0.583 | 0.000 | 0.000 | 0.875 | 0.125 | 0.125 | 2.75 | 0.1663 |
| target_field_anchor | 8 | 0.833 | 0.167 | 0.000 | 0.667 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 18.62 | 0.2901 |
| tiny_fixed_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.083 | 0.000 | 0.000 | 0.125 | 0.875 | 0.875 | 11.88 | 0.1743 |
| tiny_fixed_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.000 | 0.000 | 0.625 | 0.375 | 0.375 | 13.00 | 0.3145 |

## scale_aware_note_aware

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note_then_abstain | history_loss | target_claim | supported_target | mean_note_tokens | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 4 | 0.917 | 0.083 | 0.000 | 0.417 | 0.000 | 0.000 | 0.500 | 0.500 | 0.500 | 19.25 | 0.1451 |
| baseline | 8 | 0.917 | 0.083 | 0.000 | 0.667 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 24.62 | 0.2637 |
| target_field_anchor | 4 | 0.917 | 0.083 | 0.000 | 0.583 | 0.000 | 0.000 | 0.875 | 0.125 | 0.125 | 2.75 | 0.1663 |
| target_field_anchor | 8 | 0.833 | 0.167 | 0.000 | 0.667 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 18.62 | 0.2901 |
| tiny_fixed_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.083 | 0.000 | 0.000 | 0.125 | 0.875 | 0.875 | 11.88 | 0.1743 |
| tiny_fixed_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.000 | 0.000 | 0.625 | 0.375 | 0.375 | 13.00 | 0.3145 |

## Readout

- 这一轮看的是 compaction structure，不是 detector threshold。
- 如果 anchor 或 scaffold 能在不抬高 residual contamination 的情况下压低 `history_loss` / `empty_note_then_abstain`，就说明真实瓶颈确实可以靠 memory scaffold 直接修。
