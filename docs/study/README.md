# Agent Memory Study Hub

这个 `study/` 目录现在不再只是一个小专题，而是一个围绕 **Agent Memory / Long-term Memory for LLM Agents** 逐步搭起来的学习知识库。

它的目标不是替代论文，也不是替代开源仓库本身，而是把三种原本分散的材料整理到一个稳定入口里：

1. **方法框架**
   也就是“信息提取 / 记忆管理 / 记忆存储 / 信息检索 / benchmark / 关键结论”这条统一分析主线。

2. **大型仓库阅读攻略**
   也就是“真正值得 clone 下来研究的完整项目应该怎么读”，重点围绕 `Mem0`、`Letta`、`Graphiti`、`MemoryOS`。

3. **失败模式与工程搭建手册**
   也就是“这些系统最常怎么出错，以及如果我自己做一套应该怎么搭”。

## 目录总览

### 1. 模块化框架资料包

- [agent_memory_modular_framework/README.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/README.md)
- [agent_memory_modular_framework/00_method_and_repo_links.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/00_method_and_repo_links.md)
- [agent_memory_modular_framework/01_information_extraction.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/01_information_extraction.md)
- [agent_memory_modular_framework/02_memory_management.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/02_memory_management.md)
- [agent_memory_modular_framework/03_memory_storage.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/03_memory_storage.md)
- [agent_memory_modular_framework/04_information_retrieval.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/04_information_retrieval.md)
- [agent_memory_modular_framework/05_benchmarks.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/05_benchmarks.md)
- [agent_memory_modular_framework/06_key_conclusions.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/06_key_conclusions.md)

### 2. 大仓库阅读攻略

- [agent_memory_repo_guides/README.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/README.md)
- [agent_memory_repo_guides/mem0_reading_guide.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/mem0_reading_guide.md)
- [agent_memory_repo_guides/letta_reading_guide.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/letta_reading_guide.md)
- [agent_memory_repo_guides/graphiti_reading_guide.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/graphiti_reading_guide.md)
- [agent_memory_repo_guides/memoryos_reading_guide.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/memoryos_reading_guide.md)

### 3. 失败模式与 Debug 手册

- [agent_memory_failure_modes/README.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/README.md)
- [agent_memory_failure_modes/summary_drift.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/summary_drift.md)
- [agent_memory_failure_modes/stale_fact_override.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/stale_fact_override.md)
- [agent_memory_failure_modes/multi_hop_breakage.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/multi_hop_breakage.md)
- [agent_memory_failure_modes/temporal_reasoning_failures.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/temporal_reasoning_failures.md)

### 4. 工程搭建手册

- [agent_memory_building_playbook/README.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/README.md)
- [agent_memory_building_playbook/architecture_blueprint.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/architecture_blueprint.md)
- [agent_memory_building_playbook/memory_schema_design.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/memory_schema_design.md)
- [agent_memory_building_playbook/write_update_pipeline.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/write_update_pipeline.md)
- [agent_memory_building_playbook/retrieval_pipeline.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/retrieval_pipeline.md)
- [agent_memory_building_playbook/deployment_evaluation.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/deployment_evaluation.md)

## 三条阅读路线

### 路线 A：先学框架，再看项目

适合第一次系统了解 Agent Memory 的情况。

1. 先看 `agent_memory_modular_framework/`
2. 再看 `agent_memory_repo_guides/`
3. 最后看 `agent_memory_failure_modes/`

这条路线的优点是：先建立分类框架，后面读大仓库时不容易迷失在目录和文件里。

### 路线 B：先看大仓库，再回头抽象

适合你已经明确想研究完整工程项目。

1. 先看 `mem0_reading_guide.md`
2. 再看 `letta_reading_guide.md`
3. 再看 `graphiti_reading_guide.md`
4. 最后回到模块化框架资料包做抽象

这条路线更像“以 repo 为师”，优点是项目感最强。

### 路线 C：直接准备自己搭系统

适合你已经不只是学习，而是准备真做一套自己的 memory agent。

1. 看 `agent_memory_building_playbook/`
2. 看 `agent_memory_failure_modes/`
3. 只把 `agent_memory_modular_framework/` 当做设计原理参考

## 这个知识库还会继续往哪里长

如果后面继续扩，我建议最自然的增长方向有三个：

1. 增加更多仓库攻略
   例如面向 `LangMem`、`LangGraph memory stack`、`OpenMemory` 等项目的补充阅读。

2. 增加更具体的“文件级阅读地图”
   例如每个大型仓库里具体哪些文件最值得先读。

3. 增加真实项目模板
   比如“个人助理 memory agent 模板”“coding agent memory 模板”“CRM memory agent 模板”。

当前这一版已经不只是零散笔记，而是一个可以不断扩张的知识骨架。

更新时间：2026-06-29
