# 接官方 HaluMem evaluation.py 打分（Phase 3 集成说明）

目标：让幻觉线用**官方指标**（memory integrity / accuracy / update / QA）打分，不再只用自建 judge。

## 契约（读 `evaluation.py` + `eval_memos.py` 得到）
官方按 per-user→sessions 读数据。**gold 字段全部由 HaluMem-Medium 直接提供**，系统只需填 **3 个字段**：

| 字段 | 位置 | 类型 | 含义 |
| --- | --- | --- | --- |
| `extracted_memories` | 每个 session | list[str] | 系统为该 session 抽取的记忆（喂 memory integrity/accuracy） |
| `memories_from_system` | `is_update=="True"` 的 memory_point | list[str] | 系统对该 memory_content 的检索结果（喂 memory update） |
| `system_response` | 每个 question | str | 系统对 gold question 的回答（喂 QA，evaluation 读 `qa["system_response"]`） |

其余 `question/answer/evidence/memory_content/...` 都是 gold，原样透传。

## 三步跑法
```bash
# 1) 离线：校验契约 + 产出 skeleton（零 API，已验证 schema_problems=0）
$PY scripts/analysis/halumem_official_eval_adapter.py --validate --user-limit 2

# 2) 付费：用 TierMem 填 3 个系统字段（先把 fill_system_side 接到 run_v2_tiermem_local_bridge）
$PY scripts/analysis/halumem_official_eval_adapter.py --live --user-limit 2 \
    --output outputs/halumem_official/tiermem_filled_u2.jsonl

# 3) 付费：官方打分（内部调 LLM）
$PY benchmarks/halumem/official_repo/eval/evaluation.py \
    --file_path outputs/halumem_official/tiermem_filled_u2.jsonl \
    --output_file outputs/halumem_official/scores_u2.json
```

## 成本与规模
官方全量 = **20 users / 1387 sessions / 3467 QA / 3122 update 记忆**。全量 live+打分很贵，
**先用 `--user-limit 2`（~几百 QA）验证跑通**，再决定放大。

## 现状（诚实）
- ✅ 离线可验证部分已完成：golden 加载 + 输出 schema 校验（`--validate` 全绿）。
- ⏳ `fill_system_side` 是**唯一未接的付费集成点**——需把它连到 `run_v2_tiermem_local_bridge` 的
  write/search/answer；因为无法离线验证，故留成明确接口，接好后先小规模 `--user-limit 2` 验证。
