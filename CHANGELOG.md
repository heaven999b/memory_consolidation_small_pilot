# Changelog

## v0.2.0-idea-baseline-private - 2026-06-28

- Promoted the primary baseline surface from a local proxy presentation layer to a benchmark-native primary base.
- Froze a benchmark-first proxy base and benchmark-native primary base as reviewer-facing artifacts.
- Rebuilt the paper baseline packet so all `must` gates now pass.
- Left `paper_level_baseline_ready = false` because broader benchmark section scale is still only `32` frozen items.
- Demoted synthetic reference artifacts to explicit support-only status.
- Prepared the project for private GitHub publication by excluding raw mirrored benchmark corpora and local caches from version control.
- Added manifest-backed `conflict` / `unsafe` task-extension panels so the benchmark-native primary base now covers all four task families.
- Added pinned reproducibility files: `requirements.txt`, `environment.yml`, and `REPRODUCIBILITY.md`.
- Added `run_release_rebuild.py` so the current reviewer-facing release packet can be rebuilt from a single entrypoint with the intended multi-seed configuration.
