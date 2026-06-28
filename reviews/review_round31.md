# Review Round 31

## What Improved

1. 这一轮不是只补了一个洞，而是真的把 bundled closure round 里承诺的三件事都推进了。最关键的是 exact live closure 已经完成：`halu_02/03/04/05/08/14` 的 `literal_identity_anchor` 缺失 cache 被真实 DeepSeek 调用补齐，新的 [actual_hallucination_literal_identity_closure_summary.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/actual_hallucination_literal_identity_closure_summary.md) 显示，在这 6 条 non-literal stress item 上，`literal_identity_anchor` 的 `N=8` literal branch 没有回退，`scale_aware_unified` 与 `scale_aware_note_aware` 的 `false_present` 都是 `0.000`，`summary_only` accuracy 也还有 `0.833`。更重要的是，这批 exact rows 现在已经被接回 [actual_hallucination_claim_reintegration_pilot_summary.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/actual_hallucination_claim_reintegration_pilot_summary.md)，当前 reintegration mode 变成了 `exact_stress_closure_reintegration`，proxy rows 从旧的 `108/336` 变成 `0/336`。
2. reviewer-facing 的 frozen model-backed baseline panel 现在终于不再是假 single-seed sanity 了。`actual_recall_expansion` 和 `actual_hallucination_stress` 都已经扩成 seeds `[11, 23]`，而且机械核对全部通过。新的 recall panel 在 `N=8` 仍然复现同一结论：`summary_only` accuracy 只有 `0.208`，`tiered` 是 `0.792`，`scale_aware_unified`/`scale_aware_note_aware` 是 `0.875`，同时 `history_loss_rate` 仍高达 `0.875`。新的 stress panel 也维持同一结构：`N=1` 时 `scale_aware_note_aware false_present = 0.062`，优于 `scale_aware_unified = 0.125`；到 `N=8` 时两者都降到 `0.000`。这意味着 multi-seed 扩张没有推翻我们此前的 story，而是把它从单 seed 局部现象提升成 reviewer-facing frozen panel。
3. external benchmark 这块虽然还没有变成真正 data-ready 的主 baseline，但现在已经不再是“完全没接”。新的 [external_benchmark_adapter_layer.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/external_benchmark_adapter_layer.md) 把一条 HaluMem-style hallucination slice 和一条 LoCoMo/LongMemEval-style benign-utility slice 的 adapter contract、字段要求、冻结规则、目标指标和本地 source path 全都固定下来了。因此在新的 [paper_baseline_packet.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/paper_baseline_packet.md) 里，`primary_external_benchmark_grounding` 已经从纯 `gap` 提升成 `partial` 的 adapter-backed state，而不是继续悬空。
4. 这意味着 paper baseline packet 的 blocker 结构已经实质性收缩。现在 `multi_seed_model_backed_panel = pass`，`exact_non_proxy_frontier_closure = pass`，`primary_external_benchmark_grounding = partial`，真正还没有动摇的硬 blocker 只剩两类：benchmark data 还没放进 adapter、repo 还没变成 reviewer 会接受的 TierMem-style primary base。

## Main Weaknesses

### W1. External benchmark grounding 现在只是 adapter-ready，不是 data-ready

虽然 packet 里的 benchmark 状态已经不是纯 `gap`，但 `data_ready_count` 仍然是 `0/2`。也就是说，我们已经知道 benchmark slice 应该怎么接、接到哪里、要报哪些指标，但我们还没有真正把外部 benchmark 样本冻进 repo 并跑起来。

### W2. Primary implementation 仍然是 local proxy stack，不是论文主 baseline

这轮补齐的是 exact closure、multi-seed sanity 和 adapter contract，但没有改变 repo 的 primary face。reviewer 如果现在看代码，仍然会觉得这是一个高质量 pre-pilot proxy stack，而不是一个 benchmark-grounded、TierMem-style 主实现。

### W3. Recall-side 主科学瓶颈没有因为 multi-seed 扩张而消失

multi-seed 是好事，因为它说明结论更稳了；但它也让一个问题更难回避了：当前 benign/conflict 的主瓶颈确实已经是高 `N` 下的 answerability loss，而不是偶然 seed 波动。`scale_aware_unified` 在 `N=8` 依然有 `0.875` 的 `history_loss_rate`。这不是说当前方法没价值，而是提醒我们未来接 LoCoMo/LongMemEval-style utility slice 时，不能只看 hallucination suppression，而必须保住这条 utility failure axis。

## Bottom Line

按照 autoresearch 的标准，这一轮是非常像“真正收缩 blocker 列表”的一轮，而不是继续长局部分支。exact frontier 已经从 proxy 变成 exact，model-backed baseline panel 已经从 single-seed 变成 multi-seed，benchmark 也已经从完全没接变成 adapter-backed partial。下一轮不该回头再打新的 local policy variant，而应该直接做两件 reviewer 真正在意的事：把 benchmark data 放进现有 adapter，和把 repo 的 primary surface 往 TierMem-style base 推。
