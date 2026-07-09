# Verification Round 18

这个文件是对 actual hallucination robustness round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `192`, observed `192`.
- [PASS] Strong-anchor seed11 keeps at least as much unified N=4 tentative-clue persistence as the old persistence round: old/new seed11 unified N=4 tentative_target_claim = `0.875`/`0.875`.
- [PASS] Strong-anchor aggregate note-aware false-present stays below unified at N=4: strong unified/note-aware N=4 false_present = `0.312`/`0.000`.
- [PASS] Strong-anchor aggregate note-aware false-present is no worse than unified at N=8: strong unified/note-aware N=8 false_present = `0.188`/`0.000`.
- [PASS] Strong-anchor detector gain appears on at least one high-N setting: N=4 unified/note-aware false_present = `0.312`/`0.000`, N=8 = `0.188`/`0.000`.
- [PASS] Strong anchor preserves more high-N tentative clues than soft anchor: strong/soft unified tentative_target_claim at N=4 = `0.938`/`0.125`, at N=8 = `0.938`/`0.125`.
- [PASS] Strong-anchor note-aware keeps zero residual contamination at N=8: seed11/all-seed strong note-aware N=8 residual = `0.000`/`0.000`.
- [PASS] Strong-anchor note-aware does not lose the false-present edge on any seed: per-seed strong note-aware<=unified at N=4 `[True, True]`, at N=8 `[True, True]`.

## Bottom Line

如果这些检查通过，说明 round 19 不只是重复 round 18，而是把 actual hallucination persistence 推进成了一个更像 robustness subsection 的结果：强 contract 的 detector gain 在多 seed 下依然成立，而 softer contract 会让 clue survival 变弱。
