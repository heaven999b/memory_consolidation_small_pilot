# PSU Paper Packet

这份 packet 把当前最接近论文正文会直接引用的 PSU 证据收在一起：方法定义、主 recall 表、关键 paired-delta、artifact contract 覆盖、以及更大 benchmark section 的当前规模。

## Method

- name: `Provenance-Scaffolded Unified`
- short name: `PSU`
- routing architecture: `scale_aware_note_aware`
- compaction contract: `tiny_carry_forward_scaffold`

## Recall Main Panel (N=8)

| Method | accuracy | propagation | raw escalation | history loss | benign/conflict error | unsafe error | carry-forward record |
|---|---:|---:|---:|---:|---:|---:|---:|
| summary_only | 0.208 | 0.500 | 0.000 | 0.875 | 0.875 | 1.000 | 0.000 |
| tiered | 0.792 | 0.208 | 0.750 | 0.875 | 0.250 | 0.250 | 0.000 |
| scale_aware_unified | 0.875 | 0.125 | 0.583 | 0.875 | 0.000 | 0.750 | 0.000 |
| scale_aware_note_aware | 0.875 | 0.125 | 0.583 | 0.875 | 0.000 | 0.750 | 0.000 |
| psu_no_carry | 0.958 | 0.042 | 0.417 | 0.625 | 0.000 | 0.250 | 0.000 |
| psu | 1.000 | 0.000 | 0.042 | 0.062 | 0.000 | 0.000 | 0.500 |

## Key Paired Deltas

| Comparison | Pairs | Baseline | Treatment | Improvement Delta | 95% CI |
|---|---:|---:|---:|---:|---|
| scale_aware_note_aware -> PSU accuracy | 24 | 0.875 | 1.000 | 0.125 | [0.000, 0.292] |
| scale_aware_note_aware -> PSU history_loss | 16 | 0.875 | 0.062 | 0.812 | [0.625, 1.000] |
| scale_aware_note_aware -> PSU raw_escalation | 24 | 0.583 | 0.042 | 0.542 | [0.333, 0.750] |

## Artifact Contract Coverage

| Panel | Records | Pass Trace | Provenance | Quarantine | Stage Attribution |
|---|---:|---:|---:|---:|---:|
| actual_summarizer_slice | 128 | 1.000 | 1.000 | 0.141 | 1.000 |
| actual_recall_expansion | 288 | 1.000 | 1.000 | 0.139 | 1.000 |
| actual_hallucination_stress | 192 | 1.000 | 1.000 | 0.083 | 1.000 |
| actual_carry_forward | 96 | 1.000 | 1.000 | 0.219 | 1.000 |

## Benchmark Section Scale

- seeds: `[11, 23]`
- benign_utility_benchmark_section: `16` items from `['locomo_core_v2', 'longmemeval_direct_v1']`
- hallucination_benchmark_section: `16` items from `['halumem_core_v2', 'halumem_holdout_v1']`

## Bottom Line

- PSU is now supported by a stable multi-seed recall main panel rather than only a single-seed pilot.
- The strongest gain is not just final accuracy; it is the collapse of high-N `history_loss` and `raw_escalation`, which is exactly the mechanism the method claims to improve.
- The current benchmark-first reviewer section is broader than the initial minimal baseline, but it is still a 32-item frozen section rather than a full paper-scale benchmark sweep.
