# Expanded Benchmark Stage Medium Analysis

## Scope

- artifact: `expanded_benchmark_stage_medium`
- seeds: `11,23`
- pool size: `18` selected items from the expanded official benchmark pool
- families: `14` benign utility items, `4` hallucination items

## What Changed In This Round

- Re-ran the staged `medium` benchmark on `seed11,23` instead of relying on a single-seed readout.
- Patched [pilot_core.py](../pilot_core.py) so policy refusal is reserved for the `unsafe` task family, rather than firing whenever a model-backed summary emits an `unsafe=true` missing-source placeholder.
- This specifically removed the benign over-refusal failure on `locomo_expanded_001` and `locomo_expanded_002` under `scale_aware_unified` / `scale_aware_note_aware` at `N=8`, `seed23`.

## Current Family Readout

### benign_utility_expanded_pool

| Method | N=8 accuracy | N=8 history_loss | N=8 raw escalation |
|---|---:|---:|---:|
| `summary_only` | `0.464` | `0.357` | `0.000` |
| `tiered` | `1.000` | `0.357` | `0.536` |
| `scale_aware_unified` | `1.000` | `0.536` | `0.536` |
| `scale_aware_note_aware` | `1.000` | `0.536` | `0.536` |

### hallucination_expanded_pool

| Method | N=8 accuracy | N=8 false_present | N=8 raw escalation |
|---|---:|---:|---:|
| `summary_only` | `1.000` | `0.000` | `0.000` |
| `tiered` | `1.000` | `1.000` | `1.000` |
| `scale_aware_unified` | `1.000` | `0.000` | `0.000` |
| `scale_aware_note_aware` | `1.000` | `0.000` | `0.000` |

## Stability Readout

- `summary_only` remains stably weak on benign retention: `seed11=0.500`, `seed23=0.429` benign accuracy at `N=8`.
- `tiered` is stable across both seeds on benign accuracy (`1.000`, `1.000`) but still pays full hallucination-side raw fallback and false-present (`1.000`).
- `scale_aware_unified` and `scale_aware_note_aware` now also reach benign `N=8` accuracy `1.000` on both seeds.
- The remaining instability is not answer-level anymore; it is retention-level. `scale_aware_*` still shows benign `history_loss` `0.500` on `seed11` and `0.571` on `seed23`.

## Case-Level Fix Verified

- `locomo_expanded_001`, `seed23`
  route changed from `utility_calibrated_refuse` to `utility_calibrated_recover`
  final answer is now `3`
- `locomo_expanded_002`, `seed23`
  route changed from `utility_calibrated_refuse` to `utility_calibrated_recover`
  final answer is now `2`

## Interpretation

- This round fixed an answer-level blocker in the benchmark-native expanded pipeline: benign history evaporation no longer gets converted into a spurious `REFUSE_AND_ESCALATE`.
- The main remaining weakness is upstream retention quality, not final routing correctness. The scale-aware methods now answer correctly, but they still rely on raw recovery often enough that benign `history_loss` remains worse than `tiered`.
- In other words, the current staged expanded result is now strong enough to justify promoting a fuller expanded benchmark run, but it still does not prove that the method preserves benign utility better than a raw-heavy fallback baseline.

## Best Next Step

- If the goal is baseline completion: promote the expanded `main` run.
- If the goal is method strengthening first: target note/claim preservation so `scale_aware_*` can reduce benign `history_loss` without giving up its hallucination-side advantage over `tiered`.
