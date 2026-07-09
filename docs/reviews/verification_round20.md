# Verification Round 20

这个文件是对 actual hallucination typed-selective round 的机械核对，不引入新的主张。

- [PASS] Record count: expected `384`, observed `384`.
- [PASS] Strong-anchor branch is consistent with the previous robustness round at N=4: previous/current strong unified N=4 tentative_target_claim = `0.938`/`0.938`.
- [PASS] Strong-anchor branch is consistent with the previous robustness round at N=8: previous/current strong unified N=8 tentative_target_claim = `0.938`/`0.938`.
- [PASS] Selective-anchor baseline remains consistent with the previous intermediate round at N=4: previous/current selective unified N=4 false_present = `0.188`/`0.188`.
- [PASS] Selective-anchor baseline remains consistent with the previous intermediate round at N=8: previous/current selective summary_only N=8 accuracy = `0.438`/`0.438`, unified false_present = `0.062`/`0.062`, note-aware false_present = `0.000`/`0.000`.
- [PASS] Typed selective improves high-N summary-only realism over the prior selective anchor: selective/typed summary_only N=8 accuracy = `0.438`/`0.562`.
- [PASS] Typed selective improves high-N cleanup accuracy over the prior selective anchor: selective/typed unified N=8 accuracy = `0.938`/`1.000`, note-aware = `0.938`/`1.000`.
- [PASS] Typed selective keeps more clue survival than soft anchor: typed/soft unified tentative_target_claim at N=4 = `0.312`/`0.125`, at N=8 = `0.375`/`0.125`.
- [PASS] Typed selective does not increase false-present relative to the prior selective anchor: selective/typed unified false_present at N=4 = `0.188`/`0.188`, at N=8 = `0.062`/`0.062`.
- [PASS] Typed note-aware reduces false-present relative to typed unified at at least one high-N setting: typed unified/note-aware false_present at N=4 = `0.188`/`0.000`, at N=8 = `0.062`/`0.000`.
- [PASS] Typed selective fixes the halu_05 high-N over-refusal in both cleanup architectures: typed halu_05 N=8 unified answers = ['ABSTAIN', 'ABSTAIN'], note-aware answers = ['ABSTAIN', 'ABSTAIN'].
- [PASS] Typed note-aware keeps zero residual contamination at N=8: typed note-aware N=8 residual = `0.000`.

## Bottom Line

如果这些检查通过，说明 round 20 不只是重复 selective baseline，而是把中间 contract 进一步 typed 化：保住部分 surrogate clue 的同时，修掉 policy-window 型高-N over-refusal。
