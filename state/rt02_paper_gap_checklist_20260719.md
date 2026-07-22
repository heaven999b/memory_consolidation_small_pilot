# RT-02 → 论文：还差什么 · 问题清单 · 2026-07-19

> **用途**：把 RT-02 从"一堆实验"推到"可投稿论文"，逐条列出还没解决的问题、怎么解决、成本，以及**明确放弃**的部分。
> **主攻**：Paper B / CHIR（RQ3 改写版）。Paper A / PairGain 降为次要。
> **依据**：`rt02_v1_critical_review_20260719.md`（6 根因）、`rt02_v2_dev_smoke_report_20260719.md`、检索挤出审计（本文件 §0）、`rt02_v2_benchmark_alignment_20260719.md`。

---

## 0. 触发本次重构的关键审计发现（必须写进论文的方法节）

真实检索日志显示：**d3 池更大 → 被纠正的 source 被后代挤出 top-k**。

| 算子 | 后代占用槽位 | 纠正源被召回 (contam_d3) | 对照 (contam_d0) | d3−d0 |
|---|---|---|---|---|
| append_only | 3 | **1/3** | 3/3 | +0.78 |
| summary_rewrite | 1（摘要） | **2/3** | 3/3 | +0.67 |

效应量随**被挤槽位数**走，而非随"污染是否被固化携带"走。→ 朴素的 `d3−d0` 把**语义污染持久化**与**检索挤出**混在一起。

**这直接导致 RQ3 改写**（下节），并把主终点从 `d3−d0` 换成 `d3−safe_d3`（同池大小、同检索结构）。

---

## 1. RQ 重构决定

| RQ | 决定 | 说明 |
|---|---|---|
| **RQ3** | ✅ **改写后保留（主线）** | 新问法：**残留有多少来自语义污染持久化、多少来自检索挤出？** 用 `semantic_residual`(d3−safe_d3) / `displacement_effect`(benign_vol−d0) / `composite`(d3−d0) 三量分解 |
| **RQ1** | 🟡 **保留但降级** | 需先修好载体可比性（已用 `carrier_matched` 修）；novelty 因 RQ2 退休而受限 |
| **RQ2** | ❌ **退休** | 对手指标退化成常数、拿不到官方 TrustMem 代码。**并入 RQ1** 作"G vs current/retrieval/random/no-op 等**可得** baseline" |
| **RQ4** | ❌ **退休** | 每 case 仅 3 descendants → 40% 门与方法无关地不可达；要救须另造数据集。**战果保留**：`dev 1.0→held-out 0.412` 过拟合发现降级为 Paper B 的限制/负结论 |
| **RQ5** | ❌ **缩到最小** | 全矩阵砍掉；只保留几乎免费的 k 敏感性、域分层、第二 NLI checkpoint |

---

## 2. 阻断性问题（不解决 = 没有论文）

| # | 问题 | 怎么解决 | 成本 | 状态 |
|---|---|---|---|---|
| B1 | **主效应未在独立数据上确证** | 在**未见 30 QA** 上跑 confirmatory（串行，禁并发） | **$8–15 / ~6h** | 代码+配置就绪，**等授权** |
| B2 | **benign_vol 从未真跑过** | 已实现，随 confirmatory 跑满五臂 | 含在 B1 | 代码就绪 |
| B3 | **残留分解是否成立**（真正的生死门） | confirmatory 后看 `semantic_residual` CI 是否 >0 | 含在 B1 | 待跑 |
| B4 | **k 敏感性** | k∈{3,5,10} 各跑一遍；若效应只在 k=5 存在＝伪影 | 约 2× B1 | 已写进配置 |

> **B3 的两种结局都能成文，但是两篇不同的论文**：
> - `semantic_residual` 显著 → "污染在固化状态里语义持久化，改源不足以闭环"（原设想）
> - `semantic_residual`≈0、`displacement` 主导 → "**固化产物挤占检索预算，导致纠正无法被召回**"（更可操作，也很有意思）
> **不要预设结论，让分解决定 headline。**

## 3. 应该解决（不致命，但评审会问）

| # | 问题 | 怎么解决 | 成本 |
|---|---|---|---|
| S1 | 生成随机性未估 | ≥3 seed 重复，纳入 case bootstrap | 3× B1 |
| S2 | `full_closure` 是 oracle 上界（官方参考文本语体贴 judge，0% unsafe 不真实） | 声明为上界；或加"非 oracle 闭合"臂 | 声明=免费 |
| S3 | WF 侧纠正文本长度失配（median 0.344；QA 0.946 无此问题） | 用已建的 `rt02_v2_style_match.py` 跑 **WF 专属**语体匹配敏感臂 | 需 API 小额 |
| S4 | 单模型家族（agent=judge1=gpt-4.1-mini） | 加第二 agent model；judge 已有 gpt-4o AND 闸门 | 需 API |
| S5 | 检索是 TF-IDF 非稠密（非文献标配） | 装 sentence-transformers 跑 dense 敏感臂（接口已就绪） | **需你批准下载** |
| S6 | **引用真伪未核验** | 项目内 MemEvoBench `2604.15774`、TrustMem `2606.25161` 等编号我**无法核验**；投稿前必须你亲自确认 | **需你做** |

## 4. 救不了 → 写成限制（别再投入）

| 问题 | 为什么救不了 | 论文里怎么写 |
|---|---|---|
| RQ4 selective closure | MemEvoBench 每 case 仅 3 descendants，预算门与方法无关地不可达 | "单-query influence 排序在 held-out 上过拟合（1.0→0.412），当前数据规模不支持 selective closure 的可行性判定；结论收窄为需广泛闭环" |
| RQ2 超越 TrustMem | 无官方代码；自实现退化成常数 | "未与 TrustMem 官方实现比较；改与 current-state/retrieval/random/no-op 等可得 baseline 比较" |
| NLI 句级盲区 | 本地无 MiniCheck/AlignScore | "语义分离量基于句级 MNLI，对跨句关系错标已知不敏感（recall≈0.50），故 NLI 侧结论弱于 judge 侧" |
| RT-02 RQ5 全矩阵 | 无第二 open model / 外部数据集 | "适用边界仅在 k、域、NLI checkpoint 三个轴上报告" |

## 5. Paper A / PairGain 的额外缺口（若要继续）

| # | 问题 | 状态 |
|---|---|---|
| A1 | 载体可比性（`consolidated_state` 在 append 下结构性为零 → operator 对比曾是循环论证） | ✅ 已用 `carrier_matched` 修，待 confirmatory 验证 |
| A2 | n=6 的 permutation p=0.023 **不可信**（6 case/720 排列/24 行 5 折） | 只能靠 confirmatory 重测 |
| A3 | horizon 太浅（4–5 transitions，测不了设计要的 t+2/t+3） | 需加 transitions（成本线性上升） |
| A4 | novelty 天花板被 RQ2 退休压低 | 结构性，无法修 |

**建议**：Paper A 不与 Paper B 平行投入；等 B3 分解结果出来再决定是否跟投。

---

## 6. 最短路径（我的建议顺序）

1. **B1+B2+B3**：跑 confirmatory 五臂 × 未见 30 QA（**唯一需要你现在授权花钱的一步**）
2. 看分解结果 → 定 headline（语义型 or 挤出型）
3. **B4** k 敏感性（必做，否则效应可能是 k 的伪影）
4. **S1** 多 seed → **S2** 声明上界 → **S3/S4/S5** 按需
5. **S6** 引用核验（你做）
6. Paper A 视 B 的结果决定

**一句话**：现在离论文最近的一步是**跑那次 confirmatory 并看残留分解**——它同时决定"有没有效应"和"这是哪一篇论文"。
