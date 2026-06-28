# Repo Review And Table Analysis

## Current Snapshot

- Repo status: clean local checkout on `main`, already bound to the private GitHub repo.
- Release version: `v0.2.0-idea-baseline-private`
- Baseline gate: `minimal_closed_loop_baseline_ready = true`
- Paper gate: `paper_level_baseline_ready = false`
- Current external benchmark surface: `32` frozen items, `4` panels, `3` benchmark families, `2` task families

## Remaining Problems

### 1. Paper-facing benchmark scale is still too small

- The broader reviewer-facing benchmark section is still only `32` frozen items.
- This is enough for reviewer-credible idea reporting, but still thin for a paper-facing baseline section.
- The repo itself already admits this in `paper_level_baseline_ready = false`.

### 2. Benchmark-native grounding still covers only two task families

- The benchmark-native primary base currently covers `benign` and `hallucination`.
- It does not yet ground `conflict` or `unsafe` behavior on an equally strong benchmark-native surface.
- That means the main external evidence is strongest for abstention and benign QA, but weaker for update-conflict and safety-style claims.

### 3. Reproducibility environment is not pinned yet

- The repo does not currently ship a `requirements.txt`, `pyproject.toml`, or `environment.yml`.
- The mirrored benchmark code imports non-stdlib dependencies such as `openai`, `pandas`, `sqlalchemy`, `requests`, `tenacity`, `tqdm`, and `transformers`.
- The current snapshot is reproducible for local continuation in the existing machine context, but not yet one-command reproducible for another machine.

### 4. Full release regeneration is still fragmented

- There are many `run_*.py` and `verify_*.py` scripts, but no single release entrypoint that rebuilds the full reviewer packet from scratch.
- This is workable for active research iteration, but it creates handoff friction when someone else wants to re-run the exact release boundary.

### 5. The benign utility bottleneck is still the main empirical weakness

- On the broader benchmark benign section at `N=8`, stronger methods improve accuracy a lot, but `history_loss_rate` still stays at `0.438`.
- This means the repo is no longer mainly blocked by hallucination control alone; the harder remaining problem is preserving useful benign detail under compression without paying too much raw fallback.

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

## What The Tables Mean Overall

- The current project already supports a coherent reviewer-facing claim: pure summary compression is not stable as memory depth increases, and a scale-aware guarded policy substantially improves the risk-utility tradeoff.
- The repo also now supports a stronger second claim: this is not only a synthetic story anymore, because the main surface is benchmark-native and the benchmark reviewer section is already frozen and auditable.
- The most convincing positive result is that hallucination control now transfers onto a grounded benchmark surface without needing the old all-raw `tiered` behavior.
- The clearest remaining weakness is not “the idea fails”; it is “benign recall and paper-scale breadth are still not strong enough for a full baseline section.”

## Next Actions That Matter Most

- Expand the benchmark reviewer section beyond `32` frozen items.
- Add benchmark-native coverage for `conflict` and `unsafe` style behavior, not just `benign` and `hallucination`.
- Add a pinned environment file and one-command release rebuild path.
- Keep optimizing the benign utility path, especially the `history_loss_rate` bottleneck at higher `N`.
