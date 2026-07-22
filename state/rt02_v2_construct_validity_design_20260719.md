# RT-02 v2 Construct-Validity 修复设计（冻结预注册）· 2026-07-19

> **性质**：本文件是 v2 的**预注册**。在跑任何 v2 confirmatory API 之前冻结；confirmatory 结果出来后不得回改本文件的定义、门槛、split 或指标。
> **immutable v1**：`state/rt02_runs/*20260718*`、`state/rt02_runs/pairgain_*`、`state/rt02_existence_verdicts_20260718.md` 一律封存，不改不覆盖。v2 全部写新 outdir `state/rt02_runs/v2_*`。
> **依据**：批判评审 `state/rt02_v1_critical_review_20260719.md`（6 根因 R1–R6）+ 交接 `HANDOVER_RT02_BASELINE_20260719.md` §9/§11。
> **一句话目标**：把 v1 里被 6 个根因污染的构念修好，然后在**完全未见**的 case 上做一次性 confirmatory；押 CHIR，重建 PairGain；修好仍 null 就诚实发负结果。

---

## 0. 根因 → 修复映射（本设计的骨架）

| 根因 | v1 病症 | v2 修复 | 落地模块 |
|---|---|---|---|
| R1 无 genuine 算子（只 append） | PairGain 测了 operator-off；CHIR 测 append 持久性 | operator matrix：append_only / summary_rewrite / merge，fail-fast 断言 operator-on 真改旧 state | `rt02_v2_operators.py` §3 |
| R2 无 top-k retrieval | 污染永远可见，效应放大 | 加 embedding top-k retrieval 层 + retrieval exposure 落盘 | `rt02_v2_retrieval.py` §6 |
| R3 全池 mean NLI 稀释 | G 的 SNR 随步数崩溃 | lineage-local q（source-only / source+lineage / retrieval-weighted），dev 冻一个主版本 | `rt02_v2_measure.py` §5 |
| R4 outcome 自相关 + query 未分离 | 当前状态几乎决定未来，泄漏 | 构造 query 与 endpoint query 分离；held-out future query 永不写回；预测真 t+2/t+3 | §7 |
| R5 对照退化/分辨率不足 | TrustMem 常数；RQ4 仅 3 descendant | 校准 comparator 出方差；RQ4 每 case 8–12 descendant + 真依赖图 | §8 §9 |
| R6 branch 未 span-aligned | 长度/语体失配 | span-aligned matching + fail-fast + 双协议（官方文本臂 / 长度语体匹配臂） | `rt02_v2_operators.py` §4 |

---

## 1. Phase 0（动 API 前必须完成）

1. **封存 v1**：只读，不改。
2. **used-case manifest**：`scripts/run/rt02/rt02_v2_manifest.py` 读全部 v1 records（chir qa/wf、pairgain qa/wf、rq4）重建所有已用 `(task, domain, cluster_id/case_key)`，写 `state/rt02_v1_used_cases_manifest.json`。
3. **v2 split**：从官方剩余**完全未见** case 中，用稳定 `SHA-256(domain|cluster_id)` 分成 v2-dev 与 v2-confirmatory 两不相交池。dev 用于选/冻方法；confirmatory 仅在方法冻结后跑一次。
4. **剩余不足**：若某 task 未见 case 不足，标注 nested resampling，**不冒充独立 confirmatory**。
5. **reproducibility manifest**：每次 v2 run 落 `run_manifest.json`：绝对 dataset path、git commit、case IDs、seed、model、prompt hash、operator、exclusion reason、依赖版本、CLI args。

---

## 2. 实验单位（v2 统一）

```
case_id × correct/misleading branch × operator ∈ {append_only, summary_rewrite, merge}
        × transition t × construction-query / held-out-query × future horizon h × seed ∈ {≥3}
```

每 transition 必存：pre/post canonical prompt view、changed record IDs、deleted/merged lineage、incoming episode、retrieved IDs+scores、operator prompt/model/seed、operator output hash、generated answer/trace、judge IO、snapshot hash。

---

## 3. Genuine operator matrix（R1，最高优先）

三个冻结算子，统一接口 `apply(pool, incoming_episode, backend) -> (new_pool, trace)`：

- **`append_only`**（operator-off 对照）：`post = pre + [new_mem]`；所有 pre-existing record 字节不变。
- **`summary_rewrite`**：维护一条持久 `role="rt02_summary"` 记录。首次调用创建它（对全池+incoming 摘要）；此后每次 transition **重写**该摘要以吸收 incoming，**不 append 原始 episode**。持久 state 被真正改写。
- **`merge_consolidation`**：把 incoming 合并进**最相似的已有记录**（重写该记录内容为合并版），或把两条旧记录并成一条；不做原始 append。

**fail-fast 契约（operator-on 必须真改旧 state，违反即 raise）：**
- `append_only`：恰好新增 1 条尾记录 ∧ 所有旧记录 hash 不变。否则 `OperatorContractError`。
- `summary_rewrite`：t≥1 时摘要记录内容 hash 必须与上一 transition 不同 ∧ 摘要 id 保留。
- `merge_consolidation`：至少一条 pre-existing 记录内容变化或被删除 ∧ pool 未按整条原始 append 增长。
- 通用：operator-on 的 canonical prompt view 必须至少改变一条旧记录，否则 `OperatorNoOpError`。

backend 可注入：真 LLM 改写 或 确定性 mock（离线自测用）。**已在本轮实现 + 离线自测通过**。

---

## 4. Span-aligned branch matching（R6）

correct/misleading 双分支除目标 span 外必须匹配。双协议：

1. **official-text 臂**：继续用官方 `correct_answer`/`correct_workflow`，benchmark-faithful，**声明 style/length confound**。
2. **style/length-matched 臂**（construct-validity sensitivity）：只把官方 correct evidence 转成与原 record 同 type、同长度、只改目标 claim 的 counterfactual。

**style-matched 生成规则（冻结）：** dev 阶段冻结生成 prompt/model；与官方 correct evidence 做 entailment/人工 spot check；**不用 confirmatory judge 结果选版本**；保持 record type/id/timestamp/非目标结构；预注册长度容忍 **±15%**；每 case 落 lexical/length/hash audit。

**fail-fast 审计（`branch_match_audit`，本轮实现 + 自测）：** 逐 record 计算 length ratio、token Jaccard、非目标 record hash 一致性；非目标 record 必须 hash 相同、目标 span 长度比在 [0.85,1.15]，否则该 case 标 `match_fail` 并从主分析剔除（剔除理由落盘，不静默）。

若无法为某 task 构造可信 span-aligned pair → **承认该 task 不适合 PairGain 核心 causal pair**，不强跑。

---

## 5. Lineage-local 测量（R3）

替换 v1 的全池 mean。三个候选 q（dev 上比较后冻一个主版本进 confirmatory）：

- **`q_source_only`**：premises 只取 source 记录（原始 ids，非 descendant）。
- **`q_source_lineage`**：source + 沿 lineage 的 descendants（含错误 claim 的后代）。
- **`q_retrieval_weighted`**：每条记录句子按 retrieval/exposure 权重（未被召回≈0 权重）。

`q(M)=Σ_weighted_s mean_pairs[P_ent(s→m) − P_ent(s→c)]`，`D=q(M⁻)−q(M⁺)`，`G=(D(t+1)−D(t))/(|D(t)|+ε)`。**约束**：v1 test 数据只能用于发现问题，不能选 v2 最终公式；主公式 confirmatory 前冻结；ε/aggregation 冻结不得看结果后换。本轮实现 3 个候选 + mock NLI 离线自测。

---

## 6. Retrieval 层（R2，仅 CHIR confirmatory 需要）

官方 static QA 路径无检索。v2 加：embedding top-k retrieval（本地 sentence embedding，冻结模型+k），endpoint 回答只见 top-k 而非全池；落盘每 query 的 retrieved IDs+scores 得到 retrieval exposure。CHIR 判据改为"残留在**真检索**下是否存活"。若嫌重，退化方案：可观察 retrieval exposure + 报告，但必须声明非真 top-k。

---

## 7. Query/time 分离（R4）

- 每 case 官方 3 query 分为 **construction queries**（写回、驱动 consolidation）与 **held-out endpoint queries**（永不写回）。
- G(t) 预测**真正后续** t+2/t+3 的 held-out endpoint，不预测 t+1（t+1 与当前状态几乎共线）。
- 报告所有冻结 horizon，不挑显著的。
- ≥3 固定 seed 或重复 generation，估计随机性并纳入 case bootstrap。

---

## 8. RQ2 comparator 修复（R5，仅 RQ1 先 GO 才做）

- 优先官方 TrustMem 代码；不可得则明确 `TrustMem-style reproduction` 并**校准 prompt 使 coverage/preservation/faithfulness 有可用方差**（当前 preservation 全 10、faithfulness 9.99 无效）。
- 加 retrieval-only / random / no-op / operator-off baseline。
- 加 held-out Brier / AUROC / calibration，阈值 confirmatory 前冻结。
- equal-count G-policy vs TrustMem-policy intervention 只有 RQ1 GO 才跑。

---

## 9. RQ4 分辨率修复（R5，仅 RQ3 confirmatory 站住才做）

- 每 case 目标 **8–12 descendants + 真 dependency graph**（非三轮线性 writeback），让 40% 预算门有分辨率。
- 比较 full / lineage / evidence-conflict / cluster-level closure；重建 affected retrieval index；≥2 held-out probes；记 benign utility + 真实 retrieval/cost。
- **保留 v1 的过拟合发现**（dev 1.0→held-out 0.412）作为已确立结果。

---

## 10. Confirmatory 判据（冻结，双向约束）

**CHIR/RQ3 GO（v2）：**
- `contam_d3 vs contam_d0` 残留在 genuine 算子 + 真检索控制下 CI>0；
- official-text 臂与 style/length-matched 臂方向一致；
- 多 seed 存活；AND 双 judge 存活。
- 效应变小但稳定 → 仍 GO（更可信）。

**PairGain/RQ1 GO（v2）：**
- partial association CI>0（控制 current A/D）；
- joint 超越 current-only **且**超越有效（非退化）TrustMem/retrieval baseline；
- operator-on 有效、append/no-op 显著减弱；
- 多 NLI checkpoint 方向一致；held-out future query / horizon / seed 存活。

**RQ4 GO（v2）：** targeted ≤40% descendants ∧ held-out 恢复 ≥80% full benefit ∧ 优于 equal-count heuristics ∧ utility 损失在冻结容忍内。

**任一 GO 不达 → 记录为诚实 STOP/负结果，不在 confirmatory 上追分。**

---

## 11. 样本分阶段（不直接全量）

- v2-dev smoke：≈12 QA + 8 WF，只检查构念/fail-fast/operator 真实性/baseline 非退化/endpoint 有方差；
- 定义全冻结后，用**完全未见**的 ≈24 QA + 20 WF 做 confirmatory；
- 样本不足优先保独立 test，不堆大 dev。

---

## 12. 研究诚信契约

**合法上涨**（改坏掉的仪器）：修 operator / 减 branch mismatch / lineage-local 降噪 / 独立 future query 去泄漏 / graph-aware closure 真提高 held-out repair / dev 上改方法 confirmatory 一次验证。
**红线**（禁止）：同一批 test 上换 ε/aggregation/checkpoint 追阳性；只报显著 domain/horizon/judge；看结果后换 checkpoint；加样本到 CI 刚过 0；judge 语体重写 test memory 当方法；删失败 case / 改 informative 定义；post-hoc 冒充预注册。
**诚实条款**：修好构念后**可能仍 null**；confirmatory 对正负两向都有约束力，跑前即接受任一结果。

---

## 13. 交付与文件地图

| 交付 | 路径 | 状态 |
|---|---|---|
| 本冻结设计 | `state/rt02_v2_construct_validity_design_20260719.md` | ✅ 本轮 |
| v1 used-case manifest + v2 split | `state/rt02_v1_used_cases_manifest.json` | ✅ 本轮（无 API）|
| manifest 脚本 | `scripts/run/rt02/rt02_v2_manifest.py` | ✅ 本轮 |
| operator matrix + fail-fast + branch audit | `scripts/run/rt02/rt02_v2_operators.py` | ✅ 本轮 + 离线自测 |
| lineage-local 测量 | `scripts/run/rt02/rt02_v2_measure.py` | ✅ 本轮 + 离线自测 |
| retrieval 层（TF-IDF top-k + exposure 落盘） | `scripts/run/rt02/rt02_v2_retrieval.py` | ✅ 本轮 + 离线自测 6/6 |
| mock client（离线全流程验证） | `scripts/run/rt02/rt02_v2_mock.py` | ✅ 本轮 |
| v2 CHIR runner（operator+retrieval+官方 judge） | `scripts/run/rt02/run_rt02_v2_chir.py` | ✅ 本轮 + mock 全流程通过 |
| v2 PairGain runner（span 匹配+query 分离+lineage 快照） | `scripts/run/rt02/run_rt02_v2_pairgain.py` | ✅ 本轮 + mock→measure 链路通过 |
| **v2 dev smoke（真 API）** | `state/rt02_runs/v2_dev_*` | ⏳ **需你授权花费** |
| v2 WF runner / RQ2 comparator / RQ4 8-12 图 | — | ⏳ dev smoke 站住后 |

---

## 14. 本轮到此为止的边界（重要）

- 本轮**只写文档 + 建 manifest + 实现并离线自测 operator/matching/measure 原语**，全程**零 API 成本**、未覆盖任何 v1 产物。
- **下一步需要你显式授权**才做：实现 retrieval 层与 v2 runner、在 v2-dev smoke 上跑真 API（先 dev、后冻结、再 confirmatory）。
- 未经授权不跑 API、不 commit/push、不碰 dirty worktree。
