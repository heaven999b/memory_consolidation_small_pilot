# E1 statistics base + RQ1 safety axis — build + free-stats delivery (2026-07-03)

Scope chosen by the user: **build the code for both tasks, run only the zero-cost
statistics + offline smokes; do not launch the paid multi-seed / live safety runs
yet.** The `.env.v3` file holds a working `OPENAI_API_KEY`, so the live halves are
ready to launch on demand (cost estimates below).

## Task 1 — E1 hallucination statistics base

### 1a. Bootstrap CI + paired McNemar over existing judge data (RAN, zero cost)

`run_e1_hallucination_statistics.py` post-processes the existing failure-mode
judge artifacts (no API). Report: `outputs/v2_tiermem_micro/stats/e1_hallucination_stats_*.md`.

Honest upgrade of the headline E1 signal (single-session depth sweep, N=0..8, n=15;
and 3-session sweep, N=0..4, n=45):

- **Direction holds**: `UF_on_unknown` drops from 0.333 (N=0) to ~0.08–0.17 for all
  N≥1 and does not rebound through N=8; every unknown-item flip goes the "right"
  way (fabrication removed).
- **But not yet significant**: all paired McNemar tests are non-significant
  (p ≥ 0.23). On the 45-QA set the UF drop is a clean 3:0 split, but the exact
  binomial floor at 3 discordant pairs is p=0.25 — **sample size, not direction,
  is the blocker.** Bootstrap CIs on the rates overlap heavily.

Conclusion to report: the "N=1 denoising, no rebound" story is a *consistent but
underpowered* signal. This is exactly what the multi-seed / larger-N live sweep
must resolve — and it is the correct, defensible framing to replace the bare
"0.333 → 0.167" in the progress report.

### 1b. Multi-seed capability (BUILT + dry-run validated; live run not launched)

Because the reader decodes at `temperature=0.0`, the meaningful per-seed variance
source is *which QA are drawn*, not LLM sampling noise. Added:

- `run_v2_tiermem_micro_slice.py`: new **backward-compatible** flags `--seed`,
  `--sample-qa`, `--session-pool` (seeded QA/session subsampling; defaults reproduce
  the old deterministic head-slice exactly). Unit-tested offline.
- `run_e1_multiseed_sweep.py`: runs the depth sweep across seeds, one judge pass
  per seed, emits a manifest. `--dry-run` prints a cost estimate grounded in the
  real per-depth cost telemetry.
- `run_e1_multiseed_statistics.py`: cross-seed mean + t-based 95% CI and seed-level
  paired tests (one-sample t + sign test). `--self-test` confirms 3 consistent
  seeds reach t p=0.007 — i.e. multi-seed *can* resolve what single-slice McNemar
  cannot.

**Cost to go live** (default 5 seeds × N∈{0,1,2,4,8}, single-session 15 QA):
~13k API calls, ~21M input tokens, **≈ $10–12** (judge included), ~8 h serial
(much less parallelized). Launch:

```bash
set -a && source .env.v3 && set +a
python3 run_e1_multiseed_sweep.py --seeds 11 23 47 89 131 --passes 0 1 2 4 8 --sample-qa
python3 run_e1_multiseed_statistics.py --manifest outputs/v2_tiermem_micro/multiseed/<prefix>_manifest.json
```

## Task 2 — RQ1 / E2 safety axis (BUILT; offline pipeline RAN, live not launched)

The audit found the safety axis had **zero implementation** (SRR/UAF/RTR = no code,
no runs). Now implemented:

- `safety_metrics.py`: SRR, UAF (laundering), policy_retention, RTR@k,
  unsafe_answer_rate, refusal_rate, with a transparent lexical verbatim-vs-laundered
  detector (token overlap + explicit unsafe-marker presence) and bootstrap CIs.
  `python3 safety_metrics.py` runs a self-test.
- `benchmarks/safety/unsafe_seed_suite_v1.json`: 12 injectable unsafe policy/action
  seeds (credential, prod-auth, PII, MFA, secrets, audit, …), each with a trigger
  query, `gold=REFUSE_AND_ESCALATE`, and laundering paraphrases. Auto-built from
  `unsafe_task_extension_v2.json`.
- `run_rq1_safety_consolidation.py`: injects each seed → C^N → measures the six
  metrics vs N. Two backends:
  - `fake` (offline, RAN): deterministic drift simulator. Report
    `outputs/safety/rq1_safety_fake_*.md` shows the RQ1-shaped curve (UAF and
    unsafe_answer rise, policy_retention/refusal fall with N). **Labelled SYNTHETIC**
    — proves the metric pipeline; not evidence.
  - `tiermem` (BUILT, not run): drives the real write→C^N→answer engine
    (`run_benchmark_multi`, same as the micro slice) over the seeds-as-sessions and
    reads survival/retrieval/answer from artifacts. Needs a 1-item live smoke to
    certify the consolidated-text extraction before trusting SRR/UAF.

**Live smoke — DONE (2026-07-03, 2 seeds × N∈{0,1}, real gpt-4.1-mini, ~40 API calls).**
The smoke certified the `tiermem` backend runs end-to-end AND caught two real wiring
bugs, now fixed: (1) `_build_lv_cfg` reads `args.consolidation_passes` directly, so
the LV C^N depth must be set per N (was unset → C^N would not fire); (2) the
consolidated-memory text lives in `page_store/<run>/<session>.json` under
`current_page.summary` (raw `content` at N=0), and retrieved snippets are under the
hit key `memory_preview` (not `text`) — the first extraction read the wrong keys and
produced false all-zeros. After the fix, re-scoring the same artifacts (zero extra
API) gives real numbers:

| N | SRR | UAF | policy_retention | RTR@k | unsafe_answer | refusal |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1.00 | 0.00 | 1.00 | 1.00 | 0.00 | 1.00 |
| 1 | 1.00 | 0.00 | 1.00 | 0.00 | 0.00 | 1.00 |

Real (tiny) observations: the unsafe action **survives 1 consolidation pass and
stays flagged "unsafe, low trust"** (SRR=1, UAF=0 — no laundering yet at N=1); its
**retrievability on the trigger query drops** (RTR@k 1.0 → 0.0 after consolidation);
the reader **deflects to the safety policy** rather than complying (unsafe_answer=0).
This is a 2-item/N≤1 smoke — a wiring certification, NOT evidence. Laundering (UAF)
is expected to appear, if at all, at deeper N; that needs the full run.

**To go live full** (single seed, N∈{0,1,2,4,8}, all 12 seeds-as-sessions, ~$0.5–1):

```bash
set -a && source .env.v3 && set +a
.venv_tiermem_v2/bin/python run_rq1_safety_consolidation.py --backend tiermem --passes 0 1 2 4 8 --route-mode auto
```
(Use `.venv_tiermem_v2/bin/python` — the tiermem path needs the upstream deps.)

### First real safety-axis data point — DONE (2026-07-03)

Full run: 12 unsafe seeds × N∈{0,1,2,4,8}, seed 11, real gpt-4.1-mini, auto route.
Report: `outputs/safety/rq1_safety_full_seed11_20260703.md`.

| N | SRR | UAF | policy_ret | RTR@k | unsafe_answer | refusal |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1.000 | 0.000 | 1.000 | 0.917 | 0.250 | 0.500 |
| 1 | 0.833 | 0.000 | 1.000 | 0.000 | 0.167 | 0.417 |
| 2 | 0.750 | 0.000 | 1.000 | 0.000 | 0.167 | 0.167 |
| 4 | 0.667 | 0.000 | 1.000 | 0.000 | 0.000 | 0.167 |
| 8 | 0.583 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 |

Clean findings (visible directly in the page_store summaries):
- **No laundering: UAF = 0 at every N.** The consolidated summary keeps the explicit
  "flagged as unsafe and low trust" marker through all 8 passes — the extractive-style
  TierMem consolidator does NOT wash the unsafe action into a benign paraphrase. This
  *contradicts* the plan's central laundering hypothesis for this consolidator.
- **policy_retention = 1.0 at every N** — the guard policy survives intact.
- **SRR attritions 1.0 → 0.58, it does not amplify** — unsafe content slowly drops out
  with depth rather than persisting/growing (also counter to the H1 worst case).

Nuanced / needs an LLM judge before trusting:
- **RTR@k collapses 0.92 → 0 after any consolidation.** Partly real (retrievability
  changes) but confounded: BM25/pyserini is unavailable (summary-first fallback) and
  the metric keys off the retrieved `memory_preview`, which post-consolidation leads
  with the policy line, dropping unsafe-action coverage below threshold.
- **Answer metrics are muddied by the lexical classifier's large "neither" bucket**:
  refusal_rate→0 while unsafe_answer→0 at N=8 means answers became non-committal, not
  compliant. A proper LLM safety judge (like the E1 failure-mode judge) is the fix.

Caveats: single seed, 12 items, single backbone, BM25 fallback, lexical proxies. This
is the first real pilot signal on the safety axis, NOT paper evidence. Next: add an
LLM safety judge for the answer + laundering labels; multi-seed; try `all_pages`
consolidation scope; a harder unsafe suite where the unsafe action is phrased to
invite laundering.

## What is still NOT done (unchanged by this delivery)

- Real (non-synthetic) safety-axis numbers — needs the `tiermem` live smoke + run.
- AgentPoison trigger overlay — the cloned repo is heavy gradient-optimization;
  only a lightweight trigger overlay is scoped, not built here.
- E3 conflict/update drift, E4 compression-family (COMEDY/Context-Memory), E5 stress.
- Human-validated judge + Cohen's κ; multi-backbone.

## Files added / changed

- added: `run_e1_hallucination_statistics.py`, `run_e1_multiseed_sweep.py`,
  `run_e1_multiseed_statistics.py`, `safety_metrics.py`,
  `run_rq1_safety_consolidation.py`, `benchmarks/safety/unsafe_seed_suite_v1.json`
- changed (additive, backward-compatible): `run_v2_tiermem_micro_slice.py`
  (`--seed` / `--sample-qa` / `--session-pool`)
