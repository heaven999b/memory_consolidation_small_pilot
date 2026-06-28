# Paper Baseline Spec

## Goal

把当前 `memory_consolidation_small_pilot` 从 “能跑的 pre-pilot” 往 “论文级 baseline packet” 推进，但不虚报已经拥有 benchmark-level validity。

## Frozen Reviewer-Facing Requirements

### R1. Core closed-loop baseline trio must be frozen

必须在同一个 `N`-sweep 里同时比较：

- `raw_only`
- `summary_only`
- `tiered`

允许额外报告当前最好方法，但不能用更复杂方法替代 baseline trio 本身。

### R2. Consolidation depth must stay the primary variable

- 主轴仍然是 `N`
- baseline panel 里不能把 “换模型” 伪装成主对比

### R3. Stage-wise failure attribution must be visible

至少要能看见：

- answer-side propagation
- latent / residual contamination
- unsupported / unsafe / conflict family behavior

### R4. Utility, risk, and cost must be reported together

最小 baseline packet 不能只报 accuracy，也不能只报 safety。

至少要包含：

- benign utility / answerability
- hallucination / propagation risk
- raw escalation or equivalent fallback cost
- mean cost or latency proxy

### R5. There must be at least one model-backed sanity slice

最小论文 baseline 不能完全停留在 rule-based proxy。

至少要有：

- 一个 benign/conflict answerability sanity slice
- 一个 hallucination stress sanity slice

### R6. Paper-level readiness requires explicit gap accounting

如果还没有以下条件，artifact 必须明确写出它们仍然是 blocker：

- external benchmark grounding
- `TierMem`-style primary implementation grounding
- non-proxy exact closure on current frontier branch
- multi-seed model-backed baseline panel

## Current Intended Use

这份 spec 不是说项目已经达到论文基线，而是冻结一套之后每轮都要对齐的 reviewer-facing baseline gate。
