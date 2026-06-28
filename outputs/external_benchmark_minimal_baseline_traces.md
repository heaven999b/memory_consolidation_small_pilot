# External Benchmark Minimal Baseline Traces

这些 trace 用来快速检查 frozen benchmark slice 是否真的进入了现有 compaction / detector stack。

## halumem_hallucination

### halumem_bench_01

- `summary_only`
  N=1: probe=-; compact=Susan Thomas; final=Susan Thomas; route=compact; raw=0; llm_cost=$0.0788
  N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.4792
- `tiered`
  N=1: probe=-; compact=Susan Thomas; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.0788
  N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.4792
- `scale_aware_unified`
  N=1: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_recover; raw=1; llm_cost=$0.0788
  N=8: probe=absent / 0.245; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.4792
- `scale_aware_note_aware`
  N=1: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0788
  N=8: probe=absent / 0.245; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.4792

### halumem_bench_02

- `summary_only`
  N=1: probe=-; compact=Betty Davis; final=Betty Davis; route=compact; raw=0; llm_cost=$0.0922
  N=8: probe=-; compact=Betty Davis; final=Betty Davis; route=compact; raw=0; llm_cost=$0.4878
- `tiered`
  N=1: probe=-; compact=Betty Davis; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.0922
  N=8: probe=-; compact=Betty Davis; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.4878
- `scale_aware_unified`
  N=1: probe=absent / 0.341; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0922
  N=8: probe=uncertain / 0.428; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; llm_cost=$0.4878
- `scale_aware_note_aware`
  N=1: probe=absent / 0.171; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0922
  N=8: probe=uncertain / 0.428; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; llm_cost=$0.4878

## locomo_benign_utility

### locomo_bench_01

- `summary_only`
  N=1: probe=-; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.0370
  N=8: probe=-; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.2415
- `tiered`
  N=1: probe=-; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.0370
  N=8: probe=-; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.2415
- `scale_aware_unified`
  N=1: probe=uncertain / 0.576; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.0370
  N=8: probe=present / 0.696; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.2415
- `scale_aware_note_aware`
  N=1: probe=uncertain / 0.616; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.0370
  N=8: probe=present / 0.736; compact=Adoption agencies; final=Adoption agencies; route=compact; raw=0; llm_cost=$0.2415

### locomo_bench_02

- `summary_only`
  N=1: probe=-; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$0.0469
  N=8: probe=-; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$1.1458
- `tiered`
  N=1: probe=-; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$0.0469
  N=8: probe=-; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$1.1458
- `scale_aware_unified`
  N=1: probe=uncertain / 0.637; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$0.0469
  N=8: probe=present / 0.816; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$1.1458
- `scale_aware_note_aware`
  N=1: probe=uncertain / 0.677; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$0.0469
  N=8: probe=present / 0.816; compact=28 January 2023; final=28 January 2023; route=compact; raw=0; llm_cost=$1.1458

