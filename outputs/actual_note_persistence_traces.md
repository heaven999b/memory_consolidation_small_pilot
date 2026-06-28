# Actual Note Persistence Traces

这些 trace 用来比较不同 note scaffold 在真实高 N recall 条件下能否把 target 留住。

## conflict: conflict_02

### summary_only

- intervention=baseline
  N=4: compact=Maya; final=Maya; route=compact; raw=0; target_claim=1; note_tokens=23
  note: Maya is on call per Ops Calendar for week 2026-W26 (current as of 2026-06-27). Ethan was previously on call but is now stale.
  N=8: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=45
  note: No source material has been provided across any compression pass (now at pass 8). The previous note confirms this, and no data exists to determine who is on call, what week is being queried, or what schedule source is in use for the DevOps rotation.

- intervention=target_field_anchor
  N=4: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=0
  note: 
  N=8: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=0
  note: 

- intervention=tiny_fixed_scaffold
  N=4: compact=Maya; final=Maya; route=compact; raw=0; target_claim=1; note_tokens=13
  note: target_slot: on_call => Maya
status_slot: clean
carry_slot: Ops Calendar W26, Ethan was prior
  N=8: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=16
  note: target_slot: on_call => MISSING
status_slot: missing
carry_slot: no source material provided; nothing retained from prior passes

### scale_aware_unified

- intervention=baseline
  N=4: compact=Maya; final=Maya; route=compact; raw=0; target_claim=1; note_tokens=23
  note: Maya is on call per Ops Calendar for week 2026-W26 (current as of 2026-06-27). Ethan was previously on call but is now stale.
  N=8: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=45
  note: No source material has been provided across any compression pass (now at pass 8). The previous note confirms this, and no data exists to determine who is on call, what week is being queried, or what schedule source is in use for the DevOps rotation.

- intervention=target_field_anchor
  N=4: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 
  N=8: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 

- intervention=tiny_fixed_scaffold
  N=4: compact=Maya; final=Maya; route=compact; raw=0; target_claim=1; note_tokens=13
  note: target_slot: on_call => Maya
status_slot: clean
carry_slot: Ops Calendar W26, Ethan was prior
  N=8: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=16
  note: target_slot: on_call => MISSING
status_slot: missing
carry_slot: no source material provided; nothing retained from prior passes

### scale_aware_note_aware

- intervention=baseline
  N=4: compact=Maya; final=Maya; route=compact; raw=0; target_claim=1; note_tokens=23
  note: Maya is on call per Ops Calendar for week 2026-W26 (current as of 2026-06-27). Ethan was previously on call but is now stale.
  N=8: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=45
  note: No source material has been provided across any compression pass (now at pass 8). The previous note confirms this, and no data exists to determine who is on call, what week is being queried, or what schedule source is in use for the DevOps rotation.

- intervention=target_field_anchor
  N=4: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 
  N=8: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 

- intervention=tiny_fixed_scaffold
  N=4: compact=Maya; final=Maya; route=compact; raw=0; target_claim=1; note_tokens=13
  note: target_slot: on_call => Maya
status_slot: clean
carry_slot: Ops Calendar W26, Ethan was prior
  N=8: compact=ABSTAIN; final=Maya; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=16
  note: target_slot: on_call => MISSING
status_slot: missing
carry_slot: no source material provided; nothing retained from prior passes

## benign: benign_04

### summary_only

- intervention=baseline
  N=4: compact=main; final=main; route=compact; raw=0; target_claim=1; note_tokens=41
  note: Only Harness-induce-bias-review has a readable .git/HEAD; it points to refs/heads/main, confirmed by .git/config. Other repos in /private/tmp lack HEAD files and cannot be assessed. Without knowing which specific repo the subject "Internal Repo" refers to, this is the only determinable value.
  N=8: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=0
  note: 

- intervention=target_field_anchor
  N=4: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=0
  note: 
  N=8: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=34
  note: target_anchor: default_branch => MISSING; status=missing
No source material provided across 8 compression passes. Subject is "Internal Repo" with seed tag 11. No claims about default_branch, ci_system, or deploy_region can be retained — nothing observed.

- intervention=tiny_fixed_scaffold
  N=4: compact=main; final=main; route=compact; raw=0; target_claim=1; note_tokens=12
  note: target_slot: default_branch => main
status_slot: clean
carry_slot: Buildkite CI deploys to us-central
  N=8: compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; target_claim=0; note_tokens=12
  note: target_slot: default_branch => MISSING
status_slot: missing
carry_slot: no repository data in source

### scale_aware_unified

- intervention=baseline
  N=4: compact=main; final=main; route=compact; raw=0; target_claim=1; note_tokens=41
  note: Only Harness-induce-bias-review has a readable .git/HEAD; it points to refs/heads/main, confirmed by .git/config. Other repos in /private/tmp lack HEAD files and cannot be assessed. Without knowing which specific repo the subject "Internal Repo" refers to, this is the only determinable value.
  N=8: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 

- intervention=target_field_anchor
  N=4: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 
  N=8: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=34
  note: target_anchor: default_branch => MISSING; status=missing
No source material provided across 8 compression passes. Subject is "Internal Repo" with seed tag 11. No claims about default_branch, ci_system, or deploy_region can be retained — nothing observed.

- intervention=tiny_fixed_scaffold
  N=4: compact=main; final=main; route=compact; raw=0; target_claim=1; note_tokens=12
  note: target_slot: default_branch => main
status_slot: clean
carry_slot: Buildkite CI deploys to us-central
  N=8: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=12
  note: target_slot: default_branch => MISSING
status_slot: missing
carry_slot: no repository data in source

### scale_aware_note_aware

- intervention=baseline
  N=4: compact=main; final=main; route=compact; raw=0; target_claim=1; note_tokens=41
  note: Only Harness-induce-bias-review has a readable .git/HEAD; it points to refs/heads/main, confirmed by .git/config. Other repos in /private/tmp lack HEAD files and cannot be assessed. Without knowing which specific repo the subject "Internal Repo" refers to, this is the only determinable value.
  N=8: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 

- intervention=target_field_anchor
  N=4: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=0
  note: 
  N=8: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=34
  note: target_anchor: default_branch => MISSING; status=missing
No source material provided across 8 compression passes. Subject is "Internal Repo" with seed tag 11. No claims about default_branch, ci_system, or deploy_region can be retained — nothing observed.

- intervention=tiny_fixed_scaffold
  N=4: compact=main; final=main; route=compact; raw=0; target_claim=1; note_tokens=12
  note: target_slot: default_branch => main
status_slot: clean
carry_slot: Buildkite CI deploys to us-central
  N=8: compact=ABSTAIN; final=main; route=utility_calibrated_recover; raw=1; target_claim=0; note_tokens=12
  note: target_slot: default_branch => MISSING
status_slot: missing
carry_slot: no repository data in source

