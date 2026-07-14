# 交接文档 · Relation-Blind 论文线 · 2026-07-11(换窗口先读这一份)

## 0. 30 秒定位
- 母项目:迭代记忆固化(TierMem C^N)的安全/幻觉研究,`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot`。
- **本会话结论**:原始"固化很危险"假设(RQ1 洗白 / RQ2 造假)经实测**基本为负**;唯一活着的正向资产 = **标准评测器对"关系/角色错绑"是盲的**(词袋蕴含,recall 0.50)。
- **当前论文方向(v3)**:把资产从"评测器有盲区(静态,被占先,novelty 6)"升级成 **"固化随压缩深度主动把可检错误洗进评测器盲区"(动态,无人占据,novelty 7)**。
- **下一步 = 跑一个便宜的 kill-switch 实验**(种可检关系错→C^N 到 N=0..8→测检测器 recall-vs-深度曲线)。曲线下降 → 论文成立(冲 7);不下降 → 换方向。**别再雕 proposal,去跑那条曲线。**

## 1. 当前 proposal(v3)—— 一句话
**迭代固化 C^N 会随深度,把"本来能被检测器抓到的关系/角色错误"主动洗成检测器抓不到、还被盖章 faithful 的形态;盲区是压缩动力学的稳定吸引子,不是评测器的静态缺陷。**
- 全文:`state/proposal_v3_20260711.md`(也在 `~/Desktop/proposal_v3_relation_blind_20260711.md`)。
- 核心贡献:C1 动态洗白发现(headline,经验,便宜)/ C2 overlap-kernel blind-cone 机制(轻形式,不承重)/ C3 HaluMem benchmark 通胀 / C4 诊断套件 + provenance-linked 固化修复探针。

## 2. 核心实验(决定 7 分还是 2.5 分,M1 几天可跑)
1. 种一个 N=0 可被检测器抓到的关系错(源含消歧句,recall≈1);
2. 用现有 C^N harness 固化到 N∈{0,1,2,4,8}(faithful + lossy 算子);
3. 测每个检测器 recall vs 深度 N。
- 成功 = **recall 随 N 单调下降**(McNemar p<.01)+ provenance 确认错误还在(被藏非被改对)。
- 必须的控制:①in-window 全上下文喂 NLI(排除"证据出窗");②去 overlap 负控(recall 不掉→锚定"洗向词袋盲区")。
- 全用盘上资产:C^N harness + `scripts/core/rq2_seed_taxonomy.py`(S1 种子套件)+ 盘上 DeBERTa-MNLI/SummaC。**CPU 跑(MPS 长前提会挂)、per-session qdrant path、Clopper-Pearson 小 n。**

## 3. 修复(用户问过)= 对准病根,不是换检测器
病根:固化丢了跨句消歧上下文。修法:**provenance-linked 固化**(每条压缩记忆挂"验证该关系所需源句"的链接)+ **关系级校验**(对着链接源句查"谁-关系-谁",不查词)+ 查不出就 flag/abstain。诚实边界:只测"挽回多少 recall",别喊 solved;依赖来源链抓到消歧句 + 关系校验本身对。这正是项目原 TierMem provenance 主线(RQ3)。

## 4. 诚实风险(用户担忧,正确)
- 这类"审计+弱修复"论文**做不扎实容易被打 2/2.5**。决定 7 vs 2.5 的**就一件事:那条 recall-vs-深度曲线在真实 benchmark 上大、干净、human-gold 验证**。小/合成/只交 proposal = 2.5。
- **有真实概率曲线不下降**(固化其实保真——本会话已测到它对显式标记/policy 保真、UAF=0)。真那样就退回"静态三维盲区矩阵"(novelty~6.5)或换题。

## 5. 支撑证据(本会话实测,已落盘)
- `state/rq1_rq2_execution_results_20260711.md` —— RQ1 洗白稳健负(UAF=0、标记 N8 存活、3 prompt×route)+ 根因(固化 prompt 反洗白设计)+ RQ2 检测器盲区量化(S1:跨句 relabel recall 0.50;根因=词法重叠,overlap→0/8、no-overlap→8/8;SummaC 修不了)。
- `week2report.md` §6 —— 同上的报告版。
- `state/rq1-5_compliance_audit_20260710.md` —— RQ3 Pareto/RQ4 算子两处失实。

## 6. 完整文件地图
**Proposal 演化**:`state/proposal_ideaspark_20260711.md`(v1 审计)→ `_v2_`(重定位+加固)→ `proposal_v3_20260711.md`(**当前,动态 headline**)。
**评审+novelty(本会话 workflow 产出,已固化)**:`state/formal_reviews_summary_20260711.md`(两轮 5-persona 评审:v1=5、v2=6,到 7 需跑实验)、`state/novelty_and_scoop_landscape_20260711.md`(3 重构 + scoop 核查 + 全部 arxiv id 状态 + kill-switch)。
**autoresearch 评审项目**:`/Users/yihaiwen/Documents/New project/proposal_review_relation_blind/`(reviews/review_round_01.md、state/)。用法见 `/Users/yihaiwen/Documents/New project/autoresearch_workflow/README.md`(init→make-prompt --track review→route-review→record-iteration)。
**代码(本会话新建/改)**:`scripts/core/rq2_seed_taxonomy.py`(S1 关系错最小对+recall)、`scripts/core/rq2_summac_probe.py`、`scripts/analysis/rq1_uaf_by_n.py`;`tiermem_upstream/src/memory/linked_view_system.py` 加了 `lossy_abstractive`/`lossy_eventful` 两个真固化算子(+`run_rq1_safety_consolidation.py` choices)。
**结果 JSON**:`state/rq2_g1_control_result_20260711.json`、`rq1_uaf_{full_seed11,summaryonly,multiseed,lossy,lossyeventful}_20260711.json`、`rq2_summac_probe_result_20260711.json`。
**方法工具**:ResearchStudio-Idea(microsoft,MIT)clone 在 scratchpad(临时,换窗口丢;方法=IdeaSpark 5 阶段 + 15 pattern,可重 clone `github.com/microsoft/ResearchStudio`)。

## 7. 环境坑(必照做)
- 前置:`cd 项目根; set -a && source .env.v3 && set +a; .venv_tiermem_v2/bin/python scripts/install_dev_paths.py`。
- **本地 NLI 用 CPU**(MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli;MPS 长前提大批会挂死)。
- qdrant per-session 独立 path;跨会话记忆索引 `~/.claude/projects/-Users-yihaiwen/memory/MEMORY.md`。

## 8. 一句话交接
论文线已收敛到 v3(动态洗白,novelty 7 的形状),但**成不成立吊在一个几天就能跑的 kill-switch 曲线上**。新窗口第一件事:**跑核心实验(§2),别继续改文字。** 曲线下降→冲 7;平→换方向,别在注定 2.5 的路上投时间。
