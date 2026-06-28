# External Benchmark Minimal Baseline

这个 artifact 把两条 frozen external benchmark slice 真正跑进现有 baseline trio / unified stack，而不是只停在 adapter-ready 状态。

- seeds: `[11, 23]`
- architectures: `summary_only, tiered, scale_aware_unified, scale_aware_note_aware`
- N values: `[1, 4, 8]`

## halumem_hallucination

- slice_ids: `['halumem_bench_01', 'halumem_bench_02', 'halumem_bench_03', 'halumem_bench_04', 'halumem_bench_05', 'halumem_bench_06', 'halumem_bench_07', 'halumem_bench_08']`
- slice_manifest_version: `v2`
- num_items: `8`

| Method | N=1 acc | N=1 false_present | N=1 raw escalation | N=8 acc | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|---:|---:|---:|
| summary_only | 0.125 | 0.000 | 0.000 | 0.750 | 0.000 | 0.000 |
| tiered | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| scale_aware_unified | 1.000 | 0.500 | 0.500 | 1.000 | 0.125 | 0.125 |
| scale_aware_note_aware | 1.000 | 0.125 | 0.125 | 1.000 | 0.125 | 0.125 |

### Seed Stability (N=8)

| Method | accuracy by seed | false_present by seed | false_present span |
|---|---|---|---:|
| summary_only | 11:0.750, 23:0.750 | 11:0.000, 23:0.000 | 0.000 |
| tiered | 11:1.000, 23:1.000 | 11:1.000, 23:1.000 | 0.000 |
| scale_aware_unified | 11:1.000, 23:1.000 | 11:0.250, 23:0.000 | 0.250 |
| scale_aware_note_aware | 11:1.000, 23:1.000 | 11:0.250, 23:0.000 | 0.250 |

## locomo_benign_utility

- slice_ids: `['locomo_bench_01', 'locomo_bench_02', 'locomo_bench_03', 'locomo_bench_04', 'locomo_bench_05', 'locomo_bench_06', 'locomo_bench_07', 'locomo_bench_08']`
- slice_manifest_version: `v2`
- num_items: `8`

| Method | N=1 acc | N=1 history_loss | N=1 raw escalation | N=8 acc | N=8 history_loss | N=8 empty-note-abstain |
|---|---:|---:|---:|---:|---:|---:|
| summary_only | 1.000 | 0.000 | 0.000 | 0.375 | 0.438 | 0.188 |
| tiered | 1.000 | 0.000 | 0.000 | 0.812 | 0.438 | 0.000 |
| scale_aware_unified | 1.000 | 0.000 | 0.000 | 0.812 | 0.438 | 0.000 |
| scale_aware_note_aware | 1.000 | 0.000 | 0.000 | 0.812 | 0.438 | 0.000 |

### Seed Stability (N=8)

| Method | accuracy by seed | history_loss by seed | history_loss span |
|---|---|---|---:|
| summary_only | 11:0.375, 23:0.375 | 11:0.500, 23:0.375 | 0.125 |
| tiered | 11:0.875, 23:0.750 | 11:0.500, 23:0.375 | 0.125 |
| scale_aware_unified | 11:0.875, 23:0.750 | 11:0.500, 23:0.375 | 0.125 |
| scale_aware_note_aware | 11:0.875, 23:0.750 | 11:0.500, 23:0.375 | 0.125 |

## Readout

- HaluMem-style slice now measures benchmark-grounded unsupported-target false-present behavior under the real summarizer loop.
- LoCoMo slice now measures benchmark-grounded benign answerability / history-loss behavior under the same compaction stack.
- Multi-seed seed snapshots make it easier to tell whether the first benchmark readout is structurally stable or just a lucky single-seed slice.
- This is still a minimal benchmark panel, not a full TierMem-style primary benchmark base, but it is materially stronger than an adapter-only placeholder.
