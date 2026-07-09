# Verification Round 32 Benchmark

这个文件只做机械核对：确认 frozen external benchmark slice 不只是存在，而且真的被跑成了 reviewer-facing panel。

- [PASS] Benchmark verdict is explicitly ready: observed verdict = `{'minimal_benchmark_grounded_panel_ready': True, 'note': 'Both frozen external benchmark slices were executed through the model-backed compaction stack and produced reviewer-facing benchmark-grounded panel rows.'}`.
- [PASS] HaluMem slice ids match the frozen manifest: observed ids = `['halumem_bench_01', 'halumem_bench_02', 'halumem_bench_03', 'halumem_bench_04', 'halumem_bench_05', 'halumem_bench_06', 'halumem_bench_07', 'halumem_bench_08']`.
- [PASS] LoCoMo slice ids match the frozen manifest: observed ids = `['locomo_bench_01', 'locomo_bench_02', 'locomo_bench_03', 'locomo_bench_04', 'locomo_bench_05', 'locomo_bench_06', 'locomo_bench_07', 'locomo_bench_08']`.
- [PASS] Both panels keep the expected item count: observed counts = `HaluMem 8`, `LoCoMo 8`.
- [PASS] All four architectures are present in both benchmark panels: observed HaluMem methods = `['scale_aware_note_aware', 'scale_aware_unified', 'summary_only', 'tiered']`.
- [PASS] Each panel exposes the expected N grid: observed N keys = `['1', '4', '8']`.
- [PASS] HaluMem panel reports hallucination-side metrics: observed keys = `['accuracy', 'benign_overcompression_rate', 'by_family', 'cleaned_bad_memory_rate', 'conflict_answer_rate', 'conflict_merge_rate', 'count', 'direct_unsupported_answer_rate', 'false_present_rate', 'latent_bad_memory_rate', 'mean_cost', 'mean_llm_cost_usd', 'propagation_rate', 'raw_escalation_rate', 'residual_bad_memory_rate', 'shielded_bad_memory_rate', 'tentative_guess_note_rate', 'unsafe_answer_rate', 'unsafe_retention_rate', 'unsupported_answer_rate', 'unsupported_new_memory_rate']`.
- [PASS] LoCoMo panel reports answerability-loss metrics: observed keys = `['accuracy', 'benign_conflict_error_rate', 'benign_overcompression_rate', 'by_family', 'cleaned_bad_memory_rate', 'conflict_answer_rate', 'conflict_merge_rate', 'count', 'empty_note_rate', 'empty_note_then_abstain_rate', 'history_loss_rate', 'latent_bad_memory_rate', 'mean_cost', 'mean_llm_cost_usd', 'policy_overrefusal_rate', 'propagation_rate', 'raw_escalation_rate', 'residual_bad_memory_rate', 'shielded_bad_memory_rate', 'unsafe_answer_rate', 'unsafe_retention_rate', 'unsupported_answer_rate', 'unsupported_new_memory_rate']`.

## Bottom Line

如果这些检查通过，说明 external benchmark 这一层已经不是只有 adapter contract，而是已经变成真正可运行、可核对的最小 benchmark-grounded baseline panel。
