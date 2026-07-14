# E1 Block 1 Findings: HaluMem Targeted Cov10 Depth

Date: 2026-07-01
Benchmark: HaluMem-Medium
Setting: `summary_only`, `qa_retrieved_pages`, warmup `top_k=10`, 1 session, 15 QA

## Core Curve

| N | F1 | Correct | Abstain Forgetting (factual) | Unsupported Fabrication (unknown) | Fact Distortion (factual) | Overlap on QA Pages |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.205 | 0.533 | 0.333 | 0.333 | 0.222 | n/a |
| 1 | 0.205 | 0.667 | 0.333 | 0.167 | 0.111 | 0.733 (22/30) |
| 2 | 0.189 | 0.400 | 0.444 | 0.167 | 0.444 | 0.750 (24/32) |
| 4 | 0.162 | 0.467 | 0.444 | 0.167 | 0.333 | 0.750 (24/32) |

## Decision

Block 1 passes the planned gate.

- `unsupported_fabrication` drops at `N=1` from `2/6` to `1/6` and stays flat at `1/6` for `N=2` and `N=4`.
- Overlap is stable after targeted consolidation turns on: `0.733 -> 0.750 -> 0.750`.
- The degradation beyond `N=1` is therefore not explained by retrieval coverage collapse.
- The failure pattern shifts at deeper compression:
  - `abstain_forgetting` rises from `3/9` to `4/9` at `N>=2`
  - `fact_distortion` rises from `1/9` at `N=1` to `4/9` at `N=2`, then remains elevated at `3/9` at `N=4`

## Story

The supported story is:

1. First-pass targeted consolidation behaves like denoising.
2. Deeper consolidation does not re-open unsupported fabrication.
3. Instead, deeper consolidation reallocates errors into forgetting and factual distortion.

Short version: `denoise at N=1, then degrade via failure-mode migration for N>=2`.

## Caveats

- This is still only 1 session / 15 QA.
- BM25 is unavailable, so all results remain under the summary-first fallback path.
- Targeted consolidation is not equivalent to all-pages consolidation; this is a scoped experimental regime.

## Pointers

- Judge report: `outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_depth_20260701_judge.md`
- Partial sweep descriptor: `outputs/v2_tiermem_micro/sweep_reports/e1_halumem_targeted_cov10_depth_20260701_partial.json`
