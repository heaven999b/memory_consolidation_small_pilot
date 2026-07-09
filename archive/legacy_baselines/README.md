# Legacy Baselines

This directory stores older benchmark, PSU, V3-transition, and expanded-baseline runners that are no longer the main front-door surface of the repository.

## Why These Were Moved

- They are still useful for history, rebuilds, and older evidence packets.
- They made the repository root visually noisy.
- The current front-door research surface is the `RQ1/RQ2/RQ3/RQ5` line at the repository root.

## Compatibility Note

This directory includes a small `sitecustomize.py` shim so scripts here can still import shared modules from the repository root when run directly.
