# Review Round 12

## What Improved

1. This round turns the detector-transfer question into a real-model stress test instead of leaving it at the textual proxy level.
2. The answer is more nuanced and more useful than a binary success/failure. Transfer does exist: at `N=1`, the note-aware detector removes actual false-present recover under a real model-backed stress condition.
3. The cache-aware rerun after marker expansion is especially valuable because it shows the result is mechanistic rather than accidental: the missing signal was partly in the detector features, not only in the model output.

## Main Weaknesses

### W1. The transfer signal is local, not persistent

By `N=4/8`, the tentative hallucination cue is largely gone. That means the detector cannot keep winning at higher `N` because the compaction chain has already erased the very evidence it would need.

### W2. Stress and compactor contract are still intertwined

The round also surfaces a separate formatting vulnerability: placeholder-style target answers and tentative clue phrasing can sit uncomfortably close together. That is partly a detector issue, but also a compactor-contract issue.

## Bottom Line

This is a meaningful positive result, but a local one. The project now has real-model evidence that detector transfer is possible. The next challenge is to make the hallucination cue survive longer, or else to focus that line of work on the small-`N` regime where the signal actually lives.
