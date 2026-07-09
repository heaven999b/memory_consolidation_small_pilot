# Verification Round 23

这个文件是对 actual hallucination literal-subsplit pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `144`, observed `144`.
- [PASS] Focused pilot slice is the intended 6-item literal subsplit set: observed slice ids = `['halu_15', 'halu_16', 'halu_17', 'halu_18', 'halu_19', 'halu_20']`.
- [PASS] Typed note-aware removes the high-N false-present on the strengthened literal slice: typed unified/note-aware false_present at N=8 = `0.500`/`0.333`.
- [PASS] Broad literal note-aware removes the high-N false-present on the strengthened literal slice: literal unified/note-aware false_present at N=8 = `0.500`/`0.000`.
- [PASS] Code-only branch keeps code-like overlap clues but blocks name-overlap items: code branch signal counts on code/name ids at N=8 = `2`/`0`.
- [PASS] Name-only branch blocks code-like overlap items: name branch signal count on code ids at N=8 = `0`.
- [PASS] Strengthened name-overlap items create more detector-visible work than the weak name pair under the name-only branch: name branch signal counts on weak/strengthened name ids at N=8 = `1`/`2`.
- [PASS] Broad literal branch benefits from the strengthened name-overlap items via raw recovery: literal branch signal counts on weak/strengthened name ids at N=8 = `0`/`2`.
- [PASS] Name-only branch produces real detector-visible work on the strengthened name items: name branch strengthened-name signal/tent/raw at N=8 = `2`/`1`/`2`.
- [PASS] Code note-aware improves over unified, and name note-aware stays non-worse at high N: code unified/note-aware false_present at N=8 = `0.167`/`0.000`; name unified/note-aware = `0.333`/`0.333`.
- [PASS] All note-aware branches keep zero residual contamination at N=8: typed/literal/code/name note-aware residual at N=8 all equal `0.000`.

## Bottom Line

如果这些检查通过，说明这一轮补强不是只把 literal family 变大，而是真的把其中的人名子支路做得更可测：强化后的 name-overlap item 比旧弱样本更容易触发 detector-visible work，而且这个增益主要体现在 raw recovery / recoverable signal，而不只是 tentative target claim 的条数上。
