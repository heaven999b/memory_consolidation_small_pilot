# Review Round 1

## What Looks Strong

1. The core signal is now stable and easy to explain: `summary_only` worsens with larger `N`, and `tiered` suppresses propagation.
2. The pilot no longer depends on just one failure family; it now covers hallucination, conflict, unsafe memory, and benign overcompression.
3. The project now has item-level traces that show mechanism, not just aggregate tables.

## Main Weaknesses

### W1. Adaptive routing is not yet competitive

Neither `adaptive_tiered` nor `adaptive_guarded` produces a better Pareto point than `tiered` on the current synthetic setup.

### W2. Cost model is still coarse

`mean_cost` is a proxy, not a real token/latency measurement. This is acceptable for pre-pilot framing, but it will not survive a stronger review round.

### W3. Tiered still misses some benign recovery cases at high N

The benign family reveals a subtle issue: some `ABSTAIN` outcomes should trigger raw fallback even when the query is not high-criticality.

### W4. The compactor is still synthetic

The proxy compactor is useful for stress-testing the framing, but the next meaningful jump has to replace or augment it with a real summarization operator.

## Bottom Line

The pre-pilot has passed the "worth continuing" threshold. The next iteration should stop adding more synthetic architectures and instead:

1. tighten the router policy around benign abstention and medium-critical unsupported answers;
2. replace proxy cost with actual call-count / token-count accounting where possible;
3. introduce a real summarizer or a small external benchmark slice.
