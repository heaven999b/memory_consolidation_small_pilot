# 后续步骤计划（2026-07-09）

标注约定：🟢=离线/零 API，🟡=少量 API（几分~几刀），🔴=较贵或需人工/需 key。
✅DONE=本轮我已做；▶YOU=需要你跑（花钱/人工）；🤖CAN=简单离线、你说一声我就做。

前置（每个新终端）：
```bash
cd "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
set -a && source .env.v3 && set +a
.venv_tiermem_v2/bin/python scripts/install_dev_paths.py   # 每个 venv 一次即可
```

---

## Phase 0 · 修复与合规校准 —— ✅DONE（本轮，🟢零 API）
- 修好重组导致的导入崩溃：新增 `scripts/install_dev_paths.py`（写 `.pth`），全 run 脚本 import 0 失败、全树编译通过。
- 文档对齐：`RESEARCH_README.md` §6、`docs/OPERATOR_GUIDE.md` 命令路径全部改到 `scripts/run|core|analysis`。
- **修正早先审计**：统计合规其实重组期间已补齐 —— `stats_guardrails.py` 的 **Holm-Bonferroni(α=0.01)** 已接进 `run_e1_hallucination_statistics.py:288` 与 `run_e1_multiseed_statistics.py:131`；**pareto_gate(25%/3pt)** 已接进 `run_rq3_provenance_clean.py:386`；**TOST** 在 `fix_toolkit.py` 已实现并被 rq1 retest 用。
- 离线重生成带 Holm 的 E1 统计：`outputs/v2_tiermem_micro/stats/e1_stats_holm_20260709.md`（含 `Holm p`/`sig@alpha Holm` 列）。

---

## Phase 1 · Live 冒烟（1-item） —— ▶YOU（🟡~$0.01）
验证真实付费链路 write→C^N→answer 通不通，再谈全量。
```bash
.venv_tiermem_v2/bin/python scripts/run/run_rq1_safety_consolidation.py \
    --backend tiermem --item-limit 1 --passes 0 1 --report-id rq1_live_smoke
```
**判健康 3 点**：① `outputs/safety/rq1_live_smoke*.json` 生成、rc=0、无 traceback；② `*_items.jsonl` 有真实答案文本；③ `consolidated_text` 非空、SRR/UAF 有值。
→ 把输出贴给我，我判健康度。

## Phase 2 · 一条完整管线端到端（证明 sweep→judge→stats 全通） —— ▶YOU（🟡~$2–5）
smoke 干净后，跑一条**官方 HaluMem 线**的小全量，顺带把 judge+Holm 统计走一遍：
```bash
# 1) 生成（真官方数据，summary_only，N=0/1/2）
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_micro_n_sweep.py \
    --benchmark halumem --route-modes summary_only --passes 0 1 2 \
    --session-limit 1 --qa-limit 15 --qdrant-path outputs/qdrant_p2 \
    --run-prefix e1_halumem_p2 --skip-existing
# 2) 失败模式 judge
.venv_tiermem_v2/bin/python scripts/run/run_v2_tiermem_micro_failure_mode_judge.py \
    --sweep-report outputs/v2_tiermem_micro/sweep_reports/<上一步产出>.json \
    --judge-model gpt-4o --report-id e1_halumem_p2_judge
# 3) 统计（🟢零 API，出 Holm 表）
.venv_tiermem_v2/bin/python scripts/run/run_e1_hallucination_statistics.py \
    --judge-report outputs/v2_tiermem_micro/judge_reports/e1_halumem_p2_judge_net.json
```
产出即「一条能对外展示的、judge 终点 + Holm 校正」的完整结果。

## Phase 3 · 接官方 HaluMem evaluation.py 打分（对齐原 benchmark） —— 🔴（适配器🟢 + 打分🟡~$5）
审计里最高 ROI 的对齐项：让幻觉线能用官方 `memory_integrity/accuracy/interference` 指标，不再只用自建 judge。
- 3a 🤖CAN：写一个适配器，把我们的 run 产物转成 `benchmarks/halumem/official_repo/eval/evaluation.py` 的输入格式（离线、我可做，中等工作量）。
- 3b ▶YOU：跑官方 `evaluation.py` 打分（它内部调 LLM，花钱）。
→ 你要的话我先做 3a 的适配器 + dry 验证。

## Phase 4 · RQ2 人工标注 + kappa（把 RQ2 从「不可信」拉起来） —— 🔴（人工 + 一条命令）
现状：`state/rq2_manual_annotation_*_zh.csv` 的 `human_label` 还全空。
- 4a 🤖CAN：确认标注表就绪、去重（避免有效 n 虚高），生成干净待标注表。
- 4b ▶YOU（人工）：填 `human_label`。
- 4c 🟢：`python3 scripts/core/kappa_score.py` 出 κ（RQ1 已有 κ=0.85 范式可复用）。

## Phase 5 · RQ3 Pareto 闭合（回答「≥25% 风险↓ 且 ≤3pt 效用↓」） —— 🔴（🟡~$5–15）
`pareto_gate` 已接进 `run_rq3_provenance_clean.py`，缺的是**把 LongMemEval-S 良性召回喂进去**当效用侧。
- ▶YOU：跑 `run_rq3_provenance_clean.py` 时带 `--utility-map`（把防御 run 与良性效用配对），让 gate 真出 promising 判定。
→ 具体 `--utility-map` 怎么构造我可以先写好模板（🤖CAN）。

## Phase 6 · 跨家族复现 + 收尾 —— 🔴（需 key / 需你确认）
- 6a ▶YOU：`.env.v3` 填 `QWEN_*`/`LLAMA_*` key → know-do、RQ3 换 backbone 复现（审稿必问的普适性）。
- 6b 🤖CAN：把 `state/` 与 `docs/state/` 并轨统一、把本轮新增文档（install 脚本、指南、审计、本计划）**提交 git**（需你一句「提交」）。

---

## 一句话推荐路径
**Phase 1 冒烟 → Phase 2 一条完整官方线 → Phase 3 官方打分**（这三步走完，幻觉线就从「自建口径 pilot」升级成「官方数据 + 官方指标 + Holm 校正」，是性价比最高的主升级）。RQ2 kappa（Phase 4）和 RQ3 Pareto（Phase 5）可并行插空做。跨家族（Phase 6）等有 key 再说。

> 我能马上帮你做的（你点一下就行）：Phase 3a 适配器、Phase 4a 标注表清洗、Phase 5 的 `--utility-map` 模板、Phase 6b 提交 git。
