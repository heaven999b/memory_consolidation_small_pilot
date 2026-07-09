# Verification Round 5

这个文件是对 detector-calibration iteration 的机械核对，不引入新的主张。

- [PASS] Record count: expected `10400`, observed `10400`.
- [PASS] Utility calibrated beats utility first at N=8: `utility_calibrated` = 0.985/0.015, `utility_first` = 0.973/0.019.
- [PASS] Utility calibrated keeps zero residual contamination: all reported `residual_bad_memory_rate` values are `0.000`.
- [PASS] Tiered still wins N=1 by answer-level metric: `tiered` = 1.000/0.000, `utility_calibrated` = 0.996/0.004.
- [PASS] Utility calibrated improves N=8 over tiered on contamination/cost tradeoff: `utility_calibrated` residual/raw/cost = 0.000/0.600/3.600; `tiered` = 0.927/0.973/3.997.
- [PASS] Calibration winner table contains 5 rows: observed `5` rows for `5` N values.

## Bottom Line

校准结论在证据链上是自洽的：`utility_calibrated` 不是全局无条件最优，但它确实修补了 `utility_first` 的一部分 detector recall miss，并在高 N 保持了比 `tiered` 更干净的 residual memory。
