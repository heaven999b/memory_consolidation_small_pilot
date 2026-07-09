# Verification Round 15

这个文件是对 actual placeholder hardening round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `144`, observed `144`.
- [PASS] Hardened parser improves unified N=8 overall accuracy: refined/hardened unified accuracy = `0.833`/`0.917`.
- [PASS] Hardened parser eliminates unified N=8 hallucination placeholder answers: refined/hardened hallucination_placeholder = `0.500`/`0.000`.
- [PASS] Hardened parser preserves unified N=8 unsafe error: refined/hardened unsafe_error = `0.500`/`0.500`.
- [PASS] Hardened parser preserves unified N=8 target retention: refined/hardened target_claim = `0.375`/`0.375`.
- [PASS] Hardened parser improves summary-only N=8 accuracy: refined/hardened summary accuracy = `0.417`/`0.500`.

## Bottom Line

如果这些检查通过，说明 round 16 已经把 refined scaffold 的 frontier 从 placeholder leakage 向更稳定的 reusable parser contract 推进了一步。
