# Verification Round 28

这个文件是对 actual hallucination identity-claim bridge pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `192`, observed `192`.
- [PASS] Bridge pilot slice is the intended 8-item relation-plus-literal set: observed slice ids = `['halu_01', 'halu_12', 'halu_15', 'halu_16', 'halu_17', 'halu_18', 'halu_19', 'halu_20']`.
- [PASS] Claim-sensitive literal branch still blocks relation-style items: literal/claim relation signal at N=8 = `0`/`0`.
- [PASS] Claim-sensitive literal branch preserves code-overlap behavior: literal/claim code signal at N=8 = `1`/`1`.
- [PASS] Claim-sensitive literal branch preserves weak-name blocking: literal/claim weak-name signal at N=8 = `0`/`0`.
- [PASS] Claim-sensitive literal branch surfaces strengthened-name tentative query claims: normalized/claim strengthened-name signal/tent/raw at N=8 = `2`/`0`/`2` vs `2`/`2`/`2`.
- [PASS] Claim-sensitive literal branch keeps strengthened-name notes scaffold-stable: claim strengthened-name scaffold count at N=8 = `2`.
- [PASS] Claim-sensitive unified false-present is non-worse than normalized literal baseline: normalized/claim unified false_present at N=8 = `0.375`/`0.375`.
- [PASS] Claim-sensitive note-aware false-present is non-worse than normalized literal baseline: normalized/claim note-aware false_present at N=8 = `0.000`/`0.000`.
- [PASS] Claim-sensitive note-aware still abstains on both strengthened-name items: claim note-aware strengthened-name routes at N=8 = `[('halu_19', 'utility_calibrated_abstain', 'absent'), ('halu_20', 'utility_calibrated_abstain', 'absent')]`.
- [PASS] Claim-sensitive summary-only realism stays at least as strong as normalized literal baseline: normalized/claim summary_only N=8 accuracy = `0.500`/`0.500`.
- [PASS] Claim-sensitive note-aware residual contamination stays zero at high N: claim note-aware residual at N=8 = `0.000`.

## Bottom Line

如果这些检查通过，说明 claim-sensitive broad literal branch 不只是 6-item mixed literal slice 的局部巧合。即使把 relation item 重新接回来，它也仍然能保持 relation/code/weak-name 非回退，同时把 strengthened aligned-name case 提升成 explicit tentative target claim。
