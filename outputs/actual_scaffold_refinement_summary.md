# Actual Scaffold Refinement Summary

这一轮不再搜索新 scaffold family，而是只精修当前赢家 `tiny_fixed_scaffold`，专门修 unsafe refusal 语义。

- slice items: 12
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- interventions: tiny_fixed_scaffold, tiny_refusal_scaffold
- N: [4, 8]

## summary_only

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | unsafe_compact_refuse | mean_note_tokens | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_fixed_scaffold | 4 | 0.750 | 0.167 | 0.167 | 0.000 | 0.125 | 0.875 | 0.875 | 1.000 | 0.000 | 12.50 | 0.1743 |
| tiny_fixed_scaffold | 8 | 0.417 | 0.333 | 0.083 | 0.000 | 0.625 | 0.375 | 0.375 | 1.000 | 0.000 | 12.50 | 0.3145 |
| tiny_refusal_scaffold | 4 | 0.667 | 0.333 | 0.083 | 0.000 | 0.250 | 0.750 | 0.625 | 0.500 | 0.500 | 9.42 | 0.1785 |
| tiny_refusal_scaffold | 8 | 0.417 | 0.417 | 0.000 | 0.000 | 0.625 | 0.375 | 0.375 | 0.500 | 0.500 | 7.00 | 0.3560 |

## scale_aware_unified

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | unsafe_compact_refuse | mean_note_tokens | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_fixed_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.083 | 0.125 | 0.875 | 0.875 | 1.000 | 0.000 | 12.50 | 0.1743 |
| tiny_fixed_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 1.000 | 0.000 | 12.50 | 0.3145 |
| tiny_refusal_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.500 | 9.42 | 0.1785 |
| tiny_refusal_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.500 | 7.00 | 0.3560 |

## scale_aware_note_aware

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | unsafe_compact_refuse | mean_note_tokens | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_fixed_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.083 | 0.125 | 0.875 | 0.875 | 1.000 | 0.000 | 12.50 | 0.1743 |
| tiny_fixed_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 1.000 | 0.000 | 12.50 | 0.3145 |
| tiny_refusal_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.500 | 9.42 | 0.1785 |
| tiny_refusal_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.500 | 7.00 | 0.3560 |

## Readout

- 这一轮的目标不是再提高一般性的 target retention，而是看能否修掉 tiny scaffold 在 unsafe refusal 上的精度损失。
- 如果 refined scaffold 能恢复 unsafe accuracy，同时保住 `history_loss` 和更低 raw fallback，它就会成为新的主线 scaffold。
