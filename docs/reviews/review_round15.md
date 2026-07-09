# Review Round 15

## What Improved

1. This round is exactly the kind of cheap structural fix the framework hopes for after a good diagnosis. No new prompt search, no new route family, and no extra model behavior assumptions were needed.
2. The fix works cleanly. Placeholder hardening removes the `MISSING`-as-answer failure on the hallucination side and lifts `scale_aware_unified` / `scale_aware_note_aware` back to `0.917` accuracy at `N=8`.
3. Importantly, the gain is not bought by sacrificing the round-15 refusal improvement. Unsafe error stays at `0.500`, raw fallback stays at `0.417`, and residual contamination stays at `0.000`.

## Main Weaknesses

### W1. The remaining failure is now empty/null scaffold disappearance, not placeholder leakage

The frontier has moved again. `unsafe_01` still collapses to an empty or null structured output, which means the refusal scaffold disappears and the final answer falls back to `ABSTAIN`. That is now the clearest remaining gap.

### W2. The winning scaffold family depends on an explicit parser contract

This is not a problem so much as a design lesson: the model can emit a superficially clean placeholder claim with `supported=true`, and the system must still override it. Future scaffold variants should assume the parser contract is part of the method, not an afterthought.

## Bottom Line

This is a strong round. The project now has a refined scaffold plus a hardened parser that together recover the top-line `N=8` accuracy frontier while preserving the new unsafe gain. The next step should stay in the same family and add carry-forward fallback for empty passes, because that is now the main blocker left.
