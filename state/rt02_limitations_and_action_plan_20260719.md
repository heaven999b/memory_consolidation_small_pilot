# RT-02 · 解决不了的问题：论文限制框架 + 行动方案 · 2026-07-19

> **用途**：对每个"我现在解决不了"的问题，给出①论文里怎么诚实写成 limitation ②要真正解决需要什么、成本、以及**一条可执行命令/动作**。
> 配套：`rt02_paper_gap_checklist_20260719.md`（总清单）。凡标 🔒 的都卡在"需你授权花钱/下载"或"只能你做"，代码侧已就绪。

---

## A. 需 API/钱才能解决（代码已就绪，一条命令即跑）

### A1 · 主效应独立确证（B1/B2/B3）🔒钱
- **限制框架**（若不做）：dev 上的信号不能当结论，只能声明"pilot-level"。
- **要什么**：未见 30 QA × 五臂，串行。
- **命令**（授权后）：
  ```
  set -a; source .env.v3; set +a
  .venv_tiermem_v2/bin/python scripts/run/rt02/run_rt02_v2_chir.py \
    --operator summary_rewrite --split confirmatory \
    --outdir state/rt02_runs/v2_conf_chir_summary
  # 再单独一条 append_only（串行，勿并发）
  ```
- **成本**：$8–15 / ~6h。

### A2 · k 敏感性（B4）🔒钱
- **限制框架**（若不做）：整个残留可能是 k=5 的伪影，无法排除。**这是最硬的必做项**。
- **要什么**：k∈{3,10} 各再跑一遍（k=5 即 A1）。
- **命令**：A1 命令加 `--k-retrieval 3` / `--k-retrieval 10`，各写独立 outdir。
- **成本**：约 2× A1。

### A3 · 生成随机性（S1）🔒钱
- **限制框架**（若不做）："单次 temperature-0 生成，未估随机性"——评审可接受但会问。
- **要什么**：temperature>0 重复 3 次。**runner 侧已就绪**（本轮加 `--temperature`，写 `..._seed{1,2,3}` 三个 outdir）。
- **⚠️ stats 侧还有一个小缺口**：`rt02_v2_chir_stats.py` 的 `arm_table` 按 `(domain,cluster_id)` 建字典，**同 case 跨 seed 会互相覆盖**（最后一个 seed 胜）。正确聚合需先给每条 record 打 seed 标签、再按 `(domain,cluster_id,seed)` 分组、每 case 先跨 seed 平均。**这一步是纯代码、不花钱，但等到确定要跑 seed 时再做**（避免在未跑数据上写投机代码）。
- **成本**：3× A1（+ 一次性 stats 小改）。

### A4 · WF 语体匹配臂（S3）🔒钱 + 待建 WF runner
- **限制框架**（若不做）：QA 长度比 0.946 本就匹配、**QA 结论不受影响**；只有 WF（0.344）需声明"official-text 臂含 style confound，未做匹配敏感臂"。
- **要什么**：① 建 WF v2 runner（当前只有 QA runner，**代码缺口**）② 接 `rt02_v2_style_match.py`（已建）。
- **成本**：WF runner 是纯代码（可先建，不花钱）；跑臂需 API。
- **优先级**：低（WF 是 secondary，confirmatory 主线是 QA）。

### A5 · 第二 agent model（S4）🔒钱
- **限制框架**（若不做）："单模型家族（agent=judge1=gpt-4.1-mini）；judge 侧已有 gpt-4o AND 闸门做独立复核"——**部分缓解**。
- **要什么**：A1 命令加 `--model <第二模型>`，写独立 outdir。
- **成本**：≥1× A1。

---

## B. 需你批准下载才能解决

### B1 · 稠密检索（S5）🔒下载
- **限制框架**（若不做）："检索为 TF-IDF 词法 top-k；未与稠密 embedding 检索对比"——声明即可，**TF-IDF 是确定性可复现的合法冻结主检索**。
- **要什么**：`pip install sentence-transformers`（一次下载，含小模型权重）。接口已就绪（`get_retriever("embedding")`），装完一条命令切换。
- **动作**：**需你说"可以装"**。装后加 `RETRIEVERS` 切换即为 dense 敏感臂。

---

## C. 只能你本人解决

### C1 · 引用真伪核验（S6）🔒你
- **问题**：项目内 MemEvoBench `2604.15774`、TrustMem `2606.25161` 等 arXiv 编号是未来日期，**我无法核验其指向真实论文**。
- **动作**：投稿前你必须逐条确认这些编号/标题/作者真实存在且引用正确。**我不能替你做，也不该假装核验过。**

---

## D. 结构性救不了 → 直接写成 limitation（无需再投入）

| 问题 | 论文里的写法（可直接用） |
|---|---|
| **RQ4 selective closure** | "MemEvoBench 每 case 仅 3 个 descendants，40% 预算门在离散化下与方法无关地不可达；single-query influence 排序在 held-out 上过拟合（dev 1.0 → held-out 0.412）。因此本文不主张 selective closure 可行性，结论收窄为 **correction residual 需要广泛/完整闭环**。" |
| **RQ2 超越 TrustMem** | "未获得 TrustMem 官方实现；自建 style-reproduction 打分退化（方差近零），不足以支撑增量性比较。本文改以 current-state / retrieval / random / no-op 等**可构造** baseline 评估 G 的增量。" |
| **NLI 句级盲区** | "语义分离量基于句级 NLI（DeBERTa-MNLI + RoBERTa-MNLI 双 checkpoint），对**跨句关系/角色错标**已知不敏感（金标 recall≈0.50）；故 G 侧（NLI-based）结论**弱于** unsafe-endpoint（judge-based）结论，仅作机制性佐证。" |
| **full_closure 是 oracle 上界** | "full_closure 用官方参考文本（`test_correct_answer`）逐条重写，其 0% unsafe 是**理想化上界**（语体贴合 judge 参考），不代表真实部署可达；仅用于界定残差的可修复上限。" |
| **RQ5 全矩阵** | "外部有效性受限：单 agent 模型族、单主算子、无外部数据集。适用边界仅在 **k、domain、NLI checkpoint** 三个轴上报告，不主张跨模型/跨基准的普适性。" |
| **RT-01 / ConsolidationBench** | 不进 RT-02 论文；已封存判负（`state/RETIRED_LINES.md`）。 |

---

## E. 我现在能不花钱继续做的（按价值排序）

1. ✅ **S1 使能**（`--temperature`）——本轮已做。
2. ⏳ **WF v2 runner**（A4 的代码侧）——纯代码，可先建、mock 自测，不花钱；但 WF 是 secondary，价值中等。
3. ⏳ **多 seed 聚合逻辑**——让 stats 跨 seed 文件聚合并报生成方差；纯代码。
4. ⏳ **limitation 段落成稿**——把上表 D 直接写进一个 paper-draft 限制节。

> 除 E 外，剩下的**都卡在 A（钱）/B（下载）/C（你）**。我把 E 里 2–4 继续做完，就基本触到"不花钱能做的天花板"了。

---

## 一句话

**能不花钱解决的都解决了（构念修复、评估管线、S1 使能、限制框架）；剩下的本质上都要花钱跑确证、批准下载、或你亲自核验引用——每一件的命令/动作都已备好，你一点头就能执行。真正的科学判定仍锁在那次 confirmatory + k 敏感性上。**
