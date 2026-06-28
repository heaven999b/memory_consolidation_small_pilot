# Review Round 25

## What Improved

1. 这一步真正补到了上一轮的空白，而且补得非常干净。`normalized_refined_name_literal_anchor` 不改 compactor 语义，只在 executor 侧把 aligned tentative claim 归一成标准三行 scaffold，并显式补上 inference marker。结果是在 focused 6-item pilot、`N=8`、note-aware 条件下，`false_present` 从 `refined_name_literal_anchor` 的 `0.333` 直接降到 `0.000`，而 unified 侧保持 `0.333` 不变。也就是说，我们第一次明确看到：问题不在“有没有正确 clue”，而在“最后一跳 note 形态是否足够稳定到让 detector 读懂它”。
2. strongest aligned-name cases 现在已经同时满足了三件事：`2/2` signal、`2/2` tentative clue survival、`2/2` scaffold-stable final note。上一轮 `refined_name_literal_anchor` 在 strengthened-name pair 上虽然已经做到 `2/2` signal 和 `2/2` raw recovery，但 scaffold-stable 只有 `1/2`；这一轮把它补成了 `2/2`，并且 `halu_19/20` 在 note-aware 下都从 `utility_calibrated_recover` 变成 `utility_calibrated_abstain`。
3. 这一步没有引入代价型回退。`summary_only` 的 `N=8 accuracy` 仍然保持在 `0.667`，不比 refined 版本差；weak anti-role pair 和 code items 也继续保持 `0` signal。换句话说，这不是“为了 detector gain 牺牲 realism”，而是把已有的 refined compactor 结果变得更可解析、更可治理。

## Main Weaknesses

### W1. unified-side pressure 还在，只是 note-aware 终于读懂了它

这一轮最值得注意的限制是：unified `N=8 false_present` 仍然是 `0.333`，没有下降。说明 aligned-name normalization 解决的是 detector-readability，而不是 latent pressure 本身。换句话说，我们现在知道 strongest aligned-name cases 可以被 note-aware 干净挡住，但 broad unified literal branch 里那部分 unsupported target guess 仍然存在。

### W2. 这还是 focused single-seed result，不是 broader literal claim

当前 improvement 是在固定 6 条 item、1 个 seed、复用上一轮 compactor cache 的条件下得到的。它足够回答“executor-side normalization 是否有研究价值”，但还不足以直接当成更大 literal branch 或 expanded identity split 的最终结论。下一步必须把这个 normalization 合回更宽的 literal branch，再看 code+name 混合 slice 上的 aggregate story 是否也跟着变好。

### W3. broad literal branch 还没有继承这次 normalization

目前 `literal_identity_anchor` 在 focused literal-subsplit 里仍然是旧 executor 行为，所以它的 story 还是 “note-aware false_present = 0.000，但 stronger name gain 更多表现为 raw recovery”。现在我们已经知道如何把 aligned-name final note 归一化，所以下一阶段的关键不是继续打磨 name-only branch，而是把这套 normalization 合进 broad literal branch，重新测 code+name 共存时的 detector behavior。

## Bottom Line

这一轮把前一轮的 frontier 真正推过去了。`aligned-name carry-forward normalization` 已经证明：只靠 executor-side scaffold rewriting，就能在不改变 unified latent pressure 的前提下，把 focused name branch 的 note-aware `N=8 false_present` 从 `0.333` 降到 `0.000`。下一步最值得做的不是继续深挖 name-only，而是把这套 normalization 回灌进 broad literal branch，然后重跑 literal subsplit，检查 code+name 混合 slice 的 aggregate literal story 是否也随之升级。
