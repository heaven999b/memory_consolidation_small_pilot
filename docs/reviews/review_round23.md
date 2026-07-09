# Review Round 23

## What Improved

1. 这一步的补强是有效的，而且方向是对的。focused literal-subsplit pilot 在 6 条 literal-overlap hallucination item、1 个 seed 上显示：强化后的 name-overlap item `halu_19/20` 确实比旧的弱 pair 更容易形成 detector-visible work。最直接的证据不是 `tentative_target_claim` 条数本身，而是 unified `N=8` 下的 per-item signal：在 `name_literal_anchor` 里，weak-name pair 只有 `1/2` 条 item 触发任意 signal，而 strengthened-name pair 是 `2/2`；在 broad `literal_identity_anchor` 里，weak-name pair 是 `0/2`，strengthened-name pair 则变成 `2/2`，而且主要体现为 raw recovery。
2. `code_literal_anchor` 已经成为一个更干净的 mechanistic split，而不只是 broad literal 的子标签。统一后的 `N=8 false_present` 从 broad literal 的 `0.500` 降到 code-only 的 `0.167`，`summary_only` 的 `N=8` accuracy 也从 typed 的 `0.167` 提高到 `0.667`。更重要的是 per-item 行为非常干净：code branch 在 `halu_15/16` 上有 `2/2` detector-visible signal，而在全部四条 name item 上是 `0/4`。
3. broad literal 的 detector suppression 也更可信了。虽然 `literal_identity_anchor` 在 unified `N=8` 的 `false_present` 仍然是 `0.500`，但 `scale_aware_note_aware` 已经把它压到 `0.000`，而且 residual contamination 仍是 `0.000`。这说明强化后的 literal slice 不只是“更容易 hallucinate”，而是继续保住了可被 detector 治理的结构。

## Main Weaknesses

### W1. strengthened name-overlap 的增益主要体现在 raw recovery，而不是 compact-claim survival

这一步最重要的 nuance 是：`halu_19/20` 的增益并不主要体现为 `tentative_target_claim_rate` 上升。broad literal 在 unified `N=8` 下对 strengthened-name pair 的表现是 `tent=0/2, raw=2/2`；`name_literal_anchor` 则是 `tent=1/2, raw=2/2`。这说明我们确实把 name branch 做得更可测了，但当前 signal 更像“recoverable detector work”，还不是一个稳定的 compact-memory clue family。

### W2. name-only branch 现在可测，但还不够干净

`name_literal_anchor` 的 unified `N=8 false_present` 是 `0.333`，而 note-aware 之后还是 `0.333`，说明它不像 code-only 或 broad literal 那样已经出现明显 detector gain。per-item 上看，这个 branch 同时保留了强化后的好信号 (`halu_19/20`) 和一个较弱旧样本里的错误 tentative (`halu_18 -> Evan Scott`)。也就是说，当前的 name-only branch 已经不是空分支，但它还是把 “role-adjacent name reuse” 和 “wrong nearby person-name” 混在一起。

### W3. scaffold consistency 还是 name branch 的前沿问题

几条最有价值的 strengthened-name record 并没有稳定产出规范的 `target_slot:` note，而是出现了像 `sponsoring_employee: Morgan Lee` 这样的半结构化行，最后更多依赖 salvage / raw recovery 才把 signal 留下来。这不是致命 bug，因为 executor 最终仍然答对了，但它解释了为什么 strong-name gain 更容易出现在 `raw_escalated`，而不是 `tentative_target_claim` 指标里。

## Bottom Line

这一步已经把 literal frontier 往前推了一层。`code_literal_anchor` 现在是一个相当干净的 split；`name_literal_anchor` 也终于从 detector-light 变成了可测分支，而且强化后的 `halu_19/20` 明显比旧弱样本更容易触发 signal。下一步最值得做的不是继续盲目加 name item，而是专门收紧 name-only scaffold：让 role-aligned person-name overlap 更稳定地保留标准 query-slot note，再看 note-aware 能不能把 `N=8 false_present` 从 `0.333` 再往下压。
