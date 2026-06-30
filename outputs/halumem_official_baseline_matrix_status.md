# HaluMem Official Baseline Matrix Status

This artifact turns A1 into an explicit execution surface: which official memory systems are wired in, what each one requires, and whether the current environment is ready to run them.

- eval_dir: `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/benchmarks/halumem/official_repo/eval`

| System | Ready | Missing env | Missing packages | Script | Notes |
|---|---|---|---|---|---|
| memzero | False | MEM0_API_KEY, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, RETRY_TIMES, WAIT_TIME_LOWER, WAIT_TIME_UPPER | mem0, openai | eval_memzero.py | Single-stage run; then score with evaluation.py --frame memzero. |
| zep | False | ZEP_API_KEY, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, RETRY_TIMES, WAIT_TIME_LOWER, WAIT_TIME_UPPER | zep_cloud, openai | eval_zep.py | Two-stage run: first add, then search, then score with evaluation.py --frame zep. |
| memos | False | MEMOS_URL, MEMOS_KEY, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, RETRY_TIMES, WAIT_TIME_LOWER, WAIT_TIME_UPPER | openai | eval_memos.py | Single-stage run; then score with evaluation.py --frame memos. |

## Recommendation

- The next A1 step is to fill the missing env / package gaps for at least `memzero` and one of `zep` or `memos`, then run the official wrappers and score them through `evaluation.py`.
- This repo now has a single status surface for that work instead of relying on manual README interpretation.
