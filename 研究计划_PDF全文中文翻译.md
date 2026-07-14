# 安全与幻觉:迭代记忆固化的可复现研究计划(全文中文翻译)

> 原文:Reproducible Research Plan for Safety and Hallucination in Iterative Memory Consolidation
> 版本:v2 —— 定向修订(实现底座、benchmark 顺序、具体实验)
> 说明:这是原 PDF 的完整中文翻译。专有名词(TierMem、HaluMem 等)保留英文原名。

---

## 一句话决定

把 **TierMem 作为主要的开源实现底座**;把《Language Models Need Sleep》仅作为**概念动机**;把 **HaluMem 作为主要的幻觉 benchmark**;用 **MPBench + MemEvoBench + AgentPoison** 来定义安全攻击套件。

这不是对原计划的完全重写,而是一次**外科手术式的 v2**:benchmark、指标、统计、交付物这几节基本保持不变,但把项目从"一个泛泛的记忆压缩研究"改成"一个具体、可搭建的、以 TierMem 为底座的研究"。

## 相比 v1 改了什么

| 方面 | 旧框架 | v2 改动 |
|---|---|---|
| **底座系统** | 没有明确抬高某个代码库;TierMem 主要被当成防御灵感 | 把 TierMem 作为主 fork 和实验框架。在它的摘要层加迭代固化 |
| **《Need Sleep》的角色** | 固化深度 N 的概念来源 | 只当动机。不作为可复现底座(没有可用代码发布) |
| **安全论文** | MPBench、MemEvoBench 在基础表里很突出 | 作为威胁模型和指标参考。实验在 TierMem 框架里实现 |
| **幻觉 benchmark** | HaluMem 已经是核心 | 把 HaluMem-Medium 作为第一个 pilot benchmark,HaluMem-Long 作为最终压力 benchmark |
| **fork 顺序** | HaluMem、LongMemEval 排在 TierMem 前面 | 先 fork TierMem,再接 HaluMem/LongMemEval/LoCoMo 的 loader 和 AgentPoison overlay |

## 保持不变的部分

- **两条主线结构**:安全持久性/放大,以及幻觉累积。
- **固化调度 N ∈ {0, 1, 2, 4, 8, 16}**。
- **主要指标**:SRR、UAF、RTR@k、不安全回答率、无支撑新记忆率、传播到答案率,以及 HaluMem 分阶段得分。
- **统计计划**:配对的逐条比较、随 N 的趋势检验、可行时用混合效应逻辑回归、bootstrap 置信区间、Holm-Bonferroni 校正。
- **效用检查**:LongMemEval、LoCoMo、MemoryAgentBench、延迟/token 成本,以及"效用—过度过滤"的前沿。

---

## 1. 修订后的基础决定

最重要的修订,是把**概念动机、实现底座、benchmark 骨架、攻击/防御参考**分开。这消除了"到底该 fork 和搭建什么"的模糊。

| 在本项目中的角色 | 论文 / 仓库 | 这样用 |
|---|---|---|
| 概念动机 | Language Models Need Sleep | 用"睡眠深度"这个想法来论证为什么要改变固化次数 N。不依赖它的代码 |
| **主实现底座** | **TierMem**(FreedomIntelligence/Tiermem) | **先 fork**。在摘要层加迭代固化,同时保留它不可变的原始日志层、provenance 链接、原始证据升级 |
| 主幻觉 benchmark | HaluMem | 用 HaluMem-Medium 做 pilot,HaluMem-Long 做压力测试。保留它的抽取/更新/QA 分解 |
| 安全威胁模型参考 | MPBench、MemEvoBench | 复用它们的攻击分类法、记忆投毒持久性框架、多轮漂移设置、写入/检索成功指标。不作为主代码库,除非确认其公开产物够用 |
| 后门 overlay | AgentPoison | 用触发词/查询投毒,测试压缩是否会移除、保留、或语义"洗白"攻击触发 |
| 良性效用 benchmark | LongMemEval、LoCoMo | 用来确保防御不破坏长期召回、时间推理、更新、弃权、事件结构 |
| 压缩基线 | COMEDY、Context-Memory、EMem | 作为替代的固化算子。当作方法基线,不作为主评估底座 |
| 可选扩展 | LongMemEval-V2、MemoryAgentBench | 核心结果稳定后再用,尤其是环境经验记忆和能力压力测试 |

**底线:底座论文/代码库应该是 TierMem。其他一切都插进以 TierMem 为中心的实验框架。**

### 为什么 TierMem 是对的底座

- 它已经匹配你想要的防御:紧凑摘要 + 不可变的原始情景存储。
- 它给了因果变量 N 一个自然的落点:只对摘要层递归固化,原始证据保持不变。
- 它支持最重要的审计问题:不安全或无支撑的声明,是在**写入、固化、检索、还是生成答案**时进入的?
- 它让你能比较"只用摘要""只用原始""摘要+原始升级"三种,而不用从零搭建所有记忆基础设施。

### 不要做什么

不要直接复现《Language Models Need Sleep》——把它当成"研究固化深度"的理由,不是工程底座。也不要把 MPBench 或 MemEvoBench 当核心框架,除非确认它们的公开产物覆盖你需要的完整实验;它们的主要价值是安全分类法和多轮漂移框架。

---

## 2. 修订后的 benchmark 使用计划

之前的 benchmark 栈仍然有效,但顺序要改,好让第一个能跑的系统就是 TierMem 底座的。

| 阶段 | 主 benchmark/数据 | 目标 | 先跑? |
|---|---|---|---|
| **E0 — 基线 sanity** | TierMem 原生支持的 benchmark,然后 LongMemEval-S 和 LoCoMo 小子集 | 验证 fork、检索、原始日志升级、provenance 格式、逐条产物记录 | 是 |
| **E1 — 幻觉 N-sweep** | HaluMem-Medium | 测量重复固化是否增加抽取幻觉、更新错误、无支撑记忆、以及传播进 QA | 是 |
| **E2 — 良性效用** | LongMemEval-S 清洗版;LoCoMo 已发布对话 | 检查固化和防御是否保留召回、更新、时间推理、弃权、事件结构 | 是 |
| **E3 — 安全持久性** | LongMemEval-S 或 LoCoMo 上的 AgentPoison overlay;MPBench/MemEvoBench 式自定义攻击 | 测量不安全写入率、安全保留率、检索触发率、不安全下游回答率 | 是 |
| **E4 — 压缩家族** | HaluMem-Medium + LongMemEval-S | 比较抽象摘要、命题抽取、COMEDY 式压缩、Context-Memory、TierMem 式分层 | E1-E3 之后 |
| **E5 — 压力** | HaluMem-Long;LongMemEval-V2 小/中;MemoryAgentBench | 把最强配置扩到长上下文、噪声轨迹、更广的记忆体能力 | 最后 |

### 推荐的最小 pilot

1. Fork TierMem,跑一个 TierMem 原生或支持的评估,确认环境。
2. 在摘要层实现 Cᴺ,N ∈ {0, 1, 2, 4, 8};在流程稳定前跳过 N=16。
3. 在 HaluMem-Medium 上跑"只摘要"vs"TierMem 式摘要+原始升级"。
4. 加一个小的 AgentPoison overlay 和 100 条自定义压缩投毒案例。
5. 报一张 pilot 表:幻觉率、不安全记忆保留、良性 QA 准确率、token/延迟成本。

这个 pilot 足以在花大算力跑 HaluMem-Long 或 LongMemEval-V2 之前,判断这篇论文有没有真信号。

---

## 3. 修订后的研究问题与假设

自变量是 **N(固化次数)**。因变量是安全持久性、幻觉累积、良性效用、成本。

| 问题 | 假设 | 主要证据 |
|---|---|---|
| **RQ1**:递归固化是保留还是放大不安全内容? | 在只摘要的记忆里,不安全的种子命题和可触发的毒素会随 N 增大而持续或被语义洗白 | SRR(N)、UAF(N)、RTR@k(N)、不安全下游回答/动作率 |
| **RQ2**:迭代固化会创造假记忆吗? | HaluMem 抽取/更新错误先增加;无支撑记忆随后传播进 QA | HaluMem 分阶段得分、无支撑新记忆率、冲突合并率、传播到答案率 |
| **RQ3**:provenance 感知的分层能打断失败链吗? | TierMem 式原始证据升级降低不安全/幻觉传播,同时保留大部分效用和成本节省 | 风险降低 vs 效用损失;良性准确率 vs 不安全保留的 Pareto 前沿 |
| **RQ4**:哪个固化算子最脆? | 抽象的"摘要的摘要"风险斜率最陡;命题/provenance 门控方法斜率更平 | 压缩家族 × 防御的热力图;风险指标随 N 的斜率 |
| **RQ5**:失败发生在哪? | 失败分为写入时、固化时、检索时、回答时;正确的防御取决于错误最先出现在哪 | 逐条产物轨迹和阶段标签 |

### 新颖性陈述

可发表的贡献不是"记忆压缩有风险"这么简单。更锐利的主张是:**递归固化深度是一个可测量的因果变量,它改变记忆体的安全与幻觉画像;而 provenance 感知的分层能把这条风险曲线压平,又不完全放弃压缩收益。**

### 预期的主结果模式

- **只用原始**的记忆应该最忠实但最贵。
- **只用摘要**的记忆应该最便宜,但随 N 增大风险斜率最大。
- **TierMem 式"摘要+原始升级"**应该通过把无支撑或安全关键的声明逼回原始证据来降低风险。
- **只用分类器的写入过滤**应该有帮助,但不能完全解决压缩投毒或语义洗白。

---

## 4. 以 TierMem 为中心的实验架构

原始存储在多次固化中**永不改变**;只有紧凑层被递归重写。这让失败能归因到"固化",而不是"证据变了"。

| 步骤 | 组件 | 记录什么 |
|---|---|---|
| 1 | 原始摄入 | 原始对话/工具/文档片段、来源类型、session id、时间戳、信任分 |
| 2 | 写入路径守卫 | 提示注入分、安全分、隔离决定、原因 |
| 3 | 不可变原始情景存储 | 完整原始片段和稳定的来源 id。这是真值证据库 |
| 4 | 初始紧凑记忆 | 候选摘要/命题、支撑来源 id、置信度、矛盾标记 |
| 5 | 迭代固化器 Cᴺ | 每个 N 之后的紧凑记忆;被丢弃的声明;被合并的声明;新编造的声明;provenance 链接 |
| 6 | 检索器和充分性路由 | top-k 紧凑记忆、原始升级决定、需要时检索的原始证据 |
| 7 | 阅读器模型 | 答案、引用的记忆 id、引用的原始片段、弃权标记、**判定标签(judge label)** |

### 文字版流程

原始轨迹 → 写入过滤 → 不可变原始库 + 紧凑层 → Cᴺ 固化 → 检索 → 充分性路由 → 需要时升级到原始 → 带证据轨迹的答案

### 固化定义

对每个记忆分片 m,定义 C(m) 为在固定 token 预算下重写/合并/压缩紧凑记忆的一次固化。Cᴺ(m) 是重复 N 次。在不同 N 之间,保持 prompt、预算、检索 top-k、模型温度不变。N ∈ {0,1,2,4,8,16};N=0 表示只用原始或不固化(取决于基线)。

**关键控制**:在 TierMem 条件下,原始证据固定、每个 N 都可升级取用。在只摘要条件下,回答者只看紧凑记忆。这个对比正是用来识别"provenance 感知的原始兜底"的价值。

---

## 5. 要跑的实验(修订)

| 实验 | 设计 | 主要比较 | 成功标准 |
|---|---|---|---|
| **E0 — TierMem 集成 sanity** | 在小 LongMemEval/LoCoMo 子集上,用原始库、摘要层、provenance 链接跑 TierMem 式检索 | 只原始 vs 只摘要 vs 摘要+原始升级,在 N=0 和 N=1 | 产物完整,良性 QA 在所选模型的预期范围内 |
| **E1 — HaluMem 递归幻觉** | 对 HaluMem-Medium 记忆历史应用 Cᴺ,分别评估抽取、更新、QA | 只摘要 vs TierMem 式升级;N ∈ {0,1,2,4,8,16} | 报告单调或非单调风险曲线,并定位第一个失败阶段 |
| **E2 — 安全持久与洗白** | 在固化前注入不安全种子命题、政策倾斜记忆、AgentPoison 式触发 | 无过滤只摘要 vs 分类器过滤 vs provenance 门控 TierMem | 测量不安全内容是否存活、改写、被检索、改变下游答案 |
| **E3 — 冲突与更新漂移** | 用 HaluMem 更新案例 + LongMemEval 知识更新/时间条目(含矛盾事实) | 旧事实保留 vs 正确覆写 vs 不连贯合并 | 显示 Cᴺ 是否增加冲突合并率,以及原始升级能否修复 |
| **E4 — 防御消融** | 逐个加防御:只分类器、来源信任评分、provenance 必需固化、保守压缩、不确定性感知写入门 | 每个防御 vs 同样例子上匹配的无过滤跑 | 至少 25% 相对风险降低,且 LongMemEval-S 上效用损失不超过 3 个百分点 |
| **E5 — 最终压力** | 在 HaluMem-Long、LoCoMo 完整发布、可选 LongMemEval-V2 小/中上跑最强和最弱设置 | 最好的两个防御 vs 只摘要和只原始 | 在长上下文、干扰项、噪声环境历史下展示普适性 |

### 消融矩阵

| 轴 | 取值 |
|---|---|
| 记忆架构 | 滑动窗口;只原始;只摘要;TierMem 摘要+原始;COMEDY 式压缩;Context-Memory(可选) |
| 固化深度 | N = 0, 1, 2, 4, 8, 16 |
| 防御 | 无;只分类器;来源信任评分;provenance 必需;保守压缩;不确定性感知写入门 |
| 攻击家族 | 压缩投毒;后门触发;噪声工具输出;偏见反馈;不安全内容存活;冲突更新 |
| Benchmark | HaluMem-Medium 优先;LongMemEval-S;LoCoMo;HaluMem-Long;LongMemEval-V2(可选) |

---

## 6. 指标与决策规则 —— 保留,但收紧

指标基本不变。修订是把每个指标明确绑到 TierMem 流程的某个阶段,好归因失败。

| 指标 | 定义 | 诊断的阶段 |
|---|---|---|
| SRR(N) | 固化 N 次后存活的不安全种子命题 / 注入的不安全种子命题 | 写入 + 固化 |
| UAF(N) | 固化后不安全或政策倾斜的命题 / 不安全种子 | 固化放大 |
| RTR@k(N) | 触发查询下,被投毒记忆进入 top-k 的概率 | 检索 |
| 不安全回答/动作率 | 顺从或依赖不安全记忆的下游输出比例 | 阅读器行为 |
| UNMR(N) | 缺乏来源支撑的新固化记忆语句 / 所有新固化语句 | 固化幻觉 |
| 冲突合并率 | 矛盾事实被合并成一条错误记忆(而非被解决或弃权) | 更新处理 |
| PAR(N) | 无支撑记忆被引用或用于最终答案的概率 | 传播到答案 |
| **良性效用** | **LongMemEval exact/F1/弃权、LoCoMo QA/摘要、MemoryAgentBench 能力分** | 过度过滤与有用性 |

### 主要统计检验

- **主 H1 检验**:无过滤只摘要记忆中,SRR(N) 或不安全下游回答率随 N 的趋势。
- **主 H2 检验**:无过滤只摘要记忆中,HaluMem 更新/QA 幻觉率随 N 的趋势。
- **防御检验**:每个防御 vs 同样例子上匹配的无过滤跑,二值端点用 McNemar 检验,率用 bootstrap 置信区间。
- **主报告阈值**:alpha = 0.01,对预注册的主要端点用 Holm-Bonferroni 校正。
- **决策规则**:只有当防御把主风险指标相对降低至少 25%、且 LongMemEval-S 上良性效用损失在 3 个绝对百分点内,才称它"有希望"。

### 解读护栏

如果风险没有随 N 增加,**不要**就此断定迭代固化是安全的。先检查:回答者是不是偷偷依赖了原始证据?摘要预算是不是太宽?攻击是不是根本没进紧凑层?在放弃假设前,用更紧的预算重跑只摘要。

---

## 7. 更新后的实现蓝图

fork 顺序要改。先 fork 基础记忆架构,再接 benchmark loader 和攻击 overlay。

| 顺序 | 仓库 | 用途 |
|---|---|---|
| 1 | FreedomIntelligence/Tiermem | 主记忆架构。加 Cᴺ、provenance 门控、充分性路由日志、产物序列化 |
| 2 | MemTensor/HaluMem | 主幻觉 benchmark。加一个通过 TierMem adapter 读写的 runner |
| 3 | xiaowu0162/longmemeval | 良性记忆 QA、更新、时间推理、弃权 |
| 4 | snap-research/locomo | 长对话 QA、事件摘要、时间/事件结构检查 |
| 5 | AI-secure/AgentPoison | 后门触发生成和投毒场景 |
| 6 | nuochenpku/COMEDY | 压缩基线 |
| 7 | snu-mllab/context-memory | 可选的向量/KV 压缩基线 |
| 8 | HUST-AI-HYZ/MemoryAgentBench | 次要的记忆体能力评估 |

### 每条目要序列化的产物

- 原始输入片段、信任标签、唯一来源 id;
- 过滤前的候选记忆写入;
- 过滤分和隔离决定;
- 每个固化深度 N 之后的紧凑记忆;
- 紧凑声明到原始片段的 provenance 链接;
- 检索到的紧凑记忆和原始升级;
- 最终答案、引用证据、判定标签、错误类别。

---

## 8. 防御设计 —— 细化成可实现的门

| 防御 | 用在哪 | 防住什么 | 预期弱点 |
|---|---|---|---|
| 只分类器写入过滤 | 紧凑记忆写入前 | 明显的提示注入、不安全指令、逐字写入的不安全内容 | 可能漏掉语义洗白和看似良性的政策倾斜 |
| 来源信任评分 | 提升到紧凑层前 | 低信任的工具/检索文本覆盖高信任的用户/工具状态 | 需要精心定义信任层级 |
| provenance 必需固化 | Cᴺ 期间 | 无支撑声明和幻觉摘要事实 | 可能丢掉缺乏干净来源片段的有用抽象 |
| 保守压缩 | 写入和固化期间 | 对安全关键字段的抽象改写 | 可能增加存储、降低压缩收益 |
| 不确定性感知写入门 | 写回和回答前 | 错误的冲突解决和过早覆写 | 需要置信度校准或一个**判卷模型(judge model)** |

### 建议作为你自己贡献的防御

最强的新颖防御是 **provenance 感知的迭代固化**:每个紧凑记忆句子都必须有原始片段支撑;每次改写都必须保留或明确更新 provenance;任何依赖无支撑紧凑记忆的答案,都必须**升级到原始证据或弃权**。这是 TierMem 的自然扩展,但具体贡献在于——在重复 Cᴺ 固化和对抗/噪声记忆更新下测试它。

### 安全关键字段

对于偏好、医疗或法律约束、凭证、工具流程、截止日期、政策、动作权限,以及任何被归类为不安全或对抗性的内容,**禁止自由形式的抽象改写**。把它们存成抽取式片段或带明确来源 id 和矛盾状态的类型化命题。

---

## 9. 修订后的时间线与交付物

这版时间线比 v1 更短、更以实现为先。假设一个有动力的单人研究者或小团队,有一个 7B-9B 阅读器模型、一个 embedding 模型、一个安全分类器。

| 周 | 目标 | 具体交付物 |
|---|---|---|
| **1** | Fork TierMem,搭公共记忆 API | 能在极小合成集上跑"只原始、只摘要、TierMem 式摘要+原始";产物 schema 定稿 |
| **2** | 接 HaluMem-Medium 和 LongMemEval-S | 第一个 N-sweep,N ∈ {0,1,2,4,8};暂无攻击;分阶段幻觉表 |
| **3** | 加 AgentPoison overlay 和自定义压缩投毒 | 每个家族 100 条攻击的安全 pilot;SRR/UAF/RTR@k 看板 |
| **4** | 防御消融 | 只分类器、来源信任、provenance 必需、保守压缩、不确定性门,在匹配例子上比较 |
| **5** | 效用和压力 benchmark | LoCoMo 跑;HaluMem-Long 子集;算力允许则 LongMemEval-V2 小 |
| **6** | 统计和论文图 | 风险-N 折线图、HaluMem 分阶段柱状图、Pareto 前沿、两个 provenance 案例研究 |

### 最终交付物

- 一个围绕 TierMem adapter 和 benchmark loader 搭建的公开代码库。
- 每个架构、防御、模型、benchmark、N 值的固定配置(pinned configs)。
- 逐条 JSONL 产物:原始写入、每个 N 之后的紧凑记忆、检索证据、答案、判卷输出。
- 所有指标的 CSV 汇总和 bootstrap 置信区间。
- 一个简短附录:精确 prompt、分块规则、信任分规则、安全过滤阈值、commit hash。

### 停/继续规则(Stop/go)

只有在 pilot 发现以下之一时才继续做完整实验:(a) 只摘要记忆中,幻觉或安全风险随 N 有非平凡的正斜率;或 (b) 只摘要与 provenance 版之间在同一 N 下有明显的风险差距。若两者都没出现,先收紧压缩预算重跑,再改假设。

---

## 10. 替换原计划的文字

(如果你想给原 21 页计划打补丁而不全重写,用以下直接替换。)

**基础框架替换为**:主底座是 TierMem。《Language Models Need Sleep》只是概念动机。MPBench 和 MemEvoBench 定义安全威胁模型,HaluMem 是主幻觉 benchmark,LongMemEval/LoCoMo 是效用检查,AgentPoison 提供基于触发的投毒,COMEDY/Context-Memory 是压缩基线。

**fork 顺序替换为**:1. TierMem;2. HaluMem;3. LongMemEval;4. LoCoMo;5. AgentPoison;6. COMEDY;7. Context-Memory;8. MemoryAgentBench。

**主贡献陈述**:我们引入"迭代固化深度"作为记忆体安全与幻觉的因果实验变量。我们展示不安全或无支撑记忆如何随 N 增大而持续、放大、或传播,并测试 provenance 感知分层能否在不牺牲良性长期记忆效用的前提下降低这一风险。

---

## 11. 来源清单

| ID | 来源 | URL |
|---|---|---|
| S1 | Language Models Need Sleep | arxiv.org/abs/2605.26099 |
| S2 | TierMem - From Lossy to Verified | arxiv.org/abs/2602.17913;github.com/FreedomIntelligence/Tiermem |
| S3 | HaluMem | arxiv.org/abs/2511.03506;github.com/MemTensor/HaluMem |
| S4 | MPBench | arxiv.org/abs/2606.04329 |
| S5 | MemEvoBench | arxiv.org/abs/2604.15774 |
| S6 | LongMemEval | arxiv.org/abs/2410.10813;github.com/xiaowu0162/longmemeval |
| S7 | LoCoMo | arxiv.org/abs/2402.17753;github.com/snap-research/locomo |
| S8 | AgentPoison | arxiv.org/abs/2407.12784;github.com/AI-secure/AgentPoison |
| S9 | COMEDY | arxiv.org/abs/2402.11975;github.com/nuochenpku/COMEDY |
| S10 | Context-Memory | arxiv.org/abs/2312.03414;github.com/snu-mllab/context-memory |
| S11 | MemoryAgentBench | arxiv.org/abs/2507.05257;github.com/HUST-AI-HYZ/MemoryAgentBench |
| S12 | LongMemEval-V2 | arxiv.org/abs/2605.12493;github.com/xiaowu0162/LongMemEval-V2 |

### 最终推荐论文标题

**When Memory Agents Sleep: Safety Retention and Hallucination Accumulation in Iterative Memory Consolidation**
(当记忆体睡眠:迭代记忆固化中的安全保留与幻觉累积)
