# Review Round 10

## What Improved

1. This round finally upgrades the compactor from a hand-authored proxy into a real model-backed operator on an audited sub-slice.
2. The realism check survives. `summary_only` still degrades as consolidation depth grows, and `scale_aware_unified` still beats `tiered` on high-`N` contamination and raw fallback.
3. The experiment is cleaner than a naive API plug-in round because prompt leakage was explicitly controlled: no family labels, neutral working directory, and cache versioning after the leak audit.

## Main Weaknesses

### W1. The dominant real-model failure mode is not the old proxy bottleneck

On the actual slice, the main high-`N` problem is over-compression and answerability loss on benign/conflict cases, not hallucination false-present. That means the detector round was valuable, but the real-model bottleneck has already shifted.

### W2. Detector transfer is still under-exercised

The actual slice does not strongly reactivate hallucination-side false-present under `scale_aware_unified`, so the note-aware detector cannot yet demonstrate an additional win there. This is an informative non-result, not a negative result.

### W3. The slice is still a checkpoint, not a benchmark

The model-backed evidence is stronger than the textual proxy, but it is still only 8 audited items and one seed. The project should resist overstating that scope.

## Bottom Line

This was the right next step. The project now has real model-backed evidence for the main consolidation-risk story. The next move should be chosen based on the new real-model bottleneck: either expand benign/conflict actual-slice coverage, or build a harder actual hallucination slice if the goal is to stress detector transfer directly.
