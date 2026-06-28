# 检索管线：不要把 recall 设计成 top-k 抽奖

一个成熟的 memory agent，不应该把 retrieval 设计成“query 来了，去向量库取 top-k”。  
更稳的做法是显式做 retrieval pipeline。

## 一、建议的 5 步检索管线

### 1. Query parse

先判断这是：

- 当前状态问题
- 历史问题
- 多跳问题
- 时间问题

### 2. Route

决定优先查：

- current facts
- summary memories
- graph relations
- raw episodes

### 3. Retrieve

执行：

- lexical retrieval
- vector retrieval
- graph expansion

### 4. Validate

如有冲突或高风险，回原始证据。

### 5. Compose

把最终候选交给回答层组织输出。

## 二、为什么 route 很关键

因为不同问题最该查的层不一样。  
如果你每次都在同一 memory pool 做 top-k，相当于默认所有问题都一个样。

## 三、一句话总结

检索系统成熟与否，看的不是召回了多少，而是**有没有先判断应该查哪里、怎么查、何时回源。**
