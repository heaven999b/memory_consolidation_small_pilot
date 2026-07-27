# 第四周汇报 · 记忆系统的质量—成本—风险 trade-off 复现与研究问题收敛

**日期：2026-07-28**

> 本周是一个独立的“近期记忆论文复现与选题”工作包：先扫描近期 memory×trade-off/utility 论文，再复算公开结果、跑小样本真实 baseline、检查完整资源账本，最后从异常和设计取舍中筛选可发表的小问题。本文不使用前三周研究假设来解释这些论文。

配套文件：

- [逐论文 baseline 对照矩阵](./baseline_replication_matrix_20260728.md)
- [Research proposal 路线图](./research_proposal_roadmap_20260728.md)

## 0. 一句话结论

本周最重要的结果不是“又跑了若干模型”，而是确认了三个跨论文现象：

1. **少上下文不等于低总成本**：Engram 查询上下文缩短 8.37×，但单查询计入抽取后总 token 是 full context 的 1.35×；Supersede 的 bounded rewrite 在 108 条件中质量更低、成本和延迟反而更高；TokenPilot 的公开账本只覆盖主模型，无法识别完整 TCO。
2. **最值得优化的是何时调用昂贵 memory operation**：Lethe 的锁定 selector 在 305 条外部样本上，以 3.93pp 的质量差换取 53.48% calls 和 59.29% tokens 节省，且 0 over-delete；但跨语言出现 26.7pp 崩点，说明路由必须带 OOD 风险控制。
3. **结构化策略的收益依赖 metadata/annotation 可信度**：Pi-CWL 在干净标注下比 recency 高 2.17pp，但噪声 0.75 时反而低 2.84pp；一个冻结 fallback 在新 seed held-out 上提高 recall 0.68pp，却增加 2.03pp closure violation。

因此，当前第一研究主线是：**事件触发的 delta memory maintenance + 完整生命周期 utility**，而不是继续调摘要长度。

## 1. 本周完成了什么

### 1.1 扫描与设计解剖

- 对 8 篇主论文完成实验设计拆解、代码冒烟和候选问题生成；
- 扩展到 LongMemEval-V2、Agent-Native、TokenPilot、Engram、Supersede、Lethe、Pi-CWL 等 released baselines；
- 所有结论按 exact / released recomputation / substitute / mechanism test / NO-GO 分级；
- 没有把下载、dry-run、任务 active 或写完代码计作实验样本。

### 1.2 本周可审计实验规模

| 项目 | 有效规模 | 主要输出 |
| --- | ---: | --- |
| LongMemEval-V2 | 30 queries；42 calls；1,048,102 tokens | substitute retrieval/packing diagnostic |
| Agent-Native | 10 paired cases；20 calls；300,328 tokens | BM25 memory vs no-memory |
| TokenPilot | live paired 0/5 NO-GO；released aggregate 复算 | quality、input、main-model cost |
| Engram | released 500题输出复算；真实替代栈 30 paired；reader robustness 10 | lean/full accuracy、preprocess/query ledger |
| Supersede | 25 paired baseline + 108 condition matrix | full vs bounded accuracy/cost/latency |
| Lethe | deterministic 385；selective 80；锁定 selector 外部 305 | underforget/overdelete/calls/tokens |
| Pi-CWL | 1,200 mechanism + fresh-seed 1,200 held-out | recall/closure/annotation-noise |
| MemPrivacy | 48×8 + 48×6 controls | privacy/linkability/utility identification |
| MemTrace | 5-case mechanical audit + 4 cases×4 arms | causal replay feasibility and variance |
| MemSyco | 20×5 valid observations | packet/framing utility boundary |

全部调用仅使用当时已授权的本地代理；官方按量付费 API 调用为 0；所有 `gpt-5.6-*` 调用为 0。

## 2. 哪些实验真正研究了 trade-off 或 utility

### 2.1 直接、定量的 trade-off

| 项目 | 质量/风险端 | 资源端 | 本周得到的 trade-off 结论 |
| --- | --- | --- | --- |
| Agent-Native | BM25 memory EM 100%、F1 1.0；no-memory EM 90%、F1 .9556 | memory 多 284,288 input tokens | +10pp EM 需要每例约 +28.4k input tokens；不能默认总是加载 memory |
| TokenPilot | released quality 79.2%→81.3%（+2.1pp） | input -67.38%，主模型成本 -61.50% | 主模型账上 Pareto 改善成立，但 estimator/distiller/embedding 未入账，完整 TCO 未识别 |
| Engram | released lean 83.6% vs full 73.2%；替代栈 lean 86.67% vs full 100% | query context 省 8.37×；加预处理后一问一历史 lean 贵 1.35× | query-time 优势不等于生命周期优势；解析 break-even 为 1.406 queries/history |
| Supersede | 25题 full 76% vs bounded 40%；108 条件中 bounded 六格准确率都更低 | bounded 成本高 116.4%；平均延迟 89–142s vs full 3.3–3.7s | bounded rewrite 被 full Pareto 支配；对任意 λ≥0，`Uλ=accuracy−λ·cost` 无 crossover |
| Lethe | external305：selective-50 87.21% vs always 91.15%；0 over-delete | 节省 53.48% calls、59.29% tokens | 得到真实 held-out quality–resource Pareto；跨语言组损失扩大到 26.7pp |
| Pi-CWL | fallback recall .9809 vs CWL .9741 | 等 memory budget；closure violation 0→.0203 | recall 增益换取结构风险；不是单指标全面获胜 |
| Beyond-ML | held-out selector score 5.0 vs fixed-50k 5.4583 | token 节省 31.29% | generic router 没过 utility 门：省 token 但效用下降，按预注册规则止损 |
| MemPrivacy | typed metadata 提高 attribute/link inference；部分任务 utility 保留、部分明显下降 | metadata/token 表示不同 | 不存在全局 masking 排名；必须做 task-conditional privacy–utility–token Pareto |

### 2.2 与 utility 有关，但当前仍有因果混杂

- **MemTrace**：strict arm 平均 ΔF1 `+.1017`，输入 token 同时从约 10,148 降到 655。收益可能来自纠错，也可能来自 93.5% 上下文剪枝或生成噪声，必须加入 length-matched deletion、irrelevant replacement 和重复 placebo。
- **MemSyco**：raw utility `.90`，neutral scaffold/sham 类条件为 `1.0`，但 raw failures 只有 2/20，未达到预注册 boundary 门；只能作为 framing 机制线索。
- **GateMem**：主要测 recovery/confirmation leakage 的分阶段风险，目前没有形成可信资源—效用曲线。
- **LongMemEval-V2**：当前主要是 substitute retrieval/packing 失败诊断，不能拿 10% accuracy 构造论文级 trade-off。

### 2.3 本项目采用的 utility 观念

本项目不把“accuracy/token”简单比值当作唯一 utility，而把以下维度并列报告：

- task quality / exact match / judge score；
- under-forgetting、over-deletion、privacy/linkability 等风险；
- write、extract、consolidate、retrieve、answer、judge、sidecar 的 calls/tokens；
- latency、cache regime、失败重试；
- query reuse 和 update density；
- risk–coverage 与 Pareto frontier。

Supersede 已直接检验 `Uλ=accuracy−λ·cost`；Lethe 和 Pi-CWL 采用约束式 utility 更合理，即先约束风险上限，再最小化调用成本。

## 3. 复现了哪些 baseline，和论文是否一致

详细证据见[逐论文对照矩阵](./baseline_replication_matrix_20260728.md)。简要结论如下。

### 3.1 可以明确说“复现一致”的两项

1. **Lethe deterministic baseline**：作者公开 headline 为 `244/385=63.4%`；本地使用 released deterministic pipeline 与 scorer 重算得到 `244/385=63.38%`。分子分母完全一致，属于精确复现。
2. **Engram released outputs**：作者公开 `engram_lean 83.6%`、`full-context 73.2%`；对公开的 500 题输出独立聚合得到相同结果。它验证了 released artifact 与报告数字一致，但不是重新调用论文原始 Doubao/DeepSeek 栈。

### 3.2 公开聚合复算一致，但没有完成 live end-to-end 的一项

**TokenPilot**：官方 released continuous aggregate 为 Vanilla 79.2%、TokenPilot/LightMem2 81.3%，主模型成本约 `$7.24→$2.79`。使用作者 cost parser 重算为 `$7.242375→$2.788575`，与公开值一致；但 macOS/Linux harness 和本地 gateway 使 live paired 0/5，因此不能声称端到端复现，更不能把主模型账称为完整 TCO。

### 3.3 方向一致、数字不应要求相同的一项

**Supersede**：论文在 LongMemEval knowledge-update oracle split（n=78）报告 full-context 92%、300字符 bounded memory 77%，差 15pp。我们的替代模型小切片（n=25）为 76% vs 40%，差 36pp。方向一致，且 108 条件扩展继续显示 bounded 被支配；但由于模型、样本和规模不同，不能叫数字复现。

### 3.4 与论文不能直接比较的非精确验证

- **Engram live 30**：论文/released 方向为 lean 高 10.4pp；替代栈为 lean 低 13.33pp。这个方向反转很重要，但 n=30、模型和 embedding 均不同，不能写成推翻论文，只能写“headline 对模型/表示栈不稳健的 provisional evidence”。
- **LongMemEval-V2**：3/30=10%，但同时替换了 embedding、retrieval、截图输入和 reader，并存在 context cap；不能归因于论文 baseline。
- **Agent-Native**：论文是 22 个系统和多个自建/重构子集的横评；我们是 10 个 BM25-vs-no-memory diagnostic cases，且论文 Qwen3-8B answer backbone 不可用，没有一一对应 headline。
- **MemPrivacy、MemTrace、MemSyco、GateMem、Beyond-ML**：均得到可复算的小样本机制结果，但存在 substitute model、self-judge、shadow adapter 或数据切片变化；不报“论文数值复现”。
- **Pi-CWL**：精确调用官方 `filterContext` 完成 1,200+1,200 等预算机制实验，但这是官方函数的 mechanism test，不是论文 agent benchmark headline。

## 4. 论文结果与本周结果的核心差异

### 4.1 Engram：公开数字复算一致，但全链路结论不一致

- 论文/README 的 query-time 表：lean 83.6%、full 73.2%，约 8× 更短；
- 我们确实复算出这两个准确率；
- 但 released 账本未计构建 lean memory 的抽取 token；
- 在真实 30 题替代栈中，预处理使用 3,844,788 tokens；一问一历史时 lean 总计 4,265,154，full 为 3,155,656；
- 因此，“查询 prompt 更短”成立，“单查询端到端更省”不成立。

### 4.2 Supersede：复现了方向，并发现固定 bounded rewrite 不存在 break-even

论文的 full > bounded 方向得到支持；进一步的 108 条件结果显示，不只是 300 字符预算选错：150/300 在 short/medium/long 六格全部更差更贵。下一步应改变更新机制，而不是继续扫摘要长度。

### 4.3 Lethe：headline 精确复现，但 always-hook 不是唯一合理部署点

deterministic 63.4% 精确复现；使用替代 LLM hook 后，always 的外部集成功率为 91.15%。锁定 selector 能以少量质量损失节省过半调用，但跨语言失效说明 selector coverage 是新瓶颈。

### 4.4 TokenPilot：公开主模型成本成立，完整 TCO claim 不可识别

我们没有发现作者公开 aggregate 的算术问题。问题在测量边界：released 数据不含 estimator、distiller、embedding sidecars，所以“主模型成本下降 61.5%”成立，“整个系统总成本下降 61.5%”没有证据。

## 5. 本周形成的研究主线

### 第一优先：生命周期 utility + event-triggered delta maintenance

研究问题：在 update density、reuse count、冲突风险和完整生命周期成本共同约束下，什么时候应该 NOOP、append delta、local merge 或 full rebuild？

价值不在“不要每轮更新”这句常识，而在：

- 明确测量 write amplification；
- 用完整 ledger 找到策略相图；
- 比较 delta/local merge/full rebuild；
- 给出什么时候哪个策略被 Pareto 支配。

### 第二优先：OOD-aware 风险校准 selective forgetting

研究问题：在 under-forgetting 和 over-deletion 代价不对称的条件下，如何在语言/脚本迁移时维持风险上限，同时减少 LLM hook 调用？

硬缺口：需要新 seed、零重叠的多语言外部集。旧 38 条补丁回放只能是 exploratory。

### 第三优先：minimum-sufficient memory metadata

研究问题：完成特定任务最少需要暴露哪些类型、身份和跨会话链接结构？能否用 coarse type + session-rotating alias + task-gated reveal 降低 linkability，同时保留效用？

### 条件继续：annotation-fidelity-aware structured eviction

Pi-CWL 的噪声反转是扎实 mechanism evidence，但必须先在真实 agent traces 上测 dependency annotation 的 FPR/FNR，再决定是否发展成方法论文。

### 共同评测层：variance-aware causal replay

任何 memory intervention 都应加入 identical-prompt placebo、matched-length deletion、irrelevant replacement 和重复运行，避免把 token compression 或生成方差误判为记忆内容的因果收益。

## 6. 哪些说法只是常识，不能当论文创新

- “记忆系统也消耗 tokens”；
- “不是每轮都应该检索或更新”；
- “压缩可能丢信息”；
- “元数据也可能泄露”；
- “OOD 会导致 selector 掉点”；
- “错误标注会影响结构化算法”；
- “选择性遗忘比 always/never 更灵活”。

论文贡献必须进一步给出：可观测机制、方法、风险/资源约束、held-out 验证、失败边界和 go/no-go。

## 7. 下一阶段最低实验闭环

主 proposal 暂定：**When Should Agent Memory Update? Event-Triggered Delta Maintenance under Full-Lifecycle Utility**。

最低实验矩阵：

1. 两个数据集：长对话状态更新 + agent/tool trajectory；
2. 四臂：always full rewrite、fixed-periodic、event-triggered delta、no maintenance；
3. 2/6/12 sessions，低/高 update density，每段 history 至少 3 个独立 query；
4. 完整记录 write/extract/consolidate/retrieve/answer/judge/sidecar；
5. 指标：任务成功、stale/conflict、write amplification、tokens、latency、cache；
6. 两个 reader/writer 模型栈；
7. 配对 CI 与预注册 go/no-go。

GO 条件：相对 every-session rewrite，维护 calls 至少下降 50%，任务质量损失不超过 3pp，并在至少一个现实 reuse/update 区域进入 Pareto 前沿。

NO-GO 条件：收益完全等价于简单 fixed-periodic/token threshold，或换数据/模型后消失。

## 8. 证据边界

- 精确复现仅用于 Lethe deterministic headline；
- Engram 与 TokenPilot 的“一致”指 released artifact/aggregate 重算一致；
- 其余真实调用多数为 substitute-stack validation，不能写成论文原模型精确复现；
- 没有新数据生成器时，不用旧样本冒充确认性外部验证；
- raw prompts/responses 和本地代理凭据未进入公开仓库；
- 正式论文前仍需完成 related-work collision audit、外部数据与跨模型确认。

**本周最终判断**：作为 weekly report 已充分；作为主 proposal 的 preliminary evidence 已充分；作为最终论文仍缺事件触发方法实现、强基线、外部数据与跨模型验证。
