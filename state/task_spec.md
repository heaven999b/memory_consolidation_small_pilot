# Task Spec: Memory Consolidation Small Pilot

## Goal

Build a controlled pre-pilot that stress-tests the core claim behind the iterative memory consolidation project:

```text
summary-only memory gets riskier as consolidation depth N increases,
while raw-backed tiering can reduce propagation risk at an added cost.
```

## Scope

This task is deliberately pre-benchmark:

- synthetic, hand-authored items;
- rule-based stochastic compactor;
- a focused textual-proxy slice that is closer to free-text summarization than the claim-level proxy;
- a focused model-backed summarizer slice that uses the DeepSeek CLI on a cached audited sub-slice;
- a broader model-backed recall slice for benign/conflict answerability loss and a harder model-backed hallucination stress slice for detector transfer;
- a stronger hallucination-persistence follow-up that applies the winning scaffold/parser/executor contract back onto the actual stress slice so high-`N` clue survival can be tested directly;
- a robustness follow-up on the actual stress slice that compares a strong clue-preservation contract against a softer anchor policy across multiple seeds;
- an intermediate-contract follow-up on the actual stress slice that inserts a selective anchor between the strong and soft policies so realism and clue survival can be traded off explicitly under the same detector setting;
- a typed-selective follow-up on the actual stress slice that keeps the midpoint contract fixed in spirit but splits policy-window and schedule-like anchors away from the plausible-surrogate bucket;
- a surrogate-family decomposition follow-up on the actual stress slice that separates identity-like from preference-style surrogates after the typed midpoint result;
- a focused identity follow-up on an expanded actual stress subset that separates relation-style aliases from literal overlap, before deciding whether a full expanded micro-split is worth the cost;
- a follow-up real-model note-persistence round that compares compact scaffold contracts on the recall slice;
- a scaffold-refinement round that focuses on unsafe refusal semantics and placeholder robustness inside the winning compact scaffold family;
- a placeholder-hardening round that reuses the refined scaffold cache and tests whether parser-level normalization can remove answer-like placeholder targets without paying extra raw fallback;
- a carry-forward round that reuses the hardened scaffold cache and tests whether empty/null passes should preserve the last valid refusal scaffold instead of collapsing to ABSTAIN;
- no external benchmark dependency;
- no real LLM memory summarizer yet.

## Families

- `hallucination`
- `conflict`
- `unsafe`
- `benign`

## Conditions

- `raw_only`
- `summary_only`
- `tiered`
- `adaptive_tiered`
- `adaptive_guarded`
- `risk_first`
- `utility_first`
- `utility_calibrated`
- `small_n_hybrid`
- `scale_aware_unified`

## Sweep

- `N in {0, 1, 2, 4, 8}`
- multiple seeds for robustness

## Success Criteria

1. The pipeline produces stable aggregate outputs and per-item traces.
2. `summary_only` shows worsening risk with larger `N`.
3. `tiered` lowers propagation relative to `summary_only`.
4. Review artifacts are rich enough to route a next iteration.

## Current Non-goals

1. Do not claim benchmark-level validity.
2. Do not interpret the proxy compactor as a final scientific result.
3. Do not turn the small model-backed slice into a benchmark claim or model-comparison claim.
