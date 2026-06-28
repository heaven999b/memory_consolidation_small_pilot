# Verification Round 22

这个文件是对 actual hallucination identity-focus pilot 的机械核对，不引入新的主张。

- [PASS] Record count: expected `144`, observed `144`.
- [PASS] Focused pilot slice is the intended 6-item relation-plus-literal set: observed slice ids = `['halu_01', 'halu_12', 'halu_15', 'halu_16', 'halu_17', 'halu_18']`.
- [PASS] Typed note-aware removes the focused pilot's high-N false-present: typed unified/note-aware false_present at N=8 = `0.333`/`0.000`.
- [PASS] Identity note-aware removes the focused pilot's high-N false-present: identity unified/note-aware false_present at N=8 = `0.333`/`0.000`.
- [PASS] Relation branch keeps relation-style clues but blocks literal-overlap items: relation branch clue counts on relation/literal ids at N=8 = `1`/`0`.
- [PASS] Literal branch keeps literal-overlap clues but blocks relation-style items: literal branch clue counts on literal/relation ids at N=8 = `2`/`0`.
- [PASS] Literal note-aware removes the focused high-N code-overlap false-present: literal unified/note-aware false_present at N=8 = `0.167`/`0.000`.
- [PASS] Relation note-aware removes the focused high-N relation-style false-present: relation unified/note-aware false_present at N=8 = `0.167`/`0.000`.
- [PASS] Relation and literal summary-only contracts are both more realistic than typed at high N: typed/relation/literal summary_only N=8 accuracy = `0.167`/`0.667`/`0.667`.
- [PASS] Name-overlap literal items remain detector-light in this pilot: literal branch on `['halu_17', 'halu_18']` gives tent/raw = `[('halu_17', False, False), ('halu_18', False, False)]`.
- [PASS] All note-aware branches keep zero residual contamination at N=8: typed/identity/relation/literal note-aware residual at N=8 all equal `0.000`.

## Bottom Line

如果这些检查通过，说明 focused pilot 已经把 identity family 再往前拆开了一层：relation-style alias 和 literal-style overlap 都能形成可见 detector work，但目前 literal 里真正稳定的更像 code overlap，而不是 person-name overlap。
