# Week 1 Delivery Status

Date: 2026-07-02

This document maps the Week 1 goals from the research plan onto the current implementation.

## Week 1 Target

From the Week 1 timeline in the refined research plan:

- fork TierMem and build the common memory API
- finalize the artifact schema
- run `raw_only`, `summary_only`, and TierMem-style `summary_plus_raw`
- use a tiny synthetic set
- cover `N=0` and `N=1`

## Delivered

### 1. Common Week 1 architecture surface

- [week1_surface.py](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/week1_surface.py:1)
- [run_v2_tiermem_local_bridge.py](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/run_v2_tiermem_local_bridge.py:1)
- [run_v2_tiermem_micro_slice.py](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/run_v2_tiermem_micro_slice.py:1)

Pinned presets:

- `raw_only` -> `research_only` + `raw`
- `summary_only` -> `summary_only` + `infer`
- `summary_plus_raw` -> `auto` + `infer`

### 2. Tiny synthetic benchmark path

- dataset: [week1_tiny_synth.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/benchmarks/tiny_synth/data/week1_tiny_synth.json:1)
- upstream loader: [tiny_synth.py](/Users/yihaiwen/Documents/New project/tiermem_upstream/core/datasets/tiny_synth.py:1)

The tiny dataset includes:

- direct fact recall
- correction / update recall
- two sessions with three QA items each

### 3. Pinned Week 1 configs

- [raw_only.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/week1/raw_only.json:1)
- [summary_only.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/week1/summary_only.json:1)
- [summary_plus_raw.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/week1/summary_plus_raw.json:1)

All three configs pin:

- benchmark = `tiny_synth`
- session-limit = `2`
- qa-limit = `3`
- consolidation passes = `[0, 1]`
- page size = `4000`

### 4. Artifact schema

- schema doc: [week1_artifact_schema.md](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/docs/week1_artifact_schema.md:1)
- machine schemas:
  - [memory_write_record.schema.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/configs/schemas/week1/memory_write_record.schema.json:1)
  - [qa_record.schema.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/configs/schemas/week1/qa_record.schema.json:1)
  - [summary.schema.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/configs/schemas/week1/summary.schema.json:1)

### 5. One-command Week 1 sanity runner

- [run_week1_tiermem_sanity.py](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/run_week1_tiermem_sanity.py:1)

Modes:

- `plan`
- `pre_api_smoke`
- `run`

The runner now auto-loads `.env.v3` and `.env`, so `--mode run` works even when `OPENAI_API_KEY` is not exported in the parent shell.

## Verification

### Static checks

Verified by local compile / JSON load checks on the new Week 1 files.

### Pre-API smoke

Current matrix:

- [week1_sanity_matrix.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/week1_sanity/week1_sanity_matrix.json:1)
- [week1_sanity_matrix.md](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/week1_sanity/week1_sanity_matrix.md:1)

`pre_api_smoke` passed for:

- `raw_only`, `N=0`
- `raw_only`, `N=1`
- `summary_only`, `N=0`
- `summary_only`, `N=1`
- `summary_plus_raw`, `N=0`
- `summary_plus_raw`, `N=1`

This verifies that the Week 1 benchmark, loader, presets, Qdrant path, and TierMem bridge are wired correctly.

## Live Run Status

The full Week 1 live matrix is launched through:

```bash
cd /Users/yihaiwen/Documents/New\ project/memory_consolidation_small_pilot
python3 run_week1_tiermem_sanity.py --mode run
```

Status at the time of writing:

- runner entry is fixed and recognizes `.env.v3`
- live execution starts successfully
- the first online `raw_only` run is materially slower than smoke and should be treated as a real online cost check, not an interface failure

## Week 1 Verdict

From an implementation standpoint, Week 1 is in place:

1. TierMem fork integration exists.
2. The common Week 1 API surface exists.
3. The tiny synthetic benchmark exists and is routable.
4. The artifact schema is frozen.
5. The sanity runner exists and passes `pre_api_smoke` across all required architecture and depth combinations.

The remaining runtime validation is the full live matrix over the tiny synthetic set.
