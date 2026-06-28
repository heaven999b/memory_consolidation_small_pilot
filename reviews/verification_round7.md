# Verification Round 7

这个文件是对 scale-aware unified iteration 的机械核对，不引入新的主张。

- [PASS] Record count: expected `13000`, observed `13000`.
- [PASS] Unified matches small_n_hybrid at N=1: `scale_aware_unified` = 1.000/0.000/0.146; `small_n_hybrid` = 1.000/0.000/0.146.
- [PASS] Unified matches small_n_hybrid at N=2: `scale_aware_unified` = 1.000/0.000/0.331; `small_n_hybrid` = 1.000/0.000/0.331.
- [PASS] Unified matches utility_calibrated at N=4: `scale_aware_unified` = 0.996/0.004/0.512; `utility_calibrated` = 0.996/0.004/0.512.
- [PASS] Unified matches utility_calibrated at N=8: `scale_aware_unified` = 0.985/0.015/0.600; `utility_calibrated` = 0.985/0.015/0.600.
- [PASS] Unified beats tiered at N=1 on contamination/cost tradeoff: `scale_aware_unified` residual/raw/cost = 0.000/0.146/1.634; `tiered` = 0.392/0.796/2.454.
- [PASS] Unified keeps zero residual contamination across all N: all reported `residual_bad_memory_rate` values are `0.000`.

## Bottom Line

scale-aware unified 的证据链是自洽的：它没有创造一个全新的神奇点，而是准确保留了小 N 和高 N 两端已经验证过的局部最优行为。
