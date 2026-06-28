# Textual Proxy Slice Summary

这一轮不是再改 policy，而是把环境向前推一步：在 16 条高质量 slice 上，用一个更接近自由文本摘要 note 的 compactor proxy 测试 `scale_aware_unified`。

- slice items: 16 (`4` per family)
- architectures: summary_only, tiered, utility_calibrated, scale_aware_unified
- N: [1, 2, 4, 8]

## Aggregate Readout

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | note_missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.650 | 0.350 | 0.388 | 0.000 | 1.180 | 0.013 | 0.000 | 0.225 |
| 2 | 0.487 | 0.512 | 0.588 | 0.000 | 1.360 | 0.000 | 0.000 | 0.163 |
| 4 | 0.325 | 0.675 | 0.775 | 0.000 | 1.720 | 0.037 | 0.000 | 0.100 |
| 8 | 0.125 | 0.875 | 0.875 | 0.000 | 2.440 | 0.087 | 0.000 | 0.100 |

| family @ N=8 | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.050 | 0.950 | 0.000 |
| conflict | 0.400 | 0.600 | 0.000 |
| hallucination | 0.050 | 0.950 | 0.000 |
| unsafe | 0.000 | 1.000 | 0.000 |

### tiered

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | note_missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.988 | 0.013 | 0.388 | 0.562 | 2.080 | 0.013 | 0.212 | 0.225 |
| 2 | 1.000 | 0.000 | 0.588 | 0.713 | 2.500 | 0.000 | 0.212 | 0.163 |
| 4 | 0.975 | 0.025 | 0.775 | 0.812 | 3.020 | 0.025 | 0.212 | 0.100 |
| 8 | 0.950 | 0.050 | 0.875 | 0.912 | 3.900 | 0.050 | 0.237 | 0.100 |

| family @ N=8 | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.800 | 0.200 | 0.750 |
| conflict | 1.000 | 0.000 | 0.950 |
| hallucination | 1.000 | 0.000 | 0.950 |
| unsafe | 1.000 | 0.000 | 1.000 |

### utility_calibrated

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | note_missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.075 | 1.500 | 0.000 | 0.013 | 0.225 |
| 2 | 0.975 | 0.025 | 0.000 | 0.188 | 1.860 | 0.025 | 0.037 | 0.163 |
| 4 | 0.988 | 0.013 | 0.000 | 0.312 | 2.420 | 0.013 | 0.087 | 0.100 |
| 8 | 0.975 | 0.025 | 0.000 | 0.463 | 3.380 | 0.025 | 0.100 | 0.100 |

| family @ N=8 | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.900 | 0.100 | 0.850 |
| conflict | 1.000 | 0.000 | 0.600 |
| hallucination | 1.000 | 0.000 | 0.400 |
| unsafe | 1.000 | 0.000 | 0.000 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | note_missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.075 | 1.520 | 0.000 | 0.013 | 0.225 |
| 2 | 1.000 | 0.000 | 0.000 | 0.212 | 1.920 | 0.000 | 0.037 | 0.163 |
| 4 | 0.988 | 0.013 | 0.000 | 0.312 | 2.420 | 0.013 | 0.087 | 0.100 |
| 8 | 0.975 | 0.025 | 0.000 | 0.463 | 3.380 | 0.025 | 0.100 | 0.100 |

| family @ N=8 | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.900 | 0.100 | 0.850 |
| conflict | 1.000 | 0.000 | 0.600 |
| hallucination | 1.000 | 0.000 | 0.400 |
| unsafe | 1.000 | 0.000 | 0.000 |

## Readout

- 关键问题不是 textual proxy 会不会复制主实验数字，而是 `scale_aware_unified` 的方向性优势是否还活着。
- 如果 `summary_only` 仍随 `N` 恶化，而 `scale_aware_unified` 仍能把 residual contamination 压到低位，同时避免 `tiered` 的高 raw fallback，那么说明主张开始跨环境稳定。
- 如果优势在这个 slice 上消失，就说明前一轮的 unified story 还没有穿过 realism check。
