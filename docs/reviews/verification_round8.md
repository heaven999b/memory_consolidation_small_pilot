# Verification Round 8

这个文件是对 textual proxy slice iteration 的机械核对，不引入新的主张。

- [PASS] Record count: expected `1280`, observed `1280`.
- [PASS] Summary-only still worsens with deeper consolidation in the textual slice: N=1 `0.350` vs N=8 `0.875`.
- [PASS] Unified beats tiered on low-N contamination/cost tradeoff in the textual slice: `scale_aware_unified` residual/raw/cost = 0.000/0.212/1.920; `tiered` = 0.588/0.713/2.500.
- [PASS] Unified preserves its high-N advantage over tiered on residual contamination and raw fallback: `scale_aware_unified` residual/raw = 0.000/0.463; `tiered` = 0.875/0.912.
- [PASS] Unified stays at or above utility_calibrated on the small-N slice: `scale_aware_unified` acc/prop = 1.000/0.000; `utility_calibrated` = 0.975/0.025.
- [PASS] Unified remains materially better than summary-only at N=4: `scale_aware_unified` N=4 acc/prop = 0.988/0.013; `summary_only` N=8 propagation = 0.875.

## Bottom Line

textual proxy slice 的结果如果通过这些核对，说明 unified policy 的核心故事并没有只活在原始 claim-level proxy 里，而是开始跨到更接近自由文本摘要的环境中。
