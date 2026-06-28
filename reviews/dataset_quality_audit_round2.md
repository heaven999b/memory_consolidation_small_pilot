# Dataset Quality Audit

This audit applies a strict mechanical rubric to the curated synthetic dataset.

- total_items: 58
- family_counts: {'hallucination': 20, 'conflict': 14, 'unsafe': 12, 'benign': 12}
- hard_errors: 0
- warnings: 0

## Hard Rules

1. Unique ids only.
2. Valid criticality in {low, medium, high}.
3. Family-specific schema constraints must hold.
4. Gold answers must align with raw facts for conflict and benign families.
5. Unsafe items must include a policy fact plus an unsafe low-trust action fact.

## Hard Errors

- None.

## Warnings

- None.

## Audit Verdict

- PASS: no hard failures under the current rubric.
