# Note-Aware Detector Round Summary

这一轮只做 detector，不再改 compactor。目标是利用 note-level inference / missingness marker，压低 hallucination-side false-present recover。

## tiered

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | benign_false_absent |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.988 | 0.013 | 0.388 | 0.562 | 2.080 | 0.212 | 0.850 | 0.050 |
| 2 | 1.000 | 0.000 | 0.588 | 0.713 | 2.500 | 0.212 | 0.850 | 0.000 |
| 4 | 0.975 | 0.025 | 0.775 | 0.812 | 3.020 | 0.212 | 0.850 | 0.100 |
| 8 | 0.950 | 0.050 | 0.875 | 0.912 | 3.900 | 0.237 | 0.950 | 0.200 |

## utility_calibrated

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | benign_false_absent |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.075 | 1.500 | 0.013 | 0.050 | 0.000 |
| 2 | 0.975 | 0.025 | 0.000 | 0.188 | 1.860 | 0.037 | 0.150 | 0.100 |
| 4 | 0.988 | 0.013 | 0.000 | 0.312 | 2.420 | 0.087 | 0.350 | 0.050 |
| 8 | 0.975 | 0.025 | 0.000 | 0.463 | 3.380 | 0.100 | 0.400 | 0.100 |

## scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | benign_false_absent |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.075 | 1.520 | 0.013 | 0.050 | 0.000 |
| 2 | 1.000 | 0.000 | 0.000 | 0.212 | 1.920 | 0.037 | 0.150 | 0.000 |
| 4 | 0.988 | 0.013 | 0.000 | 0.312 | 2.420 | 0.087 | 0.350 | 0.050 |
| 8 | 0.975 | 0.025 | 0.000 | 0.463 | 3.380 | 0.100 | 0.400 | 0.100 |

## scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_present | hallucination_false_present | benign_false_absent |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.000 | 0.000 | 0.062 | 1.500 | 0.000 | 0.000 | 0.000 |
| 2 | 0.975 | 0.025 | 0.000 | 0.150 | 1.820 | 0.000 | 0.000 | 0.100 |
| 4 | 0.975 | 0.025 | 0.000 | 0.212 | 2.260 | 0.000 | 0.000 | 0.100 |
| 8 | 0.963 | 0.037 | 0.000 | 0.350 | 3.200 | 0.000 | 0.000 | 0.150 |

## Readout

- `scale_aware_note_aware` 的目标不是发明新 policy，而是在不破坏 unified skeleton 的前提下，让 hallucination note 的 recover 更谨慎。
- 最关键的看点是 `hallucination_false_present_rate` 能否在 `N=4/8` 明显下降，同时 `benign_false_absent_rate` 不要反弹过多。
