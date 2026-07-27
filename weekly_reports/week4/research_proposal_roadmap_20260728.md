# Week 4 Research Proposal Roadmap

**日期：2026-07-28**

## 1. 从“本周结果”到“完整论文”还差什么

当前已经具备：真实 baseline 结果、公开产物复算、失败案例、成本账本、部分 held-out 验证和明确 NO-GO。

仍缺：一个聚焦的问题、一项明确方法、两个外部数据来源、强 adaptive baselines、跨模型确认和冻结的统计方案。

## 2. 方向排序

| Rank | Direction | 当前证据 | 新颖性（收窄后） | 完成度 | 决定 |
| ---: | --- | --- | --- | --- | --- |
| 1 | Event-triggered delta maintenance under full-lifecycle utility | Engram + Supersede + TokenPilot + Agent-Native | 中高 | 高 | 主 proposal |
| 2 | OOD-aware risk-calibrated selective forgetting | Lethe locked external305 + cross-lingual failure | 中高 | 中高 | 继续，先补外部多语言集 |
| 3 | Minimum-sufficient memory metadata | MemPrivacy controls + framing/structure evidence | 高 | 中 | 继续，实现方法 |
| 4 | Evidence-sufficiency certificate + selective fallback | Engram representation failures | 中 | 中 | 条件继续或并入第1项 |
| 5 | Annotation-fidelity-aware structured eviction | Pi-CWL noise reversal + fresh-seed fallback | 中 | 中 | 先做真实 trace audit |
| 6 | Variance-aware causal replay | MemTrace placebo/length confound | 中 | 中 | 作为共同评测层 |

## 3. 主 proposal

### Tentative title

**When Should Agent Memory Update? Event-Triggered Delta Maintenance under Full-Lifecycle Utility**

### Research question

在更新密度、未来复用概率、冲突风险和完整生命周期成本共同约束下，agent memory 什么时候应该：

- `NOOP`；
- `APPEND_DELTA`；
- `LOCAL_MERGE`；
- `FULL_REBUILD`？

### 为什么不是常识

“不要每轮都更新”是常识；可发表的问题必须回答：

- every-session rewrite 的 write amplification 有多大；
- 哪些在线可观测量能预测 full rebuild 的必要性；
- delta 何时因碎片化、冲突或 stale state 失效；
- 在 update density × reuse count × cache regime 的哪个区域，不同策略进入 Pareto frontier；
- 计入所有辅助调用后，结论是否仍成立。

### Method sketch

事件触发器只使用在线信息：状态差异、冲突数、实体/任务边界、预测复用、memory fragmentation 和校验风险。禁止使用最终答案或 test label。

### Required baselines

1. no maintenance；
2. always full rewrite；
3. fixed-periodic rewrite；
4. fixed token-budget summary；
5. simple threshold rule；
6. learned operation policy。

### Required datasets

- 一个长对话、状态持续更新的数据集；
- 一个 agent/tool trajectory 数据集；
- 每个 history 至少三个独立 future queries，确保 maintenance setup cost 可以真实摊销。

### Metrics

- task success / answer correctness；
- stale fact、conflict、missing update；
- write amplification；
- write/extract/consolidate/retrieve/answer/judge/sidecar tokens；
- p50/p95 latency；
- cache-sensitive 与 all-cold TCO；
- Pareto frontier 与 phase diagram。

### Go / no-go

GO：相对 every-session rewrite，维护 calls 至少下降 50%，质量损失不超过 3pp；并且在两个数据集、两个模型栈的至少一个现实区域进入 Pareto frontier。

NO-GO：效果可被简单 periodic/token threshold 完全解释；或换数据/模型后消失。

## 4. 第二 proposal：OOD-aware selective forgetting

### Observation

Lethe selective-50 在 external305 上仅比 always 低 3.93pp，却节省 53.48% calls 和 59.29% tokens，0 over-delete；跨语言组却低 26.7pp。

### Research question

如何在 under-forgetting 与 over-deletion 代价不对称时，用 OOD detector 或 conformal risk control 保证最坏组风险，并在安全区域减少 LLM hook？

### Missing pieces

- 新 seed、与旧集合零文本 hash 重叠的多语言数据；
- language/script/paraphrase/attack-template 三类 OOD；
- never/always/rule/embedding/LLM/conformal selector；
- risk@coverage、worst-group、underforget、overdelete、calls/tokens；
- selector calibration/test 完全分离。

### No-go

如果新语言上为满足风险上限必须接近 100% always-hook，则 selective 方法没有部署价值。

## 5. 第三 proposal：minimum-sufficient metadata

### Observation

MemPrivacy controls 显示具体值恢复很少，但 coarse type 与跨会话链接结构本身显著改变 attribute/linkability；效用随任务强烈变化。

### Research question

对完成某类记忆任务而言，最少应暴露哪些类型、身份和链接信息？

### Method sketch

- coarse semantic type；
- session-rotating alias；
- task-gated reveal；
- 必要时才恢复稳定 identity link；
- confidence-tagged dependency。

### Missing pieces

- 实现编码方案，而不是只做 swap/shuffle；
- 个性化、时间连续性、跨会话检索三类任务；
- raw ID、hash、session-local ID、opaque、noise/DP baselines；
- utility、attribute risk、linkability、exact recovery、tokens 的联合 Pareto；
- 多攻击者、多模型、辅助知识 threat model。

## 6. 条件方向

### Representation-risk-aware fallback

普通的“何时检索/何时注入”已经拥挤。只有做成 **evidence-sufficiency certificate + provenance coverage + calibrated selective risk + local/full fallback** 才值得独立投稿。

### Annotation-fidelity-aware eviction

“坏标注会伤性能”没有新意。可发表版本必须证明存在可观测的 annotation-fidelity phase transition，并在真实 agent traces 上用风险校准 fallback 改善任务成功，而不是只在 synthetic cases 上提高 recall。

### Variance-aware causal replay

适合作为全部 proposal 的共同实验规范：identical-prompt placebo、matched-length deletion、irrelevant replacement、重复采样和 hierarchical analysis。

## 7. Related-work collision boundary

以下 broad headlines 已经拥挤，不能直接当创新：

- selective memory retrieval / abstention：[Learning When to Remember](https://arxiv.org/abs/2604.27283)
- proactive selective memory intervention：[Remember When It Matters](https://arxiv.org/abs/2607.08716)
- selective add/delete management：[How Memory Management Impacts LLM Agents](https://arxiv.org/abs/2505.16067)
- learned ADD/UPDATE/DELETE/NOOP：[Memory-R1](https://arxiv.org/abs/2508.19828)
- memory vs long-context cost break-even：[Beyond the Context Window](https://arxiv.org/abs/2603.04814)
- agent unlearning / selective forgetting：[Agentic Unlearning](https://arxiv.org/abs/2602.17692)

本项目需要坚持的差异点：

- 写入侧 maintenance frequency 与 write amplification；
- delta/local merge/full rebuild，而非普通 retrieval router；
- 全生命周期 TCO，而非只统计最终 prompt；
- 非对称遗忘风险与 OOD safety fallback；
- identity linkability 下的 minimum-sufficient metadata；
- annotation fidelity 的相变和风险控制。

## 8. 完整 research baseline 的最低交付清单

1. 一个可证伪的单句研究问题；
2. 一项明确方法，而不只是指出已有 baseline 有问题；
3. 两个数据来源，至少一个真正外部 held-out；
4. 4–6 个强 baselines，至少一个 adaptive/learned baseline；
5. 同样本、同模型、同预算的配对比较；
6. 端到端质量、风险、成本和延迟；
7. 机制消融与失败案例分类；
8. 至少两个模型栈；
9. 锁定参数、fresh seed、零重叠和置信区间；
10. sample-level outputs、scorer、账本和运行说明；
11. 明确 exact / substitute / mechanism / exploratory / NO-GO；
12. 大规模实验前完成正式 novelty collision audit。

## 9. Final recommendation

- 主攻：event-triggered delta maintenance；
- 并行准备但暂不放大：OOD-aware selective forgetting 的新外部数据；
- 概念储备：minimum-sufficient metadata；
- 其余方向并入评测/机制章节，不要把六条线硬塞进一篇论文。
