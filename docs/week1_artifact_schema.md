# Week 1 Artifact Schema

This file freezes the Week 1 artifact contract for the TierMem common memory API.

The contract is intentionally small:

- one tiny synthetic dataset
- three pinned architectures: `raw_only`, `summary_only`, `summary_plus_raw`
- one run root per architecture and consolidation depth

## Run Root

Each Week 1 sanity run writes to:

```text
outputs/week1_sanity/
  <run_id>/
    summary.json
    errors.jsonl                  # optional
    sessions/
      <session_id>_write.jsonl
      <session_id>_qa.jsonl
```

The micro runner also writes a report layer:

```text
outputs/week1_sanity/
  micro_reports/
    <run_id>.json
    <run_id>.md
  week1_sanity_matrix.json
  week1_sanity_matrix.md
```

Machine-readable schemas live under:

- [memory_write_record.schema.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/configs/schemas/week1/memory_write_record.schema.json:1)
- [qa_record.schema.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/configs/schemas/week1/qa_record.schema.json:1)
- [summary.schema.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/configs/schemas/week1/summary.schema.json:1)

## Pinned Week 1 Architectures

| Architecture | Engine route | Page write mode | Meaning |
| --- | --- | --- | --- |
| `raw_only` | `research_only` | `raw` | Answer from raw evidence only. |
| `summary_only` | `summary_only` | `infer` | Answer from compact memories only. |
| `summary_plus_raw` | `auto` | `infer` | TierMem-style summary-first with bounded raw escalation. |

These presets are defined in [week1_surface.py](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/week1_surface.py:1) and pinned in:

- [raw_only.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/week1/raw_only.json:1)
- [summary_only.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/week1/summary_only.json:1)
- [summary_plus_raw.json](/Users/yihaiwen/Documents/New project/memory_consolidation_small_pilot/configs/week1/summary_plus_raw.json:1)

## `memory_write` Record

Source of truth: [logging_utils.py](/Users/yihaiwen/Documents/New project/tiermem_upstream/core/runner/logging_utils.py:12)

Required top-level fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `run_id` | string | Unique run label. |
| `benchmark` | string | `tiny_synth` for Week 1 sanity. |
| `system` | string | Memory system name. |
| `model` | string | Reader / writer model name. |
| `phase` | string | Always `memory_write`. |
| `session_id` | string | Session identifier. |
| `turn_id` | integer | Turn index inside the selected write stream. |
| `raw_input_text` | string | Text that was written into memory. |
| `timestamp` | string | UTC timestamp. |
| `cost_metrics` | object | Latency / token / API-call counters returned by `observe()`. |
| `storage_stats` | object | Memory-layer stats such as page id, stage, and counts. |

## `qa` Record

Source of truth: [logging_utils.py](/Users/yihaiwen/Documents/New project/tiermem_upstream/core/runner/logging_utils.py:67)

Required top-level fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `run_id` | string | Unique run label. |
| `benchmark` | string | `tiny_synth` for Week 1 sanity. |
| `system` | string | Memory system name. |
| `model` | string | Reader / writer model name. |
| `phase` | string | Always `qa`. |
| `session_id` | string | Session identifier. |
| `query_id` | string | QA identifier. |
| `question` | string | User-facing evaluation question. |
| `ground_truth` | string or list | Gold answer. |
| `model_response` | string | Final answer returned by the system. |
| `score` | number | Inline task score written during QA. |
| `timestamp` | string | UTC timestamp. |
| `cost_metrics` | object | Online latency / token / API-call counters from `answer()`. |
| `mechanism_trace` | object | Retrieval route, used hits, research trace, and gate flags. |

## `summary.json`

Source of truth: [summary_phase.py](/Users/yihaiwen/Documents/New project/tiermem_upstream/core/runner/summary_phase.py:270)

Required top-level fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `run_id` | string | Unique run label. |
| `benchmark` | string | Benchmark family. |
| `system` | string | Memory system name. |
| `model` | string | Model name. |
| `config` | object | Pinned runtime config, including `architecture`, engine route, page write mode, and `consolidation_passes`. |
| `metrics` | object | Aggregate task metrics. |
| `eval_report` | object or null | Benchmark-specific evaluation report. |
| `cost_summary` | object | Write / QA / overall cost roll-up. |
| `num_sessions` | integer | Number of sessions processed. |
| `num_write_logs` | integer | Number of write records. |
| `num_qa_logs` | integer | Number of QA records. |
| `timestamp` | string | UTC timestamp. |

## Week 1 Completion Rule

Week 1 is considered implemented when all of the following exist:

1. The tiny synthetic loader and dataset can be discovered through the TierMem bridge.
2. `raw_only`, `summary_only`, and `summary_plus_raw` are pinned as explicit presets.
3. Each run emits `memory_write`, `qa`, and `summary.json` artifacts under the schema above.
4. The sanity runner can execute either `pre_api_smoke` or a live micro run for the three presets.
