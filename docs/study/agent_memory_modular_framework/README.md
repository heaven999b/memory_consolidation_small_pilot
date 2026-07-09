# Agent Memory 模块化框架学习资料包

这套资料包是从 [AGENT_MEMORY_METHOD_SUMMARY.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/AGENT_MEMORY_METHOD_SUMMARY.md) 继续向下展开出来的“深读版”。  
如果你想看当前整个知识库的总入口，而不只看这一组材料，请先看 [study/README.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/README.md)。

它的目标不是再做一遍泛泛综述，而是把原来那份总文档里的 6 个核心点，拆成可以单独学习、单独复习、单独引用的独立材料。你可以把它理解成一个面向个人研究的内部学习目录：

1. 先用总索引掌握全局。
2. 再看方法与仓库链接表，知道每种方法、论文和 GitHub 在哪。
3. 最后按 `信息提取 -> 记忆管理 -> 记忆存储 -> 信息检索 -> benchmark -> 关键结论` 的顺序深入。

这套资料包的核心出发点是：**Agent Memory 不是一个单一算法，而是一整套信息生命周期系统。**  
如果不把它拆成模块，你很容易把很多本来不同层面的东西混在一起，例如：

- 把“摘要写入”误当成“长期记忆架构”；
- 把“图检索”误当成“图存储”；
- 把“分层存储”误当成“更新策略”；
- 把“回答阶段的 LLM 推理能力”误当成“记忆系统本身的能力”。

所以这套材料坚持一个原则：**每次只讲清一个层面，并且不断回到具体方法和具体仓库。**

## 阅读顺序

如果你第一次读，建议按这个顺序走：

1. [00_method_and_repo_links.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/00_method_and_repo_links.md)
2. [01_information_extraction.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/01_information_extraction.md)
3. [02_memory_management.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/02_memory_management.md)
4. [03_memory_storage.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/03_memory_storage.md)
5. [04_information_retrieval.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/04_information_retrieval.md)
6. [05_benchmarks.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/05_benchmarks.md)
7. [06_key_conclusions.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/06_key_conclusions.md)

如果你现在的目标更偏工程实现，而不是论文框架，那建议这样跳读：

1. 先看 [00_method_and_repo_links.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/00_method_and_repo_links.md)，确认哪些是真正完整的大仓库。
2. 再看 [02_memory_management.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/02_memory_management.md) 和 [03_memory_storage.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/03_memory_storage.md)，因为工程差异主要出在这两层。
3. 最后看 [06_key_conclusions.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/study/agent_memory_modular_framework/06_key_conclusions.md)，把论文结论转成自己的设计原则。

## 这一包资料和原总文档的关系

原来的 [AGENT_MEMORY_METHOD_SUMMARY.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/AGENT_MEMORY_METHOD_SUMMARY.md) 仍然是“总览版”。  
它更像一篇浓缩 memo，适合快速回顾：

- 哪 10 种方法被统一框架放在一起比较；
- 论文的四大组件怎么拆；
- benchmark 和关键结论是什么；
- 哪些大仓库值得重点研究。

而当前这个 `study/agent_memory_modular_framework/` 目录，则更像“展开讲义”：

- 每个核心点单独成篇；
- 每篇都尽量把概念、方法、例子、工程含义讲透；
- 所有公开论文和 GitHub 链接被集中到一个索引文件里；
- 对没有成熟公开仓库的方法，也会明确标记出来。

## 这套资料包特别适合哪三种用途

第一种用途是“做文献学习卡”。  
你可以把这 6 篇当成 6 张专题卡片：提取、管理、存储、检索、评测、结论。后面无论看新论文还是看新项目，都可以快速判断它主要创新在哪一层。

第二种用途是“做项目设计前的认知校准”。  
很多人一上来就想做 memory agent，但经常把“加一个向量库”误当成长记忆系统。这套材料会反复提醒你，真正难的地方不只是存储，而是更新、迁移、关联和冲突处理。

第三种用途是“给大仓库建立阅读路线”。  
你如果之后真的去读 Letta、Mem0、Graphiti、MemoryOS 这种仓库，最好先有模块化框架。否则看几十个目录时会只剩“这个 repo 很大”，而不知道每个模块到底在解决哪一类记忆问题。

## 最后一个提醒

这套资料包虽然写得更详细，但它依然有明确边界：

- 它主要服务于“长期对话 / 长期交互 / agent stateful memory”。
- 它不是一份通用 continual learning 教程。
- 它也不是参数记忆、训练时记忆、KV cache 优化的系统综述。

如果你后面要进一步扩展，我建议最自然的后续材料会是两种：

1. “Agent Memory 开源仓库阅读攻略”
2. “Agent Memory 常见失败模式与 debug checklist”

这两份会和当前资料包形成很好的互补。

更新时间：2026-06-29
