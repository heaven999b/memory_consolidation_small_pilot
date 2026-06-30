# Expanded Benchmark Dataset Inventory

这个 artifact 记录下一阶段 official benchmark pool 的规模、来源、验证状态，以及它相对当前 reviewer section 的扩张幅度。

- panel_count: `3`
- total_items: `159`
- benchmark_family_counts: `{'HaluMem': 19, 'LoCoMo': 80, 'LongMemEval': 60}`
- task_family_counts: `{'benign': 140, 'hallucination': 19}`
- runtime_projection_valid: `159/159`
- reviewer_section_size: `32`
- scale_delta: `127`
- scale_multiplier: `4.969`

## Panels

| Panel | Manifest Version | Items | Family | Runtime Projection |
|---|---:|---:|---|---:|
| halumem_expanded_v1 | v1 | 19 | HaluMem / hallucination | 19/19 |
| locomo_expanded_v1 | v1 | 80 | LoCoMo / benign | 80/80 |
| longmemeval_expanded_v2 | v2 | 60 | LongMemEval / benign | 60/60 |

## Panel Details

### halumem_expanded_v1

- manifest_path: `benchmarks/halumem/frozen_slices/halumem_hallucination_expanded_v1.json`
- adapter_id: `halumem_hallucination_expanded_slice`
- selection_policy: `{'target_size': 19, 'source_type': 'official_hallucination_benchmark_record', 'rule': 'Keep every official HaluMem persona whose top support clues contain three clean full-name relationship anchors, then preserve the same unsupported explicit-designation query used by the benchmark-core slice.'}`
- extra: `{'unique_source_indexes': 19, 'source_index_span': [0, 19]}`
- runtime_projection_errors: `[]`

### locomo_expanded_v1

- manifest_path: `benchmarks/locomo/frozen_slices/locomo_benign_utility_expanded_v1.json`
- adapter_id: `locomo_benign_utility_expanded_slice`
- selection_policy: `{'target_size': 80, 'source_type': 'official_benign_qa_benchmark_record', 'rule': 'For each LoCoMo conversation, keep four clean category-1 direct factual QA items and four clean category-2 explicit date/time QA items with valid evidence ids, short answers, and low normalization burden.', 'per_sample_category_quota': 4}`
- extra: `{'sample_counts': {'conv-26': 8, 'conv-30': 8, 'conv-41': 8, 'conv-42': 8, 'conv-43': 8, 'conv-44': 8, 'conv-47': 8, 'conv-48': 8, 'conv-49': 8, 'conv-50': 8}, 'category_counts': {'1': 40, '2': 40}}`
- runtime_projection_errors: `[]`

### longmemeval_expanded_v2

- manifest_path: `benchmarks/locomo/frozen_slices/longmemeval_benign_utility_expanded_v2.json`
- adapter_id: `longmemeval_benign_utility_expanded_slice`
- selection_policy: `{'target_size': 60, 'source_type': 'official_benign_qa_benchmark_record', 'rule': 'Keep clean LongMemEval single-session rows with exactly one answer-bearing session id, short direct answers, and a tight answer-session context window; allocate 48 user-facing items plus 12 assistant-facing items for coverage diversity without shifting to multi-session reasoning.', 'single_session_user_target': 48, 'single_session_assistant_target': 12}`
- extra: `{'question_type_counts': {'single-session-assistant': 12, 'single-session-user': 48}}`
- runtime_projection_errors: `[]`

## Readout

- The large official pool is now almost five times the current 32-item reviewer section, while still fitting the same benchmark-native packet schema used by the current baseline surface.
- HaluMem is close to full verified-local coverage, LoCoMo is balanced across all 10 conversations, and LongMemEval is widened into a real second benign benchmark family rather than a small add-on.
- This does not yet mean the full large benchmark baseline has been run, but it removes the main dataset-construction blocker for that next stage.
