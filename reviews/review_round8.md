# Review Round 8

## What Improved

1. This round follows the autoresearch framework in the right way: once the policy skeleton became coherent, it stopped inventing new routing variants and instead pushed on environment realism.
2. The realism check worked. In the 16-item textual-proxy slice, `summary_only` still degrades sharply with larger `N`, while `scale_aware_unified` preserves the main cleanup-style advantage.
3. The advantage is not fragile. `scale_aware_unified` keeps `residual_bad_memory_rate` at `0.000` across the slice and remains better than `tiered` on raw fallback and cost at both low and high `N`.

## Main Weaknesses

### W1. The new environment is stronger, but it is still a proxy

The textual note compactor is much closer to a realistic summarization setting than the earlier claim-level proxy, but it is still hand-authored logic rather than an actual model-backed summarizer. This means the external-validity gap is narrower, not closed.

### W2. Detector weakness is now easier to see, not yet fixed

High-`N` hallucination-side false-present behavior survives the realism check. That is good diagnostically because it means the weakness is not just an artifact of the earlier environment, but it also means the next detector round should be more targeted.

### W3. The slice is intentionally small

This was the right scope for a realism checkpoint, but it is not yet the next benchmark. The slice should only grow after the same signal survives an actual summarizer on the current audited items.

## Bottom Line

This was the right next step. The project now has evidence that the unified-policy story is not confined to one synthetic environment. The next serious move is not another policy patch; it is either a detector-focused hallucination round or, preferably, an actual summarizer on the same audited slice.
