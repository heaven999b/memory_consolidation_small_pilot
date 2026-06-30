# V3 No-Rewrite Statistics

Paired synthetic dry-run statistics for the V3 no-rewrite comparison surface.

- evidence class: `synthetic_dry_run`
- runtime: `legacy_compaction_simulator`
- bootstrap samples: `4000`
- bootstrap seed: `20260630`
- depths: `[0, 1, 2, 4, 8, 16]`

Warning: this table is a synthetic dry-run over the legacy compaction simulator.
Zero-width confidence intervals or exact `0.000` / `+/-1.000` deltas here should not be interpreted as real-model stochastic evidence.

| Comparison | Family | N | Left | Right | Delta | 95% CI | Left-win | Right-win | Ties | McNemar p |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Fairness: blind -> query-aware | hallucination | 0 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | hallucination | 1 | 0.237 | 0.237 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | hallucination | 2 | 0.500 | 0.500 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | hallucination | 4 | 0.842 | 0.842 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | hallucination | 8 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | hallucination | 16 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Fairness: blind -> query-aware | conflict | 0 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Fairness: blind -> query-aware | conflict | 1 | 0.393 | 0.000 | -0.393 | [-0.571, -0.214] | 11 | 0 | 17 | 0.000977 |
| Fairness: blind -> query-aware | conflict | 2 | 0.643 | 0.000 | -0.643 | [-0.821, -0.464] | 18 | 0 | 10 | 0.000008 |
| Fairness: blind -> query-aware | conflict | 4 | 0.929 | 0.000 | -0.929 | [-1.000, -0.821] | 26 | 0 | 2 | 0.000000 |
| Fairness: blind -> query-aware | conflict | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Fairness: blind -> query-aware | conflict | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Fairness: blind -> query-aware | unsafe | 0 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | unsafe | 1 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | unsafe | 2 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | unsafe | 4 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | unsafe | 8 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | unsafe | 16 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 | 1.000000 |
| Fairness: blind -> query-aware | benign | 0 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 280 | 1.000000 |
| Fairness: blind -> query-aware | benign | 1 | 0.896 | 1.000 | 0.104 | [0.068, 0.143] | 0 | 29 | 251 | 0.000000 |
| Fairness: blind -> query-aware | benign | 2 | 0.832 | 1.000 | 0.168 | [0.121, 0.211] | 0 | 47 | 233 | 0.000000 |
| Fairness: blind -> query-aware | benign | 4 | 0.671 | 1.000 | 0.329 | [0.275, 0.386] | 0 | 92 | 188 | 0.000000 |
| Fairness: blind -> query-aware | benign | 8 | 0.461 | 1.000 | 0.539 | [0.482, 0.596] | 0 | 151 | 129 | 0.000000 |
| Fairness: blind -> query-aware | benign | 16 | 0.475 | 1.000 | 0.525 | [0.464, 0.582] | 0 | 147 | 133 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | hallucination | 0 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | hallucination | 1 | 0.237 | 0.000 | -0.237 | [-0.368, -0.105] | 9 | 0 | 29 | 0.003906 |
| Mechanism: query-aware -> no-rewrite | hallucination | 2 | 0.500 | 0.000 | -0.500 | [-0.658, -0.342] | 19 | 0 | 19 | 0.000004 |
| Mechanism: query-aware -> no-rewrite | hallucination | 4 | 0.842 | 0.000 | -0.842 | [-0.947, -0.711] | 32 | 0 | 6 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | hallucination | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | hallucination | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 0 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 1 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 2 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 4 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 8 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | conflict | 16 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 0 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 1 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 2 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 4 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | unsafe | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | benign | 0 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 280 | 1.000000 |
| Mechanism: query-aware -> no-rewrite | benign | 1 | 1.000 | 0.925 | -0.075 | [-0.107, -0.046] | 21 | 0 | 259 | 0.000001 |
| Mechanism: query-aware -> no-rewrite | benign | 2 | 1.000 | 0.868 | -0.132 | [-0.171, -0.093] | 37 | 0 | 243 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | benign | 4 | 1.000 | 0.714 | -0.286 | [-0.339, -0.236] | 80 | 0 | 200 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | benign | 8 | 1.000 | 0.529 | -0.471 | [-0.532, -0.411] | 132 | 0 | 148 | 0.000000 |
| Mechanism: query-aware -> no-rewrite | benign | 16 | 1.000 | 0.536 | -0.464 | [-0.525, -0.407] | 130 | 0 | 150 | 0.000000 |
| Main: blind -> no-rewrite | hallucination | 0 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 | 1.000000 |
| Main: blind -> no-rewrite | hallucination | 1 | 0.237 | 0.000 | -0.237 | [-0.368, -0.105] | 9 | 0 | 29 | 0.003906 |
| Main: blind -> no-rewrite | hallucination | 2 | 0.500 | 0.000 | -0.500 | [-0.658, -0.342] | 19 | 0 | 19 | 0.000004 |
| Main: blind -> no-rewrite | hallucination | 4 | 0.842 | 0.000 | -0.842 | [-0.947, -0.711] | 32 | 0 | 6 | 0.000000 |
| Main: blind -> no-rewrite | hallucination | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | hallucination | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | conflict | 0 | 0.000 | 0.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 | 1.000000 |
| Main: blind -> no-rewrite | conflict | 1 | 0.393 | 0.000 | -0.393 | [-0.571, -0.214] | 11 | 0 | 17 | 0.000977 |
| Main: blind -> no-rewrite | conflict | 2 | 0.643 | 0.000 | -0.643 | [-0.821, -0.464] | 18 | 0 | 10 | 0.000008 |
| Main: blind -> no-rewrite | conflict | 4 | 0.929 | 0.000 | -0.929 | [-1.000, -0.821] | 26 | 0 | 2 | 0.000000 |
| Main: blind -> no-rewrite | conflict | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | conflict | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 0 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 1 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 2 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 4 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 8 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | unsafe | 16 | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 | 0.000000 |
| Main: blind -> no-rewrite | benign | 0 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 0 | 0 | 280 | 1.000000 |
| Main: blind -> no-rewrite | benign | 1 | 0.896 | 0.925 | 0.029 | [0.011, 0.050] | 0 | 8 | 272 | 0.007812 |
| Main: blind -> no-rewrite | benign | 2 | 0.832 | 0.868 | 0.036 | [0.014, 0.061] | 0 | 10 | 270 | 0.001953 |
| Main: blind -> no-rewrite | benign | 4 | 0.671 | 0.714 | 0.043 | [0.021, 0.068] | 0 | 12 | 268 | 0.000488 |
| Main: blind -> no-rewrite | benign | 8 | 0.461 | 0.529 | 0.068 | [0.039, 0.100] | 0 | 19 | 261 | 0.000004 |
| Main: blind -> no-rewrite | benign | 16 | 0.475 | 0.536 | 0.061 | [0.036, 0.089] | 0 | 17 | 263 | 0.000015 |

Interpretation note: `benign` uses accuracy, while the other families use failure endpoints, so negative deltas on risk families are improvements.
Paper-safety note: do not mix this synthetic table with real TierMem or official public-baseline result tables.
