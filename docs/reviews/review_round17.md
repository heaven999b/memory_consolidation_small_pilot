# Review Round 17

## What Improved

1. This is the right lateral move after the recall slice stabilized. Instead of piling on another recall-side patch, the round carries the winning scaffold/parser/executor contract back into the actual hallucination-stress setting where the remaining scientific question still lived.
2. The main result is genuinely stronger than the old local `N=1` win. Tentative clue persistence now survives at high `N`: under `scale_aware_unified`, `tentative_target_claim_rate` reaches `0.875` at both `N=4` and `N=8`, whereas the old actual stress slice had already washed the clue away by then.
3. The detector gain is now persistent rather than local. On the full actual stress slice, `scale_aware_note_aware` lowers `false_present` from `0.500` to `0.000` at `N=4` and from `0.375` to `0.000` at `N=8`, while matching unified on `1.000` accuracy and `0.000` residual contamination.

## Main Weaknesses

### W1. This stress line is intentionally aggressive and should not be mistaken for naturalistic summarizer behavior

The stronger anchor-style scaffold does exactly what it was designed to do: it makes unsupported target clues survive. But that also means `summary_only` collapses to `0.000` accuracy across the slice. As a research instrument, that is useful; as a model of ordinary free-form compaction, it is clearly harsher than the earlier actual stress condition.

### W2. Robustness is still narrower than the result quality might make it feel

The round is full-slice and real-model-backed, which is a real step up, but it is still one seed and one strong clue-persistence contract. The next question is no longer whether detector transfer can survive into high `N` here; it is whether the same gain survives broader seeds or a softer anchor policy.

## Bottom Line

This is a strong round. The project now has a real-model stress condition where clue persistence survives long enough for note-aware detection to matter beyond `N=1`. The next step should focus on robustness, not on reopening the now-settled question of whether actual high-`N` detector transfer is possible at all.
