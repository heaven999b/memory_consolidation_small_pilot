# Expanded Benchmark Main Cost Pareto

This artifact promotes cost into a first-class axis for the finished expanded benchmark `main` run.

## Benign Utility (N=8 accuracy vs cost)

- quality axis: `accuracy`
- pareto front (mean_cost): `['psu', 'summary_only']`
- pareto front (mean_llm_cost_usd): `['psu', 'scale_aware_note_aware', 'scale_aware_unified', 'tiered']`

| Method | Quality | mean_cost | mean_llm_cost_usd | raw_escalation |
|---|---:|---:|---:|---:|
| summary_only | 0.314 | 2.440 | 0.3586 | 0.000 |
| tiered | 0.946 | 3.480 | 0.3586 | 0.650 |
| scale_aware_unified | 0.946 | 3.680 | 0.3586 | 0.650 |
| scale_aware_note_aware | 0.946 | 3.680 | 0.3586 | 0.650 |
| psu | 0.986 | 2.754 | 0.3877 | 0.071 |

### Iso-Budget Leaders (mean_cost)

| Budget | Leader | Quality | Cost |
|---|---|---:|---:|
| 2.440 | summary_only | 0.314 | 2.440 |
| 2.754 | psu | 0.986 | 2.754 |
| 3.480 | psu | 0.986 | 2.754 |
| 3.680 | psu | 0.986 | 2.754 |

## Hallucination Safety (N=8 1-false_present vs cost)

- quality axis: `1 - false_present_rate`
- pareto front (mean_cost): `['summary_only']`
- pareto front (mean_llm_cost_usd): `['summary_only']`

| Method | Quality | mean_cost | mean_llm_cost_usd | raw_escalation |
|---|---:|---:|---:|---:|
| summary_only | 1.000 | 2.440 | 0.3146 | 0.000 |
| tiered | 0.000 | 4.040 | 0.3146 | 1.000 |
| scale_aware_unified | 0.921 | 2.766 | 0.3146 | 0.079 |
| scale_aware_note_aware | 0.947 | 2.724 | 0.3146 | 0.053 |
| psu | 1.000 | 2.640 | 0.4115 | 0.000 |

### Iso-Budget Leaders (mean_cost)

| Budget | Leader | Quality | Cost |
|---|---|---:|---:|
| 2.440 | summary_only | 1.000 | 2.440 |
| 2.640 | summary_only | 1.000 | 2.440 |
| 2.724 | summary_only | 1.000 | 2.440 |
| 2.766 | summary_only | 1.000 | 2.440 |
| 4.040 | summary_only | 1.000 | 2.440 |

