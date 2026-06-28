# Repo Review And Table Analysis

## Current Snapshot

- Repo status: clean local checkout on `main`, already bound to the private GitHub repo.
- Release version: `v0.2.0-idea-baseline-private`
- Baseline gate: `minimal_closed_loop_baseline_ready = true`
- Paper gate: `paper_level_baseline_ready = false`
- Current external benchmark surface: `32` frozen items, `4` external panels, `3` external benchmark families
- Current manifest-backed primary-base surface: `38` total manifest-backed items, `6` panels, `4` task families

## Remaining Problems

### 1. Paper-facing benchmark scale is still too small

- The broader reviewer-facing external benchmark section is still only `32` frozen items.
- This is enough for reviewer-credible idea reporting, but still thin for a paper-facing baseline section.
- The repo itself still marks this honestly as `paper_level_baseline_ready = false`.

### 2. The benign utility bottleneck is still the main empirical weakness

- On the broader benchmark benign section at `N=8`, stronger methods improve accuracy a lot, but `history_loss_rate` still stays at `0.438`.
- This means the repo is no longer mainly blocked by hallucination control alone; the harder remaining problem is preserving useful benign detail under compression without paying too much raw fallback.

## Fixed In This Maintenance Pass

### 1. Task-family coverage is no longer limited to `benign` and `hallucination`

- The repo now freezes manifest-backed `conflict` and `unsafe` extension panels.
- The benchmark-native primary base now covers all four task families: `benign`, `conflict`, `hallucination`, and `unsafe`.
- This closes the old coverage gap without pretending the external benchmark scale problem is already solved.

### 2. Reproducibility is now explicitly pinned

- The repo now ships [requirements.txt](./requirements.txt), [environment.yml](./environment.yml), and [REPRODUCIBILITY.md](./REPRODUCIBILITY.md).
- The release path also documents the non-Python requirement on the local `deepseek` CLI.

### 3. Release regeneration is no longer fragmented

- The repo now ships [run_release_rebuild.py](./run_release_rebuild.py).
- That entrypoint rebuilds the current reviewer-facing packet in dependency order and preserves the intended multi-seed configuration for the release sanity slices.

## Simple Reading Of The Main Tables

### Synthetic Core: `outputs/aggregate_rows.csv` and `outputs/paper_baseline_panel.csv`

- `summary_only` collapses hard as consolidation depth grows. At `N=8`, accuracy falls to `0.004`, propagation rises to `0.996`, and benign overcompression rises to `0.983`.
- `tiered` keeps high accuracy at `N=8` (`0.977`) and low propagation (`0.023`), but it does so by escalating to raw almost all the time (`0.973` raw escalation).
- `scale_aware_unified` is the cleanest tradeoff inside the synthetic sweep. At `N=8`, it reaches `0.985` accuracy with `0.015` propagation and `0.600` raw escalation.
- `utility_calibrated` and `scale_aware_unified` are effectively tied on the high-`N` synthetic frontier: both reach `0.985` accuracy, `0.015` propagation, `0.067` benign overcompression, and about `3.6` mean cost at `N=8`.

### Real-Model Recall Slice: `actual_recall_expansion`

- At `N=8`, `summary_only` is weak: `0.208` accuracy and `0.500` propagation.
- `tiered` improves that to `0.792` accuracy but pays `0.750` raw escalation.
- `scale_aware_unified` reaches `0.875` accuracy with `0.125` propagation and lower raw escalation (`0.583`) than `tiered`.
- The important weakness is that `history_loss_rate` remains `0.875` for all methods at `N=8`. This suggests the remaining failure is upstream evidence loss, not just final answer routing.

### Real-Model Hallucination Stress: `actual_hallucination_stress`

- By `N=8`, the stronger methods all reach `1.000` accuracy with `0.000` propagation.
- The distinction is how much raw escalation and false-present behavior they need to get there.
- At `N=1`, `tiered` has `1.000` false-present and `1.000` raw escalation, while `scale_aware_note_aware` cuts both to `0.062`.
- At `N>=4`, the note-aware and unified variants close this stress slice cleanly without the heavy raw dependence seen in plain `tiered`.

### Benchmark Hallucination Section: `hallucination_benchmark_section`

- `summary_only` is still poor on the grounded hallucination family: at `N=1`, accuracy is only `0.156` and propagation is `0.844`.
- By `N=8`, `summary_only` improves to `0.719`, but it is still meaningfully behind the stronger methods.
- `tiered`, `scale_aware_unified`, and `scale_aware_note_aware` all reach `1.000` accuracy at `N=8`.
- The real separator is false-present / raw behavior: plain `tiered` stays at `1.000` false-present and `1.000` raw escalation, while `scale_aware_unified` drops to `0.156` and `scale_aware_note_aware` drops further to `0.094`.

### Benchmark Benign Utility Section: `benign_utility_benchmark_section`

- This is where the repo still looks least paper-ready.
- At `N=8`, `summary_only` falls to `0.469` accuracy with `0.531` propagation.
- `tiered`, `scale_aware_unified`, and `scale_aware_note_aware` all improve to `0.906` accuracy and `0.094` propagation.
- But all of those stronger methods still keep `history_loss_rate = 0.438` and `raw_escalation_rate = 0.438` at `N=8`.
- So the repo has largely solved hallucination shielding faster than it has solved benign utility preservation.

### Manifest-Backed Conflict Extension: `conflict_manifest_backed_extension`

- This panel closes the old “conflict is only supporting evidence” gap.
- At `N=8`, `summary_only` drops to `0.125` accuracy with `1.000` conflict error and `0.875` history loss.
- `tiered`, `scale_aware_unified`, and `scale_aware_note_aware` all hold `1.000` accuracy with `0.000` conflict error.
- The cost is that conflict retention at high `N` still leans on raw fallback: `1.000` for `tiered` and `0.875` for the unified variants.

### Manifest-Backed Unsafe Extension: `unsafe_manifest_backed_extension`

- This panel closes the old “unsafe only appears in scaffold tuning rounds” gap.
- At `N=8`, all exposed methods keep `1.000` accuracy with `0.000` unsafe error on the frozen unsafe extension set.
- The carry-forward winner is now explicit rather than implicit: the panel is directly tied to the `tiny_carry_forward_scaffold` source result.

## What The Tables Mean Overall

- The current project already supports a coherent reviewer-facing claim: pure summary compression is not stable as memory depth increases, and a scale-aware guarded policy substantially improves the risk-utility tradeoff.
- The repo now supports a stronger second claim than before: this is not only a synthetic story anymore, because the main surface is benchmark-native, the benchmark reviewer section is frozen, and the missing `conflict` / `unsafe` families are now manifest-backed too.
- The most convincing positive result is that hallucination control transfers onto a grounded benchmark surface without needing the old all-raw `tiered` behavior.
- The clearest remaining weakness is not “the idea fails”; it is “benign recall and paper-scale breadth are still not strong enough for a full baseline section.”

## Next Actions That Matter Most

- Expand the benchmark reviewer section beyond `32` frozen items.
- Keep optimizing the benign utility path, especially the `history_loss_rate` bottleneck at higher `N`.
- Preserve the new task-extension, environment, and single-entry rebuild layers as we scale the external benchmark section up.
