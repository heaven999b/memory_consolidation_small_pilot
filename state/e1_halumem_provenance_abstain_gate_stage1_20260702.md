# E1 Stage 1: Provenance Abstain Gate (2026-07-02)

## Scope

- Benchmark: `HaluMem-Medium`
- Slice: `1 session x 15 QA`
- Route: `auto`
- Depth: `N=1`
- Goal: test whether a conservative provenance-based abstention gate can reduce `unsupported_fabrication` on unknown questions without raising `abstain_forgetting` on factual questions

## Code status

- Current code uses the tightened `gate_v2` form:
  - narrower unsupported markers
  - do not override already-polar answers that begin with `yes` or `no`
- CLI plumbing is wired through:
  - `run_v2_tiermem_local_bridge.py`
  - `run_v2_tiermem_micro_slice.py`
  - `run_v2_tiermem_micro_n_sweep.py`

## Artifacts

- Baseline auto N=1 judge:
  - `outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_auto_s1_iter3_fixauto_20260701_judge_relaxed_net.json`
- Gate v1 run:
  - `outputs/v2_tiermem_micro/micro_reports/e1_halumem_targeted_cov10_auto_s1_n1_abstain_20260702.json`
- Gate v1 judge:
  - `outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_auto_s1_n1_abstain_20260702_judge_relaxed_net.json`
- Gate v2 run:
  - `outputs/v2_tiermem_micro/micro_reports/e1_halumem_targeted_cov10_auto_s1_n1_abstainv2_20260702.json`
- Gate v2 judge:
  - `outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_auto_s1_n1_abstainv2_20260702_judge_relaxed_net.json`

## Result table

| condition | summary F1 | correct | AF on factual | UF on unknown | FD on factual |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline auto N=1 | 0.194 | 0.533 | 0.000 | 0.667 | 0.333 |
| gate v1 | 0.205 | 0.533 | 0.333 | 0.333 | 0.222 |
| gate v2 | 0.228 | 0.533 | 0.000 | 0.667 | 0.333 |

## Read

1. `gate_v1` proved the mechanism can suppress unsupported fabrication.
   - `UF` dropped from `4/6` to `2/6`.
   - But it was too aggressive and converted three factual negation questions into abstentions.

2. The `gate_v1` failure mode was traceable, not mysterious.
   - It fired on coverage strings such as:
     - `No evidence suggests he worked as a nurse ...`
     - `there is no information ... with his partner in 2025`
   - These phrases are compatible with supported negation, so the original marker list was too broad.

3. `gate_v2` fixed the over-abstention problem but lost the UF gain.
   - `AF` returned to `0.000`.
   - `UF` reverted to the baseline `0.667`.
   - In this rerun, the gate fired only once, on the unknown Golden Retriever friend-name question.

4. Current Stage 1 verdict: `not passed`.
   - The provenance abstain gate is not yet delivering the intended RQ3 trade in this slice.
   - `gate_v1` shows the direction is plausible.
   - `gate_v2` shows the current heuristic is too weak once made safe.

## Why v2 still missed unknowns

- Some missed unknown cases had coverage text that did not hit the tightened markers.
  - Example: middle-name answers hallucinated `Mark` again.
- One missed unknown case came from a bad coverage assessment itself.
  - The salary question claimed salary was fully covered, so the gate had no unsupported signal to consume.

## Immediate implication

- The current gate should be treated as an exploratory ablation, not a validated defense.
- If we continue this line, the next lever is likely a better unsupported detector than raw substring matching:
  - sentence-level classification over `coverage_assessment`
  - or a separate cheap judge for `supported / unsupported / supported-negation`
