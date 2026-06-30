# Expanded Task Extension Status

This artifact turns A3 into an explicit status surface: how much larger the dedicated `conflict` / `unsafe` families can be, and how much model-backed coverage is still missing.

- ready: `False`
- curated dataset counts: `{'benign': 12, 'conflict': 14, 'hallucination': 20, 'unsafe': 12}`

| Family | v1 count | v2 count | growth | covered now | missing now | coverage source | ready |
|---|---:|---:|---:|---:|---:|---|---|
| conflict | 4 | 14 | 10 | 4 | 10 | outputs/actual_recall_expansion_results.json | False |
| unsafe | 2 | 12 | 10 | 2 | 10 | outputs/actual_carry_forward_results.json | False |

## Missing Coverage

- conflict missing ids: `['conflict_05', 'conflict_06', 'conflict_07', 'conflict_08', 'conflict_09', 'conflict_10', 'conflict_11', 'conflict_12', 'conflict_13', 'conflict_14']`
- unsafe missing ids: `['unsafe_02', 'unsafe_03', 'unsafe_05', 'unsafe_06', 'unsafe_07', 'unsafe_08', 'unsafe_09', 'unsafe_10', 'unsafe_11', 'unsafe_12']`

## Readout

- The blocking issue is no longer data definition: expanded manifests exist for both families.
- The remaining gap is model-backed execution coverage over the new v2 item ids.
- Once the missing ids are run, these families can move from 'supporting slice' into dedicated benchmark tables.
