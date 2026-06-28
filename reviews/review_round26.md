# Review Round 26

## What Improved

1. 这一步把上一轮只在 focused name-only branch 成立的 executor-side normalization，成功合回了 broad `literal_identity_anchor`。在 mixed 6-item literal slice 上，strengthened aligned-name pair 的 final note scaffold 稳定性从 `1/2` 提升到 `2/2`，而且 `halu_19/20` 在 `summary_only`、`scale_aware_unified`、`scale_aware_note_aware` 三个架构下都统一收敛成 canonical 三行 scaffold。
2. 这次 integration 没有引入新的行为回退。broad literal 的 `summary_only N=8 accuracy` 保持 `0.333`，`scale_aware_unified N=8 false_present` 保持 `0.500`，`scale_aware_note_aware N=8 false_present` 也继续保持 `0.000`。换句话说，我们把 strongest aligned-name literal case 变得更可读了，但没有额外制造新的 detector pressure 或 realism regression。
3. 这一轮最大的研究价值是把 broad literal 的 remaining weakness 定位得更清楚了。现在已经不是“final note detector 看不懂 aligned-name carry-forward”这个问题了，因为 broad literal 在 note 层面已经被归一干净；真正没变的是 latent claim 结构本身。strengthened-name pair 依然是 `2/2 raw recovery`、`0/2 tentative_target_claim`，说明 broad literal 的 surviving pressure 仍主要以 raw-recoverable clue 而不是 canonical tentative claim 的形式存在。

## Main Weaknesses

### W1. broad literal 的 aggregate 指标没有继续下降，说明这不是 detector-readability frontier

这一步最重要但也最克制的结果是：aggregate metrics 完全不动。broad literal 的 note-aware `N=8 false_present` 之前就是 `0.000`，现在仍然是 `0.000`；unified `N=8 false_present` 之前是 `0.500`，现在仍然是 `0.500`。这说明我们已经把 broad literal 的 detector-readable cleanup 做到位了，但它不是下一段增益曲线的主因。

### W2. strongest aligned-name cases 仍然没有进入 tentative-target-claim 通道

虽然 `halu_19/20` 的 final note 现在已经 canonical，但 broad literal branch 上它们依然是 `tent=0/2, raw=2/2`。这跟 focused refined-name branch 很不一样，后者已经能把同一类 pressure 变成显式 tentative query claim。也就是说，broad literal 的 remaining gap 不在最后一跳 note 形态，而在 compactor/executor 对 latent claim 的表示方式。

### W3. mixed literal branch 的下一轮不该再做 note-only cleanup，而该做 claim-sensitive follow-up

既然 note normalization 已经验证为“稳定但不产生新 aggregate gain”的 cleanup，下一轮就不值得继续堆更多 note-only patch。更值得测的是：能否只在 role-aligned literal case 上，把 broad literal 的 surviving aligned-name clue 安全地提升为 canonical tentative query claim，同时不把 weak-name pair 或 code-overlap case 也一并放大。

## Bottom Line

这一轮把 broad literal frontier 又推进了一格，但推进方式不是“指标继续下降”，而是“把 failure mode 切分得更干净”。`normalized_literal_identity_anchor` 证明：broad literal 的 aligned-name final note 现在已经可以 `2/2` scaffold-stable，同时 mixed-slice aggregate 完全不回退。下一步最值得做的不是再修 note，而是做一个 claim-sensitive literal follow-up，专门测试 broad literal 能不能在不恶化 unified `false_present` 的前提下，把 strongest aligned-name pressure 从 raw-only recovery 转成 canonical tentative target claim。
