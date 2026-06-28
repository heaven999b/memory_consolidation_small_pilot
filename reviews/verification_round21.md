# Verification Round 21

这个文件是对 actual hallucination surrogate-split round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `480`, observed `480`.
- [PASS] Strong-anchor branch is consistent with the previous typed-selective round at N=4: previous/current strong unified N=4 tentative_target_claim = `0.938`/`0.938`.
- [PASS] Strong-anchor branch is consistent with the previous typed-selective round at N=8: previous/current strong unified N=8 tentative_target_claim = `0.938`/`0.938`.
- [PASS] Typed-selective baseline remains consistent with the previous typed round at N=8: previous/current typed summary_only N=8 accuracy = `0.562`/`0.562`, unified false_present = `0.062`/`0.062`, note-aware false_present = `0.000`/`0.000`.
- [PASS] Identity split keeps more high-N clue survival than the preference split: identity/preference unified tentative_target_claim at N=8 = `0.250`/`0.125`.
- [PASS] Identity split keeps more high-N clue survival than soft anchor: identity/soft unified tentative_target_claim at N=8 = `0.250`/`0.125`.
- [PASS] Identity split still leaves detector work at high N: identity unified false_present at N=8 = `0.062`.
- [PASS] Identity note-aware reduces false-present relative to identity unified at high N: identity unified/note-aware false_present at N=8 = `0.062`/`0.000`.
- [PASS] Preference split removes high-N detector work: preference unified/note-aware false_present at N=8 = `0.000`/`0.000`.
- [PASS] Preference split buys more high-N summary-only realism than the identity split: identity/preference summary_only N=8 accuracy = `0.625`/`0.812`.
- [PASS] Both split variants keep the halu_05 high-N fix in cleanup architectures: identity unified/note-aware halu_05 answers = ['ABSTAIN', 'ABSTAIN']/['ABSTAIN', 'ABSTAIN']; preference unified/note-aware = ['ABSTAIN', 'ABSTAIN']/['ABSTAIN', 'ABSTAIN'].
- [PASS] Identity and preference note-aware branches keep zero residual contamination at N=8: identity/preference note-aware residual at N=8 = `0.000`/`0.000`.

## Bottom Line

如果这些检查通过，说明 round 21 已经把 typed midpoint 再往前拆开了一层：高-N detector signal 主要由 identity-like surrogate 支撑，而 preference-style surrogate 更像 realism-friendly 但 detector-light 的分支。
