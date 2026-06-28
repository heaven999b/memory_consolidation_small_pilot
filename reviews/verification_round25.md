# Verification Round 25

这个文件是对 actual hallucination name-normalization pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `108`, observed `108`.
- [PASS] Focused pilot slice is the intended 6-item name-normalization set: observed slice ids = `['halu_15', 'halu_16', 'halu_17', 'halu_18', 'halu_19', 'halu_20']`.
- [PASS] Normalized branch still blocks code-overlap items: normalized branch signal count on code ids at N=8 = `0`.
- [PASS] Normalized branch still blocks the weak anti-role pair: normalized branch signal count on weak-name ids at N=8 = `0`.
- [PASS] Normalized branch keeps full strong-name signal: normalized strengthened-name signal/tent/raw at N=8 = `2`/`2`/`2`.
- [PASS] Normalized branch makes both strengthened-name notes scaffold-stable: refined/normalized strengthened-name scaffold counts at N=8 = `1`/`2`.
- [PASS] Normalized note-aware false-present improves over refined at high N: refined/normalized note-aware false_present at N=8 = `0.333`/`0.000`.
- [PASS] Normalized note-aware abstains on both strengthened-name items: normalized note-aware strengthened-name routes at N=8 = `[('halu_19', 'utility_calibrated_abstain', 'absent'), ('halu_20', 'utility_calibrated_abstain', 'absent')]`.
- [PASS] Normalized unified false-present does not regress relative to refined: refined/normalized unified false_present at N=8 = `0.333`/`0.333`.
- [PASS] Normalized summary-only realism stays at least as strong as refined: refined/normalized summary_only N=8 accuracy = `0.667`/`0.667`.
- [PASS] All normalized note-aware runs keep zero residual contamination at N=8: normalized note-aware residual at N=8 = `0.000`.

## Bottom Line

如果这些检查通过，说明 aligned-name note normalization 确实补到了前一轮的真空地带：它没有改变 unified side 的 detector pressure，却把 strongest aligned-name cases 的 final note 全部归一成可解析 scaffold，并把 note-aware `N=8 false_present` 从 `0.333` 压到 `0.000`。
