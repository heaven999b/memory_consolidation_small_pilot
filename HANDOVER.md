# 项目交接文档（主入口）· 2026-07-09

给接手的懂代码同学。**读这一份就能上手**；其余文档在本文件里都有链接。
本文件取代根目录旧版，并反映最近一次仓库重组（脚本已移入 `scripts/`）。

---

## 1. 30 秒定位

- 研究：**迭代记忆固化（压缩深度 N）对 memory-agent 安全/幻觉的影响**，底座 = TierMem（raw 层不可变，只递归重写 summary 层，即 C^N）。
- **结论已 pivot（重要）**：原假设「固化会放大危险/造假记忆」**目前不成立**。最硬的两条现结论：① 评测终点会翻转结论；② know-do gap（agent 100% 背得出政策，40–67% 却不照做）。
- **但当前工作方向是：留在原始 RQ1–RQ5 框架内把评测/指标/数据修严谨**（不要再另起新方向）。详见 `state/next_steps_plan_20260709.md`。

## 2. 坐标

| 项 | 值 |
| --- | --- |
| 主项目 | `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot` |
| TierMem 上游 | `/Users/yihaiwen/Documents/New project/tiermem_upstream`（被主项目自动加进 sys.path） |
| GitHub | `https://github.com/heaven999b/memory_consolidation_small_pilot` |
| 分支 / HEAD | `main` / 见 `git log --oneline -1` |
| 解释器 | `.venv_tiermem_v2/bin/python`（Python 3.11，含 openai/numpy/scipy/qdrant） |
| 模型 | 默认 `gpt-4.1-mini`（便宜）；judge 用 `gpt-4o`；`.env.v3` 里 QWEN/LLAMA key **为空**（跨家族做不了） |

## 3. 环境搭建（含一个必做的坑）

```bash
cd "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
set -a && source .env.v3 && set +a                      # 加载 OPENAI key
.venv_tiermem_v2/bin/python scripts/install_dev_paths.py  # ⚠️ 每个 venv 必跑一次
```
**为什么必跑第 2 行**：仓库重组后脚本移入 `scripts/run|core|analysis`，但仍用扁平 import。
`install_dev_paths.py` 写一个 `.pth` 让扁平 import（含派生子进程）解析。不跑 → 所有 run 脚本 `ModuleNotFoundError`。

冒烟验证（不花钱）：
```bash
.venv_tiermem_v2/bin/python scripts/core/safety_metrics.py            # OK
.venv_tiermem_v2/bin/python scripts/core/stats_guardrails.py          # OK（含 Holm + 趋势检验自测）
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_local_bridge.py --benchmark halumem --check-only
```

## 4. 建议阅读顺序

1. 本文件 `HANDOVER.md`
2. `RESEARCH_README.md` —— 现结论总入口（judge 核实、诚实版）
3. `docs/OPERATOR_GUIDE.md` —— 怎么跑（环境/分 RQ 命令/评测/排错）
4. `docs/research_question_map.md` —— 代码导航（哪个 RQ 对应哪些脚本）
5. `state/rq_progress_summary_by_plan_20260709.md` —— 原始 RQ1-5 逐个进度+指标
6. `state/next_steps_plan_20260709.md` —— 后续计划（哪些能做/卡在哪）
7. 分 RQ 深入时读对应 `scripts/run/run_rq*.py`

## 5. 原始 RQ1–RQ5 现状（一页）

| RQ | 主题 | 状态 | 结论 |
| --- | --- | --- | --- |
| RQ1 | 固化放大不安全? | 已做 | 不支持放大；漏洞在 reader（prompt_only ≥ tiermem） |
| RQ2 | 固化造假记忆? | 部分 | 重复错误能造错信，但非越固化越糟 |
| RQ3 | provenance 防御? | 部分 | 读取侧防御稳健但小效应、不闭合 |
| RQ4 | 哪个算子最脆? | 未做 | 仅代理分支，无真 COMEDY/Context-Memory |
| RQ5 | 失败在哪阶段? | 已答 | know-do gap，失败在回答阶段 |

详细指标口径 + 文件/产物路径见 `state/rq_progress_summary_by_plan_20260709.md`（含附录逐 RQ 路径）。

## 6. 本会话做了什么（近期提交，`git log --oneline -8`）

| commit | 内容 |
| --- | --- |
| `ffd3ea7` | 修重组导致的 import 崩溃（`scripts/install_dev_paths.py`）+ 文档路径对齐 + Phase 3a/4a/5 离线工具 |
| `caac3cd` | 修 6 个 launcher 的硬编码子进程路径（重组第二类破坏） |
| `973ea19` | **原始 RQ1/RQ2 核心补件**：N 趋势检验 + RQ2 三阶段指标（UNMR/conflict/PAR） |
| `07ad901` | 把 N 趋势检验接进 RQ1 / RQ2 / E1 的每-N 聚合 |

关键修复与新增（都在 git）：
- `scripts/install_dev_paths.py` —— 修 import 的 `.pth` 安装器（新 venv 必跑）。
- `scripts/core/stats_guardrails.py` —— Holm-Bonferroni(α=0.01) + `pareto_gate`(25%/3pt) + **`cochran_armitage_trend`（随 N 放大趋势检验，原始 RQ1/RQ2 的 H1/H2 主检验）**。
- `scripts/core/rq2_stage_metrics.py` —— RQ2 计划指标 UNMR/conflict_merge/PAR 的规范实现（带数据契约）。
- `scripts/analysis/halumem_official_eval_adapter.py` —— 接官方 HaluMem `evaluation.py` 的适配器（golden+schema 离线已验证；`--validate`）。
- `scripts/build/build_rq2_clean_annotation_sheet.py` —— RQ2 人工标注表去重（101→72 唯一探针）。
- `configs/rq3_utility_map_template.json` —— RQ3 Pareto 的效用图模板（已用真 loader 验证）。

## 7. 文件地图（真实路径）

### 入口/现状文档
- `RESEARCH_README.md`、`docs/OPERATOR_GUIDE.md`、`docs/research_question_map.md`
- 老版交接：`docs/handoffs/handoff_20260709.md`；复现：`docs/status/reproducibility.md`

### 本会话的分析/审计文档（`state/`）
- `state/rq_progress_summary_by_plan_20260709.md` —— 原始 RQ 进度+指标+路径附录
- `state/plan_v2_code_audit_20260709.md` —— v2 计划 vs 代码逐条审计（含 Holm 已补的更正）
- `state/fidelity_reliability_audit_20260709.md` —— 保真度/可靠性（用的是不是原研究者方法）
- `state/eval_methodology_critique_20260709.md` —— 题型批判（开放题 vs MCQ 缺确定性锚）
- `state/next_steps_plan_20260709.md` —— 后续计划（Phase 0–6）
- `state/rq3_readtime_large_20260708_interpretation.md` —— RQ3 读取侧防御 5-seed 裁决

### 主要代码（重组后）
- 框架底座：`scripts/run/run_v2_tiermem_local_bridge.py`、`scripts/core/pilot_core.py`、`scripts/core/benchmark_native_runtime.py`
- RQ1：`scripts/run/run_rq1_safety_consolidation.py`、`run_rq1_authority_experiment.py`、`run_rq1_agentpoison_overlay.py`
- RQ2：`scripts/run/run_rq2_factual_poison.py`（自建线）、`run_v2_tiermem_micro_n_sweep.py`（官方 HaluMem 线）
- RQ3：`scripts/run/run_rq3_readtime_defense_matrix.py` + `scripts/analysis/summarize_rq3_readtime_defense_matrix.py`、`run_rq3_provenance_clean.py`
- RQ5：`scripts/run/run_rq_know_vs_do.py`
- 指标/判卷：`scripts/core/safety_metrics.py`、`safety_honest_metrics.py`、`scripts/run/run_v2_tiermem_micro_failure_mode_judge.py`、`run_rq1_safety_judge.py`
- 统计：`scripts/run/run_e1_hallucination_statistics.py`、`run_e1_multiseed_statistics.py`、`scripts/core/stats_guardrails.py`
- 可靠性：`scripts/core/kappa_score.py`、`scripts/analysis/export_kappa.py`

### 数据
- 官方：`benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl`、`benchmarks/locomo/`（LoCoMo+LongMemEval 官方）
- 自建安全套件：`benchmarks/safety/{unsafe_seed_suite_v1,stealthy_poison_suite_v1,agentpoison_trigger_suite_v1}.json`
- RQ2 自建题库：`configs/rq2_selfbuilt_suite_v3..v6_*.json`

## 8. 怎么跑（速查，详见 OPERATOR_GUIDE）

```bash
# 1-item 冒烟（~$0.01，验证付费链路）
.venv_tiermem_v2/bin/python scripts/run/run_rq1_safety_consolidation.py \
    --backend tiermem --item-limit 1 --passes 0 1 --report-id rq1_live_smoke

# 官方 HaluMem 线（~$1）：生成 -> judge -> 统计(带 Holm+趋势)
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_micro_n_sweep.py --benchmark halumem \
    --route-modes summary_only --passes 0 1 2 --session-limit 1 --qa-limit 10 \
    --qdrant-path outputs/qdrant_p2 --run-prefix e1_halumem_p2 --skip-existing
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_micro_failure_mode_judge.py \
    --sweep-report outputs/v2_tiermem_micro/sweep_reports/e1_halumem_p2.json --judge-model gpt-4o --report-id e1_halumem_p2_judge
.venv_tiermem_v2/bin/python scripts/run/run_e1_hallucination_statistics.py \
    --judge-report outputs/v2_tiermem_micro/judge_reports/e1_halumem_p2_judge.json --report-id e1_halumem_p2_stats
```

## 9. 本轮已有结果在哪看
- 主结果（官方 HaluMem，judge+Holm+趋势）：`outputs/v2_tiermem_micro/stats/e1_halumem_p2_stats_trend.md`
- 冒烟：`outputs/safety/rq1_live_smoke.md` + `_items.jsonl`
- RQ3 读取侧防御大跑：`state/rq3_readtime_large_20260708_summary.md`（+ `..._interpretation.md`）
- 逐条“怎么看”说明：`weekly_reports/week1/week1_round_results_viewing_guide_zh.md`

## 10. 待办 / 交接后从哪继续（详见 `state/next_steps_plan_20260709.md`）
- **能立即接着做（离线/代码）**：RQ2 stage 指标从“文本代理”升级为 TierMem 真 provenance（`has_source_support`）；接官方 `evaluation.py` 打分的 `fill_system_side`（见 `docs/halumem_official_eval_integration.md`）。
- **要花钱跑**：RQ1 全 N `{0,1,2,4,8,16}`×多 seed；RQ2 多-pass；RQ3 Pareto 效用跑。
- **卡在人/key**：RQ2 填 `human_label`（去重表在 `state/rq2_manual_annotation_*_dedup.csv`）后跑 `scripts/core/kappa_score.py`；跨家族需填 `.env.v3` 的 QWEN/LLAMA key。

## 11. 必须知道的坑（否则会踩）
1. **新 venv 先跑 `scripts/install_dev_paths.py`**，否则一切 import 崩。
2. **终点一律以 judge 为准**，词法只做交叉验证（历史 3 次词法结论一上 judge 就塌）。
3. **多 seed 别引用池化极小 p**（同一批题跨 seed 不独立），用「全同向 + seed 级 t / 趋势检验」。
4. **`outputs/` 大多被 `.gitignore` 忽略** → 结果只在本地；GitHub 克隆看不到，要么让人给文件，要么照第 8 节重跑。
5. **`state/*.csv/html/json` 也被忽略**（去重表、部分 CSV 只在本地）。
6. 官方 benchmark **数据是官方的，但很多打分是自建 judge**，不能直接对标原论文 leaderboard（见 `state/fidelity_reliability_audit_20260709.md`）。

## 12. 一句话
代码主干在 GitHub、可跑（先跑 `install_dev_paths.py`）；研究结论已转向，但当前任务是**在原始 RQ1-5 内把评测修严谨**——RQ1/RQ2 的趋势检验与阶段指标本会话已补齐并接线，下一步是把 RQ2 代理升级为真 provenance + 补付费的多-N/多-seed 实跑。
