# Small-N Hybrid Summary

这一轮是一个 focused experiment：只看 `N in {1, 2}`，测试是否能在小 N 区间借用 tiered-style shield 修补 cleanup policy 的窄带 miss。

## tiered

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | guardband |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.392 | 0.796 | 2.454 | 0.000 | 0.254 | 0.000 |
| 2 | 0.992 | 0.008 | 0.588 | 0.835 | 2.695 | 0.008 | 0.262 | 0.000 |

| family @ N=2 | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.967 | 0.033 | 0.317 |
| conflict | 1.000 | 0.000 | 1.000 |
| hallucination | 1.000 | 0.000 | 0.971 |
| unsafe | 1.000 | 0.000 | 1.000 |

## utility_calibrated

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | guardband |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.996 | 0.004 | 0.000 | 0.138 | 1.602 | 0.004 | 0.035 | 0.000 |
| 2 | 0.992 | 0.008 | 0.000 | 0.319 | 2.071 | 0.008 | 0.088 | 0.000 |

| family @ N=2 | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 0.967 | 0.033 | 0.317 |
| conflict | 1.000 | 0.000 | 0.586 |
| hallucination | 1.000 | 0.000 | 0.329 |
| unsafe | 1.000 | 0.000 | 0.000 |

## small_n_hybrid

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | guardband |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.146 | 1.634 | 0.000 | 0.038 | 0.008 |
| 2 | 1.000 | 0.000 | 0.000 | 0.331 | 2.109 | 0.000 | 0.092 | 0.012 |

| family @ N=2 | accuracy | propagation | raw_escalation |
|---|---:|---:|---:|
| benign | 1.000 | 0.000 | 0.350 |
| conflict | 1.000 | 0.000 | 0.586 |
| hallucination | 1.000 | 0.000 | 0.343 |
| unsafe | 1.000 | 0.000 | 0.000 |

## Headline Comparison

- `small_n_hybrid` should be judged only on `N=1/2`; it is not intended as a new high-`N` global policy.
- The key question is whether it can match `tiered`'s perfect small-`N` shielding while keeping cleanup-style zero residual contamination and much lower raw escalation.

