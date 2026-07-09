#!/bin/bash
# 轻量全覆盖 E1(RQ2/RQ3/RQ5): 20 session 全覆盖 × 每 session 前 15 QA = 300 QA,
# N{0,1,2}, 单 seed 11, 双架构串行(summary_only 纯压缩 vs auto=TierMem escalation)。
# 目的: 把 RQ2/3/5 从 3-session/45-QA pilot 拉到 20-session 全 persona 覆盖, 先探全量信号。
# 两架构串行跑(不并行, 控 API 并发 + 稳)。write-infer 是瓶颈, 预计 6-10h。
cd "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
set -a && source .env.v3 && set +a
PY=.venv_tiermem_v2/bin/python
COMMON="--benchmark halumem --seeds 11 --passes 0 1 2 --session-limit 20 --qa-limit 15 --no-sample-qa --qa-max-workers 8 --write-max-workers 3"
mkdir -p logs
{
echo "=== LIGHT FULL-COVERAGE E1 START $(date '+%m-%d %H:%M') ==="
echo "=== 20 session × 15 QA = 300 QA | N{0,1,2} | seed 11 | workers qa=8/write=3 ==="
echo ""
echo "--- 架构 1/2: summary_only 开始 $(date '+%H:%M') ---"
$PY run_e1_multiseed_sweep.py $COMMON --route-mode summary_only --run-prefix e1_lightfull_summary || echo "!! summary_only 出错(继续 auto)"
echo "--- 架构 1/2: summary_only 完成 $(date '+%H:%M') ---"
echo ""
echo "--- 架构 2/2: auto 开始 $(date '+%H:%M') ---"
$PY run_e1_multiseed_sweep.py $COMMON --route-mode auto --run-prefix e1_lightfull_auto || echo "!! auto 出错"
echo "--- 架构 2/2: auto 完成 $(date '+%H:%M') ---"
echo ""
echo "=== LIGHTFULL_E1_DONE $(date '+%m-%d %H:%M') ==="
echo "聚合命令:"
echo "  $PY run_e1_multiseed_statistics.py --manifest outputs/v2_tiermem_micro/multiseed/e1_lightfull_summary_manifest.json"
echo "  $PY run_e1_multiseed_statistics.py --manifest outputs/v2_tiermem_micro/multiseed/e1_lightfull_auto_manifest.json"
} 2>&1 | tee -a logs/e1_lightfull.log
