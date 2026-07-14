# E1 Stage 1: Structured Grounding Abstain Gate (2026-07-02)

## Scope

- Benchmark: `HaluMem-Medium`
- Slice: `1 session x 15 QA`
- Route: `auto`
- Depth: `N=1`
- Comparison:
  - same prompt version, no gate
  - same prompt version, `abstain_on_unsupported=true`

## Code

- Prompt field added in:
  - `tiermem_upstream/src/linked_view/prompts.py`
- Integration parsing + R-path gate wiring in:
  - `tiermem_upstream/src/memory/linked_view_system.py`

The gate now consumes `answer_grounded: true|false` from the integration LLM output instead of substring heuristics over `coverage_assessment`.

## Artifacts

- No-gate run:
  - `outputs/v2_tiermem_micro/micro_reports/e1_halumem_targeted_cov10_auto_s1_n1_structsig_base_20260702.json`
- Gate run:
  - `outputs/v2_tiermem_micro/micro_reports/e1_halumem_targeted_cov10_auto_s1_n1_structsig_gate_20260702.json`
- Combined judge:
  - `outputs/v2_tiermem_micro/judge_reports/e1_halumem_targeted_cov10_auto_s1_n1_structsig_compare_20260702_judge_relaxed_net.json`

## Core result

| condition | summary F1 | correct | AF on factual | UF on unknown | FD on factual |
| --- | ---: | ---: | ---: | ---: | ---: |
| no gate | 0.258 | 0.467 | 0.000 | 0.833 | 0.333 |
| structured gate | 0.262 | 0.733 | 0.000 | 0.167 | 0.333 |

## Gate behavior

- No-gate run:
  - `answer_grounded=false` appeared on `4` questions, but no abstention was applied.
- Gate run:
  - `answer_grounded=false` appeared on `5` questions
  - `abstain_gate_fired=5`
  - the gate-fired items were all unknown / abstain-style questions:
    - three middle-name questions
    - the Golden Retriever friend-name question
    - the blood-type question

## Read

1. Stage 1 passes.
   - `UF` dropped from `5/6` to `1/6`
   - `AF` stayed at `0/9`

2. This is materially stronger than the earlier substring gate attempts.
   - The v1 substring gate reduced fabrication but incorrectly abstained on supported negation.
   - The structured `answer_grounded` field preserved negation handling while still suppressing unsupported guessing.

3. The remaining missed unknown is informative.
   - Salary still fabricated in the gated run.
   - That means the integration step incorrectly judged that salary was grounded, so the bottleneck is now the LLM detector itself, not the gate wiring.

## Decision

- Proceed to the next stage.
- This version satisfies the stop/go rule for the 1-session validation slice:
  - `UF` down
  - `AF` not up

## Next move

- Expand to multi-session validation before further gate tweaking.
- The remaining question is not "does the mechanism work at all?" anymore.
- The remaining question is "does the gain survive beyond 15 QA / 1 session?"
