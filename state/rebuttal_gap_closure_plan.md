# Rebuttal Gap Closure Plan

This note maps the current repo state against the A/B/C concerns raised after the finished expanded benchmark `main` run.

## A-tier

- `A1` Official public memory-system baselines:
  current status: not yet run
  repo progress: official HaluMem wrappers are already vendored under `benchmarks/halumem/official_repo/eval`, and readiness is now tracked by `run_halumem_official_baseline_matrix.py`
- `A2` Multi-backbone robustness:
  current status: not yet run
  repo progress: summarizer backend is no longer hard-wired to DeepSeek only; `deepseek_memory_summarizer.py` now supports `MEMORY_SUMMARIZER_BACKEND=openai_compatible` as a second execution path
- `A3` Real conflict / unsafe scale:
  current status: still underpowered
  current frozen task-extension size: `conflict=4`, `unsafe=2`
  implication: these families cannot stay as top-line claims without real scale-up

## B-tier

- `B4` Cost as first-class axis:
  delivered artifact: `outputs/expanded_benchmark_stage_main_cost_pareto.{json,md}`
- `B5` Probe sensitivity curve:
  delivered artifact: `outputs/expanded_benchmark_stage_main_probe_sweep.{json,md}`
  limitation: `history_loss` is compaction-side in this repo and therefore invariant under a pure route-threshold sweep
- `B6` Main-level significance testing:
  delivered artifact: `outputs/expanded_benchmark_stage_main_significance.{json,md}`
- `B7` Human audit of automatic metrics:
  current status: not yet done

## C-tier

- `C8` failure taxonomy: not yet done
- `C9` data-seed vs model-sampling variance disentanglement: not yet done
- `C10` repeated-update conflict stress: not yet done

## Suggested order

1. Run the new `B4/B5/B6` artifacts and fold their conclusions into the paper packet.
2. Use `run_halumem_official_baseline_matrix.py` to close `A1` readiness gaps and execute at least two official systems.
3. Launch a backbone matrix once a second and third summarizer backend are configured.
4. Either scale `conflict/unsafe` into real benchmark-sized tables or reduce their prominence in the paper claim set.
