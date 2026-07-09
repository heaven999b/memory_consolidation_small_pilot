# Feasibility Report

Date: 2026-06-30

This is the Week-0 V3 feasibility gate. It records what is already locally grounded, what only partially runs, and what remains paper-only in the current workspace.

| Check | Status | Pass Condition | Current State |
|---|---|---|---|
| TierMem usable | `partial` | Clone TierMem and run one supported eval end-to-end with the real raw tier, provenance links, and router present in code. | TierMem is cloned locally and the dedicated .venv_tiermem_v2 runtime passes local import/data preflight for both LoCoMo and LongMemEval. The remaining blocker for a real tiny run is OPENAI_API_KEY. |
| HaluMem usable | `partial` | Load the official HaluMem data and run one official Medium eval end-to-end. | The mirrored HaluMem repo, eval helpers, and canonical HaluMem-Medium file are now present locally. The remaining blocker for a real end-to-end run is OPENAI_API_KEY. |
| AgentPoison usable | `partial` | Clone AgentPoison and generate at least one usable trigger/query poisoning overlay. | The official AgentPoison repo is now mirrored locally, but its trigger/query poisoning path has not yet been executed in this workspace. |
| MPBench / MemEvoBench availability | `partial` | Confirm whether MPBench and MemEvoBench release runnable code plus data, not only papers. | At least one MPBench/MemEvoBench-like repo now exists locally, but runnable artifact availability is still not fully verified. |
| Citation reality | `partial` | Every cited paper ID, repo URL, and benchmark artifact must resolve to a real accessible object before release. | TierMem, HaluMem, LongMemEval, and AgentPoison are grounded by local repos or mirrors, and MemEvoBench now also has a local repo mirror. MPBench is still unresolved as a runnable local artifact. |
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
- current state: The mirrored HaluMem repo, eval helpers, and canonical HaluMem-Medium file are now present locally. The remaining blocker for a real end-to-end run is OPENAI_API_KEY.
- evidence:
  - repo: benchmarks/halumem/official_repo
  - final_medium_present: True
  - bridge returncode=1
  - dataset_source: https://huggingface.co/datasets/IAAR-Shanghai/HaluMem
  - license_badge_in_readme: CC-BY-NC-ND-4.0
- blockers:
  - HaluMem bridge also needs OPENAI_API_KEY once the Medium file is present
- next action: Set OPENAI_API_KEY and rerun the HaluMem bridge sanity pass.

### AgentPoison usable

- status: `partial`
- pass condition: Clone AgentPoison and generate at least one usable trigger/query poisoning overlay.
- current state: The official AgentPoison repo is now mirrored locally, but its trigger/query poisoning path has not yet been executed in this workspace.
- evidence:
  - local_repo: ../agentpoison_official
  - license: MIT License
- blockers:
  - official repo is present, but local trigger generation and overlay validation are still pending
- next action: Run a minimal local AgentPoison artifact audit and generate one small trigger/query overlay.

### MPBench / MemEvoBench availability

- status: `partial`
- pass condition: Confirm whether MPBench and MemEvoBench release runnable code plus data, not only papers.
- current state: At least one MPBench/MemEvoBench-like repo now exists locally, but runnable artifact availability is still not fully verified.
- evidence:
  - mpbench_repo: not found
  - memevobench_repo: ../memevobench_official
  - memevobench_license: missing
- blockers:
  - local repo presence is no longer the blocker; runnable artifact verification is still pending
- next action: Inspect the local repo contents and confirm whether runnable benchmark data plus code are actually released.

### Citation reality

- status: `partial`
- pass condition: Every cited paper ID, repo URL, and benchmark artifact must resolve to a real accessible object before release.
- current state: TierMem, HaluMem, LongMemEval, and AgentPoison are grounded by local repos or mirrors, and MemEvoBench now also has a local repo mirror. MPBench is still unresolved as a runnable local artifact.
- evidence:
  - tiermem_repo: True
  - halumem_repo: True
  - longmemeval_repo: True
  - agentpoison_repo: /Users/yihaiwen/Documents/New project/agentpoison_official
- blockers:
  - MPBench runnable artifact is still unresolved locally
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

