# Review Round 16

## What Improved

1. This round is unusually crisp. It changes only executor behavior, reuses all existing real-model outputs, and still delivers the largest single improvement since the scaffold line started.
2. The carry-forward rule solves exactly the failure it targeted. `unsafe_01` no longer disappears into `ABSTAIN`; the last valid refusal scaffold is preserved across null and missing-only passes.
3. The gain is cleanly additive. Placeholder hardening is preserved, raw fallback does not increase, residual contamination stays at zero, and the unified high-`N` actual recall slice now reaches `1.000` accuracy with `0.000` propagation.

## Main Weaknesses

### W1. This is still audited-slice evidence, not broad robustness evidence

The recall-side story is now very strong on the current slice, but it is still one seed and a limited audited subset. The next round should spend its budget on the next unresolved frontier rather than over-interpreting this as a benchmark-level result.

### W2. The main remaining frontier has shifted away from recall and back toward stress realism

The project no longer needs another recall-side micro-fix right now. The more interesting question is whether the stronger scaffold/executor contract changes the actual hallucination-stress line, where detector transfer is still only locally established.

## Bottom Line

This is a strong closing round for the recall-side bottleneck. The scaffold family now has a coherent prompt contract, parser contract, and executor contract. The next step should move laterally: apply this stronger contract to the actual hallucination-stress setting or broaden seed coverage, instead of continuing to patch the now-stable recall slice.
