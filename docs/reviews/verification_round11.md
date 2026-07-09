# Verification Round 11

这个文件是对 actual recall expansion round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `288`, observed `288`.
- [PASS] Summary-only benign/conflict errors worsen with deeper real-model compaction: N=1 `0.062` vs N=8 `0.875`.
- [PASS] High-N empty-note-then-abstain emerges in the expanded recall slice: N=8 empty_note_then_abstain = `0.312`.
- [PASS] Unified still beats tiered on high-N contamination and raw fallback in the recall slice: `scale_aware_unified` residual/raw = 0.000/0.583; `tiered` = 0.083/0.750.
- [PASS] Unified keeps zero residual contamination even when history loss rises: residual/history_loss = 0.000/0.875.
- [PASS] Note-aware detector does not underperform unified on the recall slice at N=8: `scale_aware_note_aware` accuracy = 0.875; `scale_aware_unified` = 0.875.

## Bottom Line

如果这些检查通过，说明扩大的真实 slice 已经把 bottleneck 指向 benign/conflict answerability loss，而不是把我们带回更早的污染传播问题。
