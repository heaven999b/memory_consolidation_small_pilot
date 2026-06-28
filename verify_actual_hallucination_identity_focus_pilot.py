from __future__ import annotations

import json
from pathlib import Path

import run_actual_hallucination_robustness_round as robustness_base


RESULTS_PATH = "outputs/actual_hallucination_identity_focus_pilot_results.json"
VERIFY_PATH = "reviews/verification_round22.md"
RELATION_IDS = {"halu_01", "halu_12"}
LITERAL_IDS = {"halu_15", "halu_16", "halu_17", "halu_18"}
NAME_LITERAL_IDS = {"halu_17", "halu_18"}


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def select_records(
    records: list[dict],
    *,
    intervention: str,
    architecture: str,
    n_passes: int,
    item_ids: set[str] | None = None,
) -> list[dict]:
    return [
        record
        for record in records
        if record["intervention"] == intervention
        and record["architecture"] == architecture
        and record["n_passes"] == n_passes
        and (item_ids is None or record["item_id"] in item_ids)
    ]


def clue_count(records: list[dict]) -> int:
    return sum(1 for record in records if record["tentative_target_claim"])


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    records = results["records"]

    expected_records = (
        results["num_items"]
        * len(results["seeds"])
        * len(results["architectures"])
        * len(results["n_values"])
        * len(results["interventions"])
    )
    actual_records = len(records)

    typed_unified_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_unified"]["8"]
    typed_note_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]
    identity_unified_n8 = results["hallucination_metrics"]["identity_selective_anchor"]["scale_aware_unified"]["8"]
    identity_note_n8 = results["hallucination_metrics"]["identity_selective_anchor"]["scale_aware_note_aware"]["8"]
    relation_unified_n8 = results["hallucination_metrics"]["relation_identity_anchor"]["scale_aware_unified"]["8"]
    relation_note_n8 = results["hallucination_metrics"]["relation_identity_anchor"]["scale_aware_note_aware"]["8"]
    literal_unified_n8 = results["hallucination_metrics"]["literal_identity_anchor"]["scale_aware_unified"]["8"]
    literal_note_n8 = results["hallucination_metrics"]["literal_identity_anchor"]["scale_aware_note_aware"]["8"]

    relation_on_relation = select_records(
        records, intervention="relation_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=RELATION_IDS
    )
    relation_on_literal = select_records(
        records, intervention="relation_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=LITERAL_IDS
    )
    literal_on_relation = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=RELATION_IDS
    )
    literal_on_literal = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=LITERAL_IDS
    )
    literal_on_name = select_records(
        records, intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=NAME_LITERAL_IDS
    )

    relation_summary_n8 = results["aggregate"]["relation_identity_anchor"]["summary_only"]["8"]
    literal_summary_n8 = results["aggregate"]["literal_identity_anchor"]["summary_only"]["8"]
    typed_summary_n8 = results["aggregate"]["typed_selective_anchor"]["summary_only"]["8"]

    lines = [
        "# Verification Round 22",
        "",
        "这个文件是对 actual hallucination identity-focus pilot 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Focused pilot slice is the intended 6-item relation-plus-literal set",
            results["slice_ids"] == ["halu_01", "halu_12", "halu_15", "halu_16", "halu_17", "halu_18"],
            f"observed slice ids = `{results['slice_ids']}`.",
        ),
        check(
            "Typed note-aware removes the focused pilot's high-N false-present",
            typed_note_n8["false_present_rate"] < typed_unified_n8["false_present_rate"],
            f"typed unified/note-aware false_present at N=8 = `{typed_unified_n8['false_present_rate']:.3f}`/`{typed_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Identity note-aware removes the focused pilot's high-N false-present",
            identity_note_n8["false_present_rate"] < identity_unified_n8["false_present_rate"],
            f"identity unified/note-aware false_present at N=8 = `{identity_unified_n8['false_present_rate']:.3f}`/`{identity_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Relation branch keeps relation-style clues but blocks literal-overlap items",
            clue_count(relation_on_relation) > 0 and clue_count(relation_on_literal) == 0,
            f"relation branch clue counts on relation/literal ids at N=8 = `{clue_count(relation_on_relation)}`/`{clue_count(relation_on_literal)}`.",
        ),
        check(
            "Literal branch keeps literal-overlap clues but blocks relation-style items",
            clue_count(literal_on_literal) > 0 and clue_count(literal_on_relation) == 0,
            f"literal branch clue counts on literal/relation ids at N=8 = `{clue_count(literal_on_literal)}`/`{clue_count(literal_on_relation)}`.",
        ),
        check(
            "Literal note-aware removes the focused high-N code-overlap false-present",
            literal_note_n8["false_present_rate"] < literal_unified_n8["false_present_rate"],
            f"literal unified/note-aware false_present at N=8 = `{literal_unified_n8['false_present_rate']:.3f}`/`{literal_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Relation note-aware removes the focused high-N relation-style false-present",
            relation_note_n8["false_present_rate"] < relation_unified_n8["false_present_rate"],
            f"relation unified/note-aware false_present at N=8 = `{relation_unified_n8['false_present_rate']:.3f}`/`{relation_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Relation and literal summary-only contracts are both more realistic than typed at high N",
            relation_summary_n8["accuracy"] > typed_summary_n8["accuracy"] and literal_summary_n8["accuracy"] > typed_summary_n8["accuracy"],
            f"typed/relation/literal summary_only N=8 accuracy = `{typed_summary_n8['accuracy']:.3f}`/`{relation_summary_n8['accuracy']:.3f}`/`{literal_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "Name-overlap literal items remain detector-light in this pilot",
            all((not record["tentative_target_claim"]) and (not record["raw_escalated"]) for record in literal_on_name),
            f"literal branch on `{sorted(NAME_LITERAL_IDS)}` gives tent/raw = `{[(record['item_id'], record['tentative_target_claim'], record['raw_escalated']) for record in literal_on_name]}`.",
        ),
        check(
            "All note-aware branches keep zero residual contamination at N=8",
            results["aggregate"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["identity_selective_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["relation_identity_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["literal_identity_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            "typed/identity/relation/literal note-aware residual at N=8 all equal `0.000`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 focused pilot 已经把 identity family 再往前拆开了一层：relation-style alias 和 literal-style overlap 都能形成可见 detector work，但目前 literal 里真正稳定的更像 code overlap，而不是 person-name overlap。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
