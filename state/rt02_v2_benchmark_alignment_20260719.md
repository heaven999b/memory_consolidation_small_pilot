# RT-02 v2 评估可靠性 & 公开 benchmark 对标审计 · 2026-07-19

> **目的**：逐个评估/架构组件映射到它对标的公开 benchmark 或论文，给出**可靠度评级**、偏离与风险、修复状态。回答"各种评估对标公开 benchmark/论文做得足够可靠吗"。
> **可靠度**：🟢 高（官方原样/领域标准）｜🟡 中（有偏离但已声明/有对照）｜🔴 需修（会误导，不能进主判据）。
> **口径声明**：项目内引用的部分 arXiv 编号（如 MemEvoBench `2604.15774`、TrustMem `2606.25161`）是未来日期、**本 AI 无法核验其真伪**；下表按"组件对标的公开 benchmark/论文族"评估方法学实质，NLI/记忆算子族引用的是我知识范围内的真实文献族。

## 1. 逐组件对标表

| # | 组件 | 我们用什么 | 对标的公开 benchmark/论文族 | 可靠度 | 偏离/风险 | 修复状态 |
|---|---|---|---|---|---|---|
| 1 | 测试 case/字段 | MemEvoBench 官方 QA(108)/WF(83) 发布字段 | 官方仓库 `github.com/xiewwee11/MemEvoBench` commit a11543e | 🟢 | 无自造合成场景 | ✅ **git 实证(20260719)**:7 个 QA 数据文件 tracked 且未改 |
| 2 | unsafe 判定 rubric | 官方 `JUDGE_RESPONSE_PROMPT` 原文,经 `offi.judge_response_correctness` | 官方 judge rubric | 🟢(rubric) | — | ✅ **git 实证**:官方模块 diff 只加 sys.path 修补,judge prompt/函数/打分零改动;rt02 无自造 rubric(grep 空) |
| 2b | unsafe 判定**模型** | 主 judge1=**gpt-4.1-mini**;judge2=gpt-4o 做 AND 闸门 | 官方默认 judge_model=**gpt-4o** | 🟡 | **偏离**:主 judge 模型≠官方默认(为省钱+续 0712 pilot);rubric 相同但模型不同可能移动绝对水位 | 🟡 声明;gpt-4o AND 闸门部分缓解(官方默认模型仍在闸门里);confirmatory 可加"judge1=gpt-4o"敏感性一次性核验 |
| 3 | 纠正文本 | 官方 `correct_answer`/`correct_workflow` 原文 | MemEvoBench 官方发布字段(oracle) | 🟢(内容)/🟡(语体) | 语体不同 → style confound。**细分(v1 审计+本轮复核)**:QA 长度比 median **0.946=本就在 ±15% 带内**;WF median **0.344=严重失配** → **style-matched 臂主要是 WF 的刚需,QA 侧影响小** | 🟡 模块 `rt02_v2_style_match.py` 已建+自测 9/9(LLM 路径接好未调用,需 API 批准);gate 已验证能标出 WF 式失配、且不对 QA 误报 |
| 4 | 检索 | v2 TF-IDF 余弦 top-k(k=5,冻结) | 记忆 agent 文献常用 dense embedding 检索(MemGPT/RAG 族) | 🟡 | **词法检索 ≠ 领域标准的稠密检索**;可能漏语义相关记录 | 🟡 已抽象为可插拔接口;dense embedder 未装(sentence-transformers 缺,不擅自下载) |
| 5 | 固化算子 | append_only / summary_rewrite / merge + fail-fast | 记忆写入/摘要文献(MemGPT 记忆编辑、递归摘要、A-Mem 族) | 🟡 | 是简化算子;真系统的摘要/合并更复杂 | ✅ 三算子+fail-fast 就绪(真改旧 state 被强制) |
| 6 | 语义分离 q(NLI) | DeBERTa-v3-MNLI 句级蕴含 + roberta 敏感性 | NLI 忠实性检测族(SummaC/MiniCheck/FactCC/AlignScore) | 🟡 | **句级 MNLI 对跨句关系/细微角色错标是盲的**(见 week2 §2 结论);忠实性文献更推 doc 级 checker(MiniCheck) | 🟡 已知盲区;lineage-local 缓解稀释但不解决 MNLI 语义盲;MiniCheck 类 checker 本地无 |
| 7 | RQ2 对手指标 | TrustMem-style prompt 重实现 | TrustMem(proposal 引) | 🔴 | **退化成常数**(preservation 全 10),比较无效;非官方代码 | 🔴 v2 pairgain runner **暂未采集**;RQ2 需校准出方差或拿官方代码,仅 RQ1 GO 后做 |
| 8 | 统计 | paired bootstrap 10k / grouped CV by case / whole-curve permutation / partial Spearman | 标准重采样统计 | 🟢 | 无 | ✅ 就绪(v2 chir/pairgain stats 已实现并验证) |
| 9 | 数据泄漏防护 | v1 已用 63 case 封存;v2 用未见 dev15/confirmatory30 | 独立 held-out 惯例 | 🟢 | 无(QA 45 未见充足,无需 nested) | ✅ manifest 就绪 |
| 10 | query/时间分离 | held-out endpoint query 永不写回;G 预测未来 t+h | 防泄漏预测评估惯例 | 🟢 | horizon 深度受 transitions 数限 | ✅ 就绪(runner 落地) |

### 1b. git 实证的边界(20260719)

- **QA 主线干净**:数据未改、官方 judge 模块只改 sys.path、rt02 无自造 rubric——**已 git 逐条实证**。
- **WF 侧未核验**:官方 WF 文件 `memorybench/Workflow/normal/eval_workflow.py`、`tool_correct_memory.py`、amem/* 等**有本地改动,内容未审计**。WF 是 secondary(confirmatory 主线是 QA),但**若日后跑 WF 结论,必须先 diff 这些文件确认没动 judge/数据**。
- **judge 模型偏离**见 #2b:主 judge≠官方默认,是当前 QA 主线唯一的口径偏离。

## 2. 结论:哪些评估已"足够可靠",哪些还不能进主判据

**🟢 已足够可靠(可直接作 confirmatory 主判据的基础)**：
- 数据/judge/纠正内容/统计/split/query 分离(#1,2,3内容,8,9,10)——全部官方原样或领域标准。
- **CHIR 的主判据链**(官方 case → 官方 judge → paired delta → bootstrap → AND)是**端到端公开-benchmark 对齐**的。

**🟡 可靠但需声明/有敏感臂兜底(不单独定生死)**：
- 检索(#4):词法 top-k,须声明非稠密;确认时同时报"检索 exposure",并留 dense 接口。
- 算子(#5):简化,但 fail-fast 保证"真改 state";append_only 作 operator-off 对照即"标准锚"。
- NLI q(#6):句级盲区已知,lineage-local 修的是稀释(R3)不是语义盲;结论须配 roberta 敏感性,且 PairGain 的 NLI 侧结论**天然弱于** judge 侧。
- 纠正语体(#3):official-text 臂 benchmark-faithful,style-matched 臂做 construct sensitivity。

**🔴 现在不可靠,禁止进主判据**：
- RQ2 TrustMem-style 对手(#7):退化,必须校准出方差或换官方代码,且只有 RQ1 先 GO 才做。

## 3. confirmatory 前的可靠性待办(按优先级,均不改主判据)

1. **(P1)** #3 style/length-matched 纠正敏感臂(需 API 生成,dev 阶段冻结 prompt)。
2. **(P1)** #4 dense embedding 检索作 sensitivity(需装 sentence-transformers → **须用户批准下载**;否则 TF-IDF 为冻结主检索,dense 缺席作声明限制)。
3. **(P2)** #6 若可得 MiniCheck/AlignScore 本地权重,作 NLI 忠实性 sensitivity(否则 DeBERTa+roberta 双 checkpoint 为准,声明句级盲区)。
4. **(P2)** #7 只有 RQ1 GO 才校准 TrustMem-style 或接官方代码。

## 4. 一句话

**主链(数据/judge/纠正内容/统计/防泄漏/query 分离)已端到端对齐公开 benchmark、足够可靠;检索、NLI、纠正语体是"可靠但需声明+敏感臂"档;RQ2 对手指标当前不可靠、禁入主判据。CHIR 的 confirmatory 判据现在就站得住;PairGain 的 NLI 侧结论天然弱一档,须双 checkpoint + 声明句级盲区。**
