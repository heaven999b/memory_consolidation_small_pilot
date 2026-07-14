# Research Proposal(IdeaSpark 方法产出)· 2026-07-11

> 用 microsoft/ResearchStudio 的 **IdeaSpark** 方法(证据接地→瓶颈诊断→15-pattern 选择→候选生成→撞车审计→idea card)手动驱动;pattern 命中 `controlled_diagnostic_design`(主)+ `assumption_audit_and_pivot`(副)。证据来自本项目前序真实文献 survey + MemEvoBench(2604.15774)全文精读 + 本项目实测。

---

## Title
**Relation-Blind: A Controlled Diagnostic Showing Memory-Faithfulness Evaluators Miss Consolidation-Induced Role/Relation Misbinding — and How Much Benchmarks Overstate Faithfulness Because of It**

## Hook(瓶颈,Phase 1)
LLM-agent 记忆压缩(递归摘要固化)的安全/幻觉研究,全都依赖一把**测量记忆保真度的尺子**——但这把尺子(词法重叠 NLI、SummaC、乃至 HaluMem/MemEvoBench 的 LLM-judge)对**跨句关系/角色误绑**(surname→middle-name、agent↔patient、possessor 错位)**系统性失明**:只要错误的填充词在原文出现过,就判"支持"。**后果**:①"固化保真""benchmark accuracy=X"这类结论**建在一把测不到压缩最可能引入的那类错误的尺子上**;②MemEvoBench 这类新工作**只审注入的污染、从不审自己的 judge**。这是一个**承重假设被违反**的测量缺陷,不是"再堆一个 benchmark"能解决的。

## Core mechanism(Phase 2.2)
一个**关系结构化的诊断工具 + 三层审计**,把"关系保真"从"词法重叠"这个混淆里隔离出来(pattern: confound-isolating diagnostic):

1. **最小对探针套件(隔离混淆)**:从 LoCoMo/HaluMem 真实多轮对话取真源句,施加**保词面重叠**的类型化关系腐蚀(FRANK 分类学:EntE/CircE/CorefE/**PredE 关系重标 / RoleE 施受互换**),每个错误的填充词都刻意在原文出现过——这样**唯一变化的是关系是否正确**,词法信号恒定。~600-800 对,含**跨句消歧困难子类**(定义句与误绑句相隔 ≥2 句,人工核金标)。
2. **逐检测器 × 逐错型召回矩阵**:DeBERTa-MNLI / SummaC / MiniCheck / SRLScore / KG-triple / GPT-judge,报 per-(detector,error-type) recall + 词法-overlap MLP 消融确认根因。
3. **benchmark 通胀量化(pattern: audit-the-assumption)**:把上述关系敏感 checker 打到 **HaluMem 关系槽 + MemEvoBench 构造条目**上,vs 其原生 judge,报"faithfulness 被高估 X 个点、方向恒为 false-SAFE"。
4. **压缩深度轴(记忆压缩原生)**:用可跑任意深度的 C^N 固化 harness,在 N=0..8 × 3 个真算子(faithful/lossy-abstractive/lossy-eventful)上,测**关系保真度随压缩深度的曲线**,并对每个 (N,算子) 重算检测器召回——回答"压缩是否引入关系误绑、以及是否越压越测不到"。

## Falsification prediction(Phase 2.2 kill-switch,非平凡负控)
**最小实验**:在 §1 探针的 PredE/RoleE 子类上,同时跑 vanilla NLI 判定与关系结构化 checker。**主指标+方向**:关系结构化 checker 在这两类上的 recall **显著高于** NLI(预期 NLI≈0.5、checker≥0.8)。**唯一承重变量**:`filler_lexical_overlap`(错误填充词是否在源出现)。**非平凡负控**:对**同一批错误**,把填充词换成**源中不出现**的词(去掉词法重叠)——预测 **NLI 的 recall 会跳回到 checker 水平(≈1.0),两者差消失**;若差不消失,则盲区根因不是词法重叠、整个诊断的因果解释被证伪。(本项目已在 8 对小样本上预观测到这个翻转:overlap→NLI recall 0/8、no-overlap→8/8——正式化即主结果。)

## Compute budget(user-relative)
单台 M1 + 少量 API。本地 NLI/SummaC 走 CPU(MPS 在长前提会挂,已知);MiniCheck/关系 checker 若用 LLM 分解走 gpt-4.1-mini/deepseek ~$20-60;探针构造 + HaluMem 关系子集人工金标(先去重再抽样、报 κ)~2-3 人日。**全程 < $100 + 几天**。无 GPU 训练。

## Gap closure(Phase 2.2)
| 缺口 | 主 pattern | 怎么闭 |
|---|---|---|
| 测量被词法重叠混淆,关系保真测不到 | `controlled_diagnostic_design` | 保词面重叠的最小对隔离"关系对错"这唯一变量 |
| "benchmark judge 测的是 faithfulness"这一承重假设对关系错失效 | `assumption_audit_and_pivot` | 把关系 checker 打到 HaluMem/MemEvoBench judge 上,量化 false-SAFE 通胀 |
| 压缩是否内生关系误绑、随深度如何 | (diagnostic × 压缩深度轴) | C^N × 算子 sweep 上的关系保真曲线 |

## Differentiation from prior work(Phase 3 撞车审计后)
- **HANS(2019)**:单句合成 NLI,非跨句、非记忆、非现代检测器。
- **FRANK(2021)**:有 PredE/EntE 分类,但**无现代(2025-26)检测器逐类别召回**,非多轮记忆。
- **Reefknot**:关系幻觉,但**视觉/VLM**,非文本记忆。
- **FaithLens / 2411.16638**:显示检测器依赖表面特征,但**只在聚合层、明确把细粒度分类留给 future work**。
- **MemEvoBench(2604.15774)**:注入"omitted caveat"污染 + 3 轮 + GPT-5.2 judge——**假设污染是注入的、从不审自己 judge 的盲区、只有 3 轮**。本提案正补其三缺口:污染是否**压缩内生**、judge 是否**对关系错盲**、**深压缩**长程。
- **HaluMem**:关系记忆槽用词法/LLM judge,自认"同义/轻改写可接受"——正是掩盖机制,从未被审计。
> **almost-prior + missed step**:最接近的是 FaithLens(证了表面特征依赖),它漏掉的一步 = **按错误类别拆解召回 + 落到关系/角色这一具体盲类 + 量化它导致的 benchmark 通胀**。

## Reviewer concerns & responses(Phase 3.2 五检)
1. **"这不就是已知的 NLI 不 robust?"**(anti-pattern: 重述常识)→ 反驳:承重贡献不是"NLI 不 robust",是**逐类别召回矩阵 + 关系/角色这一具体盲类 + 由它造成的已发表 benchmark 通胀点数**,且有非平凡负控证因果。这是 FRANK/FaithLens 明确留白处。
2. **"关系 checker(SRL/triple)会不会在第一人称会话上退化,反而不 work?"**(recipe application)→ 诚实纳入:把"SRL 在 'My name is X' 上退化、naive fix 也救不了"作为**可报的子结果**(预注册),而非假设 checker 必胜。
3. **"benchmark 通胀数字会不会是标注伪影?"**(falsification structure)→ 关系子集**先去重再抽样、报 κ 与 IAA**(本项目标注纪律);通胀方向(false-SAFE)由负控锚定。
4. **paper-pointed threat**:最强竞争者 = FaithLens 家族;`parametric_family_concern` = "QA-based faithfulness(QAGS/QuestEval)可能已含关系敏感性"——**正式开工前须 scoop-check 这一族**,划清"逐类别 memory 召回矩阵"未被覆盖的边界。
5. **hard-floor 检查**:无触发 reject-lesson、无 exact-mechanism 撞车(关系敏感 memory-faithfulness 逐类别审计 + 压缩深度轴未见同款)→ **verdict: advance**(带上面 concerns 进 card)。

## 一句话(为什么这是下注)
它把本项目**唯一活着的资产(检测器对关系造假盲)**升级成一个**测量方法学论文**:不追已死的"固化很危险",而是证明"**测'固化危不危险'的尺子本身对关系错是瞎的,所以现有'保真'结论未经验证**";compute 近乎零、撞车风险低、且直接与 2026 新工作(MemEvoBench/HaluMem)对话。压缩深度轴让它同时是"记忆压缩"原生问题,不只是通用 NLI 批判。

---

### 附:IdeaSpark 运行说明(诚实)
工具已 clone(MIT)、依赖已装;其 `check_connectors`/连接器子进程在本机对 `scripts.*` 包的 PYTHONPATH 透传有 bug(`ModuleNotFoundError: scripts._time_guard`),未跑通自动检索。故按工具设计("host LLM 可内联处理 LLM 阶段")**手动驱动其方法**:真实 pattern 卡片 + 阶段 prompt + 输出 schema + 五检审计,证据用本项目前序真实 survey + MemEvoBench 全文。若要完全自动化,需修连接器 PYTHONPATH(在 `scripts/run.py` 的 connector subprocess 调用处注入 `env=PYTHONPATH=skill_root`)后 `run.py next` 一键跑。
