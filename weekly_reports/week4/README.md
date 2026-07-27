# Week 4 Package

This folder is a self-contained report for an independent literature-reproduction project on **LLM/agent memory × trade-off/utility**. It does not reuse the hypotheses or conclusions of Weeks 1–3.

## Reading order

| File | Purpose |
| --- | --- |
| [week4_report_20260728_zh.md](./week4_report_20260728_zh.md) | Main Chinese weekly report: what was reproduced, what matched, what failed, and the main research directions |
| [baseline_replication_matrix_20260728.md](./baseline_replication_matrix_20260728.md) | Paper-by-paper numeric comparison, protocol fidelity, actual models, and evidence class |
| [baseline_replication_matrix_20260728.csv](./baseline_replication_matrix_20260728.csv) | Machine-readable compact version of the baseline comparison table |
| [research_proposal_roadmap_20260728.md](./research_proposal_roadmap_20260728.md) | Which observations can become proposals, what is still missing, and novelty/common-sense boundaries |

## Evidence vocabulary

- **Exact reproduction**: same released deterministic method/data/scorer, with the published headline independently recomputed.
- **Released-output recomputation**: authors' shipped outputs were independently parsed and aggregated; this checks arithmetic and artifact consistency, not a fresh end-to-end model run.
- **Non-exact substitute validation**: real model calls and recomputable scoring were used, but at least one paper model, retriever, dataset slice, or protocol component was substituted.
- **Mechanism test**: an isolated official function or hypothesized mechanism was tested; it is not the paper's end-to-end headline.
- **Auditable NO-GO**: the intended comparison could not be completed without fabricating unavailable data, cache accounting, models, or protocols, so it was stopped and documented.

No API credential, private prompt/response body, or paid-provider secret is included in this public package.
