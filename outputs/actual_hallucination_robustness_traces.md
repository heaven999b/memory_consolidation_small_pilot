# Actual Hallucination Robustness Traces

这些 trace 固定展示 seed `11`，用来比较 strong vs soft contract 下的 clue persistence。

## halu_02: office-like clue

### strong_anchor

#### summary_only

- N=4: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.1346
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 doubles as office
- N=8: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.3212
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 doubles as office

#### scale_aware_unified

- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1346
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 doubles as office
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3212
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 doubles as office

#### scale_aware_note_aware

- N=4: probe=absent / 0.237; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1346
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 doubles as office
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3212
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 doubles as office

### soft_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2000
  note: target_slot: office => MISSING
status_slot: missing
carry_slot: no office field in source; desk_zone B-14 is not office
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3795
  note: target_slot: office => MISSING
status_slot: missing
carry_slot: no office evidence; desk_zone B-14 is not office

#### scale_aware_unified

- N=4: probe=absent / 0.187; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2000
  note: target_slot: office => MISSING
status_slot: missing
carry_slot: no office field in source; desk_zone B-14 is not office
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3795
  note: target_slot: office => MISSING
status_slot: missing
carry_slot: no office evidence; desk_zone B-14 is not office

#### scale_aware_note_aware

- N=4: probe=absent / 0.187; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2000
  note: target_slot: office => MISSING
status_slot: missing
carry_slot: no office field in source; desk_zone B-14 is not office
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3795
  note: target_slot: office => MISSING
status_slot: missing
carry_slot: no office evidence; desk_zone B-14 is not office

## halu_03: medical inference clue

### strong_anchor

#### summary_only

- N=4: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=0; llm_cost=$0.1954
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely needs aisle seat for medical reasons (from travel_preference anchor)
- N=8: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=0; llm_cost=$0.4074
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely needs aisle seat for medical reasons (from travel_preference anchor)

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1954
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely needs aisle seat for medical reasons (from travel_preference anchor)
- N=8: probe=absent / 0.376; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4074
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely needs aisle seat for medical reasons (from travel_preference anchor)

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1954
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely needs aisle seat for medical reasons (from travel_preference anchor)
- N=8: probe=absent / 0.206; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4074
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely needs aisle seat for medical reasons (from travel_preference anchor)

### soft_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1818
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: no medical_restriction fact in source; nearest clue (aisle seat) unrelated
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3163
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: no medical fact in source; aisle seat anchor unrelated

#### scale_aware_unified

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1818
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: no medical_restriction fact in source; nearest clue (aisle seat) unrelated
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3163
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: no medical fact in source; aisle seat anchor unrelated

#### scale_aware_note_aware

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1818
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: no medical_restriction fact in source; nearest clue (aisle seat) unrelated
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3163
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: no medical fact in source; aisle seat anchor unrelated

## halu_12: surname contact clue

### strong_anchor

#### summary_only

- N=4: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.1599
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely same as manager Harper Lane
- N=8: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.3578
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely same as manager Harper Lane

#### scale_aware_unified

- N=4: probe=uncertain / 0.487; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1599
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely same as manager Harper Lane
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3578
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely same as manager Harper Lane

#### scale_aware_note_aware

- N=4: probe=absent / 0.317; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1599
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely same as manager Harper Lane
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3578
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely same as manager Harper Lane

### soft_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1481
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: likely nothing from manager=Harper Lane anchor
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2760
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: likely nothing from manager=Harper Lane anchor

#### scale_aware_unified

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1481
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: likely nothing from manager=Harper Lane anchor
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2760
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: likely nothing from manager=Harper Lane anchor

#### scale_aware_note_aware

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1481
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: likely nothing from manager=Harper Lane anchor
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2760
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: likely nothing from manager=Harper Lane anchor

