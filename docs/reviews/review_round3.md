# Review Round 3

## What Improved

1. The experiment now distinguishes latent contamination from residual contamination, so we can finally tell whether a policy is actually cleaning memory or just masking it with raw fallback.
2. The new `risk_first` and `utility_first` conditions are materially stronger than the earlier adaptive baselines: they scrub unsupported / unsafe / stale claims before answering and then use a lightweight side signal to decide between safe direct output and raw recovery.
3. The central empirical story is now sharper. `utility_first` is the matched-`N` best non-raw policy for `N >= 1`, keeping `1.000` accuracy, `0.000` propagation, and `0.000` residual contamination through `N = 8` while cutting raw escalation nearly in half relative to `tiered`.

## Main Weaknesses

### W1. The side signal is still optimistic

`utility_first` does not use family labels anymore, but it still relies on `verified_target_exists`, which is derived from backing-store structure. That is a better abstraction than an oracle family tag, but it is still more favorable than what many real systems would get for free.

### W2. `risk_first` shows the expected utility cliff

The cheaper policy is not “free lunch” better. It keeps residual contamination at zero, but it under-recovers low-critical benign cases and falls to `0.600` benign-family accuracy at `N = 8`. That tradeoff is useful, but it means `risk_first` is not yet the general solution.

### W3. Proxy cost and proxy compaction remain the main realism bottlenecks

This iteration improves the internal logic of the benchmark, but the cost model and the summarization operator are still synthetic. The current result is best interpreted as a design signal: cleanup-style policy is more promising than pure router-threshold tuning on this controlled setup.

## Bottom Line

This is the first iteration where the framework says something more specific than “tiered helps.” On the current audited regression set, the winning move is not just smarter fallback; it is to clean the compact memory first, then recover from raw only when a verified answer should exist. The next step is to see how much of that advantage survives once the side signal and summarizer become more realistic.
