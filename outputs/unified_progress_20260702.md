# 统一进展汇报（截至 2026-07-02）

## 1. 本次整合使用的材料

直接材料：

- `/Users/yihaiwen/Desktop/已测结果汇总.docx`
- `/Users/yihaiwen/Desktop/演示文稿1.pptx`
- `/Users/yihaiwen/Desktop/第一周汇报_week1_report.pptx`

核对用仓库材料：

- `docs/week1_delivery_status.md`
- `state/locomo_summary_only_findings_20260701.md`
- `state/locomo_summary_only_q30_findings_20260701.md`
- `state/e1_halumem_targeted_cov10_block1_20260701.md`
- `state/e1_halumem_targeted_cov10_block2_multisession3_20260701.md`
- `state/e1_halumem_route_comparison_blockAB_20260701.md`
- `state/e1_halumem_provenance_abstain_gate_stage1_20260702.md`
- `state/e1_halumem_structured_grounding_gate_stage1_20260702.md`
- `outputs/v2_tiermem_micro/sweep_reports/e4_halumem_auto_multisession3_structsig_off_20260702.md`
- `outputs/v2_tiermem_micro/sweep_reports/e4_halumem_auto_multisession3_structsig_on_20260702.md`

版本核对结论：

- 桌面版 `已测结果汇总.docx` 与仓库内同名文件不是同一个版本。
- 桌面版 `第一周汇报_week1_report.pptx` 与仓库内同名文件也不是同一个版本。
- `演示文稿1.pptx` 当前只在桌面，仓库里没有对应副本。

## 2. 一句话总览

截至 2026 年 7 月 2 日，`memory_consolidation_small_pilot` 已经完成了 TierMem 路径的 Week 1 通路验证、LoCoMo 的 benign utility 轴检查、HaluMem 的 summary-only 深度实验、summary/auto/research 三路对照，以及三版“防无依据瞎编”的 gate 尝试。当前最值得主推的真实结果是：结构化 grounding gate 在 HaluMem 上显著降低了 unknown 题上的无依据编造，而且没有引入新的 factual 弃答。

## 3. 目前可以稳定汇报的进展

### 3.1 Week 1 / E0 已完成

- TierMem fork、本地 bridge、公共记忆 API、三种 route 配置、artifact schema 已全部落地。
- tiny synthetic Week 1 matrix 已跑通，`raw_only / summary_only / summary_plus_raw` 在 `N=0/1` 共 6 个 run 的通路验证通过。
- 这部分可以视为“工程可跑通”已完成，不再是当前 blocker。

依据：

- `docs/week1_delivery_status.md`
- `第一周汇报_week1_report.pptx`

### 3.2 LoCoMo utility 轴：深度基本不改变效用，但显著增加成本

30 QA 的早期结论已经被 100 QA 结果推翻，不应再引用倒 U 说法。

权威 100 QA 结果：

| N | F1 |
| --- | ---: |
| 0 | 0.286 |
| 1 | 0.300 |
| 2 | 0.303 |

当前可说法：

- consolidation depth 在 LoCoMo 上没有显著 utility 增益，曲线基本平。
- `N=0 -> N=1/2` 大约把成本提升到 3 倍，但没有带来可观的答题收益。
- 这条轴上的方法学结论已经比较稳定：30 QA 的小样本形状不可信，至少要到 100 QA 才能判断。

依据：

- `state/locomo_summary_only_findings_20260701.md`
- `state/locomo_summary_only_q30_findings_20260701.md`

### 3.3 HaluMem summary-only：一次固化像降噪，更深固化主要带来失败模式迁移

单 session，15 QA：

| N | F1 | Correct | AF on factual | UF on unknown | FD on factual |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.205 | 0.533 | 0.333 | 0.333 | 0.222 |
| 1 | 0.205 | 0.667 | 0.333 | 0.167 | 0.111 |
| 2 | 0.189 | 0.400 | 0.444 | 0.167 | 0.444 |
| 4 | 0.162 | 0.467 | 0.444 | 0.167 | 0.333 |

三 session，45 QA：

| N | F1 | Correct | AF on factual | UF on unknown | FD on factual |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.185 | 0.333 | 0.394 | 0.333 | 0.394 |
| 1 | 0.210 | 0.533 | 0.364 | 0.083 | 0.242 |
| 2 | 0.215 | 0.422 | 0.455 | 0.083 | 0.303 |
| 4 | 0.206 | 0.489 | 0.303 | 0.083 | 0.364 |

当前可说法：

- `N=1` 的主要效果是降 unsupported fabrication。
- 更深固化没有把 unsupported fabrication 再拉回来，但会把错误转移成 factual forgetting / factual distortion。
- 在 45 QA 上，这个“failure-mode migration”比“明显的 utility 倒 U”更可信。

依据：

- `state/e1_halumem_targeted_cov10_block1_20260701.md`
- `state/e1_halumem_targeted_cov10_block2_multisession3_20260701.md`

### 3.4 raw escalation 不是自动更安全，当前 auto 也不是理想 hybrid

单 session，15 QA，summary vs auto vs research：

| Route | N | F1 | Correct | AF | UF | FD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| summary_only | 0 | 0.205 | 0.600 | 0.333 | 0.333 | 0.111 |
| summary_only | 1 | 0.205 | 0.667 | 0.333 | 0.167 | 0.111 |
| summary_only | 2 | 0.189 | 0.533 | 0.444 | 0.167 | 0.222 |
| auto | 0 | 0.225 | 0.733 | 0.000 | 0.333 | 0.222 |
| auto | 1 | 0.194 | 0.533 | 0.000 | 0.667 | 0.333 |
| auto | 2 | 0.241 | 0.600 | 0.000 | 0.667 | 0.222 |
| research_only | 0 | 0.266 | 0.733 | 0.000 | 0.333 | 0.222 |
| research_only | 1 | 0.188 | 0.533 | 0.000 | 0.833 | 0.222 |
| research_only | 2 | 0.148 | 0.400 | 0.111 | 0.833 | 0.333 |

当前可说法：

- `research_only` 起点高，但随着深度增加退化最快。
- `auto` 在这一轮更像 `R-heavy noisy hybrid`，而不是安全地“先 summary，必要时再 raw”。
- 这条结果很重要，因为它推翻了“回原文天然更 faithful”这个直觉。

依据：

- `state/e1_halumem_route_comparison_blockAB_20260701.md`
- `演示文稿1.pptx`

### 3.5 Gate 方向已经出现真正有希望的正结果

这里的三个 gate 先用大白话解释一下：

- `gate v1`：第一版“关键词 provenance 弃答门”。做法是看 research / coverage 文本里有没有“不支持作答”的关键词，如果命中就强制改成弃答。
- `gate v2`：第二版“收紧关键词后的 provenance 弃答门”。它是在 `v1` 基础上收紧触发条件，尽量避免把本来答得对的否定题也错杀成弃答。
- `structured grounding gate`：不用字符串关键词，而是让模型先显式给出 `answer_grounded = true / false`。只有当模型自己判定“这答案没有证据支撑”时，才触发弃答。

#### 3.5.1 关键词 provenance 弃答门 v1 / v2：有方向，但还不能算通过

| Condition | F1 | Correct | AF | UF | FD |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline auto N=1 | 0.194 | 0.533 | 0.000 | 0.667 | 0.333 |
| gate v1 | 0.205 | 0.533 | 0.333 | 0.333 | 0.222 |
| gate v2 | 0.228 | 0.533 | 0.000 | 0.667 | 0.333 |

当前可说法：

- `v1` 说明“看到不支持信号就弃答”这个方向是可能有效的，因为它确实压低了 unknown 题上的乱猜。
- 但 `v1` 的问题是太猛了，连一些其实答对了的 factual 否定题也一起打成弃答。
- `v2` 就是为了解这个问题而做的收紧版；它把误杀修掉了，但同时也把主要收益修没了。
- 所以这两版仍然只是探索性尝试，不能当成已经成立的防御机制。

依据：

- `state/e1_halumem_provenance_abstain_gate_stage1_20260702.md`

#### 3.5.2 结构化 grounding gate：这是当前最强结果

单 session，15 QA，`N=1`：

| Condition | F1 | Correct | AF | UF | FD |
| --- | ---: | ---: | ---: | ---: | ---: |
| no gate | 0.258 | 0.467 | 0.000 | 0.833 | 0.333 |
| structured gate | 0.262 | 0.733 | 0.000 | 0.167 | 0.333 |

当前可说法：

- 这一版不再靠关键词猜，而是先让模型明确回答“我这个答案有没有证据支撑”。
- 当模型自己给出“不支撑”时，系统才强制弃答。
- 结果是 unknown 题上的 unsupported fabrication 从 `5/6` 降到 `1/6`。
- factual 侧没有新增 abstain forgetting。
- 这是目前整个项目里最接近“真正防御机制成立”的一条真实证据。

依据：

- `state/e1_halumem_structured_grounding_gate_stage1_20260702.md`

## 4. 这三份材料里缺的、没记录的、或者容易混淆的地方

### 4.1 缺的 / 没记录的

1. `演示文稿1.pptx` 只在桌面，不在仓库里。
2. 三份材料里没有一张真正统一的“样本量 / 指标 / route / N / 结论 / caveat / 证据路径”总表。
3. 各份材料里对 gate 的叫法不统一，有的写 `auto`、有的写 `gate`、有的直接写 `v1/v2`，如果不给解释，外人很难看懂。

### 4.2 容易混淆的版本问题

1. 桌面版 `已测结果汇总.docx` 在正式汇总后面追加了一大段临时分析文字。
2. 桌面版 `第一周汇报_week1_report.pptx` 比仓库版更新，仓库版多出一页“对照 PDF 交付物”的 slide，桌面版已经移除了这页。

### 4.3 证据卫生问题

1. synthetic dry-run 图表在仓库里仍然存在，但不能和真实 TierMem/HaluMem 结果混用。
2. `pyserini` 仍未安装，BM25 仍是简单匹配回退，这个 caveat 应保留在正式汇报里。
3. 当前所有真实结果仍然只有单 seed、单 backbone、无显著性检验。

## 5. 建议你接下来怎么收口

如果目标是“给别人看一份当前进展汇报”，建议按下面顺序整理：

1. 把这份文件当作新的文字底稿。
2. 在正式版汇报里保留 5 条主结论：
   - Week 1 / E0 已完成。
   - LoCoMo 100 QA 证明 utility 轴基本平，30 QA 倒 U 已被证伪。
   - HaluMem summary-only 的稳定现象是 `N=1` 降 UF，更深 N 迁移为 factual 失败。
   - raw escalation 不是自动更安全，当前 auto 也不是理想 hybrid。
   - structured grounding gate 是当前最强结果。
3. 把 `演示文稿1.pptx` 里的三张补充表并回正式 PPT，或者至少把它也放进仓库。
4. 清掉 `已测结果汇总.docx` 后半段聊天式草稿，避免外发时把临时分析和正式结论混在一起。
5. 如果后面还要继续补实验，建议再单独做新一轮结果更新，不要把“刚跑出来但还没整理”的东西直接塞进当前正式汇报。

## 6. 当前最适合对外说的总述

目前项目已经从“通路是否能跑通”推进到“哪种机制真正降低幻觉”的阶段。稳定结论是：单纯增加压缩深度不会带来明显的 benign utility 收益，但会改变 HaluMem 上的失败模式；单纯回原文也不是自动更安全。当前最值得讲的正结果是结构化 grounding gate：它在 15 QA 上显著压低了 unknown 题上的无依据编造，而且没有引入新的 factual 弃答。对外汇报时，建议先把这个结果讲清楚，再把前两版 gate 作为失败但有信息量的探索过程补充说明。
