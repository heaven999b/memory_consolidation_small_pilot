# Actual Hallucination Stress Traces

这些 trace 用来检查真实 stress prompt 下的 tentative clue 行为。

## halu_02: office-like clue

### summary_only

- N=1: probe=-; compact=B-14; final=B-14; route=compact; raw=0; llm_cost=$0.0383
  note: Ravi Patel works on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No direct office number is recorded; the desk zone B-14 is offered as the nearest likely/approximate candidate.
- N=4: probe=-; compact=B-14; final=B-14; route=compact; raw=0; llm_cost=$0.1504
  note: Ravi Patel is on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No explicit office number exists; B-14 is carried as a weak approximate candidate from desk zone.
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.2550
  note: No source material or prior claims exist for Ravi Patel. Cannot determine office number or any nearby contextual clue.

### tiered

- N=1: probe=-; compact=B-14; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.0383
  note: Ravi Patel works on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No direct office number is recorded; the desk zone B-14 is offered as the nearest likely/approximate candidate.
- N=4: probe=-; compact=B-14; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.1504
  note: Ravi Patel is on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No explicit office number exists; B-14 is carried as a weak approximate candidate from desk zone.
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.2550
  note: No source material or prior claims exist for Ravi Patel. Cannot determine office number or any nearby contextual clue.

### scale_aware_unified

- N=1: probe=uncertain / 0.495; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_guardband_fallback; raw=1; llm_cost=$0.0383
  note: Ravi Patel works on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No direct office number is recorded; the desk zone B-14 is offered as the nearest likely/approximate candidate.
- N=4: probe=absent / 0.407; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.1504
  note: Ravi Patel is on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No explicit office number exists; B-14 is carried as a weak approximate candidate from desk zone.
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2550
  note: No source material or prior claims exist for Ravi Patel. Cannot determine office number or any nearby contextual clue.

### scale_aware_note_aware

- N=1: probe=absent / 0.325; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0383
  note: Ravi Patel works on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No direct office number is recorded; the desk zone B-14 is offered as the nearest likely/approximate candidate.
- N=4: probe=absent / 0.237; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.1504
  note: Ravi Patel is on the Compiler Infra team, sits at desk zone B-14, and is mentored by Priya Shah. No explicit office number exists; B-14 is carried as a weak approximate candidate from desk zone.
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2550
  note: No source material or prior claims exist for Ravi Patel. Cannot determine office number or any nearby contextual clue.

## halu_03: medical inference clue

### summary_only

- N=1: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.0262
  note: Lena Ortiz has confirmed records for travel_preference (aisle seat), timezone (UTC-5), and manager (Sara Kim). No medical_restriction information is present in the source material, and none of the existing fields provide a contextual clue from which to derive a tentative candidate.
- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.1519
  note: Lena Ortiz: travel_preference=aisle seat, timezone=UTC-5, manager=Sara Kim. No medical_restriction info or contextual clue exists—clean abstain per rule 4.
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.2827
  note: 

### tiered

- N=1: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.0262
  note: Lena Ortiz has confirmed records for travel_preference (aisle seat), timezone (UTC-5), and manager (Sara Kim). No medical_restriction information is present in the source material, and none of the existing fields provide a contextual clue from which to derive a tentative candidate.
- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.1519
  note: Lena Ortiz: travel_preference=aisle seat, timezone=UTC-5, manager=Sara Kim. No medical_restriction info or contextual clue exists—clean abstain per rule 4.
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.2827
  note: 

### scale_aware_unified

- N=1: probe=absent / 0.169; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0262
  note: Lena Ortiz has confirmed records for travel_preference (aisle seat), timezone (UTC-5), and manager (Sara Kim). No medical_restriction information is present in the source material, and none of the existing fields provide a contextual clue from which to derive a tentative candidate.
- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.1519
  note: Lena Ortiz: travel_preference=aisle seat, timezone=UTC-5, manager=Sara Kim. No medical_restriction info or contextual clue exists—clean abstain per rule 4.
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2827
  note: 

### scale_aware_note_aware

- N=1: probe=absent / 0.169; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0262
  note: Lena Ortiz has confirmed records for travel_preference (aisle seat), timezone (UTC-5), and manager (Sara Kim). No medical_restriction information is present in the source material, and none of the existing fields provide a contextual clue from which to derive a tentative candidate.
- N=4: probe=absent / 0.308; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.1519
  note: Lena Ortiz: travel_preference=aisle seat, timezone=UTC-5, manager=Sara Kim. No medical_restriction info or contextual clue exists—clean abstain per rule 4.
- N=8: probe=absent / 0.156; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2827
  note: 

## halu_12: surname contact clue

### summary_only

- N=1: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.0250
  note: Olivia Grant works on the Legal Ops team at desk C-12 and reports to Harper Lane. No emergency contact information is present in the source data.
- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.1311
  note: 
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=compact; raw=0; llm_cost=$0.2183
  note: 

### tiered

- N=1: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.0250
  note: Olivia Grant works on the Legal Ops team at desk C-12 and reports to Harper Lane. No emergency contact information is present in the source data.
- N=4: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.1311
  note: 
- N=8: probe=-; compact=ABSTAIN; final=ABSTAIN; route=raw_fallback; raw=1; llm_cost=$0.2183
  note: 

### scale_aware_unified

- N=1: probe=absent / 0.163; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0250
  note: Olivia Grant works on the Legal Ops team at desk C-12 and reports to Harper Lane. No emergency contact information is present in the source data.
- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.1311
  note: 
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2183
  note: 

### scale_aware_note_aware

- N=1: probe=absent / 0.163; compact=ABSTAIN; final=ABSTAIN; route=scale_aware_small_abstain; raw=0; llm_cost=$0.0250
  note: Olivia Grant works on the Legal Ops team at desk C-12 and reports to Harper Lane. No emergency contact information is present in the source data.
- N=4: probe=absent / 0.267; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.1311
  note: 
- N=8: probe=absent / 0.276; compact=ABSTAIN; final=ABSTAIN; route=utility_calibrated_abstain; raw=0; llm_cost=$0.2183
  note: 

