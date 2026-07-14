# RQ2 自建版 v3 领域扩充（2026-07-07）

这次不是继续在旧的 `12` 个 fact 上反复换 seed / 换 `N` / 换问法，而是直接补了一套新的 **领域多样化题库**。

## 1. 这次补了什么

- 新套件版本：`v3`
- 新题总数：`18` 个 base facts
- 新 probe 数：
  - `free + operational` 时：`36` 个 probes
  - 每个 `N / seed` 条件下按这 36 个 probes 统计
- 新家族：
  - `biochemistry`
  - `molecular_biology`
  - `genetics`
  - `clinical_medicine`
  - `chemistry`
  - `microbiology`

对应数据文件：

- [rq2_selfbuilt_suite_v3_domain_diverse.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/rq2_selfbuilt_suite_v3_domain_diverse.json)

## 2. 为什么这版比旧版更像样

旧版的问题是：

1. 领域太窄，基本都像内部配置 / 安全 / 分类小题。
2. 答案形态太单一，很多就是 `yes/no`、单个词、单个短值。
3. 人工复核时会感觉像在重复刷同一种错误。

这次 v3 故意补了几类不同答案形态：

| 答案类型 | 例子 |
| --- | --- |
| 双输出 / 配对值 | `2 ATP + 2 NADH` |
| 反应产物对 | `lactate + NAD+` |
| 三元组 / 位点序列 | `Ser195-His57-Asp102` |
| 方向性短语 | `3' to 5' on the template` |
| 映射式答案 | `AUG -> methionine` |
| 概率拆分 | `25% affected, 50% carrier, 25% unaffected non-carrier` |
| 核型记法 | `47,XXY` |
| 诊断短语 | `high-anion-gap metabolic acidosis` |
| 阈值 + 单位 | `>=126 mg/dL on repeat testing` |
| 方程 / 关系式 | `[A-] = [HA]` |
| 科学计数法 | `6.022 x 10^23 mol^-1` |
| 染色 + 形态 | `Gram-negative rod` |

## 3. 各领域覆盖

| 家族 | 题数 | 代表题 |
| --- | ---: | --- |
| `biochemistry` | `3` | 糖酵解净产出、LDH 反应产物、胰凝乳蛋白酶三联体 |
| `molecular_biology` | `3` | DNA 聚合酶模板方向、起始密码子映射、RNA 合成方向 |
| `genetics` | `3` | 常隐风险拆分、Klinefelter 核型、胸腺嘧啶二聚体修复 |
| `clinical_medicine` | `3` | DKA 酸碱模式、糖尿病阈值、O 阴性红细胞规则 |
| `chemistry` | `3` | Henderson-Hasselbalch 关系、酰胺羰基碳杂化、阿伏伽德罗常数 |
| `microbiology` | `3` | 大肠杆菌染色形态、肉毒梭菌需氧类型、HIV 基因组类型 |

## 4. 运行器已经接好了

`run_rq2_factual_poison.py` 现在已经支持：

- `--suite-version v3`
- 每题自带更具体的答案格式提示
- 学术域题目自动切换成更像“讲义 / 复习笔记 / 备忘单”的错误灌入话术，而不是旧的 `team / ops / settings` 口吻

## 5. 怎么跑

### 干看结构

```bash
.venv_tiermem_v2/bin/python run_rq2_factual_poison.py \
  --suite-version v3 \
  --query-modes free operational \
  --backend prompt_only \
  --repetition 3 \
  --dry-run
```

### 先跑 prompt-only 主信号

```bash
set -a && source .env.v3 && set +a
.venv_tiermem_v2/bin/python run_rq2_factual_poison.py \
  --suite-version v3 \
  --query-modes free operational \
  --backend prompt_only \
  --repetition 1 \
  --report-id rq2_v3_rep1_prompt_only
```

再把 `--repetition` 换成 `3`、`5`。

### 再接 TierMem

```bash
set -a && source .env.v3 && set +a
.venv_tiermem_v2/bin/python run_rq2_factual_poison.py \
  --suite-version v3 \
  --query-modes free operational \
  --backend tiermem \
  --repetition 3 \
  --passes 0 1 2 \
  --seed 11 \
  --report-id rq2_v3_rep3_tiermem_seed11_n012
```

## 6. 最诚实的预期

这次扩充解决的是：

- **领域单调**
- **答案形态单调**
- **人工复核时总像在看同一题**

这次扩充**还没有解决**的是：

- 题数还不算大
- 还没跑出结果
- 还没看哪些新领域最容易被带偏

所以这一步的意义不是“直接把 RQ2 证明了”，而是：

> 把自建版从“几类内部配置小题”升级成“跨学科、跨答案类型、能继续长”的正式题库底座。

