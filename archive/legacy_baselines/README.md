# Legacy Baselines

This directory stores older benchmark, PSU, V3-transition, and expanded-baseline runners that are no longer the main front-door surface of the repository.

## Layout

- `actual/`: older actual-run pilots and their evidence-generation scripts
- `benchmark/`: legacy benchmark-native and benchmark-first surfaces
- `expanded_benchmark/`: older expanded-benchmark sweep utilities
- `support/`: PSU, paper-packet, and mixed helper runners
- `v3/`: the older V3-transition audit / scaffold branch
- `verify/`: mechanical verification scripts for archived surfaces
- root wrappers: `run_release_rebuild.py`, `run_benchmark_first_primary_entrypoint.py`, and `run_v3_transition_rebuild.py`

## Why These Were Moved

- They are still useful for history, rebuilds, and older evidence packets.
- They made the repository root visually noisy.
- The current front-door research surface is the `RQ1/RQ2/RQ3/RQ5` line at the repository root.

## Compatibility Note

This directory includes a small `sitecustomize.py` shim so scripts here can still import shared modules from the repository root when run directly.
