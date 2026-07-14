# 两轮正式评审汇总(用户 autoresearch review track,5 persona 中位数 + web novelty 核查)· 2026-07-11

> autoresearch 项目在 `/Users/yihaiwen/Documents/New project/proposal_review_relation_blind/`(reviews/、state/ 已落盘)。本文件是两轮结果+裁决的固化,换窗口先读这份定"还差什么到 7"。

## Round-01(评 v1 审计版 `proposal_ideaspark_20260711.md`)
中位数:novelty 6 / comprehensiveness 7 / clarity 7 / technical_depth 6 / experimental_validation 5 → **overall 5,全 borderline**。
- 致命:①headline"NLI 盲于关系错"被 **INFUSE/BUMP/HANS/FRANK** 部分 scoop;②通胀审计用自家 checker 当 oracle=循环;③跨句混淆 windowing;④无统计。
- 唯一 NOVEL = C2 通胀审计(memory benchmark judge 高估)。

## Round-02(评 v2 加固版 `proposal_ideaspark_v2_20260711.md`)
中位数:novelty 6(Theorist 给 7) / comprehensiveness 7 / clarity 7 / **technical_depth 7↑** / **experimental_validation 4↓** → **overall 6,五位零方差全 borderline**。
- 四个致命项全用机制解决(scoop 认输降 motivation、human-gold 锚定、in-window 控制、预注册统计)→ 抬离 reject 线。
- **卡在 6 的唯一原因(五位一致):实验没跑。** exp_validation 被结构性封顶在 3-4;"设计 registered-report 级 ≠ 证据"。
- 裁决原话:**"7 在 proposal 阶段不可达……任何文本打磨都换不来第 7 分"**;"one discriminating pilot cell away from accept"。

## 到 7 的确切条件(评审给的,已并入 v3)
1. **[决定性] 跑一个判别性 pilot**:主 cell(PredE/RoleE 跨句、in-window)≥150 对,报 McNemar 方向 + 负控反转(去 overlap→recall 回~1)。→ **这一个数字 = borderline→accept**。
2. 实测 HaluMem relationship slice 的 **RoleE 占比**(C1 存活前提;稀疏则 C1 塌 null)。
3. C1 通胀 estimand 钉死(disagreement 子集→全库映射);核/删 MemEvoBench id;RoleE 形式定义;depth 轴二选一。

## 关于"novelty 必须到 7"(用户后续要求)→ 见 `novelty_and_scoop_landscape_20260711.md`
静态审计封顶 novelty 6;换**动态 headline("固化随深度主动洗白")= v3** 才到 7,但 conditional on kill-switch 曲线下降。

## 关于"审稿人容易给 2/2.5"(用户担忧,正确)
这类"审计+弱修复"高危。**决定 7 还是 2.5 的就一件事:那条 recall-vs-固化深度曲线,在真实 benchmark 上大、干净、human-gold 验证。** 小/合成/只交 proposal = 2.5。修复(provenance-linked 固化 + 关系级校验)只当"挽回多少 recall"探针,别喊 solved。**纪律:先跑便宜 kill-switch,大而干净才做,交跑出的结果不交 proposal。**
