# Task Extension Section

这个 artifact 不替代外部 benchmark reviewer section。它补的是另一类缺口：把 `conflict` 和 `unsafe` 也冻结成 manifest-backed task extensions，让 benchmark-native primary base 覆盖完整四个任务 family。

- ready: `True`
- panel count: `2`
- item count: `6`
- task families: `['conflict', 'unsafe']`

## Conflict Extension (N=8)

| Method | accuracy | conflict_error | history_loss | raw escalation |
|---|---:|---:|---:|---:|
| summary_only | 0.125 | 0.875 | 0.875 | 0.000 |
| tiered | 1.000 | 0.000 | 0.875 | 1.000 |
| scale_aware_unified | 1.000 | 0.000 | 0.875 | 0.875 |
| scale_aware_note_aware | 1.000 | 0.000 | 0.875 | 0.875 |

## Unsafe Extension (N=8)

| Method | accuracy | unsafe_error | carry_forward_record | raw escalation |
|---|---:|---:|---:|---:|
| summary_only | 1.000 | 0.000 | 1.000 | 0.000 |
| scale_aware_unified | 1.000 | 0.000 | 1.000 | 0.000 |
| scale_aware_note_aware | 1.000 | 0.000 | 1.000 | 0.000 |

## Readout

- `conflict` 现在不再只是散落在 recall slice 里的 supporting evidence，而是有了 manifest-backed extension panel。
- `unsafe` 现在也不再只是单轮 scaffold 调参结果，而是有了 manifest-backed extension panel，并明确绑定到 carry-forward refusal winner。
- 这一步补掉的不是 benchmark scale，而是任务 family 覆盖缺口。
