# Expanded Benchmark Stage Traces: large

这些 trace 用来快速确认 staged run 里的每个 expanded panel 真的进入了同一套 compaction stack。

## halumem_expanded_v1

### halumem_expanded_01

- `summary_only`
  N=1: probe=-; compact=Susan Thomas; final=Susan Thomas; route=compact; raw=0; llm_cost=$0.0486
  N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.3703

- `tiered`
  N=1: probe=-; compact=Susan Thomas; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.0486
  N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.3703

- `scale_aware_unified`
  N=1: probe=uncertain / 0.509; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_recover; raw=1; llm_cost=$0.0486
  N=8: probe=absent / 0.288; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.3703

- `scale_aware_note_aware`
  N=1: probe=uncertain / 0.509; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_recover; raw=1; llm_cost=$0.0486
  N=8: probe=absent / 0.288; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.3703

- `psu`
  N=1: probe=absent / 0.289; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; carry=0; llm_cost=$0.0700
  N=8: probe=absent / 0.288; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3747

## locomo_expanded_v1

### locomo_expanded_001

- `summary_only`
  N=1: probe=-; compact=3; final=3; route=compact; raw=0; llm_cost=$0.0362
  N=8: probe=-; compact=3; final=3; route=compact; raw=0; llm_cost=$0.3636

- `tiered`
  N=1: probe=-; compact=3; final=3; route=compact; raw=0; llm_cost=$0.0362
  N=8: probe=-; compact=3; final=3; route=compact; raw=0; llm_cost=$0.3636

- `scale_aware_unified`
  N=1: probe=present / 0.778; compact=3; final=3; route=compact; raw=0; llm_cost=$0.0362
  N=8: probe=uncertain / 0.575; compact=3; final=3; route=compact; raw=0; llm_cost=$0.3636

- `scale_aware_note_aware`
  N=1: probe=present / 0.818; compact=3; final=3; route=compact; raw=0; llm_cost=$0.0362
  N=8: probe=uncertain / 0.615; compact=3; final=3; route=compact; raw=0; llm_cost=$0.3636

- `psu`
  N=1: probe=present / 0.818; compact=3; final=3; route=compact; raw=0; carry=0; llm_cost=$0.0536
  N=8: probe=uncertain / 0.615; compact=3; final=3; route=compact; raw=0; carry=1; llm_cost=$0.3419

### locomo_expanded_003

- `summary_only`
  N=1: probe=-; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.0462
  N=8: probe=-; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.4476

- `tiered`
  N=1: probe=-; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.0462
  N=8: probe=-; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.4476

- `scale_aware_unified`
  N=1: probe=present / 0.772; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.0462
  N=8: probe=uncertain / 0.598; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.4476

- `scale_aware_note_aware`
  N=1: probe=present / 0.812; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.0462
  N=8: probe=uncertain / 0.638; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; llm_cost=$0.4476

- `psu`
  N=1: probe=present / 0.812; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; carry=0; llm_cost=$0.0434
  N=8: probe=uncertain / 0.638; compact=19 October 2023; final=19 October 2023; route=compact; raw=0; carry=1; llm_cost=$0.3672

### locomo_expanded_004

- `summary_only`
  N=1: probe=-; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.1041
  N=8: probe=-; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.4586

- `tiered`
  N=1: probe=-; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.1041
  N=8: probe=-; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.4586

- `scale_aware_unified`
  N=1: probe=present / 0.783; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.1041
  N=8: probe=uncertain / 0.610; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.4586

- `scale_aware_note_aware`
  N=1: probe=present / 0.823; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.1041
  N=8: probe=uncertain / 0.650; compact=sunset; final=sunset; route=compact; raw=0; llm_cost=$0.4586

- `psu`
  N=1: probe=present / 0.823; compact=sunset; final=sunset; route=compact; raw=0; carry=0; llm_cost=$0.0356
  N=8: probe=uncertain / 0.650; compact=sunset; final=sunset; route=compact; raw=0; carry=3; llm_cost=$0.2478

## longmemeval_expanded_v2

### longmemeval_expanded_001

- `summary_only`
  N=1: probe=-; compact=38 subjects; final=38 subjects; route=compact; raw=0; llm_cost=$0.0384
  N=8: probe=-; compact=No relevant information available in source material; final=No relevant information available in source material; route=compact; raw=0; llm_cost=$0.3214

- `tiered`
  N=1: probe=-; compact=38 subjects; final=38 subjects; route=compact; raw=0; llm_cost=$0.0384
  N=8: probe=-; compact=No relevant information available in source material; final=38 subjects; route=raw_fallback; raw=1; llm_cost=$0.3214

- `scale_aware_unified`
  N=1: probe=present / 0.795; compact=38 subjects; final=38 subjects; route=compact; raw=0; llm_cost=$0.0384
  N=8: probe=present / 0.703; compact=ABSTAIN; final=38 subjects; route=utility_calibrated_recover; raw=1; llm_cost=$0.3214

- `scale_aware_note_aware`
  N=1: probe=present / 0.835; compact=38 subjects; final=38 subjects; route=compact; raw=0; llm_cost=$0.0384
  N=8: probe=present / 0.703; compact=ABSTAIN; final=38 subjects; route=utility_calibrated_recover; raw=1; llm_cost=$0.3214

- `psu`
  N=1: probe=present / 0.835; compact=38 subjects; final=38 subjects; route=compact; raw=0; carry=0; llm_cost=$0.0342
  N=8: probe=present / 0.813; compact=38 subjects; final=38 subjects; route=compact; raw=0; carry=0; llm_cost=$0.3507

### longmemeval_expanded_013

- `summary_only`
  N=1: probe=-; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.0567
  N=8: probe=-; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.3562

- `tiered`
  N=1: probe=-; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.0567
  N=8: probe=-; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.3562

- `scale_aware_unified`
  N=1: probe=present / 0.716; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.0567
  N=8: probe=uncertain / 0.634; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.3562

- `scale_aware_note_aware`
  N=1: probe=present / 0.756; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.0567
  N=8: probe=uncertain / 0.674; compact=Luna; final=Luna; route=compact; raw=0; llm_cost=$0.3562

- `psu`
  N=1: probe=present / 0.756; compact=Luna; final=Luna; route=compact; raw=0; carry=0; llm_cost=$0.0389
  N=8: probe=uncertain / 0.674; compact=Luna; final=Luna; route=compact; raw=0; carry=1; llm_cost=$0.3242

