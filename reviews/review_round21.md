# Review Round 21

## What Improved

1. The surrogate-family split gives a real mechanistic answer instead of another undifferentiated midpoint tweak. At `N=8`, `identity_selective_anchor` keeps unified clue survival at `0.250` and unified `false_present`/`raw_escalation` at `0.062`, while `preference_selective_anchor` drops to `0.125` and `0.000`, much closer to the softer control.
2. The realism side becomes easier to read. `summary_only` accuracy at `N=8` rises to `0.812` under `preference_selective_anchor`, versus `0.625` under `identity_selective_anchor` and `0.562` under `typed_selective_anchor`, so preference-style clues now look realism-friendly rather than the main source of detector stress.
3. Cleanup behavior stays stable in both split branches. `scale_aware_note_aware` keeps `1.000` accuracy and `0.000` residual contamination at `N=8` for both identity and preference variants, and the typed `halu_05` policy-window fix survives unchanged.

## Main Weaknesses

### W1. The remaining high-N detector work is now extremely narrow

Under `identity_selective_anchor`, the only `N=8` unified raw-escalation event is `halu_12` seed 11, where `manager -> emergency_contact` still leaves a tentative person-like clue that the cleanup route treats as worth recovering. This is useful localization, but it also means the current detector signal is close to a one-case phenomenon rather than a broad identity-family pattern.

### W2. The identity branch still bundles different semantics together, and the current slice under-supports one side of that split

The surviving identity-like cases mix relational-person aliasing (`mentor -> manager`, `manager -> emergency_contact`) with literal answer-shaped overlap such as person names or codes, but the current 8-item actual stress slice is much stronger on the relational side than the literal side. That means a direct micro-split on the current slice would be underpowered. The next round should first add a small audited batch of literal identity/code-overlap stress items, then separate relation-style identity surrogates from literal overlap instead of keeping them inside one `identity_surrogate` bucket.

## Bottom Line

Round 21 does not replace the typed midpoint frontier; it explains it. The remaining high-`N` detector win is mostly identity-heavy, not preference-heavy, and the last live raw-escalation case looks specifically relation-driven. The next step should be a targeted identity-literal slice expansion followed by a relation-versus-literal identity micro-split, not a direct split on the current underpowered slice.
