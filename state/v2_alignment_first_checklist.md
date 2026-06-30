# V2-First Alignment Checklist

Date: 2026-06-30

This note resets the project priority to **align with `01_original_plan_v2.pdf` first**, before escalating to the stricter `v3` paperization path.

## Why reset to V2 first

The user's decision is:

- first align the current repo with the original `v2` plan,
- complete the concrete `v2` implementation path,
- only then decide whether to tighten toward `v3`.

This means we should **not** treat `v3`-only requirements as the first blocker if they were not already required by `v2`.

## What V2 actually requires

From `01_original_plan_v2.pdf`, the non-negotiable core is:

1. **TierMem is the primary implementation base.**
2. `Language Models Need Sleep` is motivation only, not the engineering base.
3. **HaluMem is the main hallucination benchmark.**
4. **LongMemEval + LoCoMo are the benign utility checks.**
5. **AgentPoison + MPBench/MemEvoBench-style attacks define the safety suite.**
6. The first real pilot should run:
   - TierMem sanity
   - `C^N` over the summary tier
   - `N in {0,1,2,4,8}` first
   - HaluMem-Medium
   - a small AgentPoison/custom poisoning overlay
7. The main contrast is:
   - `raw-only`
   - `summary-only`
   - `TierMem-style summary-plus-raw escalation`

## What the current repo already satisfies for V2

These parts are already useful and should be kept:

1. Official benchmark grounding is largely in place:
   - HaluMem local mirror / eval helpers
   - LongMemEval local mirror / cleaned subsets
   - LoCoMo local mirror / frozen subsets
2. The repo already has benchmark-facing staged evaluation infrastructure.
3. Artifact / trace / monitor / per-item logging infrastructure is already strong enough to reuse.
4. The repo already has a usable local notion of:
   - `summary-only`
   - stronger routed variants
   - propagation-style metrics
5. The repo already contains a provenance-oriented reporting layer, even if not TierMem-native.

## What is still not V2-aligned

These are the true V2 gaps that should be treated as first priority:

1. **TierMem upstream is now cloned locally, but not yet integrated or run through the repo pipeline.**
   - Local path: `../tiermem_upstream`
   - This removes the "repo not present" blocker, but the project is still not TierMem-based in execution.
2. The current implementation is still a **local proxy stack**, not a TierMem-based harness.
3. The current main benchmark surface is built around local architectures:
   - `summary_only`
   - `tiered`
   - `scale_aware_unified`
   - `scale_aware_note_aware`
   - `psu`
   rather than the `raw-only / summary-only / TierMem-style` V2 contrast.
4. The current expanded benchmark run uses only **N = {1,8}**, while V2 wants `{0,1,2,4,8}` first.
5. There is no completed V2-style **AgentPoison/custom poisoning overlay pilot** yet.
6. There is no clean V2 pilot table that jointly reports:
   - hallucination risk
   - unsafe retention
   - benign QA utility
   - token/latency cost

## What we should do next under V2-first priority

### Immediate task order

1. **Week-0 V2 feasibility check**
   - run a real TierMem benchmark sanity pass from the newly cloned upstream repo
   - verify that raw store / summary path / routing / outputs are executable, not just present in code
2. **Build the V2 base harness**
   - adapt existing benchmark loaders to a real TierMem adapter
   - preserve raw store / summary tier / escalation logs
3. **Restore the V2 pilot comparison**
   - `raw-only`
   - `summary-only`
   - `TierMem-style summary-plus-raw escalation`
4. **Restore the V2 pilot N schedule**
   - start with `N in {0,1,2,4,8}`
5. **Run the V2 benchmark order**
   - TierMem sanity
   - HaluMem-Medium
   - LongMemEval-S / LoCoMo small utility checks
   - small AgentPoison/custom poisoning overlay
6. **Produce one V2 pilot table**
   - hallucination
   - unsafe retention
   - benign utility
   - cost

### Things that can wait until after V2 alignment

These may still matter later, but they are **not the first-order blocker** if we are explicitly following V2 first:

1. real public memory-system baselines such as Mem0 / Zep / MemoryOS
2. multi-backbone robustness
3. human-validated judge agreement
4. stricter V3-only milestone gating
5. full V3 novelty framing around the narrower safety-critical-field contribution

## Working interpretation

The correct reading is:

- the current repo is **not yet V2-aligned**, because it is still not TierMem-based;
- but it already contains a lot of reusable infrastructure for reaching V2 faster;
- therefore the next move is **not** "throw everything away and jump to v3",
- the next move is **use the current repo as a migration source and complete the V2 base path first**.
