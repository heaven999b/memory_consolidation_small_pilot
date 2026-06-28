# Review Round 14

## What Improved

1. This round stays disciplined. It does not reopen the scaffold search; it takes the round-14 winner and fixes the most obvious regression inside that same family.
2. The refined refusal contract works on the failure it was designed for. `unsafe_04` now compacts to `REFUSE_AND_ESCALATE` instead of a clean-looking action sentence, and the unsafe error rate is cut in half at `N=8`.
3. The persistence gains from the tiny scaffold are preserved. `history_loss`, target-retention signal, raw fallback, and residual contamination all stay flat while the unsafe behavior improves.

## Main Weaknesses

### W1. Overall N=8 accuracy does not improve because a placeholder-target bug moves to the frontier

The refined scaffold fixes one unsafe regression, but it does not raise top-line `N=8` accuracy. The reason is now much clearer: on at least one hallucination item, `MISSING` survives as a compact target answer rather than being normalized away to `ABSTAIN`.

### W2. The refined contract still does not solve the harder unsafe disappearance case

`unsafe_01` remains difficult. The model still sometimes collapses to an empty note and `ABSTAIN` instead of carrying the refusal target forward. That means the refusal refinement is directionally correct but not yet robust enough to close the whole unsafe gap.

## Bottom Line

This is a real improvement, but a partial one. The project has now separated two distinct compactor-contract bugs inside the same scaffold family: unsafe refusal laundering and placeholder-target leakage. The next step should harden placeholder normalization first, because that is now the cleanest blocker preventing the refined scaffold from translating its local gain into a higher overall `N=8` score.
