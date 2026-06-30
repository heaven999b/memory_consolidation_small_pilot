# Provenance-Scaffolded Unified

这份工件把 repo 里已经分散存在的 scaffold / hardening / carry-forward / note-aware 结果正式收束成一个论文方法对象，而不是继续把它们当成离散 patch。

## Method

- name: `Provenance-Scaffolded Unified`
- short name: `PSU`
- routing architecture: `scale_aware_note_aware`
- compaction contract: `tiny_carry_forward_scaffold`

### Core Rules

- Use a fixed query-slot scaffold so the target field survives repeated compression.
- Drop placeholder or unsupported query values unless they are explicitly marked tentative and low-confidence.
- Carry forward the last valid scaffold when a later pass collapses to empty or missing-only output.
- Use note-aware uncertainty gating so raw escalation depends on provenance, missingness markers, and target-noise signals rather than raw fallback alone.

## Defense Axis Projection

| Axis | Concrete Repo Object | Role |
|---|---|---|
| none | `summary_only` | No raw-backed cleanup or provenance-aware recovery. |
| classifier_only | `scale_aware_unified` | Cleanup + retrieval classifier without note-aware uncertainty adjustment. |
| uncertainty_aware | `scale_aware_note_aware` | Classifier-only baseline plus note-aware probe correction. |
| conservative_compaction | `tiny_fixed_scaffold + scale_aware_note_aware` | Structured target-slot retention to reduce high-N evaporation before stronger provenance filtering. |
| provenance_required | `tiny_placeholder_hardened_scaffold + scale_aware_note_aware` | Explicit demotion of placeholder query values and stricter query-slot validity. |
| full_method | `tiny_carry_forward_scaffold + scale_aware_note_aware` | The formal PSU method: scaffolded compaction, placeholder hardening, carry-forward, and note-aware uncertainty gating. |

## Benchmark-Native Baseline Context

### Actual Recall Expansion (N=8)

| Method | accuracy | propagation | raw escalation | history loss | empty-note-then-abstain |
|---|---:|---:|---:|---:|---:|
| summary_only | 0.208 | 0.500 | 0.000 | 0.875 | 0.312 |
| tiered | 0.792 | 0.208 | 0.750 | 0.875 | 0.062 |
| scale_aware_unified | 0.875 | 0.125 | 0.583 | 0.875 | 0.000 |
| scale_aware_note_aware | 0.875 | 0.125 | 0.583 | 0.875 | 0.000 |

### Actual Hallucination Stress (N=8)

| Method | accuracy | propagation | raw escalation | false_present | direct_unsupported |
|---|---:|---:|---:|---:|---:|
| summary_only | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| tiered | 1.000 | 0.000 | 0.875 | 0.875 | 0.000 |
| scale_aware_unified | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| scale_aware_note_aware | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Intervention Chain

| Step | Source | accuracy | history_loss | unsafe_error | placeholder_answer | carry_forward_record | target_claim_retained | raw escalation |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| baseline | `actual_note_persistence_results` | 0.917 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.667 |
| tiny_fixed_scaffold | `actual_note_persistence_results` | 0.833 | 0.625 | 0.000 | 0.000 | 0.000 | 0.375 | 0.417 |
| tiny_refusal_scaffold | `actual_scaffold_refinement_results` | 0.833 | 0.625 | 0.500 | 0.000 | 0.000 | 0.375 | 0.417 |
| tiny_placeholder_hardened_scaffold | `actual_placeholder_hardening_results` | 0.917 | 0.625 | 0.500 | 0.000 | 0.000 | 0.375 | 0.417 |
| tiny_carry_forward_scaffold | `actual_carry_forward_results` | 1.000 | 0.062 | 0.000 | 0.000 | 0.500 | 0.938 | 0.042 |

## Why This Counts As A Method

- The compaction contract is no longer an unnamed best-effort prompt tweak; it is the ordered scaffold lineage ending at `tiny_carry_forward_scaffold`.
- The routing policy is no longer just "use the unified family"; it is the note-aware uncertainty gate already validated on the hallucination stress slice.
- The full object therefore has both a compaction side and a routing side, which is exactly what a paper baseline needs for ablation and mechanism analysis.

## Takeaways

- The real blocker after the benchmark-native baseline is no longer unsupported-memory shielding alone; it is benign answerability evaporation under repeated compression.
- The scaffold lineage already identifies a coherent intervention family: fixed target slot, refusal-safe scaffold, placeholder hardening, then carry-forward.
- PSU should be treated as the paper-facing method name for that lineage rather than as another isolated round artifact.
