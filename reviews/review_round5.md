# Review Round 5

## What Improved

1. This iteration follows the autoresearch pattern more faithfully: one new direction, one focused experiment, then a separate verification artifact that checks the evidence chain mechanically.
2. The direction itself is cleaner. Instead of inventing another policy family, we calibrated the detector inside the existing cleanup policy and tested whether the gains survive on the same audited regression set.
3. The result is meaningful. `utility_calibrated` improves on `utility_first` at `N = 1`, `N = 4`, and `N = 8`, while preserving `residual_bad_memory_rate = 0.000` across all `N`.

## Main Weaknesses

### W1. Calibration helped recall, but not hallucination-side waste

The new profile rescues some low-score conflict and benign recovery cases, but it does not materially reduce high-`N` false-present behavior on hallucination items. That means the next gain is likely to come from better probe features, not another threshold nudge.

### W2. Tiered still has the best small-`N` shield

`utility_calibrated` becomes stronger at larger `N`, but `tiered` still wins the `N = 1` matched comparison on pure answer-level metrics. So the cleanup family is not yet the universal winner; its advantage is clearest once consolidation depth is no longer trivial.

### W3. The realism ceiling is still the synthetic compactor

The detector story is now substantially better instrumented, but the compactor and the cost model are still proxy components. This framework iteration improves trust in the experimental logic, not in the external validity of the absolute numbers.

## Bottom Line

This was the right next step. The framework did not need another architecture explosion; it needed a targeted repair on the component that had become the bottleneck. That repair worked: `utility_calibrated` is now the stronger cleanup profile, and the remaining weaknesses are clearer and more structural.
