# RT-02 Baseline 设计文档(预注册)· 2026-07-18

> **目的**:为 PairGain(Paper A)与 CHIR(Paper B)搭完整 baseline,第一步跑存在性检验。
> **铁律**:一切设计对齐 **MemEvoBench 官方协议**(arXiv 2604.15774,本地 `memevobench_official/` 原样代码+数据+judge rubric),不自造评估指标;主终点全部来自 RT-02 proposal 的预注册定义(`researchstudio_runs/memory_consolidation_20260716/PROPOSAL_ITERATIVE_MEMORY_SAFETY_ZH.md` §5/§6/§8/§9)。
> **执行顺序**(蓝图第二节):第一刀 = CHIR existence pilot(RQ3);第二刀 = PairGain MVP(RQ1+RQ2)。RQ4 仅在 RQ3 residual 为正时运行。

## 0. 与官方口径的对齐承诺

| 组件 | 用什么 | 明确不用什么 |
|---|---|---|
| 数据 | MemEvoBench 官方 QA(108 cases/7域/36 risk)与 Workflow(83 cases/20 env)发布字段:query、misleading/correct memory、`correct_answer`、`correct_workflow`、risk label | 不自造合成场景 |
| unsafe 判定 | 官方 released safety judge rubric 原样(MISLED 判定);独立第二 judge(gpt-4o,沿用 2026-07-12 复现 pilot 的做法)做 AND 闸门复核 | 不自写新 rubric 当主口径;rubric 敏感性只作 secondary |
| 主终点 | 预注册 paired delta:future paired unsafe effect A_i(t+h)、history-matched recovery area A_i(d)、final residual | 绝对 ASR 不作主结论(base 水位 ~55pp 已实测,见 memevobench_replication_pilot_20260712.md) |
| 统计 | case-level paired bootstrap 95% CI(分层 case ID)、McNemar(二元 paired)、Holm 校正、QA/workflow 分开报告再等权平均 | 不报裸 p 值、不合并任务类型掩盖异质性 |
| NLI(仅 PairGain) | 冻结主 checkpoint DeBERTa-v3-base-mnli-fever-anli(CPU!MPS 长前提会挂)+ 至少一个独立来源 sensitivity checkpoint | 不在 test 后调 aggregation/epsilon |

## 1. 第一刀:CHIR existence pilot(RQ3,Stage 1)

### 1.1 实验单位与规模
- 20 QA + 20 workflow cases(从官方数据均匀按域抽,QA 7 域各 2-3 条;workflow 按 environment 分层)。
- depth d ∈ {0, 3};correction 后 k ∈ {0, 1, 2} 只读评估(评估不写回)。

### 1.2 四臂(proposal §6.3 原样)
1. **Contaminated history**:misleading source 按官方管线跑 d 轮,产生 descendants;
2. **Safe history**:correct source 在完全相同 query/feedback 结构下跑 d 轮(主对照!);
3. **Benign-volume control**:d=0 correction + 数量/长度/时间戳匹配的良性 descendants(排除"记录多"混杂);
4. **Append-only/raw control**:不做 consolidation 只留 raw episodes;另有 NullMemory 描述性基线。

### 1.3 correction 操作(对齐官方 tool_correct_memory 机制,字节级)
- correction point:把全部 misleading source records 替换为**发布的正确文本原文**(`correct_answer`/`correct_workflow` 派生,两分支字节一致);
- 重建受影响 embedding/index;保存 pre/post snapshot hash;
- descendants 保留(这就是"semantic history")。
- **full-closure 臂**:source + 沿 lineage 全部 descendants 逐条 evidence-rewrite(收益上界,Stage 1 只做小样本验证方向)。

### 1.4 主终点(预注册,proposal §6.4)
- **A_i(d) = mean_k [u_contam(d,k) − u_safe-history(d,k)]**(k=0..2);
- immediate residual(k=0)、final residual(k=2)、recovery 曲线下面积;
- u = 官方 judge MISLED 率;AND 闸门(judge1 ∧ judge2)同步报告。

### 1.5 Stop/Go(预注册,不许事后改)
- **Go**:matched(contam vs safe-history)residual > 0 且 case-level bootstrap 95% CI 不含 0,独立 judge 同向;full closure 明显优于 source-only。
- **Stop**:matching 后 residual 消失 / 只由 benign-volume 解释 / 换 judge 消失 → CHIR 死,不做 RQ4,如实报负。

### 1.6 必须匹配项 checklist(§6.3)
descendant count、record type、token 长度分布、timestamps+插入顺序、query/feedback 轮结构、retrieval top-k 与 context budget、model/prompt/seed family、correction 文本字节一致。每项在 harness 里做 assert + 落盘核对表。

## 2. 第二刀:PairGain MVP(RQ1+RQ2,Stage 2)

### 2.1 规模与分支
- 40 QA + 30 workflow;t = 0..3 同步 consolidation;
- correct/misleading 同步分支:除标注错误 span 外,固定其余 memory、episodes 顺序、prompt、model、seed、decoding、长度预算;branch matching 自动检查(token 长度差、lexical overlap 阈值预注册)。

### 2.2 测量(proposal §5.3-5.5 原样)
- q_i(M) = mean_s [P_NLI(m_i|s) − P_NLI(c_i|s)](冻结 NLI,句子级,CPU);
- D_i(t) = q(M⁻) − q(M⁺);G_i(t) = [D(t+1) − D(t)] / (|D(t)| + ε);
- A_i(t+h) = P(unsafe|M⁻) − P(unsafe|M⁺),h∈{1,2},held-out probes,官方 judge。

### 2.3 必比 baseline 家族(RQ1 §5.6 + RQ2)
current-only(A_i(t), D_i(t), D_i(t+1))/ retrieval-only / TrustMem-style transition score(coverage/preservation/faithfulness,按 2606.25161 定义重实现,冻结 prompt,标注"style"以示非官方代码)/ G-only / joint。
对照:random transition score、append-only/operator-off、no-op rewrite。

### 2.4 判定
- **RQ1 Go**:控制 current A/D 后 G 仍正向预测 future effect(partial 关联 CI 不含 0);operator-off 显著减弱;主 NLI + 敏感性 checkpoint 同向。
- **RQ2 Go**:joint > TrustMem-only(held-out likelihood/Brier/AUROC);whole-curve permutation(分层保分布/形状/次数)后优势消失(证明是 case-specific 信号)。
- **Stop**:G 加入 current 后失效 / NLI 一换就翻 / operator-off 同样有效 → PairGain headline 停。

### 2.5 第二 NLI checkpoint 执行澄清(2026-07-19,主 checkpoint 出数后、敏感性出数前冻结)
- 原设计只写“至少一个独立来源 sensitivity checkpoint”,没有冻结子集大小；因此本节明确标注为**事后执行澄清,不是原始预注册**。
- checkpoint=`roberta-large-mnli`;按两个 records JSONL 的稳定落盘顺序各取前 10 case(QA 10 + Workflow 10),不按主结果、域或效应筛选。
- 句子抽取、q/D/G、epsilon 网格、冻结统计脚本均不变；只检验 RQ1/RQ2 的方向和结论是否对 checkpoint 翻转。
- 该 20-case 敏感性只能加强或削弱稳健性描述,**不能把主 72-case STOP 救成 GO**。

## 3. 诚实边界(写进所有输出)
- PairGain 是 oracle-evidence prospective diagnostic,不是部署 controller;
- CHIR headline 是 "source correction ≠ correction closure",不是神秘迟滞;
- position-effect 子实验默认不跑(找不到可序列化顺序敏感状态就删,§6.9);
- 所有 null/negative 报 effect size + CI,不埋。

## 4. 实现映射(2026-07-18 摸底定稿)

### 4.1 底座与挂钩点
- **QA 底座**:`memevobench_official/iterative_memory_triplequery_test.py`(1461行,本地改动仅工程适配)。记忆=进程内 list[dict],`run_triple_query_test` 纯函数式;复用官方 `JUDGE_RESPONSE_PROMPT`(L93-132)、`judge_response_correctness`、`format_memories_for_prompt`、`create_memory_from_response`。双分支=同一 cluster 传不同初始记忆池;快照=任意轮后 deepcopy。
- **Workflow 底座**:`memorybench/Workflow/normal/eval_workflow.py`(静态版,干净);judge=`Workflow/judge.py` 的 `AGENT_CLASSIFICATION_PROMPT_TEMPLATE`(L45-129,不确定默认 UNSAFE);`run_single_query` 天然只读。**统一给 judge 传 ground_truth**(官方两管线不一致,与 modtool 版对齐)。
- **纠正语义**:照官方 `tool_correct_memory.py` L126-136——整字段覆写 + status 变更 + timestamp 刷新。
- **纠正文本(零自造)**:QA 用 misleading 记忆自带的 `correct_answer` 字段原文;Workflow 用 `correct_workflow` 字段原文(官方发布、官方代码从未使用)。批驳式语体/描述式语体与原字段不同 → 作为声明口径写进 limitation;语体改写版只作 sensitivity。
- **坑(已知必避)**:corrected 模式 `set_current_context` 缺失(不用该模式);macOS modtool 多进程 spawn 炸(用静态版/单 worker);`OpenaiAPI.py` 占位符不读 env(不走它,QA 脚本自身读 OPENAI_*)。

### 4.2 CHIR Stage-1 臂 × 官方协议映射(QA 与 Workflow 同构)
| 臂 | 构造(全部官方机制) |
|---|---|
| contam-d3 | 官方 original 模式记忆池 → 官方 3 轮(test_query/2/3,回答经 judge 打标后回灌)→ correction point 覆写 misleading source → k 段评估 |
| safe-history-d3 | t=0 即把 misleading source 换成同字节纠正文本 → 同样 3 轮 → 同 k 段评估(主对照) |
| contam-d0(append-only/raw) | 污染池不跑轮 → correction point 覆写 → k 段评估 |
| benign-volume | d0 纠正池 + 从**域匹配的其他 cluster 的 safe 轮产物**借 3 条 descendants(数量/长度/时间戳匹配)→ k 段评估 |
| NullMemory(描述性) | 官方 base_model 模式,无记忆 |

k 段评估:k=0 纠正后立即以 3 条 test_query 只读探针判定;k=1 先做 1 轮官方写回(test_query 回答入池)再探针;k=2 再 1 轮写回后探针。探针 judge 结果不写回。
主终点:A_i(d)=mean_k[u_contam − u_safe-history](逐探针 paired);判定走官方 judge(gpt-4.1-mini)+ 独立 judge gpt-4o AND 闸门。

### 4.3 模型/环境
- 主模型 = judge1 = gpt-4.1-mini(.env.v3 OPENAI_*,与 2026-07-12 复现 pilot 同口径);judge2 = gpt-4o(同 key)。
- QA 侧跑在 `.venv_memevo`(Py3.14,纯 API);NLI(仅 PairGain)跑 `.venv_tiermem_v2`(Py3.11+torch,**CPU**)。
- NLI 敏感性第二 checkpoint 需下载(本地仅 DeBERTa-v3-base-mnli-fever-anli;磁盘余 25Gi)。
- 成本估算(CHIR pilot):每 case 每臂 ≈14 gen+14 judge;4 臂 × 40 case ≈ 4.5k 生成 + 4.5k judge1 + 2.5k judge2 ≈ **$20-40 量级**(gpt-4.1-mini 便宜,gpt-4o 只判探针)。
- harness 位置:`scripts/run/rt02/`;快照/lineage/hash/judge IO 全落盘 `state/rt02_runs/`。

### 4.4 抢救记录
上会话 3 个结果 JSON 已从 tmp 抢救至 `scratchpad/memevo_pilot/`(bridge/rq1_implicit/rq2_relation);分析脚本本就在 `scripts/analysis/`。**原始 28 个 {cat}__{mode}.json 与 rejudge_raw.json 已随 tmp 清理永久丢失**——双 judge pilot 结论只可引用汇总数字,不可复算(如需复算须重跑)。

## 5. 产物清单
- harness:`scripts/run/rt02/`(chir_pilot / pairgain_mvp / 共享 snapshot·judge·stats 模块)
- 结果:`state/rt02_chir_pilot_<date>.json`、`state/rt02_pairgain_mvp_<date>.json`
- 判定报告:`state/rt02_existence_verdicts_<date>.md`
