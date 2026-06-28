# 方法、论文与 GitHub 链接总表

这份索引的作用很直接：把当前资料包涉及到的代表方法、论文地址、项目地址和 GitHub 链接统一收口，避免后面读到一半又回头翻。

需要先强调一件事：**论文方法和公开工程实现并不是一一对应的。**  
有些方法论文很经典，但没有成熟、持续维护的公开仓库；有些方法最初是论文方法，后来演化成了更大的产品化项目；还有一些则本来就是产品或平台驱动，再反过来写成论文。

因此，这张表里我会分三类状态：

- `完整公开仓库`：适合真正 clone 下来做工程阅读。
- `研究仓库`：适合看方法机制，但不适合作为生产级架构范本。
- `未明确定位到官方仓库`：说明至少在这轮整理里，没有找到清晰、稳定、官方归属明确的公开实现。

## 一、10 种代表方法总表

| 方法 | 论文 / 项目地址 | GitHub / 代码地址 | 当前状态 | 备注 |
| --- | --- | --- | --- | --- |
| `A-MEM` | [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110) | [agiresearch/A-mem](https://github.com/agiresearch/A-mem), [WujiangXu/AgenticMemory](https://github.com/WujiangXu/AgenticMemory) | 研究仓库 | 前者更像系统实现，后者更偏论文复现实验 |
| `MemoryBank` | [MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://arxiv.org/abs/2305.10250) | 本轮未明确定位到官方、持续维护的公开仓库 | 论文为主 | 经典方法，常通过 SiliconFriend 语境被引用 |
| `MemGPT` | [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) | [letta-ai/letta](https://github.com/letta-ai/letta) | 完整公开仓库 | 原 `cpacker/MemGPT` 已并入 Letta 体系，当前官方主线是 Letta |
| `Mem0` | [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413) | [mem0ai/mem0](https://github.com/mem0ai/mem0) | 完整公开仓库 | 当前最值得研究的产品化 memory layer 之一 |
| `Mem0g` | 同 `Mem0` 论文，图记忆是其中增强变体 | 公开主仓库仍以 [mem0ai/mem0](https://github.com/mem0ai/mem0) 为主 | 完整公开仓库，但 graph 不是独立 repo | 更适合作为 Mem0 的 graph variant 来理解 |
| `MemoChat` | [MemoChat: Tuning LLMs to Use Memos for Consistent Long-Range Open-Domain Conversation](https://arxiv.org/abs/2308.08239) | [LuJunru/MemoChat](https://github.com/LuJunru/MemoChat) | 研究仓库 | 更偏训练与实验 pipeline，不是工业级平台 |
| `Zep` | [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956) | [getzep/graphiti](https://github.com/getzep/graphiti), [getzep/zep](https://github.com/getzep/zep) | 完整公开仓库 + 集成仓库 | `Graphiti` 是图记忆内核，`zep` 更偏 examples 和 integrations |
| `MemTree` | [From Isolated Conversations to Hierarchical Schemas: Dynamic Tree Memory Representation for LLMs](https://arxiv.org/abs/2410.14052) | 本轮未明确定位到成熟官方仓库 | 论文为主 | 结构思想很重要，但没有看到 Letta / Mem0 级别的完整 OSS |
| `MemoryOS` | [Memory OS of AI Agent](https://arxiv.org/abs/2506.06326) | [BAI-LAB/MemoryOS](https://github.com/BAI-LAB/MemoryOS) | 完整公开仓库 | 当前最像“论文方法走向框架化”的项目 |
| `MemOS` | [MemOS: A Memory OS for AI System](https://arxiv.org/abs/2507.03724) | 本轮未明确定位到官方成熟 GitHub 仓库 | 论文为主 | 更宏观，覆盖 plaintext / activation / parameter memory |

## 二、两类 benchmark 的链接

| 基准 | 论文地址 | GitHub / 数据公开情况 | 备注 |
| --- | --- | --- | --- |
| `LoCoMo` | [Evaluating Very Long-Term Conversational Memory of LLM Agents](https://arxiv.org/abs/2402.17753) | 本轮未明确定位到官方 GitHub 主仓库 | 更偏“人类-人类长程对话” |
| `LongMemEval` | [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813) | 本轮未明确定位到官方 GitHub 主仓库 | 更偏“用户-AI 长期交互” |

## 三、如果只想看完整大仓库，优先级怎么排

如果你现在的目标是“研究完整工业级项目，而不是看研究原型”，那我建议优先级直接按下面这个顺序：

1. [mem0ai/mem0](https://github.com/mem0ai/mem0)
2. [letta-ai/letta](https://github.com/letta-ai/letta)
3. [getzep/graphiti](https://github.com/getzep/graphiti)
4. [BAI-LAB/MemoryOS](https://github.com/BAI-LAB/MemoryOS)

理由很简单：

- `Mem0` 最像独立产品层，可以学 memory layer 自己怎样落地。
- `Letta` 最像完整 agent runtime，可以学“memory + agent + tool + persistence”是怎样整合的。
- `Graphiti` 最像图记忆引擎，可以学 temporal graph memory 怎样做。
- `MemoryOS` 最像论文架构走向工程化框架，可以学分层 memory 系统怎样从 paper 变成 package / MCP / playground。

## 四、读这些链接时要注意什么

第一，要分清“论文方法”和“当前官方主线代码”。  
例如 `MemGPT` 的方法论来自论文，但今天真正值得研究的主线仓库是 Letta，而不是只停留在老的论文仓库名义上。

第二，要分清“引擎内核”和“集成层”。  
例如 `Zep` 这一组里，`Graphiti` 更像内核引擎，`zep` repo 更像产品配套与接入示例。你要研究时间知识图该看前者，要研究和外部框架接法则更多看后者。

第三，要接受一个现实：**有些重要方法就是没有成熟公开工程仓库。**  
这时候正确做法不是强行找一个“看起来像”的 repo，而是转去看“方法精神最接近、但工程上更完整”的替代项目。

## 五、按学习目标给一个快捷入口

如果你想学“摘要写入 + 持久化 + 检索层”：

- 先看 `Mem0`
- 再看 [01_information_extraction.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/01_information_extraction.md)
- 再看 [04_information_retrieval.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/04_information_retrieval.md)

如果你想学“层级 memory runtime”：

- 先看 `Letta`
- 再看 `MemoryOS`
- 再看 [02_memory_management.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/02_memory_management.md)
- 再看 [03_memory_storage.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/03_memory_storage.md)

如果你想学“图记忆和关系检索”：

- 先看 `Graphiti`
- 再看 `Zep` 论文
- 再看 [04_information_retrieval.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/04_information_retrieval.md)

这张索引本身不负责把方法讲透，它负责让你不迷路。真正的展开讲解，见后面的 6 篇主题文档。
