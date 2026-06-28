# Reproducibility

## Pinned Environment

- Python environment: [environment.yml](./environment.yml)
- Optional pip-only dependency pinning: [requirements.txt](./requirements.txt)

## Non-Python Requirement

- The model-backed rebuild path expects the `deepseek` CLI to be installed and authenticated because the local summarizer wrapper shells out to that binary.
- If the local output caches already exist, the rebuild can reuse them without issuing fresh model calls.

## Single-Entry Rebuild

Run the full reviewer-facing rebuild with:

```bash
python3 run_release_rebuild.py
```

Skip the verifier layer with:

```bash
python3 run_release_rebuild.py --skip-verify
```

The rebuild script pins the current release seeds internally:

- `ACTUAL_RECALL_EXPANSION_SEEDS=11,23`
- `ACTUAL_HALLU_STRESS_SEEDS=11,23`

## What The Rebuild Covers

- frozen task-extension manifests
- actual recall / hallucination / carry-forward supporting outputs
- external benchmark adapter / minimal panel / reviewer section
- task-extension section
- benchmark-native primary base
- benchmark-first proxy base
- tiermem-style primary surface
- paper baseline packet
- verification artifacts for the task extensions, native primary base, and paper packet
