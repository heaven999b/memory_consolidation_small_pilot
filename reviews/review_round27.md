# Review Round 27

## What Improved

1. 这一步不只是把 broad literal 的 note 写规范，而是真的把 strongest aligned-name pressure 变成了 explicit tentative query claim。`claim_normalized_literal_identity_anchor` 在 mixed 6-item literal slice、`N=8`、`scale_aware_unified` 条件下，把 strengthened-name pair 从 `2/2 signal, 0/2 tentative, 2/2 raw, 2/2 scaffold` 提升到 `2/2 signal, 2/2 tentative, 2/2 raw, 2/2 scaffold`。这是第一次在 broad literal branch 上，把 raw-only recoverable clue 明确推进成了 canonical tentative target claim。
2. 这个 claim surfacing 没有带来 aggregate regression。`scale_aware_unified N=8 false_present` 仍然是 `0.500`，`scale_aware_note_aware N=8 false_present` 仍然是 `0.000`，`summary_only N=8 accuracy` 仍然是 `0.333`。同时 code-overlap 和 weak-name pair 的 unified signal 也完全不变，分别保持 `1` 和 `0`。这说明这一步不是把 literal branch 整体放宽，而是对 role-aligned name-literal frontier 做了受控定点增强。
3. 这一轮还给了我们一个更强的 mechanistic 结论。之前 broad literal 已经能 canonicalize final note，但 `tentative_target_claim` 一直是 `0/2`；现在只靠 executor-side claim rewrite，就能把它补成 `2/2`，而 unified route 仍然保持 `compact_answer=ABSTAIN`、`raw_escalated=true`，note-aware route 仍然保持 `utility_calibrated_abstain`。换句话说，cleanup policy 本身没变，变的是 latent representation 的可解释性和可测性。

## Main Weaknesses

### W1. 这还是一个 focused 6-item、single-seed result，不是 broader actual stress verdict

虽然这轮的 localized win 比上一轮更硬，但它仍然只发生在固定 mixed code+name literal slice 上。我们还没有把 `claim_normalized_literal_identity_anchor` 带回更宽的 identity/literal frontier，也还没有在多 seed 或更大 actual hallucination stress slice 上验证它。

### W2. aggregate false-present 仍然没动，说明局部 representation win 还没被证明能改变更大 story

这一步把 strongest aligned-name cases 的 representation 做对了，但 mixed-slice top-line `false_present` 指标没有变化。这个结果本身是有价值的，因为它说明局部 representation fix 可以不伤 aggregate；但还不能说明它会在更大 identity family 或更宽 hallucination slice 上变成可见的 overall gain。

### W3. broad literal 和 refined name-only 之间现在存在两条“好分支”，还没做统一比较

当前我们有两个都表现不错的局部前沿：`normalized_refined_name_literal_anchor` 代表 focused name-only best case，`claim_normalized_literal_identity_anchor` 代表 broad literal best case。下一步需要把 broad claim-sensitive 版本带回更外层 pilot，看它到底只是更自然的 literal branch，还是已经足够替代更窄的 refined name-only branch。

## Bottom Line

这一轮是一个真正的 frontier push。`claim_normalized_literal_identity_anchor` 证明 broad literal branch 不仅能把 aligned-name note 写成 canonical scaffold，还能把 strongest aligned-name pressure 显式表达成 tentative query claim，同时保持 code/weak-name 非回退、unified/non-note-aware false-present 非回退、note-aware `N=8 false_present = 0.000` 不变。下一步最值得做的不是继续在这 6 条上打磨，而是把这个 claim-sensitive broad literal branch 带回更宽的 identity/literal pilot，看它能不能在更外层 slice 上也保持这种“局部更强、整体不坏”的性质。
