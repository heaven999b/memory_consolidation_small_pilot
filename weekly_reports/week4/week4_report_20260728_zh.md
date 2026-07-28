# 第四周汇报 · 记忆系统的质量—成本—风险 trade-off 复现与研究问题收敛

**日期：2026-07-28**

> 本周是一个独立的“近期记忆论文复现与选题”工作包：先扫描近期 memory×trade-off/utility 论文，再复算公开结果、跑小样本真实 baseline、检查完整资源账本，最后从异常和设计取舍中筛选可发表的小问题。本文不使用前三周研究假设来解释这些论文。

配套文件：

- [第一轮五线确认实验结果](./round1_followup_results_20260728.md)
- [逐论文 baseline 对照矩阵](./baseline_replication_matrix_20260728.md)
- [Research proposal 路线图](./research_proposal_roadmap_20260728.md)
- [下一阶段投入决策](./investment_decision_20260728.md)

## 0. 一句话结论

本周最重要的结果不是“又跑了若干模型”，而是确认了三个跨论文现象：

1. **少上下文不等于低总成本**：Engram 查询上下文缩短 8.37×，但单查询计入抽取后总 token 是 full context 的 1.35×；Supersede 的 bounded rewrite 在 108 条件中质量更低、成本和延迟反而更高；TokenPilot 的公开账本只覆盖主模型，无法识别完整 TCO。
2. **最值得优化的是何时调用昂贵 memory operation**：Lethe 的锁定 selector 在 305 条外部样本上，以 3.93pp 的质量差换取 53.48% calls 和 59.29% tokens 节省，且 0 over-delete；但跨语言出现 26.7pp 崩点，说明路由必须带 OOD 风险控制。
3. **结构化策略的收益依赖 metadata/annotation 可信度**：Pi-CWL 在干净标注下比 recency 高 2.17pp，但噪声 0.75 时反而低 2.84pp；一个冻结 fallback 在新 seed held-out 上提高 recall 0.68pp，却增加 2.03pp closure violation。

因此，本周已经形成了可靠的问题证据；但后续五线确认实验进一步改变了排序：**minimum-sufficient identity continuity、candidate-first safe forgetting、replay-certified retrieval repair** 成为前三。原 OOD router 因只省 11.46% calls 而 NO-GO，Annotation observable 因缺乏 corruption discrimination 而 NO-GO；生命周期 confirmation 只得到由 2/12 histories 驱动的稀疏增益。完整证据见[第一轮五线确认实验结果](./round1_followup_results_20260728.md)。

### 0.1 第一轮确认实验后的增量结论

- 五条正式接续共完成 1,178 次真实本地代理调用、3,126,042 tokens；公开数据来源、prompt hash、actual model、sample-level scorer 和 cluster-aware CI 均有审计产物。
- MemPrivacy 的 stable typed→rotating typed 令 link balanced accuracy 从 100% 降至 50%，user-cluster 95% CI 为 `[38.89,57.58]pp`；但 attribute inference 未同步降低，且 full-48 gated loss 5.21pp、recovery 66.7% 未过方法门，证明 value、attribute、link、utility 不能合并成一个分数。
- MemTrace 正确替换相对 baseline 的 F1 增益为 `+.1864 [.0463,.3880]`，且显著胜 length-matched deletion 与 irrelevant replacement；但所有 strict EM 都为 0，只能称为机制信号。
- Lethe risk policy 与 always 同为 90% accuracy，却只省 11.46% calls；6/15 always failures 在 candidate-empty 阶段就阻断 hook，下一步应前移到 candidate recovery，而不是再调 router。
- Lifecycle BM25 只多答对 2 题却多用 1.027M tokens；Annotation 的旧 observable 对四类 corruption 的 route-change 最高仅 0.90%。两线均不应继续无条件扩样。

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
| MemPrivacy | 48-source 四臂 minimum-metadata confirmation；685 calls | value/attribute/link/utility 分离与 user-cluster inference |
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

## 5. 证据质量、撞题情况与修正后的研究主线

### 5.1 哪些结果质量足以继续投资

| 结果 | 内部效度 | 外部效度 | 当前研究价值 | 主要限制 |
| --- | --- | --- | --- | --- |
| Lethe selective forgetting | 高：锁定 selector、external305、零重叠、配对资源账 | 中高 | 已形成可发表级 Pareto seed | hook 为替代模型；缺新生成多语言确认集 |
| Supersede 108 conditions | 高：paired CI、两种成本口径、utility 无 crossover | 中 | 强负结果与 write-amplification 证据 | 12 cases/cell；模型替代 |
| Pi-CWL 2,400 cases | 高：官方函数、fresh seed、零 hash 重叠 | 中低 | annotation-noise sign reversal 很清楚 | synthetic mechanism，不是完整 agent 任务 |
| Engram lifecycle audit | 中高：released500 + live30 + 全链路 ledger | 中 | 很好的测量/critical re-evaluation 证据 | live 模型与 embedding 非论文原栈 |
| MemPrivacy controls | 中 | 中低 | linkability 机制 seed | 尚未实现新 metadata 方法 |
| MemTrace causal replay | 中低 | 低 | 可作为所有方向的评测规范 | 例数少；compression/variance 混杂 |
| Agent-Native / LongMemEval | 低到中 | 低 | 诊断和止损价值 | 与论文主协议差异太大 |

### 5.2 哪些 broad ideas 已经被占位

| Broad idea | 已有近邻 | 结论 |
| --- | --- | --- |
| 学习 `ADD/UPDATE/DELETE/NOOP` | [Memory-R1](https://arxiv.org/abs/2508.19828) | 不能再把 memory operation policy 本身当创新 |
| incremental/delta experience memory | [DeltaMem](https://arxiv.org/abs/2606.03083) | “写 delta 而非全量重写”本身已经不新 |
| buffer + periodic consolidation | [Infini Memory](https://arxiv.org/abs/2606.10677) | 定期/分层维护已有直接方案 |
| 统一控制 retrieve/consolidate/forget | [MemCon](https://arxiv.org/abs/2607.13591) | generic adaptive controller 已高度拥挤 |
| selective retrieval / abstention | [Learning When to Remember](https://arxiv.org/abs/2604.27283) 等 | 普通 router/fallback 不足以独立投稿 |
| selective forgetting / agent unlearning | [FSFM](https://arxiv.org/abs/2604.20300)、[Secure Forgetting](https://arxiv.org/abs/2604.00430)、[Agentic Unlearning](https://arxiv.org/abs/2602.17692) | 必须收窄到 persistent-memory mutation 的非对称风险与 OOD |
| typed privacy placeholder | [MemPrivacy](https://arxiv.org/abs/2605.09530) | 不能只重复 type-aware masking；必须研究 cross-session linkability |
| dependency-structured memory | Pi-CWL、[ContextWeaver](https://arxiv.org/abs/2604.23069) | 不能只证明结构优于 recency；要研究 annotation 不可信时的反转 |

### 5.3 修正后的优先级

1. **Minimum-sufficient identity continuity**：48-source 结果已显示 stable alias 的 link 风险与 attribute/value 风险分离，但当前方法门 NO-GO；下一步实现非 oracle reveal policy，并做 user-disjoint / 第二公开 benchmark 确认。
2. **Candidate-first safe forgetting**：原 OOD router 正式 NO-GO；利用 6 个 candidate-empty 失败，研究 multilingual dense recovery、abstention 与 mutation-level routing。
3. **Replay-certified retrieval repair**：MemTrace 五臂多 seed 机制门通过；扩大到 20–30 个预冻结 cases，并把 strict task success 作为主终点。
4. **Marginal-value memory invocation benchmark**：Lifecycle 的增益只来自 2/12 histories，先确认 history-level 稀疏性并比较强 selective baselines，不直接造 generic router。
5. **Annotation-fidelity observable redesign**：旧 validator 正式 NO-GO；先找到同结构内有变异且与 downstream failure 校准的 observable，暂不烧模型 token。
6. **Representation fallback**：普通版本撞题最严重；除非能做 evidence-sufficiency certificate，否则降级。

## 6. 哪些说法只是常识，不能当论文创新

- “记忆系统也消耗 tokens”；
- “不是每轮都应该检索或更新”；
- “压缩可能丢信息”；
- “元数据也可能泄露”；
- “OOD 会导致 selector 掉点”；
- “错误标注会影响结构化算法”；
- “选择性遗忘比 always/never 更灵活”。

论文贡献必须进一步给出：可观测机制、方法、风险/资源约束、held-out 验证、失败边界和 go/no-go。

## 7. 下一阶段投入闭环

### A. OOD forgetting：优先烧 token

- 先生成新 seed、零重叠的五语言集合；
- 比较 never、always、当前 frozen selector、canonicalization、multilingual/OOD gate；
- 报 underforget、overdelete、worst-language、risk@coverage、calls/tokens；
- GO：相对 always 节省≥30% calls，总体差≤5pp，最坏语言差≤10pp，overdelete 不升高。

### B. Metadata linkability：第二优先烧 token

- raw identity、stable typed、session-rotating typed alias、opaque + task-gated reveal 四臂；
- 同时测 exact recovery、attribute inference、cross-session link、三类 utility 和 tokens；
- GO：linkability 至少降低20pp，utility 损失≤3pp，并能在需要身份连续性的任务上恢复效用。

### C. Annotation fidelity：先做数据，不先烧 token

- 收集真实 agent traces 并进行双人盲标；
- 先测 dependency/type annotation 的 precision/recall 与 validator FPR/FNR；
- 真实 FPR≤10% 才启动 CWL/recency/fallback 的大矩阵。

### D. Lifecycle：先复现强近邻，不直接造方法

- 先接入 DeltaMem、MemCon、Memory-R1、Infini Memory 的 released code；
- 统一记录 write/extract/consolidate/retrieve/answer/sidecar；
- 操纵 update density、query reuse、history length、cache regime；
- 只有发现现有方法在稳定 workload 区域被支配，才提出新 scheduler。

### E. MemTrace：低成本立即补严谨性

- 4 cases × 5 repeats × baseline/placebo/correct replacement/matched deletion/irrelevant replacement；
- 先估计生成噪声和 compression contribution，再决定是否扩20例。

## 8. 证据边界

- 精确复现仅用于 Lethe deterministic headline；
- Engram 与 TokenPilot 的“一致”指 released artifact/aggregate 重算一致；
- 其余真实调用多数为 substitute-stack validation，不能写成论文原模型精确复现；
- 没有新数据生成器时，不用旧样本冒充确认性外部验证；
- raw prompts/responses 和本地代理凭据未进入公开仓库；
- 正式论文前仍需完成 related-work collision audit、外部数据与跨模型确认。

**本周最终判断**：作为 weekly report 已充分，而且五线确认实验已经把“候选想法”推进到有 GO/NO-GO 的研究决策。最合理的下一步不是平均扩所有 baseline：优先把 token 投向 minimum-sufficient identity continuity 与 MemTrace 外部扩展；Lethe 只做 candidate-first redesign；Lifecycle 先复现增益稀疏性；Annotation 在 observable 资格门通过前停止模型调用。
