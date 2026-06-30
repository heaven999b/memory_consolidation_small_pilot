# V3 No-Rewrite Statistics

Paired local statistics for the V3 no-rewrite comparison surface.

- bootstrap samples: `4000`
- bootstrap seed: `20260630`

| Comparison | Family | N | Left | Right | Delta | 95% CI | Left-win | Right-win | Ties | McNemar p |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Fairness: blind -> query-aware | hallucination | 8 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | hallucination | 16 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | conflict | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Fairness: blind -> query-aware | conflict | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Fairness: blind -> query-aware | unsafe | 8 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | unsafe | 16 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | benign | 8 | 0.461 | 1.000 | 0.539 | [0.479, 0.596] | 0 | 151 | 129 | 0.000000 |
| Fairness: blind -> query-aware | benign | 16 | 0.475 | 1.000 | 0.525 | [0.464, 0.582] | 0 | 147 | 133 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | hallucination | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | hallucination | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 8 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 16 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | benign | 8 | 1.000 | 0.529 | -0.471 | [-0.529, -0.414] | 132 | 0 | 148 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | benign | 16 | 1.000 | 0.536 | -0.464 | [-0.521, -0.404] | 130 | 0 | 150 | 0.000000 |
| Main: blind -> no-rewrite | hallucination | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | hallucination | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | conflict | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | conflict | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | benign | 8 | 0.461 | 0.529 | 0.068 | [0.039, 0.100] | 0 | 19 | 261 | 0.000004 |
| Main: blind -> no-rewrite | benign | 16 | 0.475 | 0.536 | 0.061 | [0.036, 0.089] | 0 | 17 | 263 | 0.000015 |

Interpretation note: `benign` uses accuracy, while the other families use failure endpoints, so negative deltas on risk families are improvements.
