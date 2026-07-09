# 本轮结果怎么看（给没看过这个项目的人）· 2026-07-09

项目根目录：`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot`
所有路径都相对这个根目录。`.md` 用任意编辑器/Markdown 预览打开（或终端 `cat`）；`.jsonl` 是每行一个 JSON；`.csv` 用 Excel/Numbers 打开。

---

## 0. 只看一个文件的话，看这个

**`outputs/v2_tiermem_micro/stats/e1_halumem_p2_stats.md`**

这是本轮的**主结果**：在官方 HaluMem 数据上，随记忆固化深度 N（0/1/2）变化的幻觉/正确率，经 LLM judge 打分 + Holm 多重比较校正（α=0.01）。终端直接看：
```bash
cat outputs/v2_tiermem_micro/stats/e1_halumem_p2_stats.md
```

怎么读那张表（每列含义）：
| 列 | 意思 | 想看到 |
| --- | --- | --- |
| `N` | 固化深度（做了几轮压缩） | — |
| `correct_rate` | 答对比例（judge 判 CORRECT） | 越高越好 |
| `UF_on_unknown` | 该抱歉说“不知道”却**乱编**的比例 | 越低越好 |
| `AF_on_factual` | 该答却**弃答/忘了**的比例 | 越低越好 |
| `FD_on_factual` | 答了但**把事实说歪**的比例 | 越低越好 |
| 中括号 `[.. , ..]` | 95% 置信区间 | — |
| `Holm p` / `sig@alpha Holm` | 多重比较校正后的显著性(α=0.01) | `yes`=稳 |

**本轮这张表说了什么**（一句话）：`correct_rate` 0.60→0.80、`FD_on_factual` 0.50→0.25 —— **固化没有把幻觉搞得更糟，反而略好**；但样本只有 10 题、单 seed，Holm 校正后都不显著（属“功效不足”，不是“无效应”）。所以它是**流程跑通的 pilot**，不是能写进论文的定论。

---

## 1. 本轮全部结果文件（按 Phase）

### Phase 1 · Live 冒烟（验证真实付费链路能跑）
- `outputs/safety/rq1_live_smoke.md` —— SRR/UAF 表（安全轴指标随 N）。
- `outputs/safety/rq1_live_smoke_items.jsonl` —— 逐条明细。看这里能确认“真的跑了”：
```bash
# 看每条的答案 + 固化后的记忆文本（N=0 是原始对话，N=1 变成压缩摘要=C^N 真的生效）
python3 -c "import json;[print('N=',r.get('passes'),'|',str(r.get('answer_text',''))[:80]) for r in map(json.loads, open('outputs/safety/rq1_live_smoke_items.jsonl'))]"
```

### Phase 2 · 官方 HaluMem 线（本轮主结果，三步产物）
1. 生成：`outputs/v2_tiermem_micro/sweep_reports/e1_halumem_p2.md`（模型对每道官方 HaluMem 题的原始回答）
2. 判卷：`outputs/v2_tiermem_micro/judge_reports/e1_halumem_p2_judge.md`（gpt-4o 判每条属 CORRECT / 乱编 / 弃答 / 歪曲）
3. 统计：`outputs/v2_tiermem_micro/stats/e1_halumem_p2_stats.md`（**上面第 0 节那张表**，带 Holm）

想看模型到底答了啥（最直观）：
```bash
grep -A4 '"question"' outputs/v2_tiermem_micro/sweep_reports/e1_halumem_p2.md | head -20
```

### Phase 3a · 官方评测适配器（离线验证，零花费）
不是一个结果文件，是一个**能跑的校验命令**。跑它=证明我们的输出格式和官方 `evaluation.py` 对得上：
```bash
.venv_tiermem_v2/bin/python scripts/analysis/halumem_official_eval_adapter.py --validate
# 期望输出: "schema_problems": 0  +  "Schema OK"
```

### Phase 4a · RQ2 待标注表（去重后，等你打标）
- `state/rq2_manual_annotation_core_zh_dedup.csv`（+ `_diverse_zh_dedup.csv`、`_v4_tiermem_diverse_zh_dedup.csv`）
- 用 Excel 打开，`human_label` 列是空的、留给人填；`dedup_group_size` 表示这条代表了几条重复。

### Phase 5 · RQ3 效用图模板
- `configs/rq3_utility_map_template.json` —— 里面全是 `null` 占位，`_README` 字段讲怎么填。

---

## 2. 怎么把本轮从零复现一遍（想自己跑）

```bash
cd "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
set -a && source .env.v3 && set +a
.venv_tiermem_v2/bin/python scripts/install_dev_paths.py     # 每个 venv 一次

# Phase 1 冒烟（~$0.01）
.venv_tiermem_v2/bin/python scripts/run/run_rq1_safety_consolidation.py \
    --backend tiermem --item-limit 1 --passes 0 1 --report-id rq1_live_smoke

# Phase 2 官方线（~$1）：生成 -> 判卷 -> 统计
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_micro_n_sweep.py \
    --benchmark halumem --route-modes summary_only --passes 0 1 2 \
    --session-limit 1 --qa-limit 10 --qdrant-path outputs/qdrant_p2 \
    --run-prefix e1_halumem_p2 --skip-existing
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_micro_failure_mode_judge.py \
    --sweep-report outputs/v2_tiermem_micro/sweep_reports/e1_halumem_p2.json \
    --judge-model gpt-4o --report-id e1_halumem_p2_judge
.venv_tiermem_v2/bin/python scripts/run/run_e1_hallucination_statistics.py \
    --judge-report outputs/v2_tiermem_micro/judge_reports/e1_halumem_p2_judge.json \
    --report-id e1_halumem_p2_stats
```
> 注意：`outputs/` 大多被 `.gitignore` 忽略，所以这些结果**只在本地**，git 里看不到；要复现就照上面跑。

---

## 3. 本轮改了哪些代码（在 git 里看）

```bash
git log --oneline -2
#   caac3cd  Fix hardcoded subprocess script paths broken by the reorg
#   ffd3ea7  Fix reorg imports, align docs, add Phase 3a/4a/5 offline tooling
git show ffd3ea7 --stat     # 看这两个 commit 具体动了哪些文件
```

## 4. 背景（想先懂项目再看结果）
按顺序读：`RESEARCH_README.md`（结论）→ `docs/OPERATOR_GUIDE.md`（怎么跑）→ `state/next_steps_plan_20260709.md`（后续计划）。
一句话现状：原假设“固化会放大危险/幻觉”**已被推翻**；本轮的官方 HaluMem pilot 又给了同方向的一个数据点（固化没放大幻觉）。
