# 搭建蓝图：一套稳妥的 Agent Memory 总架构

如果你准备自己搭一套长期 memory agent，最容易犯的错是：上来先选向量库、先选 graph DB、先写 embedding pipeline。  
但这些都不是第一步。第一步应该是先把总架构想清楚：**memory 在整个 agent 系统里到底处在哪一层。**

我建议用下面这张脑图来理解：

1. 交互输入层
2. memory write / update 层
3. memory storage 层
4. retrieval / routing 层
5. answer / action 层
6. audit / evaluation 层

## 一、最稳妥的分层架构

一个适合作为第一版的架构通常包含下面 5 个存储对象：

### 1. Raw episodes

保存原始交互、原始事件、原始工具结果。  
这层的目标只有一个：保住证据。

### 2. Summary memories

保存压缩后的稳定摘要、偏好摘要、项目状态摘要。  
这层的目标是减负，而不是替代 raw。

### 3. Structured facts

保存显式字段，如：

- 当前 owner
- 当前 deadline
- 当前偏好
- entity relation

### 4. Retrieval index

向量索引、词汇索引或图索引。  
这是 retrieval service 的底座，不是 memory 本体的全部。

### 5. Audit artifacts

保存：

- 哪些 memory 被写了
- 哪些 memory 被改了
- 回答时用了哪些 memory
- 哪些冲突被检测到

这层对后期 debug 极其重要。

## 二、为什么这个蓝图稳

因为它把几类容易混在一起的东西分开了：

- 原始证据 vs 派生摘要
- 当前状态 vs 历史事件
- memory object vs retrieval index
- 业务逻辑 vs debug 证据

一旦这些东西混在一起，系统后面几乎必然越来越乱。

## 三、第一版不要做什么

第一版最不建议一上来就做：

- 全图系统
- 全树系统
- 只依赖摘要不保 raw
- 只看最终答案不存中间 trace

更稳的路线是：

1. 先 raw + summary + current facts
2. 先把 update 和 retrieval 做稳
3. 等多跳和时间问题成为真实瓶颈，再加图或树

## 四、一句话总结

好的 memory 架构不是“多加一个数据库”，而是让证据、摘要、状态、检索和审计各自有位子。  
这才是一套长期系统能长大的前提。
