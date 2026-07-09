# Verification Round 34 Primary Surface

这个文件只做机械核对：确认 repo 现在确实有一个 benchmark-first 的 primary surface，而不是继续只靠 packet 文字说明。

- [PASS] Primary surface is explicitly marked benchmark-first ready: observed status block = `{'benchmark_first_surface_ready': True, 'tiermem_style_primary_base_status': 'pass', 'full_tiermem_native_grounding': False, 'benchmark_source_kind': 'broader_reviewer_section', 'benchmark_first_entrypoint_path': 'run_benchmark_first_primary_entrypoint.py', 'benchmark_first_entrypoint_ready': True, 'benchmark_first_proxy_base_path': 'outputs/benchmark_first_proxy_base.json', 'benchmark_first_proxy_base_complete': True, 'benchmark_native_primary_base_path': 'outputs/benchmark_native_primary_base.json', 'benchmark_native_primary_base_ready': True, 'benchmark_native_primary_base_status': 'pass', 'exact_non_proxy_frontier_ready': True, 'note': 'The repo now exposes a benchmark-native primary base over frozen benchmark manifests, so the reviewer-facing primary baseline is no longer just a local proxy surface; the remaining gap is that this is still not a literal full TierMem reproduction or a final large-scale paper section.'}`.
- [PASS] TierMem-style primary base is now marked pass: observed primary-base status = `pass`.
- [PASS] Full TierMem-native grounding remains explicitly false: observed full-native flag = `False`.
- [PASS] Reviewer sequence starts from the benchmark-native primary base: observed reviewer sequence = `['Start with the benchmark-native primary base rather than the synthetic proxy trio.', 'Use the model-backed sanity slices as realism support for answerability-loss and hallucination-side behavior.', 'Treat the synthetic core panel as a control-plane reference, not the primary source of evidence.']`.
- [PASS] Benchmark core now uses the broader reviewer section rather than the minimal starter panel: observed source kind = `broader_reviewer_section`.
- [PASS] Benchmark core exposes both broader family rollups: observed panel names = `['benign_utility_benchmark_section', 'hallucination_benchmark_section']`.
- [PASS] Benchmark core references four slice panels behind the family rollups: observed slice panel names = `['halumem_core_v2', 'halumem_holdout_v1', 'locomo_core_v2', 'longmemeval_direct_v1']`.
- [PASS] Benchmark core keeps 16-item family rollups on both sides: observed counts = `16`, `16`.
- [PASS] Benchmark core keeps all four architectures at N=8: observed HaluMem methods = `['scale_aware_note_aware', 'scale_aware_unified', 'summary_only', 'tiered']`.
- [PASS] Benchmark-first entrypoint is explicitly surfaced and marked ready: observed entrypoint = `run_benchmark_first_primary_entrypoint.py`, ready = `True`.
- [PASS] Primary surface now explicitly marks the benchmark-first proxy base complete: observed proxy-base path = `outputs/benchmark_first_proxy_base.json`, complete = `True`.
- [PASS] Primary surface explicitly marks the benchmark-native primary base ready: observed native-base path = `outputs/benchmark_native_primary_base.json`, ready = `True`, status = `pass`.
- [PASS] Primary surface explicitly marks the frontier as proxy-free: observed exact-frontier flag = `True`.
- [PASS] Model-backed support layers are attached: observed support layers = `['actual_hallucination_stress', 'actual_recall_expansion']`.
- [PASS] Synthetic reference still exists but is no longer the only top-level surface: synthetic reference present = `True`.

## Bottom Line

如果这些检查通过，说明 repo 的主表面已经不只是 minimal starter panel，也不再只是 proxy-first surface，而是升级成了 benchmark-native primary base；同时它仍然诚实地区分了“baseline 已过”和“还没到最终 paper 版本”。
