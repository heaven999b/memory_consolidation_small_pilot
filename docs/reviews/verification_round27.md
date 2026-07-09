# Verification Round 27

这个文件是对 actual hallucination literal-claim pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `216`, observed `216`.
- [PASS] Focused pilot slice is the intended 6-item mixed literal set: observed slice ids = `['halu_15', 'halu_16', 'halu_17', 'halu_18', 'halu_19', 'halu_20']`.
- [PASS] Claim-sensitive rewrite preserves code-overlap signal behavior: normalized/claim code signal at N=8 = `1`/`1`.
- [PASS] Claim-sensitive rewrite preserves weak-name blocking behavior: normalized/claim weak-name signal at N=8 = `0`/`0`.
- [PASS] Claim-sensitive rewrite keeps strengthened-name signal while surfacing tentative query claims: normalized/claim strengthened-name signal/tent/raw at N=8 = `2`/`0`/`2` vs `2`/`2`/`2`.
- [PASS] Claim-sensitive rewrite keeps both strengthened-name notes scaffold-stable: normalized/claim strengthened-name scaffold counts at N=8 = `2`/`2`.
- [PASS] Claim-sensitive unified branch still routes strengthened-name cases through cleanup rather than compact answers: claim unified strengthened-name compact/raw at N=8 = `[('halu_19', 'ABSTAIN', True), ('halu_20', 'ABSTAIN', True)]`.
- [PASS] Claim-sensitive note-aware still abstains on both strengthened-name items: claim note-aware strengthened-name routes at N=8 = `[('halu_19', 'utility_calibrated_abstain', 'absent'), ('halu_20', 'utility_calibrated_abstain', 'absent')]`.
- [PASS] Claim-sensitive note-aware false-present is non-worse than normalized baseline: normalized/claim note-aware false_present at N=8 = `0.000`/`0.000`.
- [PASS] Claim-sensitive unified false-present is non-worse than normalized baseline: normalized/claim unified false_present at N=8 = `0.500`/`0.500`.
- [PASS] Claim-sensitive summary-only realism stays at least as strong as normalized baseline: normalized/claim summary_only N=8 accuracy = `0.333`/`0.333`.
- [PASS] Claim-sensitive note-aware residual contamination stays zero at high N: claim note-aware residual at N=8 = `0.000`.

## Bottom Line

如果这些检查通过，说明 broad literal 的下一步 frontier 确实是 claim surfacing：我们可以把 strongest aligned-name pressure 从 raw-only recovery 提升成 explicit tentative query claim，同时不让 weak-name/code item 回退，也不让 note-aware 或 unified false-present 变差。
