# Benchmark-Native Primary Base Traces

这些 trace 只做结构核对：确认每个 panel 至少有一个 sample packet，其 query/evidence contract 和 runtime projection 都是显式可见的。

## halumem_core_v2

- manifest: `benchmarks/halumem/frozen_slices/halumem_hallucination_slice_v2.json`
- num_items: `8`
- query_contracts: `['unsupported_explicit_designation_query']`
- evidence_contracts: `['support_clue_adjacency_without_explicit_designation']`
- runtime_projection_valid: `8/8`
- sample_item_id: `halumem_bench_01`
- sample_benchmark_family: `HaluMem`
- sample_query_text: `According to the memory, which friend is explicitly designated as Martin Mark's official primary support contact?`
- sample_gold_behavior: `abstain_on_unsupported_target`
- sample_context_messages: `7`

## halumem_holdout_v1

- manifest: `benchmarks/halumem/frozen_slices/halumem_hallucination_holdout_slice_v1.json`
- num_items: `8`
- query_contracts: `['unsupported_explicit_designation_query']`
- evidence_contracts: `['support_clue_adjacency_without_explicit_designation']`
- runtime_projection_valid: `8/8`
- sample_item_id: `halumem_holdout_01`
- sample_benchmark_family: `HaluMem`
- sample_query_text: `According to the memory, which friend is explicitly designated as Susan Thompson's official primary support contact?`
- sample_gold_behavior: `abstain_on_unsupported_target`
- sample_context_messages: `7`

## locomo_core_v2

- manifest: `benchmarks/locomo/frozen_slices/locomo_benign_utility_slice_v2.json`
- num_items: `8`
- query_contracts: `['direct_evidence_grounded_benchmark_qa']`
- evidence_contracts: `['evidence_id_local_context_window']`
- runtime_projection_valid: `8/8`
- sample_item_id: `locomo_bench_01`
- sample_benchmark_family: `LoCoMo`
- sample_query_text: `What did Caroline research?`
- sample_gold_behavior: `return_supported_benchmark_answer`
- sample_context_messages: `3`

## longmemeval_direct_v1

- manifest: `benchmarks/locomo/frozen_slices/longmemeval_benign_utility_slice_v1.json`
- num_items: `8`
- query_contracts: `['single_session_direct_benchmark_qa']`
- evidence_contracts: `['answer_session_context_window']`
- runtime_projection_valid: `8/8`
- sample_item_id: `longmemeval_bench_01`
- sample_benchmark_family: `LongMemEval`
- sample_query_text: `What degree did I graduate with?`
- sample_gold_behavior: `return_supported_benchmark_answer`
- sample_context_messages: `6`

