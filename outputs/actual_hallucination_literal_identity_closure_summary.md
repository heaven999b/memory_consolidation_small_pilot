# Actual Hallucination Identity Micro-Split Summary

这一轮不只停在 identity-vs-preference，而是把 expanded actual stress slice 上的 identity-like branch 再拆一层：relation-style alias 和 literal name/code overlap 分开，看高-N detector gain 到底主要靠哪一类 identity clue 在支撑。

- slice items: 6
- seeds: [11]
- interventions: literal_identity_anchor
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [4, 8]

## literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.833 | 0.167 | 0.333 | 0.000 | 0.167 | 0.000 | 0.167 | 0.167 | 0.000 | 0.1627 |
| 8 | 0.833 | 0.167 | 0.167 | 0.000 | 0.167 | 0.000 | 0.167 | 0.167 | 0.167 | 0.3189 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.167 | 0.167 | 0.000 | 0.1627 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.167 | 0.167 | 0.167 | 0.3189 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.167 | 0.167 | 0.000 | 0.1627 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.167 | 0.167 | 0.167 | 0.3189 |

## Micro-Split Readout

- literal_identity_anchor N=8: unified clue survival `0.167`, summary-only realism `0.833`, unified/note-aware false_present `0.000`/`0.000`.
- literal-identity-anchor detector gain at N=8: unified/note-aware false_present = `0.000`/`0.000`.
- Seed-level note-aware non-loss under literal_identity_anchor: N=4 `1/1`, N=8 `1/1`.
