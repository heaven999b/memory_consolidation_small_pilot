# Review Round 4

## What Improved

1. The cleanup-policy result is now more believable because `utility_first` and `risk_first` no longer rely on a direct backing-store oracle. They use an explicit noisy retrieval probe, and the probe state now appears in exemplar traces.
2. The main result survives the harder setting. `utility_first` is weaker than before, but it still becomes the matched-`N` best non-raw policy for `N >= 2`.
3. The tradeoff is sharper and more realistic now. At `N = 8`, `utility_first` gives up a little answer accuracy relative to `tiered` (`0.973` vs `0.977`) but reduces propagation (`0.019` vs `0.023`), removes residual contamination entirely (`0.000` vs `0.927`), and still uses substantially less raw fallback (`0.588` vs `0.973`).

## Main Weaknesses

### W1. Detector calibration is now the bottleneck

The side signal is no longer unrealistically strong, which is good, but that also means the probe now drops some answerable benign/conflict cases. Tiered retaking the matched-`N` lead at `N = 1` is the clearest sign that the next gain will come from detector recall, not another router variant.

### W2. `risk_first` is too conservative under the harder probe

Once the probe becomes noisy, the cheaper policy falls off harder. By `N = 8`, `risk_first` drops to `0.835` accuracy and `0.158` propagation, mostly because it refuses to recover enough benign utility cases.

### W3. The benchmark is still synthetic where it matters most

The compactor and the cost model are still proxy components. This round increases trust in the experimental logic, but the next credibility jump still requires a real summarizer slice and better cost accounting.

## Bottom Line

The story changed in a healthy way. We no longer have an implausibly perfect cleanup policy; we have a more realistic one that still looks promising under a harder detector. That makes the next step clearer: tune or replace the probe, then see whether `utility_first` keeps its edge once retrieval uncertainty is modeled even more honestly.
