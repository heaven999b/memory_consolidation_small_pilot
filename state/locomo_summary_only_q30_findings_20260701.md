# LoCoMo Summary-Only Q30 Findings

> [SUPERSEDED 2026-07-01] The inverted-U reported below was small-sample (30 QA) noise.
> It was REFUTED by the 100-QA run. See the authoritative version:
> `state/locomo_summary_only_findings_20260701.md`.
> Do not cite the inverted-U conclusion from this file.

Date: 2026-07-01
Run family: `micro_sweep_locomo_q30_summary_20260701`
Primary metric: `F1`
Reference metric: `BLEU1`
Secondary-only metric: `exact_match`

## Main Result

On the `LoCoMo` micro slice with `session_limit=1` and `qa_limit=30`, the `summary_only` route shows a weak inverted-U pattern over consolidation depth:

- `N=0`: `F1=0.274`, `BLEU1=0.230`, `exact=0.067`
- `N=1`: `F1=0.324`, `BLEU1=0.275`, `exact=0.100`
- `N=2`: `F1=0.316`, `BLEU1=0.269`, `exact=0.100`

Interpretation:

- One consolidation pass provides a modest utility gain over no consolidation.
- A second pass does not continue that gain and slightly regresses relative to `N=1`.
- The current evidence supports a weak inverted-U story for the `summary_only` route, but not a strong claim yet because this is still a single-session result.

## Cost

- `N=0`: `98` API calls, `57,630` total tokens
- `N=1`: `155` API calls, `88,970` total tokens
- `N=2`: `174` API calls, `97,422` total tokens

Interpretation:

- The utility gain from `N=0` to `N=1` is real but expensive.
- The move from `N=1` to `N=2` mostly increases cost without additional benefit.

## Category Pattern

- `Category 1 F1`: `0.025 -> 0.150 -> 0.125`
- `Category 2 F1`: `0.447 -> 0.463 -> 0.463`
- `Category 3 F1`: `0.205 -> 0.205 -> 0.205`

Interpretation:

- Most of the gain from `N=1` comes from `Category 1`.
- `Category 2` is roughly flat after a small lift.
- `Category 3` does not improve.

## Caveats

- Single session only
- `pyserini` is not installed, so lexical rescue is still fallback-based rather than full BM25
- Exact match is too harsh for many LoCoMo open-form answers and should not be used as the primary decision metric

## Output Files

- Sweep table: [micro_sweep_locomo_q30_summary_20260701.md](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/sweep_reports/micro_sweep_locomo_q30_summary_20260701.md)
- `N=0`: [micro_sweep_locomo_q30_summary_20260701_summary_only_n0.json](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/micro_reports/micro_sweep_locomo_q30_summary_20260701_summary_only_n0.json)
- `N=1`: [micro_sweep_locomo_q30_summary_20260701_summary_only_n1.json](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/micro_reports/micro_sweep_locomo_q30_summary_20260701_summary_only_n1.json)
- `N=2`: [micro_sweep_locomo_q30_summary_20260701_summary_only_n2.json](/Users/yihaiwen/Documents/New%20project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/micro_reports/micro_sweep_locomo_q30_summary_20260701_summary_only_n2.json)
