# RT-02 两刀存在性检验判定 · 2026-07-18（2026-07-19 完成 PairGain/RQ4）

> 对应设计文档(预注册):`state/rt02_baseline_design_20260718.md`
> 原始数据:`state/rt02_runs/{chir_qa,chir_wf,pairgain_qa}_20260718/`、`state/rt02_runs/pairgain_wf_20260718_v2/`
> 口径:一切 unsafe 判定 = MemEvoBench 官方 judge prompt 原文;judge1=gpt-4.1-mini(与 20260712 复现 pilot 连续)、judge2=gpt-4o、AND 闸门。CHIR 主终点为 paired delta、case-bootstrap 10k;PairGain 主关联为 case-bootstrap 2k、whole-curve permutation 1k。

## 一句话总结

**第一刀(CHIR/RQ3):双侧 GO,强积极信号**——source correction ≠ correction closure 在官方 benchmark 上确证,QA 侧效应巨大(+0.70)且全部 7 域同向,volume 对照干净,full closure 能修复。
**CHIR/RQ4:STOP,明确负信号**——问题存在,但当前 cross-fitted correction-influence 排序不能实现 selective closure;held-out 只恢复 41.2% full-closure benefit,且不优于 equal-count heuristics。结论收窄为 full / broad closure necessity,不保留 selective-method headline。
**第二刀(PairGain/RQ1-RQ2):STOP,明确负信号**——72-case 合并后,控制 current A/D 的 partial Spearman 仅 +0.070,95% CI [−0.083,+0.200];joint 比 current-only 的 held-out CV R² 低 0.0025,whole-curve permutation p=0.571。第二 NLI checkpoint 的 20-case 敏感性仍为 STOP。PairGain 的必要前提 RQ1 不成立,按 proposal Stop gate 不进入 intervention proof-of-concept。

## 1. CHIR Stage-1(RQ3)· 判定 GO

### 1.1 设置
21 QA case(7 域 × 3)+ 20 Workflow case;六臂(contam_d3 / safe_d3 / full_closure / contam_d0 / benign_vol / null_mem);d=3 官方轮 → source correction(官方发布字段逐字节)→ k=0/1/2(k 间官方写回轮,探针只读)。分支字节匹配断言 **41/41 case 全部通过**。

### 1.2 主终点(judge1;完整三口径见 verdict JSON)

| 终点 | QA (n=21) | Workflow (n=20) |
|---|---|---|
| **A(3) matched residual**(contam vs safe 同深度) | **+0.704 [+0.550, +0.847]** | **+0.189 [+0.028, +0.367]** |
| immediate residual(k0) | +0.698 [+0.540, +0.841] | +0.200 [+0.033, +0.383] |
| final residual(k2) | +0.698 [+0.540, +0.841] | +0.200 [+0.033, +0.383] |
| volume 检查(benign_vol − d0,应≈0) | +0.026 [−0.011, +0.069] ✓ | +0.011 [−0.056, +0.072] ✓ |
| closure 增益(source-only − full) | +0.762 [+0.608, +0.899] | +0.578 [+0.394, +0.761] |
| 深度效应(d3 − d0) | +0.730 [+0.582, +0.862] | +0.217 [+0.050, +0.394] |

**levels(QA j1)**:contam_d3 76.2% / safe_d3 5.8% / contam_d0 3.2% / benign_vol 5.8% / full_closure 0% / null_mem 58.7%。
**levels(WF j1)**:contam_d3 58.3% / safe_d3 39.4% / contam_d0 36.7% / benign_vol 37.8% / full_closure 0.6% / null_mem 65.0%。

### 1.3 稳健性
- **AND 双 judge 闸门存活**:QA +0.698 [+0.545, +0.841];WF +0.189 [+0.028, +0.367]。
- **QA 按域全部正向**:customerservice +0.67 / finance +0.78 / food +0.89 / health +0.26 / mental +0.44 / privacy +0.89 / traffic +1.00——非个别域驱动。
- 最干净的因果句:**contam_d3 vs contam_d0 = +73pt(QA)/+22pt(WF)——同样的 source correction,唯一差别是污染 descendants 在不在**;benign_vol 排除"记录数量"解释。

### 1.4 诚实边界(必须随结果一起说)
1. **safe 历史远低于 null 基线**(QA 5.8% vs 58.7%):正确记忆主动压低 base 水位,matched residual 同时包含"污染 descendants 有害"和"正确记忆有益"两个方向;单方向主张请引用 d3-vs-d0。
2. **WF 侧天花板**:judge 不确定即判 UNSAFE,null 基线 65%,safe 历史仍 39%(agent 自身轨迹被判 unsafe);WF 效应真实但小,且 j2 单独口径 +0.144 [−0.000, +0.306] CI 贴 0(预注册只要求 j2 同向,满足,但要写明)。
3. **full_closure 的 0% 有语体加成**:descendant 重写用的官方参考文本(test_correct_answer/ground_truth)是"理想化安全说法",与真实轨迹语体不同,其修复力上界应打折扣看;RQ4 做 selective closure 时要加语体匹配的重写臂。
4. 纠正文本 = 官方发布字段原文(QA 是批驳式 correct_answer),语体与原字段不同——已声明为口径;语体改写版留作敏感性。
5. d 只有 0/3 两档、k 只到 2;半衰期曲线要 Stage 2+ 才有分辨率。
6. 本 pilot 判定与 20260712 复现 pilot 同 judge 家族(gpt-4.1-mini/gpt-4o);更强独立 judge(如官方默认 gpt-5.2)未跑。

### 1.5 结论
按预注册判据(matched residual CI>0 ∧ j2 同向 ∧ volume 干净):**GO**。CHIR 的 existence 假设站住了,"source correction is not correction closure" 有真数据支撑;进入 RQ4(descendant influence + selective closure)合法。

### 1.6 RQ4 selective closure · 判定 STOP

RQ4 使用与 Stage-1 完全相同的 21 个 QA case,从已落盘的 contaminated d=3 responses 重建 source-only snapshot;**21/21 pre-correction hash 一致**。每个 case 的 3 个官方 query 由稳定 SHA-256 在 API 调用前分为 2 个 development query 和 1 个 held-out query。排序只看 development judge1;held-out 同时跑 judge1 / judge2 / AND。纠正文本仍只来自官方 `correct_answer`,不引入自造 rubric 或安全终点。

7-case pilot 因只有 4 个 held-out-informative case 按冻结规则判 INSUFFICIENT,随后无改规则扩到 21 case。完整结果:

| RQ4 终点 | 结果 |
|---|---:|
| dev-eligible / held-out-informative | 19 / 17 |
| m*=1 / 2 / 3 case 数 | 9 / 7 / 3 |
| 中位 repaired-descendant fraction | **2/3**(门槛 ≤0.40,失败) |
| mean dev recovery ratio | 1.000 |
| mean held-out recovery ratio | **0.412**(门槛 ≥0.80,失败) |
| held-out unsafe:source-only / targeted / full(j1) | 89.5% / 52.6% / 0.0% |
| targeted − full unsafe(j1) | **+0.526 [+0.316,+0.737]** |

equal-count 比较中,正值表示 heuristic 比 targeted 更 unsafe、即 targeted 更好;实际 j1 paired delta 为 random −0.053 [−0.263,+0.158]、recency −0.211 [−0.421,0]、length −0.263 [−0.526,0]、current-unsafe −0.263 [−0.526,0]、deletion-influence −0.211 [−0.474,0]。方向多数相反;judge2 下 recency/length/current-unsafe 更显著优于 targeted。

因此按冻结规则:**selective-feasibility=false,influence-method GO=false,overall STOP**。最重要的机制读法是 development recovery 1.0 降到 held-out 0.412,说明单 query-family influence 排序严重过拟合;当前数据支持“correction residual 需要 broad/full closure”,不支持“少量 influence-ranked descendants 即可修复”。完整判定:`state/rt02_runs/chir_rq4_qa_20260718/verdict_qa_full21.json`;设计:`state/rt02_chir_rq4_design_20260718.md`。

## 2. PairGain MVP(RQ1+RQ2)

### 2.1 设置与完整性

42 QA + 30 Workflow case,每个 case 为 misleading/correct 同步分支、t=0..3,共 **72 records / 576 snapshots / 216 transition rows**。future endpoint `A(t+1)` 只由 MemEvoBench 官方 MISLED judge 输出构成;不新增安全 rubric。主 NLI checkpoint=`MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`,句子抽取、q/D/G 与 epsilon={0.01,0.05,0.1} 均按设计冻结。

原 Workflow runner 以非唯一 `cluster_id` 命名,7 个重复 ID 会覆盖快照;修复版使用稳定 `case_key=wf_row_{absolute row}_cluster_{cluster_id}`。重跑后 **30/30 records、240/240 snapshots、30/30 unique case_key** 均通过存在性/步数检查。

DeBERTa CPU 在 M1 上极慢;Workflow 用同 checkpoint 的 MPS 后端独立重算完整 30 case,没有与 CPU 行混写。22 个 CPU/MPS 重叠 case 的主 epsilon G Spearman=0.99983,median |ΔG|=0.000130,max |ΔG|=0.00265;D median |ΔD|=0.0000565,max |ΔD|=0.000456。该检查支持把差异解释为执行后端浮点误差,而非指标变更。

### 2.2 冻结统计结果

| 主终点 / 模型(Y1) | QA (n=42) | Workflow (n=30) | 合并 (n=72) |
|---|---:|---:|---:|
| current-only CV R² | +0.511 | +0.735 | +0.732 |
| TrustMem-style-only CV R² | −0.056 | −0.072 | −0.045 |
| G-only CV R² | −0.060 | −0.083 | −0.004 |
| joint CV R² | +0.501 | +0.740 | +0.729 |
| joint − current-only | **−0.0096** | +0.0047 | **−0.0025** |
| partial Spearman(G,Y1\|current),95% CI | +0.055 [−0.195,+0.259] | +0.102 [−0.077,+0.361] | **+0.070 [−0.083,+0.200]** |
| whole-curve permutation p | 0.537 | 0.046 | 0.571 |
| RQ1 / RQ2 / overall | false / false / **STOP** | false / true / **STOP** | false / false / **STOP** |

合并 epsilon grid 的 partial Spearman 为 0.016/0.070/0.091(ε=0.01/0.05/0.1):方向同为弱正,但主 case-bootstrap CI 跨 0。最关键的是 joint 没有超越 current-only;因此 G 的现有波动不能建立“控制当前状态后的未来增量预测力”。Workflow 单侧 RQ2 恰过 permutation 门(p=0.046),但 RQ1 仍失败,QA 与合并也不复现,不能保留 PairGain headline。

### 2.3 第二 checkpoint 敏感性

原设计没有冻结敏感性子集大小;因此在主 checkpoint 出数后、敏感性出数前,诚实登记为**事后执行澄清**:按 records 稳定顺序取 QA 10 + Workflow 10,checkpoint=`roberta-large-mnli`,其他定义不变。这一分析只能检查翻转,不能救主结论。

RoBERTa 合并 20-case 仍为 **STOP**:partial Spearman=+0.136 [−0.081,+0.389],current-only CV R²=0.676,joint=0.660(joint−current=−0.0159),permutation p=0.543。QA 10 为 −0.139 [−0.529,+0.374],Workflow 10 为 +0.205 [−0.136,+0.529],两侧均跨 0且 overall STOP。

### 2.4 判定与边界

按冻结必要条件,**RQ1=false,RQ2=false,PairGain overall STOP**。这是清晰负信号,不是“尚未跑出阳性”:完整 72-case 主分析与独立 checkpoint 子集都没有显示 G 在 current A/D 之外的稳定增量价值。Paper A 的当前 headline 应停止;不要继续调 epsilon、aggregation 或样本来追阳性。

必须同时声明:本轮是 existence MVP,不是 proposal 中完整的 intervention stage。TrustMem 是 style reimplementation,且尚未跑 retrieval-only、operator-off、equal-count policy intervention以及预先阈值化的 Brier/AUROC/calibration。因为 RQ1 这个必要前提已失败,proposal §9 的 Stop gate 要求不进入这些昂贵后续;本报告的决定性负结论只依赖官方 unsafe endpoint 上的 RQ1 partial-association CI,不把未完成的完整 RQ2 说成已验证。

## 3. 成本与产物

- 运行:CHIR RQ3 41 case × 6 臂 + RQ4 21 QA case;PairGain 72 case × 双分支 × 4 步。API 主体使用 gpt-4.1-mini 生成+judge1、gpt-4o judge2;API 成本量级 $30-60。NLI 为本地冻结模型,不产生 API 成本。
- 代码:`scripts/run/rt02/`(10 个脚本);判定:`state/rt02_runs/rt02_chir_verdict_20260718.json`、`state/rt02_runs/chir_rq4_qa_20260718/verdict_qa_full21.json`、`state/rt02_runs/rt02_pairgain_verdict_20260718.json`。
- PairGain 分侧判定:`state/rt02_runs/pairgain_qa_20260718/verdict_qa_full42.json`、`state/rt02_runs/pairgain_wf_20260718_v2/verdict_wf_full30.json`;RoBERTa 敏感性:`state/rt02_runs/pairgain_roberta_sensitivity_20260719/`。
- 快照/lineage/judge IO 全落盘,可复算。
