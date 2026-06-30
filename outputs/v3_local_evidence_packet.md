# V3 Local Evidence Packet

Consolidated local synthetic dry-run packet for the current V3 transition state.

## Current State

- Evidence class: `synthetic_dry_run`
- Paper safe: `False`
- Do-not-mix-with-real-results: `True`
- TierMem week-0 gate: `partial`
- Public baseline readiness: `partial`
- No-rewrite audit N=8 blocked protected rate: `0.9783`
- No-rewrite comparison item count: `185`
- Local N sweep: `[0, 1, 2, 4, 8, 16]`
- Local seeds: `[11, 23]`
- Local architectures: `['raw_only', 'summary_only', 'summary_query_aware', 'summary_only_no_rewrite', 'summary_query_aware_no_rewrite', 'tiered', 'tiered_no_rewrite']`
- Capability counts: `{'yes': 8, 'partial': 4, 'no': 0}`

## Main Synthetic Statistical Readout (blind -> no-rewrite at N=16)

| Family | Left | Right | Delta | 95% CI | McNemar p |
|---|---:|---:|---:|---|---:|
| hallucination | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 0.000000 |
| conflict | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 0.000000 |
| unsafe | 1.000 | 0.000 | -1.000 | [-1.000, -1.000] | 0.000000 |
| benign | 0.475 | 0.536 | 0.061 | [0.036, 0.089] | 0.000015 |

## Mechanism Decomposition

- On this synthetic proxy surface, `query-aware` alone fixes the current local `conflict` collapse and restores `benign` accuracy (`0.475` -> `1.000` at `N=16`), but it does not reduce `hallucination` or `unsafe` risk in this dry-run surface.
- On the same synthetic surface, `no-rewrite` is the part that removes the local `hallucination` and `unsafe` failures: `hallucination` risk `1.000` -> `0.000`, `unsafe` risk `1.000` -> `0.000` at `N=16`.
- Relative to the blind summary baseline, `summary_only_no_rewrite` gives a smaller but still synthetic-only significant `benign` gain (`0.475` -> `0.536`), while fully removing the three local risk-family failures.

## Cost Readout

- At `N=8`, `summary_only_no_rewrite` reaches local safety score `1.0` at mean proxy cost `2.49`, versus `raw_only` cost `3.2` and `tiered` cost `4.001`.
- At the same `N=8`, `summary_query_aware` is cheap and recall-friendly (mean cost `2.47`), but it still leaves hallucination and unsafe risk untouched in this local proxy setting.

## Interpretation

- This packet is useful for local mechanism instantiation, fairness pairing, and audit scaffolding, but it is still synthetic dry-run evidence.
- The strongest safe conclusion here is narrow: in the legacy simulator, query awareness aligns with conflict/benign recovery, while the no-rewrite rule aligns with hallucination/unsafe suppression.
- The decisive remaining gap is empirical: real TierMem runs, real public baselines, real benchmark data placement, and real external credentials.
