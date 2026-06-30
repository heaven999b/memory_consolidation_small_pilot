# V3 Official Eval Runtime Audit

Scaffold/runtime audit for the mirrored HaluMem official evaluation path, excluding live API execution.

- status: `partial`
- official eval venv present: `False`
- ready runtime count: `1`
- base requirements present: `True`
- HaluMem expected dataset present: `True`
- HaluMem expected dataset path: `benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl`

## Env Templates

- .env.v3.example: `True`
- .env.official_eval.example: `True`
- benchmarks/halumem/official_repo/eval/.env-example: `True`

## Runtime Matrix

| Runtime | Exists | Common Missing | Mem0 Missing | Zep Missing | MemOS Missing |
|---|---|---|---|---|---|
| `current_python` | `True` | openai, dotenv, tenacity, tqdm, requests | mem0 | zep_cloud | none |
| `tiermem_venv` | `True` | none | mem0 | zep_cloud | none |
| `official_eval_venv` | `False` | openai, dotenv, tenacity, tqdm, requests | mem0 | zep_cloud | none |

## Next Commands

- `python3 -m venv .venv_official_eval`
- `.venv_official_eval/bin/pip install -r requirements-official-eval-base.txt`
- `Populate .env.official_eval using the chosen system's keys and endpoints.`
- `Install the selected system SDK after choosing a concrete baseline (for example, Mem0 or Zep).`
