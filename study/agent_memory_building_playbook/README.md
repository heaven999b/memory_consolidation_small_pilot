# Agent Memory 工程搭建手册

这一组文档服务的是一个更直接的问题：

> 如果不是只做学习总结，而是真的要搭一套自己的 Agent Memory 系统，应该怎么开始？

很多资料都能告诉你 memory 有哪些方法，但真正到落地时，最常见的困难是：

- 不知道系统边界怎么划
- 不知道 schema 该怎么定
- 不知道写入和更新管线怎么组织
- 不知道检索是不是该混合做
- 不知道部署、评测和 debug 怎么收口

所以这组手册不再按“论文方法分类”，而按“工程搭建顺序”来写。

## 当前收录内容

1. [architecture_blueprint.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/architecture_blueprint.md)
2. [memory_schema_design.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/memory_schema_design.md)
3. [write_update_pipeline.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/write_update_pipeline.md)
4. [retrieval_pipeline.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/retrieval_pipeline.md)
5. [deployment_evaluation.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_building_playbook/deployment_evaluation.md)

## 推荐阅读顺序

1. 先看总架构蓝图
2. 再看 schema
3. 再看写入/更新
4. 再看检索
5. 最后看部署和评测

这个顺序基本对应你真正搭系统时的决策顺序。

## 一句核心原则

这组手册的核心原则是：

> **先把 memory 当系统，而不是当功能。**

一旦你这么看，很多原本模糊的问题就会清楚很多。
