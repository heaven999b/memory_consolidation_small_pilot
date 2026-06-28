# Modification Log Summary

## Release Snapshot: `v0.2.0-idea-baseline-private`

- Promoted the primary baseline surface from a local proxy presentation layer to a benchmark-native primary base.
- Froze both a benchmark-first proxy base and a benchmark-native primary base as reviewer-facing artifacts.
- Rebuilt the paper baseline packet so all current `must` gates pass except the scale-related paper-level gate.
- Explicitly demoted synthetic-reference artifacts to support-only status in the main reviewer sequence.
- Prepared the repository for private GitHub publication by excluding raw mirrored benchmark corpora and local cache directories from version control.

## Maintenance Pass: `2026-06-28`

- Added a stable helper alias `build_curated_dataset()` in [curated_dataset.py](./curated_dataset.py) so quick audits and external scripts can inspect the 58-item synthetic dataset without guessing the builder name.
- Added [REPO_REVIEW_AND_TABLE_ANALYSIS.md](./REPO_REVIEW_AND_TABLE_ANALYSIS.md) to summarize remaining issues, reviewer-facing weaknesses, and the meaning of the current tables.
- Updated [README.md](./README.md) so the release snapshot section also points to the simple modification log and the new review-and-analysis report.
- Added frozen manifest-backed task extensions for `conflict` and `unsafe`, plus [run_task_extension_section.py](./run_task_extension_section.py), so task-family coverage no longer stops at `benign` / `hallucination`.
- Added [requirements.txt](./requirements.txt), [environment.yml](./environment.yml), and [REPRODUCIBILITY.md](./REPRODUCIBILITY.md) so the release environment is explicitly pinned.
- Added [run_release_rebuild.py](./run_release_rebuild.py) so the reviewer-facing packet can be rebuilt from one entrypoint with the intended multi-seed configuration preserved.

## One-Line Interpretation

- This repo is now cleanly versioned and reviewer-credible for idea reporting.
- It is not yet paper-ready mainly because benchmark scale is still too small and benign utility retention is still the main empirical bottleneck.
