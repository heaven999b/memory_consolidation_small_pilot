# Verification Round 26

这个文件是对 actual hallucination literal-normalization pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `180`, observed `180`.
- [PASS] Focused pilot slice is the intended 6-item mixed literal set: observed slice ids = `['halu_15', 'halu_16', 'halu_17', 'halu_18', 'halu_19', 'halu_20']`.
- [PASS] Normalization preserves code-overlap signal behavior: baseline/normalized code signal at N=8 = `1`/`1`.
- [PASS] Normalization preserves weak-name blocking behavior: baseline/normalized weak-name signal at N=8 = `0`/`0`.
- [PASS] Normalization preserves strengthened-name signal behavior: baseline/normalized strengthened-name signal/tent/raw at N=8 = `2`/`0`/`2` vs `2`/`0`/`2`.
- [PASS] Normalization makes both strengthened-name literal notes scaffold-stable: baseline/normalized strengthened-name scaffold counts at N=8 = `1`/`2`.
- [PASS] Normalized note-aware false-present is non-worse than baseline: baseline/normalized note-aware false_present at N=8 = `0.000`/`0.000`.
- [PASS] Normalized note-aware still abstains on both strengthened-name items: normalized note-aware strengthened-name routes at N=8 = `[('halu_19', 'utility_calibrated_abstain', 'absent'), ('halu_20', 'utility_calibrated_abstain', 'absent')]`.
- [PASS] Normalized unified false-present is non-worse than baseline: baseline/normalized unified false_present at N=8 = `0.500`/`0.500`.
- [PASS] Normalized summary-only realism stays at least as strong as baseline: baseline/normalized summary_only N=8 accuracy = `0.333`/`0.333`.
- [PASS] Normalized note-aware residual contamination stays zero at high N: normalized note-aware residual at N=8 = `0.000`.

## Bottom Line

如果这些检查通过，说明 broad literal integration 这一步是稳定的 executor cleanup，而不是新的 latent-claim patch：它保留 mixed code+name literal slice 的 signal / abstain story，不额外制造 unified 侧回退，同时把 strengthened aligned-name cases 的 final note 全部归一成 detector-readable scaffold。
