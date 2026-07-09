# V2 Mac Feasibility Report

Date: 2026-06-30

This report answers one narrow question: under the current **V2-first** priority, what can be done on this Mac right now, what can be done after local setup, and what is still blocked?

## Executive summary

The good news is that the project is now much closer to a real V2 path than before:

1. the **real TierMem upstream repo is cloned locally** at `/Users/yihaiwen/Documents/New project/tiermem_upstream`;
2. the local repo already has strong benchmark mirrors for **LoCoMo** and **LongMemEval**;
3. TierMem's embedded `mem0 -> qdrant` stack supports a **local path mode**, so a minimal Mac baseline does **not** strictly require Docker;
4. a dedicated local environment has now been created at:
   - `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/.venv_tiermem_v2`
5. the minimum critical runtime packages for a bridge run are now installed there:
   - `openai`
   - `qdrant-client`
   - `json-repair`
   - `tiktoken`

The main blockers are now concrete engineering blockers, not paper-level ambiguity:

1. the wrong Python interpreter is selected when commands are run from inside `tiermem_upstream`;
2. `OPENAI_API_KEY` is not set;
3. the final `HaluMem-Medium.jsonl` file required by the TierMem HaluMem loader is **not** mirrored locally;
4. optional packages for stronger variants are still absent, but they no longer block the smallest bridge run.

## What is already doable on this Mac

These items are already completed or directly runnable after the changes made in this round:

1. **Static V2 feasibility audit of the real TierMem codebase**
   - confirmed real TierMem runner, dataset loaders, linked-view system, mem0 stack, and Qdrant config paths.
2. **Local benchmark inventory**
   - LoCoMo local mirror exists:
     - `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/benchmarks/locomo/locomo_official/data/locomo10.json`
   - LongMemEval-S cleaned local mirror exists:
     - `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/benchmarks/locomo/longmemeval_official/data/cleaned/longmemeval_s_cleaned.json`
   - HaluMem construction-stage files exist, but the final TierMem-ready medium file is missing.
3. **A real TierMem bridge entrypoint has been added**
   - script:
     - [run_v2_tiermem_local_bridge.py](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/run_v2_tiermem_local_bridge.py)
   - this script:
     - imports the actual TierMem upstream stack;
     - rewires TierMem dataset loaders to use local benchmark mirrors;
     - uses **local-path Qdrant mode** instead of assuming a remote Qdrant server;
     - redirects `mem0` local state into the project outputs tree instead of relying on `~/.mem0`;
     - forces the LongMemEval bridge path onto the built-in char-count fallback instead of first-run `tiktoken` network fetches;
     - performs readiness checks before a run.
4. **A dedicated local runtime has been created and verified**
   - environment:
     - `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/.venv_tiermem_v2`
   - verified installed modules in that environment:
     - `openai`
     - `qdrant_client`
     - `json_repair`
     - `tiktoken`

## What can be done after local setup

These are feasible on this Mac, but not yet runnable in the current environment:

1. **LoCoMo minimal TierMem sanity run**
   - now blocked only by `OPENAI_API_KEY`.
2. **LongMemEval minimal TierMem sanity run**
   - now blocked only by `OPENAI_API_KEY`.
3. **HaluMem TierMem sanity run**
   - after `OPENAI_API_KEY` is set and the missing final dataset file is added:
     - expected default path:
       `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl`
4. **V2-first raw-only / summary-only / TierMem-style comparison scaffold**
   - now that a real TierMem bridge exists, this can be built on top of actual TierMem rather than the previous pure proxy surface.

## What is blocked right now

### 1. Interpreter mismatch

The machine resolves `python3` differently depending on the working directory:

1. from the workspace root, `python3` points to:
   - `/opt/anaconda3/bin/python3`
2. from inside `tiermem_upstream`, `python3` points to:
   - `/opt/homebrew/opt/python@3.14/bin/python3.14`

This matters because the Homebrew 3.14 interpreter is much less prepared for this project. For example, TierMem entry scripts failed there immediately on `tqdm`.

### 2. Minimum package blocker has been cleared

The smallest bridge run originally failed because the active environment lacked:

1. `openai`
2. `qdrant_client`
3. `json_repair`
4. `tiktoken`

Those were the original minimum blockers. They are now installed inside:

1. `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/.venv_tiermem_v2`

So package installation is no longer the main blocker for the smallest bridge run.

### 3. Missing required environment variable

The current shell environment still does not expose:

1. `OPENAI_API_KEY`

It also does not expose:

1. `OPENAI_BASE_URL`
2. `OPENAI_MODEL`
3. `QDRANT_HOST`
4. `QDRANT_PORT`

The last two are less important now because the new bridge uses local-path Qdrant mode.

### 4. HaluMem final file is missing

TierMem's HaluMem loader expects a final medium file like:

1. `./data/HaluMem/halumem_raw/HaluMem-Medium.jsonl`

But the local benchmark mirror currently contains stage-construction files rather than that final TierMem-ready dataset file. So a true HaluMem V2 run is still blocked by data availability.

### 5. Optional modules for stronger variants are still absent

The following packages are still missing in the bridge environment:

1. `sentence_transformers`
2. `fastembed`
3. `tantivy`

This matters for richer retrieval / embedding variants, but it does **not** block the smallest LoCoMo or LongMemEval bridge readiness anymore.

### 6. Upstream runner does not expose HaluMem directly in its main CLI

TierMem upstream includes `core/datasets/halumem.py`, but its generic benchmark CLI currently exposes:

1. `locomo`
2. `longmemeval`
3. `memory_agent_bench`
4. `hotpotqa`

The new local bridge script closes that gap on our side, but this is still an upstream limitation worth remembering.

## What is probably not a good fit for this Mac

These are not the next thing to do locally:

1. **GPU-heavy reranker experiments**
   - upstream notes already mark reranker mode as GPU-oriented.
2. **Router training / deepspeed / bitsandbytes style work**
   - possible in principle elsewhere, but not the right baseline path for this Mac.
3. **Large vLLM serving stacks**
   - not needed for the minimal V2 baseline and likely too heavy for this machine-first workflow.

## Recommended next move

The next concrete move should be:

1. use the prepared environment:
   - `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/.venv_tiermem_v2/bin/python`
2. set `OPENAI_API_KEY`;
3. run:
   - `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/.venv_tiermem_v2/bin/python /Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/run_v2_tiermem_local_bridge.py --check-only --benchmark locomo`
4. then run a tiny sanity pass:
   - `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/.venv_tiermem_v2/bin/python /Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/run_v2_tiermem_local_bridge.py --benchmark locomo --limit 2`

After that, the next strongest target is LongMemEval. HaluMem remains the key V2 benchmark, but it still needs the final medium dataset file before a true TierMem run is possible.
