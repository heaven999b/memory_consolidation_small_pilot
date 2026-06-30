# V3 Public Baseline Readiness

Local readiness audit for the real public memory-system baselines demanded by V3.

- overall status: `partial`
- ready adapters: `0`
- partial adapters: `3`

| System | Frame | Status | Dataset | Best Runtime | Missing Env | Missing Imports |
|---|---|---|---|---|---|---|
| Mem0 | `memzero` | `partial` | `True` | `current_python` | MEM0_API_KEY, OPENAI_API_KEY | mem0, dotenv, tenacity, tqdm |
| Zep | `zep` | `partial` | `True` | `current_python` | ZEP_API_KEY, OPENAI_API_KEY | zep_cloud, dotenv, tenacity, tqdm |
| MemoryOS / MemOS | `memos` | `partial` | `True` | `current_python` | MEMOS_URL, MEMOS_KEY, OPENAI_API_KEY | requests, dotenv, tenacity, tqdm |

## Next Actions

- Mem0: script=`benchmarks/halumem/official_repo/eval/eval_memzero.py`; runtime=`current_python`; dataset_source=`https://huggingface.co/datasets/IAAR-Shanghai/HaluMem`; next=`python3 benchmarks/halumem/official_repo/eval/eval_memzero.py`; blocker=`missing env vars: ['MEM0_API_KEY', 'OPENAI_API_KEY']; missing imports in best local runtime (current_python): ['mem0', 'dotenv', 'tenacity', 'tqdm']`
- Zep: script=`benchmarks/halumem/official_repo/eval/eval_zep.py`; runtime=`current_python`; dataset_source=`https://huggingface.co/datasets/IAAR-Shanghai/HaluMem`; next=`python3 benchmarks/halumem/official_repo/eval/eval_zep.py`; blocker=`missing env vars: ['ZEP_API_KEY', 'OPENAI_API_KEY']; missing imports in best local runtime (current_python): ['zep_cloud', 'dotenv', 'tenacity', 'tqdm']`
- MemoryOS / MemOS: script=`benchmarks/halumem/official_repo/eval/eval_memos.py`; runtime=`current_python`; dataset_source=`https://huggingface.co/datasets/IAAR-Shanghai/HaluMem`; next=`python3 benchmarks/halumem/official_repo/eval/eval_memos.py`; blocker=`missing env vars: ['MEMOS_URL', 'MEMOS_KEY', 'OPENAI_API_KEY']; missing imports in best local runtime (current_python): ['requests', 'dotenv', 'tenacity', 'tqdm']`