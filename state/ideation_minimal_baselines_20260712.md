# 新方向最小 baseline 结果(gap1 记忆操作归因 / gap4 supersession)· 2026-07-12

> IdeaSpark ideation 出 4 gap,选 gap1(记忆操作反事实归因)+ gap4(supersession 非对称)跑最小 kill-switch。
> 规则(用户):拿到正向就继续做完整 proposal;拿不到就删 baseline 代码换 idea。

## gap4 · Supersession 非对称 —— 判负,删代码

装置 `scripts/run/run_supersession_asymmetry.py`(+ `_answertime.py`):10 persona,同结构对照(只变是否安全承载):benign 陈旧(城市 old→new)vs safety 撤回(过敏→"医生说可能误标")。旋钮=固化 supersession 激进度(annotate/prefer_new/replace,prompt 不提 safety)。

| policy | benign_correct(note) | safety_recall(note) | benign_fresh(answer) | benign_stale(answer) | safety_ok(answer) |
|---|---|---|---|---|---|
| annotate | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 |
| prefer_new | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 |
| replace | 1.00 | **0.50** | 1.00 | 0.00 | 1.00 |

**判定:负。** 核心"交叉前沿/单一策略两边不能全好"被反驳:answer 时 benign 全程 100% 新鲜零陈旧(agent 读"current"标记),**没有 benign 权衡可交易**;prefer_new 两边全满分。唯一效应=极端 replace 下 note 级 safety 掉 0.5(Sofia 过敏整条抹、Martin 降级),但 answer 时都被谨慎答复救回(safety_ok 1.0)。无交叉 → kill-switch 未触发。类比 RQ1:系统比假设的失败更鲁棒。**→ 删 supersession baseline 代码。**

## gap1 · 记忆操作反事实归因 —— 实验正,但方法被 scoop

装置 `scripts/run/run_memop_attribution.py`:6 persona × 3 元凶 op(write-drop/consolidate-drop/retrieve-miss),单元凶构造(held-out oracle 已知)。反事实 restore-one-op 回放定位元凶,对比 LLM-judge 基线。

| 指标 | 值 |
|---|---|
| 失败项(baseline 答错) | 18/18 |
| **反事实定位准确率** | **1.00**(18/18 命中) |
| LLM-judge 定位准确率 | **0.389**(几乎总答 retrieve) |
| random-op restore 修复率(应~0) | **0.00** |

**判定:实验正**——反事实原语 100% 定位、碾压 LLM-judge(39%)、非同义反复控制干净。**但两点诚实**:
1. 100% 有"单元凶构造天生成立"成分;真正有信息量的是 LLM-judge 仅 39%(印证 CAR)。
2. **scoop 未解**:方法 = Causal Agent Replay(2606.08275,intervention algebra + MC-Shapley + CI over agent steps)换成 memory op。正实验不解决"方法=CAR"。CausalFlow(2605.25338)step-level 反事实;TreeMem(2605.04811)记忆管线 credit assignment。

**幸存 novelty delta(要靠它才能过 7)**:
- **restore 干预**(重注入被固化掉的记忆)是记忆持久 substrate 独有,CAR 的前向 do-step 做不到("你不能给一个推理 step 补回它从没有的信息")。
- **真 benchmark 失败预算分解**:HaluMem 自然失败里哪类 op 主导(CAR 不做 memory op)。
- **merge 节点可识别性**(provenance DAG,非 step chain)。

**差异化实验(真 HaluMem,已跑)= 正**。`scripts/run/run_memop_halumem.py`,官方 HaluMem-Medium,3 user × 12 session,事实召回类问题,per-session C^1 固化 → 检索 → 回答;自然失败上用 provenance(question.evidence)做 restore 归因;LLM-judge correctness。
| 指标 | 值 |
|---|---|
| 问题 / 自然失败 / 已解析 | 45 / 27 / 20 |
| 失败预算 | **consolidate=13, retrieve=7, unresolved=7** |
| LLM-judge 在 consolidate 元凶上 recall | **0.077**(13 只对 1) |
| random-restore 修复率(控制,应~0) | **0.185** |
- ✓ **consolidation-drop 主导**(13/20=65%),且归因器**区分**出 7 个 retrieve-miss(非无脑全 consolidate)。
- ✓ **restore 打败 trace-only judge**:judge 看不见被固化掉的证据(recall 7.7%),restore 用 provenance 重放抓到——正是分开 CAR(memory-agnostic/只看 trace)的核心。
- ⚠️ **弱点**:random-restore 0.185(控制不够干净,部分归因或是"任何上下文都救"的非特异效应)→ 全量需 per-item 收紧(evidence-restore 修好且 random 不修);规模小(3user/45问)、单 answerer+judge 同源。
**判定:GO(但 v1 有伪影,已修)**。

### v1 双评估 → v1 伪影 → clean 修复(关键教训)
- v1 proposal 双评估:autoresearch(gpt-4.1-mini)8.0 = 假阳;**opus 5-persona = median 5 REJECT**,重算 JSON 抓到**致命伪影**:v1 的 `restore_consolidate` 与 `restore_retrieve` **是同一个干预**(都注入 gold 证据),13/13 consolidate 元凶两者都修 → "consolidate 65%"是 tie-break 标注产物;LLM-judge 是近常数分类器(26/27 retrieve)。
- **clean 修复**(`run_memop_halumem.py` v2):restore-retrieve 改为**只从现有 store 检索**(不注入,证据不在 store 就 no-op);restore-consolidate 放回 store 再检索;归因靠二者**分歧**;judge 改公平 prompt(告知固化可能丢证据)。
- **clean 结果**(8 user/132 问/89 失败,`state/memop_halumem_clean_20260712.json`):
  | 指标 | 值 |
  |---|---|
  | 失败预算 | consolidate=37, retrieve=4, nonspecific=6, **unresolved=42** |
  | 清洁归因 consolidate 占比 | **0.902** |
  | 两干预分歧 | **43/89**(真区分 op,修掉 v1 伪影) |
  | consolidate 元凶"store 检索修不好" | **37/37**(干净分离) |
  | 公平 trace-judge 在 consolidate 上 recall | **0/37 = 0.0**(结构性盲,C3 强) |
- ✓ 评审致命批评正面解决;⚠️ 诚实边界:**unresolved 47%**(主张限"可干净归因子集")、8 user、单源 judge、C^1 档。
- proposal v2(clean)= `state/proposal_memop_attribution_20260712.md`;重评估(wf_69fd5812)= **median 6(novelty 7),v1 伪影真修但 C2 是新伪影**,5 个 blocking:write/consolidate 混淆、词法阈值脆、rc trivial、share-of-clean 选择偏差、judge 低基率。

### 第三轮:重构 + 收紧(v3)
按评审 4 修复改 harness:①**write 分支**(`written_in_transcript` 单轮答案 membership,解开 write/consolidate 混淆)②**真 store-only 反事实**(rr 由答案定,非词法门;报 store_overlap 阈值敏感)③**distractor-evidence 控制**(注入别问题的证据)④headline 降级 share-of-ALL。
**v3 结果**(15 user/223 问/149 失败,`state/memop_halumem_v3_20260712.json`):
| op | 占全部失败 |
|---|---|
| unresolved | 28.2% |
| **consolidate** | **27.5%**(最大单一可识别原因,占 clean 60%) |
| retrieve | 18.1% |
| nonspecific | 15.4% |
| write | 10.7% |
- distractor 修 consolidate 元凶 **0/41**(gold 非 trivial ✓);两干预分歧 67/149(45%);阈值脆弱带 9/41(透明);公平 judge consolidate 基率 6%、recall 7.3%。
- **诚实故事**:失败干净分解到各 op,consolidation-drop 最大单一原因(28%,**不主导**),trace-only 系统性欠归因。承重=C1(方法+双控制)+C4(可识别性);C2 降为诚实分解。
- proposal 重构为 **v3 以 C1/C4 领衔**;评审 median 6。

### 收敛:真实-6 + 到7唯一路(4轮收紧5评审后)
- v4(LLM write-check+k=8)数字稳到"无主导op"(consolidate23≈retrieve22≈write18),但评审又抓到**"无主导"也是tie-break**(rc修72/rr修31,rc严格强;consolidate占比23-50%随排序漂)。**净判真实-6(非伪影),到7唯一路=造带真值benchmark。** proposal v4在桌面(含地址)。

### 用户选线A → 造带真值benchmark(path-to-7,已建已跑)
`scripts/run/run_memop_groundtruth.py`:真HaluMem trace上**注入已知元凶op**(write_drop/consolidate_drop/retrieve_miss)+注入**干扰事实逼自信答错**(受控oracle缺的硬regime)。**关键机制发现**:restore-修答案的信号在干扰下失效(agent黏着干扰值),真正robust的是**membership信号**(证据在各阶段在不在)。归因=write_ok(LLM读对话)/store_has(严格LLM store成员检查)/retrieve。
**全量结果**(8user,242注入失败,179 confident-wrong,`state/memop_groundtruth_20260712.json`):
| | 归因器 | LLM-judge |
|---|---|---|
| 总体 | **0.55** | 0.37 |
| confident-wrong | **0.547** | 0.374 |
| retrieve_miss | **0.73** | 0.28 |
| consolidate_drop | **0.475** | 0.26 |
| write_drop | 0.44 | 0.56(judge赢) |
- ✓ **验证了核心主张**:provenance归因在硬regime上打赢trace-only(55vs37),且**retrieve/consolidate边界能分开**(自然实验的tie-break在真值上被解决)。
- ⚠️ **软肋**:①绝对55%不惊艳;②**write_drop短板**(44%<judge)——我pipeline无真"写入抽取"步,write-check是LLM读对话~40%误判;③membership检查在改写+干扰下有~30%误差。
- **诚实定位**:path-to-7走通、解决了卡6的两blocker,但落成**验证过的中等结果(1.5x over baseline)**,非干净90%。

### 20260713 · 几何伪影 + 理论弱 + 20u扩规模(三个诚实结论)
- **几何归因器=伪影**:`run_memop_manifold.py`+`memop_hybrid_ablation.py`,几何67% vs LLM55% vs judge36%,消融+10、permutation p=0.005——**但对抗评审拆穿**:手调2刀阈值(0.69)匹配"学出的"分类器,几何只是读注入指纹;可解释系数循环(复述注入设计);sim_r死(0.25<随机);真n=8(GroupKFold)。**score从6倒退到5**。守住没造假:用数据把它证成伪影而非硬包。
- **理论腿弱**:`state/theorem_memop_identifiability_20260713.md`,对抗理论审稿判"assume-observation-then-attribute":引理1平凡、定理1空洞(A3给)、定理2近同义反复(A2′定义)、命题3 hand-waving、带噪推论唯一有内容但并界证错。**修正版(1-ε)^κ精确,但预测"越深越难"与实测(retrieve最好)相反**。**结论:此问题撑不起深定理,理论降格为"形式化框架"小节,不进三大贡献。**
- **20u扩规模(好)**:`run_memop_groundtruth.py --users 20`,`state/memop_groundtruth_20u_20260713.json`。**578注入失败/456自信答错,provenance-restore 55% vs judge 34%,与8u完全复现**(retrieve76.5/consolidate43/write45)。C2从pilot→20 base user,稳。
- **三大贡献重定位(诚实)**:①带真值benchmark(工具)②评测方法学(指纹陷阱+正确协议,拆不倒)③实证(trace-judge失效55vs34,20u复现)。**理论=框架小节;几何=cautionary负结果。** 到7命脉仍=P2自然失败人工κ金标(要用户标)。

## 产物
- `state/supersession_result_20260712.json` / `_answertime_20260712.json`(将随代码删除)
- `state/memop_attribution_result_20260712.json`
- `scripts/run/run_memop_attribution.py`(保留)
