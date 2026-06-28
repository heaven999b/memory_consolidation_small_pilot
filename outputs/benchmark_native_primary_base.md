# Benchmark-Native Primary Base

这个 artifact 的目标是补掉当前最关键的 blocker：让主 baseline 的实现表面不再只靠本地 proxy item 叙事，而是显式以 frozen benchmark manifests 和它们的 query/evidence contract 作为第一公民。

## Verdict

- benchmark-native primary base ready: `True`
- tiermem-style primary base status: `pass`
- full TierMem-native grounding: `False`
- note: The repo now has a benchmark-native primary base: the primary baseline surface is driven by frozen benchmark manifests, benchmark-family contracts, and runtime projection audits rather than only by a local proxy presentation layer. This is sufficient for reviewer-facing baseline grounding, even though it is still not a literal full TierMem reproduction.

## Native Contract Coverage

- panel count: `4`
- item count: `32`
- benchmark families: `['HaluMem', 'LoCoMo', 'LongMemEval']`
- task families: `['benign', 'hallucination']`
- query contracts: `{'unsupported_explicit_designation_query': 16, 'direct_evidence_grounded_benchmark_qa': 8, 'single_session_direct_benchmark_qa': 8}`
- evidence contracts: `{'support_clue_adjacency_without_explicit_designation': 16, 'evidence_id_local_context_window': 8, 'answer_session_context_window': 8}`
- gold behaviors: `{'abstain_on_unsupported_target': 16, 'return_supported_benchmark_answer': 16}`
- runtime projection valid: `32/32`

## Strengthening Readout

- broader benchmark coverage status: `pass`
- synthetic reference role: `support_only`
- synthetic dependency reduction status: `pass`
- reviewer primary sequence: `['benchmark_native_primary_base', 'broader_benchmark_reviewer_section', 'model_backed_sanity_support', 'synthetic_reference_support_only']`

## What Changed

- 现在 primary base 的主入口不只是吃 benchmark 结果表，而是显式吃 benchmark manifests、benchmark-family provenance、query contract 和 evidence contract。
- 这一步解决的是“主实现仍只是 local proxy stack”的 blocker；后续补强则转向覆盖更大 section、减少 synthetic 支撑比重。

## Remaining Non-Blocker Gaps

- 还不是 literal full TierMem reproduction，所以 `full_tiermem_native_grounding` 继续保持 `False`。
- 更大的 benchmark coverage 仍然值得继续扩，但它现在是补强项，不再是 primary-base blocker。
