# 下一阶段投入决策 · Token、方法与数据优先级

**日期：2026-07-28**

## 0. 决策摘要

当前不应平均扩大所有实验。最合理的资源配置是：

1. **优先烧 token**：OOD-aware persistent-memory forgetting；
2. **第二优先烧 token**：cross-session linkability 下的 minimum-sufficient metadata；
3. **先做数据再烧 token**：annotation-fidelity-aware eviction；
4. **先复现强近邻再决定方法**：full-lifecycle maintenance benchmark；
5. **小成本立即补**：MemTrace variance-aware causal gate；
6. **停止**：generic controller、普通 retrieval router、继续扫摘要长度、旧 cross-lingual 集上调规则。

所有估算均指已授权本地代理或离线计算；不构成对任何官方按量付费 API 的授权。

## 1. 总体投入表

| Direction | 现有证据 | 新颖性空间 | 下一硬缺口 | 应投入什么 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| OOD-aware selective forgetting | external305 强 Pareto；跨语言明确崩点 | persistent-memory mutation 的非对称风险、worst-group、risk@coverage | 新 seed 多语言外部集 | 数据生成 + 方法 + 中等规模模型调用 | P0 |
| Minimum-sufficient metadata | 48-source controls；跨模型 type/link 通道 | session-rotating alias、task-gated reveal、identity continuity | 新表示方法尚未实现 | 方法实现 + 攻击/utility矩阵 | P0/P1 |
| Annotation-fidelity eviction | 2,400 synthetic cases；噪声反转 | 真实 annotation error 与 confidence-aware fallback | 真实 traces 双盲标签 | 数据/人工审计优先 | P1 |
| Full-lifecycle maintenance | Engram/Supersede/TokenPilot/Agent-Native 跨论文证据 | 统一 TCO、write amplification、workload phase diagram | 强近邻 DeltaMem/MemCon 等未统一跑 | baseline integration + ledger | P1 |
| MemTrace causal replay | 初步 placebo/length 混杂 | 记忆收益的因果识别协议 | 重复运行与 matched controls | 小规模模型调用 | P0 小任务 |
| Representation fallback | Engram failure seed | 仅 certificate/provenance 版本尚有空间 | 普通 router 已高度撞题 | 暂缓 | P2 |

## 2. P0-A：OOD-aware persistent-memory forgetting

### 为什么值得投入

- 当前有最强 held-out 证据：external305、selector 锁定、与 calibration 零重叠；
- 已得到非平凡 Pareto：少 3.93pp，省 53.48% calls、59.29% tokens，0 over-delete；
- 已出现可研究的最坏组机制：cross-lingual 差 26.7pp；
- 现有 multilingual unlearning 多研究参数知识，和外部 persistent-memory mutation selector 仍有差异。

### Stage 0：数据资格门，不调用模型

- 五种语言/脚本，建议覆盖 Latin、CJK、Arabic、Cyrillic、Indic；
- 每种至少50 cases，总计约250；
- 使用新的实体、属性、数字和攻击模板；
- 与原385、前80和external305做文本 hash 与结构模板去重；
- 人工抽查语义等价、forget scope 与 scorer 可复算性。

未通过零重叠和质量抽查，不进入模型阶段。

### Stage 1：方法门

比较：

1. never hook；
2. always hook；
3. 当前 frozen selector；
4. Unicode/script canonicalization；
5. multilingual embedding selector；
6. OOD/risk-calibrated gate。

核心指标：underforget、overdelete、worst-language、risk@coverage、calls、tokens、p95 latency。

### 预计资源

- 数据构建：主要是离线与人工审计；
- 250-case 小矩阵：约 500–800 个有效 hook calls，规划量级约 0.6–1.5M 本地代理 tokens；
- 若过门扩500 cases：约 1.2–3M tokens；
- deterministic scorer 应尽量离线，避免给每个样本增加 judge 调用。

### Go / no-go

GO：相对 always，calls 至少降低30%；总体成功差≤5pp；最坏语言差≤10pp；overdelete 不升高。

NO-GO：为了控制最坏组风险必须路由接近100%；或 hook 本身在新语言上失败。

## 3. P0/P1-B：Minimum-sufficient metadata under linkability

### 为什么值得投入

MemPrivacy 已经占据 typed placeholder，因此我们的贡献不能是“类型替换保 utility”。真正的增量是区分：

- value secrecy；
- attribute inference；
- cross-session identity linkability；
- 需要身份连续性时的任务效用。

### 方法四臂

1. raw/stable identity；
2. stable typed placeholder；
3. session-rotating typed alias；
4. opaque session-local alias + task-gated reveal。

### 任务与攻击

- Basic memory / factual recall；
- temporal continuity；
- personalization；
- cross-session retrieval；
- exact value recovery；
- attribute inference；
- link attack with/without auxiliary knowledge。

### 预计资源

- 先复用48 source blocks；
- 48×4 arms=192 memory representations；
- 加三类攻击和三类 utility 后，预计约 600–1,000 个有效 observations；
- 规划量级约 1.5–3M 本地代理 tokens，具体取决于是否能使用确定性 scorer；
- 第一阶段只跑12 source blocks，过门后再扩48。

### Go / no-go

GO：相对 stable typed，cross-session link 至少下降20pp；平均 utility 损失≤3pp；在需要身份连续性的任务上，gated reveal 恢复至少80%的损失。

NO-GO：风险下降完全来自 utility 崩溃；或者 auxiliary knowledge 一加入，rotating alias 立即可链接。

## 4. P1-C：Annotation-fidelity-aware eviction

### 为什么不能先烧 token

Pi-CWL 的现有 sign reversal 来自 synthetic annotation noise。真实 agent trace 中，“单依赖”“缺 task link”等结构可能本来合法；如果 validator 在真实数据上高误报，扩大模型矩阵只会把 synthetic artifact 放大。

### 先做的数据门

- 采集约200段真实 agent/tool traces；
- 两名标注者独立标 task boundary、dependency、completion、reusable evidence；
- 仲裁分歧；
- 统计自动 annotation 与 validator 的 precision/recall/FPR/FNR；
- 按真实错误分布重新注入 noise，而不是继续使用均匀随机噪声。

### 进入模型阶段的条件

- validator FPR≤10%；
- 标注者 agreement 达到可接受水平；
- closure violation 与真实 downstream failure 有显著关联。

通过后再比较 CWL、recency、task-boundary、confidence fallback 和 learned policy。预计模型阶段约 0.5–1.5M tokens。

## 5. P1-D：Full-lifecycle maintenance benchmark

### 为什么不直接造 event-triggered controller

Memory-R1 已有操作策略；DeltaMem 已有 residual incremental memory；Infini Memory 已有 buffer/consolidation；MemCon 已控制 retrieve/consolidate/forget。直接再造 generic controller 的新颖性不足。

### 第一阶段：强近邻接入

- 克隆并冻结 DeltaMem、MemCon、Memory-R1、Infini Memory；
- 做 released smoke 与 scorer 对齐；
- 给每个系统加统一 sidecar ledger；
- 记录所有 write/extract/consolidate/retrieve/answer/retry/cache。

### 第二阶段：最小 workload grid

- 12 histories；
- update density：低/中/高；
- query reuse：1/3/6；
- history length：短/长；
- full context、periodic、各论文方法；
- 先用单模型栈过门，再换第二模型。

预计小矩阵约 2–5M 本地代理 tokens。只有发现方法排名发生稳定反转，才扩完整矩阵。

### 值得提出新方法的条件

- 至少一个跨数据/模型稳定区域，所有现有方法都被简单策略支配；或
- 现有方法因漏算 sidecar/write cost 从 Pareto 前沿退出；或
- update density/reuse 的可观测特征能稳定预测最优策略。

否则产出应定位为 benchmark/audit，而不是硬造方法。

## 6. P0 小任务：MemTrace variance-aware causal gate

### 立即可跑的矩阵

- 4 mechanically reconstructable cases；
- 5 repeats；
- baseline、identical-prompt placebo、correct replacement、length-matched deletion、irrelevant replacement；
- 共约100 calls，规划量级约 0.5–1M tokens。

### Go / no-go

GO：correct replacement 超过重复噪声95%带，并且比 matched deletion 多至少0.10 F1。

NO-GO：correct replacement 与 deletion/placebo 无法区分；则现有收益主要是 compression 或生成噪声。

它本身不一定是一篇论文，但能显著提高之后所有 memory causal claims 的可信度。

## 7. 如果有 10M 本地代理 token，应如何分配

| Direction | 建议比例 | 目的 |
| --- | ---: | --- |
| OOD selective forgetting | 40% | 新多语言外部集 + risk-calibrated gate |
| Minimum-sufficient metadata | 30% | 四臂方法和攻击/utility矩阵 |
| Lifecycle strong-baseline benchmark | 20% | DeltaMem/MemCon/Memory-R1/Infini 小矩阵 |
| MemTrace causal gate | 10% | 重复与 matched controls |

Annotation fidelity 在人工/真实标签门通过前，不从这10M中分配大规模模型预算。

## 8. 明确停止投入的项目

- 继续在旧38条 Lethe cross-lingual cases 上调 Unicode 规则；
- 再扫 Supersede 100/200/400 等摘要长度；
- 没有完整 sidecar 的 TokenPilot cost 扩展；
- 在当前 substitute LongMemEval chain 上从30盲目扩到更多 queries；
- Agent-Native 继续扩大同一10-case diagnostic，而不恢复论文数据/骨干；
- generic no-memory/retrieve/full-context router；
- 只把多个现有 memory modules 拼在一起；
- 在 synthetic Pi-CWL 上继续扩大到更多随机 cases，而不进入真实 traces；
- 任何没有 fresh seed / locked policy / held-out 的确认性主张。

## 9. 最终投入顺序

1. 立即完成 MemTrace 100-call causal gate；
2. 并行完成 Lethe 多语言新数据生成与零重叠审计；
3. 实现 metadata 四臂并先跑12-source gate；
4. 离线接入 DeltaMem/MemCon/Memory-R1/Infini Memory；
5. 开始真实 agent trace 的 dependency 双盲标注；
6. 只有各自通过资格门，才启动大规模 token 扩展。
