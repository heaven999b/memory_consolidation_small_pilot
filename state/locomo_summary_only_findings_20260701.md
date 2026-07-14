# LoCoMo Summary-Only Findings (Final: 100-QA)

Date: 2026-07-01
Authoritative run family: `micro_sweep_locomo_s5_summary_20260701` (5 sessions x 20 QA = 100 QA)
Superseded run family: `micro_sweep_locomo_q30_summary_20260701` (1 session x 30 QA)
Primary metric: `F1`
Reference metric: `BLEU1`
Secondary-only metric: `exact_match`

## How to read these scores (0.x means what)

All scores are answer-quality scores on a 0-1 scale (0 = wrong, 1 = perfect).

- `F1` (primary): word-overlap between the model answer and the gold answer. Partial credit.
  Example: gold `transgender woman`, model `trans community member` -> partial F1 (~0.3-0.4), not 0.
  `F1=0.286` means the model answers overlap with the gold answers by roughly 29% on average.
- `BLEU1`: another word-overlap score, tracks F1 closely; use only as a cross-check.
- `exact_match`: 1 only if the answer is word-for-word identical, else 0. Far too harsh for
  open-form LoCoMo answers (penalizes semantically-correct paraphrases). Do NOT use as a decision metric.

## Main Result (100 QA, authoritative)

On the `LoCoMo` slice with `session_limit=5` and `qa_limit=20` (100 QA), the `summary_only` route
shows essentially NO meaningful effect of consolidation depth on utility:

- `N=0`: `F1=0.286`, `BLEU1=0.249`
- `N=1`: `F1=0.300`, `BLEU1=0.261`
- `N=2`: `F1=0.303`, `BLEU1=0.264`

All three values sit within `0.017` F1 of each other (noise). The curve is flat / very slightly
monotonically increasing. There is NO inverted-U.

### Important correction vs the earlier 30-QA result

The earlier single-session 30-QA run suggested a weak inverted-U (`N=0/1/2 = 0.274 / 0.324 / 0.316`,
i.e. N=1 best, N=2 regressing). Scaling to 100 QA REFUTED this:

- The `N=0 -> N=1` gain shrank from `+18%` relative (30 QA) to `+5%` relative (100 QA).
- The `N=2` regression disappeared; at 100 QA, `N=2` is slightly above `N=1`.

Read: the 30-QA inverted-U was small-sample noise. Any conclusion below 100 QA on this slice is unreliable.

## Cost (100 QA)

- `N=0`: `158` API calls, `102,428` tokens
- `N=1`: `460` API calls, `327,636` tokens
- `N=2`: `452` API calls, `319,388` tokens

Read: consolidation roughly TRIPLES cost (N=0 -> N=1/2) for no measurable utility gain.

## Category Pattern (100 QA)

- `Category 1 F1` (n=39): `0.113 -> 0.139 -> 0.161` (small monotone rise, ~0.05 total)
- `Category 2 F1` (n=45): `0.442 -> 0.441 -> 0.437` (flat)
- `Category 3 F1` (n=14): `0.229 -> 0.243 -> 0.224` (flat / noise)
- `Category 4 F1` (n=2):  `0.100` flat (too few samples, ignore)

Read: even at the category level the inverted-U is gone. C1 shows a tiny monotone gain; C2/C3 are flat.
The effect is far too small to claim anything on the utility axis.

## Bottom-line conclusions (stable across scale)

1. Route matters: `research_only` (raw evidence, F1 ~0.76 on prior slices) strongly beats
   `summary_only` (F1 ~0.29). This is the robust finding.
2. Consolidation depth N does NOT improve utility on LoCoMo and roughly triples cost.
   The utility axis for this question is exhausted; more LoCoMo sweeps will not change this.

## Caveats

- Single conversation family scaled by QA count; not yet multi-conversation diversity at large scale.
- `pyserini` is not installed, so lexical rescue is still fallback-based rather than full BM25.
- `exact_match` is too harsh for open-form LoCoMo answers and must not be the decision metric.
- This is the UTILITY axis (plan E2), not the hallucination/safety axis (plan E1/E3). The plan's
  go/no-go rule is defined on hallucination/safety risk vs N, which is NOT tested by these runs.
  Next step is HaluMem-Medium (hallucination axis), not more LoCoMo utility sweeps.

## Output Files

- Sweep table (100 QA, authoritative): `outputs/v2_tiermem_micro/sweep_reports/micro_sweep_locomo_s5_summary_20260701.md`
- Sweep table (30 QA, superseded): `outputs/v2_tiermem_micro/sweep_reports/micro_sweep_locomo_q30_summary_20260701.md`
- Per-item artifacts: `outputs/v2_tiermem_micro/locomo/linked_view/micro_sweep_locomo_s5_summary_20260701_summary_only_n{0,1,2}/`
