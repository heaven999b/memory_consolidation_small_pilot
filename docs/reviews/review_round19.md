# Review Round 19

## What Improved

1. This round breaks the realism deadlock from round 18. `selective_anchor` is a genuine middle regime rather than a cosmetic variant: `summary_only` accuracy rises from `0.062`/`0.062` under `strong_anchor` to `0.500`/`0.438` at `N=4/8`, while unified tentative-target persistence remains `0.375`/`0.375` instead of collapsing to `0.125`/`0.125` under `soft_anchor`.
2. The detector story survives inside that middle regime. Under `selective_anchor`, `scale_aware_note_aware` reduces `false_present` from `0.188` to `0.000` at `N=4` and from `0.062` to `0.000` at `N=8`, with seed-level non-loss `2/2` at both settings.
3. The traces now support a more nuanced mechanism claim. `must_copy` cases such as `halu_02` still behave like the hard stress instrument, `weak_context` cases such as `halu_14` collapse cleanly to `MISSING`, and plausible-surrogate cases such as `halu_03` / `halu_12` survive only intermittently rather than by force.

## Main Weaknesses

### W1. Selective clue survival is real, but still sparse

The new middle contract leaves unified tentative-target persistence at only `0.375`, so the remaining detector work is carried by a narrow subset of surrogate-friendly items rather than the whole slice. This is much more realistic than `strong_anchor`, but it is not yet a broad naturalistic detector setting.

### W2. The remaining high-N error is semantic over-refusal, not contamination

At `N=8`, both unified and note-aware selective runs miss exactly one case: `halu_05`. There, `retention_window=90 days` drifts into `retention_exception => 90 days`, and routing ends at `REFUSE_AND_ESCALATE` instead of `ABSTAIN`. That leaves selective high-`N` accuracy at `0.938` even though residual contamination stays at `0.000`.

## Bottom Line

This is the strongest realism advance so far on the actual stress slice. The project can now say there is a real middle region between adversarial clue preservation and total clue collapse. The next step should not be broader seed coverage again, but a typed selective-anchor refinement that keeps person/code-like surrogates while demoting policy-window and schedule-like anchors to `weak_context`.
