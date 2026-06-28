from __future__ import annotations

import os

import run_actual_hallucination_identity_micro_split_round as base


PILOT_IDS = "halu_01,halu_12,halu_15,halu_16,halu_17,halu_18"
PILOT_SEEDS = "11"


def main() -> None:
    os.environ.setdefault("ACTUAL_HALLU_IDENTITY_MICRO_IDS", PILOT_IDS)
    os.environ.setdefault("ACTUAL_HALLU_IDENTITY_MICRO_SEEDS", PILOT_SEEDS)
    base.INTERVENTIONS = [
        "typed_selective_anchor",
        "identity_selective_anchor",
        "relation_identity_anchor",
        "literal_identity_anchor",
    ]
    base.JSON_PATH = "outputs/actual_hallucination_identity_focus_pilot_results.json"
    base.SUMMARY_PATH = "outputs/actual_hallucination_identity_focus_pilot_summary.md"
    base.TRACE_PATH = "outputs/actual_hallucination_identity_focus_pilot_traces.md"
    base.TRACE_IDS = {
        "halu_01": "mentor-to-manager surrogate",
        "halu_12": "manager-to-emergency-contact surrogate",
        "halu_15": "code-overlap badge clue",
        "halu_16": "code-overlap archive-pin clue",
        "halu_17": "name-overlap sponsor clue",
        "halu_18": "name-overlap approver clue",
    }
    base.main()


if __name__ == "__main__":
    main()
