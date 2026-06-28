# Actual Hallucination Stress Summary

这一轮不是普通 actual slice，而是更难的 hallucination stress 条件：真实 summarizer 被允许保留 tentative clue，从而专门测试 detector transfer。

- slice items: 8
- seeds: [11, 23]
- architectures: summary_only, tiered, scale_aware_unified, scale_aware_note_aware
- N: [1, 4, 8]

## summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.750 | 0.250 | 0.250 | 0.000 | 0.250 | 0.000 | 0.125 | 0.0370 |
| 4 | 0.750 | 0.250 | 0.250 | 0.000 | 0.250 | 0.000 | 0.000 | 0.1764 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.2875 |

## tiered

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.250 | 1.000 | 0.000 | 1.000 | 0.125 | 0.0370 |
| 4 | 1.000 | 0.000 | 0.250 | 1.000 | 0.000 | 1.000 | 0.000 | 0.1764 |
| 8 | 1.000 | 0.000 | 0.000 | 0.875 | 0.000 | 0.875 | 0.000 | 0.2875 |

## scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.125 | 0.000 | 0.125 | 0.125 | 0.0370 |
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.1764 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.2875 |

## scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.062 | 0.000 | 0.062 | 0.125 | 0.0370 |
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.1764 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.2875 |

## Readout

- 这个 round 的关键不是 overall accuracy，而是看真实 summarizer 在更激进压缩时会不会重新暴露 detector round 针对的 hallucination-side recover 误报。
- 如果 `scale_aware_note_aware` 能在 `false_present` 上明显低于 `scale_aware_unified`，就说明 detector gain 不只活在 textual proxy 里。
