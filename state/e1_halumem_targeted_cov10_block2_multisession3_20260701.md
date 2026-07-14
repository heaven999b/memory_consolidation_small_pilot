# E1 Block 2: HaluMem multi-session depth sweep (2026-07-01)

## Scope

- Benchmark: `HaluMem-Medium`
- Sessions: `3`
- QA per session: `15`
- Route: `summary_only`
- Consolidation: `targeted` (`qa_retrieved_pages`, warmup `top-k=10`)
- Depths: `N={0,1,2,4}`

Primary artifacts:

- Sweep report (JSON): `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/sweep_reports/e1_halumem_targeted_cov10_multisession3_fix_20260701.json`
- Sweep report (MD): `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/sweep_reports/e1_halumem_targeted_cov10_multisession3_fix_20260701.md`
- Judge report (valid, network rerun JSON): `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_multisession3_fix_20260701_judge_net.json`
- Judge report (valid, network rerun MD): `/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_multisession3_fix_20260701_judge_net.md`

## Core table

| N | summary_F1 | judge_correct | abstain_forgetting_on_factual | unsupported_fabrication_on_unknown | fact_distortion_on_factual | overlap_on_QA_pages | total_latency_sec | total_api_calls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.185 | 0.333 | 0.394 | 0.333 | 0.394 | 0.000 | 227.1 | 492 |
| 1 | 0.210 | 0.533 | 0.364 | 0.083 | 0.242 | 0.722 | 743.9 | 1069 |
| 2 | 0.215 | 0.422 | 0.455 | 0.083 | 0.303 | 0.681 | 1090.3 | 1199 |
| 4 | 0.206 | 0.489 | 0.303 | 0.083 | 0.364 | 0.701 | 2029.7 | 1459 |

Denominators from the judge:

- factual questions: `33`
- unknown / abstain questions: `12`

## Main read

1. The cleanest multi-session signal is still `N=0 -> N=1`.
   - `unsupported_fabrication_on_unknown` drops from `0.333` to `0.083`.
   - `fact_distortion_on_factual` drops from `0.394` to `0.242`.
   - judge-level correctness rises from `0.333` to `0.533`.

2. The single-session "N=1 peak, N=2 crash" weakens under 3 sessions, but the post-`N=1` degradation story survives on failure modes.
   - `summary_F1` does **not** form a sharp inverted-U: `0.185 -> 0.210 -> 0.215 -> 0.206`.
   - judge correctness **does** peak at `N=1`: `0.333 -> 0.533 -> 0.422 -> 0.489`.
   - `N=2` is the clearest regression point on factual retention:
     - `abstain_forgetting_on_factual`: `0.364 -> 0.455`
     - `fact_distortion_on_factual`: `0.242 -> 0.303`

3. Deep compression no longer reintroduces unsupported fabrication, but it keeps redistributing factual failure modes.
   - `unsupported_fabrication_on_unknown` stays flat at `0.083` for `N=1/2/4`.
   - `N=4` does not undo the denoising benefit on unknown-answer questions.
   - `N=4` still shows elevated factual distortion (`0.364`) with a large cost jump.

4. Retrieval mismatch is not the main explanation for the `N>=2` drop.
   - overlap on QA pages is stable once consolidation is enabled:
     - `N=1`: `0.722`
     - `N=2`: `0.681`
     - `N=4`: `0.701`
   - This supports the interpretation that the main regression is from memory transformation, not page-target mismatch.

## Concrete examples that match the story

- `N=0 -> N=1` repair:
  - `Did Martin Mark work as a nurse at Huaxin Consulting on Sep 06, 2025?`
    - `N=0`: abstains
    - `N=1`: correct `director`

- `N=1 -> N=2` degradation:
  - `Did Martin Mark mention a preference for reptiles as pets on Sep 07, 2025?`
    - `N=1`: correct
    - `N=2`: abstain forgetting

- Deep-pass factual drift:
  - `Did Martin Mark establish a global health initiative with his partner in 2025?`
    - `N=4`: adds a wrong `2035` launch timeline and distorts the partner frame

## Cost read

- The cost curve is steep even with targeted consolidation:
  - `N=0`: `227s`
  - `N=1`: `744s`
  - `N=2`: `1090s`
  - `N=4`: `2030s`

- This is enough for Block 2, but it keeps `N=8` expensive unless we accept long wall-clock time or optimize consolidation further.

## Caveats

1. BM25 is still unavailable (`pyserini` missing), so all runs are under summary-first fallback.
2. This is targeted consolidation, not full-page consolidation; conclusions apply to the targeted setting we actually ran.
3. The first local judge attempt failed due sandbox DNS / connection issues and produced all-`ERROR` labels.
   - Use the `_judge_net` report above as the valid artifact.

## Bottom line

- Multi-session Block 2 **does support** the claim that the strongest benefit is at `N=1`.
- What survives most clearly is **failure-mode migration**, not a clean utility inverted-U.
- Best current wording:
  - consolidation sharply reduces unsupported fabrication at `N=1`;
  - deeper passes do not bring fabrication back, but they start trading the gain for more factual abstention / distortion at higher cost.
