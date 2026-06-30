# Reviewer Blockers Clean List

Date: 2026-06-30

This note records the cleaned blocker list that should drive the next execution phase.
The omitted item is the separate `>=5 seed` requirement, which is tracked elsewhere.

## 1. Week-0 feasibility gate is not yet truly passed

- `feasibility_report.md` still shows TierMem and HaluMem as `partial`.
- TierMem is blocked by `OPENAI_API_KEY`, so there is still no real LoCoMo / LongMemEval end-to-end run.
- HaluMem is no longer blocked by dataset placement: the canonical `HaluMem-Medium.jsonl` is now present locally, and the remaining blocker is also `OPENAI_API_KEY`.
- AgentPoison and MemEvoBench are now locally grounded at the repository level, but they still do not count as executed attack-suite evidence.
- MPBench is still unresolved as a runnable local artifact.
- Working conclusion: there is not yet a real-model, real-benchmark, end-to-end minimum run that can serve as the empirical anchor.

## 2. `outputs/v3_no_rewrite_statistics.md` should be treated as synthetic dry-run evidence

- The reported risk-family deltas are exact `0.000` or exact `+/-1.000`, with zero-width confidence intervals.
- That pattern does not look like real LLM output variation; it looks like a by-construction proxy result.
- Working conclusion: these artifacts must be labeled as synthetic / dry-run and must not be mixed into the same evidence table as real benchmark results.

## 3. The N sweep is still too shallow on the real-facing path

- The plan called for `N in {0,1,2,4,8,16}`.
- The synthetic local no-rewrite surface now exposes the full sweep, but the real benchmark-facing path still does not.
- That means a real-path trend claim is still unavailable.
- Working conclusion: restore at least `{0,1,2,4,8}` on the real benchmark-facing path before making any N-trend argument.

## 4. The safety attack suite is still not executed evidence

- AgentPoison is now locally grounded at the repository level, but no trigger/query overlay has been executed yet.
- MemEvoBench is now locally grounded at the repository level, but no tiny runnable path has been executed yet.
- MPBench is still not locally verified.
- Any current `unsafe` family table is therefore best understood as a proxy extension, not a true attack benchmark result.
- Working conclusion: do not claim executable attack-suite evidence until real trigger cases are grounded and run.

## 5. Legacy pilot scripts still show strong small-sample overfitting risk

- The repository contains many narrowly patched pilot scripts for highly specific hallucination failure modes.
- This is consistent with repeated in-sample tuning on tiny panels.
- The repo already partially acknowledges this by stating that tuned PSU small-panel wins are not paper-grade evidence.
- Working conclusion: keep these legacy artifacts clearly quarantined from formal benchmark claims.

## 6. Experiment order is currently inverted

- By plan, `E0` should first validate the harness on real raw-store / provenance / summary-tier sanity checks.
- `feasibility_report.md` still shows that this step is not actually complete.
- That means current `v3_no_rewrite_*` conclusions were generated before the base harness was empirically validated.
- Working conclusion: pass `E0` first, then run defense comparisons.

## 7. Perfect ties on benign utility sub-comparisons are another proxy warning sign

- Blind vs query-aware shows all ties on some hallucination / unsafe family metrics.
- That usually means either the test pool is too weak, or the metric path is being short-circuited by fixed rules rather than true model-output sensitivity.
- Working conclusion: inspect whether these family metrics actually depend on model outputs, or whether the current scoring path is effectively rule-determined.

## Overall interpretation

The repository currently looks strongest as:

- V3 migration infrastructure
- audit and readiness scaffolding
- benchmark plumbing and packaging

It is still weak as:

- real-model, real-benchmark empirical evidence
- attack-suite execution
- final paper-grade statistical support

## Execution order implied by this list

1. Pass the Week-0 feasibility gate for TierMem and HaluMem.
2. Establish one real `E0` sanity run on LoCoMo / LongMemEval and one real HaluMem path.
3. Clearly separate synthetic dry-run artifacts from real benchmark evidence in docs and tables.
4. Restore a meaningful N sweep.
5. Ground at least one real attack-suite source, starting with AgentPoison.
6. Only then promote defense, utility, and safety conclusions into paper-facing artifacts.
