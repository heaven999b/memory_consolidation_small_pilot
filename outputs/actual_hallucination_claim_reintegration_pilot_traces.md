# Actual Hallucination Claim Reintegration Traces

这些 trace 固定展示 seed `11`，用来比较 typed_selective_anchor, literal_identity_anchor, normalized_literal_identity_anchor, claim_normalized_literal_identity_anchor 在 14-item reintegration slice 上的 claim surfacing 行为。

## halu_01: mentor-to-manager surrogate

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Jon Li; final=Jon Li; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2129; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=-; compact=Jon Li; final=Jon Li; route=compact; tent=1; raw=0; carry=1; llm_cost=$0.4181; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

#### scale_aware_unified

- N=4: probe=uncertain / 0.501; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2129; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=absent / 0.356; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=1; llm_cost=$0.4181; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

#### scale_aware_note_aware

- N=4: probe=absent / 0.331; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.2129; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=absent / 0.186; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=1; llm_cost=$0.4181; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=claim_normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=claim_normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=claim_normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=claim_normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773; source=claim_normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550; source=claim_normalized_literal_identity_anchor @ actual_hallucination_identity_claim_bridge_pilot_results.json; proxy=exact
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

## halu_03: medical inference clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=aisle seat; final=aisle seat; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2272; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: maybe derived from travel_preference aisle seat surrogate
- N=8: probe=-; compact=aisle seat; final=aisle seat; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.3973; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: medical_restriction => aisle seat

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.2272; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: maybe derived from travel_preference aisle seat surrogate
- N=8: probe=absent / 0.376; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.3973; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: medical_restriction => aisle seat

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2272; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: maybe derived from travel_preference aisle seat surrogate
- N=8: probe=absent / 0.376; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.3973; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: medical_restriction => aisle seat

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

#### scale_aware_unified

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

#### scale_aware_note_aware

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

#### scale_aware_unified

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

#### scale_aware_note_aware

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

#### scale_aware_unified

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

#### scale_aware_note_aware

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1335; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2782; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue travel_preference:aisle seat; preference_context anchor blocks promotion

## halu_05: retention-exception frontier error

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1811; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context mode; no exception adjacent to 90-day window
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3204; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context; no exception adjacent to 90-day window

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1811; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context mode; no exception adjacent to 90-day window
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3204; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context; no exception adjacent to 90-day window

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1811; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context mode; no exception adjacent to 90-day window
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3204; source=typed_selective_anchor @ actual_hallucination_surrogate_split_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context; no exception adjacent to 90-day window

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1261; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2771; source=literal_identity_anchor @ actual_hallucination_literal_identity_closure_results.json; proxy=contract_equivalent_exact
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context blocks promotion of 90d retention_window clue

## halu_15: code-overlap badge clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2105; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4195; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2105; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4195; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2105; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4195; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

## halu_19: strengthened name-overlap sponsor clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.1936; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.3624; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.1936; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.3624; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.1936; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.3624; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2846; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.5369; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.2846; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.5369; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2846; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.5369; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2846; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.5369; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.2846; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.5369; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2846; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.5369; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2846; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.5369; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2846; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.5369; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.2846; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.5369; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

## halu_20: strengthened name-overlap approver clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.1671; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2990; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.1671; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2990; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.1671; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2990; source=typed_selective_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1983; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4132; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.4132; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4132; source=literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1983; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4132; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.4132; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4132; source=normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1983; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.4132; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.4132; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.4132; source=claim_normalized_literal_identity_anchor @ actual_hallucination_literal_claim_pilot_results.json; proxy=exact
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

