# Memory Architecture Mini Panel

- source: local frozen artifacts only
- note: no fresh external API rerun in this packet
- generated_at_utc: `2026-07-10T03:59:49.825097+00:00`

## Closed-loop Live Smoke

| architecture | direction | N | exact_match | f1 | avg_tokens_in | avg_latency_ms | raw_route_rate | page_store_bytes | summary_chars | content_chars | memory_items |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw_only | raw_control | 0 | 1.0 | 1.0 | 2125.5 | 6453.3 | 1.0 | 4318 | 0 | 1549 | 2 |
| raw_only | raw_control | 1 | 0.833 | 0.955 | 1564.8 | 9570.5 | 1.0 | 3625 | 412 | 1549 | 2 |
| summary_only | compression_only | 0 | 0.0 | 0.379 | 172.3 | 1524.3 | 0.0 | 3460 | 0 | 1549 | 8 |
| summary_only | compression_only | 1 | 0.167 | 0.488 | 132.3 | 745.5 | 0.0 | 3641 | 420 | 1549 | 2 |
| tiered_week1 | hierarchical_reopen | 0 | 0.0 | 0.379 | 643.0 | 1510.8 | 0.0 | 3460 | 0 | 1549 | 8 |
| tiered_week1 | hierarchical_reopen | 1 | 0.333 | 0.571 | 717.2 | 2226.0 | 0.167 | 3589 | 395 | 1549 | 2 |

## Synthetic Control Trio

| architecture | direction | N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| raw_only | raw_control | 0 | 1.0 | 0.0 | 0.0 | 1.0 | 3.2 |
| raw_only | raw_control | 1 | 1.0 | 0.0 | 0.0 | 1.0 | 3.2 |
| raw_only | raw_control | 2 | 1.0 | 0.0 | 0.0 | 1.0 | 3.2 |
| raw_only | raw_control | 4 | 1.0 | 0.0 | 0.0 | 1.0 | 3.2 |
| raw_only | raw_control | 8 | 1.0 | 0.0 | 0.0 | 1.0 | 3.2 |
| summary_only | compression_only | 0 | 0.769 | 0.231 | 0.231 | 0.0 | 1.0 |
| summary_only | compression_only | 1 | 0.588 | 0.412 | 0.392 | 0.0 | 1.18 |
| summary_only | compression_only | 2 | 0.369 | 0.631 | 0.588 | 0.0 | 1.36 |
| summary_only | compression_only | 4 | 0.131 | 0.869 | 0.808 | 0.0 | 1.72 |
| summary_only | compression_only | 8 | 0.004 | 0.996 | 0.927 | 0.0 | 2.44 |
| tiered | hierarchical_reopen | 0 | 1.0 | 0.0 | 0.231 | 0.75 | 2.2 |
| tiered | hierarchical_reopen | 1 | 1.0 | 0.0 | 0.392 | 0.796 | 2.454 |
| tiered | hierarchical_reopen | 2 | 0.992 | 0.008 | 0.588 | 0.835 | 2.695 |
| tiered | hierarchical_reopen | 4 | 0.977 | 0.023 | 0.808 | 0.9 | 3.16 |
| tiered | hierarchical_reopen | 8 | 0.977 | 0.023 | 0.927 | 0.973 | 3.997 |

## Model-backed Sanity: actual_recall_expansion

| architecture | direction | N | accuracy | propagation | residual_bad_memory | history_loss | raw_escalation | mean_llm_cost_usd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| summary_only | compression_only | 8 | 0.208 | 0.5 | 0.083 | 0.875 | 0.0 | 0.246584 |
| tiered | hierarchical_reopen | 8 | 0.792 | 0.208 | 0.083 | 0.875 | 0.75 | 0.246584 |
| scale-aware unified | policy_gated_reopen | 8 | 0.875 | 0.125 | 0.0 | 0.875 | 0.583 | 0.246584 |
| scale-aware note-aware | policy_gated_reopen | 8 | 0.875 | 0.125 | 0.0 | 0.875 | 0.583 | 0.246584 |

## Model-backed Sanity: actual_hallucination_stress

| architecture | direction | N | accuracy | propagation | residual_bad_memory | false_present | raw_escalation | mean_llm_cost_usd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| summary_only | compression_only | 8 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.287457 |
| tiered | hierarchical_reopen | 8 | 1.0 | 0.0 | 0.0 | 0.875 | 0.875 | 0.287457 |
| scale-aware unified | policy_gated_reopen | 8 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.287457 |
| scale-aware note-aware | policy_gated_reopen | 8 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.287457 |

## Benchmark-grounded Rollup: benign_utility_expanded_pool

| architecture | direction | N | accuracy | propagation | residual_bad_memory | history_loss | raw_escalation | mean_cost | mean_llm_cost_usd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| psu | provenance_scaffolded_policy | 8 | 0.964 | 0.036 | 0.0 | 0.036 | 0.036 | 2.697 | 0.367882 |
| scale-aware note-aware | policy_gated_reopen | 8 | 0.964 | 0.036 | 0.0 | 0.607 | 0.607 | 3.611 | 0.334176 |
| scale-aware unified | policy_gated_reopen | 8 | 0.964 | 0.036 | 0.0 | 0.607 | 0.607 | 3.611 | 0.334176 |
| summary_only | compression_only | 8 | 0.357 | 0.643 | 0.143 | 0.464 | 0.0 | 2.44 | 0.334176 |
| tiered | hierarchical_reopen | 8 | 0.964 | 0.036 | 0.143 | 0.464 | 0.607 | 3.411 | 0.334176 |

## Benchmark-grounded Rollup: hallucination_expanded_pool

| architecture | direction | N | accuracy | propagation | residual_bad_memory | false_present | raw_escalation | mean_cost | mean_llm_cost_usd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| psu | provenance_scaffolded_policy | 8 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.64 | 0.424362 |
| scale-aware note-aware | policy_gated_reopen | 8 | 1.0 | 0.0 | 0.0 | 0.167 | 0.167 | 2.907 | 0.369779 |
| scale-aware unified | policy_gated_reopen | 8 | 1.0 | 0.0 | 0.0 | 0.167 | 0.167 | 2.907 | 0.369779 |
| summary_only | compression_only | 8 | 0.833 | 0.167 | 0.167 | 0.0 | 0.0 | 2.44 | 0.369779 |
| tiered | hierarchical_reopen | 8 | 1.0 | 0.0 | 0.167 | 1.0 | 1.0 | 4.04 | 0.369779 |

## PSU Recall Panel

| architecture | direction | N | accuracy | propagation | history_loss | raw_escalation | unsafe_error | mean_llm_cost_usd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| summary_only | compression_only | 8 | 0.208 | 0.5 | 0.875 | 0.0 | 1.0 | 0.246584 |
| tiered | hierarchical_reopen | 8 | 0.792 | 0.208 | 0.875 | 0.75 | 0.25 | 0.246584 |
| scale-aware unified | policy_gated_reopen | 8 | 0.875 | 0.125 | 0.875 | 0.583 | 0.75 | 0.246584 |
| scale-aware note-aware | policy_gated_reopen | 8 | 0.875 | 0.125 | 0.875 | 0.583 | 0.75 | 0.246584 |
| psu (no carry) | policy_scaffold_ablation | 8 | 0.958 | 0.042 | 0.625 | 0.417 | 0.25 | 0.343942 |
| psu | provenance_scaffolded_policy | 8 | 1.0 | 0.0 | 0.062 | 0.042 | 0.0 | 0.343942 |

## Cost Pareto Snapshot

| section | architecture | direction | quality | mean_cost | mean_llm_cost_usd | raw_escalation |
| --- | --- | --- | --- | --- | --- | --- |
| Benign Utility (N=8 accuracy vs cost) | summary_only | compression_only | 0.314 | 2.44 | 0.35864 | 0.0 |
| Benign Utility (N=8 accuracy vs cost) | tiered | hierarchical_reopen | 0.946 | 3.48 | 0.35864 | 0.65 |
| Benign Utility (N=8 accuracy vs cost) | scale-aware unified | policy_gated_reopen | 0.946 | 3.68 | 0.35864 | 0.65 |
| Benign Utility (N=8 accuracy vs cost) | scale-aware note-aware | policy_gated_reopen | 0.946 | 3.68 | 0.35864 | 0.65 |
| Benign Utility (N=8 accuracy vs cost) | psu | provenance_scaffolded_policy | 0.986 | 2.754 | 0.387664 | 0.071 |
| Hallucination Safety (N=8 1-false_present vs cost) | summary_only | compression_only | 1.0 | 2.44 | 0.314566 | 0.0 |
| Hallucination Safety (N=8 1-false_present vs cost) | tiered | hierarchical_reopen | 0.0 | 4.04 | 0.314566 | 1.0 |
| Hallucination Safety (N=8 1-false_present vs cost) | scale-aware unified | policy_gated_reopen | 0.921 | 2.766 | 0.314566 | 0.079 |
| Hallucination Safety (N=8 1-false_present vs cost) | scale-aware note-aware | policy_gated_reopen | 0.947 | 2.724 | 0.314566 | 0.053 |
| Hallucination Safety (N=8 1-false_present vs cost) | psu | provenance_scaffolded_policy | 1.0 | 2.64 | 0.411536 | 0.0 |

## Signal Board

- Compression-only has a real efficiency signal on the live smoke slice: `summary_only@N=0` uses 172.3 avg input tokens vs `2125.5` for `raw_only@N=0` (8.1%), but exact-match drops from 1.0 to 0.0.
- Hierarchical reopen shows a modest recovery signal on the same live slice: `tiered_week1@N=1` reaches exact-match 0.333 vs `0.167` for `summary_only@N=1`, with raw reopen rate 0.167.
- On the expanded benign-utility pool at `N=8`, plain reopening is not optional for utility: `summary_only` accuracy is 0.357, while `tiered` reaches 0.964.
- Ungated reopening looks unsafe on the hallucination pool: `tiered` has false-present rate 1.0 at raw escalation 1.0, while `scale_aware_note_aware` cuts false-present to 0.167.
- The strongest current local signal is the provenance/policy line: `psu@N=8` keeps benign accuracy at 0.964 with history-loss 0.036 and raw escalation 0.036, while also keeping hallucination false-present at 0.0.
- Within the recall-heavy panel, `psu` improves over `scale_aware_note_aware` at the same `N=8`: accuracy 1.0 vs 0.875, history-loss 0.062 vs 0.875, raw escalation 0.042 vs 0.583.

## Caveats

- This packet aggregates existing local artifacts; it does not add a fresh benchmark rerun.
- Occupancy proxies currently come from the week1 live smoke runs where page-store JSON is directly available.
- The strongest policy result (`psu`) is still a local frozen panel and should be treated as a positive signal, not final closure.
