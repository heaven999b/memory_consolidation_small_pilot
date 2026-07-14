# E1 Block A+B: Summary vs Auto vs Research (2026-07-01)

## Scope

- Benchmark: `HaluMem-Medium`
- Sessions: `1`
- QA per session: `15`
- Depths compared here: `N={0,1,2}`
- Routes:
  - `summary_only` targeted baseline from Block 1
  - `auto` after the research-integration robustness fix
  - `research_only` with `max_research_iters=3`

## Primary artifacts

- Summary baseline judge JSON:
  `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_depth_20260701_judge_relaxed_net.json`
- Auto sweep JSON:
  `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/sweep_reports/e1_halumem_targeted_cov10_auto_s1_iter3_fixauto_20260701.json`
- Auto judge JSON:
  `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_auto_s1_iter3_fixauto_20260701_judge_relaxed_net.json`
- Research sweep JSON:
  `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/sweep_reports/e1_halumem_targeted_cov10_research_s1_iter3_fixauto_20260701.json`
- Research judge JSON:
  `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_research_s1_iter3_fixauto_20260701_judge_relaxed_net.json`

## Core table

| Route | N | F1 | Correct | Abstain Forgetting (factual) | Unsupported Fabrication (unknown) | Fact Distortion (factual) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| summary_only | 0 | 0.205 | 0.600 | 0.333 | 0.333 | 0.111 |
| summary_only | 1 | 0.205 | 0.667 | 0.333 | 0.167 | 0.111 |
| summary_only | 2 | 0.189 | 0.533 | 0.444 | 0.167 | 0.222 |
| auto | 0 | 0.225 | 0.733 | 0.000 | 0.333 | 0.222 |
| auto | 1 | 0.194 | 0.533 | 0.000 | 0.667 | 0.333 |
| auto | 2 | 0.241 | 0.600 | 0.000 | 0.667 | 0.222 |
| research_only | 0 | 0.266 | 0.733 | 0.000 | 0.333 | 0.222 |
| research_only | 1 | 0.188 | 0.533 | 0.000 | 0.833 | 0.222 |
| research_only | 2 | 0.148 | 0.400 | 0.111 | 0.833 | 0.333 |

Judge denominators:

- factual questions: `9`
- unknown / abstain questions: `6`

## Route behavior

- `auto` is not acting like a real hybrid gate yet.
  - `N=0`: `15/15` queries routed to `R`
  - `N=1`: `13/15` routed to `R`, `2/15` to `S`
  - `N=2`: `14/15` routed to `R`, `1/15` to `S`
- In this session, `auto` behaves much more like a mostly-research route than a selective escalation policy.

## Decision

Block A does **not** pass the intended RQ3 gate.

- The hoped-for story was:
  - keep `unsupported_fabrication` close to summary
  - keep forgetting / factual loss close to research
- What actually happened:
  - `auto` at `N=1/2` sharply worsened `unsupported_fabrication` to `4/6`
  - `research_only` at `N=1/2` was even worse on `unsupported_fabrication` at `5/6`
  - neither `auto` nor `research_only` produced a cleaner defended curve than `summary_only`

Short version: the current gate does **not** combine the best of summary and research.

## Main read

1. Engineering result: the fix worked.
   - Both `auto` and `research_only` now complete clean `N={0,1,2}` sweeps.
   - Dirty `linked_facts` payloads are repaired or partially skipped instead of crashing `_research_integration_v2`.

2. Scientific result: raw escalation does not rescue deeper compression in this slice.
   - `research_only` shows a clean decline: `F1 0.266 -> 0.188 -> 0.148`
   - judge correctness also declines: `0.733 -> 0.533 -> 0.400`
   - `unsupported_fabrication_on_unknown` worsens from `0.333` at `N=0` to `0.833` at `N=1/2`

3. `auto` is better read as “R-heavy noisy hybrid” than as a genuine gate.
   - It inherits the same fabrication problem once consolidation turns on:
     - `UF`: `0.333 -> 0.667 -> 0.667`
   - `N=2` recovers some utility (`F1 0.241`) relative to `N=1`, but not because it became safer.
   - Its failure mix remains dominated by fabrication + distortion, not by the summary route's abstention pattern.

4. The strongest defended setting in this 1-session comparison is still `summary_only, N=1`.
   - It keeps `UF` at `1/6`
   - It keeps `FD` at `1/9`
   - It has the best judge correctness among the actually defended (`N>0`) routes: `0.667`

## Retrieval / targeting read

- Targeted consolidation overlap stayed stable for the routes that used it:
  - `auto N=1`: `0.711`
  - `auto N=2`: `0.737`
  - `research_only N=1`: `0.725`
  - `research_only N=2`: `0.722`
- This makes “coverage collapse” a weak explanation for the route comparison.
- The bigger issue is failure-mode composition after route choice, not overlap drift.

## Cost read

- `auto`:
  - `N=0`: `475.6s`
  - `N=1`: `832.2s`
  - `N=2`: `806.6s`
- `research_only`:
  - `N=0`: `618.5s`
  - `N=1`: `521.7s`
  - `N=2`: `588.8s`

The important point is not the exact ordering of wall-clock time. It is that both `auto` and `research_only` are now cheap enough to iterate on locally, so the blocker has shifted from “can it run?” to “does the route policy actually help?”

## Implications

1. Do **not** scale the current `auto` gate to 3 sessions yet.
   - The route policy is not delivering the intended safety/utility trade.

2. The current RQ3 answer is negative.
   - “Summary by default, escalate to raw when needed” is not yet validated in the present implementation.

3. The next design move should be stronger than brute-force raw escalation.
   - This points toward the plan's stronger-defense branch (`E4`-style provenance / conservative defenses), not a simple “run more research_only”.

## Caveats

1. This is still only `1 session / 15 QA`.
2. BM25 is unavailable (`pyserini` missing), so all runs remain under the summary-first fallback retrieval regime.
3. The relaxed judge changed the interpretation of short, polarity-correct answers.
   - Compare against earlier pre-relaxed judge numbers only with care.
4. `auto` barely used `S` in this slice.
   - So this is evidence about the **current** gate implementation, not about the idealized gate concept.
