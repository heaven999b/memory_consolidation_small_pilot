# Verification Round 33 Primary Surface

这个文件只做机械核对：确认 repo 现在确实有一个 benchmark-first 的 primary surface，而不是继续只靠 packet 文字说明。

- [PASS] Primary surface is explicitly marked benchmark-first ready: observed status block = `{'benchmark_first_surface_ready': True, 'tiermem_style_primary_base_status': 'partial', 'full_tiermem_native_grounding': False, 'note': 'The repo now exposes a benchmark-first primary surface with real frozen HaluMem and LoCoMo panels, but the implementation underneath is still a local proxy-stack partial rather than a full TierMem-native benchmark base.'}`.
- [PASS] TierMem-style primary base is honestly marked partial rather than pass: observed primary-base status = `partial`.
- [PASS] Full TierMem-native grounding remains explicitly false: observed full-native flag = `False`.
- [PASS] Reviewer sequence starts from the benchmark-grounded core: observed reviewer sequence = `['Start with the benchmark-grounded core panel rather than the synthetic proxy trio.', 'Use the model-backed sanity slices as realism support for answerability-loss and hallucination-side behavior.', 'Treat the synthetic core panel as a control-plane reference, not the primary source of evidence.']`.
- [PASS] Benchmark core exposes both HaluMem and LoCoMo panels: observed panel names = `['halumem_hallucination', 'locomo_benign_utility']`.
- [PASS] Benchmark core carries v2 frozen slice metadata: observed versions = `v2`, `v2`.
- [PASS] Benchmark core keeps all four architectures at N=8: observed HaluMem methods = `['scale_aware_note_aware', 'scale_aware_unified', 'summary_only', 'tiered']`.
- [PASS] Model-backed support layers are attached: observed support layers = `['actual_hallucination_stress', 'actual_recall_expansion']`.
- [PASS] Synthetic reference still exists but is no longer the only top-level surface: synthetic reference present = `True`.

## Bottom Line

如果这些检查通过，说明 repo 的主表面已经从“只有 proxy/pilot 叙事”前进到“benchmark-first 但仍诚实标注 partial”的状态，这比继续把 benchmark panel 藏在 packet 里更接近 reviewer 预期。
