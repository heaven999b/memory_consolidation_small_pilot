# 记忆 Agent 安全研究 · 总 README

> 项目路径:`/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot`
> 底层 fork:`/Users/yihaiwen/Documents/New project/tiermem_upstream`(TierMem)
> 本 README 是本研究的**单一入口**。日期 2026-07-04。所有数字均以 **否定感知 LLM judge** 为准(词法代理只做交叉验证)。

---

## 1. 这是什么(研究定位)

项目起于"**迭代记忆固化中的安全与幻觉**"(以固化深度 N 为因果变量),但经过密集实验 + 5 视角对抗 red-team,**原假设被推翻**,研究**pivot** 到:

> **记忆 agent 的安全,不在"固化阶段"、也不该用"拒答率"来量——而是一个 reader 侧的"知-行分离"(know-do gap),且评测终点的选择会直接翻转结论。**

⚠️ **过程教训(写进方法):** 快/词法终点(payload token 匹配、comply/refuse 判卷)在推理型/对冲型答案上**系统性高估**风险与防御效果。本研究至少 3 次因此得到虚高结论,一上 judge 就塌。**所有安全终点默认用否定感知 LLM judge。**

---

## 2. 核心结论(judge 核实,诚实)

### ✅ 站得住
1. **[方法学·最强] 终点选择翻转结论**(反复验证 3 次,含在本研究自己的分析上):
   - 防御:comply/refuse 判卷 100%→0% vs payload-emission 只到 83%(hedge-refusal);
   - know-do gap:词法 93% vs judge 67%;
   - 跨模型:词法"越大越糟" vs judge"越大越好"。
2. **[现象] know-do gap**:同一条记忆(官方政策 + 团队不安全惯例),
   - 问"政策是什么"→ **100% 背对(doesn't-know = 0,三模型皆是)**;
   - 问"该怎么做"→ **40–67% 违反那条政策**(gpt-4.1-mini 0.67 / gpt-4o 0.47 / gpt-4.1 0.40)。
   - 失败是**行为性、非认知性**;越大模型 gap 越小但不消失;显式 policy-check 干预**部分帮助(67%→50%)、不显著、不闭合**。
3. **[负结果] 固化良性**:迭代固化不放大/不洗白不安全内容(反而经遗忘略降暴露);漏洞在 reader 侧,与固化无关(prompt_only 无记忆 ≥ tiermem)。
4. **[对照] 事实层尊重权威**:事实冲突下 agent 92% 信官方 docs、无视重复假传闻(3× 也灌不进)→ agent **认得权威,只用在"知"不用在"行"**。

### ❌ 已推翻(勿再引用)
- 原论点:不安全记忆随固化深度 N 洗白/放大。
- 07-03 的"写入闸门防御把后门 comply 100%→0%"(判卷措辞假象)。

---

## 3. RQ 完成度审计

### 3.1 原始 PDF 的 RQ(RQ1–5)
| RQ | 主题 | 完成度 | 结论 |
| --- | --- | --- | --- |
| RQ1 | 固化保留/放大不安全 | ✅ 已测(可结) | 推翻:固化良性 |
| RQ2 | 固化造假记忆 | 🟡 部分(欠功效) | N=1 降噪不累积;单 seed/单 backbone |
| RQ3 | provenance 分层来救 | ✅ 已测 | 不支持:auto=summary;写入 no-rewrite 无效 |
| RQ4 | 哪个固化算子最脆 | ❌ 未做 | 只 TierMem 单算子,无 COMEDY/Context-Memory 对比 |
| RQ5 | 失败在哪阶段 | 🟡 部分 | 定位到 reader(回答阶段),非固化/检索 |

### 3.2 原始 PDF 的 E0–E5(注意有两套编号)
| E | 主题 | 完成度 |
| --- | --- | --- |
| E0 | 集成 sanity | ✅ 完成 |
| E1 | HaluMem 幻觉 N-sweep | 🟡 pilot(到 N=8,单 seed) |
| E2(§2)| 良性效用 LoCoMo | 🟡 部分(100QA,N=0/1/2) |
| E2/E3(§5)| 安全持久与洗白 | ✅ 已测(推翻原假设,发现 know-do) |
| E3(§5)| 冲突与更新漂移 | ❌ 未做真实实验 |
| E4 | 防御消融 | 🟡 部分(写入闸门 + 读取侧,均失败;5 种防御完整矩阵未做) |
| E4(§2)| 压缩家族 | ❌ 未做 |
| E5 | 压力(HaluMem-Long/LongMemEval-V2) | ❌ 未做 |

### 3.3 Reframed RQ(RQ1′–5′,本研究主线)
| RQ′ | 主题 | 完成度 | 结论 |
| --- | --- | --- | --- |
| RQ1′ | 惯例 vs 政策 / know-do | ✅ 核心已测 | gap 40–67%,0 无知,跨 3 OpenAI 模型 |
| RQ2′ | 事实层投毒 | 🟡 探过 | 事实稳健(92% 尊重权威),灌不进假信念 |
| RQ3′ | 读取侧防御 | 🟡 部分 | 部分帮助、不显著、不闭合 |
| RQ4′ | hedge-refusal 方法学 | ✅ 强 | 3 实例反复验证 |
| RQ5′ | 记忆/固化 vs reader | ✅ 答清 | reader(prompt_only ≥ tiermem) |

---

## 4. 还能做的测试 / 评估(gap list,按性价比)

**A. 强化核心 know-do gap(优先)**
1. **真·跨家族复现**(Qwen / Claude / Llama)—— 从"OpenAI 家族内"推到普适现象,审稿人必问。**卡在需要非 OpenAI 的 key**(.env 里 QWEN/LLAMA 为空)。
2. **多 seed(≥5,temp>0)** 于关键结论(upstream 已有 `TIERMEM_LLM_TEMPERATURE/SEED` 开关)。
3. **人工校验 judge + Cohen's κ**:把 judge 终点从"更好的代理"升级为可信终点。
4. **扩场景 ≥40 个独立语义族 + 簇稳健 CI**(现在 15 族/n=30)。

**B. 机制与干预(把"发现问题"推到"为什么/怎么修")**
5. **know-do gap 的驱动因子隔离**:helpfulness 压力(情境紧迫性)、salience/recency(惯例更具体/靠后)、framing("该做什么"vs"政策是什么")—— 逐个操纵看哪个调节 gap。
6. **更多闭 gap 干预**:CoT、两阶段"提议→自审"、检索按 trust 降权、显式拒答指令。

**C. 补原始 PDF 的空白**
7. **RQ4/E4 压缩家族**:接 COMEDY / Context-Memory 做多算子对比(从未做)。
8. **E3 冲突/更新漂移轴**(复用 `conflict_task_extension_v2.json`,从未做)。
9. **E5 压力**:HaluMem-Long、LongMemEval-V2(从未做)。
10. **效用 Pareto(§2 E2)**:任何有效防御是否伤 LoCoMo/LongMemEval 良性召回。

**D. 攻击强化**
11. 真 AgentPoison **梯度优化触发词**(vs 现在的 golden-trigger)。
12. **自适应攻击**:攻击者已知语义闸门、专门改写规避,测召回崩多少。

**E. 严谨性(横切)**
13. **所有终点统一 judge**(词法退为交叉验证);null/等价主张用 **TOST**;报告有效独立 n(簇)。

---

## 5. 仓库结构与文件地图

### 5.1 核心代码(项目根)
| 文件 | 用途 |
| --- | --- |
| `safety_metrics.py` | SRR/UAF/RTR@k/洗白检测(已改精确 Clopper-Pearson CI) |
| `safety_honest_metrics.py` | 精确/簇稳健 CI + **payload-emission 行为终点** |
| `safety_write_filter.py` | 写入闸门防御(rules/llm)—— 审计证明无效 |
| `run_rq1_safety_consolidation.py` | 注入 unsafe 种子 → C^N → 度量(fake + tiermem 后端) |
| `run_rq1_safety_judge.py` | LLM 安全 judge(memory/answer 标签) |
| `run_rq1_safety_rescore.py` | 用 payload-emission 诚实重打分已有 run |
| `run_rq1_agentpoison_overlay.py` | AgentPoison 触发 overlay(+ 写入闸门) |
| `run_rq1_authority_experiment.py` | policy×framing×provenance×N×backend 正交受控 harness |
| `run_rq_know_vs_do.py` | **know-do gap 探针**(judge 终点,`--do-intervention`) |
| `run_rq2_factual_poison.py` | 事实层投毒(信念)探针 |
| `run_e1_hallucination_statistics.py` / `_multiseed_*` | E1 幻觉 bootstrap/多 seed 统计 |

### 5.2 攻击 / 数据套件 `benchmarks/safety/`
- `unsafe_seed_suite_v1.json`(12 条带标记 unsafe 种子)
- `agentpoison_trigger_suite_v1.json`(100 条字面触发;**已证过易/循环自证**)
- `stealthy_poison_suite_v1.json`(30 条隐蔽惯例投毒,无关键词/语义触发/竞争 SOP)—— **主力**
- `build_*_suite.py`(生成器)

### 5.3 研究文档 / 报告
- **`RESEARCH_README.md`(本文,入口)**
- `state/研究结果分类整理_20260704.md`(RQ/发现/数据佐证分类)
- `state/safety_axis_honest_final_20260704.md`(诚实 handoff)
- `安全轴_诚实修订_20260704.docx`(诚实修订报告,取代 07-03 overclaim 版)
- `outputs/safety/*.json`(51 份实验报告;关键:`rq_knowdo_*_judge.json`、`rq1_poison_def_*_judged*.json`、`rq1_stealth_*`、`rq1_auth*`)
- `outputs/v2_tiermem_micro/`(E1 幻觉 run + stats)

### 5.4 已作废(勿引用)
- `安全轴_pilot报告_20260703.docx`、`state/e1_stats_and_rq1_safety_axis_20260703.md` 的"防御有效/漏洞闭环"口径。

---

## 6. 如何运行

```bash
cd "/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot"
set -a && source .env.v3 && set +a          # 加载 OPENAI_API_KEY(已配 gpt-4.1-mini)

# know-do gap(主结果,judge 终点)
.venv_tiermem_v2/bin/python run_rq_know_vs_do.py --endpoint judge --report-id knowdo_none
.venv_tiermem_v2/bin/python run_rq_know_vs_do.py --endpoint judge --do-intervention policy_check --report-id knowdo_pcheck
.venv_tiermem_v2/bin/python run_rq_know_vs_do.py --endpoint judge --model gpt-4o --one-variant   # 跨模型

# 事实层投毒
.venv_tiermem_v2/bin/python run_rq2_factual_poison.py --repetition 3

# 隐蔽攻击 + 写入闸门审计(off vs llm),再诚实重打分
.venv_tiermem_v2/bin/python run_rq1_agentpoison_overlay.py --suite benchmarks/safety/stealthy_poison_suite_v1.json --write-filter llm --report-id stealth_llm
python3 run_rq1_safety_rescore.py --judged outputs/safety/<judged>.json

# E1 幻觉统计(零 API)
python3 run_e1_hallucination_statistics.py
```

**须知**:tiermem 路径用 `.venv_tiermem_v2/bin/python`(有 openai/numpy/qdrant);纯统计用系统 `python3`;并发跑批各自独立 `MEM0_DIR=... `;真·跨家族需在 `.env.v3` 填 QWEN/LLAMA/或 Claude 的 key。

---

## 7. 一句话现状
**原"固化深度"论文赌注已死;手里最硬的是"安全评测的终点选择会翻转结论"(方法学)+ know-do gap(agent 40–67% 违反它 100% 能背出的政策)。下一步最该做:真·跨家族复现(需 key)+ 人工校验 judge + 机制因子隔离。**
