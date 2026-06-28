# Paper Baseline Packet

这个 artifact 不假装我们已经有 benchmark-ready paper baseline。它做的事情是把 reviewer 真正在意的 baseline gate 冻结下来：哪些最小比较已经具备，哪些模型级 sanity 已经落地，哪些 blocker 仍然阻止我们把当前结果写成论文级 baseline。

## Verdict

- minimal closed-loop baseline ready: `True`
- paper-level baseline ready: `False`
- reason: the project now has a real closed-loop baseline trio, multi-seed model-backed sanity slices, an exact non-proxy stress-frontier closure, a broader reviewer-facing external benchmark section, a complete benchmark-first proxy base, and a benchmark-native primary base, but it still lacks larger-scale benchmark coverage before the baseline should be presented as paper-ready.

## Requirement Gate

- `PASS` Core baseline trio is frozen on the same sweep: observed architectures include `['adaptive_guarded', 'adaptive_tiered', 'raw_only', 'risk_first', 'scale_aware_unified', 'small_n_hybrid', 'summary_only', 'tiered', 'utility_calibrated', 'utility_first']`.
- `PASS` Consolidation depth remains the primary variable: observed N values = `[0, 1, 2, 4, 8]`.
- `PASS` Stage-wise failure attribution is visible: synthetic panel exposes answer-side and latent/residual failure rates in aggregate rows.
- `PASS` Utility, risk, and cost are reported together: synthetic panel reports accuracy, propagation, raw escalation, and mean cost together.
- `PASS` Real-model benign/conflict sanity slice exists: actual recall slice uses `12` items, seeds `[11, 23]`, and exposes answerability-loss metrics such as `history_loss`.
- `PASS` Real-model hallucination sanity slice exists: actual hallucination stress slice uses `8` items, seeds `[11, 23]`, and exposes `false_present` / `direct_unsupported_answer`.
- `PASS` Frozen model-backed baseline panel is multi-seed: actual recall seeds = `[11, 23]`, actual stress seeds = `[11, 23]`.
- `PASS` Primary baseline is grounded on an external benchmark slice: benchmark adapter layer status = `pass`, data-ready adapters = `2/2`, slice-ready adapters = `2/2`, benchmark panel attached = `True`, broader reviewer section attached = `True`.
- `PASS` Primary implementation is grounded in a TierMem-style base rather than a local proxy stack: primary surface status = `pass`, benchmark-first ready = `True`, native primary base ready = `True`, full TierMem-native grounding = `False`.
- `PASS` Benchmark-first proxy base is frozen end-to-end: proxy-base status = `pass`, proxy-base ready = `True`, full TierMem-native grounding = `False`.
- `PARTIAL` Broader benchmark reviewer section has enough scale for paper-facing use: current broader benchmark section size = `32` items across both family rollups.
- `PASS` Synthetic reference is explicitly demoted to support-only status: native primary base marks synthetic reference role = `support_only`.
- `PASS` Current stress frontier is closed without proxy rows: current reintegration mode = `exact_stress_closure_reintegration`, proxy rows = `0`.
- `PASS` Reviewer-facing paper baseline packet is frozen: this artifact freezes the baseline trio, model-backed sanity slices, and explicit blockers in one place.

## Synthetic Core Panel

同一 `N`-sweep 上的 baseline trio 已经存在，因此 reviewer 至少能看到 clean closed-loop comparison，而不是一串无法对齐的局部 patch。

| Method | N=0 acc | N=8 acc | N=8 propagation | N=8 residual | N=8 raw escalation | N=8 mean cost |
|---|---:|---:|---:|---:|---:|---:|
| raw_only | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 3.200 |
| summary_only | 0.769 | 0.004 | 0.996 | 0.927 | 0.000 | 2.440 |
| tiered | 1.000 | 0.977 | 0.023 | 0.927 | 0.973 | 3.997 |
| scale_aware_unified | 1.000 | 0.985 | 0.015 | 0.000 | 0.600 | 3.600 |

## Model-Backed Sanity

我们已经不只停在纯 proxy：real-model recall slice 和 real-model hallucination stress slice 都存在，所以 baseline story 至少有 model-backed sanity，而不是只有手写 compactor。

### Actual Recall Expansion (N=8)

| Method | accuracy | propagation | residual | raw escalation | history loss | empty-note-then-abstain | llm cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| summary_only | 0.208 | 0.500 | 0.083 | 0.000 | 0.875 | 0.312 | 0.2466 |
| tiered | 0.792 | 0.208 | 0.083 | 0.750 | 0.875 | 0.062 | 0.2466 |
| scale_aware_unified | 0.875 | 0.125 | 0.000 | 0.583 | 0.875 | 0.000 | 0.2466 |
| scale_aware_note_aware | 0.875 | 0.125 | 0.000 | 0.583 | 0.875 | 0.000 | 0.2466 |

### Actual Hallucination Stress

| Method | N=1 propagation | N=1 false_present | N=1 raw escalation | N=8 propagation | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|---:|
| summary_only | 0.250 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| tiered | 0.000 | 1.000 | 1.000 | 0.000 | 0.875 | 0.875 |
| scale_aware_unified | 0.000 | 0.125 | 0.125 | 0.000 | 0.000 | 0.000 |
| scale_aware_note_aware | 0.000 | 0.062 | 0.062 | 0.000 | 0.000 | 0.000 |

## Benchmark-First Primary Surface

- primary surface attached: `True`
- primary surface status: `pass`
- primary surface note: `The repo now exposes a benchmark-native primary base over frozen benchmark manifests, so the reviewer-facing primary baseline is no longer just a local proxy surface; the remaining gap is that this is still not a literal full TierMem reproduction or a final large-scale paper section.`

## Benchmark-First Proxy Base

- proxy base attached: `True`
- proxy base status: `pass`
- proxy base ready: `True`
- proxy base note: `The local benchmark-first proxy base is now complete and remains frozen as a support layer: adapter grounding, minimal external panel, broader reviewer section, benchmark-first primary surface, and exact non-proxy frontier closure are all still explicit, even though the main blocker has now moved up to a benchmark-native primary base.`

## Benchmark-Native Primary Base

- native primary base attached: `True`
- native primary base ready: `True`
- native primary base status: `pass`
- native primary base note: `The repo now has a benchmark-native primary base: the primary baseline surface is driven by frozen benchmark manifests, benchmark-family contracts, and runtime projection audits rather than only by a local proxy presentation layer. This is sufficient for reviewer-facing baseline grounding, even though it is still not a literal full TierMem reproduction.`

## Frontier Status

- current claim reintegration mode: `exact_stress_closure_reintegration`
- proxy rows in current reintegration artifact: `0/336`
- claim reintegration unified `N=8 false_present`: `0.214`
- claim reintegration note-aware `N=8 false_present`: `0.000`

## Benchmark Adapter Status

- benchmark adapter grounding status: `pass`
- benchmark adapter data-ready count: `2/2`
- benchmark adapter slice-ready count: `2/2`

## Benchmark-Grounded Panel

- benchmark panel attached: `True`
- benchmark panel names: `['halumem_hallucination', 'locomo_benign_utility']`
- broader reviewer section attached: `True`
- broader reviewer section families: `['benign_utility_benchmark_section', 'hallucination_benchmark_section']`

## Why This Is Not Paper-Ready Yet

- 当前 external benchmark 已经不再只是 adapter 占位，而且 reviewer-facing benchmark section 也已经从 starter panel 扩成了更宽的 family rollups；但它还不是完整的大规模 benchmark section。
- 当前 repo 已经有 benchmark-first primary surface，而且 benchmark-native primary base 也已经补上；但 paper-facing benchmark coverage 还不够大。
- 当前 benchmark-first proxy base 和 benchmark-native primary base 都已经补齐，所以接下来主要是扩 benchmark scale、继续压低 synthetic support 占比。
- 即使 primary-base blocker 已经补掉，当前更大的任务仍然是把 benchmark section 扩到更接近 paper-facing 的规模。

## Next Required Actions

- Expand the broader reviewer-facing benchmark section to a larger frozen scale so the paper-level baseline gate can move from reviewer-credible to fully paper-ready.
- Further reduce how much reviewer-facing interpretation depends on synthetic-reference support artifacts.
