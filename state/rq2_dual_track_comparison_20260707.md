# RQ2 双路线对照（官方版 vs 自建版）

日期：2026-07-07

这份说明只做一件事：

> 把 `RQ2` 的 **官方版** 和 **自建版** 彻底拆开，后面汇报不再混说。

---

## 1. 一眼版

| 路线 | 实际数据源 | 现在结果 | 能不能支持原始 RQ2 |
| --- | --- | --- | --- |
| 官方版 | 官方 `HaluMem` 数据切片 | 目前偏负面，而且样本少 | **不支持** |
| 自建版 | 自建 factual poison 套件 | 已有很强的重复带偏信号 | **支持“会造错信”**，但不是官方 benchmark 证据 |

最短人话：

- **官方版** 现在的答案是：没看到“固化把幻觉越搞越大”，而且样本不够，不能硬说正反。
- **自建版** 现在的答案是：只要错误说法反复出现，模型确实会越来越相信它；但进入 TierMem 以后，不同家族变化不一样。

---

## 2. 官方版到底是什么

官方版这里我只认这条口径：

- 来源是官方 `HaluMem` 数据
- 本仓库里用的是从官方数据切出来的固定切片
- 所以它是 **benchmark-grounded**
- 但它 **不是** “官方 wrapper 全量 benchmark 原封不动跑完整套”

对应文件：

- 官方数据： [HaluMem-Medium.jsonl](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl)
- 来源登记： [SOURCE_MANIFEST.json](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/benchmarks/halumem/SOURCE_MANIFEST.json)
- 官方线统计： [e1_hallucination_stats_20260703_014542.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/stats/e1_hallucination_stats_20260703_014542.md)
- 官方线统计： [e1_hallucination_stats_20260703_015934.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/stats/e1_hallucination_stats_20260703_015934.md)

### 官方版现在的结果

| 子线 | 样本量 | 关键结果 | 支持不支持 |
| --- | ---: | --- | --- |
| 单 session 深度扫 | `n=15` | `UF_on_unknown` 从 `0.333` 降到 `0.167` | 不支持 |
| 3-session 版 | `n=45` | `UF_on_unknown` 从 `0.333` 降到 `0.083` | 不支持 |

### 官方版现在最诚实的结论

> 在官方 `HaluMem` 数据切片上，没有看到原始 `RQ2` 设想的“固化放大幻觉”。
> 方向甚至更像“固化后乱编变少一点”，但因为样本太小、检验都不过，所以现在只能说 **没有观察到放大效应**，不能说“已经证明会降低幻觉”。

### 官方版可信度

| 维度 | 评价 | 原因 |
| --- | --- | --- |
| 数据口径 | 较高 | 用的是官方数据 |
| 样本量 | 偏低 | 只有 `15` 和 `45` 这两个量级 |
| 结论强度 | 低 | 方向有，但统计不站住 |
| 适合对外说吗 | 可以，但只能保守说 | 只能说“没看到支持 RQ2 的证据” |

---

## 3. 自建版到底是什么

自建版这里我只认这条口径：

- 完全不是官方 benchmark
- 是自己造的 factual poison 套件
- 它测的是：
  - 错误团队说法反复出现，会不会把模型带偏
  - 带偏后进 TierMem，会不会在不同家族出现不同轨迹

对应文件：

- 主脚本： [run_rq2_factual_poison.py](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/run_rq2_factual_poison.py)
- 固定协议： [rq2_selfbuilt_protocol_20260707.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/state/rq2_selfbuilt_protocol_20260707.md)
- 重评分汇总包： [rq2_selfbuilt_packet_20260707_rescored.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/state/rq2_selfbuilt_packet_20260707_rescored.md)

### 自建版现在的结果

#### 3.1 最强主信号

| repetition | 样本量 | FALSE_BELIEF | 结论 |
| --- | ---: | --- | --- |
| `1` | `48` | `3/48 = 0.062` | 基本带不偏 |
| `3` | `48` | `40/48 = 0.833` | 已经大面积带偏 |
| `5` | `48` | `46/48 = 0.958` | 几乎全面带偏 |

#### 3.2 TierMem 里的多家族结果

| family | seed | `N=0` | `N=1` | `N=2` | 结论 |
| --- | --- | --- | --- | --- | --- |
| classification | `11` | `0.600` | `0.500` | `0.400` | 下降 |
| classification | `17` | `0.600` | `0.400` | `0.700` | 到 `N=2` 反弹 |
| security | `11` | `0.625` | `0.375` | `0.375` | 下降后持平 |
| security | `17` | `0.500` | `0.500` | `0.750` | 到 `N=2` 升高 |
| config | `11` | `0.333` | `1.000` | `0.833` | 第一轮最危险 |
| config | `17` | `0.500` | `1.000` | `0.667` | 第一轮最危险，复现 |

### 自建版现在最诚实的结论

> 自建版已经很强地支持：**重复错误说法会造出错信。**
> 但进入 TierMem 以后，不能说“越固化越糟”普遍成立；更准确的说法是：**不同家族轨迹不同，其中 `config` 家族最像有稳定的第一轮固化危险点。**

### 自建版可信度

| 维度 | 评价 | 原因 |
| --- | --- | --- |
| 数据口径 | 中等偏低 | 不是官方 benchmark |
| 机制清晰度 | 高 | 测的就是“错信息反复出现会不会压过真信息” |
| 结果强度 | 较高 | `repetition=1/3/5` 的主信号很强 |
| 人审准备度 | 较高 | 已导出 `144` 条人审包并修过一次标签 bug |

---

## 4. 两条线怎么用

| 用途 | 该用哪条 |
| --- | --- |
| 你想说“这是官方 benchmark 告诉我的” | 用 **官方版** |
| 你想说“这个机制真的会发生” | 用 **自建版** |
| 你想做论文里最干净的主表 | 先放 **官方版** |
| 你想解释为什么明明官方线不强，但机制上还是值得研究 | 再放 **自建版** |

所以后面最好固定成这个写法：

1. **官方版主结论**：没有观察到原始 `RQ2` 的放大效应，目前偏负面且欠功效。
2. **自建版机制结论**：重复错误说法会强烈制造错信；但进入 TierMem 后，放大/恢复取决于题目家族。

---

## 5. 现在不能再说的话

1. 不能再说“RQ2 全都是官方 benchmark 跑出来的”。
2. 不能再说“自建版和官方版可以混成一个结论”。
3. 不能再说“固化一定会把幻觉越压越大”。

---

## 6. 现在可以直接拿去汇报的一句话

> `RQ2` 现在已经被拆成两条线：  
> **官方版** 用官方 `HaluMem` 数据切片，当前没有看到支持“固化放大幻觉”的证据；  
> **自建版** 用 factual poison 套件，已经强烈看到“重复错误说法会制造错信”，但进入 TierMem 后的变化是家族相关的，不是统一单调放大。

