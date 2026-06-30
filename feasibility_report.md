# Feasibility Report

Date: 2026-06-30

This is the Week-0 V3 feasibility gate. It records what is already locally grounded, what only partially runs, and what remains paper-only in the current workspace.

| Check | Status | Pass Condition | Current State |
|---|---|---|---|
| TierMem usable | `partial` | Clone TierMem and run one supported eval end-to-end with the real raw tier, provenance links, and router present in code. | TierMem is cloned locally and the dedicated .venv_tiermem_v2 runtime passes local import/data preflight for both LoCoMo and LongMemEval. The remaining blocker for a real tiny run is OPENAI_API_KEY. |
| HaluMem usable | `partial` | Load the official HaluMem data and run one official Medium eval end-to-end. | The mirrored HaluMem repo and eval helpers are present, and the official README points to the Hugging Face release. The remaining local gap is the missing HaluMem-Medium.jsonl file expected by both TierMem and the official eval scripts. |
| AgentPoison usable | `paper_only` | Clone AgentPoison and generate at least one usable trigger/query poisoning overlay. | No local AgentPoison repo was found in the workspace. |
| MPBench / MemEvoBench availability | `paper_only` | Confirm whether MPBench and MemEvoBench release runnable code plus data, not only papers. | Neither MPBench nor MemEvoBench local repos were found in the workspace, so they should still be treated as taxonomy references only. |
| Citation reality | `partial` | Every cited paper ID, repo URL, and benchmark artifact must resolve to a real accessible object before release. | TierMem, HaluMem, and LongMemEval are grounded by local repos or mirrors, but the more recent safety-side citations are still only plan references in this workspace. |
| License compatibility | `partial` | All reused repos must have a verified license compatible with the intended public release plan. | TierMem and LongMemEval expose local license files. HaluMem's mirrored root does not ship a standalone LICENSE file, but its README advertises CC-BY-NC-ND-4.0, so the remaining task is to verify and document that signal cleanly before release. |

## Details

### TierMem usable

- status: `partial`
- pass condition: Clone TierMem and run one supported eval end-to-end with the real raw tier, provenance links, and router present in code.
- current state: TierMem is cloned locally and the dedicated .venv_tiermem_v2 runtime passes local import/data preflight for both LoCoMo and LongMemEval. The remaining blocker for a real tiny run is OPENAI_API_KEY.
- evidence:
  - repo: ../tiermem_upstream
  - license: MIT License
  - locomo bridge returncode=1
  - longmemeval bridge returncode=1
  - locomo env_only_blocked=True
  - longmemeval env_only_blocked=True
  - locomo dataset_loader_preflight: OK (session_id=conv-26; keys=['meta', 'qa_pairs', 'session_chunks', 'session_id', 'turns'])
  - longmemeval dataset_loader_preflight: OK (session_id=e47becba; keys=['meta', 'qa_pairs', 'session_chunks', 'session_id', 'turns'])
- blockers:
  - LoCoMo tiny sanity run is blocked only by OPENAI_API_KEY
  - LongMemEval tiny sanity run is blocked only by OPENAI_API_KEY
- next action: Set OPENAI_API_KEY and run a tiny bridge sanity pass on LoCoMo, then LongMemEval.

### HaluMem usable

- status: `partial`
- pass condition: Load the official HaluMem data and run one official Medium eval end-to-end.
- current state: The mirrored HaluMem repo and eval helpers are present, and the official README points to the Hugging Face release. The remaining local gap is the missing HaluMem-Medium.jsonl file expected by both TierMem and the official eval scripts.
- evidence:
  - repo: benchmarks/halumem/official_repo
  - final_medium_present: False
  - bridge returncode=1
  - dataset_source: https://huggingface.co/datasets/IAAR-Shanghai/HaluMem
  - license_badge_in_readme: CC-BY-NC-ND-4.0
- blockers:
  - final HaluMem-Medium.jsonl is not mirrored locally; source is the official Hugging Face dataset
  - HaluMem bridge also needs OPENAI_API_KEY once the Medium file is present
- next action: Download HaluMem-Medium from the official Hugging Face dataset, place it under benchmarks/halumem/official_repo/data/, and rerun the bridge check with a real API key.

### AgentPoison usable

- status: `paper_only`
- pass condition: Clone AgentPoison and generate at least one usable trigger/query poisoning overlay.
- current state: No local AgentPoison repo was found in the workspace.
- evidence:
  - local_repo: not found
- blockers:
  - local AgentPoison artifacts are absent
- next action: Clone AgentPoison and confirm trigger generation before claiming the safety attack suite is executable.

### MPBench / MemEvoBench availability

- status: `paper_only`
- pass condition: Confirm whether MPBench and MemEvoBench release runnable code plus data, not only papers.
- current state: Neither MPBench nor MemEvoBench local repos were found in the workspace, so they should still be treated as taxonomy references only.
- evidence:
  - mpbench_repo: not found
  - memevobench_repo: not found
- blockers:
  - artifact availability is still unverified locally
- next action: Keep them out of promised experiments until real public artifacts are confirmed.

### Citation reality

- status: `partial`
- pass condition: Every cited paper ID, repo URL, and benchmark artifact must resolve to a real accessible object before release.
- current state: TierMem, HaluMem, and LongMemEval are grounded by local repos or mirrors, but the more recent safety-side citations are still only plan references in this workspace.
- evidence:
  - tiermem_repo: True
  - halumem_repo: True
  - longmemeval_repo: True
  - agentpoison_repo: not found
- blockers:
  - recent safety benchmark repos are not yet verified locally
  - HaluMem final dataset packaging remains incomplete locally
- next action: Do a fresh citation-and-license pass before any public release or paper submission.

### License compatibility

- status: `partial`
- pass condition: All reused repos must have a verified license compatible with the intended public release plan.
- current state: TierMem and LongMemEval expose local license files. HaluMem's mirrored root does not ship a standalone LICENSE file, but its README advertises CC-BY-NC-ND-4.0, so the remaining task is to verify and document that signal cleanly before release.
- evidence:
  - tiermem_license: MIT License
  - longmemeval_license: MIT License
  - halumem_license_present: False
  - halumem_license_badge: CC-BY-NC-ND-4.0
- blockers:
  - none recorded
- next action: Verify the exact licenses of all mirrored benchmark repos before packaging a public release.

