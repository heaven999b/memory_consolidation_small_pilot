# Expanded Benchmark Tuning Sweep: large

这份 sweep 固定同一个 expanded benchmark stage，只改变 scale-aware / note-aware 相关阈值，比较三组 profile 在统一 benchmark 面上的 tradeoff。

- stage: `large`
- architectures: `scale_aware_unified, scale_aware_note_aware, psu`
- compared profiles: `baseline, recover_more_v1, note_soft_v1`

## baseline

- description: Current benchmark-stage baseline with the default probe, note-aware, and routing thresholds.
- env overrides: `{}`

| Method | benign N=8 acc | benign N=8 history_loss | benign N=8 raw | hallucination N=8 acc | hallucination N=8 false_present | hallucination N=8 raw |
|---|---:|---:|---:|---:|---:|---:|
| scale_aware_unified | 0.964 | 0.607 | 0.607 | 1.000 | 0.167 | 0.167 |
| scale_aware_note_aware | 0.964 | 0.607 | 0.607 | 1.000 | 0.167 | 0.167 |
| psu | 0.964 | 0.036 | 0.036 | 1.000 | 0.000 | 0.000 |

## recover_more_v1

- description: Makes answerable noisy targets easier to recover while reducing the absent-target noise bonus.
- env overrides: `{'MEMORY_PROBE_EXISTS_NOISE_PENALTY': '0.03', 'MEMORY_PROBE_ABSENT_NOISE_BONUS': '0.16', 'MEMORY_PROBE_UNCERTAIN_THRESHOLD': '0.40'}`

| Method | benign N=8 acc | benign N=8 history_loss | benign N=8 raw | hallucination N=8 acc | hallucination N=8 false_present | hallucination N=8 raw |
|---|---:|---:|---:|---:|---:|---:|
| scale_aware_unified | 0.964 | 0.607 | 0.607 | 1.000 | 0.167 | 0.167 |
| scale_aware_note_aware | 0.964 | 0.607 | 0.607 | 1.000 | 0.167 | 0.167 |
| psu | 0.964 | 0.036 | 0.036 | 1.000 | 0.000 | 0.000 |

## note_soft_v1

- description: Builds on recover_more_v1 and softens note-aware penalties so answerable medium-criticality benchmark items are less likely to collapse into absent.
- env overrides: `{'MEMORY_PROBE_EXISTS_NOISE_PENALTY': '0.03', 'MEMORY_PROBE_ABSENT_NOISE_BONUS': '0.16', 'MEMORY_PROBE_UNCERTAIN_THRESHOLD': '0.40', 'MEMORY_NOTE_INFERENCE_PENALTY_ABSENT': '0.14', 'MEMORY_NOTE_INFERENCE_PENALTY_PRESENT': '0.04', 'MEMORY_NOTE_MISSING_PENALTY': '0.08', 'MEMORY_NOTE_MISSING_CONFLICT_PENALTY': '0.03', 'MEMORY_NOTE_CLEAN_BONUS': '0.06'}`

| Method | benign N=8 acc | benign N=8 history_loss | benign N=8 raw | hallucination N=8 acc | hallucination N=8 false_present | hallucination N=8 raw |
|---|---:|---:|---:|---:|---:|---:|
| scale_aware_unified | 0.964 | 0.607 | 0.607 | 1.000 | 0.167 | 0.167 |
| scale_aware_note_aware | 0.964 | 0.607 | 0.607 | 1.000 | 0.167 | 0.167 |
| psu | 0.964 | 0.036 | 0.036 | 1.000 | 0.000 | 0.000 |

## Delta Readout

| Method | Metric | baseline | recover_more_v1 | note_soft_v1 |
|---|---|---:|---:|---:|
| scale_aware_unified | benign accuracy | 0.964 | 0.964 | 0.964 |
| scale_aware_unified | benign history_loss | 0.607 | 0.607 | 0.607 |
| scale_aware_unified | benign raw escalation | 0.607 | 0.607 | 0.607 |
| scale_aware_unified | hallucination false_present | 0.167 | 0.167 | 0.167 |
| scale_aware_note_aware | benign accuracy | 0.964 | 0.964 | 0.964 |
| scale_aware_note_aware | benign history_loss | 0.607 | 0.607 | 0.607 |
| scale_aware_note_aware | benign raw escalation | 0.607 | 0.607 | 0.607 |
| scale_aware_note_aware | hallucination false_present | 0.167 | 0.167 | 0.167 |
| psu | benign accuracy | 0.964 | 0.964 | 0.964 |
| psu | benign history_loss | 0.036 | 0.036 | 0.036 |
| psu | benign raw escalation | 0.036 | 0.036 | 0.036 |
| psu | hallucination false_present | 0.000 | 0.000 | 0.000 |

## Interpretation

- 这组 sweep 主要回答的是 route/probe/detector 门槛能不能在不牺牲 hallucination-side cleanliness 的前提下，改善 benchmark-grounded benign utility。
- 如果 `scale_aware_note_aware` 和 `psu` 在 benign 侧 gains 明显，而 hallucination false_present 仍接近 `0`，就说明下一步值得把该 profile 推到更大的 expanded main run。
- 如果 benign `history_loss` 基本不变，那说明仅靠 route/probe 调参不够，后续就该优先继续优化 PSU 的 compaction contract，而不是只调 detector 门槛。
