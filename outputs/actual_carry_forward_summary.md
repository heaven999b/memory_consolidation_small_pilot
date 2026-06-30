# Actual Carry Forward Summary

这一轮固定 refined scaffold prompt 和 placeholder hardening，把 carry-forward 从 unsafe refusal 扩成更一般的 query-slot scaffold recovery：当后续压缩把已有的有效 target slot 压成空或 missing 时，保住上一轮有效 scaffold。

- slice items: 12
- seeds: [11, 23]
- architectures: scale_aware_note_aware
- interventions: tiny_placeholder_hardened_scaffold, tiny_carry_forward_scaffold
- N: [4, 8]

## scale_aware_note_aware

| intervention | N | accuracy | propagation | residual_bad_memory | raw_escalation | history_loss | target_claim | supported_target | unsafe_error | hallucination_placeholder | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tiny_placeholder_hardened_scaffold | 4 | 0.917 | 0.083 | 0.000 | 0.208 | 0.312 | 0.750 | 0.688 | 0.500 | 0.000 | 0.000 | 0.1773 |
| tiny_placeholder_hardened_scaffold | 8 | 0.958 | 0.042 | 0.000 | 0.417 | 0.625 | 0.375 | 0.375 | 0.250 | 0.000 | 0.000 | 0.3439 |
| tiny_carry_forward_scaffold | 4 | 1.000 | 0.000 | 0.000 | 0.042 | 0.062 | 1.000 | 0.938 | 0.000 | 0.000 | 0.250 | 0.1773 |
| tiny_carry_forward_scaffold | 8 | 1.000 | 0.000 | 0.000 | 0.042 | 0.062 | 0.938 | 0.938 | 0.000 | 0.000 | 0.500 | 0.3439 |

## Readout

- 这一轮不再只看 unsafe refusal，而是同时看 benign/conflict 上的 target-slot 蒸发能不能被 query-slot carry-forward 压回去。
- 如果 carry-forward 能同时降低 `history_loss`、`raw_escalation` 和 `unsafe_error`，就说明 PSU 已经从 isolated patch 变成可放进 recall 主面板的完整 compaction contract。
