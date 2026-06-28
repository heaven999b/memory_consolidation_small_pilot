# Actual Carry Forward Summary

这一轮固定 refined scaffold prompt 和 placeholder hardening，只增加一个窄的 carry-forward rule 来修空/null unsafe passes。

- slice items: 12
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- interventions: tiny_placeholder_hardened_scaffold, tiny_carry_forward_scaffold
- N: [4, 8]

## summary_only

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | hallucination_placeholder | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_placeholder_hardened_scaffold | 4 | 0.750 | 0.250 | 0.083 | 0.000 | 0.250 | 0.750 | 0.625 | 0.500 | 0.000 | 0.000 | 0.1785 |
| tiny_placeholder_hardened_scaffold | 8 | 0.500 | 0.333 | 0.000 | 0.000 | 0.625 | 0.375 | 0.375 | 0.500 | 0.000 | 0.000 | 0.3560 |
| tiny_carry_forward_scaffold | 4 | 0.833 | 0.167 | 0.083 | 0.000 | 0.250 | 0.750 | 0.625 | 0.000 | 0.000 | 0.083 | 0.1785 |
| tiny_carry_forward_scaffold | 8 | 0.583 | 0.250 | 0.000 | 0.000 | 0.625 | 0.375 | 0.375 | 0.000 | 0.000 | 0.167 | 0.3560 |

## scale_aware_unified

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | hallucination_placeholder | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_placeholder_hardened_scaffold | 4 | 0.917 | 0.083 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.000 | 0.000 | 0.1785 |
| tiny_placeholder_hardened_scaffold | 8 | 0.917 | 0.083 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.000 | 0.000 | 0.3560 |
| tiny_carry_forward_scaffold | 4 | 1.000 | 0.000 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.000 | 0.000 | 0.083 | 0.1785 |
| tiny_carry_forward_scaffold | 8 | 1.000 | 0.000 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.000 | 0.000 | 0.167 | 0.3560 |

## scale_aware_note_aware

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | hallucination_placeholder | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_placeholder_hardened_scaffold | 4 | 0.917 | 0.083 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.500 | 0.000 | 0.000 | 0.1785 |
| tiny_placeholder_hardened_scaffold | 8 | 0.917 | 0.083 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.500 | 0.000 | 0.000 | 0.3560 |
| tiny_carry_forward_scaffold | 4 | 1.000 | 0.000 | 0.000 | 0.250 | 0.375 | 0.750 | 0.625 | 0.000 | 0.000 | 0.083 | 0.1785 |
| tiny_carry_forward_scaffold | 8 | 1.000 | 0.000 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.000 | 0.000 | 0.167 | 0.3560 |

## Readout

- 这一轮只看一个问题：空/null unsafe pass 能不能通过 carry-forward 保住已有 refusal scaffold。
- 如果 carry-forward 能把 unsafe_error 再压下去，同时不破坏 placeholder hardening 和高-N frontier，就说明当前主线已经进入 executor-level robustness 阶段。
