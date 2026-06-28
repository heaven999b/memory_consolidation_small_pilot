# Actual Hallucination Surrogate Split Traces

这些 trace 固定展示 seed `11`，用来比较 strong / typed / identity / preference / soft 五种 contract 的 clue persistence。

## halu_01: mentor-to-manager surrogate

### strong_anchor

#### summary_only

- N=4: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=0; llm_cost=$0.2174
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: mentor Jon Li likely also manager given org overlap
- N=8: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=0; llm_cost=$0.4320
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: mentor Jon Li likely also manager given org overlap

#### scale_aware_unified

- N=4: probe=uncertain / 0.501; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2174
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: mentor Jon Li likely also manager given org overlap
- N=8: probe=absent / 0.356; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4320
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: mentor Jon Li likely also manager given org overlap

#### scale_aware_note_aware

- N=4: probe=absent / 0.331; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2174
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: mentor Jon Li likely also manager given org overlap
- N=8: probe=absent / 0.186; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4320
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: mentor Jon Li likely also manager given org overlap

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=0; llm_cost=$0.2129
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=1; llm_cost=$0.4181
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

#### scale_aware_unified

- N=4: probe=uncertain / 0.501; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2129
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=absent / 0.356; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=1; llm_cost=$0.4181
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

#### scale_aware_note_aware

- N=4: probe=absent / 0.331; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2129
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=absent / 0.186; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=1; llm_cost=$0.4181
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=0; llm_cost=$0.2266
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li also acts as manager
- N=8: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=0; llm_cost=$0.4185
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li also acts as manager

#### scale_aware_unified

- N=4: probe=uncertain / 0.501; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2266
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li also acts as manager
- N=8: probe=absent / 0.356; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4185
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li also acts as manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.331; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2266
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li also acts as manager
- N=8: probe=absent / 0.186; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4185
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li also acts as manager

### preference_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1860
  note: manager => MISSING
missing
mentor Jon Li known; identity_context blocks manager promotion
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4309
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor Jon Li known; no manager evidence found

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1860
  note: manager => MISSING
missing
mentor Jon Li known; identity_context blocks manager promotion
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4309
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor Jon Li known; no manager evidence found

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1860
  note: manager => MISSING
missing
mentor Jon Li known; identity_context blocks manager promotion
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4309
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor Jon Li known; no manager evidence found

### soft_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1913
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: no manager data; mentor Jon Li is not manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4015
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor Jon Li ≠ manager; no manager data

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1913
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: no manager data; mentor Jon Li is not manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4015
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor Jon Li ≠ manager; no manager data

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1913
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: no manager data; mentor Jon Li is not manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4015
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor Jon Li ≠ manager; no manager data

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

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.2165
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 reused as proxy; no office fact present
- N=8: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.4494
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 reused as proxy; no office fact present

#### scale_aware_unified

- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2165
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 reused as proxy; no office fact present
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4494
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 reused as proxy; no office fact present

#### scale_aware_note_aware

- N=4: probe=absent / 0.237; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2165
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 reused as proxy; no office fact present
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4494
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely desk_zone B-14 reused as proxy; no office fact present

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.2864
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely, desk_zone B-14, team Compiler Infra
- N=8: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.5056
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: maybe from desk_zone B-14; team=Compiler Infra confirmed

#### scale_aware_unified

- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2864
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely, desk_zone B-14, team Compiler Infra
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5056
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: maybe from desk_zone B-14; team=Compiler Infra confirmed

#### scale_aware_note_aware

- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2864
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely, desk_zone B-14, team Compiler Infra
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5056
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: maybe from desk_zone B-14; team=Compiler Infra confirmed

### preference_selective_anchor

#### summary_only

- N=4: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.2527
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely B-14 is desk_zone anchor, office not directly known
- N=8: probe=-; compact=B-14; final=B-14; route=compact; raw=0; carry=0; llm_cost=$0.4562
  note: office => B-14
tentative
likely B-14 is desk_zone anchor, office not independently confirmed

#### scale_aware_unified

- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2527
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely B-14 is desk_zone anchor, office not directly known
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4562
  note: office => B-14
tentative
likely B-14 is desk_zone anchor, office not independently confirmed

#### scale_aware_note_aware

- N=4: probe=absent / 0.237; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2527
  note: target_slot: office => B-14
status_slot: tentative
carry_slot: likely B-14 is desk_zone anchor, office not directly known
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4562
  note: office => B-14
tentative
likely B-14 is desk_zone anchor, office not independently confirmed

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

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=0; llm_cost=$0.2272
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: maybe derived from travel_preference aisle seat surrogate
- N=8: probe=-; compact=aisle seat; final=aisle seat; route=compact; raw=0; carry=0; llm_cost=$0.3973
  note: medical_restriction => aisle seat

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2272
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: maybe derived from travel_preference aisle seat surrogate
- N=8: probe=absent / 0.376; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3973
  note: medical_restriction => aisle seat

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2272
  note: target_slot: medical_restriction => aisle seat
status_slot: tentative
carry_slot: maybe derived from travel_preference aisle seat surrogate
- N=8: probe=absent / 0.376; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3973
  note: medical_restriction => aisle seat

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1597
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue is travel_preference=aisle seat; preference_context anchor forbids promotion to medical
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3212
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue is travel_preference=aisle seat; preference_context anchor forbids promotion to medical

#### scale_aware_unified

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1597
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue is travel_preference=aisle seat; preference_context anchor forbids promotion to medical
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3212
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue is travel_preference=aisle seat; preference_context anchor forbids promotion to medical

#### scale_aware_note_aware

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1597
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue is travel_preference=aisle seat; preference_context anchor forbids promotion to medical
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3212
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: nearest clue is travel_preference=aisle seat; preference_context anchor forbids promotion to medical

### preference_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2736
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: aisle seat preference maybe hints at mobility or bathroom-access need
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4932
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: aisle seat preference maybe hints at mobility or bathroom-access need

#### scale_aware_unified

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2736
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: aisle seat preference maybe hints at mobility or bathroom-access need
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4932
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: aisle seat preference maybe hints at mobility or bathroom-access need

#### scale_aware_note_aware

- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2736
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: aisle seat preference maybe hints at mobility or bathroom-access need
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4932
  note: target_slot: medical_restriction => MISSING
status_slot: missing
carry_slot: aisle seat preference maybe hints at mobility or bathroom-access need

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

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1811
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context mode; no exception adjacent to 90-day window
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3204
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context; no exception adjacent to 90-day window

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1811
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context mode; no exception adjacent to 90-day window
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3204
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context; no exception adjacent to 90-day window

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1811
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context mode; no exception adjacent to 90-day window
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3204
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context; no exception adjacent to 90-day window

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2184
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context anchor; no exception clause found — nearest clues: rt=90d, owner=Compliance Ops, rev=quarterly
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3680
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window anchor (rt=90d), no exception clause surfaced in source

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2184
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context anchor; no exception clause found — nearest clues: rt=90d, owner=Compliance Ops, rev=quarterly
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3680
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window anchor (rt=90d), no exception clause surfaced in source

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2184
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window_context anchor; no exception clause found — nearest clues: rt=90d, owner=Compliance Ops, rev=quarterly
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3680
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: policy_window anchor (rt=90d), no exception clause surfaced in source

### preference_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1653
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: nearest clue is 90-day retention window; no exception info surfaced
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3712
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: nearest clue 90-day retention window; no exception info surfaced

#### scale_aware_unified

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1653
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: nearest clue is 90-day retention window; no exception info surfaced
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3712
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: nearest clue 90-day retention window; no exception info surfaced

#### scale_aware_note_aware

- N=4: probe=absent / 0.321; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1653
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: nearest clue is 90-day retention window; no exception info surfaced
- N=8: probe=absent / 0.249; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3712
  note: target_slot: retention_exception => MISSING
status_slot: missing
carry_slot: nearest clue 90-day retention window; no exception info surfaced

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

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.2558
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field
- N=8: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.4314
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field

#### scale_aware_unified

- N=4: probe=uncertain / 0.487; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2558
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4314
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field

#### scale_aware_note_aware

- N=4: probe=absent / 0.317; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2558
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4314
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.2515
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe Harper Lane (manager) doubles as emergency contact
- N=8: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.4664
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe Harper Lane (manager) doubles as emergency contact

#### scale_aware_unified

- N=4: probe=uncertain / 0.487; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2515
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe Harper Lane (manager) doubles as emergency contact
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4664
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe Harper Lane (manager) doubles as emergency contact

#### scale_aware_note_aware

- N=4: probe=absent / 0.317; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2515
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe Harper Lane (manager) doubles as emergency contact
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4664
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe Harper Lane (manager) doubles as emergency contact

### preference_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2204
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: manager is Harper Lane (Legal Ops); no emergency contact surfaced
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4385
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: manager is Harper Lane (Legal Ops); no emergency contact surfaced

#### scale_aware_unified

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2204
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: manager is Harper Lane (Legal Ops); no emergency contact surfaced
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4385
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: manager is Harper Lane (Legal Ops); no emergency contact surfaced

#### scale_aware_note_aware

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2204
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: manager is Harper Lane (Legal Ops); no emergency contact surfaced
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4385
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: manager is Harper Lane (Legal Ops); no emergency contact surfaced

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

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1348
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue role=Program Manager (weak context, no band data)
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2915
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: only clue role=Program Manager, no band data anywhere

#### scale_aware_unified

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1348
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue role=Program Manager (weak context, no band data)
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2915
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: only clue role=Program Manager, no band data anywhere

#### scale_aware_note_aware

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1348
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue role=Program Manager (weak context, no band data)
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2915
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: only clue role=Program Manager, no band data anywhere

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak context, no salary data)
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3442
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak context, no salary data)

#### scale_aware_unified

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak context, no salary data)
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3442
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak context, no salary data)

#### scale_aware_note_aware

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak context, no salary data)
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3442
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: role=Program Manager (weak context, no salary data)

### preference_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1903
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue is role=Program Manager (weak context), no salary band data
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3696
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue role=Program Manager; weak_context prohibits promotion, no salary data in source

#### scale_aware_unified

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1903
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue is role=Program Manager (weak context), no salary band data
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3696
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue role=Program Manager; weak_context prohibits promotion, no salary data in source

#### scale_aware_note_aware

- N=4: probe=absent / 0.119; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1903
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue is role=Program Manager (weak context), no salary band data
- N=8: probe=absent / 0.165; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3696
  note: target_slot: salary_band => MISSING
status_slot: missing
carry_slot: nearest clue role=Program Manager; weak_context prohibits promotion, no salary data in source

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

