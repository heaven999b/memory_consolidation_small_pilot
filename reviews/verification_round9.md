# Verification Round 9

这个文件是对 note-aware detector round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `1280`, observed `1280`.
- [PASS] Note-aware detector lowers hallucination false-present at N=4: `scale_aware_note_aware` = 0.000; `scale_aware_unified` = 0.350.
- [PASS] Note-aware detector lowers hallucination false-present at N=8: `scale_aware_note_aware` = 0.000; `scale_aware_unified` = 0.400.
- [PASS] Note-aware detector keeps zero residual contamination at N=4 and N=8: N=4 `0.000`, N=8 `0.000`.
- [PASS] Accuracy does not collapse relative to unified at high N: `scale_aware_note_aware` acc = 0.963; `scale_aware_unified` = 0.975.
- [PASS] Benign false-absent does not spike at N=8: `scale_aware_note_aware` = 0.150; `scale_aware_unified` = 0.100.

## Bottom Line

如果这些检查通过，说明 note-aware detector 的收益是真正聚焦在 hallucination recover 误报，而不是通过重新引入大范围 abstain 把主线结果打坏。
