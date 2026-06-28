# Review Round 29

## What Improved

1. 这一步把 claim-sensitive broad literal branch 从 8-item bridge 再往外扩成了一个 14-item mixed stress+literal reintegration。新的 proxy-expanded artifact 一次性覆盖 `halu_01/02/03/04/05/08/12/14/15/16/17/18/19/20`，总计 `336` 条记录，并且把所有 proxy 假设都写进了 payload 和 verification，而不是把 stitched 扩张伪装成新的 exact live run。
2. 更宽 slice 上的 aggregate 结果依然干净。`scale_aware_unified N=8 false_present` 从 typed baseline 的 `0.286` 压到 broad literal 三个版本统一的 `0.214`，`scale_aware_note_aware N=8 false_present` 则从 typed 的 `0.143` 压到 literal/normalized/claim 三个版本统一的 `0.000`。这说明把 bridge 再往外推一层之后，claim-sensitive broad literal branch 仍然没有破坏 cleanup story。
3. 最关键的局部表示信号也保住了。更宽 14-item slice 上，relation item 继续 `0/2 signal`，stress-context item 保持 `1/6 signal` 且 claim 与 literal 完全一致，code item 继续 `1/2 signal`，weak-name pair 继续 `0/2 signal`，strengthened-name pair 则继续从 normalized 的 `2/2 signal, 0/2 tentative, 2/2 raw, 2/2 scaffold` 升级到 claim 的 `2/2 signal, 2/2 tentative, 2/2 raw, 2/2 scaffold`。也就是说，扩张之后新增的是 coverage，而不是新的 regression。
4. 这轮还给了一个更容易累积的 top-line。此前 bridge slice 上 `summary_only N=8` 只有 `0.500` realism，而这次 wider mixed slice 上 broad literal 三个版本都达到 `0.643`。这不说明方法突然“更强”了，而是说明在更宽 slice 上我们没有因为 reintegration 本身把 realism 拖垮。

## Main Weaknesses

### W1. 这还是 proxy-expanded reintegration，不是 exact literal-identity stress rerun

这轮最重要的诚实限制是：`108/336` 条记录来自 mode-equivalent proxy，而不是 fresh literal-identity compaction。`halu_02/04/05/08/14` 用 typed row 代理，`halu_03` 用 identity-selective row 代理，理由在 contract 语义上是合理的，但它仍然不等于真正跑过一遍 exact literal-identity prompt。

### W2. single-seed 限制依然存在

虽然 item 数已经从 8 扩到 14，但当前还是 `seed=11`。因此这轮更适合被解读为“bridge win 往外再推一层依然不回退”，而不是“已经得到稳定多 seed stress 结论”。

### W3. stress-context 里仍然残留一个可见 clue，说明 exact realism 扩张还没走到头

更宽 slice 上 broad literal 在 stress-context item 仍有 `1/6 signal`。这不构成新的 regression，因为 claim 与 literal 完全一致，但也提醒我们：下一步如果要做 exact live rerun，应该优先盯住这 6 个 non-literal stress item，确认 proxy 下的稳定性不会在真 literal-identity run 里被打破。

## Bottom Line

这一轮把 claim-sensitive broad literal branch 从 8-item bridge 推进成了 14-item proxy-expanded reintegration，而且是用完全显式的 provenance 和机械校验做出来的。当前最强信号是：即使把更宽 mixed stress slice 一次性接回来，`claim_normalized_literal_identity_anchor` 仍然保持 relation/code/weak-name 非回退、note-aware `false_present=0.000`，并继续把 strengthened aligned-name pair 提升成 explicit tentative target claim。下一步最值得做的已经不是再补 bridge 分析，而是对那 6 个缺 cache 的 stress item 做一次 exact literal-identity live closure，看看 proxy win 能不能真正落成 broader actual-stress result。
