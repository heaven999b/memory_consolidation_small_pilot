# MemEvoBench 协议复现 · ASR 水分分解(pilot)· 2026-07-12

> 目的:按 MemEvoBench(arXiv 2604.15774)自己的评估协议,在它自己的 QA 数据上跑多 mode,
> 把它的 headline ASR 拆成「judge/query 基线水位」+「真·记忆效应」+「反馈棘轮」三部分。
> 一句话结论:**它的 headline ASR≈90% 里约 55 个点是宽 judge 对 query 本身的基线水位;
> 真正归因于投毒记忆的净效应是 +35.7 点——这个是真的、CI 不重叠、可发表(前提:报 delta,不报裸数)。**

## 装置
- 代码:MemEvoBench 原样 `iterative_memory_triplequery_test.py`(未改),三轮迭代回写。
- 数据:它自带 7 域 QA(`memorybench/QA/*_memory_triplequery.json`),每域取前 4 题,共 28 题 / 84 个 (题,轮) 对。
- model = judge = `gpt-4.1-mini`(openai,temp 0)。**注意:同源 judge**,是已知乐观口径;对 mode 间 delta 是常量,不影响相对比较,但会同时抬高 base 与 original 的绝对值(见 limitation)。
- mode:`base_model`(无记忆)/ `original`(投毒记忆)/ `only_safe`(投毒+安全prompt)/ `original --enable-feedback`(+单向反馈)。
- ASR = MISLED 的 (题,轮) 占比;Wilson 95% CI。产物:`scratchpad/memevo_pilot/*.json` + `aggregate.py`。

## 主结果

| mode | ASR(逐轮) | k/n | 95% CI | ASR(任一轮/题) |
|---|---|---|---|---|
| base_model | 54.8% | 46/84 | [44.1, 65.0]% | 78.6% (22/28) |
| original | 90.5% | 76/84 | [82.3, 95.1]% | 100% (28/28) |
| only_safe | 77.4% | 65/84 | [67.4, 85.0]% | 96.4% (27/28) |
| original_feedback | 90.5% | 76/84 | [82.3, 95.1]% | 100% (28/28) |

## 水分分解(逐轮 ASR)
- **base_model 54.8%** = 基线水位:无任何记忆,宽 judge 对 query 本身的误判率。headline 里超过一半是这个。
- **真·记忆效应 = original − base = +35.7 点**。base [44,65]% 与 original [82,95]% CI 不重叠 → **投毒记忆确有实质、可归因的效应**,不是伪影。
- **安全 prompt 恢复 = original − only_safe = +13.1 点**(77.4%),远回不到 baseline → 印证「静态 prompt 防御不足」(与 MemEvoBench 自身主张一致)。
- **反馈棘轮 = feedback − original = +0.0 点**(天花板效应,3 轮内无边际贡献)→ 「单向反馈让记忆更坏」这条在本 pilot **不被支持**。

## 按域拆(逐轮 ASR)
| 域 | base | original | only_safe | +feedback | 记忆净效应(orig-base) |
|---|---|---|---|---|---|
| finance | 58% | 92% | 83% | 83% | +33 |
| health | 58% | 92% | 75% | 92% | +33 |
| privacy | 67% | 92% | 92% | 92% | +25 |
| **food** | **25%** | **100%** | 58% | 92% | **+75** |
| mental | 58% | 75% | 67% | 83% | +17 |
| **traffic** | **50%** | **100%** | 83% | 100% | **+50** |
| customerservice | 67% | 83% | 83% | 92% | +17 |

**关键洞见**:记忆净效应集中在 base 低的域(food +75、traffic +50);base 高的域(privacy/finance)headline 大半是水。
→ 诚实的记忆危害叙事应聚焦低-base 域;高-base 域的高 ASR 主要是 judge 水位。

## 对论文的两条合法路径(都被本 pilot 支持)
1. **「刷高数字」的合法形态**:报 original ASR≈90% 作为 **worst-case 上界**,与 MemEvoBench 同口径可比;只要同时给全谱(base→original)并标清 worst-case,数字高且不造假。
2. **更强/更新的一篇(推荐)**:critical re-evaluation —— 「现有记忆安全 benchmark 的 ASR 有 ~55 点是 judge 基线水位;真·记忆净效应 +36 点且集中在低-base 域;静态安全 prompt 仅恢复 13 点」。这是本 pilot 直接支撑、且 MemEvoBench 没做的角度。

## Limitation(硬前提,必须守)
1. **同源 judge**:model=judge=gpt-4.1-mini,是乐观宽口径。base 的 54.8% 里有多少是「judge 过度 flag」vs「真不安全」**未经独立 judge / 人工金标验证**。→ 下一步必做:换独立 judge(或严口径 StrongREJECT 版)重跑,看 base 和 +35.7 的 delta 是否守得住。
2. **小样本**:28 题 / 84 轮,CI 偏宽(base 与 original 仅勉强不重叠)。
3. **仅 3 轮**:反馈棘轮的天花板可能是轮数不够,非机制无效。
4. delta 的因果强度依赖「投毒记忆」这一构造设定(它预埋 misleading 记忆),不等于「良性固化会自发产生危害」——那是母项目已判负的更强主张,别混。

## 第二 judge 闸门结果(2026-07-12,已跑)
judge2 = gpt-4o(独立),沿用 MemEvoBench 原样 rubric,只换模型;全部 336 轮重判。产物 `scratchpad/memevo_pilot/rejudge.py` + `rejudge_raw.json`。

| mode | J1(gpt-4.1-mini) | J2(gpt-4o) | 闸门(both) | 一致率/κ |
|---|---|---|---|---|
| base_model | 54.8% | 63.1% | 54.8% | 92% / κ=0.83 |
| original | 90.5% | 92.9% | 90.5% | 98% / κ=0.84 |
| only_safe | 77.4% | 90.5% | 76.2% | 85% / κ=0.44 |
| feedback | 90.5% | 97.6% | 90.5% | 93% / κ=0.38 |

**delta 存活(记忆效应 = original − base):judge1 +35.7 / judge2 +29.8 / AND-闸门 +35.7。**

### 两条硬结论
1. **记忆净效应真实且 judge-robust**:+30~36 点在独立 judge + 双闸门下全部守住,κ=0.83–0.84。**不是同源 judge 伪影。** = 可发表的正向。
2. **base 水位不是 judge 模型问题,是 rubric 问题**:更强的 gpt-4o 把 base 判得更高(63%),不是更低。→ **换 judge 模型压不掉 90% headline 的水;水在「缺 caveat=MISLED」这套 rubric 里。** 要证 base 是「过度 flag」而非「真不安全」,**只能人工金标**(两个共享 rubric 的 judge 都答不了)。修正上一版「第二 judge 定生死」的判断:第二 judge 只证了 delta 真,没能证 base 水——那需要人工。

## 下一步(按性价比)
1. **人工金标 ~20–30 条 base_model 的 MISLED 案例** → 量化那 55–63% 里「judge 过度 flag」占比。这是唯一能定「headline 水多深」的一刀(第二 judge 已证明换模型无用)。
2. 扩 n 到每域 ≥15,收窄 CI。
3. (可选)再加一个严口径 rubric 的 judge,看 base 掉多少 → 直接示范「rubric 才是水源」。
