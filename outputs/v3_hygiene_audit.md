# V3 Hygiene Audit

| Check | Value |
|---|---|
| absolute path leak files | `2` |
| outputs file count | `8262` |
| outputs total bytes | `1026716693` |

## Absolute Path Leaks

| Path | Hits | Sample |
|---|---|---|
| outputs/v3_halumem_dataset_preflight.json | `1` | "copy_hint": "cp /path/to/HaluMem-Medium.jsonl '/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl'", |
| outputs/v3_halumem_dataset_preflight.md | `1` | - copy hint: `cp /path/to/HaluMem-Medium.jsonl '/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/benchmarks/halumem/official_repo/data/HaluMem-Medium.jsonl'` |

## Recommendations

- Strip `/Users/` absolute paths from submission-facing docs and HTML before any external release.
- Treat the current outputs tree as an internal working surface until a double-blind cleanup pass is complete.
- Prefer the new V3 reports and snapshots over older legacy packet artifacts when preparing paper-facing materials.
