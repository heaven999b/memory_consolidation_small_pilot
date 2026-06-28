# Actual Placeholder Hardening Summary

这一轮不改 refined scaffold prompt，只硬化 parser/normalization，专门消灭 `MISSING` 这类 placeholder target answer。

- slice items: 12
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- interventions: tiny_refusal_scaffold, tiny_placeholder_hardened_scaffold
- N: [4, 8]

## summary_only

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | placeholder_answer | hallucination_placeholder | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_refusal_scaffold | 4 | 0.667 | 0.333 | 0.083 | 0.000 | 0.250 | 0.750 | 0.625 | 0.500 | 0.083 | 0.500 | 0.1785 |
| tiny_refusal_scaffold | 8 | 0.417 | 0.417 | 0.000 | 0.000 | 0.625 | 0.375 | 0.375 | 0.500 | 0.083 | 0.500 | 0.3560 |
| tiny_placeholder_hardened_scaffold | 4 | 0.750 | 0.250 | 0.083 | 0.000 | 0.250 | 0.750 | 0.625 | 0.500 | 0.000 | 0.000 | 0.1785 |
| tiny_placeholder_hardened_scaffold | 8 | 0.500 | 0.333 | 0.000 | 0.000 | 0.625 | 0.375 | 0.375 | 0.500 | 0.000 | 0.000 | 0.3560 |

## scale_aware_unified

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | placeholder_answer | hallucination_placeholder | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_refusal_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.083 | 0.500 | 0.1785 |
| tiny_refusal_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.083 | 0.500 | 0.3560 |
| tiny_placeholder_hardened_scaffold | 4 | 0.917 | 0.083 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.000 | 0.000 | 0.1785 |
| tiny_placeholder_hardened_scaffold | 8 | 0.917 | 0.083 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.000 | 0.000 | 0.3560 |

## scale_aware_note_aware

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | placeholder_answer | hallucination_placeholder | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_refusal_scaffold | 4 | 0.833 | 0.167 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.083 | 0.500 | 0.1785 |
| tiny_refusal_scaffold | 8 | 0.833 | 0.167 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.083 | 0.500 | 0.3560 |
| tiny_placeholder_hardened_scaffold | 4 | 0.917 | 0.083 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.000 | 0.000 | 0.1785 |
| tiny_placeholder_hardened_scaffold | 8 | 0.917 | 0.083 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.000 | 0.000 | 0.3560 |

## Readout

- 这一轮只看一个问题：placeholder target answer 能不能在不损失 refined scaffold 其他收益的情况下被压回 `ABSTAIN`。
- 如果 hardened parser 同时提升 `N=8` accuracy 并把 hallucination placeholder 降到 0，就说明 frontier 已经从 prompt contract 转向 parser contract。
