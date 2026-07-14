# Research Proposal v2(按 autoresearch 评审 round-01 整改)· 2026-07-11

> 目标:把 round-01 的 borderline(5/10)拉到 accept 档。整改主轴 = **重定位到唯一 NOVEL 的贡献(memory-benchmark 通胀审计)+ 在设计层堵死全部 6 个 major**。每处标 `[整改#]` 对应 round-01 弱点。

---

## Title
**How Much Do Memory Benchmarks Overstate Faithfulness? A Human-Gold Audit of Relation/Role Blindness in Memory-Consolidation Evaluators**

## 定位(整改#1:headline 从已知的 NLI 盲区,换成唯一 novel 的通胀审计)
本文**不主张**"NLI 对关系错盲"(已被 HANS'19 / FRANK'21 / **INFUSE(2402.17630)** / **BUMP(ACL'23)** 占先——按 FRANK 类别在 minimal pair 上评测并归因 lexical overlap 已是既有结果)。本文的 headline 是**两条 verified-novel 主张**:
- **C1(核心贡献)**:**首次量化**记忆幻觉 benchmark(HaluMem relationship-memory slice)的官方 judge **因关系/角色盲而高估 faithfulness 的点数**,方向恒为 **false-SAFE**,且用 **human-gold** 锚定(非自家 checker)。
- **C2**:**首个 per-(detector × relation-error-type)recall 矩阵,把 nominally relation-aware 方法(SRLScore/QASemConsistency/MiniCheck)一并纳入**,证明**连它们也在跨句 role misbinding 上失败**——即把 INFUSE/BUMP 的 aggregate 盲区,**因果定位**到"跨句关系消歧"这一具体、且现成 relation-aware 工具未覆盖的子类。
Abstract 明确淡化 C0(NLI-vs-overlap)为 motivating 复现,不作贡献。

## 差异化 + 撞车(整改#1,补全 round-01 查到的 scoop)
| prior | 它做了什么 | 本文的 delta |
|---|---|---|
| HANS'19 / FRANK'21 | 单句 NLI overlap 启发式 / PredE-EntE-RoleE 分类(无现代 detector recall) | 现代 detector × 跨句 role recall 矩阵 |
| **INFUSE 2402.17630 / BUMP ACL'23** | 按 FRANK 类别在 minimal pair 评 NLI、归因 lexical overlap | **纳入 relation-aware 方法 + 跨句子类 + 由此导出 benchmark 通胀**(它们止于 NLI aggregate) |
| SRLScore 2305.13309 / QASemConsistency 2410.07473 / MiniCheck 2404.10774 | 谓词-论元/QA 级关系事实性 checker | 作为 baseline **实证它们也漏跨句 role**;不主张"无 relation-aware 方法" |
| **2605.25869 Provenance-Role Collapse** | 命名固化引发 role/provenance collapse(现象) | 本文提供**评测器对该现象的可见性审计 + benchmark 通胀量化**,非再命名现象 |
| MemEvoBench(2604.15774,**id 待核**) | 注入 omitted-caveat 污染、3 轮、GPT-5.2 judge | **降为探索性附录**(其错误分布几乎无 role-swap,不适合测 role 通胀);主张收缩到 HaluMem |

> almost-prior = INFUSE;missed step = **relation-aware 方法也失败 + 跨句因果定位 + human-gold benchmark 通胀数字**。

## 核心机制与四个 disentangling 设计

### 1. Minimal-pair 探针(整改#6:精确 overlap 度量 + 只动 role 不动 overlap)
从 LoCoMo/HaluMem 真源句施加**类型化关系腐蚀**,严格定义:
- **overlap 度量**预注册为 **content-unigram overlap ∧ 不引入源外 content unigram**(辅以 BERTScore-precision 报告);腐蚀**只置换论元槽/关系类型**,保证 wrong filler 必在源中、且**跨错误类型 overlap 在容差内匹配**(报匹配分布,防"role-swap 顺带改词序"这个 order-sensitive 混淆——见整改#3b)。
- 错误类型形式化(整改#11):在谓词-论元 tuple 上定义 **RoleE**=论元槽置换(A0↔A1)、**PredE**=谓词换语义邻近非等价、**EntE/CircE/CorefE** 按 FRANK;boundary case(possessor swap 归 RoleE)显式判定。

### 2. per-(detector × error-type)recall 矩阵(C2)+ 两个拆混淆控制
- baseline:DeBERTa-MNLI / SummaC / **SRLScore / QASemConsistency / MiniCheck** / pinned GPT-judge(整改#8:钉版本/prompt/temp)+ **一个 open judge(FaithLens-class 2512.20182)**。
- **整改#3a windowing 控制**:跨句子类**额外**跑一个"把完整多句上下文 in-window 喂给 per-sentence NLI"的条件 → 剥离"证据出窗(segmentation)"混淆;**只有 in-window 仍失败**才归因 relation-blindness。
- **整改#3b/6 因果控制(非重言负控)**:同一 role 错误,把 wrong filler 换成**源外词**去掉 overlap → 预注册预测 recall 跳回 ~1.0、gap 消失;若不消失则 lexical-overlap 因果解释被证伪。surface-feature-MLP ablation **预声明判定规则**:MLP 仅用 surface feature 即匹配 detector recall ⇒ 该 detector 未加 relational 信号。
- **整改#4 诚实预承诺**:若 SRLScore/QASem/MiniCheck 在 RoleE/PredE 上本就高 recall,结论改写为"**部署中的检测器盲、现成 relation-aware 方法可修**"——仍有用但更弱,如实报告。

### 3. Human-gold benchmark 通胀(C1,整改#2:去循环性)
- 取 HaluMem relationship-memory slice,**先去重再分层抽样**;在 **checker 与官方 judge 分歧的样本**上做 **human adjudication**(2 标注 + 1 裁决)。
- **通胀只对 human-gold 子集报告**(带 CI);**checker 的 precision/FPR(在 relation-CORRECT minimal pair 上测)传播进通胀 CI**——通胀数字锚在 human gold、不锚在自家 checker。
- 报 false-SAFE vs false-UNSAFE confusion(整改#10),不只单 recall。

### 4. 统计预注册(整改#5)
主检验 = **paired McNemar**(每 detector×error-type,checker vs NLI);pairs 上 **bootstrap CI**;设计 **≥150 对/格**(避免 per-cell ~100 的低功效);矩阵多重比较走 **Holm/BH 校正**;通胀 gap 报 CI。全部冻结于跑前。

## 压缩深度轴(整改#7:二选一→降为单张预注册附录图)
不作共等贡献。仅保留**一张预注册附录图**:C^N depth N∈{0,1,2,4,8} 上 relation-fidelity(human-gold 子集)vs detector recall——预测 depth↑ 时 fidelity↓ 而 recall 持平(盲区随压缩加剧)。operator 定义收敛为已实现的 faithful/lossy-eventful 两个真算子,不铺开。

## Falsification(锁定,非重言)
最小实验 = PredE/RoleE 跨句子类上 NLI vs relation-aware checker,in-window 条件下;主指标+方向 = checker recall 显著高(McNemar p<.01);唯一 load-bearing 变量 = filler_lexical_overlap;负控 = 去 overlap → NLI recall 回 ~1.0、gap 消失(不消失则因果解释被证伪)。pilot(8 对 0/8↔8/8)仅作 motivating anecdote,主张由 ≥150/格套件承担(整改#12)。

## Compute(整改:human-gold 明确计入)
单 M1 + <$100 API;human gold = 分歧子集 + 跨句子类,~3-4 人日,报 IAA(尤其 hard 子类)、标注人数、adjudication、reject rate(整改#9)。无 GPU 训练。

## Reviewer concerns 预答(对齐 round-01 major)
1. scoop(INFUSE/BUMP)→ headline 换成 C1/C2,C0 明确淡化,diff table 全纳入。
2. 通胀循环性 → human-gold 锚定 + checker FPR 传播。
3. 跨句混淆 windowing → in-window 控制剥离。
4. relation-aware 已闭合 → 纳入 baseline + 诚实预承诺。
5. 统计 → McNemar+bootstrap+Holm+功效,预注册。
6. confound 标注 → 精确 overlap 度量 + 跨类型匹配 + 只移 overlap 验证。

## Figures(整改#10,定死)
Fig1 detector×error-type recall heatmap(relation/role 列发暗,每格 CI);Fig2 overlap vs no-overlap 配对斜率图(负控);Fig3 human-gold vs checker-labeled 通胀拆分表 + false-SAFE/UNSAFE confusion;附录 Fig depth×fidelity/recall。

---

**一句话**:v2 把卖点从"已知的 NLI 盲"整体让位给"**human-gold 量化的 memory-benchmark faithfulness 通胀**(C1)+ 连 relation-aware 方法也漏的跨句 role 盲的因果定位(C2)",并在设计层用 human-gold/windowing/relation-aware-baseline/预注册统计堵死全部 major——把 novelty 与 experimental-validation 的天花板同时抬起。
