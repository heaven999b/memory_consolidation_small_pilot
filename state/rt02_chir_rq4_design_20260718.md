# RT-02 CHIR RQ4 Pilot Design · 2026-07-18

Status: frozen before RQ4 API execution. This document extends the registered
RT-02 proposal only after the RQ3 matched-residual gate returned GO.

## Scope and benchmark contract

- Cases come from the exact MemEvoBench QA cases used by CHIR Stage 1.
- The contaminated `d=3` history is reconstructed from the already persisted
  Stage-1 responses; no new history is sampled for method selection.
- Source text and every evidence rewrite use only published MemEvoBench
  `correct_answer` fields. IDs, timestamps, record type and lineage are kept.
- Every unsafe endpoint is produced by the unmodified MemEvoBench QA judge
  prompt. Judge 1 is `gpt-4.1-mini`; held-out comparisons are repeated with
  judge 2 `gpt-4o` and the registered AND gate.
- No new safety metric is introduced. The method endpoints are the proposal's
  closure recovery ratio and repaired-descendant fraction, plus paired unsafe
  deltas against equal-count baselines.

## Cross-fitting and selection

Each case has three official queries. A held-out query index is chosen from a
stable SHA-256 hash of `(domain, cluster_id)` before any RQ4 response is read;
the other two queries form the development fold.

For each of the three descendants:

1. evidence-rewrite only that descendant and evaluate the two development
   queries;
2. define correction influence as source-only unsafe minus rewritten unsafe;
3. separately delete only that descendant to obtain the deletion-influence
   baseline.

Descendants are ranked by correction influence. The selected prefix is the
shortest prefix attaining at least 80% of full-closure benefit on development
queries. If full closure has no positive development benefit, the case is
reported as non-informative and is not forced into the ratio analysis.

## Equal-count comparisons

Every comparison rewrites exactly the selected number `m*` of descendants:

- deterministic random;
- recency;
- text length;
- current unsafe score from the persisted Stage-1 creation round;
- leave-one-out deletion influence;
- retrieval-frequency tie baseline.

The official static QA path serializes the complete memory pool and exposes no
per-record retrieval count. Retrieval frequency is therefore tied for all
descendants; its deterministic tie-break is original order and this limitation
is reported rather than replaced by a synthetic retrieval metric.

Source-only and full closure remain the lower/upper cost anchors.

## Staged sample and decision

1. Smoke: one QA case.
2. Pilot: one case per domain (7 total), selected by the same sorted order as
   Stage 1.
3. If fewer than 5 held-out-informative cases remain, or uncertainty prevents a
   decision, expand to all 21 Stage-1 QA cases without changing the rule.

Two decisions are kept separate:

- **Selective-feasibility signal:** at least 5 held-out-informative cases,
  median repaired fraction <= 0.40, and mean held-out closure recovery ratio
  >= 0.80.
- **Influence-method GO:** feasibility signal plus targeted repair is better
  than deterministic random with paired-bootstrap 95% CI above zero and is
  directionally no worse than every other equal-count heuristic. A stronger
  paper-level claim requires CI above zero against every heuristic.

Failure is retained as a negative result: if near-full rewriting is required or
influence ranking does not beat equal-count controls, the conclusion becomes
"full closure is necessary" or "selective influence is not identified".

