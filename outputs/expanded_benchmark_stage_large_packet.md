# Expanded Benchmark Stage Large Packet

这份 packet 把当前 stage 最值得在汇报或正文里直接引用的证据收在一起：覆盖规模、N=8 主表、可选调参对比、paired error analysis，以及是否值得继续往 full main 推进的判定。

## Stage

- description: Larger staged pass with broader official-benchmark coverage and PSU included, meant to sit between medium validation and the full main run.
- items: `34`
- seeds: `[11]`
- architectures: `summary_only, tiered, scale_aware_unified, scale_aware_note_aware, psu`
- verdict: `True`
- reason: PSU preserves benign N=8 accuracy while sharply reducing history_loss/raw_escalation, does not worsen hallucination false_present, and shows no paired regressions in the current error-analysis artifact.

## Coverage

| Panel | Selected | Available | Fraction | Strata |
|---|---:|---:|---:|---|
| halumem_expanded_v1 | 6 | 19 | 0.316 | {'halumem_unsupported_designation_abstain': 6} |
| locomo_expanded_v1 | 16 | 80 | 0.200 | {'locomo_absolute_temporal': 8, 'locomo_entity_or_attribute': 4, 'locomo_quantity_or_duration': 4} |
| longmemeval_expanded_v2 | 12 | 60 | 0.200 | {'longmemeval_single_session_assistant': 4, 'longmemeval_single_session_user': 8} |

## Family Table (N=8)

### benign_utility_expanded_pool

- focus label: `history_loss`
- num items: `28`

| Method | accuracy | history_loss | raw escalation |
|---|---:|---:|---:|
| summary_only | 0.357 | 0.464 | 0.000 |
| tiered | 0.964 | 0.464 | 0.607 |
| scale_aware_unified | 0.964 | 0.607 | 0.607 |
| scale_aware_note_aware | 0.964 | 0.607 | 0.607 |
| psu | 0.964 | 0.036 | 0.036 |

### hallucination_expanded_pool

- focus label: `false_present`
- num items: `6`

| Method | accuracy | false_present | raw escalation |
|---|---:|---:|---:|
| summary_only | 0.833 | 0.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 0.167 | 0.167 |
| scale_aware_note_aware | 1.000 | 0.167 | 0.167 |
| psu | 1.000 | 0.000 | 0.000 |

## Tuning Sweep

这部分只在当前 stage 已经做过 profile sweep 时出现。

### baseline

| Family | Method | accuracy | history_loss | false_present | raw escalation |
|---|---|---:|---:|---:|---:|
| benign_utility_expanded_pool | scale_aware_unified | 0.964 | 0.607 | - | 0.607 |
| benign_utility_expanded_pool | scale_aware_note_aware | 0.964 | 0.607 | - | 0.607 |
| benign_utility_expanded_pool | psu | 0.964 | 0.036 | - | 0.036 |
| hallucination_expanded_pool | scale_aware_unified | 1.000 | - | 0.167 | 0.167 |
| hallucination_expanded_pool | scale_aware_note_aware | 1.000 | - | 0.167 | 0.167 |
| hallucination_expanded_pool | psu | 1.000 | - | 0.000 | 0.000 |

### recover_more_v1

| Family | Method | accuracy | history_loss | false_present | raw escalation |
|---|---|---:|---:|---:|---:|
| benign_utility_expanded_pool | scale_aware_unified | 0.964 | 0.607 | - | 0.607 |
| benign_utility_expanded_pool | scale_aware_note_aware | 0.964 | 0.607 | - | 0.607 |
| benign_utility_expanded_pool | psu | 0.964 | 0.036 | - | 0.036 |
| hallucination_expanded_pool | scale_aware_unified | 1.000 | - | 0.167 | 0.167 |
| hallucination_expanded_pool | scale_aware_note_aware | 1.000 | - | 0.167 | 0.167 |
| hallucination_expanded_pool | psu | 1.000 | - | 0.000 | 0.000 |

### note_soft_v1

| Family | Method | accuracy | history_loss | false_present | raw escalation |
|---|---|---:|---:|---:|---:|
| benign_utility_expanded_pool | scale_aware_unified | 0.964 | 0.607 | - | 0.607 |
| benign_utility_expanded_pool | scale_aware_note_aware | 0.964 | 0.607 | - | 0.607 |
| benign_utility_expanded_pool | psu | 0.964 | 0.036 | - | 0.036 |
| hallucination_expanded_pool | scale_aware_unified | 1.000 | - | 0.167 | 0.167 |
| hallucination_expanded_pool | scale_aware_note_aware | 1.000 | - | 0.167 | 0.167 |
| hallucination_expanded_pool | psu | 1.000 | - | 0.000 | 0.000 |

## Paired Error Analysis

| Family | Base | Paired | PSU better | Tie | PSU worse | Base focus error | PSU focus error | Base raw | PSU raw |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| benign | scale_aware_unified | 28 | 16 | 12 | 0 | 0.607 | 0.036 | 0.607 | 0.036 |
| benign | scale_aware_note_aware | 28 | 16 | 12 | 0 | 0.607 | 0.036 | 0.607 | 0.036 |
| hallucination | scale_aware_unified | 6 | 1 | 5 | 0 | 0.167 | 0.000 | 0.167 | 0.000 |
| hallucination | scale_aware_note_aware | 6 | 1 | 5 | 0 | 0.167 | 0.000 | 0.167 | 0.000 |

## Bottom Line

- 这个 packet 的价值在于，它把“规模是否够、PSU 的 gain 是否只是平均数假象、调参有没有真改变结论”压缩到一页里。
- 如果后续 `main` 复现相同 paired pattern，那么我们就不仅有更大 benchmark coverage，也有一份更像论文 error-analysis section 的直接证据。
