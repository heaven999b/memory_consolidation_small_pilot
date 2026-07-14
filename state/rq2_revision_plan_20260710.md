# RQ2 修正执行方案(可落地 · 分阶段 · 预注册)

**对标 rq2_compliance_reference_20260710.md | 2026-07-10**

> 三路深挖(stage 指标接线 / 题型数据集构造 / N×算子 sweep+统计+成本)经 workflow 合成。
> **核心纪律:Phase 0 两条合规命脉(stage 指标落盘 + 题型覆盖)不做,后续 sweep 跑出的任何正斜率都是采样伪影。**

---

我已确认所有关键接口:`--seed`/`sample_qa`/`session_pool` 分层抽样已存在但无 `question_type` 分层;`cochran_armitage_trend(levels, events, totals)` 和 `annotate_holm(rows, p_key, alpha)` 签名;`stage_metrics_by_pass` 契约;sweep 的 `--passes/--route-modes/--page-write-mode`。三份设计的代码基座全部对齐。现在合成方案。

---

# RQ2 修正设计 · 合成执行方案

三份设计合并后的一句话:**先补两条合规命脉(stage 指标真正落盘 + 题型覆盖到 benchmark 标准),否则 N×算子 sweep 跑出来的正斜率全是采样伪影;命脉补齐后再接双轨指标、跑预注册 sweep、最后按 go/no-go 决定是否上深 N/多算子/规模。**

依赖链(硬序):`Phase 0`(改 harness,离线为主)→ `Phase 1`(接线,纯离线)→ `Phase 2`(花钱跑 + 判定)→ `Phase 3`(条件触发)。Phase 0 的两条并行,但都必须在 Phase 2 第一次花钱前完成。

---

## Phase 0 — 合规命脉(不做则后续全是伪影)

两条子线并行,均以"改代码/离线"为主,各自末尾有一次小额冒烟验证。

### 0A. Stage 指标真正落盘(provenance → 三类 record)

问题:`rq2_stage_metrics.py` 的契约(`:20-27`)要求每 item 产 `{is_new, has_source_support}` / `{is_contradictory, merged_incorrectly}` / `{used_unsupported_memory}`,但当前 run 只落到 **page 粒度 provenance**,无句级支持判定。不补,UNMR/conflict/PAR 三条曲线全是空壳。

| 步 | 改哪些文件 | 产出 | 离线/花钱 | 成本时间 |
|---|---|---|---|---|
| 0A-1 | 上游 `tiermem_upstream/src/memory/linked_view_system.py` 加旁路函数 `_score_note_provenance(note, source_text=page.content, page)→list[record]`;在 `run_consolidation_passes` reindex 前(**1298-1319**,`1318` 后)对每 page 把 `note`(来自 `_generate_consolidated_note` **1027-1042**)切句,逐句 NLI/judge 核对是否被 `page.content` entail,落 `stage:"consolidation_provenance"` 日志(带句子/`page_id`/`raw_log_ids`)。UPDATE 分支(`_do_add_fact_internal` smart_action="UPDATE",**4420-4425**,`replaced_id` 存在=一次合并)另落 `stage:"consolidation_conflict"`。**不改 mem0/index/数据流,纯旁路记录。** | 每 pass 每 page 的句级 `supported: bool` + 冲突合并事件,写进 run logs | 改代码(离线) | 0.5-1 天 |
| 0A-2 | 新建 `scripts/core/rq2_stage_extract.py`:读 `run_root/sessions/*_write.jsonl` + `*_qa.jsonl`,按 `consolidation_pass` 分桶,产 `records_by_pass[N]={"new_memory":[],"conflict":[],"answer":[]}`。判据映射:`is_new`= pass≥1 固化句(精确版=与 pass0 `page.content` 句集比对新增才算);`has_source_support`= 0A-1 的 entail 命中≥1;`is_contradictory`= UPDATE 前后 fact judge 判相反;`merged_incorrectly`= `updated_text` 与 HaluMem gold(`is_update` 标注)不一致或丢信息;`used_unsupported_memory`= 答案引用的 `mechanism_trace.hits_summary` 对应句 `has_source_support=False` | 一个纯函数,吃 run 目录 → 吐契约字典,直接喂 `stage_metrics_by_pass`(`rq2_stage_metrics.py:60`) | 改代码(离线) | 0.5 天 |
| 0A-3 | 冒烟:在**已有的一个小 run**(或 N=2 单档,~$5)上跑 0A-1+0A-2,确认三桶非空、`stage_metrics_by_pass` 不报错、`den>0` | 证明契约打通,不是空壳 | 复用旧 run=离线;若无旧 run 则一次 ~$5 冒烟 | 0.5 天(含 ~$5) |

conflict 数据来源(三份一致):**优先 HaluMem `Dynamic Update` / `Memory Conflict` 自带的 `is_update=True` 前后对**(gold 明确 → 直接判 `merged_incorrectly`),不人工构造矛盾对;覆盖不足再补 LongMemEval `knowledge-update`。

### 0B. 题型覆盖到 benchmark 标准(废头截断,上分层抽样)

问题:`run_v2_tiermem_micro_slice.py` 的 `--session-limit/--qa-limit` 头截断(**51-52,124,133**)只取前 N session/QA,系统性撞上 persona 首 session、漏掉 `Multi-hop`/`Dynamic Update`/`Memory Conflict` 等难题型。`--seed` 分层抽样脚手架已存在(**94,114,122,130-131**,`sample_qa`/`session_pool`),但**只按 session/QA 随机,不按 `question_type` 分层**。

| 步 | 改哪些文件 | 产出 | 离线/花钱 | 成本时间 |
|---|---|---|---|---|
| 0B-1 | `run_v2_tiermem_micro_slice.py`:在现有 `rng.sample` 逻辑(**122/130-131**)上加 `--stratify-by question_type` 与 `--family-quota` 参数,遍历**全 20 persona 全 session** 建 per-type 候选池,再 `rng.sample` 凑配额。保留 `--seed` 复现。 | 四家族均衡切片,不再头截断 | 改代码(离线) | 0.5-1 天 |
| 0B-2 | 新建 `scripts/core/rq2_dataset_build.py`:实现四家族取题映射与识别键(下表),LongMemEval 走已在 dataset 层的 `_spec_for("longmemeval")` 按 `question_type` 过滤 oracle 500 | 冻结的题目清单(带 family 标签)+ 判分路由 | 改代码(离线) | 0.5 天 |
| 0B-3 | 冒烟:对每家族抽 5-10 题干跑,确认识别键命中率、evidence 空/非空判别正确、abstention 正例(`Memory Boundary`∧`evidence==[]`∧`answer` 以 "Unknown" 开头)被正确路由 | 证明四家族可稳定取满配额 | 离线(纯数据,不调 LLM) | 0.25 天 |

**四家族映射(目标 ~100/家族,冻结于跑前)**:

| 家族 | 主源 (question_type) | 补源 | 识别键 | 目标 |
|---|---|---|---|---|
| ① 单跳客观短答 | HaluMem `Basic Fact Recall`(746) | — | `type==Basic Fact Recall` ∧ `len(evidence)==1` | 100 |
| ② 多跳 | HaluMem `Multi-hop Inference`(198) | LME `multi-session`(133) | HaluMem 该 type ∧ `len(evidence)>=2`;LME `type==multi-session` | 100(HM70+LME30) |
| ③ 时间/更新 | HaluMem `Dynamic Update`(180) | LME `knowledge-update`(78)+`temporal-reasoning`(133) | HaluMem `type==Dynamic Update` ∧ `memory_points.is_update=="True"`;LME 两 type | 100(HM50+LME50) |
| ④ 冲突/abstention | HaluMem `Memory Conflict`(769)+`Memory Boundary`(828) | — | Conflict:`type==Memory Conflict`;Abstain 正例:`Memory Boundary`∧`evidence==[]`∧`answer` 以 "Unknown"/"not provided" 开头 | 100(Conflict50+Boundary50) |

`Generalization & Application`(746)留作分布外 held-out,**不计入主检验**(避免 judge 主观性污染)。判分:①②官方 `evaluation.py` judge + evidence 精确/子串双通道取合取;③判"当前值"(答旧值=Hallucination 非 miss);④ Conflict 判是否输出被撤销旧事实,Abstention 正例答 unknown=Correct、猜确定事实=Hallucination(非 partial,`eval_tools.py:254-255`)。**②开放跳与客观锚家族分列报告**,防主观分掩盖机制信号。

> **Phase 0 门槛(进 Phase 1 的前提)**:0A-3 三桶非空且 `den>0`;0B-3 四家族各取满配额且识别键正确。任一不过,禁止进入花钱阶段。

---

## Phase 1 — 双轨指标接线(纯离线,零花钱)

把 Phase 0 的两条命脉接进报告管道,产出"记忆对象层 ‖ 答案层 + PAR 桥"的宽表。此阶段**不跑任何 LLM**,只在已有/冒烟 run 上验证接线。

| 步 | 改哪些文件 | 产出 | 离线/花钱 |
|---|---|---|---|
| 1-1 | `run_v2_tiermem_micro_slice.py` 的 `_build_micro_report`(**174-291**):调 `rq2_stage_extract`(0A-2)→ `stage_metrics_by_pass`(`rq2_stage_metrics.py:60`),把 `rq2_stage_metrics` 键写进 report json(落盘,配合已有 `stage=="consolidation_pass"` 读取 **233**) | 每 run report 带 per-N 的 `{unmr, conflict_merge_rate, par}`(带 Clopper-Pearson CI) | 离线 |
| 1-2 | 记忆对象层双轨:接 `scripts/analysis/halumem_official_eval_adapter.py`(`--live` 落 `extracted_memories`/`memories_from_system`,行 **312/316**)输出 official **integrity/accuracy/update**(0/1/2),与 UNMR/conflict-merge-rate 同表 | 记忆对象层左轨(official 三分 + 两条 stage 指标) | 离线(接线;`--live` 花钱在 Phase 2) |
| 1-3 | 答案层右轨:official QA judge **Correct/Hallucination/Omission**(含 abstention 正例)+ 自建 `classify_answer`;**桥 PAR(N)** 把两轨钉在一起(UNMR↑ 是否传播成 PAR↑)。报为 `metric×N` 宽表,arm A/B 双列 | 双轨并列宽表模板 | 离线 |
| 1-4 | 在 0A-3 的冒烟 run 上端到端跑一遍 Phase 1 管道,确认宽表所有 cell 有值、CI 合理 | 可发布的报告骨架 | 离线 |

产出:一张**空的但结构完整**的双轨宽表(等 Phase 2 灌数)。约 1-1.5 天,零成本。

---

## Phase 2 — N×算子 sweep(预注册判据,第一次花钱)

命脉与接线都通了,才在这里花钱。**这是唯一的 go/no-go 关口。**

### 跑什么(最小合规档,已省格)

- 走现成 `run_v2_tiermem_micro_n_sweep.py`:`--passes`(**63**)、`--route-modes`(**57-62**)、`--page-write-mode`(**50**)。
- **算子对(PDF 唯一强制对)**:arm A=TierMem infer 升级 `--page-write-mode infer --route-modes research_only`;arm B=摘要 baseline(PDF §146)`--page-write-mode infer --route-modes summary_only`。命题化/COMEDY 属 RQ4,**不在本 RQ 跑**。
- **切片**:Phase 0B 的分层四家族切片,扩到 **~7 session/~120 QA**(功效需要,见下),×**2 seed**。
- **N∈{0,2,8,16}**(4 档定斜率符号)× {A,B} × 2 seed = **16 run**。

**功效依据**(冻结):update/QA judge 实测 62.5%↔37.5% 摆动 ⇒ p≈0.5、方差最大;CA trend 要在 N 网格测到 ~4pt/step(0→16 约 25pt 差),80% power@α=.01 需**每格 n≥120 QA**(现 45 太小)。conflict/update 稀疏,用 `--session-index`/定向选 `is_update` session 凑 **≥30 事件/格**。

### 预注册 stop/go 判据(对齐 PDF §7 正斜率)

**全部冻结于跑前**:斜率符号、α、seed 数、样本量、家族清单。

- **主终点** = `PAR(N)` 随 N 正斜率。检验 `cochran_armitage_trend(levels=[0,2,8,16], events, totals)`(`stats_guardrails.py:126`),要求返回 `direction=="amplifying"` 且 Holm 后 **p<0.01**。
- **多终点家族** = {UNMR, conflict_merge_rate, PAR, QA-Halluc率, update-error率},各跑一次 trend,`annotate_holm(rows, p_key="p_value", alpha=0.01)`(`:65`)校正 5 个 p。
- **GO(支持 RQ2)**:PAR 或 UNMR 至少一个 Holm-reject 且 amplifying,**且 UNMR 先于 PAR**(阶段序:错误先在固化层出现,再传播到答案)。→ 进 Phase 3。
- **NO-GO(反驳)**:全部 flat/attenuating。**反驳前必须**按 §7 先收紧压缩预算(`--consolidation-target-max-pages` 调小,**48**)重跑一轮再定案,防止"预算太松→没触发固化压力"的假阴性。

### 成本

| 项 | 量 | 成本 | 墙钟 |
|---|---|---|---|
| 最小合规档 | 16 run(4 N × A/B × 2 seed),~120 QA/格,`--live` fill + judge | **$60–90** | **1–1.5 天**(瓶颈=write-infer 墙钟) |

---

## Phase 3 — 深 N / 多算子 / 规模(仅 GO 后触发)

Phase 2 判 GO 才跑,是把已确证的斜率**加密、复制、上规模**,不新增机制假设。

| 子项 | 改哪些文件 | 跑什么 | 成本 |
|---|---|---|---|
| 3-1 深 N | 无需改码,`--passes 0 1 2 4 8 16` 全 6 档 | 6 N × A/B × **3 seed** 补齐主检验网格 | 计入下方完整档 |
| 3-2 自建 poison 库 | 复用 0B 数据管道加 poison 变体 | 自建库锚 N∈{0,2,8,16} 定形状(官方全 N 定检验) | 计入下方 |
| 3-3 LongMemEval 复制样本 | `_spec_for("longmemeval")` 已就位,按 type 过滤 | 仅作**独立复制**(§7 之后),验证 HaluMem 斜率可迁移 | 计入下方 |
| 3-4 规模 | 加 user/session | integrity/accuracy 连续 0/1/2 方差小,每格 60 记忆点×2 seed 即测到 0.15 分/step | 计入下方 |

**完整档合计**:~40 run(6 N × 3 seed + 自建库 + LME 复制)≈ **$220–320 / 3–4 天**。HaluMem-Long 不在盘,本轮不列。

---

## 依赖排序(改代码 vs 跑)

```
[改码·离线]  0A-1 provenance旁路(upstream) ─┐
[改码·离线]  0A-2 rq2_stage_extract          ├─► 0A-3 冒烟(~$5) ─┐
[改码·离线]  0B-1 分层抽样(废头截断)        │                  │
[改码·离线]  0B-2 rq2_dataset_build          ├─► 0B-3 冒烟(离线) ┤
                                             │                  │
[改码·离线]  Phase1 双轨接线(1-1~1-4) ◄──────┘◄─────────────────┘
                                             │
[跑·花钱]    Phase2 sweep 16run($60-90) ─► go/no-go 判据
                                             │  GO
[跑·花钱]    Phase3 完整档40run($220-320)
```

改代码(离线,可并行,无 API 花费):0A-1、0A-2、0B-1、0B-2、Phase 1 全部。
跑(花钱,严格串行在改码之后):0A-3 冒烟($5)、Phase 2($60-90)、Phase 3($220-320)。

---

## 最小可发表合规档 · 推荐路径

**目标**:一份口径干净、能过 §7 预注册、可发表的 RQ2 结果——不追求 Phase 3 的加密与规模。

推荐路径 = **Phase 0(全)+ Phase 1(全)+ Phase 2(最小合规档)**,到 go/no-go 为止:

1. 0A(provenance 落盘)+ 0B(分层四家族)+ 各自冒烟 —— **~2.5–3 天改码 + ~$5**。
2. Phase 1 双轨接线 —— **~1–1.5 天,$0**。
3. Phase 2:16 run,4 N × A/B × 2 seed × ~120 QA,预注册 PAR/UNMR 正斜率 + Holm α=0.01 + UNMR 先于 PAR —— **$60–90 / 1–1.5 天**。

**最小合规档总计:约 4.5–6 天工程 + $65–95。** 产出即可发表的双轨宽表 + 一个预注册的 go/no-go 结论(PAR/UNMR 是否随 N amplifying)。GO 才追加 Phase 3 完整档(+$220-320);NO-GO 则按 §7 先收紧压缩预算重跑一轮再定案,仍属最小档预算内的一次小重跑。

---

**核心文件路径(绝对)**
- 上游 provenance 旁路:`/Users/yihaiwen/Documents/New project/tiermem_upstream/src/memory/linked_view_system.py`(1027-1042,1298-1319,4420-4476)
- page 底座:`/Users/yihaiwen/Documents/New project/tiermem_upstream/src/linked_view/page_store.py`(53,231,283,358)
- stage 契约(已存在,勿改):`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/core/rq2_stage_metrics.py`(20-27 契约,60 入口)
- 新建 extract:`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/core/rq2_stage_extract.py`(0A-2)
- 新建数据构造:`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/core/rq2_dataset_build.py`(0B-2)
- 切片器(改分层):`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/run/run_v2_tiermem_micro_slice.py`(51-52,124,133 待废头截断;94/114/122/130-131 seed 抽样脚手架;174-291 `_build_micro_report`,233 stage 读取)
- sweep 驱动:`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/run/run_v2_tiermem_micro_n_sweep.py`(50 `--page-write-mode`,57-62 `--route-modes`,63 `--passes`)
- 官方 eval adapter:`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/analysis/halumem_official_eval_adapter.py`(312/316 `--live` 落盘)
- 统计:`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/scripts/core/stats_guardrails.py`(65 `annotate_holm`,126 `cochran_armitage_trend`);`safety_honest_metrics.py`(28 `clopper_pearson`)