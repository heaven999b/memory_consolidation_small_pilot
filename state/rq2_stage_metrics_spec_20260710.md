# RQ2 stage 指标判定规格(0A)—— 确定性、零付费 judge

**2026-07-10 | 基于 provenance 勘察 + 相关工作(NLI attribution + summary-drift)**

> 目标:让 UNMR / conflict / PAR + 漂移 四个 stage 指标**确定性、可复现、不调付费 LLM judge** 地落盘。躲开 RQ2 最痛的 judge 方差,同时用 NLI+overlap(测捏造)+ 高风险句式(测漂移)覆盖"固化制造假记忆"的两种形态。

---

## 1. 数据源(勘察结论)

**主源 = `outputs/**/page_store/*.json`(富回指)**:每页含
- `content`:累积**原始全文**(NLI 的原文侧 / premise)。
- `memories`:固化后 compact memory(≈`summary`,hypothesis 侧)。
- `summary`:固化 note(逐 pass 覆写)。
- `raw_log_ids`:回指 raw turn。

**辅源 = `*_qa.jsonl`**:`mechanism_trace.hits_summary[*].page_id` → 回指 page_store content(做 PAR)。

回指粒度:**page 级可追**(memory→page→content),句级不可追(固化是整页 LLM 改写)——所以判定用**页级配对**(记忆句 vs 同页 content),这是可接受的确定性近似。全程不碰 write.jsonl、不调付费 LLM。

---

## 2. 四个判定(都确定性)

### ① UNMR —— support / 捏造(NLI)
- 对每页每条 `memories[i]`,用**本地 NLI 模型**判它是否被同页 `content` entail(premise=content,hypothesis=memory)。
- `has_source_support = (entail_prob ≥ τ)`;`UNMR(N) = 第 N pass 新建 memory 中 unsupported 比例`。
- 对应 FActScore / AttrScore 的 NLI-attribution 路线,可复现、零付费。

### ② 漂移 —— fidelity / over-generalization(UNMR 的盲区补充)
- **为什么单独做**:丢限定词的弱化记忆(如"少量喝牛奶,优先燕麦奶"→"可以喝牛奶")**仍被原文 entail**,UNMR 放过它,但它已失真。
- 判定:`content` vs `summary` 比**高风险句式 / 时间限定 / 例外条件是否丢失**。
- `drift = 原文含高风险限定词、但固化后丢失`。确定性(词表匹配;可选加 NLI 判"summary 是否严格比 content 更宽泛=content⊨summary 但 summary⊭content")。
- **高风险句式表**(from summary_drift.md):`但 / 除非 / 最近 / 暂时 / 默认 / 优先 / only / except / currently / temporarily` + 时间词(日期 / 之前 / 现在 / 曾) + 数量限定(少量 / 部分 / 大约)。

### ③ PAR —— 传播到答案
- `qa.jsonl` 的 `hits_summary[*].page_id` → 找到被引用的 memory;若该 memory 在 ① 中判为 unsupported,则 `used_unsupported_memory = True`。
- `PAR(N) = 答案引用了 unsupported memory 的比例`。这是"错误从固化层传播到答案"的直接度量。

### ④ conflict-merge
- **用 HaluMem gold 判,不依赖 TierMem 内部 UPDATE 旧文本**(那在 online smart_backfill 线、不落盘)。
- 对 `is_update==True` 的 gold memory_point:固化后系统记忆的值 vs gold 更新后的值。`merged_incorrectly = 不一致 or 丢信息`。

---

## 3. 数据契约映射(→ `rq2_stage_metrics.stage_metrics_by_pass`)

| 契约字段 | 判定来源 |
|---|---|
| `is_new` | pass≥1 新建的固化句(精确版=与 pass0 content 句集比对新增) |
| `has_source_support` | ① NLI entail_prob ≥ τ |
| `is_contradictory` / `merged_incorrectly` | ④ HaluMem gold is_update 前后对 |
| `used_unsupported_memory` | ③ hit page_id 回指、被引 memory 是否 unsupported |
| (新增)`drift` | ② 高风险句式丢失 |

---

## 4. 要你拍板的三个决策

1. **本地 NLI 选型**:
   - `DeBERTa-v3-large-MNLI`(准、慢、~1.5GB)—— 推荐,判 entail 质量高;
   - `nli-deberta-v3-base` / `roberta-large-mnli`(快、略弱)。
   - 都是 HuggingFace 离线 checkpoint,一次下载后**纯本地推理、零 API**。
2. **漂移要不要随 N 曲线**:
   - 要 → 需上游**最小改动**:`run_consolidation_passes`(linked_view_system.py ~1253)每 pass 把 note 存进 `page.consolidation_history[]`(否则中间 pass summary 被覆写、只能看"最终 vs 原文");
   - 不要 → 只做"最终固化记忆 vs 原文"的漂移,不改上游。
   - **建议要**——RQ2 的核心就是"随 N 恶化",漂移曲线正是命脉之一。
3. **entail 阈值 τ**(预注册,如 0.5)+ 是否加 overlap 双通道(NLI ∧ evidence 子串)做客观锚。

---

## 5. 上游最小改动(仅决策 2 选"要"时)

`tiermem_upstream/src/memory/linked_view_system.py` 的 `run_consolidation_passes`(~1253):每 pass 生成 note 后 append 到 `page.consolidation_history`(纯旁路记录,不改 mem0/index/数据流)。Page dataclass(page_store.py:44-55)加一个 `consolidation_history: list = field(default_factory=list)` 字段。

---

## 6. 落地顺序(拍板后)

1. 选 NLI + 定 τ → 写 `scripts/core/rq2_stage_extract.py`(吃 page_store JSON,产三类 record + drift,喂 `stage_metrics_by_pass`)。**离线**。
2. (若决策 2=要)上游加 `consolidation_history` 旁路。**改上游**。
3. 冒烟:在一个已有小 run 的 page_store JSON 上跑 extract,确认三桶非空、UNMR/PAR/drift 有值、CI 合理。**离线(复用旧 run)**。
