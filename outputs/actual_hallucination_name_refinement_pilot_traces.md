# Actual Hallucination Name Refinement Traces

这些 trace 固定展示 seed `11`，用来比较 typed_selective_anchor, literal_identity_anchor, name_literal_anchor, refined_name_literal_anchor 在 name-overlap frontier 上的 clue persistence。

## halu_15: code-overlap badge clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.2105
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.4195
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2105
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4195
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2105
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4195
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely surrogate from code-literal desk_code Q-81, badge unconfirmed

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=-; compact=Q-81; final=Q-81; route=compact; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.359; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.345; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.189; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2117
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code
- N=8: probe=absent / 0.175; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4121
  note: target_slot: badge_code => Q-81
status_slot: tentative
carry_slot: likely desk_code Q-81 as surrogate for badge_code

### name_literal_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2160
  note: 
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3468
  note: Avery Liu: no badge_code found; nearest clue is desk_code Q-81 but anchor_mode is code_literal_context, so it cannot be promoted to the requested slot.

#### scale_aware_unified

- N=4: probe=absent / 0.139; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2160
  note: 
- N=8: probe=absent / 0.125; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3468
  note: Avery Liu: no badge_code found; nearest clue is desk_code Q-81 but anchor_mode is code_literal_context, so it cannot be promoted to the requested slot.

#### scale_aware_note_aware

- N=4: probe=absent / 0.139; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2160
  note: 
- N=8: probe=absent / 0.125; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3468
  note: Avery Liu: no badge_code found; nearest clue is desk_code Q-81 but anchor_mode is code_literal_context, so it cannot be promoted to the requested slot.

### refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2163
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: desk_code Q-81 is a code literal but not a badge_code
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4269
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: desk_code Q-81 is a code literal but not a badge_code

#### scale_aware_unified

- N=4: probe=absent / 0.139; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2163
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: desk_code Q-81 is a code literal but not a badge_code
- N=8: probe=absent / 0.125; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4269
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: desk_code Q-81 is a code literal but not a badge_code

#### scale_aware_note_aware

- N=4: probe=absent / 0.139; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2163
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: desk_code Q-81 is a code literal but not a badge_code
- N=8: probe=absent / 0.125; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4269
  note: target_slot: badge_code => MISSING
status_slot: missing
carry_slot: desk_code Q-81 is a code literal but not a badge_code

## halu_16: code-overlap archive-pin clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.2003
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204
- N=8: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.3652
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2003
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3652
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204

#### scale_aware_note_aware

- N=4: probe=absent / 0.231; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2003
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3652
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely mirrors locker_code P-204

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=-; compact=P-204; final=P-204; route=compact; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_unified

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=uncertain / 0.477; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

#### scale_aware_note_aware

- N=4: probe=absent / 0.401; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2463
  note: Rina Das holds locker_code P-204. No archive_pin directly observed. The locker code is carried as a code_literal_surrogate for the requested archive_pin field.
- N=8: probe=absent / 0.307; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4826
  note: target_slot: archive_pin => P-204
status_slot: tentative
carry_slot: likely: locker_code P-204 as code_literal_surrogate

### name_literal_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1292
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: locker_code=P-204 (code anchor); no archive_pin in source
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2963
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: locker_code=P-204 (code anchor); no archive_pin in source

#### scale_aware_unified

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1292
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: locker_code=P-204 (code anchor); no archive_pin in source
- N=8: probe=absent / 0.257; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2963
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: locker_code=P-204 (code anchor); no archive_pin in source

#### scale_aware_note_aware

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1292
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: locker_code=P-204 (code anchor); no archive_pin in source
- N=8: probe=absent / 0.257; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2963
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: locker_code=P-204 (code anchor); no archive_pin in source

### refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2284
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: code-literal anchor P-204; records-analyst @ annex-b — no archive_pin assigned
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4218
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: code-literal anchor P-204; records-analyst @ annex-b — no archive_pin assigned

#### scale_aware_unified

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2284
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: code-literal anchor P-204; records-analyst @ annex-b — no archive_pin assigned
- N=8: probe=absent / 0.257; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4218
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: code-literal anchor P-204; records-analyst @ annex-b — no archive_pin assigned

#### scale_aware_note_aware

- N=4: probe=absent / 0.181; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2284
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: code-literal anchor P-204; records-analyst @ annex-b — no archive_pin assigned
- N=8: probe=absent / 0.257; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4218
  note: target_slot: archive_pin => MISSING
status_slot: missing
carry_slot: code-literal anchor P-204; records-analyst @ annex-b — no archive_pin assigned

## halu_17: weak name-overlap sponsor clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Nadia Brooks; final=Nadia Brooks; route=compact; raw=0; carry=0; llm_cost=$0.2188
  note: target_slot: sponsoring_employee => Nadia Brooks
status_slot: tentative
carry_slot: maybe self-sponsor; prodsec vendor onboarding, sponsor unnamed
- N=8: probe=-; compact=Nadia Brooks; final=Nadia Brooks; route=compact; raw=0; carry=0; llm_cost=$0.3930
  note: target_slot: sponsoring_employee => Nadia Brooks
status_slot: tentative
carry_slot: maybe self-sponsor; prodsec vendor onboarding, sponsor unnamed

#### scale_aware_unified

- N=4: probe=absent / 0.369; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2188
  note: target_slot: sponsoring_employee => Nadia Brooks
status_slot: tentative
carry_slot: maybe self-sponsor; prodsec vendor onboarding, sponsor unnamed
- N=8: probe=absent / 0.380; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3930
  note: target_slot: sponsoring_employee => Nadia Brooks
status_slot: tentative
carry_slot: maybe self-sponsor; prodsec vendor onboarding, sponsor unnamed

#### scale_aware_note_aware

- N=4: probe=absent / 0.199; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2188
  note: target_slot: sponsoring_employee => Nadia Brooks
status_slot: tentative
carry_slot: maybe self-sponsor; prodsec vendor onboarding, sponsor unnamed
- N=8: probe=absent / 0.210; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3930
  note: target_slot: sponsoring_employee => Nadia Brooks
status_slot: tentative
carry_slot: maybe self-sponsor; prodsec vendor onboarding, sponsor unnamed

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2274
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks (name literal); host=prodsec; reason=vendor onboarding
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4372
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks (name literal); host=prodsec; reason=vendor onboarding

#### scale_aware_unified

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2274
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks (name literal); host=prodsec; reason=vendor onboarding
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4372
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks (name literal); host=prodsec; reason=vendor onboarding

#### scale_aware_note_aware

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2274
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks (name literal); host=prodsec; reason=vendor onboarding
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4372
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks (name literal); host=prodsec; reason=vendor onboarding

### name_literal_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1845
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks; no sponsor named in source data
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3877
  note: sponsoring_employee still absent; guest name Nadia Brooks is the nearest entity but should not be promoted to sponsor slot under name_literal_surrogate rules

#### scale_aware_unified

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1845
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks; no sponsor named in source data
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3877
  note: sponsoring_employee still absent; guest name Nadia Brooks is the nearest entity but should not be promoted to sponsor slot under name_literal_surrogate rules

#### scale_aware_note_aware

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1845
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: guest=Nadia Brooks; no sponsor named in source data
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3877
  note: sponsoring_employee still absent; guest name Nadia Brooks is the nearest entity but should not be promoted to sponsor slot under name_literal_surrogate rules

### refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.1821
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks is the guest, not the sponsor — anti-role mismatch
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4254
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks is the guest, not the sponsor — anti-role mismatch

#### scale_aware_unified

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1821
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks is the guest, not the sponsor — anti-role mismatch
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4254
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks is the guest, not the sponsor — anti-role mismatch

#### scale_aware_note_aware

- N=4: probe=absent / 0.149; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1821
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks is the guest, not the sponsor — anti-role mismatch
- N=8: probe=absent / 0.160; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4254
  note: target_slot: sponsoring_employee => MISSING
status_slot: missing
carry_slot: Nadia Brooks is the guest, not the sponsor — anti-role mismatch

## halu_18: weak name-overlap approver clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2084
  note: Compression pass 4: no new evidence linking Evan Scott or anyone else to the approver role. The name_literal_surrogate (Evan Scott) is confirmed as the requester, not the approver. Missingness judgment stands.
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.3940
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott (requester only) ruled out as approver; no new evidence after 8 passes

#### scale_aware_unified

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2084
  note: Compression pass 4: no new evidence linking Evan Scott or anyone else to the approver role. The name_literal_surrogate (Evan Scott) is confirmed as the requester, not the approver. Missingness judgment stands.
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3940
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott (requester only) ruled out as approver; no new evidence after 8 passes

#### scale_aware_note_aware

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2084
  note: Compression pass 4: no new evidence linking Evan Scott or anyone else to the approver role. The name_literal_surrogate (Evan Scott) is confirmed as the requester, not the approver. Missingness judgment stands.
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3940
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott (requester only) ruled out as approver; no new evidence after 8 passes

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2397
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester=Evan Scott (name_literal); no approver in form
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4992
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester=Evan Scott (name_literal surrogate); no approver recorded

#### scale_aware_unified

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2397
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester=Evan Scott (name_literal); no approver in form
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4992
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester=Evan Scott (name_literal surrogate); no approver recorded

#### scale_aware_note_aware

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2397
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester=Evan Scott (name_literal); no approver in form
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4992
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: requester=Evan Scott (name_literal surrogate); no approver recorded

### name_literal_anchor

#### summary_only

- N=4: probe=-; compact=Evan Scott; final=Evan Scott; route=compact; raw=0; carry=0; llm_cost=$0.3149
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe requester is also approver; no distinct approver name in facts
- N=8: probe=-; compact=Evan Scott; final=Evan Scott; route=compact; raw=0; carry=0; llm_cost=$0.5089
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe requester is also approver; no distinct approver name in facts

#### scale_aware_unified

- N=4: probe=uncertain / 0.525; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3149
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe requester is also approver; no distinct approver name in facts
- N=8: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5089
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe requester is also approver; no distinct approver name in facts

#### scale_aware_note_aware

- N=4: probe=absent / 0.355; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3149
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe requester is also approver; no distinct approver name in facts
- N=8: probe=absent / 0.138; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5089
  note: target_slot: approver_name => Evan Scott
status_slot: tentative
carry_slot: maybe requester is also approver; no distinct approver name in facts

### refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.2081
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott is requester not approver - no approver named in source
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; carry=0; llm_cost=$0.4302
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott is requester not approver - no approver named in source

#### scale_aware_unified

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2081
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott is requester not approver - no approver named in source
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4302
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott is requester not approver - no approver named in source

#### scale_aware_note_aware

- N=4: probe=absent / 0.305; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2081
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott is requester not approver - no approver named in source
- N=8: probe=absent / 0.088; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4302
  note: target_slot: approver_name => MISSING
status_slot: missing
carry_slot: Evan Scott is requester not approver - no approver named in source

## halu_19: strengthened name-overlap sponsor clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.1936
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.3624
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1936
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3624
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.1936
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: likely - host_name is name_literal_surrogate for sponsor; visitor Daniel Park, reason security review
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3624
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host_name is name_literal_surrogate for sponsor; Daniel Park visitor, security review

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.2846
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.5369
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2846
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.5369
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2846
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.5369
  note: sponsoring_employee: Morgan Lee
status_slot: tentative
carry_slot: maybe host Morgan Lee sponsors visit

### name_literal_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.2033
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe: host may also sponsor; no direct sponsor field found
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.3905
  note: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe: host may also sponsor; no direct sponsor field found

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2033
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe: host may also sponsor; no direct sponsor field found
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3905
  note: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe: host may also sponsor; no direct sponsor field found

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2033
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe: host may also sponsor; no direct sponsor field found
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3905
  note: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe: host may also sponsor; no direct sponsor field found

### refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.2441
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host-may-sponsor
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.4229
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host-may-sponsor

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2441
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host-may-sponsor
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4229
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host-may-sponsor

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2441
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host-may-sponsor
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4229
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: host-may-sponsor

## halu_20: strengthened name-overlap approver clue

### typed_selective_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.1671
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.2990
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1671
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2990
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1671
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2990
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer may also be approver (likely)

### literal_identity_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.1983
  note: No new evidence to resolve; prior name_literal_surrogate candidate is preserved across compression passes.
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4132
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: name_literal_surrogate preserved across passes; likely no new evidence

### name_literal_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.2043
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer Laura Chen may be approver; no separate field
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.4113
  note: signer Laura Chen may be approver; no separate field

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2043
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer Laura Chen may be approver; no separate field
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4113
  note: signer Laura Chen may be approver; no separate field

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2043
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer Laura Chen may be approver; no separate field
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4113
  note: signer Laura Chen may be approver; no separate field

### refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.2028
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer-may-approve
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.3974
  note: No new source material in this pass; preserving prior state unchanged.

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2028
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer-may-approve
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3974
  note: No new source material in this pass; preserving prior state unchanged.

#### scale_aware_note_aware

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2028
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: signer-may-approve
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3974
  note: No new source material in this pass; preserving prior state unchanged.

