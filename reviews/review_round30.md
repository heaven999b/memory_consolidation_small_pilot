# Review Round 30

## What Improved

1. 这一轮没有再继续把局部 heuristic 往外推，而是把项目第一次真正整理成了一个 reviewer-facing 的 paper baseline packet。新产物 [paper_baseline_packet.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/paper_baseline_packet.md) 把 synthetic closed-loop baseline trio、model-backed sanity slices、frontier proxy 状态、以及 paper-level blockers 放进同一个冻结 artifact 里。这个动作本身就很符合 autoresearch：先把 gate 冻结，再围着 gate 打。
2. 这个 packet 让“我们到底已经跑通了什么”第一次变得机械可验。它明确标记 `minimal_closed_loop_baseline_ready = true`，同时明确标记 `paper_level_baseline_ready = false`，并把主要 blocker 固定成四个：没有 external benchmark grounding、没有 TierMem-style primary grounding、冻结的 model-backed baseline panel 还不是 multi-seed、以及当前 stress-frontier claim result 仍是 proxy-backed exact-closure gap。
3. 这轮还把 baseline 面板从“代码里其实有”变成了“论文里可以直接拿出来讲”。synthetic core panel 现在能一眼看出：`summary_only` 在 `N=8` 时 accuracy 掉到 `0.004`、propagation 升到 `0.996`；`tiered` 在 `N=8` 仍有 `0.977` accuracy 和 `0.023` propagation；`scale_aware_unified` 在 `N=8` 有 `0.985` accuracy 和 `0.015` propagation。这个对比已经是 reviewer 能快速抓住的 clean baseline story。
4. model-backed sanity 也被放进了同一个包里，所以我们不再需要口头补充“其实还有 real slice”。现在 benign/conflict recall sanity 和 hallucination stress sanity 都是 baseline packet 里的正式组成部分，而不是散在各轮 review 里的旁证。

## Main Weaknesses

### W1. baseline packet 只是冻结了差距，不是自动补上差距

这轮最大的进步是诚实和结构化，但它没有神奇地把 project 变成 benchmark paper。external benchmark grounding、TierMem-style primary grounding、multi-seed frozen model-backed panel、exact non-proxy frontier closure 仍然都没做完。

### W2. exact closure 仍然是当前最短板的实验 blocker

虽然 broader claim frontier 已经有一个 14-item proxy-expanded packet，但 reviewer 很自然会问：为什么 `108/336` 行还是 proxy？如果这个问题不解决，当前最有趣的 stress-side representation result 仍然只能当作强 follow-up 线索，不能当作论文主结果。

### W3. baseline 与 benchmark 之间还差 adapter layer

我们现在已经很清楚论文要什么 benchmark role：hallucination 主轴、benign utility 主轴、以及 raw/summary/tiered 统一协议。但 repo 里还没有一层冻结的 benchmark adapter，把 HaluMem/LongMemEval/LoCoMo-style slice 映射进当前 evaluation contract。没有这一层，paper baseline 仍然停在 local audited slice。

## Bottom Line

这轮最大的价值不是新数字，而是把“论文级 baseline 到底差什么”变成了一个不再含糊的固定门槛。按照 autoresearch 的框架，这正是该做的事：当实验系统已经能跑、局部 frontier 也开始复杂起来时，下一步不是继续长分支，而是先冻结 reviewer-facing baseline gate。现在 gate 已经有了，下一轮就该对着它补最短板，而不是再泛化地说“离论文更近了”。
