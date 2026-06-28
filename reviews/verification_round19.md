# Verification Round 19

这个文件是对 actual hallucination intermediate-contract round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `288`, observed `288`.
- [PASS] Strong-anchor branch is consistent with the previous robustness round at N=4: previous/current strong unified N=4 tentative_target_claim = `0.938`/`0.938`.
- [PASS] Strong-anchor branch is consistent with the previous robustness round at N=8: previous/current strong unified N=8 tentative_target_claim = `0.938`/`0.938`.
- [PASS] Selective anchor improves summary-only realism over strong anchor at N=4 or N=8: summary_only strong/selective accuracy at N=4 = `0.062`/`0.500`, at N=8 = `0.062`/`0.438`.
- [PASS] Selective anchor keeps more clue survival than soft anchor at N=4 or N=8: selective/soft unified tentative_target_claim at N=4 = `0.375`/`0.125`, at N=8 = `0.375`/`0.125`.
- [PASS] Selective anchor remains weaker than strong anchor on clue survival: strong/selective unified tentative_target_claim at N=4 = `0.938`/`0.375`, at N=8 = `0.938`/`0.375`.
- [PASS] Selective anchor still leaves detector work at at least one high-N setting: selective unified false_present at N=4/N=8 = `0.188`/`0.062`.
- [PASS] Selective note-aware reduces false-present relative to selective unified at at least one high-N setting: selective unified/note-aware false_present at N=4 = `0.188`/`0.000`, at N=8 = `0.062`/`0.000`.
- [PASS] Selective note-aware keeps zero residual contamination at N=8: selective note-aware N=8 residual = `0.000`.

## Bottom Line

如果这些检查通过，说明 round 19 已经把 realism frontier 往前推了一步：selective_anchor 不再像 strong_anchor 那样极端，但也没有像 soft_anchor 那样完全失去 clue survival。
