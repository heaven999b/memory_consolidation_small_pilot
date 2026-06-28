# Review Round 18

## What Improved

1. This is exactly the right follow-up to round 17. Instead of merely repeating the strong persistence result, the round converts it into a real robustness question: does the gain survive more than one seed, and does it depend on how aggressively the contract preserves clues?
2. The strong-contract result holds up well. Across two seeds on the full actual stress slice, `scale_aware_note_aware` keeps `false_present` at `0.000` for both `N=4` and `N=8`, while `scale_aware_unified` remains at `0.312` and `0.188`. Accuracy and residual contamination stay perfect.
3. The soft-contract control is highly informative. It does not merely weaken the result a little; it largely removes the detector problem itself by letting clue survival collapse. Under `soft_anchor`, unified tentative target-claim rate falls to `0.125` at both `N=4` and `N=8`, and the note-aware detector no longer has much work to do.

## Main Weaknesses

### W1. The project now faces a realism-vs-signal tradeoff rather than a detector doubt

The strong contract is useful precisely because it is harsh: it forces clue survival and makes detector transfer visible. But that comes with a realism cost. `summary_only` falls to `0.062` accuracy under `strong_anchor`, which is better read as a stress instrument than as a naturalistic compaction regime.

### W2. The soft control is cleaner, but perhaps too weak to preserve the phenomenon

`soft_anchor` is a useful negative control because it shows the effect is not automatic. At the same time, it may undershoot: once target clues mostly vanish, detector transfer is no longer testable. The next round should search for an intermediate contract, not merely choose between these two extremes.

## Bottom Line

This is a strong robustness round. The project can now say that high-`N` detector transfer under actual model-backed stress is not a one-seed fluke, but it can also say something more precise: the phenomenon depends on preserving weak target clues long enough for the detector to act. The next step should focus on intermediate stress realism, not on re-proving that the detector works under the current strongest contract.
