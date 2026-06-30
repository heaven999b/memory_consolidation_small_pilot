# V3 Local Capability Matrix

Local capability matrix for what this Mac can execute now under the V3 migration plan.

- fully doable now: `8`
- partially doable now: `3`
- blocked locally: `1`

| Task | Can Do | Status | Blocker | Next Command |
|---|---|---|---|---|
| V3 transition rebuild | `yes` | `ready` | none | `python3 run_v3_transition_rebuild.py` |
| TierMem tiny sanity run | `partial` | `partial` | LoCoMo tiny sanity run is blocked only by OPENAI_API_KEY; LongMemEval tiny sanity run is blocked only by OPENAI_API_KEY | `.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --benchmark locomo --limit 2` |
| Official public baseline setup audit | `yes` | `partial` | none | `python3 run_v3_public_baseline_readiness.py` |
| HaluMem dataset preflight | `yes` | `partial` | canonical HaluMem-Medium.jsonl file is still missing | `python3 run_v3_halumem_dataset_preflight.py` |
| Official eval runtime scaffold | `yes` | `partial` | scaffold exists, but .venv_official_eval has not been created yet | `python3 run_v3_official_eval_runtime_audit.py` |
| Official public baseline live runs | `partial` | `partial` | Mem0: HaluMem-Medium.jsonl missing (official source: https://huggingface.co/datasets/IAAR-Shanghai/HaluMem); missing env vars: ['MEM0_API_KEY', 'OPENAI_API_KEY']; missing imports in best local runtime (current_python): ['mem0'] \| Zep: HaluMem-Medium.jsonl missing (official source: https://huggingface.co/datasets/IAAR-Shanghai/HaluMem); missing env vars: ['ZEP_API_KEY', 'OPENAI_API_KEY']; missing imports in best local runtime (current_python): ['zep_cloud'] \| MemOS: HaluMem-Medium.jsonl missing (official source: https://huggingface.co/datasets/IAAR-Shanghai/HaluMem); missing env vars: ['MEMOS_URL', 'MEMOS_KEY', 'OPENAI_API_KEY'] | `python3 benchmarks/halumem/official_repo/eval/eval_memzero.py` |
| Safety-critical no-rewrite dry-run audit | `yes` | `ready` | none | `python3 run_v3_no_rewrite_policy_audit.py` |
| Legacy support analyses for V3 appendix | `yes` | `ready` | none | `python3 run_expanded_benchmark_main_cost_pareto.py && python3 run_expanded_benchmark_main_probe_sweep.py && python3 run_expanded_benchmark_main_significance.py` |
| TierMem pre-API smoke | `yes` | `ready` | none | `.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --pre-api-smoke --benchmark locomo` |
| Legacy multi-backbone profile runs | `partial` | `partial` | configured profiles: gpt=False, qwen=False, llama=False; deepseek_cli=True | `python3 run_expanded_benchmark_backbone_profile.py main gpt_openai_profile` |
| AgentPoison attack suite grounding | `no` | `paper_only` | local AgentPoison artifacts are absent | `Clone AgentPoison before claiming the safety attack suite is executable.` |
| V3 defended-method maturity | `yes` | `partial` | local no-rewrite scaffold exists, but it is still a dry-run surface; current N=8 blocked protected rate = 0.9783 | `Wire the no-rewrite rule into the real TierMem path after the tiny bridge sanity run succeeds.` |