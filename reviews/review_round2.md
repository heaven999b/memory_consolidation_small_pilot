# Review Round 2

## What Improved

1. The dataset is now meaningfully stronger: the pilot runs on a curated 52-item synthetic set spanning four families, and the strict audit passed with 0 hard errors and 0 warnings.
2. The earlier lightweight sample has effectively been replaced by clearer, more single-target, gold-aligned items, so the current readout is less likely to be driven by weak prompt construction.
3. The main signal survives expansion: `summary_only` still collapses with larger `N`, while `tiered` remains the only low-risk Pareto point on this synthetic setup.

## Main Weaknesses

### W1. Adaptive routing still does not beat tiered

`adaptive_tiered` and `adaptive_guarded` lower some raw fallback cost at high `N`, but they pay for it with materially worse benign recovery and hallucination handling. On the current frontier, they still do not provide the “same safety, lower cost” story we want.

### W2. Tiered is protecting outputs more than cleaning memory

The larger run exposes an important nuance: answer-level propagation stays very low under `tiered`, but latent compact-memory contamination still accumulates. `unsafe_retention` remains non-zero and `conflict_merge` rises with `N`, which means the current policy behaves like a strong answer-time shield rather than a true memory-consolidation repair mechanism.

### W3. The cost and compaction layers are still proxy components

The benchmark is now more trustworthy as a synthetic regression set, but `mean_cost` is still a proxy and the compactor is still hand-designed. That is acceptable for pre-pilot framing, but the next jump in credibility has to come from plugging in a real summarization operator and better cost accounting.

## Bottom Line

This iteration upgrades confidence in the framing: the core risk signal is no longer just a tiny-sample artifact. The next research move should focus less on adding more synthetic baselines and more on designing a router or cleanup policy that can reduce cost without leaving a contaminated latent memory behind.
