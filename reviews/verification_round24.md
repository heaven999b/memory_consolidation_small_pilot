# Verification Round 24

这个文件是对 actual hallucination name-refinement pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `144`, observed `144`.
- [PASS] Focused pilot slice is the intended 6-item name-refinement set: observed slice ids = `['halu_15', 'halu_16', 'halu_17', 'halu_18', 'halu_19', 'halu_20']`.
- [PASS] Refined name branch still blocks code-overlap items: refined name branch signal count on code ids at N=8 = `0`.
- [PASS] Refined name branch fully removes detector-visible work from the weak anti-role pair: refined name branch signal count on weak-name ids at N=8 = `0`.
- [PASS] Refined name branch keeps detector-visible work on both strengthened aligned-name items: refined name branch strengthened-name signal/tent/raw at N=8 = `2`/`2`/`2`.
- [PASS] Refined name branch improves compact-stable clue survival on strengthened-name items: baseline/refined strengthened-name tentative counts at N=8 = `1`/`2`.
- [PASS] Refined name branch removes the weak-pair false tentative that remained in the baseline name branch: baseline/refined weak-name tentative counts at N=8 = `1`/`0`.
- [PASS] Refined summary-only realism improves over the baseline name-only branch: baseline/refined summary_only N=8 accuracy = `0.500`/`0.667`.
- [PASS] Refined name note-aware branch is non-worse than the baseline at high N: baseline/refined note-aware false_present at N=8 = `0.333`/`0.333`.
- [PASS] Refined name unified false-present does not regress relative to the baseline: baseline/refined unified false_present at N=8 = `0.333`/`0.333`.
- [PASS] All refined note-aware runs keep zero residual contamination at N=8: refined note-aware residual at N=8 = `0.000`.

## Bottom Line

如果这些检查通过，说明 name-only scaffold tightening 的主要收益已经被机械确认：weak anti-role names 被稳定压回 MISSING，strong aligned names 从 recoverable signal 更靠近 compact-stable clue，同时 summary-only realism 变好；但 detector-side false_present 还没有继续下降，所以前沿问题已从 data split 转成 executor / carry-forward consistency。
