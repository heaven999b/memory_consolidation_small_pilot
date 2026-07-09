# Review Round 9

## What Improved

1. This round follows the framework well because it does not invent a new policy family. It targets the specific remaining detector weakness from the weakness router: hallucination-side false-present recover under note-level compaction.
2. The result is sharp. `scale_aware_note_aware` removes hallucination false-present entirely on the textual slice at `N=4/8`.
3. The gain is mechanistically interpretable. It comes from note-level inference and missingness markers, not from collapsing back into broad tiered-style fallback.

## Main Weaknesses

### W1. The detector gain is a tradeoff, not free lunch

The note-aware detector becomes more conservative on some answerable benign cases. That is acceptable for a focused round, but it means the feature set should be read as a targeted fix rather than the final detector design.

### W2. This is still proxy-space detector evidence

The round says something real and useful, but it says it inside the textual-proxy environment. The next credibility test is whether the same detector logic matters once the compactor itself becomes model-backed.

## Bottom Line

This was a good detector round. It converts a previously identified weakness into a concrete, local, auditable fix. The next question is not whether the fix exists, but whether real summarization actually surfaces the same failure mode strongly enough for the fix to matter.
