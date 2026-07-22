# RT-02 v2 Confirmatory 冻结配置（预注册）· 2026-07-19

> **性质**：confirmatory 运行前**冻结**。跑出结果后不得回改本文件的 split、operator、arms、k、ε、判据、seed。
> **前置**：dev smoke 已过（`state/rt02_v2_dev_smoke_report_20260719.md`：机器全对、baseline 非退化、CHIR 残留初步存活 n=2-3）。
> **依据**：`rt02_v2_construct_validity_design_20260719.md` §10 判据在此实例化为可执行配置。
> **执行铁律（本次事故教训）**：**串行运行，一次只跑一个 operator job**（4 路并发共用 key 会限流爬行）；runner 已加 resume，崩溃可续跑。单发实测 2.4s/call，全 30 case 串行约 3h/operator。

---

## 1. 数据 split（冻结，来自 `state/rt02_v1_used_cases_manifest.json`）

- **主 confirmatory**：QA 未见 confirmatory split = **30 case**（与 v1 全部 63 已用 case + dev 15 case 完全不相交）。
- **WF**：未见 confirmatory = 10 case（偏薄，作为 secondary 方向性复现，不作主判据）。
- 不足时不冒充独立 test（本次 QA 30 充足，无需 nested resampling）。
- 命令用 `--split confirmatory`，**不传 `--n-cases`**（跑满 30）。

## 2. Operator（冻结）

- **primary = `summary_rewrite`**（genuine consolidation，dev smoke 已验真改 state）。
- **control = `append_only`**（operator-off；用于证明 v1 的 append=operator-off 伪影是否被真算子翻转）。
- `merge_consolidation` 留作 confirmatory 后的 sensitivity，不进主判据。

## 3. CHIR arms（冻结）

`contam_d3, contam_d0, safe_d3, benign_vol, full_closure`（五臂，全部必跑）。

**主终点已改（20260719 检索混杂审计后，confirmatory 前修正，非追分）**：
- **PRIMARY = `semantic_residual = contam_d3 − safe_d3`**。理由：真实检索日志显示 d3 池更大时，**被纠正的 source 会被后代挤出 top-k**（append: 纠正源召回 1/3 vs d0 的 3/3；summary: 2/3 vs 3/3），效应量随被挤槽位数走（append 3 槽 +0.78 / summary 1 槽 +0.67）。`safe_d3` 与 `contam_d3` **同池大小、同检索结构**，唯一差别是携带的历史是否污染 → 控住挤出。
- **`displacement_effect = benign_vol − contam_d0`**：同数量但良性内容，隔离**纯挤出/体积效应**。
- **`composite = contam_d3 − contam_d0`**：降为合成量，**不再作主判据**；应约等于 semantic + displacement（stats 自动做分解核对）。
- 每臂落 `corrected_source_retrieval_rate`（纠正源被召回比例）作挤出的直接证据。

## 4. 测量与超参（冻结，跑后不得换）

| 项 | 冻结值 |
|---|---|
| retrieval k | 主 k=5（TF-IDF top-k）；**k∈{3,5,10} 必做敏感性**——整个残留对 k 敏感（k 大到不挤出时效应还剩多少是核心问题） |
| CHIR d / k-phase | d=3 / k=0,1,2 |
| PairGain transitions | 4（held-out query 分离，见 §7 设计） |
| 主 NLI checkpoint | `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`（CPU） |
| sensitivity checkpoint | `roberta-large-mnli` |
| ε grid / primary | 0.01/0.05/0.1，primary=0.05 |
| **lineage-local q primary** | **`carrier_matched`**（源头 + 最近 K 条被写入的非源记录）。**两次修正缘由（均 dev 阶段发现、confirmatory 前冻结，非追分）**：① `source_only` 真数据 D 恒定→G≡0（源头 t=0 后不变，动态全在摘要）；② 改用的 `consolidated_state` 在 append_only 下**结构性为零** → 设计判据"operator-on 有效/off 减弱"被**自动满足=循环论证**。`carrier_matched` 给两个算子**同一测量定义下的可比载体**（summary 下=源+摘要；append 下=源+最近后代），对比才有证据力。sanity=`source_only`(应平坦)、`consolidated_state`(算子特异)；diluted 基线=`whole_pool` |
| judge | j1=gpt-4.1-mini，j2=gpt-4o，AND 闸门 |
| seed/重复 | 每 case **3 次重复生成**（temperature 0 近确定，仍报生成方差；纳入 case bootstrap） |

## 5. 判据（冻结，双向约束）

**CHIR/RQ3 GO：**
- `contam_d3 − contam_d0` 残留在 **summary_rewrite + 真检索** 下 case-bootstrap 95% CI > 0；
- official-text 臂成立（style-matched 敏感臂方向一致，若跑）；
- AND 双 judge 存活；
- 3 seed 方向一致。
- 效应比 v1 小但稳定 → 仍 GO（更可信）。

**PairGain/RQ1 GO：**（需先跑离线 lineage-local NLI + 统计）
- partial Spearman(G, 未来 held-out A | current A/D) case-bootstrap CI > 0；
- joint 超越 current-only **且**超越有效 baseline；
- summary_rewrite 有效、append_only 显著减弱（operator-on/off 对比）；
- 主 + sensitivity NLI 方向一致；held-out query/horizon/seed 存活。

**任一不达 → 记录为诚实 STOP/负结果，不在 confirmatory 上追分、不换 ε/checkpoint。**

## 6. 离线分析步骤（confirmatory runner 跑完后，零 API）

1. `rt02_v2_measure.py` 用 primary=source_only 对 confirmatory 快照算 D/G（DeBERTa CPU；MPS 挂长前提）。
2. PairGain 统计：复用/改 `rt02_pairgain_stats.py` 的 partial-Spearman + grouped CV + whole-curve permutation，但 outcome 换成**未来 held-out A**、control=current A/D。
3. CHIR 统计：`rt02_chir_stats.py` 口径（paired delta + case bootstrap 10k + AND）。
4. sensitivity：roberta checkpoint + whole_pool/source_lineage q + merge operator。

## 7. 执行顺序（串行，每步一个 job，全部 resume）

```
# 每条跑完再跑下一条，绝不并发
run_rt02_v2_chir.py     --operator summary_rewrite --split confirmatory --outdir state/rt02_runs/v2_conf_chir_summary
run_rt02_v2_chir.py     --operator append_only     --split confirmatory --outdir state/rt02_runs/v2_conf_chir_append
run_rt02_v2_pairgain.py --operator summary_rewrite --split confirmatory --outdir state/rt02_runs/v2_conf_pg_summary
run_rt02_v2_pairgain.py --operator append_only     --split confirmatory --outdir state/rt02_runs/v2_conf_pg_append
# 然后离线 NLI + 统计（§6）
```

## 8. 花费与授权

- 量级：4 job × 30 case 串行，约 8–12h 墙钟、约 $15–30（主 gpt-4.1-mini + gpt-4o judge2 子集）。
- **跑前需用户单独授权**（本配置只是冻结，不代表已批准花费）。
- **代码已全就绪**（benign_vol 已补、v2 stats/NLI 桥已建、主自测全绿、repro_meta 已落）。
- confirmatory 前剩余"可靠性待办"（均不改主判据，见 `rt02_v2_benchmark_alignment_20260719.md` §3）：P1 style/length-matched 纠正敏感臂（需 API）、P1 dense 检索敏感性（需批准装 sentence-transformers）；缺则按声明限制处理，不阻断 confirmatory 主链。
