# PSU Recall Main Panel

这份工件把 recall 主面板重新整理成论文可直接引用的形状：同一张表里同时放 baseline routing family、PSU 无 carry 的近邻 ablation、以及最终 PSU。

## N=4

| Method | accuracy | propagation | raw escalation | history loss | empty-note-then-abstain | benign/conflict error | unsafe error | hallucination placeholder | carry-forward record |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| summary_only | 0.458 | 0.417 | 0.000 | 0.438 | 0.125 | 0.438 | 1.000 | 0.000 | 0.000 |
| tiered | 0.833 | 0.167 | 0.625 | 0.438 | 0.062 | 0.125 | 0.250 | 0.000 | 0.000 |
| scale_aware_unified | 0.833 | 0.167 | 0.292 | 0.438 | 0.000 | 0.000 | 0.750 | 0.000 | 0.000 |
| scale_aware_note_aware | 0.833 | 0.167 | 0.292 | 0.438 | 0.000 | 0.000 | 0.750 | 0.000 | 0.000 |
| psu_no_carry | 0.917 | 0.083 | 0.208 | 0.312 | 0.000 | 0.000 | 0.500 | 0.000 | 0.000 |
| psu | 1.000 | 0.000 | 0.042 | 0.062 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 |

## N=8

| Method | accuracy | propagation | raw escalation | history loss | empty-note-then-abstain | benign/conflict error | unsafe error | hallucination placeholder | carry-forward record |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| summary_only | 0.208 | 0.500 | 0.000 | 0.875 | 0.312 | 0.875 | 1.000 | 0.000 | 0.000 |
| tiered | 0.792 | 0.208 | 0.750 | 0.875 | 0.062 | 0.250 | 0.250 | 0.000 | 0.000 |
| scale_aware_unified | 0.875 | 0.125 | 0.583 | 0.875 | 0.000 | 0.000 | 0.750 | 0.000 | 0.000 |
| scale_aware_note_aware | 0.875 | 0.125 | 0.583 | 0.875 | 0.000 | 0.000 | 0.750 | 0.000 | 0.000 |
| psu_no_carry | 0.958 | 0.042 | 0.417 | 0.625 | 0.000 | 0.000 | 0.250 | 0.000 | 0.000 |
| psu | 1.000 | 0.000 | 0.042 | 0.062 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 |

## Direct Delta At N=8

| Comparison | Pairs | Mean Delta | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---:|
| scale_aware_note_aware -> PSU accuracy | 24 | 0.125 | 3 | 0 | 21 |
| scale_aware_note_aware -> PSU history loss | 16 | 0.812 | 13 | 0 | 3 |
| scale_aware_note_aware -> PSU raw escalation | 24 | 0.542 | 13 | 0 | 11 |
| psu_no_carry -> PSU unsafe error | 4 | 0.250 | 1 | 0 | 3 |

## Readout

- `psu_no_carry` isolates the scaffold + placeholder hardening state just before the final carry-forward rule, so the last step is not conflated with earlier scaffold work.
- If PSU lowers both `history_loss` and `raw escalation` against `scale_aware_note_aware`, then recall-side gains are no longer only coming from more aggressive fallback; they are coming from better compact-memory survival.
