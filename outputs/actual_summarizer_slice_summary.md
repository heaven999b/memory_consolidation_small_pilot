# Actual Summarizer Slice Summary

这一轮把 textual proxy 换成真实模型-backed summarizer。输入在每一轮只看到上一轮 note + claims，因此 drift 来自真实摘要器而不是手写规则。

- slice items: 8
- seeds: [11]
- architectures: summary_only, tiered, scale_aware_unified, scale_aware_note_aware
- N: [1, 2, 4, 8]

## summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.750 | 0.250 | 0.250 | 0.000 | 1.180 | 0.000 | 0.000 | 0.0356 |
| 2 | 0.625 | 0.375 | 0.250 | 0.000 | 1.360 | 0.000 | 0.000 | 0.0808 |
| 4 | 0.250 | 0.500 | 0.125 | 0.000 | 1.720 | 0.000 | 0.000 | 0.1459 |
| 8 | 0.125 | 0.625 | 0.125 | 0.000 | 2.440 | 0.000 | 0.000 | 0.2618 |

## tiered

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.250 | 0.750 | 2.380 | 0.250 | 1.000 | 0.0356 |
| 2 | 0.875 | 0.125 | 0.250 | 0.500 | 2.160 | 0.125 | 0.500 | 0.0808 |
| 4 | 0.875 | 0.125 | 0.125 | 0.750 | 2.920 | 0.125 | 0.500 | 0.1459 |
| 8 | 0.750 | 0.250 | 0.125 | 0.750 | 3.640 | 0.125 | 0.500 | 0.2618 |

## scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.000 | 1.400 | 0.000 | 0.000 | 0.0356 |
| 2 | 0.750 | 0.250 | 0.000 | 0.000 | 1.580 | 0.000 | 0.000 | 0.0808 |
| 4 | 0.625 | 0.375 | 0.000 | 0.375 | 2.520 | 0.000 | 0.000 | 0.1459 |
| 8 | 0.625 | 0.375 | 0.000 | 0.500 | 3.440 | 0.000 | 0.000 | 0.2618 |

## scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.000 | 1.400 | 0.000 | 0.000 | 0.0356 |
| 2 | 0.750 | 0.250 | 0.000 | 0.000 | 1.580 | 0.000 | 0.000 | 0.0808 |
| 4 | 0.625 | 0.375 | 0.000 | 0.375 | 2.520 | 0.000 | 0.000 | 0.1459 |
| 8 | 0.625 | 0.375 | 0.000 | 0.500 | 3.440 | 0.000 | 0.000 | 0.2618 |

## Readout

- 这不是大样本 benchmark，而是一个真实 summarizer realism checkpoint。
- 如果 `summary_only` 仍随 `N` 恶化，而 `scale_aware_unified` / `scale_aware_note_aware` 继续优于 `tiered`，说明主线结论已经不只活在手写 proxy 里。
- 如果 `scale_aware_note_aware` 还能进一步压 hallucination-side false-present，就说明 detector round 也开始跨环境稳定。
