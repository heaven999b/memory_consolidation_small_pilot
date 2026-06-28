# External Benchmark Adapter Layer

这个 artifact 现在已经不只是 adapter contract 了：一条 HaluMem-style hallucination slice 和一条 LoCoMo/LongMemEval-style benign-utility slice 都已经以 frozen manifest 的形式落在本地，所以 external benchmark grounding 至少已经推进到 slice-ready。

- grounding_status: `pass`
- adapters: `2`
- source_manifest_count: `2`
- data_ready_count: `2`
- slice_ready_count: `2`
- reviewer_section_ready: `True`

## halumem_hallucination_slice

- benchmark_family: `HaluMem-style`
- task_type: `hallucination_risk`
- adapter_state: `slice_ready`
- source_manifest_path: `benchmarks/halumem/SOURCE_MANIFEST.json`
- source_manifest_present: `True`
- local_source_globs: `benchmarks/halumem/official_repo/**/*`
- local_match_count: `31`
- frozen_slice_manifest_glob: `benchmarks/halumem/frozen_slices/*.json`
- slice_manifest_count: `3`
- frozen_target_size: `8`
- target_metrics: `false_present_rate, direct_unsupported_answer_rate, raw_escalation_rate`

## locomo_benign_utility_slice

- benchmark_family: `LoCoMo/LongMemEval-style`
- task_type: `benign_utility`
- adapter_state: `slice_ready`
- source_manifest_path: `benchmarks/locomo/SOURCE_MANIFEST.json`
- source_manifest_present: `True`
- local_source_globs: `benchmarks/locomo/locomo_official/**/*; benchmarks/locomo/longmemeval_official/README.md; benchmarks/locomo/longmemeval_official/LICENSE; benchmarks/locomo/longmemeval_official/custom_history/*.py; benchmarks/locomo/longmemeval_official/data/cleaned/longmemeval_oracle.json; benchmarks/locomo/longmemeval_official/data/cleaned/longmemeval_s_cleaned.json`
- local_match_count: `10`
- frozen_slice_manifest_glob: `benchmarks/locomo/frozen_slices/*.json`
- slice_manifest_count: `3`
- frozen_target_size: `8`
- target_metrics: `accuracy, history_loss_rate, empty_note_then_abstain_rate, raw_escalation_rate`

## Next Requirements

- replace the remaining local proxy-stack internals behind the benchmark-first primary surface so TierMem-style grounding can move from partial to pass
- carry the broader reviewer-facing benchmark section into more slice families and larger frozen coverage
- keep reducing how much the reviewer-facing story depends on synthetic reference artifacts rather than benchmark-native sections
