# V3 No-Rewrite Pareto

Proxy cost/utility and cost/safety Pareto readout for the V3 no-rewrite comparison surface.

## N=8

- benign Pareto front: `['summary_only', 'summary_query_aware']`
- safety Pareto front: `['summary_only', 'summary_only_no_rewrite', 'summary_query_aware']`

### Benign Accuracy vs Cost

| Method | Accuracy | mean_cost | history_loss |
|---|---:|---:|---:|
| raw_only | 1.000 | 3.200 | 0.000 |
| summary_only | 0.461 | 2.440 | 0.539 |
| summary_query_aware | 1.000 | 2.470 | 0.000 |
| summary_only_no_rewrite | 0.529 | 2.490 | 0.471 |
| summary_query_aware_no_rewrite | 1.000 | 2.520 | 0.000 |
| tiered | 1.000 | 4.001 | 0.000 |
| tiered_no_rewrite | 1.000 | 3.696 | 0.000 |

### Safety Score vs Cost

| Method | Safety Score | mean_cost | hallucination_risk | conflict_risk | unsafe_risk |
|---|---:|---:|---:|---:|---:|
| raw_only | 1.000 | 3.200 | 0.000 | 0.000 | 0.000 |
| summary_only | 0.000 | 2.440 | 1.000 | 1.000 | 1.000 |
| summary_query_aware | 0.333 | 2.470 | 1.000 | 0.000 | 1.000 |
| summary_only_no_rewrite | 1.000 | 2.490 | 0.000 | 0.000 | 0.000 |
| summary_query_aware_no_rewrite | 1.000 | 2.520 | 0.000 | 0.000 | 0.000 |
| tiered | 1.000 | 4.001 | 0.000 | 0.000 | 0.000 |
| tiered_no_rewrite | 1.000 | 3.696 | 0.000 | 0.000 | 0.000 |

## N=16

- benign Pareto front: `['raw_only']`
- safety Pareto front: `['raw_only']`

### Benign Accuracy vs Cost

| Method | Accuracy | mean_cost | history_loss |
|---|---:|---:|---:|
| raw_only | 1.000 | 3.200 | 0.000 |
| summary_only | 0.475 | 3.880 | 0.525 |
| summary_query_aware | 1.000 | 3.910 | 0.000 |
| summary_only_no_rewrite | 0.536 | 3.930 | 0.464 |
| summary_query_aware_no_rewrite | 1.000 | 3.960 | 0.000 |
| tiered | 1.000 | 5.480 | 0.000 |
| tiered_no_rewrite | 1.000 | 5.167 | 0.000 |

### Safety Score vs Cost

| Method | Safety Score | mean_cost | hallucination_risk | conflict_risk | unsafe_risk |
|---|---:|---:|---:|---:|---:|
| raw_only | 1.000 | 3.200 | 0.000 | 0.000 | 0.000 |
| summary_only | 0.000 | 3.880 | 1.000 | 1.000 | 1.000 |
| summary_query_aware | 0.333 | 3.910 | 1.000 | 0.000 | 1.000 |
| summary_only_no_rewrite | 1.000 | 3.930 | 0.000 | 0.000 | 0.000 |
| summary_query_aware_no_rewrite | 1.000 | 3.960 | 0.000 | 0.000 | 0.000 |
| tiered | 1.000 | 5.480 | 0.000 | 0.000 | 0.000 |
| tiered_no_rewrite | 1.000 | 5.167 | 0.000 | 0.000 | 0.000 |
