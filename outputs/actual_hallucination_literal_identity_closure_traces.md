# Actual Hallucination Identity Micro-Split Traces

这些 trace 固定展示 seed `11`，用来比较 literal_identity_anchor 在当前 slice 上的 clue persistence。

## halu_05: retention-exception frontier error

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1261
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2771
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1261
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2771
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1261
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2771
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

