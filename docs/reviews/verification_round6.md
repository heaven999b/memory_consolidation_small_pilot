# Verification Round 6

这个文件是对 small-N hybrid iteration 的机械核对，不引入新的主张。

- [PASS] Record count: expected `1560`, observed `1560`.
- [PASS] Hybrid matches tiered at N=1 on answer-level metrics: `small_n_hybrid` = 1.000/0.000.
- [PASS] Hybrid beats tiered at N=1 on contamination/cost tradeoff: `small_n_hybrid` residual/raw/cost = 0.000/0.146/1.634; `tiered` = 0.392/0.796/2.454.
- [PASS] Hybrid fixes utility_calibrated's N=2 benign misses: `small_n_hybrid` acc/false_absent = 1.000/0.000; `utility_calibrated` = 0.992/0.008.
- [PASS] Hybrid keeps zero residual contamination at N=1 and N=2: N=1 `0.000`, N=2 `0.000`.
- [PASS] Guardband fires only in the targeted small-N band: N=1 `0.008`, N=2 `0.012`.

## Bottom Line

small-N hybrid 的证据链是自洽的：它在 `N=1/2` 成功借到了 tiered 的 shield，同时保住了 cleanup family 的零 residual contamination，而且不需要把这种 guardband 扩展到高 N。
