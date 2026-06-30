# Expanded Benchmark Main Significance

This artifact upgrades the finished expanded benchmark `main` run from a score table into paired significance tests at paper-facing scale.

- bootstrap samples: `5000`
- bootstrap seed: `20260630`

## Main Tests

| Comparison | Pairs | Baseline | PSU | Delta | 95% CI | Baseline-win | PSU-win | Ties | McNemar p |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Benign N=8 accuracy: tiered -> PSU | 280 | 0.946 | 0.986 | 0.039 | [0.018, 0.064] | 1 | 12 | 267 | 0.003418 |
| Benign N=8 history retention: summary_only -> PSU | 280 | 0.446 | 0.929 | 0.482 | [0.414, 0.546] | 11 | 146 | 123 | 0.000000 |
| Benign N=8 no-raw-escalation: summary_only -> PSU | 280 | 1.000 | 0.929 | -0.071 | [-0.104, -0.043] | 20 | 0 | 260 | 0.000002 |
| Hallucination N=8 no-false-present: summary_only -> PSU | 38 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Hallucination N=8 accuracy: tiered -> PSU | 38 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |

## Baseline Selection

- benign accuracy strongest baseline: `tiered`
- benign history-loss strongest baseline: `summary_only`
- benign raw-escalation strongest baseline: `summary_only`
- hallucination false-present strongest baseline: `summary_only`
- hallucination accuracy strongest baseline: `tiered`
