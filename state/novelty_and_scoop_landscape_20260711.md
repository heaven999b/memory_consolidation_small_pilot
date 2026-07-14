# Novelty 重构 + Scoop 核查(web+PDF 核过)· 2026-07-11

> 由 novelty-lift workflow 产出、硬审(含 2605.12978 全文 PDF 逐词核查)固化。**换窗口后先读这份定 novelty 边界,别再重查。**

## 结论:novelty 从 6→7 的路径 = 动态重构(Reframe 2/攻击类的经验版)
静态"评测器盲于关系错"= novelty 6(被 HANS/FRANK/INFUSE/BUMP 占先)。要 7,必须换成**动态** headline:**"固化随深度主动把可检错误洗进评测器盲区"**(无人占据)。这是 v3 proposal 的核心(见 `state/proposal_v3_20260711.md`)。

## 三个候选重构(可辩护 novelty,已 discount 自评)
| 重构 | novelty | 要点 | 短板 |
|---|---|---|---|
| **② Overlap-Kernel Blind Cone**(分离判据 + 固化=收缩映射把错误拖进盲锥 + 可证跳出 certifier) | **7.0**(赢家) | separation criterion + 新动力学定理 + provable-surpass 三元组无人占 | 全押在一个**经验收缩常数**上(kill-switch);invariance lemma 是 folklore |
| ① Consolidation Laundering(会话级攻击诱导可信固化合成假绑定) | 6.5 | 会话级弱对抗 + 跨 evaluator-类 transfer + overlap-monotonicity lemma | 形式后端只 lemma;transfer 吊在"relation-aware 抓不抓 split case";"laundering"与 2606.24322 撞词 |
| ③ Role-Sealed Memory(predicate-argument 密封 + detectable-permutation 保证) | 6.0 | intra-item 槽位密封 + soundness/completeness | 保证=extractor 质量,读作工程拼装 |

**采纳**:v3 用 ② 的"收缩/吸引子"命题的**经验版**当 headline(测 recall-vs-深度衰减),形式部分只作 motivation 不承重 → 既拿 novelty 7 又实验便宜。

## Kill-switch(唯一决定成败)
novelty 7 与总分 7 都 **conditional on**:固化在真实 HaluMem/LoCoMo 上**真的把角色错误随深度拖进盲区**(检测器 recall 随 N 下降 / kernel 收缩常数 <1)。**M1 几天可测,必须最先跑。** 不成立 → 全部跌破 7,退回"静态三维盲区矩阵"(~6.5)或换题。

## Scoop 地图(arxiv id 已 web/PDF 核实)
| 论文 | 状态 | 与本工作的关系 |
|---|---|---|
| HANS'19 / FRANK'21(2104.13346) / **INFUSE 2402.17630** / **BUMP ACL'23** | 已占先**静态** NLI 逐类别盲区 | v3 的"NLI 盲"半边正确认输 SCOOPED,只作 motivation |
| **2605.12978** "Useful Memories Become Faulty…" | **全文 PDF 核过**:无对抗/无跨检测器 transfer/无定理/无 role 分类(69页,逐词=0) | 最近的经验邻居;它当良性退化,v3 转"深度洗白 detectability"+ 跨检测器类 → delta 干净 |
| **2605.22842** Misattribution Gap | 直接写共享 store 的 doc 投毒 + Retrieval-Coverage 分离定理 | 注入不经固化 rewrite;v3 洗白经可信固化、guarantee 在 evaluator 类 |
| **2605.25869** MemIR(typed-memory 防御) | 全文核过:只 7 类 atom,无 role 槽/无定理/无 role-swap 闭合实验 | **最大残余 scoop 威胁**——若它长出定理会挤压 C2 certifier 半边;故 C1 经验曲线主承重 |
| 2606.12703 SMSR / 2606.24322 TMA-NM | item/origin 级权威绑定(HMAC),不覆盖 intra-item 槽位;TMA-NM 证"authority 不被 laundering 降低"(**撞"laundering"措辞**) | 与 intra-item relation binding 不同层,可辩 |
| SRLScore 2305.13309 / QASemConsistency 2410.07473 / MiniCheck 2404.10774 | 成熟的关系感知 checker | 作 baseline 实证它们**跨句也漏**;不得声称"无 relation-aware 方法" |
| HaluMem 2511.03506 | 确认真实,有 relationship slice | C3 通胀审计靶子 |
| MemEvoBench 2604.15774 | **id 检索未命中、存疑**,错误分布几乎无 role-swap | inflation 主张收缩到 HaluMem;此 id camera-ready 前必须核实或删 |

> 关键 de-risk:2605.12978 的 PDF 已落 `~/.claude/projects/-Users-yihaiwen/6d90903b.../tool-results/webfetch-1783739357144-6q3fjf.pdf`(换会话会丢,结论已记于上)。
