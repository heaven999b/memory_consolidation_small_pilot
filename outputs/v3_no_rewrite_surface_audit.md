# V3 No-Rewrite Surface Audit

Audit of the synthetic no-rewrite surface, focused on evidence class, N coverage, deterministic rows, and tie-heavy slices.

- evidence class: `synthetic_dry_run`
- runtime: `legacy_compaction_simulator`
- paper safe: `False`
- do_not_mix_with_real_results: `True`
- comparison depths: `[0, 1, 2, 4, 8, 16]`
- statistics depths: `[0, 1, 2, 4, 8, 16]`
- statistics rows: `72`
- deterministic rows: `45`
- perfect tie rows: `25`

## Deterministic Warning

- Exact `0.000` / `+/-1.000` deltas with zero-width confidence intervals are present on this surface.
- That pattern is consistent with rule-constrained or by-construction dry-run behavior, not with ordinary stochastic LLM output.

## Tie Warning

- Some blind-vs-query-aware rows are perfect ties across all paired items.
- That means those family metrics are not expressing useful sensitivity on this surface and should be treated as proxy diagnostics only.

## Focus Rows

| Comparison | Family | N | Delta | 95% CI | Left-win | Right-win | Ties |
|---|---|---:|---:|---|---:|---:|---:|
| Fairness: blind -> query-aware | hallucination | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Fairness: blind -> query-aware | hallucination | 1 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Fairness: blind -> query-aware | hallucination | 2 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Fairness: blind -> query-aware | hallucination | 4 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Fairness: blind -> query-aware | hallucination | 8 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Fairness: blind -> query-aware | hallucination | 16 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Fairness: blind -> query-aware | conflict | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Fairness: blind -> query-aware | unsafe | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 |
| Fairness: blind -> query-aware | unsafe | 1 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 |
| Fairness: blind -> query-aware | unsafe | 2 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 |
| Fairness: blind -> query-aware | unsafe | 4 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 |
| Fairness: blind -> query-aware | unsafe | 8 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 |
| Fairness: blind -> query-aware | unsafe | 16 | 0.000 | [0.000, 0.000] | 0 | 0 | 24 |
| Fairness: blind -> query-aware | benign | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 280 |
| Mechanism: query-aware -> no-rewrite | hallucination | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Mechanism: query-aware -> no-rewrite | hallucination | 8 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | hallucination | 16 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | conflict | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Mechanism: query-aware -> no-rewrite | conflict | 1 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Mechanism: query-aware -> no-rewrite | conflict | 2 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Mechanism: query-aware -> no-rewrite | conflict | 4 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Mechanism: query-aware -> no-rewrite | conflict | 8 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Mechanism: query-aware -> no-rewrite | conflict | 16 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Mechanism: query-aware -> no-rewrite | unsafe | 0 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | unsafe | 1 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | unsafe | 2 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | unsafe | 4 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | unsafe | 8 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | unsafe | 16 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Mechanism: query-aware -> no-rewrite | benign | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 280 |
| Main: blind -> no-rewrite | hallucination | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 38 |
| Main: blind -> no-rewrite | hallucination | 8 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 |
| Main: blind -> no-rewrite | hallucination | 16 | -1.000 | [-1.000, -1.000] | 38 | 0 | 0 |
| Main: blind -> no-rewrite | conflict | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 28 |
| Main: blind -> no-rewrite | conflict | 8 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 |
| Main: blind -> no-rewrite | conflict | 16 | -1.000 | [-1.000, -1.000] | 28 | 0 | 0 |
| Main: blind -> no-rewrite | unsafe | 0 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Main: blind -> no-rewrite | unsafe | 1 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Main: blind -> no-rewrite | unsafe | 2 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Main: blind -> no-rewrite | unsafe | 4 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Main: blind -> no-rewrite | unsafe | 8 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Main: blind -> no-rewrite | unsafe | 16 | -1.000 | [-1.000, -1.000] | 24 | 0 | 0 |
| Main: blind -> no-rewrite | benign | 0 | 0.000 | [0.000, 0.000] | 0 | 0 | 280 |

## Conclusion

This surface is a synthetic dry-run over a legacy simulator. It is useful for mechanism instantiation and audit, but it is not real-model evidence and should not appear in the same result layer as TierMem or official public-baseline tables.
