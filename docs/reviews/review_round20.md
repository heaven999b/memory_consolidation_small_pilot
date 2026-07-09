# Review Round 20

## What Improved

1. The typed refinement achieves exactly what round 19 asked for. `typed_selective_anchor` fixes the lone high-`N` frontier error on `halu_05`: both unified and note-aware now return `ABSTAIN` at `N=8` for both seeds, rather than drifting into `REFUSE_AND_ESCALATE`.
2. The new midpoint is strictly better than the old one on realism. `summary_only` accuracy rises from `0.500`/`0.438` under `selective_anchor` to `0.562`/`0.562` at `N=4/8`, while strong-anchor behavior remains untouched and soft-anchor remains the lower-signal control.
3. The detector result survives the typing pass. Under `typed_selective_anchor`, unified `false_present` stays at `0.188`/`0.062` for `N=4/8`, and `scale_aware_note_aware` still reduces both to `0.000` with `1.000` accuracy and `0.000` residual contamination.

## Main Weaknesses

### W1. The remaining detector work is now concentrated in a tiny surrogate family set

At `N=8`, typed clue survival is carried only by `halu_01`, `halu_02`, `halu_03` seed11, and `halu_12` seed11. The actual false-present event at high `N` is narrower still: only `halu_12` triggers unified raw recovery there. This is a better realism point, but the detector phenomenon is now visibly concentrated rather than broad.

### W2. Preference-style and relational-person surrogates are still bundled together

The typed rule cleanly removed policy-window errors, but it still treats several different surrogate families as one bucket. `mentor -> manager`, `manager -> emergency_contact`, and `travel_preference -> medical_restriction` are probably not equally natural. The next round should separate identity-like surrogates from preference-style surrogates rather than keep calling all of them `plausible_surrogate`.

## Bottom Line

This is a real frontier step, not just a cleanup patch. `typed_selective_anchor` becomes the new midpoint baseline: it improves realism, preserves the high-`N` note-aware detector win, and removes the previous typed-semantics bug. The next step should be a surrogate-family decomposition round, especially identity-like versus preference-like surrogates.
