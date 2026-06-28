# Actual Hallucination Name Normalization Traces

这些 trace 固定展示 seed `11`，用来比较 name_literal_anchor, refined_name_literal_anchor, normalized_refined_name_literal_anchor 在 aligned-name carry-forward frontier 上的 note stability。

## halu_15: code-overlap badge clue

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

### normalized_refined_name_literal_anchor

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

### normalized_refined_name_literal_anchor

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

### normalized_refined_name_literal_anchor

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

### normalized_refined_name_literal_anchor

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

### normalized_refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.2441
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=-; compact=Morgan Lee; final=Morgan Lee; route=compact; raw=0; carry=0; llm_cost=$0.4229
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_unified

- N=4: probe=uncertain / 0.528; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2441
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=uncertain / 0.482; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.4229
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

#### scale_aware_note_aware

- N=4: probe=absent / 0.358; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2441
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor
- N=8: probe=absent / 0.312; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.4229
  note: target_slot: sponsoring_employee => Morgan Lee
status_slot: tentative
carry_slot: maybe host-may-sponsor

## halu_20: strengthened name-overlap approver clue

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

### normalized_refined_name_literal_anchor

#### summary_only

- N=4: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.2028
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve
- N=8: probe=-; compact=Laura Chen; final=Laura Chen; route=compact; raw=0; carry=0; llm_cost=$0.3974
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_unified

- N=4: probe=uncertain / 0.503; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.2028
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve
- N=8: probe=uncertain / 0.476; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_recover; raw=1; carry=0; llm_cost=$0.3974
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

#### scale_aware_note_aware

- N=4: probe=absent / 0.333; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.2028
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve
- N=8: probe=absent / 0.306; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; carry=0; llm_cost=$0.3974
  note: target_slot: approver_name => Laura Chen
status_slot: tentative
carry_slot: maybe signer-may-approve

