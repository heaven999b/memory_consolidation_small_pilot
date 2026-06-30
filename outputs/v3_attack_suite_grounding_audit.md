# V3 Attack Suite Grounding Audit

Local grounding audit for safety-side benchmark and attack-suite repositories.

## Status

- AgentPoison: `partial`
- MPBench: `missing`
- MemEvoBench: `partial`

## AgentPoison

- repo: `/Users/yihaiwen/Documents/New project/agentpoison_official`
- license: `MIT License`
- has_environment_yml: `True`
- has_trigger_optimization: `True`
- has_scripts_dir: `True`
- requires_external_dataset_download: `True`
- readme_mentions_openai_or_remote_models: `True`
- next_action: Create a minimal local artifact audit and generate one tiny trigger/query overlay.

## MPBench

- repo: `None`
- next_action: Search for the official runnable MPBench artifact.

## MemEvoBench

- repo: `/Users/yihaiwen/Documents/New project/memevobench_official`
- license: `None`
- has_readme: `True`
- has_evaluation_dir: `True`
- has_memorybench_dir: `True`
- mentions_workflow_json: `True`
- mentions_openai_key: `True`
- mentions_judge_key: `True`
- next_action: Inspect one QA-style command and one workflow-style command on a tiny local slice.

## Conclusion

AgentPoison and MemEvoBench are now locally grounded at the repository level, but neither attack-suite path is yet counted as executed evidence. MPBench remains unresolved.
