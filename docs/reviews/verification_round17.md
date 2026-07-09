# Verification Round 17

这个文件是对 actual hallucination persistence round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `72`, observed `72`.
- [PASS] Stronger contract increases unified N=4 tentative clue persistence versus the old stress baseline: old/new unified N=4 tentative_guess_note = `0.000`/`1.000`.
- [PASS] Note-aware detector lowers false-present at N=4 under the stronger contract: new unified/note-aware N=4 false_present = `0.500`/`0.000`.
- [PASS] Stronger contract keeps tentative clue alive into at least one high-N setting: N=4/N=8 tentative_target_claim = `0.875`/`0.875`.
- [PASS] Note-aware detector keeps zero residual contamination at N=8: `scale_aware_note_aware` residual = `0.000`.
- [PASS] Note-aware detector does not underperform unified on accuracy at N=8: new note-aware/unified N=8 accuracy = `1.000`/`1.000`.

## Bottom Line

如果这些检查通过，说明 round 18 已经把 actual hallucination stress 从局部 N=1 detector transfer 推向了更持久的 contract-level clue persistence 检验。
