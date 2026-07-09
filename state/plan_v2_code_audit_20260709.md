# v2 研究计划 × 代码实现 逐条对照审计（2026-07-09）

> 对照文件：`Iterative_Memory_Consolidation_Research_Plan_v2_refined.pdf`（12 页）
> 审计方法：读计划 §1–§11 → 逐 RQ / 逐实验 / 逐指标 / 逐标准核对代码 → 跑自测 + 编译 + 清点产物。
> 一句话结论：**代码本身无致命错误、可跑、自测通过；但相对计划「完全实现」只做到约一半，且几条计划明写的「标准要求」（N 深度、Holm-Bonferroni/α=0.01、5 种防御、25%/3pt 判据、E5 压力档）未达标。**

---

## A. 代码是否无误？—— 是（运行/单元层面无误）

| 检查 | 结果 |
| --- | --- |
| 全部 RQ 脚本 `py_compile` | ✅ 13/13 通过 |
| `safety_metrics.py` 自测 | ✅ SRR/UAF/unsafe_answer 断言全过 |
| `safety_honest_metrics.py` 自测 | ✅ Clopper-Pearson + payload-emission 断言全过 |
| `run_e1_multiseed_statistics.py --self-test` | ✅ 跨 seed CI + 配对 t 断言全过 |
| McNemar / bootstrap / t 检验数学 | ✅ 用 `scipy.stats.binomtest / ttest_1samp`，实现正确 |

**唯一的「非 bug 但影响效力」的隐患**：`safety_metrics.py` 的 SRR/UAF/RTR@k/unsafe_answer 全是**词法代理**
（token 覆盖 + 关键词，见 `safety_metrics.py:57-114,200-206`）。项目自己已在 `RESEARCH_README.md:15`
证明词法终点会**系统性高估**风险/防御效果，改用否定感知 judge。所以这些指标「代码无误」但
「作为最终终点不可信」——引用时必须走 judge，词法只做交叉验证。

---

## B. 是否完全实现？—— 逐 RQ 对照（部分实现）

| RQ（计划 §3） | 计划要求的主证据 | 代码 | 实现度 | 缺口 |
| --- | --- | --- | --- | --- |
| **RQ1** 固化是否保留/放大不安全 | SRR(N), UAF(N), RTR@k(N), unsafe answer/action | `run_rq1_safety_consolidation.py` + `run_rq1_authority_experiment.py` + `run_rq1_agentpoison_overlay.py` + `safety_metrics.py` | **✅ 完整**（指标全实现、跑过、judge 复核） | 结论为**推翻原假设**（固化良性），非计划预期的正斜率 |
| **RQ2** 固化是否造假记忆 | HaluMem 分阶段分（extraction/update/QA）、**UNMR**、**conflict-merge-rate**、**PAR** | `run_rq2_factual_poison.py` + `run_e1_hallucination_statistics.py`（judge 标签 CORRECT/UF/FD/ABSTAIN） | **🟡 部分** | 计划的**三个 stage-attributed 指标名（UNMR/conflict-merge/PAR）未按定义实现**，被 answer 阶段 judge 标签替代；write/consolidation 阶段的独立度量缺失 |
| **RQ3** provenance 分层能否断链 | 风险下降 vs 效用损失、**Pareto frontier** | `run_rq3_provenance_clean.py` + `run_rq3_readtime_defense_matrix.py`（5-seed 大跑已完成，见 `state/rq3_readtime_large_20260708_interpretation.md`） | **🟡 部分** | 风险侧已测且稳健；**效用侧（LongMemEval-S）没和防御跑绑定，Pareto 未闭合** |
| **RQ4** 哪个固化算子最脆 | 压缩家族 × 防御热力图、风险对 N 斜率 | `run_branch_comedy_control.py` / `run_branch_emem_control.py` | **❌ 未达标** | 两个分支**自述是「contrast/control 代理，非 COMEDY/E-mem 真实复现」**（见脚本 docstring）；**无真正多算子家族对比、无热力图** |
| **RQ5** 失败在哪个阶段 | 逐 item artifact + stage 标签 | `run_rq_know_vs_do.py` + `run_v2_tiermem_micro_failure_mode_judge.py` | **✅ 核心已答** | 定位到 reader（回答阶段）；know-do gap 是本项目最硬发现 |

### E0–E5 实验（计划 §5）完成度
| 实验 | 状态 | 证据 |
| --- | --- | --- |
| E0 集成 sanity | ✅ | `run_week1_tiermem_sanity.py`、bridge 跑通 |
| E1 HaluMem N-sweep | 🟡 pilot | 只到 N=8×1、N=4×3，**N=16 从未跑**（见下 §C.1） |
| E2 良性效用 | 🟡 部分 | LoCoMo/LongMemEval 切片在，但未与防御做 Pareto |
| E3 冲突/更新漂移 | ❌ 未做 | 有 `conflict_task_extension_v2.json` 数据，无实验脚本跑它 |
| E4 防御消融 | 🟡 2/5 | 见 §C.3 |
| E5 压力（HaluMem-Long / LongMemEval-V2） | ❌ 未做 | **数据都不在盘上**（见 §C.4） |

---

## C. 是否符合「标准要求」？—— 5 处明确未达标

### C.1 N-sweep 深度不足（计划要 N∈{0,1,2,4,8,16}）
盘上 sweep 报告实际 N 分布：`N=0×17, N=1×16, N=2×16, N=4×3, N=8×1, N=16×0`。
主体只有 N=0/1/2。**恰恰是「深固化放大」最该显形的 N=8/16 几乎没覆盖。**
（不过项目按计划 §7 stop/go 做了 tight-budget 收紧重跑，见 `state/e1_halumem_tightbudget_rerun_20260708.md`——这点**符合**计划的排查纪律。）

### C.2 统计规范：Holm-Bonferroni + α=0.01 —— ⚠️ 已于 07-09 补齐（本节原判过时）
> 更新（2026-07-09）：仓库重组期间新增 `scripts/core/stats_guardrails.py`，**已实现 Holm-Bonferroni(α=0.01) 并接进
> `run_e1_hallucination_statistics.py:288`、`run_e1_multiseed_statistics.py:131`**；TOST 在 `fix_toolkit.py` 已实现。
> 下面原始记录保留作历史，判定应以本更新为准。

（历史记录）
计划 §6 明写「α=0.01 + Holm-Bonferroni 校正预注册主终点」。实际：
- McNemar ✅、bootstrap CI ✅、N 趋势（seed 级 t/sign）✅；
- 但**Holm-Bonferroni 全仓无实现**，唯一出现处是自省报告 `gen_report_ascii.py:136,203`
  白纸黑字写「Holm-Bonferroni 计划有代码无 / 未实现 / 多重比较未校正」；
- 分析脚本硬编码 `sig@0.05`（`run_e1_hallucination_statistics.py:337`），**未用 α=0.01**；
- mixed-effects logistic（计划「where feasible」）未实现。

### C.3 防御只做 2/5（计划 §8 要 5 种）❌
| 计划防御 | 代码 | 状态 |
| --- | --- | --- |
| classifier-only write filter | `safety_write_filter.py`（rules+llm） | ✅ 实现且跑过 |
| provenance-required / no-rewrite | `v3_no_rewrite_policy.py` + read-time meta-policy（122 处引用） | ✅ 实现且跑过 |
| source-trust scoring | 仅枚举占位 1 处 | ❌ 未实现 |
| conservative compaction | 仅枚举占位 1 处 | ❌ 未实现 |
| uncertainty-aware write gate | 仅枚举占位 1 处 | ❌ 未实现 |

### C.4 benchmark 齐备度：E5 压力档缺数据 ❌
| 计划要求 | 盘上 | |
| --- | --- | --- |
| HaluMem-Medium | ✅ `official_repo/data/HaluMem-Medium.jsonl` | |
| HaluMem-Long | ❌ 不在盘上 | E5 无法跑 |
| LongMemEval-S | ✅ `benchmarks/locomo/longmemeval_official` | |
| LongMemEval-V2（官方） | ❌ 只有自建 v2 切片，非官方 V2 数据集 | E5 无法跑 |
| LoCoMo | ✅ | |
攻击家族：compaction poisoning ✅、backdoor trigger ✅；**noisy tool output / biased feedback / conflict update 三类未实现**。
隐蔽投毒套件 30 题（`stealthy_poison_suite_v1.json`），计划 §5 建议「每家族 100 例」——**未达量**。

### C.5 防御判据未闭合（计划 §6：≥25% 相对风险下降 且 ≤3pt 效用损失）
- 风险侧：read-time 防御相对下降约 **15%**（0.90→0.77），**未到 25% 门槛**；
- 效用侧：**LongMemEval-S 效用损失检查没和防御 run 绑定**，判据的第二半根本没测。

---

## D. 最重要的缺口（按补起来的性价比排序）

1. **统计合规**（便宜、高价值）：给现有 McNemar/趋势检验加 **Holm-Bonferroni + α=0.01** 主终点校正；把「无害/等价」主张改 **TOST**。这是审稿必查项，且项目自己已列为「严重」。
2. **RQ3 Pareto 闭合**：把 read-time 防御的同一批 run 接上 LongMemEval-S 良性召回，才能真正回答计划 §6 判据。
3. **RQ2 stage 指标**：要么按计划实现 UNMR/conflict-merge/PAR 的分阶段度量，要么在文档里明确「本项目用 judge 标签替代原 stage 指标」并说明理由。
4. **N 深度补 8/16**（贵）：至少补 tight-budget 下 N=4/8 的多 seed，验证深端是否仍无放大。
5. **RQ4 真算子对比 / E5 压力**（最贵、可延后）：接真 COMEDY/Context-Memory，取 HaluMem-Long / 官方 LongMemEval-V2。

---

## E. 诚实说明：计划已被结论 pivot，「符合标准」要分两层看
- **执行纪律层面**：项目在多处**忠实于计划的严谨要求**——per-item JSONL artifact ✅、bootstrap CI ✅、McNemar ✅、tight-budget stop/go 排查 ✅、judge 终点纪律甚至**超出**计划（计划用词法指标，项目发现词法不可信后升级到 judge）。
- **计划蓝图层面**：因为原假设（固化放大危险/造假记忆）被推翻，计划里为「证明放大」设计的一批实验/指标（深 N-sweep、UNMR/conflict-merge/PAR、压缩家族热力图、5 防御矩阵、E5 压力）**要么部分、要么未做**。这不是「代码写错」，而是**研究转向后这些实验的边际价值下降**——但如果要对外声称「按 v2 计划完成」，上面 C 节的缺口必须补齐或在论文里显式声明替代口径。
