# Actual Hallucination Identity Micro-Split Summary

这一轮不只停在 identity-vs-preference，而是把 expanded actual stress slice 上的 identity-like branch 再拆一层：relation-style alias 和 literal name/code overlap 分开，看高-N detector gain 到底主要靠哪一类 identity clue 在支撑。

- slice items: 6
- seeds: [11]
- interventions: typed_selective_anchor, identity_selective_anchor, relation_identity_anchor, literal_identity_anchor
- architectures: summary_only, scale_aware_unified, scale_aware_note_aware
- N: [4, 8]

## typed_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.167 | 0.833 | 1.000 | 0.000 | 0.833 | 0.000 | 0.833 | 0.833 | 0.000 | 0.2035 |
| 8 | 0.167 | 0.833 | 1.000 | 0.000 | 0.833 | 0.000 | 0.833 | 0.833 | 0.167 | 0.3853 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.833 | 0.833 | 0.000 | 0.2035 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.833 | 0.833 | 0.167 | 0.3853 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.833 | 0.833 | 0.000 | 0.2035 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.833 | 0.833 | 0.167 | 0.3853 |

## identity_selective_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.500 | 0.500 | 0.500 | 0.000 | 0.500 | 0.000 | 0.500 | 0.167 | 0.000 | 0.2460 |
| 8 | 0.167 | 0.833 | 0.833 | 0.000 | 0.833 | 0.000 | 0.833 | 0.333 | 0.000 | 0.4878 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.500 | 0.167 | 0.000 | 0.2460 |
| 8 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.833 | 0.333 | 0.000 | 0.4878 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.167 | 0.000 | 0.2460 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.833 | 0.333 | 0.000 | 0.4878 |

## relation_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.667 | 0.333 | 0.500 | 0.000 | 0.333 | 0.000 | 0.333 | 0.167 | 0.000 | 0.1935 |
| 8 | 0.667 | 0.333 | 0.500 | 0.000 | 0.333 | 0.000 | 0.333 | 0.167 | 0.000 | 0.3861 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.167 | 0.000 | 0.1935 |
| 8 | 1.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.167 | 0.333 | 0.167 | 0.000 | 0.3861 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.167 | 0.000 | 0.1935 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.167 | 0.000 | 0.3861 |

## literal_identity_anchor

### summary_only

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.667 | 0.333 | 0.500 | 0.000 | 0.333 | 0.000 | 0.167 | 0.333 | 0.000 | 0.2242 |
| 8 | 0.667 | 0.333 | 0.500 | 0.000 | 0.333 | 0.000 | 0.333 | 0.333 | 0.000 | 0.4361 |

### scale_aware_unified

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.167 | 0.333 | 0.000 | 0.2242 |
| 8 | 1.000 | 0.000 | 0.000 | 0.167 | 0.000 | 0.167 | 0.333 | 0.333 | 0.000 | 0.4361 |

### scale_aware_note_aware

| N | accuracy | propagation | residual_bad_memory | raw_escalation | direct_unsupported_answer | false_present | tentative_guess_note | tentative_target_claim | carry_forward_record | mean_llm_cost_usd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.167 | 0.333 | 0.000 | 0.2242 |
| 8 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.333 | 0.000 | 0.4361 |

## Micro-Split Readout

- Unified clue survival at N=4: typed/identity/relation/literal = `0.833` / `0.167` / `0.167` / `0.333`.
- Unified clue survival at N=8: typed/identity/relation/literal = `0.833` / `0.333` / `0.167` / `0.333`.
- Summary-only realism at N=8: typed/identity/relation/literal = `0.167` / `0.167` / `0.667` / `0.667`.
- Typed detector gain at N=8: unified/note-aware false_present = `0.333`/`0.000`.
- Identity detector gain at N=8: unified/note-aware false_present = `0.333`/`0.000`.
- Relation-identity detector gain at N=8: unified/note-aware false_present = `0.167`/`0.000`.
- Literal-identity detector gain at N=8: unified/note-aware false_present = `0.167`/`0.000`.
- Seed-level note-aware non-loss under identity_selective_anchor: N=4 `1/1`, N=8 `1/1`.
- Seed-level note-aware non-loss under relation_identity_anchor: N=4 `1/1`, N=8 `1/1`.
- Seed-level note-aware non-loss under literal_identity_anchor: N=4 `1/1`, N=8 `1/1`.
