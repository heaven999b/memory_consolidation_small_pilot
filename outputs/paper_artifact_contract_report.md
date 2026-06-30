# Paper Artifact Contract Report

这份工件检查 primary model-backed panel 是否已经具备 reviewer 需要的 item-level artifact contract，而不只是最终汇总表。

| Panel | Records | Pass Trace Coverage | Provenance Coverage | Quarantine Coverage | Stage Attribution Coverage |
|---|---:|---:|---:|---:|---:|
| actual_summarizer_slice | 128 | 1.000 | 1.000 | 0.141 | 1.000 |
| actual_recall_expansion | 288 | 1.000 | 1.000 | 0.139 | 1.000 |
| actual_hallucination_stress | 192 | 1.000 | 1.000 | 0.083 | 1.000 |
| actual_carry_forward | 96 | 1.000 | 1.000 | 0.219 | 1.000 |

## Readout

- `pass_trace_coverage` checks whether we kept per-pass compact memory history rather than only the final note.
- `provenance_link_coverage` checks whether each record exposes at least one raw-span linkage in final retained memory, pass-level claim lineage, note lineage, or an explicit raw-context witness when the model collapsed to empty output.
- `quarantine_signal_coverage` checks whether cleanup architectures expose explicit claim filtering or quarantine decisions.
- `stage_attribution_coverage` checks whether every record can be routed to a first failing stage instead of only a final correctness flag.
