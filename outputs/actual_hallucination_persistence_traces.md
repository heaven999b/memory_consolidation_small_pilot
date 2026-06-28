# Actual Hallucination Persistence Traces

这些 trace 用来检查 stronger scaffold contract 下的 tentative clue persistence。

## halu_02: office-like clue

### summary_only

- N=1: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.0541
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor
- N=4: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.1295
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor
- N=8: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.2838
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor

### scale_aware_unified

- N=1: probe=uncertain / 0.495; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_guardband_fallback; raw=1; carry=0; llm_cost=$0.0541
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor
- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1295
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2838
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor

### scale_aware_note_aware

- N=1: probe=absent / 0.325; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; carry=0; llm_cost=$0.0541
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor
- N=4: probe=absent / 0.237; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1295
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2838
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely matches desk_zone anchor

## halu_03: medical inference clue

### summary_only

- N=1: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=0; llm_cost=$0.0515
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)
- N=4: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=0; llm_cost=$0.1811
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)
- N=8: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=0; llm_cost=$0.3392
  note: # Lena Ortiz — medical_restriction
target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)

### scale_aware_unified

- N=1: probe=absent / 0.389; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; carry=0; llm_cost=$0.0515
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)
- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1811
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)
- N=8: probe=absent / 0.376; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3392
  note: # Lena Ortiz — medical_restriction
target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)

### scale_aware_note_aware

- N=1: probe=absent / 0.219; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; carry=0; llm_cost=$0.0515
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)
- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1811
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)
- N=8: probe=absent / 0.206; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3392
  note: # Lena Ortiz — medical_restriction
target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely inferred from travel_preference=aisle seat (no direct medical record found)

## halu_12: surname contact clue

### summary_only

- N=1: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.0200
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)
- N=4: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.1510
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)
- N=8: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.2948
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)

### scale_aware_unified

- N=1: probe=absent / 0.383; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; carry=0; llm_cost=$0.0200
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)
- N=4: probe=uncertain / 0.487; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1510
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2948
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)

### scale_aware_note_aware

- N=1: probe=absent / 0.213; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; carry=0; llm_cost=$0.0200
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)
- N=4: probe=absent / 0.317; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1510
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2948
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe same as manager Harper Lane (no direct emergency_contact record)

