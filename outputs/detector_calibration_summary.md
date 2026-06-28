# Detector Calibration Summary

这轮是一个结构化 detector-calibration iteration：不再新增 policy family，而是对 `utility_first` 的 noisy probe 做定向修补。

## tiered

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | uncertain_then_wrong | answerable_recovery |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.231 | 0.750 | 2.200 | 0.000 | 0.250 | 0.000 | 0.000 |
| 1 | 1.000 | 0.000 | 0.392 | 0.796 | 2.454 | 0.000 | 0.254 | 0.000 | 0.019 |
| 2 | 0.992 | 0.008 | 0.588 | 0.835 | 2.695 | 0.008 | 0.262 | 0.000 | 0.035 |
| 4 | 0.977 | 0.023 | 0.808 | 0.900 | 3.160 | 0.023 | 0.269 | 0.000 | 0.038 |
| 8 | 0.977 | 0.023 | 0.927 | 0.973 | 3.997 | 0.023 | 0.269 | 0.000 | 0.046 |

## risk_first

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | uncertain_then_wrong | answerable_recovery |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 1.120 | 0.000 | 0.000 | 0.000 | 0.000 |
| 1 | 0.969 | 0.023 | 0.000 | 0.077 | 1.423 | 0.031 | 0.000 | 0.023 | 0.077 |
| 2 | 0.946 | 0.054 | 0.000 | 0.185 | 1.775 | 0.054 | 0.000 | 0.038 | 0.185 |
| 4 | 0.885 | 0.108 | 0.000 | 0.292 | 2.308 | 0.115 | 0.000 | 0.073 | 0.292 |
| 8 | 0.835 | 0.158 | 0.000 | 0.331 | 3.089 | 0.165 | 0.000 | 0.127 | 0.331 |

## utility_first

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | uncertain_then_wrong | answerable_recovery |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 1.180 | 0.000 | 0.000 | 0.000 | 0.000 |
| 1 | 0.988 | 0.004 | 0.000 | 0.131 | 1.569 | 0.012 | 0.035 | 0.004 | 0.096 |
| 2 | 0.992 | 0.008 | 0.000 | 0.319 | 2.051 | 0.008 | 0.088 | 0.008 | 0.231 |
| 4 | 0.988 | 0.004 | 0.000 | 0.504 | 2.706 | 0.012 | 0.108 | 0.004 | 0.396 |
| 8 | 0.973 | 0.019 | 0.000 | 0.588 | 3.562 | 0.027 | 0.119 | 0.019 | 0.469 |

## utility_calibrated

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | uncertain_then_wrong | answerable_recovery |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 1.200 | 0.000 | 0.000 | 0.000 | 0.000 |
| 1 | 0.996 | 0.004 | 0.000 | 0.138 | 1.602 | 0.004 | 0.035 | 0.004 | 0.104 |
| 2 | 0.992 | 0.008 | 0.000 | 0.319 | 2.071 | 0.008 | 0.088 | 0.008 | 0.231 |
| 4 | 0.996 | 0.004 | 0.000 | 0.512 | 2.738 | 0.004 | 0.108 | 0.004 | 0.404 |
| 8 | 0.985 | 0.015 | 0.000 | 0.600 | 3.600 | 0.015 | 0.119 | 0.015 | 0.481 |

## Matched-N Best Calibrated Cleanup Policy

这个表只比较 `utility_first` 和 `utility_calibrated`，先选最低 propagation，再选最高 accuracy、最低 false_absent、最低 cost。

| N | architecture | accuracy | propagation | false_absent | false_present | raw_escalation | mean_cost |
|---|---|---:|---:|---:|---:|---:|---:|
| 0 | utility_first | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.180 |
| 1 | utility_calibrated | 0.996 | 0.004 | 0.004 | 0.035 | 0.138 | 1.602 |
| 2 | utility_first | 0.992 | 0.008 | 0.008 | 0.088 | 0.319 | 2.051 |
| 4 | utility_calibrated | 0.996 | 0.004 | 0.004 | 0.108 | 0.512 | 2.738 |
| 8 | utility_calibrated | 0.985 | 0.015 | 0.015 | 0.119 | 0.600 | 3.600 |

## Main Readout

- `utility_calibrated` 修补了 `utility_first` 在低分 conflict / benign case 上的部分 recall miss。
- 校准后最明显的提升出现在 `N=1`, `N=4`, `N=8`，同时保持 `residual_bad_memory_rate = 0.000`。
- `tiered` 仍然在 `N=1` 保持最强 answer-level shield，但它依然没有解决 residual contamination。
