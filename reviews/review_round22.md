# Review Round 22

## What Improved

1. 这一步终于把 identity family 再往前拆开了一层，而且不是空拆。focused pilot 在 6 条 expanded actual stress item、1 个 seed 上显示：`relation_identity_anchor` 和 `literal_identity_anchor` 都能在 `N=8` 留下可见 detector work，统一后的 `false_present` 都是 `0.167`，而 `scale_aware_note_aware` 都能把它压到 `0.000`。
2. relation 和 literal 的分流不是只体现在 aggregate 上，而是体现在 per-item 行为上。relation branch 在 `halu_01` / `halu_12` 这组 relation-style case 上保留 clue、同时把 `halu_15` 到 `halu_18` 压回 `MISSING`；literal branch 则反过来，在 `halu_15` / `halu_16` 这组 code-overlap case 上保留 clue，同时把 relation items 压回 `MISSING`。
3. realism 也往前走了一步。在这个 focused slice 上，`summary_only` 的 `N=8` accuracy 从 `typed_selective_anchor` 的 `0.167` 提高到 relation/literal 两支各自的 `0.667`，说明把 identity bucket 再拆细之后，确实能更自然地保留局部 stress signal，而不是只能继续靠 typed midpoint 的大桶。

## Main Weaknesses

### W1. 当前 literal branch 的稳定 signal 主要来自 code overlap，不是 person-name overlap

`halu_15` 和 `halu_16` 在 literal branch 下都能留下高-`N` tentative clue，其中 `halu_16` 还会触发 unified raw recovery；但 `halu_17` 和 `halu_18` 这两个 person-name overlap case 在 literal branch 下都收敛成 `MISSING`。这说明 “literal identity” 目前不是一个均匀 family，更像是 code-like overlap 先跑出来了，而人名重叠还不够强。

### W2. 这还是 focused pilot，不是 expanded full round

当前结果只覆盖 6 条 item 和 1 个 seed，已经足够回答“值不值得继续拆”这个问题，但还不足以当成稳健性结论。下一步不该立刻扩大结论，而应该先把 literal branch 再细分成 code overlap 与 person-name overlap，或者补更强的人名重叠 item，再决定是否跑完整 expanded micro-split。

## Bottom Line

这一步是有研究价值的，不只是数据补丁。expanded literal items 证明了：identity branch 里确实同时存在 relation-style 和 literal-style 两种 detector fuel，而且两者都能在高 `N` 留下可被 note-aware 抑制的 signal。但当前 literal signal 主要是 code overlap，不是 name overlap。下一步最值得做的是把 literal family 继续拆成 `code-like` vs `person-name`，而不是立刻把这一步当成最终 expanded 结论。
