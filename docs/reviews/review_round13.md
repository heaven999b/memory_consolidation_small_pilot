# Review Round 13

## What Improved

1. This round finally attacks the real bottleneck directly instead of circling it with more routing logic. The intervention lives inside the compaction contract itself, which is exactly what the framework called for after round 12.
2. `tiny_fixed_scaffold` is a real positive result, not just a stylistic change. On `summary_only`, it improves N=4 and N=8 target retention materially; on `scale_aware_unified`, it lowers raw fallback while keeping residual contamination at zero.
3. The round also usefully kills a branch. `target_field_anchor` is not a near-tie loser; it is a brittle prompt contract that often collapses into empty or vacuous notes and should not stay on the main frontier.

## Main Weaknesses

### W1. The winning scaffold still trades some final N=8 accuracy for lower raw fallback

Under `scale_aware_unified`, `tiny_fixed_scaffold` clearly improves persistence and reduces raw recovery pressure, but final N=8 accuracy drops from `0.917` to `0.833`. That means the project has not solved the real bottleneck yet; it has found the right intervention family.

### W2. Anchor-style prompt wording is too fragile under repeated compression

The contrast between the two interventions is instructive. A short slot-based scaffold survives. A natural-language anchor line often does not. The next prompt design cycle should treat that as a structural lesson, not as noise.

## Bottom Line

This is a good round because it converts note persistence from an abstract hypothesis into a concrete design direction. The next step should refine `tiny_fixed_scaffold` so it keeps the persistence gain while recovering the small answer-level loss at high `N`; reopening the failed anchor branch would be lower value.
