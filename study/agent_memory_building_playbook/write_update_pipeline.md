# 写入与更新管线：长期记忆系统真正的主战场

很多人把 memory 系统想成“用户说一句，我写一条”。  
这对长期 agent 来说远远不够。真正成熟的系统必须把写入和更新拆成一条明确管线。

## 一、建议的 6 步写入管线

### 1. Capture

先抓原始事件：

- 用户消息
- 工具结果
- 系统输出
- 外部状态变化

### 2. Extract

抽出可能值得持久化的候选信息：

- 偏好
- 事实
- 项目状态
- 关系

### 3. Match

判断它和已有 memory 是否相关：

- 是新增
- 是补充
- 是覆盖
- 是冲突

### 4. Update

根据判断执行：

- append
- merge
- revise
- supersede

### 5. Index

更新：

- 向量索引
- 词汇索引
- 图结构

### 6. Audit

记录这次写入做了什么变更。

## 二、为什么 update 比 write 更难

因为 write 只解决“记住没”，update 要解决“怎么和旧世界相处”。  
真正的长期系统复杂度主要都出在这一步。

## 三、一句话总结

长期 memory 最重要的不是 `add_memory()`，而是一整条 `capture -> extract -> match -> update -> index -> audit` 管线。
