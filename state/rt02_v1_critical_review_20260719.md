# RT-02 v1 逐 RQ 批判性评审 · 2026-07-19

> **用途**：把 RT-02 v1（CHIR + PairGain existence 检验）的每个 Research Question 按统一维度逐条体检，标出可靠性与问题，最后汇总出下一轮修改建议。
> **评审人立场**：独立评审，正负两个方向都不放大。数字可复算 ≠ 研究问题被正确测到。
> **source of truth**：`HANDOVER_RT02_BASELINE_20260719.md` → `state/rt02_existence_verdicts_20260718.md` → verdict JSON → 冻结设计。本文件是评审意见，不覆盖上述结果。
> **一句话前提**：全项目核心构念 "consolidation（记忆重写/合并）" 从未被实现——两条线跑的都是 append-only pool（`pool.append(new_mem)`，无 summary/merge）。这条几乎重定义了每个 RQ 结果的含义。

---

## A. 评审维度定义

每个 RQ 按下列维度打分：

| 维度 | 含义 |
|---|---|
| 目前结果 | verdict + 关键数字 |
| 数字可靠性 | 落盘/可复算/CI/双 judge 层面是否扎实 |
| 构念可靠性 | 跑出来的数字**是否真的在测这个 RQ 想测的东西** |
| 代码可靠 | harness 实现是否忠实于设计、有无 bug |
| 评估 endpoint | unsafe 判定用什么 |
| 数据集来源 | case/字段从哪来 |
| 有真相结果 | 是否有 ground-truth（官方 `correct_answer`/label）锚定 |
| 灯 | 🟢 可直接采用 / 🟡 有条件采用（需收窄或修构念）/ 🔴 当前不可用 / ⚪ 未跑 |

**"一路绿灯"判据**：代码可靠 ∧ 官方评估 ∧ 官方数据集 ∧ 有真相锚定 ∧ 构念无致命混杂 → 🟢。任一有问题 → 降级并列出。

---

## B. 逐 RQ 体检

### RQ1 — 单次 transition 的 G 能否**提前**预测未来风险？ 🔴

| 维度 | 评估 |
|---|---|
| 目前结果 | STOP。合并 72-case，partial Spearman(G,Y1\|current)=+0.070，95% CI [−0.083,+0.200]；joint−current CV R²=−0.0025；permutation p=0.571 |
| 数字可靠性 | **高**：case-grouped CV、case-bootstrap 2k、whole-curve permutation、eps grid、CPU/MPS 等价审计（G Spearman 0.99983） |
| 构念可靠性 | **低** |
| 代码可靠 | 实现忠实，但忠实地实现了错误的被测对象 |
| 评估 endpoint | 官方 MISLED judge（gpt-4.1-mini），未加自造 rubric ✓ |
| 数据集来源 | MemEvoBench 官方 QA/WF 发布字段 ✓ |
| 有真相结果 | endpoint 有官方真相；但自变量 G 依赖的"consolidation transition"无真相（因为没有真算子）|
| 灯 | 🔴 **STOP 对研究问题基本无信息量** |

**核心问题（四条叠加，任一即可造假阴性）：**
1. **无 consolidation 算子** → G 测的是 append，正是 Proposal 里本该当 operator-off 对照的条件 → **近乎同义反复**（`run_rt02_pairgain_qa.py:109-114`）。
2. **全池 mean NLI 稀释** → `q(M)=mean` over 最多 64 句全池；pool 每步 append，source 信号被越来越多追加句稀释，SNR 随步数单调恶化（`rt02_pairgain_nli.py:30-45,74-111`）。
3. **outcome 自相关 + query 泄漏** → `Spearman(A_t,Y1)=0.847`，只有 3 次 transition，同 3 条 query 既做构造又做 endpoint，当前状态几乎决定下一状态，G 无残差方差可解释。
4. **branch 未 span-aligned** → 整条 misleading 替换为官方 correct，WF 分支长度比 median 0.344（严重失配），改变 NLI/attention/pool 增长。

---

### RQ2 — PairGain 是否**超越** current-state / TrustMem verifier？ 🔴

| 维度 | 评估 |
|---|---|
| 目前结果 | STOP。joint 不超 current-only；TrustMem-style-only CV R²≈−0.05 |
| 数字可靠性 | 中（分析可复算，但输入退化）|
| 构念可靠性 | **很低** |
| 代码可靠 | 分析代码可靠；comparator 实现退化 |
| 评估 endpoint | 官方 judge ✓ |
| 数据集来源 | 官方字段 ✓ |
| 有真相结果 | 同 RQ1 |
| 灯 | 🔴 **比较对象退化，结论无效** |

**核心问题：**
1. **TrustMem-style comparator 退化成常数**：preservation 全 10，faithfulness 9.99，coverage 98.4% 落 9–10，几乎零方差（`run_rt02_pairgain_qa.py:29-45`）。跟常数比得出的"joint 不超 TrustMem"没有统计意义，**既不能证明超越、也不能证明没超越**。
2. **RQ2 verdict 规则本身是 MVP**：脚本 `rq2_go = joint>trustmem-only + permutation p<0.05`，未实现 Proposal 的 joint>current/retrieval、Brier/AUROC/calibration、equal-count intervention（`rt02_pairgain_stats.py:220`）。JSON 里的 `rq2_go` 不是完整 RQ2 verdict。
3. **依赖 RQ1**：RQ1 是必要前提，已 false，RQ2 无独立结论意义。

---

### RQ3 — 把错误 source 改正确后，系统是否**已恢复**？ 🟡（窄口径可 🟢）

| 维度 | 评估 |
|---|---|
| 目前结果 | GO。QA matched residual +0.704 [0.550,0.847]，WF +0.189 [0.028,0.367]；7 域全正；benign_vol≈0；full closure 显著优于 source-only |
| 数字可靠性 | **高**：case-bootstrap 10k、AND 双 judge 存活、branch byte-match 41/41 |
| 构念可靠性 | **中偏低**（headline 被放大）|
| 代码可靠 | 六臂构造忠实官方机制，assert + hash 落盘 ✓ |
| 评估 endpoint | 官方 JUDGE_RESPONSE_PROMPT + gpt-4o AND 闸门 ✓ |
| 数据集来源 | 官方 QA(21)/WF(20) ✓ |
| 有真相结果 | 是，unsafe endpoint + correction 文本均来自官方 `correct_answer`/`correct_workflow` ✓ |
| 灯 | 🟡 整体；**窄口径 `contam_d3 vs contam_d0` + benign_vol 对照 ≈ 🟢** |

**可直接采用的窄核心（这是全项目唯一接近🟢的结论）：**
> `contam_d3 − contam_d0 = +73pt(QA)/+22pt(WF)`：同样的 source correction，唯一差别是污染 descendants 在不在；benign_vol≈0 排除"记录数量"解释。代码可靠、官方评估、官方数据、真相锚定、双 judge、7 域同向。

**headline 被放大的因素（必须收窄，不能采用 `+0.704` 当外推结论）：**
1. **无 top-k retrieval**：static QA 路径序列化整个 pool，污染 descendant 永远"在场"→ 现在测的是 **append 日志持久性**，不是 consolidation 迟滞；真实检索下陈旧 descendant 未必被召回。
2. **full_closure 用官方参考文本重写 descendant** → 语体贴 judge reference，0% unsafe 是理想上界（`rt02_common.py:73-85`）。
3. **matched residual 混方向**：safe 历史单独就把 unsafe 从 58.7% 压到 5.8%，`+0.704` = 污染有害 + 正确历史有益的合成。单方向主张只能引 `d3-vs-d0`。
4. **无 genuine summary/merge 算子与 append-only 对照**；d 只 0/3、k 只到 2，无半衰期曲线。

---

### RQ4 — Residual 存在时，只修哪些 descendants？ 🟡（拆两半）

| 维度 | 评估 |
|---|---|
| 目前结果 | STOP。dev recovery 1.0 → held-out 0.412（门槛 ≥0.80 失败）；median repaired fraction 2/3（门槛 ≤0.40 失败）；targeted 不优于 equal-count heuristics |
| 数字可靠性 | **高**：21/21 hash 一致、稳定 SHA-256 dev/held-out 分割、equal-count 六 baseline |
| 构念可靠性 | 混合：过拟合发现可靠，可行性门是伪影 |
| 代码可靠 | 忠实；reconstruction 从 Stage-1 落盘响应重建 ✓ |
| 评估 endpoint | 官方 judge + AND ✓ |
| 数据集来源 | 复用 RQ3 的 21 QA case，官方 `correct_answer` 重写 ✓ |
| 有真相结果 | endpoint/重写有真相；但 descendant 依赖图是三轮线性 writeback，非真实 lineage |
| 灯 | 🟡 **过拟合发现可留（🟢），可行性 STOP 半为伪影（🔴）** |

**可留的真发现：** `dev 1.0 → held-out 0.412` 是真实的单-query influence 排序过拟合，本身可写。

**是伪影/不可当理论结论的部分：**
1. **3 descendant 离散化**：40% 预算 = "只能修 1 条"，修 2 条立刻 66.7% → ≤0.40 门几乎不可达，**与方法无关**。Proposal 本要 8–12 条。
2. **无区分空间**：3 条里各方法挑到几乎同样的 1–2 条 →"targeted 不优于 heuristic"部分是没得可选。
3. retrieval-frequency baseline 在 static full-pool 下全 tied，不是真检索 baseline；未测 benign utility；只 QA 无 WF。
→ STOP 只否定"当前单-query influence ranking"，不否定所有 graph-aware selective closure。

---

### RQ5 — 结论适用边界？ ⚪ 未跑

| 维度 | 评估 |
|---|---|
| 目前结果 | 未正式运行。仅有零散 QA/WF/域/第二 checkpoint 方向信息 |
| 数字可靠性 | N/A |
| 构念可靠性 | N/A |
| 代码可靠 | 无专用 harness |
| 评估 endpoint | — |
| 数据集来源 | 计划中 HaluMem/第二数据集未接 |
| 有真相结果 | — |
| 灯 | ⚪ **未开始**；当前所有结论外部效度=低（单 benchmark、单模型家族、单算子、无真检索）|

**核心问题：** 一个 agent 模型家族、一个 append 算子、无第二 open model、无外部 dataset、generation seed 方差未估。RQ5 不能在主构念站住前跑（否则是在错误构念上扩矩阵）。

---

## C. 跨 RQ 汇总的根因（问题不是 5 个，是 5 个 RQ 共享的 5 个根因）

| # | 根因 | 命中的 RQ | 后果 |
|---|---|---|---|
| R1 | **无 genuine consolidation 算子**（只 append） | RQ1,RQ2,RQ3,RQ4,RQ5 | PairGain 测了自己的 null 对照；CHIR 测的是 append 持久性 |
| R2 | **无 top-k retrieval**（全池序列化） | RQ3,RQ4 | 污染永远可见，效应被理想化放大 |
| R3 | **测量非 lineage-local**（全池 mean NLI 稀释） | RQ1,RQ2 | G 的 SNR 随步数崩溃 |
| R4 | **outcome 自相关 + query 未分离** | RQ1,RQ2 | 当前状态几乎决定未来，G 无残差方差；构造 query 泄漏进 endpoint |
| R5 | **comparator/对照退化或分辨率不足** | RQ2（TrustMem 常数）,RQ4（3 descendant） | 比较无效 / 预算门不可达 |
| R6 | **branch 未 span-aligned** | RQ1,RQ3 | 长度/语体失配污染 NLI 与 pool 增长 |

**唯一接近🟢的资产：** RQ3 的窄核心 `contam_d3 vs contam_d0 + benign_vol`。其余全部至少命中一个根因。

---

## D. 下一轮修改建议（按杠杆排序，每条对应根因）

> 原则：**先修构念再谈结论**。下面"合法上涨"改的是坏掉的仪器不是参数；修好后仍 null 也必须接受并发表为诚实负结果。

### D1. 押 CHIR，做一次真 confirmatory（最高优先，最可能出论文）
- 重构 headline：`hysteresis/迟滞` → **`correction closure under append/provenance`**（诚实且更 novel）。
- confirmatory 只加三样：
  1. **genuine 算子**（summary_rewrite / merge，对 R1）；
  2. **真 top-k retrieval 或可观察 retrieval exposure**（对 R2）；
  3. **语体/长度匹配的 correction 敏感臂**（对 R6，配 official-text 臂做双协议）。
- 加多 seed（分离生成随机性）、更长 d/k 曲线。
- **判据**：`contam_d3 vs contam_d0` 残留在真算子 + 真检索下**存活即 GO**（哪怕效应变小——变小但稳定反而更可信）。

### D2. 重建 PairGain 构念，再下 verdict（不要现在发 null，不要花钱做 intervention）
- **实现真算子**（对 R1）——第一杠杆。
- **lineage-local / source-anchored 测量**替换全池 mean（对 R3）：在 dev 上比 source-only q / source+lineage q / retrieval-weighted q，**冻结一个主版本**再进 confirmatory。
- **query/time 分离**（对 R4）：held-out future query 永不写回；G(t) 预测真正 t+2/t+3 endpoint；报告所有冻结 horizon。
- **span-aligned branch matching + fail-fast**（对 R6）：只改目标 span、非目标 hash 一致、预注册 ±10–15% 长度容忍、每 case 落 lexical/length audit。
- **判据**：小 dev 集搭好并冻结 → 跑**一次** confirmatory。仍 null 就作诚实负结果发（"prospective transition-gain marker 打不过 current state" 本身是贡献）。

### D3. 修 RQ2 comparator（对 R5，仅 RQ1 先 GO 才做）
- 优先官方 TrustMem 代码；不可得则明确叫 `TrustMem-style reproduction` 并**校准 prompt 出方差**。
- 加 retrieval-only/random/no-op/operator-off；held-out Brier/AUROC/calibration（阈值 test 前冻结）。

### D4. 修 RQ4 分辨率（对 R5，仅 RQ3 confirmatory 站住才做）
- 每 case 目标 **8–12 descendants + 真 dependency graph**，让 40% 预算门有分辨率。
- 比较 full / lineage / evidence-conflict / cluster-level closure；重建 retrieval index；≥2 held-out probes；记 benign utility + 真实 cost。
- 保留 v1 的过拟合发现作为已确立结果。

### D5. Phase 0 硬前置（动任何 API 前）
- 封存 `state/rt02_runs/*20260718*` 为 immutable v1，不改不覆盖。
- 建 `state/rt02_v1_used_cases_manifest.json`，从官方剩余 case 划**完全未见**的 v2 dev/confirmatory split（不足则标注 nested resampling，不冒充独立 test）。
- 先写 `state/rt02_v2_construct_validity_design_YYYYMMDD.md` 冻结上述定义，再实现。
- 补完整 reproducibility manifest（绝对 dataset path、commit、case IDs、seed、model、prompt hash、operator、exclusion reason、依赖版本）。

### D6. RQ5 暂缓
- 主构念（D1/D2）站住前不跑跨模型/跨 operator/HaluMem 矩阵。

### 红线（下一轮明令禁止）
- 在同一批 v1 72-case 上换 epsilon/aggregation/checkpoint 追 CI 过 0；
- 只报显著 domain/horizon/judge；加样本到 CI 刚过 0；
- 用 judge 参考语体重写 test memory 再当"方法"；
- 改 informative-case 定义剔失败；把 post-hoc sensitivity 说成预注册。

---

## E. 一句话结论

**v1 里唯一能"一路绿灯"直接采用的是 RQ3 的窄核心 `contam_d3 vs contam_d0`（代码/评估/数据/真相全绿，只需收窄口径）；其余 RQ 的结果数字可靠但构念被 5 个共享根因污染，尤其 PairGain 的 STOP 因"append=operator-off"近乎无信息量。下一轮把资源压在"给 CHIR 做真算子+真检索的 confirmatory"，同时把 PairGain 的构念（真算子 / lineage-local 测量 / query 分离 / span 匹配）重建后做一次性 confirmatory——修好仍 null 就诚实发负结果，绝不在旧 test 上追分。**
