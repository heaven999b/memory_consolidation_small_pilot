# V3 Hygiene Audit

| Check | Value |
|---|---|
| absolute path leak files | `4` |
| outputs file count | `8266` |
| outputs total bytes | `1026848976` |

## Absolute Path Leaks

| Path | Hits | Sample |
|---|---|---|
| outputs/v3_attack_suite_grounding_audit.json | `2` | "repo": "/Users/yihaiwen/Documents/New project/agentpoison_official", |
| outputs/v3_attack_suite_grounding_audit.md | `2` | - repo: `/Users/yihaiwen/Documents/New project/agentpoison_official` |
| feasibility_report.md | `1` | - agentpoison_repo: /Users/yihaiwen/Documents/New project/agentpoison_official |
| outputs/v3_feasibility_gate.json | `1` | "agentpoison_repo: /Users/yihaiwen/Documents/New project/agentpoison_official" |

## Recommendations

- Strip `/Users/` absolute paths from submission-facing docs and HTML before any external release.
- Treat the current outputs tree as an internal working surface until a double-blind cleanup pass is complete.
- Prefer the new V3 reports and snapshots over older legacy packet artifacts when preparing paper-facing materials.
