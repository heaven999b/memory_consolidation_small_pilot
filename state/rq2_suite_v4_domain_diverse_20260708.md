# RQ2 自建版 v4 领域扩充（2026-07-08）

这次不是只把旧的 `18` 题多看几遍，而是把自建版题库继续扩成一套 **42 题、14 个领域** 的正式版本。

## 1. 现在有多少题

- `v3` 旧增量：`18` 题
- `v4 extra` 新增量：`24` 题
- 合计：`42` 个 base facts
- 若按 `free + operational` 两种问法一起跑：`84` 个 probes

## 2. 新增了哪些领域

`v4 extra` 新补了 8 个领域，每个领域 3 题：

- `physiology` / 生理学
- `pharmacology` / 药理学
- `immunology` / 免疫学
- `neuroscience` / 神经科学
- `statistics` / 统计学
- `physics` / 物理学
- `astronomy` / 天文学
- `earth_science` / 地球科学

加上 `v3` 的 6 个领域，现在总共 14 个领域：

- 生物化学
- 分子生物学
- 遗传学
- 临床医学
- 化学
- 微生物学
- 生理学
- 药理学
- 免疫学
- 神经科学
- 统计学
- 物理学
- 天文学
- 地球科学

## 3. 这次解决了什么问题

相比旧版，这次主要解决三件事：

1. **题太少**
   现在不再是十几题的小池子，而是 42 题的正式底座。

2. **领域太单一**
   不再只像生信/医学小题，已经扩到理化统天文地学。

3. **答案形态太单调**
   现在有：
   - 组合答案
   - 映射式答案
   - 概率拆分
   - 阈值 + 单位
   - 公式 / 关系式
   - 代码 / 核型 / 类别记法
   - 普通短语型答案

## 4. 脚本状态

主脚本已经接好：

- [run_rq2_factual_poison.py](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/run_rq2_factual_poison.py)

现在支持：

- `--suite-version v4`
- 学术类题目使用更像“讲义/复习笔记”的错误灌入话术

干跑校验已经通过，结果是：

- `n_base_items = 42`
- `n_probes = 84`

## 5. 可直接查看的页面

- 题库总览页：
  [rq2_suite_v4_catalog_zh.html](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/state/rq2_suite_v4_catalog_zh.html)

- 旧的多样性人工审稿页：
  [rq2_manual_annotation_diverse_zh.html](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/state/rq2_manual_annotation_diverse_zh.html)

注意：

- `rq2_manual_annotation_diverse_zh.html` 还是基于旧实验结果构建，所以目前只能长到 `22` 条。
- 真正看 42 道题库本体质量，请优先看 `rq2_suite_v4_catalog_zh.html`。
