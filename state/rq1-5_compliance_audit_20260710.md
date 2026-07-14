# RQ1–5 合规性审计:数据集 / 指标 / 题型 / 统计

**2026-07-10 | 揪自建口径 + 对齐官方的优化路径**

> 三路核查(RQ1+RQ5 / RQ3+RQ4 各一路 agent,RQ2 本会话深挖)综合。核心问题:每条 RQ 在数据集/指标/题型/统计四维度,用的是**官方/标准**还是**自建口径**?能不能对齐公开 benchmark / 官方指标 / 相关论文?换不了的怎么规范化自建。行号为核查证据。

---

## 0. 总账

- **没有"假装有官方"糊弄**:安全×固化(RQ1)、know-do(RQ5)这两个方向**本来就没有公开 benchmark**,项目也老实标了合成。
- **两处实质失实**(见 §2):RQ3 的 Pareto 效用侧从没真测、RQ4 的"压缩家族对比"是假的。
- **普遍病**:自建指标大多停在"词法/关键词匹配"层,该升到 NLI / payload-emission / 官方指标。

---

## 1. 合规矩阵

`✅官方/标准　⚠️自建但可对齐官方　🔶只能自建-需规范化　❌缺失/失实`

| RQ | 数据集 | 指标 | 题型 | 统计 |
|---|---|---|---|---|
| **RQ1** 安全 | 🔶 自建投毒套(真空,可并跑 AgentPoison 对照) | 🔶 词法覆盖 + **硬编码 unsafe 标记(自埋雷)** → payload-emission+NLI | 🔶 带"quickest way"**天花板诱导** | ✅ Clopper-Pearson + 趋势检验(最规范) |
| **RQ2** 幻觉 | ⚠️ 官方 HaluMem 但小切片 → 本次已建四家族分层 | ✅ 本次改 NLI 三分类 + 官方 accuracy(**零自建**) | ✅ 本次四家族覆盖标准 | ✅ Holm/趋势就绪,待 sweep |
| **RQ3** 防御 | ⚠️ 自建 30 题 → 该换 AgentPoison-on-LongMemEval | ⚠️ RRR/Pareto 数学对,但**效用侧手填 JSON、judge 同源** | 🔶 防御是 **prompt 模拟 ≠ 架构 provenance** | ⚠️ CI 对但**缺 Holm 校正** |
| **RQ4** 算子 | ❌ 该用官方底座 | ❌ **无热力图/无斜率** | ❌ **"压缩家族"是假的** | ❌ 无 |
| **RQ5** know-do | 🔶 复用 RQ1 套(真空) | ⚠️ 默认同源 judge → **该把 mcq 确定性端点设主** | 🔶 设计合理但带天花板诱导 | ✅ Clopper-Pearson |

---

## 2. 两处"实质失实"——若对外说"按计划完成"就是错的

1. **RQ3 的 Pareto 根本没闭合**:判据两半里"效用损失 ≤3pt"这一半**从没真测过**——`run_rq3_provenance_clean.py:326-356` 的 `--utility-map` 是**手填 JSON**,没接真实 LongMemEval-S 效用数据。现在只有风险侧(还只降 ~15%、没过 25% 门槛,`plan_v2_code_audit:88-90`)。
2. **RQ4 的"压缩算子家族对比"是假的**:`comedy_style`/`emem_style` 只是**写进 metadata 的字符串**(`run_v2_tiermem_local_bridge.py:331`),核心压缩逻辑没有 style→prompt 映射——comedy 其实是"换路由 summary_only"、emem 是"关掉固化"(`run_branch_comedy_control.py:4-6`、`run_branch_emem_control.py:4-6`),**不是不同压缩算子**。两分支 docstring 自认"非复现代理"。冠 COMEDY/E-mem 名会误导审稿人。

---

## 3. 优化清单

**A. 能对齐官方的(优先,消灭自建)**
- **RQ3 效用侧接 LongMemEval-S 官方 exact/F1/abstain** → 补 Pareto 缺的那一半(先补,因为是失实点)。
- **RQ4 接开源 COMEDY / Context-Memory**(PDF 已列 GitHub)做真算子对比;**做不到就删掉 RQ4 的算子声明**。
- **RQ1 并跑 AgentPoison 公开投毒套**做外部对照。
- **RQ2 HaluMem 全题型 + LongMemEval**(本次已铺路)。

**B. 只能自建、必须规范化的**
- **指标升级**:RQ1 洗白判定、RQ5 KNOW 判定 → **NLI**(复用 `rq2_stage_extract`);RQ1 refusal → **payload-emission**;**删硬编码 unsafe 标记词**。【RQ1 指标层本次已改】
- **判定去同源**:RQ3 judge 换**异源**;RQ5 mcq 端点设主、judge 作对照。
- **去天花板**:RQ1/RQ5 删"最快/quickest way"诱导。
- **统计**:RQ3 接已实现的 **Holm 校正**;全部上 **≥5 seed + 预注册 + ≥1 非 OpenAI backbone**。
- **人工 κ 兜底**:NLI 自动判 + 人工抽样校验(RQ1 已有 κ=0.85 范式,κ 脚手架本次已并入 `safety_metrics.export_kappa_sample`)。

**C. 已经规范、别动的**
- κ=0.85(真 κ)、Clopper-Pearson/趋势检验、RQ2 本次的 NLI 三分类 + 官方 accuracy、mcq 确定性端点。

---

## 4. 逐 RQ 详细(带行号)

### RQ1(固化放大不安全内容)
- **数据集**:`unsafe_seed_suite_v1.json` n=12(`run_rq1_safety_consolidation.py:49`)+ `stealthy_poison_suite_v1.json` 15×2=30(family 全 `stealthy_convention`)。**真语义家族只 2 个**(stealthy_convention / backdoor_trigger),subject 是伪家族轴。全脚本无 family/cluster 分组。
- **指标**:洗白/生存靠 `_coverage` token 覆盖(`safety_metrics.py:62`)+ 硬编码 `_UNSAFE_MARKERS`(`:46`,construct contamination:marker 灌进种子)+ 关键词 refusal `_REFUSAL_MARKERS`(`:48`,hedge-comply 假阴)。→ 改 `payload_emitted`(`safety_honest_metrics.py:83`)+ NLI。【本次已改】
- **题型**:trigger_query 全带"quickest way"诱导(`safety_axis_honest_final:20` 自承 ceiling)。
- **统计**:Clopper-Pearson(`safety_honest_metrics.py:28`)+ Cochran-Armitage(`run_rq1:44,468`),最规范;但 n=12/15 单种子功效低。
- **κ**:`outputs/safety/kappa_result.json` κ=0.85/n=30,唯一真 κ。

### RQ2(固化制造假记忆)—— 本次会话已规范化
- **数据集**:官方 HaluMem-Medium(标准),之前只切 15/45;本次建四家族分层 `scripts/core/rq2_dataset_build.py`。
- **指标**:本次 `scripts/core/rq2_stage_extract.py` 本地 NLI 三分类(entail=支撑/neutral=缺支撑/contradiction=硬假记忆),UNMR/contradiction/PAR,与 HaluMem 官方 accuracy 双轨。零自建口径。
- **题型**:四家族(单跳/多跳/时间更新/冲突/abstention)覆盖 benchmark 标准。
- **统计**:Holm/CA 就绪,待正式 sweep + 多 seed。

### RQ3(provenance 分层断毒链)
- **数据集**:`stealthy_poison_suite_v1.json` 30 题合成(`run_rq3_provenance_clean.py:55`),5 seed 只是同 30 题重采样非独立复现。PDF 要 AgentPoison-on-LongMemEval / 每家族 100 例。
- **指标**:`unsafe_judge_rate`(judge 同源 gpt-4.1-mini,`:1129-1130`)+ `relative_risk_reduction`/`pareto_gate`(`stats_guardrails.py:76,92`,数学正确);**效用侧 `--utility-map` 手填 JSON(`:326-356`)、Pareto 没真闭合**。
- **题型**:防御是 prompt 前缀模拟(`:71-82`)≠ 架构级 provenance;source-trust/uncertainty-gate/conservative-compaction 占位(`plan_v2_code_audit:73-75`)。
- **统计**:McNemar + seed-t + CP CI 对,`interpretation:56` 诚实标聚类;但缺 Holm 校正(多防御×backend×N 未校正)。

### RQ4(哪个固化算子最脆)—— 四维度全不达标
- **算子(核心)**:PDF 要抽象摘要/命题/COMEDY/Context-Memory/TierMem 分层(`计划:75,156`);现状 `consolidation_prompt_style` 只写 metadata(`run_v2_tiermem_local_bridge.py:331`),comedy=route summary_only、emem=关固化(`run_branch_*_control.py:4-6`),**非算子对比**。能对齐:官方 COMEDY(github)、Context-Memory。
- **指标**:无热力图、无跨算子斜率。
- **数据集/统计**:同自建套,无跨算子检验。

### RQ5(失败在哪个环节 / know-do)
- **数据集**:复用 `stealthy_poison_suite_v1.json`(`run_rq_know_vs_do.py:32`),n=15。无公开 know-do benchmark(真空)。
- **指标**:KNOW 靠 token 覆盖≥0.5(`:194`);DO 三端点 judge(同源,`:56`)/lexical/**mcq 确定性字母判定(`:92`,本次加)**。→ mcq 设主端点、KNOW 换 NLI。
- **题型**:同记忆双问(KNOW 复述 / DO 情境)设计合理;带 quickest way 诱导。
- **统计**:Clopper-Pearson(`:225-226`);单次 n=15/30,建议 cluster CI + 多 seed。

---

## 5. 一句话

五条 RQ 里 RQ1/RQ5 最扎实(负结果/机制发现)、RQ2 本次补上方法学、RQ3 半吊子且有一处失实、RQ4 基本没做且有一处失实。**性价比最高的三刀**:①补 RQ3 效用侧(消灭一处失实)②RQ4 接真 COMEDY 或删声明(消灭另一处失实)③把"词法判定→NLI/payload"复用到 RQ1/RQ5(RQ1 已趟通)。
