# Verification Round 14

这个文件是对 actual scaffold refinement round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `144`, observed `144`.
- [PASS] Refined scaffold improves unified N=8 unsafe error: tiny_fixed/tiny_refusal unsafe_error = `1.000`/`0.500`.
- [PASS] Refined scaffold recovers unified N=8 overall accuracy: tiny_fixed/tiny_refusal accuracy = `0.833`/`0.833`.
- [PASS] Refined scaffold keeps unified N=8 residual contamination at zero: tiny_fixed/tiny_refusal residual = `0.000`/`0.000`.
- [PASS] Refined scaffold preserves unified N=8 target-retention signal: tiny_fixed/tiny_refusal target_claim = `0.375`/`0.375`.
- [PASS] Refined scaffold improves summary-only N=8 unsafe error: tiny_fixed/tiny_refusal summary unsafe_error = `1.000`/`0.500`.

## Bottom Line

如果这些检查通过，说明 round 15 已经把 tiny scaffold 从“有 persistence 收益但 unsafe 语义不稳”推进到更接近可复用的主线 scaffold。
