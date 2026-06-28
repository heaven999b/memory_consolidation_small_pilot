# Verification Round 12

这个文件是对 actual hallucination stress round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `192`, observed `192`.
- [PASS] Stress slice triggers tentative hallucination behavior at N=1: N=1 tentative_guess_note_rate = `0.125`.
- [PASS] Note-aware detector lowers false-present at N=1 under actual stress: `scale_aware_note_aware` = 0.062; `scale_aware_unified` = 0.125.
- [PASS] Tentative clue pressure does not persist to high N in the actual stress slice: N=4/N=8 tentative_guess_note_rate = 0.000/0.000.
- [PASS] Note-aware detector keeps zero residual contamination at N=8: `scale_aware_note_aware` residual = 0.000.
- [PASS] Note-aware detector does not underperform unified on accuracy at N=8: `scale_aware_note_aware` accuracy = 1.000; `scale_aware_unified` = 1.000.

## Bottom Line

如果这些检查通过，更准确的结论是：detector transfer 已经在真实模型-backed stress 下被局部触发，但这个 stress signal 在更高 N 会被 compaction 自己洗掉，因此下一轮要么扩大 N=1/2 hallucination slice，要么设计更持久的 actual hallucination cue。
