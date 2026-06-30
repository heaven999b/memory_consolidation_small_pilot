# Reproducibility

This repo now has **two reproducibility surfaces**:

1. the **legacy pilot rebuild**
2. the **V3 transition rebuild**

They serve different purposes.

## Pinned Python Environments

- baseline repo environment:
  - [environment.yml](./environment.yml)
  - [requirements.txt](./requirements.txt)
- TierMem bridge environment:
  - `.venv_tiermem_v2/`
- official HaluMem eval scaffold:
  - `.env.official_eval.example`
  - `requirements-official-eval-base.txt`
  - optional runtime target: `.venv_official_eval/`

## Legacy Pilot Rebuild

This is the older reviewer-facing packet rebuild.

Run:

```bash
python3 run_release_rebuild.py
```

Skip verifiers:

```bash
python3 run_release_rebuild.py --skip-verify
```

This path still assumes the older model-backed local stack and may depend on the local `deepseek` CLI being installed and authenticated.

## V3 Transition Rebuild

This is the new V3 status refresh entrypoint.

Run:

```bash
python3 run_v3_transition_rebuild.py
```

It refreshes:

- `feasibility_report.md`
- `outputs/v3_feasibility_gate.json`
- `outputs/v3_halumem_dataset_preflight.{json,md}`
- `outputs/v3_public_baseline_readiness.{json,md}`
- `outputs/v3_official_eval_runtime_audit.{json,md}`
- `outputs/v3_no_rewrite_policy_audit.{json,md}`
- `outputs/v3_no_rewrite_comparison.{json,md}`
- `outputs/v3_no_rewrite_statistics.{json,md}`
- `outputs/v3_no_rewrite_surface_audit.{json,md}`
- `outputs/v3_no_rewrite_pareto.{json,md}`
- `outputs/v3_hygiene_audit.{json,md}`
- `outputs/v3_local_capability_matrix.{json,md}`
- `outputs/v3_local_evidence_packet.{json,md}`
- `outputs/v3_transition_status.{json,md}`
- `state/v3_transition_snapshot.json`

## Real TierMem Bridge Checks

Use the dedicated TierMem environment:

```bash
.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --check-only --benchmark locomo
```

Pre-API smoke:

```bash
.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --pre-api-smoke --benchmark locomo
```

Tiny real sanity run:

```bash
.venv_tiermem_v2/bin/python run_v2_tiermem_local_bridge.py --benchmark locomo --limit 2
```

This real bridge path still requires a valid `OPENAI_API_KEY`.

Until that real bridge path succeeds, the `v3_no_rewrite_*` artifacts remain synthetic dry-run scaffolds rather than real benchmark evidence.

## Official Eval Scaffold

Before any live public-baseline run, prepare:

```bash
cp .env.official_eval.example .env.official_eval
python3 run_v3_halumem_dataset_preflight.py
python3 run_v3_official_eval_runtime_audit.py
```

If you want a dedicated runtime later:

```bash
python3 -m venv .venv_official_eval
.venv_official_eval/bin/pip install -r requirements-official-eval-base.txt
```
