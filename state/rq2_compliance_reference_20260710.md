# RQ2 合规基准参考:数据集 / 压缩 / 指标 / 题型

**对标 v2 PDF 计划 + 公开 benchmark + 相关文献 | 2026-07-10**

> 三路核查(PDF 计划 / 文献·benchmark 标准 / 现状代码)综合固化。**以后设计或审稿 RQ2 直接查这份,不必重跑核查。** 行号为核查时的证据出处。

---

## 0. 一句话

RQ2 = "固化(压缩 / consolidation)是否制造假记忆(幻觉)"。当前实现的负结论("固化良性 / 无正斜率")**可信度低,根因是设计不合规**(三个 stage 指标未落盘 + 题型切片剔除了固化幻觉主战场),而非规模不足。先补合规、再谈规模。

---

## 1. PDF 计划对 RQ2 的要求

**数据集**
- 主 = **HaluMem-Medium**(pilot / E1)+ **HaluMem-Long**(E5 压力测试),保留 抽取/更新/QA 分解(计划:22,43,72,76,146,160)。
- E3 冲突/更新线:HaluMem update 案例 + **LongMemEval** 知识更新/时间条目(计划:148)。
- pilot 每攻击家族 **100 例**(计划:83)。**未要求自建题库。**

**压缩/固化**
- 主轴:固化深度 **N ∈ {0,1,2,4,8,16}**(计划:75,99,146,156)。
- RQ2 本身:**只摘要 vs TierMem 式(摘要+原始升级)** 对比(计划:146)。
- 多算子家族(抽象摘要 / 命题化 / COMEDY / Context-Memory / TierMem 分层)属 **E4/RQ4**(计划:75,99,156)。

**指标 —— 三个 stage-attributed 指标(RQ2 命脉)**
- **UNMR(N)**:Unsupported New Memory Rate —— 第 N 次固化新建的记忆里、缺任何源支撑的比例(**固化阶段幻觉**)。
- **conflict-merge-rate(N)**:矛盾事实对被错误合并成一条的比例(**更新处理**)。
- **PAR(N)**:Propagation-to-Answer Rate —— 答案里引用/依赖了无支撑记忆的比例(**传播到答案**)。
- 加 HaluMem 分阶段分(extraction/update/QA)(计划:97,174-176)。

**题型**
- HaluMem 客观 QA + reader 阶段 judge label + **abstention**(计划:127,177)。

**成功判据(stop/go)**
- **支持假设** = HaluMem 抽取/更新错误**先升**、无支撑记忆**随后传播进 QA**,即风险随 N 有**非平凡正斜率**(计划:97,146,182,263)。
- **反驳** = 无正斜率,但须先按 §7 **收紧压缩预算重跑**再放弃(计划:189,263)。

---

## 2. 公开 benchmark + 文献的标准评估方式

**HaluMem 官方**
- 四指标:**integrity / accuracy / update**(记忆对象层,0/1/2 分,含 hallucinated-memory 判级)+ **QA**(答案层)(`docs/halumem_official_eval_integration.md:3`;`evaluation.py:38-41`)。
- **全程 LLM judge 主观分,无 MCQ**;QA 判 `Correct | Hallucination | Omission`(`eval_tools.py:218-280`)。
- **含 abstention 正例**:gold = "unknown/无法确定" 时,系统答 unknown = Correct,猜确定事实 = Hallucination(`eval_tools.py:254-255`)。

**LOCOMO / LongMemEval**
- LOCOMO:**单跳 / 多跳 / 时间推理 / 开放域** 四类,均 198.6 题/对话(`05_benchmarks.md:25-30`)。
- LongMemEval:500 题,信息提取 / 多会话推理 / 知识更新 / 时间推理 + abstain(`05_benchmarks.md:44-56`)。
- 指标:混客观短答(F1/精确匹配)+ judge 开放答。

**压缩/摘要文献(summary-drift,与 COMEDY 精神同构)**
- 测法:**不看最终答案是否相关,而追溯中间 memory object 相对原始证据是否丢限定词/时间/例外**(source-backed memory audit)(`summary_drift.md:45-46,88-98`)。属**记忆质量层**。

**主观题结论(关键)**
- 公开 benchmark **普遍含主观开放题 + LLM judge**。
- **只用客观题**(短答/MCQ)会漏:摘要漂移、多跳断链、时间态覆盖 —— **正是"压缩制造幻觉"的主战场**。
- **只用主观题**会受同源 judge 乐观、backbone LLM 时间能力混入污染,失去可复现锚点(`06_key_conclusions.md:69-75`)。

**符合标准的 RQ2 应覆盖**
- 题型:①单跳客观短答 ②多跳 ③时间/更新 ④冲突/abstention(`05_benchmarks.md:100-114`)。
- 指标:**记忆对象层(integrity/accuracy/update)+ 答案层(QA judge)双轨**,而非单一 QA 正确率。

---

## 3. 现状(2026-07-10)

**数据集(双路线)**
- HaluMem-Medium 手工切片:最干净 **1 session / 15 QA**,已扩 3 session / 45 QA(`rq2_dual_track_refresh_20260708.md:113-127,144-149`)。一 golden user ~65 session(`halumem_official_eval_adapter.py:41`)。
- 自建 factual poison(合成灌毒,非官方):v4 = 42 base / 14 领域 / 84 probes(`rq2_suite_v4_domain_diverse_20260708.md:3-7,76`);v6 = 100 base / 200 probes(refresh:42-58)。
- **HaluMem-Long 不在盘上,E5 无法跑。**

**压缩**
- 单一 TierMem N-pass infer(N=0/1/2/4;`slice.py:72`;`adapter.py:402-404`)。
- comedy_style 只落盘 1 次(`poison:483`);无摘要/命题算子;**N=16 从未跑**。

**指标**
- **只有自建 judge 真跑**:`classify_answer` → FALSE_BELIEF/TRUE/OTHER(`poison:302-339`);`halluc()` 正则(`rq2_fixed.py:9-13`)。
- **UNMR/conflict/PAR:`rq2_stage_metrics.py` 定义在但无 run 调用、零落盘**;poison 内 `*_proxy` 也零命中。
- 官方 HaluMem 指标:刚接通(skeleton/validate),未真跑落盘。

**题型**
- 自建默认开放题(free/operational)+ 支持 MCQ(forced_choice A/B)已跑(`poison:313-322`)。
- HaluMem QA 开放题(`adapter:71`)。
- 有 abstain 检测(`rq2_fixed.py:9-10`)但 MCQ 无显式弃权选项。
- **外部切片系统性排除多跳(LOCOMO cat-3)、时间、开放漂移题**(`round32:25`;`round34:25`)。

---

## 4. 合规对照 + 差距

| 维度 | PDF 要求 | benchmark 标准 | 现状 | 差距 |
|---|---|---|---|---|
| 数据集 | HaluMem-Medium+**Long** + LongMemEval;每家族 100 例 | 多题型全覆盖 | HaluMem 切片 15/45 + 自建合成 poison | 缺 Long、缺规模、切片排难题、掺计划外合成题 |
| 压缩 | N∈{0..16} + 多算子 | 记忆对象层审计 | 单一 TierMem infer N≤4;comedy 1 次 | 缺深 N、缺多算子对比 |
| 指标 | **UNMR/conflict/PAR** + HaluMem 分阶段 | **记忆层 + 答案层双轨** | 只自建 judge;stage 指标零落盘;官方未跑 | **只测答案层、没测固化阶段**;单轨 |
| 题型 | HaluMem QA + judge + abstention | 单跳+**多跳+时间+漂移**+abstention | 开放+MCQ;但切片剔除多跳/时间/漂移 | **缺固化幻觉主战场题型** |

---

## 5. 核心诊断

当前"固化良性"负结论 = **两层构造性偏差叠加的伪影**:
1. **指标测错了层**:RQ2 机制是"错误先在固化阶段出现(UNMR)→ 再传播进答案(PAR)",但 stage 指标零落盘,只看了答案终点 —— **根本没测"固化阶段是否先造错"**。
2. **题型测错了场**:切片只留客观短答 + ABSTAIN 二分,剔掉了多跳/时间/开放漂移题 —— 而这些是压缩幻觉主战场。**在最不可能暴露固化危害的题型上,用测不到固化阶段的指标 → 必然得"固化良性"。**

---

## 6. 实现 stage 指标需要的数据契约(from `rq2_stage_metrics.py`)

run 必须逐 item 落盘:
- new-memory record:`{is_new: bool, has_source_support: bool}`
- conflict record:`{is_contradictory: bool, merged_incorrectly: bool}`
- answer record:`{used_unsupported_memory: bool}`

`has_source_support` 由固化 harness 从 **TierMem 的 provenance links** 填(一条 compact 记忆指向 ≥1 raw span 才算 supported)。**若 run 还不能输出 provenance,那是 RQ2 需要的 harness 改动,不是打分改动。**
