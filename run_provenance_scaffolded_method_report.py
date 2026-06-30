from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/provenance_scaffolded_method_report.json"
SUMMARY_PATH = "outputs/provenance_scaffolded_method_report.md"


def load_json(base_dir: Path, relative_path: str) -> dict[str, Any]:
    return json.loads((base_dir / relative_path).read_text(encoding="utf-8"))


def recall_row(payload: dict[str, Any], architecture: str, n_passes: int) -> dict[str, Any]:
    aggregate = payload["aggregate"][architecture][str(n_passes)]
    metrics = payload["recall_metrics"][architecture][str(n_passes)]
    return {
        "accuracy": aggregate["accuracy"],
        "propagation": aggregate["propagation_rate"],
        "raw_escalation": aggregate["raw_escalation_rate"],
        "history_loss": metrics["history_loss_rate"],
        "empty_note_then_abstain": metrics["empty_note_then_abstain_rate"],
    }


def stress_row(payload: dict[str, Any], architecture: str, n_passes: int) -> dict[str, Any]:
    aggregate = payload["aggregate"][architecture][str(n_passes)]
    metrics = payload["hallucination_metrics"][architecture][str(n_passes)]
    return {
        "accuracy": aggregate["accuracy"],
        "propagation": aggregate["propagation_rate"],
        "raw_escalation": aggregate["raw_escalation_rate"],
        "false_present": metrics["false_present_rate"],
        "direct_unsupported": metrics["direct_unsupported_answer_rate"],
    }


def intervention_row(
    payload: dict[str, Any],
    metric_block: str,
    architecture: str,
    intervention: str,
    n_passes: int,
) -> dict[str, Any]:
    aggregate = payload["aggregate"][architecture][intervention][str(n_passes)]
    metrics = payload[metric_block][architecture][intervention][str(n_passes)]
    row = {
        "accuracy": aggregate["accuracy"],
        "propagation": aggregate["propagation_rate"],
        "raw_escalation": aggregate["raw_escalation_rate"],
        "residual_bad_memory": aggregate["residual_bad_memory_rate"],
    }
    row.update(metrics)
    return row


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    recall = load_json(base_dir, "outputs/actual_recall_expansion_results.json")
    stress = load_json(base_dir, "outputs/actual_hallucination_stress_results.json")
    persistence = load_json(base_dir, "outputs/actual_note_persistence_results.json")
    refinement = load_json(base_dir, "outputs/actual_scaffold_refinement_results.json")
    hardening = load_json(base_dir, "outputs/actual_placeholder_hardening_results.json")
    carry = load_json(base_dir, "outputs/actual_carry_forward_results.json")

    method_spec = {
        "name": "Provenance-Scaffolded Unified",
        "short_name": "PSU",
        "routing_architecture": "scale_aware_note_aware",
        "compaction_contract": "tiny_carry_forward_scaffold",
        "component_lineage": [
            "baseline compact note contract",
            "tiny_fixed_scaffold",
            "tiny_refusal_scaffold",
            "tiny_placeholder_hardened_scaffold",
            "tiny_carry_forward_scaffold",
        ],
        "rules": [
            "Use a fixed query-slot scaffold so the target field survives repeated compression.",
            "Drop placeholder or unsupported query values unless they are explicitly marked tentative and low-confidence.",
            "Carry forward the last valid scaffold when a later pass collapses to empty or missing-only output.",
            "Use note-aware uncertainty gating so raw escalation depends on provenance, missingness markers, and target-noise signals rather than raw fallback alone.",
        ],
        "goal": "Reduce high-N benign history loss and unsafe scaffold collapse without giving back the hallucination-side false-present gains already achieved by the note-aware cleanup family.",
    }

    defense_axis_projection = [
        {
            "axis": "none",
            "repo_object": "summary_only",
            "role": "No raw-backed cleanup or provenance-aware recovery.",
            "evidence_source": "actual_recall_expansion N=8 / actual_hallucination_stress N=8",
        },
        {
            "axis": "classifier_only",
            "repo_object": "scale_aware_unified",
            "role": "Cleanup + retrieval classifier without note-aware uncertainty adjustment.",
            "evidence_source": "actual_recall_expansion N=8 / actual_hallucination_stress N=8",
        },
        {
            "axis": "uncertainty_aware",
            "repo_object": "scale_aware_note_aware",
            "role": "Classifier-only baseline plus note-aware probe correction.",
            "evidence_source": "actual_recall_expansion N=8 / actual_hallucination_stress N=8",
        },
        {
            "axis": "conservative_compaction",
            "repo_object": "tiny_fixed_scaffold + scale_aware_note_aware",
            "role": "Structured target-slot retention to reduce high-N evaporation before stronger provenance filtering.",
            "evidence_source": "actual_note_persistence_results N=8",
        },
        {
            "axis": "provenance_required",
            "repo_object": "tiny_placeholder_hardened_scaffold + scale_aware_note_aware",
            "role": "Explicit demotion of placeholder query values and stricter query-slot validity.",
            "evidence_source": "actual_placeholder_hardening_results N=8",
        },
        {
            "axis": "full_method",
            "repo_object": "tiny_carry_forward_scaffold + scale_aware_note_aware",
            "role": "The formal PSU method: scaffolded compaction, placeholder hardening, carry-forward, and note-aware uncertainty gating.",
            "evidence_source": "actual_carry_forward_results N=8",
        },
    ]

    recall_baseline_table = {
        architecture: recall_row(recall, architecture, 8)
        for architecture in ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware"]
    }
    stress_baseline_table = {
        architecture: stress_row(stress, architecture, 8)
        for architecture in ["summary_only", "tiered", "scale_aware_unified", "scale_aware_note_aware"]
    }
    intervention_chain = [
        {
            "step": "baseline",
            "description": "Natural compact note with no scaffold or carry-forward rule.",
            "source": "actual_note_persistence_results",
            "metrics": intervention_row(persistence, "persistence_metrics", "scale_aware_note_aware", "baseline", 8),
        },
        {
            "step": "tiny_fixed_scaffold",
            "description": "Structured target_slot/status_slot/carry_slot scaffold.",
            "source": "actual_note_persistence_results",
            "metrics": intervention_row(persistence, "persistence_metrics", "scale_aware_note_aware", "tiny_fixed_scaffold", 8),
        },
        {
            "step": "tiny_refusal_scaffold",
            "description": "Unsafe/policy semantics moved from raw action text into explicit refusal scaffold.",
            "source": "actual_scaffold_refinement_results",
            "metrics": intervention_row(refinement, "refinement_metrics", "scale_aware_note_aware", "tiny_refusal_scaffold", 8),
        },
        {
            "step": "tiny_placeholder_hardened_scaffold",
            "description": "Placeholder or missing-like query values are filtered instead of treated as valid target content.",
            "source": "actual_placeholder_hardening_results",
            "metrics": intervention_row(hardening, "hardening_metrics", "scale_aware_note_aware", "tiny_placeholder_hardened_scaffold", 8),
        },
        {
            "step": "tiny_carry_forward_scaffold",
            "description": "The final PSU compaction contract; preserves the last valid scaffold when later passes collapse.",
            "source": "actual_carry_forward_results",
            "metrics": intervention_row(carry, "carry_metrics", "scale_aware_note_aware", "tiny_carry_forward_scaffold", 8),
        },
    ]

    conclusions = [
        "The real blocker after the benchmark-native baseline is no longer unsupported-memory shielding alone; it is benign answerability evaporation under repeated compression.",
        "The scaffold lineage already identifies a coherent intervention family: fixed target slot, refusal-safe scaffold, placeholder hardening, then carry-forward.",
        "PSU should be treated as the paper-facing method name for that lineage rather than as another isolated round artifact.",
    ]

    payload = {
        "method_spec": method_spec,
        "defense_axis_projection": defense_axis_projection,
        "baseline_panels": {
            "recall_n8": recall_baseline_table,
            "hallucination_stress_n8": stress_baseline_table,
        },
        "intervention_chain": intervention_chain,
        "conclusions": conclusions,
    }

    lines = [
        "# Provenance-Scaffolded Unified",
        "",
        "这份工件把 repo 里已经分散存在的 scaffold / hardening / carry-forward / note-aware 结果正式收束成一个论文方法对象，而不是继续把它们当成离散 patch。",
        "",
        "## Method",
        "",
        f"- name: `{method_spec['name']}`",
        f"- short name: `{method_spec['short_name']}`",
        f"- routing architecture: `{method_spec['routing_architecture']}`",
        f"- compaction contract: `{method_spec['compaction_contract']}`",
        "",
        "### Core Rules",
        "",
    ]
    for rule in method_spec["rules"]:
        lines.append(f"- {rule}")

    lines.extend(
        [
            "",
            "## Defense Axis Projection",
            "",
            "| Axis | Concrete Repo Object | Role |",
            "|---|---|---|",
        ]
    )
    for row in defense_axis_projection:
        lines.append(f"| {row['axis']} | `{row['repo_object']}` | {row['role']} |")

    lines.extend(
        [
            "",
            "## Benchmark-Native Baseline Context",
            "",
            "### Actual Recall Expansion (N=8)",
            "",
            "| Method | accuracy | propagation | raw escalation | history loss | empty-note-then-abstain |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for architecture, row in recall_baseline_table.items():
        lines.append(
            f"| {architecture} | {row['accuracy']:.3f} | {row['propagation']:.3f} | {row['raw_escalation']:.3f} | "
            f"{row['history_loss']:.3f} | {row['empty_note_then_abstain']:.3f} |"
        )

    lines.extend(
        [
            "",
            "### Actual Hallucination Stress (N=8)",
            "",
            "| Method | accuracy | propagation | raw escalation | false_present | direct_unsupported |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for architecture, row in stress_baseline_table.items():
        lines.append(
            f"| {architecture} | {row['accuracy']:.3f} | {row['propagation']:.3f} | {row['raw_escalation']:.3f} | "
            f"{row['false_present']:.3f} | {row['direct_unsupported']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Intervention Chain",
            "",
            "| Step | Source | accuracy | history_loss | unsafe_error | placeholder_answer | carry_forward_record | target_claim_retained | raw escalation |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in intervention_chain:
        metrics = row["metrics"]
        lines.append(
            f"| {row['step']} | `{row['source']}` | {metrics.get('accuracy', 0.0):.3f} | "
            f"{metrics.get('history_loss_rate', 0.0):.3f} | "
            f"{metrics.get('unsafe_error_rate', 0.0):.3f} | "
            f"{metrics.get('placeholder_answer_rate', metrics.get('hallucination_placeholder_answer_rate', 0.0)):.3f} | "
            f"{metrics.get('carry_forward_record_rate', 0.0):.3f} | "
            f"{metrics.get('target_claim_retained_rate', 0.0):.3f} | "
            f"{metrics.get('raw_escalation', metrics.get('raw_escalation_rate', 0.0)):.3f} |"
        )
    lines.extend(
        [
            "",
            "## Why This Counts As A Method",
            "",
            "- The compaction contract is no longer an unnamed best-effort prompt tweak; it is the ordered scaffold lineage ending at `tiny_carry_forward_scaffold`.",
            "- The routing policy is no longer just \"use the unified family\"; it is the note-aware uncertainty gate already validated on the hallucination stress slice.",
            "- The full object therefore has both a compaction side and a routing side, which is exactly what a paper baseline needs for ablation and mechanism analysis.",
            "",
            "## Takeaways",
            "",
        ]
    )
    for conclusion in conclusions:
        lines.append(f"- {conclusion}")

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
