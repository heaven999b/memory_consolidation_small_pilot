# Week 2 汇报

主报告:[week2_report_20260713_zh.md](week2_report_20260713_zh.md)

## 内容骨架
- §0–6 原始 RQ1/RQ2 小样本判定 + 根因消融(固化对安全信息保真的负结论)
- §7 MemEvoBench 复现 + 批判性再评估(90% ASR headline 里 ~55pt 是基线水位;真记忆净效应 +30pt,judge-robust)
- §8 桥实验(投毒记忆 → 固化 → ASR:不放大)
- §9 RQ1/RQ2 全面复测(去伪影 + 换强检测器 + 隐式风险门):四条独立证据均确认固化保真到略微保护性
- §10 新研究构思:ConsolidationBench —— 把记忆漂移归因到固化算子本身(Δ_op = 活固化 − 冻结写入)

## 支撑材料(在仓库 `state/` 与 `scripts/analysis/`)
- MemEvoBench 复现详版:`state/memevobench_replication_pilot_20260712.md`
- RQ1/RQ2 修复方案:`state/rq1_rq2_fix_masterplan_20260712.md`
- RQ1 隐式风险物料:`state/rq1_implicit_materials_20260712.md`
- ConsolidationBench 构思文档:`state/consolidationbench_idea_{zh,en}_20260713.md`
- 分析脚本:`scripts/analysis/{rq2_stage_verdict_fixed,bridge_consolidate_asr,rq2_gpt4o_relation_sweep,rq1_implicit_sweep,aggregate,rejudge}.py`
