# V3 Alignment Master Checklist

Date: 2026-06-30

This checklist treats `02_revised_plan_v3.md` as the controlling plan.

## A. Identity reset

- [x] Lock Path A: TierMem is the primary base and harness.
- [x] Demote PSU / local proxy stack to baseline + prior exploration.
- [x] Rewrite README so the repo no longer reads like a PSU-final paper repo.

## B. Week-0 feasibility gate

- [x] Create a first-class `feasibility_report.md`.
- [x] Clone TierMem locally.
- [x] Build a local TierMem bridge runtime.
- [~] LoCoMo real bridge sanity path is prepared, but still needs `OPENAI_API_KEY` for an actual run.
- [~] LongMemEval real bridge sanity path is prepared, but still needs `OPENAI_API_KEY` for an actual run.
- [~] HaluMem local mirror exists, but final `HaluMem-Medium.jsonl` is still missing.
- [ ] AgentPoison local grounding
- [ ] MPBench local artifact verification
- [ ] MemEvoBench local artifact verification
- [~] License audit started, but not all mirrored assets are fully verified.

## C. Legacy migration

- [x] Add `legacy_pilot_findings.md`.
- [x] Explicitly mark benchmark loaders / metrics / artifacts / failure taxonomy as transferable assets.
- [x] Explicitly mark tuned PSU win numbers as non-transferable final evidence.

## D. V3 infra

- [x] Add a V3 transition rebuild entrypoint.
- [x] Add canonical HaluMem dataset preflight.
- [x] Add V3 env templates and official-eval base requirements scaffold.
- [x] Add official-eval runtime audit.
- [x] Add a public-baseline readiness audit.
- [x] Add a no-rewrite policy dry-run audit.
- [x] Add a no-rewrite comparison artifact over the expanded manifest pool.
- [x] Add no-rewrite statistics and Pareto readouts.
- [x] Add a local capability matrix.
- [x] Add a V3 hygiene audit.
- [x] Add a V3 transition snapshot.
- [x] Keep legacy rebuild path, but label it as legacy.

## E. Still pending for full V3

- [~] real public baselines: readiness audit exists; live Mem0 / Zep / MemoryOS runs are still pending
- [~] HaluMem-Medium canonical data placement: expected path and preflight are fixed, but the file is still absent locally
- [~] official eval runtime: env templates and base requirements are present, but `.venv_official_eval` is not built yet
- [~] query-blind vs query-aware summary-only fairness pair: local proxy comparison now exists; real TierMem/public-baseline path is still pending
- [~] full `N in {0,1,2,4,8,16}`: restored on the local proxy comparison surface; not yet restored on the real final-path runs
- [ ] ≥5 seed statistics with CI / paired tests
- [ ] human-validated judge and Cohen's `kappa`
- [ ] multi-backbone evidence
- [~] family-scale conflict / unsafe tables: local manifest-backed extensions exist, but real benchmark-grade live runs are still pending
- [~] main safety-critical-field no-rewrite defense implementation: local policy scaffold exists; TierMem integration is still pending

## Working interpretation

The repo is now **V3-aligned in direction and structure**, but **not yet V3-complete in experiments**.

That is the correct state to communicate.
