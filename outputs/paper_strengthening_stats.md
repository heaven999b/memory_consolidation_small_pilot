# Paper Strengthening Stats

这份工件补的是论文级统计层，不再只报单个 frozen table，而是对关键比较给出 paired bootstrap delta 和简单 slope 分析。

- bootstrap samples: 2000

## Paired Bootstrap

| Comparison | Pairs | Baseline | Treatment | Improvement Delta | 95% CI | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| Recall N=8 accuracy: summary_only -> scale_aware_note_aware | 24 | 0.208 | 0.875 | 0.667 | [0.500, 0.833] | 16 | 0 | 8 |
| Recall N=8 history loss: summary_only -> scale_aware_note_aware | 16 | 0.875 | 0.875 | 0.000 | [0.000, 0.000] | 0 | 0 | 16 |
| Stress N=1 false-present: scale_aware_unified -> scale_aware_note_aware | 16 | 0.125 | 0.062 | 0.062 | [0.000, 0.188] | 1 | 0 | 15 |
| Stress N=8 false-present: scale_aware_unified -> scale_aware_note_aware | 16 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 16 |
| Note persistence N=8 history loss: baseline -> tiny_fixed_scaffold | 8 | 1.000 | 0.625 | 0.375 | [0.125, 0.750] | 3 | 0 | 5 |
| Scaffold refinement N=8 unsafe error: tiny_fixed_scaffold -> tiny_refusal_scaffold | 12 | 0.167 | 0.083 | 0.083 | [0.000, 0.250] | 1 | 0 | 11 |
| Placeholder hardening N=8 placeholder answer: tiny_refusal_scaffold -> tiny_placeholder_hardened_scaffold | 12 | 0.083 | 0.000 | 0.083 | [0.000, 0.250] | 1 | 0 | 11 |
| Carry-forward N=8 unsafe error: tiny_placeholder_hardened_scaffold -> tiny_carry_forward_scaffold | 24 | 0.042 | 0.000 | 0.042 | [0.000, 0.125] | 1 | 0 | 23 |
| Recall N=8 accuracy: scale_aware_note_aware -> PSU | 24 | 0.875 | 1.000 | 0.125 | [0.000, 0.292] | 3 | 0 | 21 |
| Recall N=8 history loss: scale_aware_note_aware -> PSU | 16 | 0.875 | 0.062 | 0.812 | [0.625, 1.000] | 13 | 0 | 3 |
| Recall N=8 raw escalation: scale_aware_note_aware -> PSU | 24 | 0.583 | 0.042 | 0.542 | [0.333, 0.750] | 13 | 0 | 11 |

## Slope Readout

| Metric | Slope |
|---|---:|
| summary_only_recall_history_loss_slope | 0.1158 |
| scale_aware_note_aware_recall_history_loss_slope | 0.1158 |
| psu_recall_history_loss_slope | 0.0000 |
| tiered_stress_false_present_slope | -0.0186 |
| scale_aware_note_aware_stress_false_present_slope | -0.0084 |

## Interpretation

- Positive improvement delta means the treatment is better under the metric's intended direction.
- Positive slope means the metric rises with `N`; for harmful metrics like `history_loss` or `false_present`, that is undesirable.
