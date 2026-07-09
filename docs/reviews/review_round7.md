# Review Round 7

## What Improved

1. This round completes an important autoresearch transition: a sequence of local fixes has now been consolidated into one structural policy, `scale_aware_unified`.
2. The unification is honest rather than decorative. Verification shows the unified policy exactly preserves the strongest known low-`N` and high-`N` behaviors instead of introducing a fresh compromise.
3. The project now has a coherent policy story across the full sweep. We are no longer choosing between unrelated local winners.

## Main Weaknesses

### W1. The main uncertainty is no longer policy choice

Once the unified policy is in place, the largest remaining uncertainty shifts to the detector and the environment. High-`N` hallucination-side false-present cost is now more important than another routing tweak.

### W2. Synthetic compaction is now the main realism gap

The framework has become internally coherent enough that its next failure mode is external validity. If the same policy advantage does not survive on a real summarizer slice, then the current synthetic conclusions will have reached their ceiling.

### W3. Cost still lacks operational grounding

The current `mean_cost` is useful for relative comparisons, but it is still proxy accounting. A stronger next round should either improve that accounting or clearly bracket its limitations.

## Bottom Line

This was the right structural move. The framework no longer needs another local policy invention before testing harder conditions. It now needs to carry the unified policy into a more realistic environment and see whether the story survives contact with a real summarizer and better cost signals.
