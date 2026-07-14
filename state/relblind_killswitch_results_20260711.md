# Relation-Blind Kill-Switch:核心实验结果(pilot)· 2026-07-11

> proposal_v3 的唯一 kill-switch:种 N=0 可检测的关系错 → C^N 固化 → 测检测器 recall-vs-深度。
> **一句话结论(pilot,待对抗验证 workflow 确认):v3 的"深度单调衰减/固化动力学吸引子" headline 被证伪(是 N=1 悬崖,非深度梯度);但一个更窄、更干净的"单趟固化=洗白算子"发现是真的、显著的。**

## 装置
- Harness:`scripts/run/run_relblind_depth_sweep.py`(纯递归摘要,复用仓库原样 `_OpenAILLM`+`_make_consolidation_prompt`+`_normalize_consolidated_note`,零检索/qdrant/mem0 → 隔离压缩算子)。
- C^N = `note_k = normalize(LLM(prompt(note_{k-1}, k, style)))`,note_0=源文;单 persona=单页,精确等价 `LinkedViewSystem.run_consolidation_passes`。
- 8 personas × 3 算子(tiermem_default / lossy_eventful / lossy_abstractive)× N∈{0,1,2,4,8};检测器 = 盘上 vanilla DeBERTa-MNLI(CPU);固化 = live gpt-4.1-mini(temp 0)。
- 轨迹缓存:`state/relblind_trajectories_v2_20260711.json`;结果:`state/relblind_depth_sweep_v2_20260711.json`。
- 探针家族(每类都种成 N=0 可检):
  - **disambig_relabel**(洗白 headline):源文含显式消歧句"<Surname> is my surname, and I do not have a middle name";错误="<First>'s middle name is <Surname>"。词全在源文(overlap)。
  - **role_swap**(方向错,overlap):agent↔patient 互换。
  - **role_swap_novlp**(负控,无重叠):同互换但 payload 词不在源文。
  - **entity_swap**(粗错对照):born 2035 / Tokyo。
  - **faithful**(假阳控制):真实复述。

## 主结果(recall = P(非entail|错);false-SAFE = P(entail|错))

**disambig_relabel(唯一洗白的家族):**
| 算子 | N=0 | N=1..8(持平) | McNemar N0→N8 |
|---|---|---|---|
| tiermem_default | rec 1.00(8/8 contra) | rec 0.62 / **fsafe 0.38**(3/8 entail) | 3→0,p=0.25(n.s.) |
| lossy_eventful | rec 1.00 | rec 0.12 / **fsafe 0.88**(7/8 entail) | 7→0,**p=0.016** |
| lossy_abstractive | rec 1.00 | rec 0.00 / **fsafe 1.00**(8/8 entail) | 8→0,**p=0.008** |

- **contradiction→entailment 硬翻转**,中间不经 neutral(最强 false-SAFE)。
- **role_swap / role_swap_novlp / entity_swap:三算子每个 N 全程 recall=1.00**(方向错、无重叠错、粗错都不洗;负控成立)。
- faithful 对照:eventful 全程 16/16 entail、default 15/16;abstractive 掉到 8/16(良性遗忘)→ 检测器没有"见谁都翻",仍正常工作。

## 机制(provenance 眼验坐实)
- 洗白 = **固化压掉消歧句、保留误导性姓氏 token**;NLI 词袋蕴含:"middle name is Mark" + premise "Martin Mark..." → entailment。错误被**藏(hidden)非改对(corrected)**。
- `tiermem_default` 的 prompt 明令"Preserve ... explicit updates/corrections",实测**~5/8 persona 保留了"No middle name"句** → 按比例抵抗洗白(故只 0.38)。lossy 算子 N=1 即全丢。
- 对照 RQ1:这与"固化对显式安全标记保真、UAF=0"**不矛盾**——安全标记是要"记住的正向事实",而这里洗白的是"**否定式消歧约束**"(它一旦丢失,残留表面词就反向蕴含错误)。

## 诚实边界(必须守)
1. **不是深度衰减**:洗白在 N=1 一趟完成,N1..N8 持平。**v3 的"深度作为主动洗白动力学/稳定吸引子"字面证伪。** 成立的是"单趟 lossy 固化即洗白"。
2. **算子依赖**:保真 default 只洗 0.38;全洗需我们设计的激进 lossy 算子。
3. **错误类窄**:只有"依赖显式消歧句 + 词重叠残留"这一类洗白;role_swap(方向错)不洗(丢实体→neutral→仍 caught)。
4. **单检测器**:全程 vanilla DeBERTa-MNLI;SummaC 同源 MNLI(S2 已证无效),MiniCheck 离线不可得 → 跨检测器族未测(诚实 limitation)。
5. **pilot 规模**:8 persona/格,远小于计划的 ≥150/格。McNemar 已显著但样本小。

## 待补(对抗验证 workflow 输出后追加)
- workflow `verify-relblind-washing`(run wf_4bdf10d7-e0b):4 证伪线(rigged probe / detector artifact / not-safety / depth claim)+ novelty 重评 + 综合裁决。
- 裁决三选一:proceed_reframed(冲窄 headline)/ retreat_static_matrix(退静态盲区矩阵 ~6.5)/ change_topic。

## 对抗验证裁决(workflow verify-relblind-washing,6 agent,4 证伪线跑了真破坏测试)

**finding_is_real = FALSE。kill-switch 为负。建议 retreat / 换题。novelty≈4,overall≈3.5。**

四条破坏性测试(独立 agent 真跑,非推理):
1. **in-window 控制(proposal 自己要求的,最致命)**:把全源文 + N1 摘要拼一起喂 NLI → **entailment 0/8,回到 contradiction 8/8**。⇒ false-SAFE 只在"消歧句不在前提里"时发生,本质=**证据出窗/遗忘**,不是"洗成保真形态"。
2. **因果 agent 错了**:不做固化、**纯手工删那一句从句**就能完全复现 contra→entail 翻转(e 0.007→0.986)。⇒ 因果是"删从句"而非"固化";"固化=laundering operator"是过度归因。
3. **"certified" 一碰就碎**:第二个便宜的 live gpt-4.1-mini judge **8/8 判 NOT_SUPPORTED**;重注入"no middle name" 8/8 翻回 contradiction;姓氏 token 消融→翻转塌;SummaC max-pool 连 N=0 的 recall=1.00 锚点都反转成 entail 8/8。
4. **锚点是人为的**:换自然 source(无刻意否定从句),注入错误在 **N=0 就已是 entailment(e=0.99)**⇒ 现实条件下根本没有"可检测→被洗白"的状态转变。

叠加:①depth novelty 死(N=1 悬崖,无深度曲线);②唯一现实算子 tiermem_default **p=0.25 不显著**,强效应全在故意做 lossy 的稻草人算子;③静态盲区(HANS/FRANK/BUMP/INFUSE + 2605.12978)代码库自己已认输被 scoop(`rq2_stage_extract.py:15`、`novelty_landscape:23`);④n=8 合成、单弱检测器 = 项目自己的红线"小/合成/单检测器 = 2.5"。

**唯一诚实幸存物(workshop/short-paper 级,非 CCF-A)**:"whole-premise DeBERTa-MNLI 对'摘要删一句显式否定从句'不鲁棒,换个便宜二次信号(LLM-judge/重注入/句级 max-pool)即破。"——一句检测器鲁棒性 note,不是"固化"的因果主张。

**下一步(若还想救,按性价比排序)**:
1. 最便宜的判生死:自然消歧(非植入否定)下,HaluMem 关系切片上"可检测→被 certified"的转变到底存不存在?自然 source 下 N=0 已 entail = 无发现。
2. 只用 realistic default 算子扩到 ≥150 人工金标判别项;仍 n.s. → "洗白"死在唯一会被部署的算子上。
3. 第二独立检测器当**闸门**(非脚注):DeBERTa 与 {gpt judge/MiniCheck/SummaC} 需一致才算 false-SAFE。
4. 预注册"手工删从句"为控制臂,坐实因果只能叫 clause-fragility,不能叫 operator behavior。

裁决全文:`/private/tmp/.../tasks/w87rv1owh.output`(refutations + novelty + synthesis)。
