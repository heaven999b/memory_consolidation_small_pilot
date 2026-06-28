# Verification Round 10

这个文件是对 actual summarizer slice 的机械核对，不引入新的主张。

- [PASS] Record count: expected `128`, observed `128`.
- [PASS] Summary-only still worsens with deeper consolidation under the actual summarizer: N=1 `0.250` vs N=8 `0.625`.
- [PASS] Unified beats tiered on high-N contamination and raw fallback under the actual summarizer: `scale_aware_unified` residual/raw = 0.000/0.500; `tiered` = 0.125/0.750.
- [PASS] Actual slice does not reintroduce hallucination false-present under the cleanup family at N=8: `scale_aware_note_aware` = 0.000; `scale_aware_unified` = 0.000.
- [PASS] Note-aware detector keeps zero residual contamination at N=8: `scale_aware_note_aware` residual = 0.000.
- [PASS] Note-aware detector does not underperform unified at N=8 on accuracy: `scale_aware_note_aware` accuracy = 0.625; `scale_aware_unified` = 0.625.

## Bottom Line

如果这些检查通过，说明真实 summarizer slice 已经保留住主线趋势；至于 detector gain，本轮更准确的结论是它没有被 actual slice 反驳，但也还没有在这个更保守的真实 summarizer 上再次被强力触发。
