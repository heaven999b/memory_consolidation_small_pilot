# Benchmarks

This directory stores official-source benchmark files used to ground the local adapter layer.

Policy:
- Keep official raw files, helper scripts, and READMEs under stable local paths.
- Track exact source URLs, included local files, and any intentional omissions or quarantined files in each benchmark family's `SOURCE_MANIFEST.json`.
- Do not mark an adapter fully grounded until a frozen local slice manifest exists under that adapter's declared `frozen_slices/` path.

Current state:
- `halumem/` contains the mirrored official HaluMem repo data and evaluation helpers.
- `locomo/` contains mirrored LoCoMo raw data plus LongMemEval helper files and verified cleaned subsets.
- `task_extensions/` contains frozen local manifest-backed conflict/unsafe extension slices used to complete four-family primary-base coverage.

Git publication note:
- The private Git snapshot tracks `SOURCE_MANIFEST.json` files and the frozen `frozen_slices/` artifacts.
- The large mirrored raw benchmark corpora under `official_repo/data/`, `locomo_official/data/`, and `longmemeval_official/data/` are intentionally ignored in git to keep the repository publishable and reviewer-facing.
- Anyone who wants to rebuild the frozen slices from raw sources should restore those local raw files according to each benchmark family's `SOURCE_MANIFEST.json`.
