# Review Round 24

## What Improved

1. 这一步真的把 name-only branch 从“可测但混杂”推进成了“结构上更干净的 split”。在 focused 6-item pilot、`N=8`、unified 条件下，`refined_name_literal_anchor` 把 weak anti-role pair `halu_17/18` 的 detector-visible signal 从 baseline name branch 的 `1/2` 压到 `0/2`，同时把 strengthened aligned-name pair `halu_19/20` 的 tentative clue survival 从 `1/2` 提高到 `2/2`。这说明新 scaffold 不只是继续依赖 raw recovery，而是真的把 strong name branch 往 compact-stable clue 推进了一步。
2. 这轮的 prompt tightening 也显著改善了 summary-only realism。`summary_only` 的 `N=8 accuracy` 从 baseline `name_literal_anchor` 的 `0.500` 提高到 `refined_name_literal_anchor` 的 `0.667`，而且 `tentative_guess_note_rate` 从 `0.333` 降到 `0.000`。这意味着 role-mismatched names 不再被轻易写成“也许就是答案”的 loose note，而是更稳定地被压回 `MISSING`。
3. refined branch 没有牺牲原有的 blocking discipline。它在 code items `halu_15/16` 上仍然保持 `0/2` signal，同时在 strengthened aligned-name items 上保留 `2/2` signal 和 `2/2` raw recovery。也就是说，新的 gain 不是来自把 bucket 放大，而是来自把 name bucket 内部做得更 role-sensitive。

## Main Weaknesses

### W1. detector-side false_present 没有继续下降

这一轮最大的限制是：虽然 compactor 变得更好，但 detector 侧的 aggregate frontier 没再往前走。`refined_name_literal_anchor` 在 `scale_aware_unified` 和 `scale_aware_note_aware` 下的 `N=8 false_present` 都还是 `0.333`，与 baseline `name_literal_anchor` 持平。说明这一步主要改善了 “哪些 clue 该留下” 与 “留下时长什么样”，但还没有改变 detector 对 aligned-name surrogate 的 recover decision。

### W2. aligned-name carry-forward 仍然会在个别 item 上漂成非 scaffold prose

`halu_19` 已经稳定回到标准三行 scaffold，但 `halu_20` 的最终 note 仍会在高 `N` pass 漂成 “No new source material in this pass; preserving prior state unchanged.” 这种 prose，同时保留了正确的 tentative query-field claim。换句话说，role-alignment rule 已经够强去保住 clue，但还不够强去保证每一轮最终 note 都留在严格的 slot-based form 里。

### W3. 当前前沿问题已经从 name split 转成 executor / normalization consistency

这一轮最有价值的结论其实是路由变化：我们不再主要缺 “更好的 name item” 或 “更细的数据拆分”，而是缺一个更稳定的 carry-forward / normalization contract，让 aligned tentative clue 在 repeated compression 下持续输出同一种可解析 scaffold。现在 compactor 已经能把 weak anti-role names 清掉、把 strong aligned names保住；接下来卡住 detector gain 的，是 final note 形式和 recover threshold 的一致性，而不是 name branch 本身不存在。

## Bottom Line

这一轮是成功的，而且成功得很具体。`refined_name_literal_anchor` 已经把 name-only branch 做成了更干净的 mechanism split：weak anti-role names 被稳定压回 `MISSING`，strong aligned names 变成 `2/2` tentative + `2/2` raw signal，summary-only realism 也明显改善。下一步最值得做的不是继续扩 name 数据，而是补一个 aligned-name carry-forward normalization：确保像 `halu_20` 这样的 item 在最后一跳也输出标准 `target_slot/status_slot/carry_slot` scaffold，再看 note-aware 的 `N=8 false_present` 能不能从 `0.333` 再往下压。
