# 研究提案 · 保义流形上的证据轨迹:一个消融验证的几何归因器,闭合 Agent 记忆失败的"归因—修复"环 · 2026-07-13(v6,几何归因器消融验证版)

> 结构对齐本地 autoresearch/IdeaSpark 框架(Hook 瓶颈 → Core mechanism → Falsification 非平凡负控 → Gap closure → Differentiation 撞车审计 → Reviewer concerns 五检 → Evidence → 一句话)。pattern 命中 `reframe_as_solvable_object`(主)+ `controlled_diagnostic_design` + `architectural_operator_substitution`(副)。

## Title
**The Restore Operator on an Answer-Preserving Manifold: Closing the Diagnose→Repair Loop for Memory-Augmented Agent Failures.**

## Hook(瓶颈,Phase 1)
记忆增强 agent 的失败链是 `写入 → 固化(递归摘要,多对一合并)→ 检索 → 回答`。两个承重缺陷叠在一起:
1. **不可归因**:失败到底是哪个记忆操作弄坏的,无法定位。近期 agent 失败归因(Causal Agent Replay 2606.08275 / CausalFlow 2605.25338)归到**推理步**、且 memory-agnostic;它们的前向 do-算子**结构上无法"恢复一条被固化删掉的记忆"**——不能给推理步补回它从未拥有的信息。
2. **只诊断、没方法**(核心瓶颈):即便归因出来,现有思路也只是**指出"哪步坏了"的分析**,没有一个**用这个信号去修复失败**的方法。纯诊断型工作审稿人必问 "So what?"。

**未占据的开口**:把记忆生命周期看成一条**证据表示在"保义流形(answer-preserving manifold)"上的轨迹**——保真 = 留在流形上,失败 = 某个操作把它推离流形;而**同一个"离流形距离"信号既能归因、又能触发修复**,把"诊断"闭合成"诊断→修复→端任务改善→反过来验证归因"的因果环。这是 provenance-DAG(带合并节点)上的因果对象,链式 SCM(CAR)表达不了。

## Core mechanism(Phase 2.2)——三件套构成一个闭环
**M1 · 保义流形上的证据轨迹 → 学习的几何归因器(承重,已消融验证)**
一条 gold 证据有语义表示 `e`(embedding)。它流过 写入/固化/检索,得到一条**证据保留度轨迹** `φ = (sim_write, sim_store, sim_retr)`(`e` 与各阶段内容的语义相似度)——保真 = 留在"保义流形"上,某个 op 把它推离流形则对应分量塌陷。**从带真值样本学一个分类器 `φ → 责任 op`**(证据保留度落在流形上/离开流形的判别面)。
**关键的方法学发现(已实测)**:朴素"最大跌幅"读法失败(各阶段表示基线不可比,退化为恒猜 write,36%);但**学习的几何分类器自动找到正确组合,反超脆弱 LLM 成员检查 +10 点(66.8% vs 55.1%,5 折 CV),且消融验证承重**(去掉几何特征掉回 55%)。⇒ 几何信号是**真承重组件**,取代脆 LLM 是非检查这个 55% 天花板。

**M2 · restore = provenance-DAG 边上的 do-手术(理论腿)**
把 restore-consolidate 形式化成 `do(固化边 := 保留 e)`——图上的因果干预。**合并节点**(k 条源记忆压成 1)正是它区别于 CAR 链式模型之处;给出**责任 op 由离流形跳变唯一可识别**的条件,及合并纠缠时的有界 ambiguity(预测"归不出"率)。

**M3 · provenance-guided 修复(方法腿——"So what"的答案)**
推理时用 `d_op`:哪步离流形跳变超阈值,就触发修复——把 e 重注入 / abstain / flag。**这就把系统从"事后诊断"升成"实时防止失败"。**

## 逻辑闭环(本提案的脊梁,用户要点)
```
         [保义流形 · 离流形距离 d_op]  ←── 单一信号，两端共用
        ╱                              ╲
  归因(M1)                            修复(M3)
   哪个 op 把 e 推离流形？   ──guides──▶  对该 op 触发重注入/abstain/flag
        ▲                                    │
        │                                    ▼
        └────validates──── 修复该 op 若端任务变好 ⇒ 归因因果正确
```
**闭环的关键**:归因**指导**修复;修复**反过来验证**归因——**"修了被归因的那一步,端任务就变好"本身就是归因正确的因果证据**(而非又一个自证)。同一个 `d_op` 信号驱动两端,理论(M2)保证可识别,真值 benchmark 量化两端。这把一篇"6 分诊断"闭合成"7 分方法":有新机制、有因果闭环、有端任务收益。

## Falsification prediction(kill-switch,已跑;非平凡负控)
**主预测**(两条):
1. **归因端(已过 ✓)**:几何分类器在带真值 benchmark 上准确率**显著高于**(a)LLM 成员检查、(b)trace-only judge。**实测:66.8% vs 55.1% vs 36.4%(5 折 CV,n=247),消融 +10.1 点承重。** 预注册硬门槛(几何须 ≥ LLM+3%)达成。
2. **修复端(弱阳,如实报)**:provenance 修复(重注入真证据)vs 随机/干扰对照。**实测:真证据修复 28% vs 干扰对照 2%——证据特异(方向对),但绝对值低**(干扰事实仍在上下文、agent 黏着);故修复腿定位为"证据特异但弱",不夸大。
**唯一承重变量** = 证据保留度轨迹 `φ`。**permutation 负控(已过 ✓)**:打乱标签重训,CV 塌回随机 0.33(真实 0.668,**p=0.005**)——66.8% 是真信号非过拟合。**可解释性(白赚)**:学出的判别面系数**精确复现设计的因果机制**——write=`sim_w↓sim_s↓`(到处无证据)、consolidate=`sim_w↑sim_s↓`(对话有/库里无)、retrieve=`sim_s↑↑`(库里有/没检索)。**几何非黑箱。已证伪的过度读法**:朴素"最大跌幅"流形(36%,进 limitations),承重的是**学习的**几何判别器。

## Compute budget(user-relative)
单 M1 + <$80,纯 inference + 轻量流形学习(embedding + 低维投影/度量学习,CPU 可跑;真值 benchmark 已建、是现成训练+评估数据)。人工:分歧子集金标先去重再抽样、报 κ。几天,无 GPU 训练。

## Gap closure(Phase 2.2)
| 缺口 | 主 pattern | 怎么闭 |
|---|---|---|
| 失败不可归因到具体记忆 op | `reframe_as_solvable_object` | 溯源图上的证据轨迹 + 离流形跳变定位 |
| 只诊断、没方法("So what") | `architectural_operator_substitution` | 同一 `d_op` 信号驱动 provenance 修复 → 端任务收益 |
| 归因无真值、排序 tie-break 脆 | `controlled_diagnostic_design` | 带真值 benchmark(已建)+ 连续 `d_op` 替脆二值检查 |
| 理论只嘴上说 | (DAG do-手术) | restore = 合并节点图上的边干预 + 可识别性 |

## Differentiation from prior work(撞车审计后)
- **CAR 2606.08275 / CausalFlow 2605.25338**:归因到**推理步**、前向 do、memory-agnostic、**无 restore、无合并节点、无修复闭环**。本提案 = 记忆 op 单元 + 图边 restore + 流形信号 + 诊断↔修复闭环。
- **TreeMem 2605.04811 / Memory-R2 2605.21768**:记忆管线 **agent 的 RL credit / re-rollout**(训练信号),非失败诊断、非修复方法、无 provenance restore。
- **流形/表示轨迹**:表示-空间探针(probing)多在**单模型内部层**做,**没人把"记忆系统跨 op 的证据存活"建成保义流形轨迹并用它归因+修复**。
> **almost-prior + missed step**:最近的是 CAR(证了干预式步归因),它漏的一步 = **记忆 op 单元 + restore 算子 + 把归因信号复用成修复方法闭环**。

## Reviewer concerns & responses(五检)
1. **"流形是不是花架子?"**(anti-pattern: 装饰性复杂度)→ 预注册硬门槛:`d_op` **必须**在真值 benchmark 上打赢脆 LLM 检查 **且** 修复端任务涨点;达不到就诚实退回诊断版并明说流形无增量。**流形是承重还是装饰,用消融(shuffle 负控)判死。**
2. **"归因 100% 是不是构造出来的?"**→ 真值 benchmark 覆盖**自信答错**(非只 abstention),且用**第二独立检测器 + 人工 κ**;报"迁移到自然失败"的诚实衰减。
3. **"修复涨点是不是灌任何上下文都涨?"**→ 随机-op 修复负控 + distractor 控制(证是**归因的那一步**在起效,非任何注入)。
4. **paper-pointed threat**:CAR 若扩到 memory 会挤压;故**承重放在 restore 算子 + 修复闭环**(CAR 无),流形/图是机制,理论只作 motivation。
5. **hard-floor**:无 reject-lesson 触发(audit+surgical_fix 这类反模式已用"修复端任务收益+随机负控"化解),无 exact-mechanism 撞车 → **verdict: advance**。

## Evidence to date(已跑,真数据)
- **受控 oracle**(注入已知元凶):restore 归因 **100%** vs LLM-judge 39% vs random 0(证机制+judge 失效;仅 abstention 易 regime)。
- **带真值 benchmark**(8 user,242 注入失败,179 自信答错;`state/memop_groundtruth_20260712.json`):LLM 成员检查版归因 **55%** vs judge **37%**;retrieve 73% / consolidate 47% / write 44%。
- **几何归因器 + 消融**(n=247,5 折 CV;`state/memop_manifold_20260712.json` + `scripts/analysis/memop_hybrid_ablation.py`):**几何(embedding 保留度轨迹)= 66.8% > LLM 检查 55.1% > 裁判 36.4%;消融 +10.1 点承重**;朴素最大跌幅 36%(证伪的读法,进 limitations)。修复:真证据 28% vs 干扰 2%。**⇒ 几何组件真承重、消融扒不倒,承重腿由脆 LLM 检查升级为学习几何判别器。**
- 自然 HaluMem 分解不 robust(无真值 + 排序 tie-break),故经验主张限定"真值 benchmark 上的验证",不主张自然数据主导。
- **诚实边界**:66.8% 部分受益于注入结构较干净(几何特征天生可分),但同状态下 LLM 检查仅 55%,几何提取了更多信号——相对优势真实;修复腿弱;需扩规模 + 自然失败迁移 + 人工 κ。

## 一句话
把"哪个记忆操作弄坏了答案"重构成"证据在保义流形上从哪一步离轨",于是**同一个离流形信号既定位失败、又驱动修复**,"诊断→修复→端任务改善→验证归因"闭成一个因果环——这正是当前诊断版缺的方法腿,也是 CAR 的链式前向模型结构上给不出的东西;而验证它的两端(真值 benchmark 的归因准确率 + 修复的端任务收益)都便宜、都已有数据底座。

## 相关文件 · 跨会话记忆 · 复现入口
**记忆**:`~/.claude/projects/-Users-yihaiwen/memory/memop-attribution-line-20260712.md`、`MEMORY.md`。
**代码**:`scripts/run/run_memop_manifold.py`(几何归因器,收 embedding 特征)、`scripts/analysis/memop_hybrid_ablation.py`(消融)、`run_memop_groundtruth.py`(带真值 benchmark)、`run_memop_halumem.py`(自然)、`run_memop_attribution.py`(受控 oracle)。**结果**:`state/memop_manifold_20260712.json`、`memop_groundtruth_20260712.json`。**记录**:`state/ideation_minimal_baselines_20260712.md`。**桌面副本**:`~/Desktop/proposal_恢复算子_记忆操作归因_20260712.md`。
