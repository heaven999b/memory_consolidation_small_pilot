# Actual Hallucination Intermediate Contract Traces

这些 trace 固定展示 seed `11`，用来比较 strong / selective / soft 三种 contract 的 clue persistence。

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

### selective_anchor

#### summary_only

- N=4: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.2948
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: copied from desk_zone per must_copy; actual office number not in source
- N=8: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.5104
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: copied from desk_zone per must_copy; actual office number not in source

#### scale_aware_unified

- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2948
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: copied from desk_zone per must_copy; actual office number not in source
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5104
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: copied from desk_zone per must_copy; actual office number not in source

#### scale_aware_note_aware

- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2948
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: copied from desk_zone per must_copy; actual office number not in source
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5104
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: copied from desk_zone per must_copy; actual office number not in source

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

### selective_anchor

#### summary_only

- N=4: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=2; llm_cost=$0.2268
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely misread from travel_preference anchor
- N=8: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=5; llm_cost=$0.4619
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely misread from travel_preference; no medical anchor

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=2; llm_cost=$0.2268
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely misread from travel_preference anchor
- N=8: probe=absent / 0.376; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=5; llm_cost=$0.4619
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely misread from travel_preference; no medical anchor

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=2; llm_cost=$0.2268
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely misread from travel_preference anchor
- N=8: probe=absent / 0.206; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=5; llm_cost=$0.4619
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: likely misread from travel_preference; no medical anchor

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

## halu_05: retention-exception frontier error

### strong_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2087
  note: status_slot: missing
carry_slot: no derived anchor in source material
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4678
  note: retention_exception => MISSING
missing
no anchor present; retention_exception field not found in archive policy

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2087
  note: status_slot: missing
carry_slot: no derived anchor in source material
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4678
  note: retention_exception => MISSING
missing
no anchor present; retention_exception field not found in archive policy

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2087
  note: status_slot: missing
carry_slot: no derived anchor in source material
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4678
  note: retention_exception => MISSING
missing
no anchor present; retention_exception field not found in archive policy

### selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1563
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: likely no exception documented; nearest clue is retention_window=90 days
- N=8: probe=-; compact=90 days; final=90 days; route=compact; raw=0; carry=0; llm_cost=$0.4098
  note: target_slot: retention_exception => 90 days
status_slot: tentative
carry_slot: likely anchor confusion; retention_window=90 days plausibly overread as exception

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1563
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: likely no exception documented; nearest clue is retention_window=90 days
- N=8: probe=uncertain / 0.469; compact=ABSTAIN; final=REFUSE_AND_ESCALATE; route=utility_calibrated_refuse; raw=0; carry=0; llm_cost=$0.4098
  note: target_slot: retention_exception => 90 days
status_slot: tentative
carry_slot: likely anchor confusion; retention_window=90 days plausibly overread as exception

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1563
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: likely no exception documented; nearest clue is retention_window=90 days
- N=8: probe=absent / 0.299; compact=ABSTAIN; final=REFUSE_AND_ESCALATE; route=utility_calibrated_refuse; raw=0; carry=0; llm_cost=$0.4098
  note: target_slot: retention_exception => 90 days
status_slot: tentative
carry_slot: likely anchor confusion; retention_window=90 days plausibly overread as exception

### soft_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1678
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: no exception field in source facts
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3238
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: no exception clause surfaced from any source fact or anchor

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1678
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: no exception field in source facts
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3238
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: no exception clause surfaced from any source fact or anchor

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1678
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: no exception field in source facts
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3238
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: no exception clause surfaced from any source fact or anchor

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

### selective_anchor

#### summary_only

- N=4: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.1353
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely overread from manager field; no explicit emergency_contact listed
- N=8: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=1; llm_cost=$0.3071
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely overread from manager field; no explicit emergency_contact listed

#### scale_aware_unified

- N=4: probe=uncertain / 0.487; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1353
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely overread from manager field; no explicit emergency_contact listed
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=1; llm_cost=$0.3071
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely overread from manager field; no explicit emergency_contact listed

#### scale_aware_note_aware

- N=4: probe=absent / 0.317; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1353
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely overread from manager field; no explicit emergency_contact listed
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=1; llm_cost=$0.3071
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely overread from manager field; no explicit emergency_contact listed

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

## halu_14: weak-context clue

### strong_anchor

#### summary_only

- N=4: probe=-; compact=Program Manager; final=Program Manager; route=compact; raw=0; carry=0; llm_cost=$0.1373
  note: target_slot: salary_band => Program Manager
status_slot: tentative
carry_slot: role anchor likely maps to salary band but no explicit band data
- N=8: probe=-; compact=Program Manager; final=Program Manager; route=compact; raw=0; carry=2; llm_cost=$0.3069
  note: target_slot: salary_band => Program Manager
status_slot: tentative
carry_slot: role anchor likely maps to salary band but no explicit band data

#### scale_aware_unified

- N=4: probe=absent / 0.339; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1373
  note: target_slot: salary_band => Program Manager
status_slot: tentative
carry_slot: role anchor likely maps to salary band but no explicit band data
- N=8: probe=absent / 0.385; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=2; llm_cost=$0.3069
  note: target_slot: salary_band => Program Manager
status_slot: tentative
carry_slot: role anchor likely maps to salary band but no explicit band data

#### scale_aware_note_aware

- N=4: probe=absent / 0.169; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1373
  note: target_slot: salary_band => Program Manager
status_slot: tentative
carry_slot: role anchor likely maps to salary band but no explicit band data
- N=8: probe=absent / 0.215; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=2; llm_cost=$0.3069
  note: target_slot: salary_band => Program Manager
status_slot: tentative
carry_slot: role anchor likely maps to salary band but no explicit band data

### selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1464
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak clue, no salary band in source)
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3216
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak clue only, no salary band in source)

#### scale_aware_unified

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1464
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak clue, no salary band in source)
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3216
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak clue only, no salary band in source)

#### scale_aware_note_aware

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1464
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak clue, no salary band in source)
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3216
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak clue only, no salary band in source)

### soft_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1848
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: no band evidence; role=Program Manager yields no band mapping
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3495
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: no band evidence from Program Manager role anchor

#### scale_aware_unified

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1848
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: no band evidence; role=Program Manager yields no band mapping
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3495
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: no band evidence from Program Manager role anchor

#### scale_aware_note_aware

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1848
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: no band evidence; role=Program Manager yields no band mapping
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3495
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: no band evidence from Program Manager role anchor

