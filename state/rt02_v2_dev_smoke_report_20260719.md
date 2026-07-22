# RT-02 v2 dev smoke 报告 · 2026-07-19

> **性质**：dev smoke = 验证 v2 机器/构念/baseline 非退化/endpoint 方差，**不产出研究判定**。设计 `rt02_v2_construct_validity_design_20260719.md` §11。
> **重要执行事故**：4 个 runner 并发共用一个 API key 触发严重限流，叠加指数退避把每次调用拖到分钟级，5 小时只跑完 PairGain(2×6) + CHIR 部分(append 3 / summary 2)。单发延迟实测 gen 1.3s + judge 1.1s ≈ 2.4s/call——**慢是并发限流，不是 API 慢；下轮必须串行**。这是部署失误，不影响已落盘数据的正确性。

## 1. 完成情况

| 任务 | 状态 | 完整 case |
|---|---|---|
| PairGain append_only | ✅ 完成 | 6/6 |
| PairGain summary_rewrite | ✅ 完成 | 6/6 |
| CHIR append_only | ⏸ 停于并发爬行 | 3/6 |
| CHIR summary_rewrite | ⏸ 停于并发爬行 | 2/6 |

## 2. 机器体检（真 API）——全过

- **R1 genuine operator 成立**：CHIR/PairGain 的 summary_rewrite 在真 LLM 上均为 `created`+`mut`（真创建并逐轮重写摘要），append_only 仅 `append`；fail-fast 无 `OperatorNoOpError`，两算子行为被正确区分。
- **R2 retrieval 生效**：所有 probe 的 `n_retrieved`=5（k=5 上限），上下文被真限制到 top-k，不再序列化全池。
- **R6 branch 对齐**：PairGain 两算子 branch match_fail 全 0/6。
- **endpoint 有方差**：PairGain A_j1 ∈ {0,1}；CHIR 各臂水位分明。
- 快照/records/hash 完整落盘；无 crash。

## 3. baseline 非退化（CHIR 部分数据）

各臂 mean unsafe(j1)（across k），及关键对比：

| operator | n | contam_d3 | contam_d0 | safe_d3 | full_closure | **d3−d0** | d3−safe |
|---|---|---:|---:|---:|---:|---:|---:|
| append_only | 3 | 0.85 | 0.07 | 0.19 | 0.00 | **+0.78** | +0.67 |
| summary_rewrite | 2 | 0.72 | 0.06 | 0.00 | 0.06 | **+0.67** | +0.72 |

- 各臂清晰分层：contam_d3 高、contam_d0/safe 低、full_closure≈0（ceiling 有效）→ **baseline 非退化**。

## 4. 初步信号（n=2–3，方向性，**不是判定**）

v1 的核心担忧：CHIR 残留可能是 **append=operator-off 伪影**（全池无检索让污染 descendants 永远可见）。

v2 在**同时**加入 (a) genuine summary_rewrite 真算子（污染 descendants 被折叠进被重写的摘要）和 (b) 真 top-k 检索（上下文限 top-5）后：

> **`contam_d3 vs contam_d0` 残留仍然存活：summary_rewrite +0.67、append_only +0.78。**

即：同样只修 source，差别仅在污染历史是否被 consolidation 携带进摘要状态——**残留在真算子 + 真检索下没有消失**。这是 CHIR 核心信号"不是纯 append 伪影"的**第一个正向迹象**，方向上支持"押 CHIR"。

**必须同时声明的边界**：
- n=2–3，无 CI，**绝不能当作确证**；
- d3−safe(+0.67~0.72) 仍混"污染有害 + 正确历史有益"两方向，单方向只引 d3−d0；
- full_closure≈0 有官方参考文本语体加成（理想上界）；
- CHIR 未跑满 6 case；PairGain 的真正 RQ（G 是否预测未来增量风险）需**离线 lineage-local NLI（D/G）+ 统计**那一步，本 smoke 未做。

## 5. PairGain（两算子各 6/6）

- held-out 端点强非退化：minus(污染)≈1.00 unsafe、plus(纠正)≈0.13–0.16、mean A_j1 ≈ +0.85（两算子几乎一致）。
- 但 append 与 summary 端点水位几乎相同 → **是否改变 G 动态必须看 NLI 那步**，当前不能下结论。

## 5b. 关键构念发现（真 NLI 桥在 smoke 快照上暴露，冻结 confirmatory 前抓到）

对 PairGain summary_rewrite 的 6 个 case 跑真实 lineage-local NLI，发现 **`source_only` 的 D 在所有 t 上恒定**（如 finance/13 全 = 0.089）→ **G≡0，测量结构性失效**。

- **机制**：`source_only` 只测源头记录，而源头在 t=0 纠正后不再变；consolidation 的动态全在**摘要/后代**里，被 source_only 排除。
- **修正（dev 上改、confirmatory 前冻结，非追分）**：新增并冻结 **`consolidated_state`** 为 PairGain primary q = 源头 + 固化写入的载体（摘要/合并记录）。它捕捉 operator 动态且不被全池稀释；append_only 下自动退回源头=平坦（正确的 operator-off 对照）。`source_only` 降为"应平坦"sanity，`whole_pool` 为稀释基线 sensitivity。
- **价值**：这正是 dev/smoke 的目的——若当初冻结 source_only 直接跑 confirmatory，会得到 G≡0 的**假 STOP**。已同步改 `rt02_confirmatory_config_20260719.md` §4 与 `rt02_v2_measure.py`（含自测）。

## 6. 成本与下一步

- 成本量级：约 5 小时并发跑了 ~1200+ 次调用（主 gpt-4.1-mini + gpt-4o judge2 子集），量级约单位数美元（无法从本地精确读取）。
- **不建议**再花钱扩这个 smoke——它的验证目的已达成。
- **下一次真花费应是冻结后的 confirmatory**：在未见 QA confirmatory split(30 case) 上，**串行**跑（~35min/6case，全 30 case 约 3h 但不再限流），需先：
  1. 冻结 confirmatory 配置（operator 选 summary_rewrite、k、arms）；
  2. 补 PairGain 的离线 lineage-local NLI（source_only vs whole_pool 的 D/G）；
  3. 你另行授权花费。

## 7. 一句话

**smoke 通过：v2 机器在真 API 上全部正确，baseline 非退化；且初步（n=2–3）看到 CHIR 残留在真算子+真检索下存活——这是 v1 append 伪影担忧的第一个反证，但远未确证。执行上唯一教训是别并发（限流），confirmatory 串行跑。**
