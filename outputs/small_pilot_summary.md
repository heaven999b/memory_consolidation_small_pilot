# Small Pilot Summary

这是一个受控合成 pre-pilot，不是正式 benchmark 结论。

- items: 52
- seeds: 5
- architectures: raw_only, summary_only, tiered, adaptive_tiered, adaptive_guarded, risk_first, utility_first, utility_calibrated, small_n_hybrid, scale_aware_unified
- N: [0, 1, 2, 4, 8]

## Aggregate Readout

### raw_only

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 3.200 |
| 1 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 3.200 |
| 2 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 3.200 |
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 3.200 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 3.200 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 1.000 | 0.000 | 1.000 |
| conflict | 1.000 | 0.000 | 1.000 |
| hallucination | 1.000 | 0.000 | 1.000 |
| unsafe | 1.000 | 0.000 | 1.000 |

### summary_only

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.769 | 0.000 | 0.231 | 0.000 | 0.231 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.231 | 0.000 | 0.000 | 0.000 | 1.000 |
| 1 | 0.588 | 0.096 | 0.231 | 0.065 | 0.412 | 0.123 | 0.231 | 0.243 | 0.183 | 0.392 | 0.392 | 0.000 | 0.000 | 0.000 | 1.180 |
| 2 | 0.369 | 0.200 | 0.231 | 0.158 | 0.631 | 0.285 | 0.231 | 0.586 | 0.350 | 0.588 | 0.588 | 0.000 | 0.000 | 0.000 | 1.360 |
| 4 | 0.131 | 0.323 | 0.231 | 0.254 | 0.869 | 0.450 | 0.231 | 0.943 | 0.667 | 0.808 | 0.808 | 0.000 | 0.000 | 0.000 | 1.720 |
| 8 | 0.004 | 0.427 | 0.231 | 0.269 | 0.996 | 0.538 | 0.231 | 1.000 | 0.983 | 0.927 | 0.927 | 0.000 | 0.000 | 0.000 | 2.440 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.017 | 0.983 | 0.000 |
| conflict | 0.000 | 1.000 | 0.000 |
| hallucination | 0.000 | 1.000 | 0.000 |
| unsafe | 0.000 | 1.000 | 0.000 |

### tiered

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.231 | 0.231 | 0.000 | 0.750 | 2.200 |
| 1 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.123 | 0.231 | 0.243 | 0.000 | 0.392 | 0.392 | 0.392 | 0.000 | 0.796 | 2.454 |
| 2 | 0.992 | 0.000 | 0.000 | 0.000 | 0.008 | 0.285 | 0.231 | 0.586 | 0.033 | 0.588 | 0.588 | 0.588 | 0.000 | 0.835 | 2.695 |
| 4 | 0.977 | 0.000 | 0.000 | 0.000 | 0.023 | 0.450 | 0.231 | 0.943 | 0.100 | 0.808 | 0.808 | 0.808 | 0.000 | 0.900 | 3.160 |
| 8 | 0.977 | 0.000 | 0.000 | 0.000 | 0.023 | 0.538 | 0.231 | 1.000 | 0.100 | 0.927 | 0.927 | 0.927 | 0.000 | 0.973 | 3.997 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.900 | 0.100 | 0.883 |
| conflict | 1.000 | 0.000 | 1.000 |
| hallucination | 1.000 | 0.000 | 1.000 |
| unsafe | 1.000 | 0.000 | 1.000 |

### adaptive_tiered

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.231 | 0.231 | 0.000 | 0.750 | 2.300 |
| 1 | 0.981 | 0.019 | 0.000 | 0.000 | 0.019 | 0.123 | 0.231 | 0.243 | 0.000 | 0.392 | 0.392 | 0.373 | 0.000 | 0.777 | 2.523 |
| 2 | 0.946 | 0.054 | 0.000 | 0.000 | 0.054 | 0.285 | 0.231 | 0.586 | 0.000 | 0.588 | 0.588 | 0.535 | 0.000 | 0.788 | 2.722 |
| 4 | 0.927 | 0.073 | 0.000 | 0.000 | 0.073 | 0.450 | 0.231 | 0.943 | 0.000 | 0.808 | 0.808 | 0.735 | 0.000 | 0.850 | 3.180 |
| 8 | 0.773 | 0.227 | 0.000 | 0.000 | 0.227 | 0.538 | 0.231 | 1.000 | 0.650 | 0.927 | 0.927 | 0.700 | 0.000 | 0.769 | 3.771 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.350 | 0.650 | 0.333 |
| conflict | 1.000 | 0.000 | 1.000 |
| hallucination | 0.714 | 0.286 | 0.714 |
| unsafe | 1.000 | 0.000 | 1.000 |

### adaptive_guarded

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.231 | 0.231 | 0.000 | 0.769 | 2.381 |
| 1 | 0.977 | 0.023 | 0.000 | 0.000 | 0.023 | 0.123 | 0.231 | 0.243 | 0.100 | 0.392 | 0.392 | 0.369 | 0.000 | 0.788 | 2.592 |
| 2 | 0.962 | 0.038 | 0.000 | 0.000 | 0.038 | 0.285 | 0.231 | 0.586 | 0.167 | 0.588 | 0.588 | 0.550 | 0.000 | 0.812 | 2.808 |
| 4 | 0.777 | 0.108 | 0.000 | 0.115 | 0.223 | 0.450 | 0.231 | 0.943 | 0.400 | 0.808 | 0.808 | 0.585 | 0.000 | 0.700 | 2.990 |
| 8 | 0.665 | 0.177 | 0.000 | 0.158 | 0.335 | 0.538 | 0.231 | 1.000 | 0.683 | 0.927 | 0.927 | 0.592 | 0.000 | 0.662 | 3.648 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.317 | 0.683 | 0.300 |
| conflict | 0.414 | 0.586 | 0.414 |
| hallucination | 0.929 | 0.071 | 0.929 |
| unsafe | 1.000 | 0.000 | 1.000 |

### risk_first

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.000 | 1.120 |
| 1 | 0.969 | 0.000 | 0.000 | 0.008 | 0.023 | 0.000 | 0.000 | 0.000 | 0.100 | 0.392 | 0.000 | 0.065 | 0.392 | 0.077 | 1.423 |
| 2 | 0.946 | 0.000 | 0.000 | 0.000 | 0.054 | 0.000 | 0.000 | 0.000 | 0.233 | 0.588 | 0.000 | 0.162 | 0.588 | 0.185 | 1.775 |
| 4 | 0.885 | 0.000 | 0.000 | 0.008 | 0.108 | 0.000 | 0.000 | 0.000 | 0.467 | 0.808 | 0.000 | 0.277 | 0.808 | 0.292 | 2.308 |
| 8 | 0.835 | 0.000 | 0.000 | 0.008 | 0.158 | 0.000 | 0.000 | 0.000 | 0.683 | 0.927 | 0.000 | 0.300 | 0.927 | 0.331 | 3.089 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.317 | 0.683 | 0.300 |
| conflict | 0.971 | 0.000 | 0.971 |
| hallucination | 1.000 | 0.000 | 0.000 |
| unsafe | 1.000 | 0.000 | 0.000 |

### utility_first

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.000 | 1.180 |
| 1 | 0.988 | 0.000 | 0.000 | 0.008 | 0.004 | 0.000 | 0.000 | 0.000 | 0.017 | 0.392 | 0.000 | 0.112 | 0.392 | 0.131 | 1.569 |
| 2 | 0.992 | 0.000 | 0.000 | 0.000 | 0.008 | 0.000 | 0.000 | 0.000 | 0.033 | 0.588 | 0.000 | 0.277 | 0.588 | 0.319 | 2.051 |
| 4 | 0.988 | 0.000 | 0.000 | 0.008 | 0.004 | 0.000 | 0.000 | 0.000 | 0.017 | 0.808 | 0.000 | 0.442 | 0.808 | 0.504 | 2.706 |
| 8 | 0.973 | 0.000 | 0.000 | 0.008 | 0.019 | 0.000 | 0.000 | 0.000 | 0.083 | 0.927 | 0.000 | 0.523 | 0.927 | 0.588 | 3.562 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.917 | 0.083 | 0.900 |
| conflict | 0.971 | 0.000 | 0.971 |
| hallucination | 1.000 | 0.000 | 0.443 |
| unsafe | 1.000 | 0.000 | 0.000 |

### utility_calibrated

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.000 | 1.200 |
| 1 | 0.996 | 0.000 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 0.000 | 0.017 | 0.392 | 0.000 | 0.119 | 0.392 | 0.138 | 1.602 |
| 2 | 0.992 | 0.000 | 0.000 | 0.000 | 0.008 | 0.000 | 0.000 | 0.000 | 0.033 | 0.588 | 0.000 | 0.277 | 0.588 | 0.319 | 2.071 |
| 4 | 0.996 | 0.000 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 0.000 | 0.017 | 0.808 | 0.000 | 0.450 | 0.808 | 0.512 | 2.738 |
| 8 | 0.985 | 0.000 | 0.000 | 0.000 | 0.015 | 0.000 | 0.000 | 0.000 | 0.067 | 0.927 | 0.000 | 0.531 | 0.927 | 0.600 | 3.600 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.933 | 0.067 | 0.917 |
| conflict | 1.000 | 0.000 | 1.000 |
| hallucination | 1.000 | 0.000 | 0.443 |
| unsafe | 1.000 | 0.000 | 0.000 |

### small_n_hybrid

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.000 | 1.220 |
| 1 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.392 | 0.000 | 0.127 | 0.392 | 0.146 | 1.634 |
| 2 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.588 | 0.000 | 0.288 | 0.588 | 0.331 | 2.109 |
| 4 | 0.996 | 0.000 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 0.000 | 0.017 | 0.808 | 0.000 | 0.450 | 0.808 | 0.512 | 2.758 |
| 8 | 0.985 | 0.000 | 0.000 | 0.000 | 0.015 | 0.000 | 0.000 | 0.000 | 0.067 | 0.927 | 0.000 | 0.531 | 0.927 | 0.600 | 3.620 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.933 | 0.067 | 0.917 |
| conflict | 1.000 | 0.000 | 1.000 |
| hallucination | 1.000 | 0.000 | 0.443 |
| unsafe | 1.000 | 0.000 | 0.000 |

### scale_aware_unified

| N | accuracy | unsupported_answer | unsafe_answer | conflict_answer | propagation | unsupported_new_memory | unsafe_retention | conflict_merge | benign_overcompression | latent_bad_memory | residual_bad_memory | shielded_bad_memory | cleaned_bad_memory | raw_escalation | mean_cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.231 | 0.000 | 0.000 | 0.231 | 0.000 | 1.220 |
| 1 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.392 | 0.000 | 0.127 | 0.392 | 0.146 | 1.634 |
| 2 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.588 | 0.000 | 0.288 | 0.588 | 0.331 | 2.109 |
| 4 | 0.996 | 0.000 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 0.000 | 0.017 | 0.808 | 0.000 | 0.450 | 0.808 | 0.512 | 2.738 |
| 8 | 0.985 | 0.000 | 0.000 | 0.000 | 0.015 | 0.000 | 0.000 | 0.000 | 0.067 | 0.927 | 0.000 | 0.531 | 0.927 | 0.600 | 3.600 |

Family breakdown:

| family | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.933 | 0.067 | 0.917 |
| conflict | 1.000 | 0.000 | 1.000 |
| hallucination | 1.000 | 0.000 | 0.443 |
| unsafe | 1.000 | 0.000 | 0.000 |

## Candidate Pareto Frontier

| architecture | N | accuracy | propagation | mean_cost |
|---|---:|---:|---:|---:|
| risk_first | 0 | 1.000 | 0.000 | 1.120 |
| summary_only | 0 | 0.769 | 0.231 | 1.000 |

## Matched-N Best Non-Raw Policy

这个表只在相同 `N` 下比较非 `raw_only` 条件：先选最低 propagation，再选最高 accuracy、最低 residual contamination、最低 cost。

| N | architecture | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost |
|---|---|---:|---:|---:|---:|---:|
| 0 | risk_first | 1.000 | 0.000 | 0.000 | 0.000 | 1.120 |
| 1 | small_n_hybrid | 1.000 | 0.000 | 0.000 | 0.146 | 1.634 |
| 2 | small_n_hybrid | 1.000 | 0.000 | 0.000 | 0.331 | 2.109 |
| 4 | utility_calibrated | 0.996 | 0.004 | 0.000 | 0.512 | 2.738 |
| 8 | utility_calibrated | 0.985 | 0.015 | 0.000 | 0.600 | 3.600 |

## What To Look For

- `summary_only` 的 unsupported / unsafe / conflict 风险是否随 `N` 上升。
- `tiered` 是否明显压低 propagation-to-answer，同时带来 raw escalation 成本。
- `risk_first` / `utility_first` 能不能通过 scrub policy 把 latent contamination 变成更低的 residual contamination。
- `utility_calibrated` 能不能通过 detector calibration 修补 `utility_first` 在低 N 的 recall miss，同时保留 cleanup policy 的低 residual contamination。
- `scale_aware_unified` 能不能把 `small_n_hybrid` 的低-N 优势和 `utility_calibrated` 的高-N 优势拼成一个全 sweep 结构化策略。
- `raw_only` 是否提供接近 risk floor 的上界。

## Caveat

这个结果只能说明当前实验 framing 和指标在小样本合成环境下是可运行的，不代表真实模型一定表现相同。
