# Review Round 6

## What Improved

1. This iteration followed the autoresearch architecture cleanly: a new direction was chosen from the weakness router, the experiment scope was deliberately narrowed to `N=1/2`, and the result was verified in a separate artifact.
2. The chosen direction worked. `small_n_hybrid` closes the remaining small-`N` gap without turning into a broad fallback policy.
3. The gain is not subtle. At `N=1`, `small_n_hybrid` matches `tiered` on answer-level correctness (`1.000` accuracy, `0.000` propagation) while keeping cleanup-style `0.000` residual contamination and using far less raw fallback (`0.146` vs `0.796`).

## Main Weaknesses

### W1. The fix is local, not yet unified

This is a strong patch, but it is intentionally a patch. `small_n_hybrid` is only meant for the narrow small-`N` miss band; it does not answer what the single best all-`N` policy should be.

### W2. Detector quality is still the real long-term bottleneck

The guardband helps because the calibrated probe still confuses some small-`N` answerable cases. That means the local policy win does not remove the underlying detector-design problem, especially on the hallucination side at larger `N`.

### W3. Realism still bottoms out at the compactor and cost model

The framework now has a better scale-aware story in synthetic space, but that is still synthetic space. External validity still depends on replacing the proxy summarizer slice and upgrading cost accounting.

## Bottom Line

This was a good autoresearch-style round because it resisted the temptation to overgeneralize. Instead of pretending we had found the one universal policy, we isolated the remaining failure band, patched it locally, verified it mechanically, and learned that the next real move is a scale-aware unification rather than another isolated tweak.
