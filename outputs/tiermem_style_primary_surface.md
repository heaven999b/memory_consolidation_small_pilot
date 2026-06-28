# TierMem-Style Primary Surface

这个 artifact 的目标不是宣称我们已经变成完整 TierMem-native base，而是把 reviewer 应该先看到的 benchmark-grounded panel 放到最前面，把 synthetic / proxy 结果降成支撑层。

## Status

- benchmark-first surface ready: `True`
- tiermem-style primary base status: `pass`
- full TierMem-native grounding: `False`
- benchmark source kind: `broader_reviewer_section`
- benchmark-first entrypoint: `run_benchmark_first_primary_entrypoint.py`
- benchmark-first entrypoint ready: `True`
- benchmark-first proxy base path: `outputs/benchmark_first_proxy_base.json`
- benchmark-first proxy base complete: `True`
- benchmark-native primary base path: `outputs/benchmark_native_primary_base.json`
- benchmark-native primary base ready: `True`
- benchmark-native primary base status: `pass`
- exact non-proxy frontier ready: `True`
- note: The repo now exposes a benchmark-native primary base over frozen benchmark manifests, so the reviewer-facing primary baseline is no longer just a local proxy surface; the remaining gap is that this is still not a literal full TierMem reproduction or a final large-scale paper section.

## Benchmark-Grounded Core

- source path: `outputs/external_benchmark_reviewer_section.json`
- source kind: `broader_reviewer_section`
- adapter grounding status: `pass`
- panel names: `['benign_utility_benchmark_section', 'hallucination_benchmark_section']`
- slice panel names: `['halumem_core_v2', 'halumem_holdout_v1', 'locomo_core_v2', 'longmemeval_direct_v1']`

### HaluMem-Style Hallucination Section (N=8)

| Method | accuracy | propagation | raw escalation | false_present |
|---|---:|---:|---:|---:|
| summary_only | 0.719 | 0.281 | 0.000 | 0.000 |
| tiered | 1.000 | 0.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 0.000 | 0.156 | 0.156 |
| scale_aware_note_aware | 1.000 | 0.000 | 0.094 | 0.094 |

### Benign Utility Section (N=8)

| Method | accuracy | propagation | raw escalation | history_loss |
|---|---:|---:|---:|---:|
| summary_only | 0.469 | 0.531 | 0.000 | 0.438 |
| tiered | 0.906 | 0.094 | 0.438 | 0.438 |
| scale_aware_unified | 0.906 | 0.094 | 0.438 | 0.438 |
| scale_aware_note_aware | 0.906 | 0.094 | 0.438 | 0.438 |

## Model-Backed Support

### Actual Recall Expansion (N=8)

| Method | accuracy | propagation | raw escalation | history_loss |
|---|---:|---:|---:|---:|
| summary_only | 0.208 | 0.500 | 0.000 | 0.875 |
| tiered | 0.792 | 0.208 | 0.750 | 0.875 |
| scale_aware_unified | 0.875 | 0.125 | 0.583 | 0.875 |
| scale_aware_note_aware | 0.875 | 0.125 | 0.583 | 0.875 |

### Actual Hallucination Stress

| Method | N=1 accuracy | N=1 false_present | N=8 accuracy | N=8 false_present |
|---|---:|---:|---:|---:|
| summary_only | 0.750 | 0.000 | 1.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 | 0.875 |
| scale_aware_unified | 1.000 | 0.125 | 1.000 | 0.000 |
| scale_aware_note_aware | 1.000 | 0.062 | 1.000 | 0.000 |

## Synthetic Reference

| Method | N=8 accuracy | N=8 propagation | N=8 raw escalation | N=8 mean cost |
|---|---:|---:|---:|---:|
| raw_only | 1.000 | 0.000 | 1.000 | 3.200 |
| summary_only | 0.004 | 0.996 | 0.000 | 2.440 |
| tiered | 0.977 | 0.023 | 0.973 | 3.997 |
| scale_aware_unified | 0.985 | 0.015 | 0.600 | 3.600 |

## Why This Is Still Not Paper-Ready

- 现在主表面已经进入 benchmark-native primary base 阶段：主 baseline 显式吃 frozen benchmark manifests、query contract 和 evidence contract，而不是只靠 local proxy surface。
- blocker 已经从 must-fix 变成补强：接下来要继续扩更大 benchmark section，并进一步降低 reviewer-facing 解释对 synthetic support 的依赖。
- 当前 frontier 虽然已经是 `exact_stress_closure_reintegration`，且 proxy rows = `0/336`，这说明 stress-closure 已经去 proxy 化；现在如果还要继续推进，重点就不是补 proxy，而是扩 benchmark coverage 和收紧 paper-facing证据结构。
