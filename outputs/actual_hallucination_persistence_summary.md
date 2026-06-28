# Actual Hallucination Persistence Summary

这一轮把更强的 scaffold/parser/executor contract 带回 actual hallucination stress，测试 tentative clue 能否跨更多压缩轮次活下来。

- slice items: 8
- seeds: [11]
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [1, 4, 8]

## summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.750 | 0.000 | 0.0468 |
| 4 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.875 | 0.125 | 0.1657 |
| 8 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.875 | 0.250 | 0.3433 |

## scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 1.000 | 0.750 | 0.000 | 0.0468 |
| 4 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 1.000 | 0.875 | 0.125 | 0.1657 |
| 8 | 1.000 | 0.000 | 0.000 | 0.375 | 0.000 | 0.375 | 1.000 | 0.875 | 0.250 | 0.3433 |

## scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.750 | 0.000 | 0.0468 |
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.875 | 0.125 | 0.1657 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.875 | 0.250 | 0.3433 |

## Readout

- 这一轮的关键不是 recall，而是 stronger scaffold contract 会不会让 actual stress clue 在 N=4/8 仍然可见。
- 如果 `scale_aware_note_aware` 在更高 N 重新低于 `scale_aware_unified` 的 false_present，就说明 detector transfer 已经不再只是局部 N=1 现象。
