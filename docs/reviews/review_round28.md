# Review Round 28

## What Improved

1. 这一步把 `claim_normalized_literal_identity_anchor` 从 6-item mixed literal slice 成功带回了更宽的 identity/literal frontier。新的 8-item bridge pilot 同时包含 relation、code-overlap、weak-name、strong-name 四类 item，结果显示 broad literal claim surfacing 在更宽 slice 上依然稳定：relation item 继续 `0/2 signal`，code item 继续 `1/2 signal`，weak-name pair 继续 `0/2 signal`，strengthened-name pair 继续从 `2/2 signal, 0/2 tentative, 2/2 raw, 2/2 scaffold` 升级到 `2/2 signal, 2/2 tentative, 2/2 raw, 2/2 scaffold`。
2. 这个 outward expansion 没有带来 aggregate regression。bridge slice 上 `scale_aware_unified N=8 false_present` 在 literal/normalized/claim 三个 broad literal 版本里都保持 `0.375`，`scale_aware_note_aware N=8 false_present` 则在三个 broad literal 版本里都保持 `0.000`。这说明 claim surfacing 不只是局部 representation win，而且在 relation+literal 更宽混合条件下仍然没有破坏 detector-side cleanup story。
3. 这轮还提供了一个更重要的结构性信号：此前最担心的是 relation item 一旦重新接回，broad literal 的 claim-sensitive rewrite 可能会误把 relation-style alias 也拉进 tentative query claim 通道。但 bridge pilot 明确显示这种回退没有发生。`halu_01/12` 在 claim-sensitive broad literal 下依然保持 `compact_answer=ABSTAIN`、`tentative_target_claim=false`、`raw_escalated=false`，说明我们当前的 claim rewrite 至少在这个 bridge slice 上是 role-aligned 且局部受控的。

## Main Weaknesses

### W1. 这仍然是 bridge pilot，不是 fully unified stress reintegration

这轮虽然比上一轮更外层，但它仍然是一个 stitching-style pilot：relation item 复用 relation frontier cache，literal item 复用 literal frontier cache，而不是重新训练一套统一 prompt contract。这个设计适合快速检验“claim surfacing 一旦接回 relation item 会不会立刻回退”，但还不足以当作更广泛 actual stress 结论。

### W2. single-seed + focused slice 的限制还在

目前 bridge pilot 还是单 seed、8 item、focused expansion。它已经足够说明局部 win 可以 survive 一个更宽 identity/literal slice，但还不能说明它会在更大 actual hallucination stress slice 或 multi-seed 条件下继续稳定。

### W3. aggregate false-present 没有变好，说明下一步要测的是 transfer，不是再做局部 polishing

这轮最重要的不是 top-line metric 继续下降，而是“更外层 slice 上不回退”。既然这一点已经得到支持，下一步就不该继续在 bridge slice 上打磨局部表示，而该把 `claim_normalized_literal_identity_anchor` 带回更接近真实的 actual hallucination stress frontier，看 representation gain 是否会在更宽 slice 上产生新的 detector-visible difference。

## Bottom Line

这一轮把 broad literal claim surfacing 从局部 literal win 推进成了更宽 identity/literal frontier 上的非回退结果。`claim_normalized_literal_identity_anchor` 现在已经在 8-item bridge slice 上证明：它能保住 relation/code/weak-name blocking，不恶化 unified 或 note-aware false-present，同时继续把 strengthened aligned-name case 提升成 explicit tentative target claim。下一步最值得做的是从 bridge pilot 再往外推一层，把这条 branch 带回更宽的 actual hallucination stress slice 或更大 multi-seed reintegration，验证这个 representation win 是否能从 focused bridge 变成 broader stress result。
