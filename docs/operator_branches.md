# Operator Branches

这次单独开的两个支线，不是“换研究问题”，而是“在同一 RQ 上换压缩/记忆管理方式做对照”。

## 支线 1: `COMEDY-style`

- 入口: `run_branch_comedy_control.py`
- 核心近似:
  - 强制走 `summary_only`
  - 继续用文本压缩
  - 把原来的 `TierMem` 压缩 prompt 换成更整体、更会融合“事实 + 关系 + 过往事件”的 `comedy_style`
  - 关闭研究阶段写回摘要层
- 这条线回答的问题:
  - 如果压缩器更“整体化”“会总结气氛和关系”，RQ1/RQ2 会不会更容易出问题

### 例子

```bash
.venv_tiermem_v2/bin/python run_branch_comedy_control.py --task rq2_selfbuilt --suite-version v6 --repetition 3 --query-modes free forced_choice --passes 0 1 2
```

```bash
.venv_tiermem_v2/bin/python run_branch_comedy_control.py --task rq1_agentpoison --item-limit 10 --passes 0 1 2
```

## 支线 2: `E-mem-style`

- 入口: `run_branch_emem_control.py`
- 核心近似:
  - 强制 `passes=0`
  - 强制走 `research_only`
  - `page_write_mode=raw`
  - 关闭研究阶段写回摘要层
  - 开 `abstain_on_unsupported`
- 这条线不是字面复现 E-mem 的多 agent 架构，而是抓住它最关键的对照思想:
  - `尽量不做预压缩`
  - `更多依赖原文片段和回答时重建`

### 例子

```bash
.venv_tiermem_v2/bin/python run_branch_emem_control.py --task rq2_selfbuilt --suite-version v6 --repetition 3 --query-modes free forced_choice
```

```bash
.venv_tiermem_v2/bin/python run_branch_emem_control.py --task rq1_safety --item-limit 12
```

## 任务映射

- `rq1_safety`: `run_rq1_safety_consolidation.py`
- `rq1_authority`: `run_rq1_authority_experiment.py`
- `rq1_agentpoison`: `run_rq1_agentpoison_overlay.py`
- `rq2_selfbuilt`: `run_rq2_factual_poison.py`

## 现在的解释边界

- `COMEDY-style` 是“文本压缩算子对照”，不是 COMEDY 原论文的完整系统复现。
- `E-mem-style` 是“反压缩 / 原文优先对照”，不是 E-mem 原论文的完整多 agent 复现。
- 这样做的目的是先回答你最关心的问题:
  - `是不是压缩方式本身，让 RQ1/RQ2 看起来偏负或偏弱`
