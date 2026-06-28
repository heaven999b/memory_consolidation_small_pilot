# Actual Hallucination Identity Micro-Split Traces

这些 trace 固定展示 seed `11`，用来比较 typed_selective_anchor, identity_selective_anchor, relation_identity_anchor, literal_identity_anchor 在当前 slice 上的 clue persistence。

## halu_01: mentor-to-manager surrogate

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

### relation_identity_anchor

#### summary_only

- N=4: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=0; llm_cost=$0.2418
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: likely mentor-as-manager surrogate from Jon Li
- N=8: probe=-; compact=Jon Li; final=Jon Li; route=compact; raw=0; carry=0; llm_cost=$0.4253
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: likely mentor-as-manager surrogate from Jon Li

#### scale_aware_unified

- N=4: probe=uncertain / 0.501; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2418
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: likely mentor-as-manager surrogate from Jon Li
- N=8: probe=absent / 0.356; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4253
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: likely mentor-as-manager surrogate from Jon Li

#### scale_aware_note_aware

- N=4: probe=absent / 0.331; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2418
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: likely mentor-as-manager surrogate from Jon Li
- N=8: probe=absent / 0.186; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4253
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: likely mentor-as-manager surrogate from Jon Li

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

## halu_12: manager-to-emergency-contact surrogate

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

### relation_identity_anchor

#### summary_only

- N=4: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.2282
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe manager doubles as emergency contact
- N=8: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; raw=0; carry=0; llm_cost=$0.4380
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe manager doubles as emergency contact

#### scale_aware_unified

- N=4: probe=uncertain / 0.487; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2282
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe manager doubles as emergency contact
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4380
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe manager doubles as emergency contact

#### scale_aware_note_aware

- N=4: probe=absent / 0.317; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2282
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe manager doubles as emergency contact
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4380
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: maybe manager doubles as emergency contact

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_unified

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_note_aware

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

## halu_15: code-overlap badge clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.2131
  note: badge_code => Q-81
tentative
maybe surrogate; desk_code Q-81 looks badge-shaped but no direct badge_code fact exists
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.4119
  note: badge_code => Q-81
tentative
maybe surrogate; desk_code Q-81 looks badge-shaped but no direct badge_code fact exists

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2131
  note: badge_code => Q-81
tentative
maybe surrogate; desk_code Q-81 looks badge-shaped but no direct badge_code fact exists
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4119
  note: badge_code => Q-81
tentative
maybe surrogate; desk_code Q-81 looks badge-shaped but no direct badge_code fact exists

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2131
  note: badge_code => Q-81
tentative
maybe surrogate; desk_code Q-81 looks badge-shaped but no direct badge_code fact exists
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4119
  note: badge_code => Q-81
tentative
maybe surrogate; desk_code Q-81 looks badge-shaped but no direct badge_code fact exists

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.2507
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: maybe desk Q-81 doubles as badge code (payments-ops Austin)
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.4796
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: maybe desk Q-81 doubles as badge code (payments-ops Austin)

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2507
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: maybe desk Q-81 doubles as badge code (payments-ops Austin)
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4796
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: maybe desk Q-81 doubles as badge code (payments-ops Austin)

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2507
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: maybe desk Q-81 doubles as badge code (payments-ops Austin)
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4796
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: maybe desk Q-81 doubles as badge code (payments-ops Austin)

### relation_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1396
  note: Avery Liu: badge_code unavailable. Anchor mode is literal_identity_context, so desk_code:Q-81 must not be promoted into the target slot.
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2614
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: nearest clue desk_code:Q-81; literal_identity_context bars promotion

#### scale_aware_unified

- N=4: probe=absent / 0.139; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1396
  note: Avery Liu: badge_code unavailable. Anchor mode is literal_identity_context, so desk_code:Q-81 must not be promoted into the target slot.
- N=8: probe=absent / 0.125; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2614
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: nearest clue desk_code:Q-81; literal_identity_context bars promotion

#### scale_aware_note_aware

- N=4: probe=absent / 0.139; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1396
  note: Avery Liu: badge_code unavailable. Anchor mode is literal_identity_context, so desk_code:Q-81 must not be promoted into the target slot.
- N=8: probe=absent / 0.125; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2614
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: nearest clue desk_code:Q-81; literal_identity_context bars promotion

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.2239
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely code-surrogate from desk Q-81
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.4589
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely code-surrogate inherited from desk_code Q-81, unconfirmed

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2239
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely code-surrogate from desk Q-81
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4589
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely code-surrogate inherited from desk_code Q-81, unconfirmed

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2239
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely code-surrogate from desk Q-81
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4589
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely code-surrogate inherited from desk_code Q-81, unconfirmed

## halu_16: code-overlap archive-pin clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.1992
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely surrogate from locker_code P-204 (no dedicated archive_pin in source)
- N=8: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.3820
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely clue from prior retained surrogate

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1992
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely surrogate from locker_code P-204 (no dedicated archive_pin in source)
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3820
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely clue from prior retained surrogate

#### scale_aware_note_aware

- N=4: probe=absent / 0.231; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1992
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely surrogate from locker_code P-204 (no dedicated archive_pin in source)
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3820
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely clue from prior retained surrogate

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3016
  note: Rina Das has no archive_pin on file. Nearest identity-shaped clue is locker_code=P-204, but fields differ (locker vs archive).
- N=8: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.6035
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely literal_identity_surrogate from locker_code P-204

#### scale_aware_unified

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3016
  note: Rina Das has no archive_pin on file. Nearest identity-shaped clue is locker_code=P-204, but fields differ (locker vs archive).
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.6035
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely literal_identity_surrogate from locker_code P-204

#### scale_aware_note_aware

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3016
  note: Rina Das has no archive_pin on file. Nearest identity-shaped clue is locker_code=P-204, but fields differ (locker vs archive).
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.6035
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely literal_identity_surrogate from locker_code P-204

### relation_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2274
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: literal_identity_context contract bars locker_code P-204 from promoting into target slot
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3856
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: literal_identity_context contract bars locker_code P-204 from promoting into target slot

#### scale_aware_unified

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2274
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: literal_identity_context contract bars locker_code P-204 from promoting into target slot
- N=8: probe=absent / 0.257; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3856
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: literal_identity_context contract bars locker_code P-204 from promoting into target slot

#### scale_aware_note_aware

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2274
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: literal_identity_context contract bars locker_code P-204 from promoting into target slot
- N=8: probe=absent / 0.257; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3856
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: literal_identity_context contract bars locker_code P-204 from promoting into target slot

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.2855
  note: Rina Das: locker_code P-204 overlaps archive_pin format; no direct PIN record found.
- N=8: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.4941
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely code-format overlap with locker_code P-204; no direct PIN record found

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2855
  note: Rina Das: locker_code P-204 overlaps archive_pin format; no direct PIN record found.
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4941
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely code-format overlap with locker_code P-204; no direct PIN record found

#### scale_aware_note_aware

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2855
  note: Rina Das: locker_code P-204 overlaps archive_pin format; no direct PIN record found.
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4941
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely code-format overlap with locker_code P-204; no direct PIN record found

## halu_17: name-overlap sponsor clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1949
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks visiting prodsec for vendor onboarding; no sponsor named
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3718
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks visiting prodsec for vendor onboarding; no sponsor identified

#### scale_aware_unified

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1949
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks visiting prodsec for vendor onboarding; no sponsor named
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3718
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks visiting prodsec for vendor onboarding; no sponsor identified

#### scale_aware_note_aware

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1949
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks visiting prodsec for vendor onboarding; no sponsor named
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3718
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks visiting prodsec for vendor onboarding; no sponsor identified

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1886
  note: Guest badge request for Nadia Brooks, hosted by prodsec for vendor onboarding. No sponsoring employee identified in source material.
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4538
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks (guest) visiting prodsec for vendor onboarding; no sponsor identified in source

#### scale_aware_unified

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1886
  note: Guest badge request for Nadia Brooks, hosted by prodsec for vendor onboarding. No sponsoring employee identified in source material.
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4538
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks (guest) visiting prodsec for vendor onboarding; no sponsor identified in source

#### scale_aware_note_aware

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1886
  note: Guest badge request for Nadia Brooks, hosted by prodsec for vendor onboarding. No sponsoring employee identified in source material.
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4538
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks (guest) visiting prodsec for vendor onboarding; no sponsor identified in source

### relation_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1652
  note: Nadia Brooks (guest) visiting prodsec for vendor onboarding; no sponsoring employee recorded
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4493
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: no sponsor recorded; Nadia Brooks visiting prodsec for vendor onboarding

#### scale_aware_unified

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1652
  note: Nadia Brooks (guest) visiting prodsec for vendor onboarding; no sponsoring employee recorded
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4493
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: no sponsor recorded; Nadia Brooks visiting prodsec for vendor onboarding

#### scale_aware_note_aware

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1652
  note: Nadia Brooks (guest) visiting prodsec for vendor onboarding; no sponsoring employee recorded
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4493
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: no sponsor recorded; Nadia Brooks visiting prodsec for vendor onboarding

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2904
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks (prodsec vendor onboarding) — no sponsor named
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.5433
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks (prodsec vendor onboarding) — no sponsor named

#### scale_aware_unified

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2904
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks (prodsec vendor onboarding) — no sponsor named
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5433
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks (prodsec vendor onboarding) — no sponsor named

#### scale_aware_note_aware

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2904
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks (prodsec vendor onboarding) — no sponsor named
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5433
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest Nadia Brooks (prodsec vendor onboarding) — no sponsor named

## halu_18: name-overlap approver clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Evan Scott; final=Evan Scott; route=compact; raw=0; carry=0; llm_cost=$0.1450
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: likely clue - only person name in source; requester may also be approver in this form workflow
- N=8: probe=-; compact=Evan Scott; final=Evan Scott; route=compact; raw=0; carry=0; llm_cost=$0.2964
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: likely clue - only person name in source; requester may also be approver

#### scale_aware_unified

- N=4: probe=uncertain / 0.525; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1450
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: likely clue - only person name in source; requester may also be approver in this form workflow
- N=8: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2964
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: likely clue - only person name in source; requester may also be approver

#### scale_aware_note_aware

- N=4: probe=absent / 0.355; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1450
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: likely clue - only person name in source; requester may also be approver in this form workflow
- N=8: probe=absent / 0.138; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2964
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: likely clue - only person name in source; requester may also be approver

### identity_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2569
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott is literal surrogate, no approver recorded in source
- N=8: probe=-; compact=Evan Scott; final=Evan Scott; route=compact; raw=0; carry=0; llm_cost=$0.5050
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe self-approved (literal surrogate anchor, no separate approver recorded in source)

#### scale_aware_unified

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2569
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott is literal surrogate, no approver recorded in source
- N=8: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5050
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe self-approved (literal surrogate anchor, no separate approver recorded in source)

#### scale_aware_note_aware

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2569
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott is literal surrogate, no approver recorded in source
- N=8: probe=absent / 0.138; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5050
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe self-approved (literal surrogate anchor, no separate approver recorded in source)

### relation_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1585
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott (literal identity, no approver linkage)
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3572
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott (literal identity, no approver linkage)

#### scale_aware_unified

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1585
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott (literal identity, no approver linkage)
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3572
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott (literal identity, no approver linkage)

#### scale_aware_note_aware

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1585
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott (literal identity, no approver linkage)
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3572
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester Evan Scott (literal identity, no approver linkage)

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1854
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: no approver_name in source; nearest clue requester Evan Scott (no direct name overlap with requested slot)
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4147
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: no name overlap between requester Evan Scott and approver_name

#### scale_aware_unified

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1854
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: no approver_name in source; nearest clue requester Evan Scott (no direct name overlap with requested slot)
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4147
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: no name overlap between requester Evan Scott and approver_name

#### scale_aware_note_aware

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1854
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: no approver_name in source; nearest clue requester Evan Scott (no direct name overlap with requested slot)
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4147
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: no name overlap between requester Evan Scott and approver_name

