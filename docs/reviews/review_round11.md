# Review Round 11

## What Improved

1. This round does exactly what the framework needed next: it does not add another policy, it expands the real model-backed slice where the current bottleneck actually lives.
2. The new slice is more informative than the earlier 8-item checkpoint. With more benign/conflict coverage, the high-`N` failure mode becomes structurally clear rather than anecdotal.
3. The project now has stronger evidence that the real-model bottleneck has shifted. The main problem is no longer contamination propagation, but answerability evaporation under repeated compression.

## Main Weaknesses

### W1. The cleanup family still does not solve the real compaction bottleneck

`scale_aware_unified` keeps residual contamination at zero, which is good, but it only protects final answers by spending more raw fallback once compaction has already lost the target. That means the next intervention should target note persistence, not more detector tuning.

### W2. The slice is stronger, but still not broad

This is now much better evidence than the first actual slice, but it is still one seed and a limited audited subset. It is enough to localize the bottleneck, not enough to claim a stable benchmark frontier.

## Bottom Line

This round is important because it tells us where not to spend the next cycle. Another routing tweak would be lower-value than a compaction or memory-scaffold intervention aimed directly at `history_loss` and empty-note collapse.
