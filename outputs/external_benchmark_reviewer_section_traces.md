# External Benchmark Reviewer Section Traces

这些 trace 用来快速确认 reviewer section 里的新增 slices 也真的进入了同一套 compaction stack。

## halumem_core_v2

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

## halumem_holdout_v1

### halumem_holdout_01

- `summary_only`
  N=1: probe=-; compact=Linda Martinez; final=Linda Martinez; route=compact; raw=0; llm_cost=$0.1056
  N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.2757

- `tiered`
  N=1: probe=-; compact=Linda Martinez; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.1056
  N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.2757

- `scale_aware_unified`
  N=1: probe=uncertain / 0.423; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_recover; raw=1; llm_cost=$0.1056
  N=8: probe=absent / 0.233; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2757

- `scale_aware_note_aware`
  N=1: probe=absent / 0.253; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.1056
  N=8: probe=absent / 0.233; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2757

## locomo_core_v2

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

## longmemeval_direct_v1

### longmemeval_bench_01

- `summary_only`
  N=1: probe=-; compact=Business Administration; final=Business Administration; route=compact; raw=0; llm_cost=$0.0421
  N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.2321

- `tiered`
  N=1: probe=-; compact=Business Administration; final=Business Administration; route=compact; raw=0; llm_cost=$0.0421
  N=8: probe=-; compact=ABSTAIN; final=Business Administration; route=raw_fallback; raw=1; llm_cost=$0.2321

- `scale_aware_unified`
  N=1: probe=uncertain / 0.611; compact=Business Administration; final=Business Administration; route=compact; raw=0; llm_cost=$0.0421
  N=8: probe=present / 0.731; compact=ABSTAIN; final=Business Administration; route=utility_calibrated_recover; raw=1; llm_cost=$0.2321

- `scale_aware_note_aware`
  N=1: probe=uncertain / 0.651; compact=Business Administration; final=Business Administration; route=compact; raw=0; llm_cost=$0.0421
  N=8: probe=present / 0.731; compact=ABSTAIN; final=Business Administration; route=utility_calibrated_recover; raw=1; llm_cost=$0.2321

