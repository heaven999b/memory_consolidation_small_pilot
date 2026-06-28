# Actual Recall Expansion Summary

这一轮扩的是真实 summarizer 的 benign/conflict 覆盖，不是再加 hallucination stress。目标是把 over-compression 的真实瓶颈看清楚。

- slice items: 12
- seeds: [11, 23]
- architectures: summary_only, tiered, scale_aware_unified, scale_aware_note_aware
- N: [1, 4, 8]

## summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note | empty_note_then_abstain | history_loss | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.792 | 0.208 | 0.250 | 0.000 | 0.062 | 0.062 | 0.062 | 0.062 | 0.0343 |
| 4 | 0.458 | 0.417 | 0.208 | 0.000 | 0.438 | 0.125 | 0.125 | 0.438 | 0.1354 |
| 8 | 0.208 | 0.500 | 0.083 | 0.000 | 0.875 | 0.312 | 0.312 | 0.875 | 0.2466 |

## tiered

| N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note | empty_note_then_abstain | history_loss | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.958 | 0.042 | 0.250 | 0.625 | 0.000 | 0.062 | 0.000 | 0.062 | 0.0343 |
| 4 | 0.833 | 0.167 | 0.208 | 0.625 | 0.125 | 0.125 | 0.062 | 0.438 | 0.1354 |
| 8 | 0.792 | 0.208 | 0.083 | 0.750 | 0.250 | 0.312 | 0.062 | 0.875 | 0.2466 |

## scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note | empty_note_then_abstain | history_loss | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.958 | 0.042 | 0.000 | 0.042 | 0.000 | 0.062 | 0.000 | 0.062 | 0.0343 |
| 4 | 0.833 | 0.167 | 0.000 | 0.292 | 0.000 | 0.125 | 0.000 | 0.438 | 0.1354 |
| 8 | 0.875 | 0.125 | 0.000 | 0.583 | 0.000 | 0.312 | 0.000 | 0.875 | 0.2466 |

## scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | benign_conflict_error | empty_note | empty_note_then_abstain | history_loss | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.958 | 0.042 | 0.000 | 0.042 | 0.000 | 0.062 | 0.000 | 0.062 | 0.0343 |
| 4 | 0.833 | 0.167 | 0.000 | 0.292 | 0.000 | 0.125 | 0.000 | 0.438 | 0.1354 |
| 8 | 0.875 | 0.125 | 0.000 | 0.583 | 0.000 | 0.312 | 0.000 | 0.875 | 0.2466 |

## Readout

- 这个 round 的关键不是再证明 hallucination 风险，而是量化真实 model-backed compaction 在 benign/conflict 上如何丢失 answerability。
- `empty_note_then_abstain` 和 `history_loss` 如果在高 N 明显上升，就说明真实瓶颈已经从污染传播转向压缩后信息蒸发。
