# Agent Memory 失败模式与 Debug 手册

这组文档的目标不是总结“memory 可能出错”，而是把最常见、最伤系统、也最容易在大项目里被低估的失败模式拆出来单独讲。

为什么这一组很重要？因为真正的大型 memory 项目，不只是看起来功能多，而是要能回答：

- 这个系统最容易怎么坏？
- 坏了以后你怎么发现？
- 你能不能在系统层定位到原因？
- 你有什么稳定的修复策略，而不是每次临场补洞？

这组材料现在先覆盖 4 个最关键的失败模式：

1. [摘要漂移](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/summary_drift.md)
2. [旧事实覆盖失败](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/stale_fact_override.md)
3. [多跳检索断链](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/multi_hop_breakage.md)
4. [时间推理失败](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_failure_modes/temporal_reasoning_failures.md)

## 建议怎么使用这组材料

### 如果你是读论文

把它当成“方法反向校验表”：

- 这个方法最容易踩哪一类失败？
- 它有没有显式机制避免这个问题？
- 它的 benchmark 是否真的覆盖了这一类失败？

### 如果你是读大仓库

把它当成“代码阅读过滤器”：

- 这个仓库在哪一层处理这个失败模式？
- 是写入期处理、更新期处理，还是回答期补救？
- 它有没有回源机制、版本机制、冲突处理或结构检索来抑制失败？

### 如果你是自己搭系统

把它当成“上线前 checklist”：

- 你要主动设计监控指标；
- 要有最小 debug artifact；
- 要在系统里留下可回溯证据，而不是只看最后答案。

## 一个总原则

长期记忆系统真正难的地方，从来不是“存进去”，而是**系统在很久之后仍然知道自己哪里可能错了**。  
所以这组手册的核心精神是：

> **memory 不是只要会 recall 就行，还要会暴露自己的脆弱点。**
