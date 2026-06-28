# Memory Schema 设计：长期记忆对象到底该怎么建模

做 memory system 时，schema 设计比很多人想象中更重要。  
因为 schema 决定的不是“数据库长什么样”，而是系统后面有没有能力：

- 表示当前状态
- 表示历史变化
- 表示来源
- 表示关系
- 表示不确定性

## 一、最小 schema 应该包含哪些对象

我建议最少有下面 4 类对象：

### 1. Episode

表示原始交互或原始事件。  
字段至少包括：

- `episode_id`
- `timestamp`
- `source_type`
- `raw_content`
- `workspace_id`
- `user_id`

### 2. Memory object

表示派生出来的长期可复用记忆。  
字段建议包括：

- `memory_id`
- `memory_type`
- `content`
- `confidence`
- `stability_level`
- `source_episode_ids`
- `created_at`
- `updated_at`

### 3. Current fact

表示当前有效状态。  
字段建议包括：

- `entity_id`
- `field_name`
- `current_value`
- `valid_from`
- `source_memory_id`
- `version`

### 4. Relation

表示对象之间的结构关系。  
字段建议包括：

- `from_id`
- `to_id`
- `relation_type`
- `valid_from`
- `valid_to`

## 二、为什么要把 current facts 单独拎出来

因为只存历史事件是不够的。  
用户很多时候问的是“现在是什么”，而不是“历史上发生过什么”。  
如果每次都要从所有历史重新推当前值，系统会越来越脆。

所以最稳的做法是：

- 历史事件保留
- 当前状态单独维护

## 三、schema 里一定要有的三个字段

### 1. source / provenance

没有来源，你就没法 debug。

### 2. version / supersedes

没有版本关系，你就没法优雅处理旧事实覆盖失败。

### 3. stability / confidence

没有稳定性等级，系统很容易把一次临时观察误升成长期事实。

## 四、一句话总结

memory schema 不是“把文本存进去”，而是给长期状态演化留出表达空间。  
如果 schema 只适合静态文本，后面几乎所有高级能力都会难做。
