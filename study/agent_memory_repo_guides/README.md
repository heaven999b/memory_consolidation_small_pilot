# 大型仓库阅读攻略

这一组文档只做一件事：**把“大型 Agent Memory 仓库到底该怎么读”讲清楚。**

为什么需要单独开这一组？因为真正的完整仓库和论文阅读是两回事。  
论文能告诉你方法主线，但面对一个几千到上万行代码、带 server、DB、tests、integrations、deployment 的仓库时，最容易出现两个问题：

1. 你知道它很大，但不知道应该先看哪。
2. 你能看懂某个函数，却不知道它在整个 memory architecture 里起什么作用。

所以这组攻略的目标，不是给出逐行代码解释，而是给出一套**阅读路线图**。

## 当前收录的 4 个重点项目

1. [Mem0 阅读攻略](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/mem0_reading_guide.md)
2. [Letta 阅读攻略](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/letta_reading_guide.md)
3. [Graphiti 阅读攻略](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/graphiti_reading_guide.md)
4. [MemoryOS 阅读攻略](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_repo_guides/memoryos_reading_guide.md)

这四个项目被放进来，不是因为它们刚好都很火，而是因为它们在“工业级完整项目”这个维度上，分别代表了 4 种不同的 memory engineering 路线：

- `Mem0`：产品化 memory layer
- `Letta`：stateful agent runtime
- `Graphiti`：temporal graph memory engine
- `MemoryOS`：论文驱动的分层记忆框架

## 建议阅读顺序

如果你只准备认真啃两个仓库，我建议优先：

1. `Mem0`
2. `Letta`

因为这两个最容易帮你建立“一个长期 memory system 真正在工程里需要什么”的直觉。

如果你第三个要补结构化关系和时间事实，再去看：

3. `Graphiti`

如果你第四个想看论文方法怎样走向 package / MCP / playground，再看：

4. `MemoryOS`

## 每篇攻略会回答什么

每篇攻略都尽量回答下面这些问题：

1. 这个仓库在 Agent Memory 生态里扮演什么角色？
2. 它更像方法实现、平台底座，还是产品层？
3. 应该先看哪些目录？
4. 哪些目录是“理解 memory 逻辑”的关键，不是配套基础设施？
5. 如果只花 2 小时，最值的阅读路线是什么？
6. 这个项目最值得学的设计思想是什么？
7. 它不适合拿来学什么？

这样你后面不管是自己读 repo、做笔记，还是拿它们做对比，都更容易进入“结构化学习”状态。
