# Letta 阅读攻略

项目地址：
- 论文：[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- GitHub：[letta-ai/letta](https://github.com/letta-ai/letta)

如果说 `Mem0` 最像产品化 memory layer，那 `Letta` 最像一个**带长期记忆的完整 agent runtime**。  
它值得研究，不是因为它只做了 memory，而是因为它在认真回答一个更大的问题：

> 如果 agent 不是一次性聊天，而是持续运行、可调用工具、可持久化状态、可跨多轮交互，那么 memory 应该处在系统的哪一层？

这其实是 `MemGPT` 那条路线最有价值的地方。它不是把 memory 视为“多存点上下文”，而是把 memory、上下文窗口、工具使用、状态持久化放在同一个运行时视角里。

## 一、先用一句话理解 Letta

`Letta` 可以理解成：**一个把长期记忆纳入 agent 运行时核心机制的 stateful agent platform。**

和很多“带记忆的聊天机器人”不同，它不只是给 agent 多加一个 RAG 后端，而更像在说：

- agent 有自己的状态；
- 状态需要持久化；
- 记忆不是外挂，而是 runtime 资源；
- 记忆使用和工具使用一样，是系统调度的一部分。

## 二、打开仓库后应该先看哪里

当前比较值得优先关注的目录通常包括：

- `letta/`
- `db/`
- `alembic/`
- `sandbox/`
- `tests/`
- `compose.yaml` 或等价本地栈配置

### 1. `letta/`：主运行时核心

这是整个项目最核心的地方。  
你应该在这里理解：

- agent object 是怎么定义的；
- 消息、上下文、memory 状态怎么被组织；
- tool use、memory read、memory write 在 runtime 里如何交错；
- agent 的执行循环有没有显式状态机特征。

如果 `Mem0` 的重点是“memory layer 本身”，那 `Letta` 的重点更像“memory 在 agent system 中如何成为 first-class runtime object”。

### 2. `db/` 和 `alembic/`：状态持久化不是附属问题

`Letta` 很值得学的一点，是它会逼你正视长期 agent 系统最现实的问题：**持久化状态到底怎么落。**

很多 demo 都会把“记忆”说得很漂亮，但真正的长期系统一定绕不开：

- memory object 怎么存；
- agent state 怎么存；
- 用户 / workspace / session 怎么隔离；
- schema 怎么演化；
- 版本升级后旧状态怎么迁移。

所以 `db/` 和 `alembic/` 不是配角，而是理解 Letta 成熟度的重要窗口。

### 3. `sandbox/`：长期 memory 不能脱离动作环境理解

这部分很关键。  
长期记忆系统一旦进入 agent 场景，就不只是“会不会回答”，而是“记忆如何影响行动”。  
`sandbox/` 这类目录存在，本身就说明项目在认真处理：

- 工具调用边界；
- 环境隔离；
- memory-conditioned action；
- agent 行为的可控性与安全性。

这和纯 chat memory 项目非常不一样。你要读懂 Letta，就必须接受：它不是 memory library，而是 memory-aware agent runtime。

### 4. `tests/`：系统工程视角的关键证据

读 `Letta` 一定要看 tests。  
原因很简单：这类项目复杂度极高，不看测试你很难判断哪些行为是项目真正想保证的，哪些只是当前实现碰巧如此。

对长期 memory 系统来说，测试特别能透露两个东西：

1. 作者最担心什么 regression
2. 系统真正稳定承诺了哪些能力

## 三、一个高效的阅读顺序

建议的第一轮阅读顺序：

1. 根 README 和 quickstart
2. `letta/` 主运行时入口
3. agent / message / state 相关模块
4. memory 读写在 runtime 中的位置
5. `db/` + `alembic/`
6. `sandbox/`
7. `tests/`

这个顺序的逻辑是：先理解它是个什么系统，再理解 memory 在系统里扮演什么角色。

如果你上来先盯着具体 memory 实现细节，反而会错过 Letta 最有价值的地方：  
**它是把 memory 做进 runtime，而不是把 runtime 建在 memory 外面。**

## 四、读 Letta 时最值得学的 5 件事

### 1. 记忆是系统资源，不只是数据

这是 Letta 最大的不同。  
很多项目把 memory 看成数据层，而 Letta 更像把它看成 runtime resource，类似：

- 上下文窗口预算；
- agent 可访问状态；
- 工具调用前后的条件资源；
- 长期 state 的一部分。

### 2. memory 和 tool use 是同一个 execution loop 里的事

这非常重要。  
在长期 agent 系统里，记忆不是回答前“先查一下库”那么简单，而是：

- 查到的记忆会影响是否调用工具；
- 工具执行结果会反过来更新记忆；
- 新记忆会改变后续规划和行动。

也就是说，memory 和 action 是互相缠绕的。

### 3. 持久化层是理解长期 agent 的必修课

如果你未来自己做系统，Letta 会逼你正视最现实的一层：  
没有持久化、迁移、状态隔离，就没有真正的长期 agent。

这也是为什么研究 Letta，不能只停留在 memory 算法，而必须把 DB、schema 和 state lifecycle 一起看。

### 4. 它代表的是“平台式思维”

`Letta` 和很多 research repo 的差别在于，它不是只讲一个方法，而是在尝试提供一个平台。  
平台思维意味着：

- 多种 agent；
- 多种工具；
- 多种持久化状态；
- 多种部署方式；
- 对外接口与生态接入。

这对你理解“工业级项目感”很有帮助。

### 5. 它特别适合学系统边界

如果 `Mem0` 适合学 memory layer 本身，`Letta` 特别适合学**系统边界**：

- memory 属于哪一层；
- agent loop 怎么组织；
- 哪些状态应该持久化；
- 外部工具怎样进入执行面。

## 五、不要误读 Letta 的地方

第一，不要把 Letta 只看成“MemGPT 的代码升级版”。  
它已经明显超出单篇论文复现的范围，更像一个独立 agent platform。

第二，不要只从 memory algorithm 角度评价它。  
它真正的价值是在 runtime 设计，而不是某一个提取或检索技巧。

第三，也不要指望从 Letta 学到最细致的图记忆结构。  
如果你要研究强关系和时间图谱，还是应该补 `Graphiti`。

## 六、最适合谁读

`Letta` 最适合：

1. 想做 stateful agent platform 的人
2. 想理解长期记忆如何进入 agent runtime 的人
3. 想研究 memory 与 tool/action loop 结合方式的人

## 七、最后一句总结

如果让我用一句话概括 `Letta` 的学习价值，我会写：

> **它让你看到，长期记忆不是单独一层插件，而可以成为 agent 运行时本体的一部分。**

这就是 Letta 最值得研究的地方。
