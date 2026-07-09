#!/bin/bash
# 过夜 E1 HaluMem 多 seed × 多 persona N-sweep(验 pilot 的 escalation fab 信号是否跨 persona/seed 稳)
# 两架构串行跑(绝不并行——同 persona 会踩同一 Qdrant index、卡死)。
# 每架构: 3 persona × 2 seed × N{0,1,2}。summary_only(纯压缩) vs auto(TierMem escalation)。
set -e
cd "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
set -a && source .env.v3 && set +a
PY=.venv_tiermem_v2/bin/python
COMMON="--benchmark halumem --seeds 11 23 --passes 0 1 2 --session-limit 3 --qa-limit 15"

echo "=== [$(date '+%m-%d %H:%M')] OVERNIGHT E1 START ==="
echo "=== [$(date '+%m-%d %H:%M')] 架构 1/2: summary_only 开始 ==="
$PY run_e1_multiseed_sweep.py $COMMON --route-mode summary_only || echo "!! summary_only sweep 出错(继续 auto)"

echo "=== [$(date '+%m-%d %H:%M')] 架构 2/2: auto(escalation) 开始 ==="
$PY run_e1_multiseed_sweep.py $COMMON --route-mode auto || echo "!! auto sweep 出错"

echo "=== [$(date '+%m-%d %H:%M')] OVERNIGHT_E1_DONE ==="
echo "明早聚合: run_e1_multiseed_statistics.py --manifest <各架构 multiseed manifest>"
