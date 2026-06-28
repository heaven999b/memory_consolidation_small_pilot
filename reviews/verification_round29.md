# Verification Round 29

这个文件是对 actual hallucination claim-reintegration proxy pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `336`, observed `336`.
- [PASS] Reintegration slice is the intended 14-item stress-plus-literal set: observed slice ids = `['halu_01', 'halu_02', 'halu_03', 'halu_04', 'halu_05', 'halu_08', 'halu_12', 'halu_14', 'halu_15', 'halu_16', 'halu_17', 'halu_18', 'halu_19', 'halu_20']`.
- [PASS] Artifact is explicitly marked as a proxy-expanded stitch: observed mode = `proxy_expanded_stitch`.
- [PASS] Proxy rows are restricted to the intended non-literal stress items: observed proxy rows = `108`, proxy items = `['halu_02', 'halu_03', 'halu_04', 'halu_05', 'halu_08', 'halu_14']`.
- [PASS] Typed-equivalent proxy coverage matches the five must-copy or weak/policy items: typed-equivalent proxy rows = `90`.
- [PASS] Identity-equivalent proxy coverage matches the single preference-context item: identity-equivalent proxy rows = `18`.
- [PASS] Claim-sensitive literal branch still blocks relation-style items: literal/claim relation signal at N=8 = `0`/`0`.
- [PASS] Claim-sensitive literal branch preserves wider stress-context behavior under proxy expansion: literal/claim stress-context signal at N=8 = `1`/`1`.
- [PASS] Claim-sensitive literal branch preserves code-overlap behavior: literal/claim code signal at N=8 = `1`/`1`.
- [PASS] Claim-sensitive literal branch preserves weak-name blocking: literal/claim weak-name signal at N=8 = `0`/`0`.
- [PASS] Claim-sensitive literal branch surfaces strengthened-name tentative query claims: normalized/claim strengthened-name signal/tent/raw at N=8 = `2`/`0`/`2` vs `2`/`2`/`2`.
- [PASS] Claim-sensitive literal branch keeps strengthened-name notes scaffold-stable: claim strengthened-name scaffold count at N=8 = `2`.
- [PASS] Claim-sensitive unified false-present is non-worse than normalized literal baseline: normalized/claim unified false_present at N=8 = `0.214`/`0.214`.
- [PASS] Claim-sensitive note-aware false-present is non-worse than normalized literal baseline: normalized/claim note-aware false_present at N=8 = `0.000`/`0.000`.
- [PASS] Claim-sensitive note-aware still abstains on both strengthened-name items: claim note-aware strengthened-name routes at N=8 = `[('halu_19', 'utility_calibrated_abstain', 'absent'), ('halu_20', 'utility_calibrated_abstain', 'absent')]`.
- [PASS] Claim-sensitive summary-only realism stays at least as strong as normalized literal baseline: normalized/claim summary_only N=8 accuracy = `0.643`/`0.643`.
- [PASS] Claim-sensitive note-aware residual contamination stays zero at high N: claim note-aware residual at N=8 = `0.000`.

## Bottom Line

如果这些检查通过，说明这次 proxy-expanded reintegration 至少没有暴露出更宽 mixed slice 上的立即回退。它不能替代未来的 exact literal-identity live rerun，但已经足够把 claim-sensitive broad literal branch 从 8-item bridge 再往外推一层，同时把 proxy 假设本身写清楚并机械锁住。
