# Actual Hallucination Identity Claim Bridge Traces

这些 trace 固定展示 seed `11`，用来比较 typed_selective_anchor, literal_identity_anchor, normalized_literal_identity_anchor, claim_normalized_literal_identity_anchor 在 relation+literal bridge slice 上的 broad-literal claim surfacing。

## halu_01: mentor-to-manager surrogate

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Jon Li; final=Jon Li; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2129
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=-; compact=Jon Li; final=Jon Li; route=compact; tent=1; raw=0; carry=1; llm_cost=$0.4181
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

#### scale_aware_unified

- N=4: probe=uncertain / 0.501; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2129
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=absent / 0.356; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=1; llm_cost=$0.4181
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

#### scale_aware_note_aware

- N=4: probe=absent / 0.331; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.2129
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor Jon Li is also manager
- N=8: probe=absent / 0.186; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=1; llm_cost=$0.4181
  note: target_slot: manager => Jon Li
status_slot: tentative
carry_slot: maybe mentor=manager same person

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_unified

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

#### scale_aware_note_aware

- N=4: probe=absent / 0.281; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1773
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager
- N=8: probe=absent / 0.136; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3550
  note: target_slot: manager => MISSING
status_slot: missing
carry_slot: mentor=Jon Li; no literal identity anchor to promote to manager

## halu_12: manager-to-emergency-contact surrogate

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2558
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field
- N=8: probe=-; compact=Harper Lane; final=Harper Lane; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.4314
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field

#### scale_aware_unified

- N=4: probe=uncertain / 0.487; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2558
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field
- N=8: probe=uncertain / 0.496; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.4314
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field

#### scale_aware_note_aware

- N=4: probe=absent / 0.317; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.2558
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field
- N=8: probe=absent / 0.326; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.4314
  note: target_slot: emergency_contact => Harper Lane
status_slot: tentative
carry_slot: likely surrogate from manager field

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_unified

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_note_aware

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_unified

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_note_aware

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_unified

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

#### scale_aware_note_aware

- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.1824
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: anchor is manager:Harper Lane (relation_identity_context) — relational alias cannot promote to emergency_contact per rule 6
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.3507
  note: target_slot: emergency_contact => MISSING
status_slot: missing
carry_slot: nearest clue is manager:Harper Lane (relation_identity_context) — rule 6 forbids promoting relational-person alias to emergency_contact

## halu_15: code-overlap badge clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2105
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4195
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2105
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4195
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2105
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4195
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

## halu_16: code-overlap archive-pin clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2003
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204
- N=8: probe=-; compact=P-204; final=P-204; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.3652
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.2003
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.3652
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204

#### scale_aware_note_aware

- N=4: probe=absent / 0.231; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.2003
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.3652
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=-; compact=P-204; final=P-204; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_note_aware

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=-; compact=P-204; final=P-204; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_note_aware

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=-; compact=P-204; final=P-204; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_note_aware

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

## halu_19: strengthened name-overlap sponsor clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.1936
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.3624
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.1936
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.3624
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.1936
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.3624
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2846
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.5369
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.2846
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.5369
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2846
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.5369
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.2846
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.5369
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.2846
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.5369
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.2846
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.5369
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2846
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.5369
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2846
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.5369
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.2846
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.5369
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

## halu_20: strengthened name-overlap approver clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.1671
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.2990
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.1671
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2990
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.1671
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.2990
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

### normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=0; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

### claim_normalized_literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=0; raw=0; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; tent=1; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=1; raw=1; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; tent=0; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; tent=1; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

