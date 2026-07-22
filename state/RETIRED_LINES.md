# 已封存/退休的研究线 · 2026-07-19

> 这些线**已判负或已停止投入**。文件**保留不删**——它们被周报和 README 引用着（删除会造成断链），且体积很小。
> 目的：防止未来窗口重新捡起来做，或误以为它们是活跃线。

## RT-01 / ConsolidationBench（已判负，2026-07-13~14）

**构思**：用 `Δ_op = S(固化开) − S(固化关)` 把记忆漂移归因到固化算子本身。

**实测结果 = NULL**：
- 默认保真算子 `Δ_op = 0.000`
- 激进 lossy 算子 `Δ_op = −0.058`，95% CI [−0.175, 0.0]（跨 0）
- 只有 1/12 真侵蚀

**判定**：主效应为 null，保留为**测量有效性负结果**。明确**不建议**扩成 A-MEM / Mem0 / MemoryBank 全套工程。

**相关文件（保留）**：
- `state/consolidationbench_idea_zh_20260713.md`、`..._en_20260713.md`
- `state/consolidationbench_pilot_20260713.json`、`..._lossy_20260713.json`
- `scripts/run/run_consolidationbench_pilot.py`

**被引用于**（这是不删的原因）：`weekly_reports/week2/week2_report_20260713_zh.md` §9、`RESEARCH_README.md`、`weekly_reports/README.md`、`weekly_reports/week2/README.md`、`weekly_reports/week2/research_topics/README.md`、`HANDOVER_memop_20260713.md`

## RT-02 内部已退休的 RQ（2026-07-19）

见 `state/rt02_paper_gap_checklist_20260719.md` §1：

- **RQ2**（G 超越 TrustMem）：对手指标退化成常数、无官方代码 → 退休，并入 RQ1 作"vs 可得 baseline"
- **RQ4**（selective closure 可行性）：每 case 仅 3 descendants，预算门与方法无关地不可达 → 退休；过拟合发现（dev 1.0→held-out 0.412）降级为 Paper B 的限制
- **RQ5**（适用边界全矩阵）：缩到 k / 域 / NLI checkpoint 三轴

## 不属于 RT-02、本轮未触碰

`scripts/run/` 下的 memop（`run_memop_*.py`）、E1（`run_e1_*.py`）、rq1/rq2 retest 等属于**其他研究线**，本轮清理一概未动。
