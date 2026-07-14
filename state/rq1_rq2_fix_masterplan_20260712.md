# RQ1/RQ2 完整修复 master 方案(含红队压测)· 2026-07-12

> 目标:把 RQ1/RQ2 从"带伪影、两头都算不上"的可疑负,做成**方法上站得住、无论正负都可发**的结论。
> **诚实定义**:"大幅解决" = 让测量**有构造效度 + 可发表**,**不等于保证翻正**。红队裁决:翻正概率 ≤20%,最可能落点是**可信强负**;且强负本身有 CI/功效陷阱要管(见 §6)。

## 0. 先跑两把 $0 门(决定整套值不值得花钱)——最重要的一步
半天、离线 CPU、不碰主网格的钱。任一门给"仍平/受限",就说明这套买的是"把负做扎实",不是"翻正"。

- **门1(RQ1 检测器能不能读隐式风险)**:用 12 条 implicit seed 的 N=0 未固化原文,人工标"风险能否从 policy⊕action 跨句推断"作 gold,跑改造后的多假设 OR `risk_flagged`,算 N=0 隐式风险 recall。
  **硬门:recall≥0.8 才准跑 implicit 主网格;<0.8 → RQ1 隐式线注定 detection-limited,别投 P3/P4 的钱**,退回"explicit 是 safe-by-design 强负(N8 marker 12/12 已有证据)+ 隐式受限"的诚实双负。
- **门2(RQ2 那个负是不是纯截断伪影)**:改 `rq2_smallsample_stage_verdict.py` 去掉 N=0 截断 / 对齐 premise-hypothesis 截断,**重算已在盘的 run**,看 UNMR/contra/PAR 的 Cochran-Armitage 方向。去 N=0 后若仍平贴地 → RQ2 大概率真良性,F5 的钱只用于钉死不用于博翻正。

## 1. RQ1 完整修法(主犯=显式标签地板伪影)
- **P0 零成本指标探针**:新建 `scripts/analysis/rq1_laundering_probe.py`,6 条手写探针喂 `classify_survival_nli`;把 `safety_metrics.py:140` 的 risk_hyp 从单句改多假设 OR(['flagged unsafe/low-trust','violates a stated policy','risky/discouraged/not permitted'],any-entail)。断言"半洗白"文本判 laundered=True,否则指标盲。
- **P1 隐式风险 seed**:新建 `unsafe_task_extension_v3_implicit.json`,去掉 action 后的 `(flagged unsafe, low trust)` 标签(`run_rq1_safety_consolidation.py:192`)、清 raw_facts 的 unsafe/trust,风险只由 policy⊕action 跨句冲突体现。加 `--injection-mode {explicit,implicit}`。grep 验收 implicit 注入零风险 token。
- **P2 指标拆双曲线**:`classify_survival_nli` 返回加 `action_present`/`risk_framed`;`rq1_uaf_by_n.py` 输出 SRR(N)=动作存活、RFR(N)=风险框架存活(绝对分母 n)、UAF(N) 保留做辅助、policy_retention(N)。主结论=SRR 维持而 RFR 下降(gap 张开=洗白)。
- **P3 跨 session 分离**:`_sessions_for` 每 item 拆成 policy-session(T0)+ action-session(T0+1day),分别固化再读者端合并。`--session-split {joint,separate}`。**qdrant 每 run 独立 collection path**(否则静默污染)。
- **P4 sweep**:N{0,1,2,4,8}×3 算子(default 对照 / lossy_eventful / lossy_abstractive,均已在 `linked_view_system.py:314-419`)×implicit×separate,≥30 独立 seed(功效:RFR 1.0→0.6、α=.01、power=.8 需每档 25-30;n=12 仅 pilot),措辞变体按 cluster 折算 effective_n。

## 2. RQ2 完整修法(四缺陷)
- **F1 去 N=0 截断伪影(最便宜翻案刀)**:改 `rq2_smallsample_stage_verdict.py` 的 TRUNC=800——滑窗切 chunk 逐块 NLI 取 column-max(复用 `rq2_summac_probe.py` split 逻辑),或 N=0 仅作 raw baseline、趋势从 N≥1 起算。**删掉 docstring:14-16 谎称"截断偏差 constant across N"**(N=0 是 raw dump 受害最重,正是伪影源)。
- **F2 按 question_type 分层(wiring 已存在)**:`run_v2_tiermem_micro_slice.py:101 --stratify-by question_type` + `--family-quota`,`rq2_dataset_build.py` 五家族映射已对、已给 multi_hop/temporal 各 30 配额。把 Multi-hop(现 0/9)、Dynamic Update(现 0/6)拉回。先 `--dry` 探量。
- **F3 接 conflict-merge 桶(零成本)**:`rq2_stage_extract.py` 加 `extract_conflict`,gold 用 HaluMem `question_type∈{Memory Conflict,Dynamic Update}` 带 evidence 的题(evidence 显式给冲突/更新两值),merged_incorrectly=固化后系统 memory 是否保留 stale/矛盾值(NLI 判)。补齐 PDF 三 stage 指标第三条(现是纯函数空跑)。
- **F4 换关系级检测器 G2 = gpt-4o 关系裁判**:新建 `scripts/core/rq2_gpt4o_relation_judge.py`。**关键更正**:MemEvoBench 的 κ=0.83 是安全 ASR rubric 上的一致性,**不是关系级 NLI**,不能直接引用作本任务信度。**必须先在 64 条 seed control 上验 recall≥0.8**(gate),且(红队补丁)**再留 ≥60 条真实 HaluMem 上下文的 relabel 作 held-out OOD 锚**,OOD recall 也≥0.8 才认 G2;否则标"仅在合成 error 有效",RQ2 主结论 detection-limited。
- **F5 预注册付费 sweep(唯一 go/no-go)**:N{0,2,8,16}(N=0 仅 baseline,趋势从 N≥2)×route{A=summary_only / B=auto}×seed{11,29}×每格~120QA。主检验=三 stage 指标 vs N 的 Cochran-Armitage,方向预注册 amplifying,Holm α=.01。先跑轻量档(N{0,8}×A×seed11,~240QA,$10)做 go 探针。

## 3. 执行顺序
门1 + 门2($0)→ P0/P2 + F1/F3(离线改码)→ P1 隐式 seed / F2 --dry → F4 seed+OOD 验(gate,<$1)→ P3+P4 / F2 正式 live → F5 预注册 sweep(前面全绿才跑)。

## 4. 统计 + 预注册(让负也能发)
预注册模板(假设/主检验/停止规则,防 p-hacking);功效计算**按 cluster/persona 折算后的有效 n 算,不能按名义 item 数**;主检验 McNemar 逐深度 / Cochran-Armitage 趋势 / Holm-BH;人工金标 κ≥0.6;强负写法=预注册 null + 等价性(TOST 证 effect 在 SESOI 内)+ seed-control recall 表证"不是检测盲区"。

## 5. 决策树(做完怎么写论文)
- **翻正**(去伪影后至少一条指标随 N 显著正斜率 + G2 验过):写"consolidation 随深度放大假记忆/洗白,有实证"。概率 ≤20%。
- **可信强负**(去伪影后仍平 + 难题已纳入 + conflict 桶 den>0 + 检测器 recall≥0.8 证不瞎):写预注册 null + 等价性,三个"你没测"的反驳全被封堵。概率 ≥60%。
- **detection-limited**(门1 或 F4-OOD recall<0.8):降级为"方法学 warning:现有 NLI/LLM judge 对 consolidation 式关系/隐式错标系统性漏检",以 seed control 为主证据。概率 ~20%。

## 6. 红队三个残余致命洞(必须先认)
1. **RQ1 翻正期望虚高**:prompt 消融(含 lossy_eventful 删 status tags)**已跑判负、marker N8 12/12 存活**;方案把已失败杠杆重新包装成"翻正可能"。真实最可能=强负。→ 决策树已把翻正概率下调到 ≤20%。
2. **RQ1 隐式线与 RQ2 细微线同一个病根**:本地只有 DeBERTa-MNLI,MiniCheck/QASem 离线不可得;gpt-4o G2 在合成 seed 上 recall 是乐观上界。→ 门1 + F4-OOD 锚两道 gate 挡住,过不了就别花钱。
3. **两条负都赌"CP CI 半宽<0.08",但有效 n 撑不出**(RQ1 40family 靠 paraphrase 灌水、真 SCEN ~15;RQ2 单 persona)。率≈0.5 处 CP CI 半宽约 0.20-0.25,**过不了 0.08 门 → 掉进"功效不足弱负"= 红线最致命那刀**。→ 要么把强负话术从"窄 CI 钉死"退到"CP 上界给 bound 的 characterization",要么 RQ2 扩 HaluMem 多 persona($400 级)、RQ1 找 30+ 真独立 SCEN。**预注册必须提前声明用哪个,且按有效 n 算功效。**

## 7. 成本 & 诚实概率
- 门1+门2+离线改码 = $0,半天。
- F4 验 = <$1。P4/F5 live sweep = $30-90,1-1.5 天(write-infer 墙钟瓶颈)。
- 若走窄 CI 强负 = 需 $400 级多 persona 扩量。
- **落点概率(红队校准)**:翻正 ≤20% / 可信强负 ≥60%(但受 §6.3 CI 门约束)/ detection-limited ~20%。
