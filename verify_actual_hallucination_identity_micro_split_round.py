from __future__ import annotations

import json
from pathlib import Path

import run_actual_hallucination_robustness_round as robustness_base
import run_actual_summarizer_slice as actual_base


RESULTS_PATH = "outputs/actual_hallucination_identity_micro_split_results.json"
BASELINE_RESULTS_PATH = "outputs/actual_hallucination_surrogate_split_results.json"
VERIFY_PATH = "reviews/verification_round22.md"
OVERLAP_IDS = {"halu_01", "halu_02", "halu_03", "halu_04", "halu_05", "halu_08", "halu_12", "halu_14"}
RELATION_IDS = {"halu_01", "halu_12"}
LITERAL_IDS = {"halu_15", "halu_16", "halu_17", "halu_18"}


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
    item_id: str | None = None,
) -> list[dict]:
    return [
        record
        for record in records
        if record["intervention"] == intervention
        and record["architecture"] == architecture
        and record["n_passes"] == n_passes
        and (item_id is None or record["item_id"] == item_id)
        and (item_ids is None or record["item_id"] in item_ids)
    ]


def agg_accuracy(records: list[dict]) -> float:
    return actual_base.aggregate(records)["accuracy"]


def hallucination_metrics(records: list[dict]) -> dict[str, float]:
    return robustness_base.hallucination_metrics(records)


def clue_count(records: list[dict]) -> int:
    return sum(1 for record in records if record["tentative_target_claim"])


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    baseline = json.loads((base_dir / BASELINE_RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["n_values"]) * len(results["interventions"])
    actual_records = len(results["records"])
    slice_ids = set(results["slice_ids"])

    overlap_strong_new_n8 = select_records(
        results["records"], intervention="strong_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=OVERLAP_IDS
    )
    overlap_typed_summary_new_n8 = select_records(
        results["records"], intervention="typed_selective_anchor", architecture="summary_only", n_passes=8, item_ids=OVERLAP_IDS
    )
    overlap_typed_unified_new_n8 = select_records(
        results["records"], intervention="typed_selective_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=OVERLAP_IDS
    )
    overlap_typed_note_new_n8 = select_records(
        results["records"], intervention="typed_selective_anchor", architecture="scale_aware_note_aware", n_passes=8, item_ids=OVERLAP_IDS
    )
    overlap_identity_new_n8 = select_records(
        results["records"], intervention="identity_selective_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=OVERLAP_IDS
    )
    overlap_identity_note_new_n8 = select_records(
        results["records"], intervention="identity_selective_anchor", architecture="scale_aware_note_aware", n_passes=8, item_ids=OVERLAP_IDS
    )
    overlap_preference_new_n8 = select_records(
        results["records"], intervention="preference_selective_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=OVERLAP_IDS
    )

    baseline_strong_n8 = baseline["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["8"]
    baseline_typed_summary_n8 = baseline["aggregate"]["typed_selective_anchor"]["summary_only"]["8"]
    baseline_typed_unified_n8 = baseline["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_unified"]["8"]
    baseline_typed_note_n8 = baseline["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]
    baseline_identity_n8 = baseline["hallucination_metrics"]["identity_selective_anchor"]["scale_aware_unified"]["8"]
    baseline_identity_note_n8 = baseline["hallucination_metrics"]["identity_selective_anchor"]["scale_aware_note_aware"]["8"]
    baseline_preference_n8 = baseline["hallucination_metrics"]["preference_selective_anchor"]["scale_aware_unified"]["8"]

    relation_unified_n8 = select_records(
        results["records"], intervention="relation_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=RELATION_IDS
    )
    literal_on_relation_unified_n8 = select_records(
        results["records"], intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=RELATION_IDS
    )
    literal_unified_n8 = select_records(
        results["records"], intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=LITERAL_IDS
    )
    relation_on_literal_unified_n8 = select_records(
        results["records"], intervention="relation_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_ids=LITERAL_IDS
    )
    relation_note_n8 = select_records(
        results["records"], intervention="relation_identity_anchor", architecture="scale_aware_note_aware", n_passes=8
    )
    relation_unified_all_n8 = select_records(
        results["records"], intervention="relation_identity_anchor", architecture="scale_aware_unified", n_passes=8
    )
    literal_note_n8 = select_records(
        results["records"], intervention="literal_identity_anchor", architecture="scale_aware_note_aware", n_passes=8
    )
    literal_unified_all_n8 = select_records(
        results["records"], intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8
    )
    halu05_relation_unified_n8 = select_records(
        results["records"], intervention="relation_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_id="halu_05"
    )
    halu05_relation_note_n8 = select_records(
        results["records"], intervention="relation_identity_anchor", architecture="scale_aware_note_aware", n_passes=8, item_id="halu_05"
    )
    halu05_literal_unified_n8 = select_records(
        results["records"], intervention="literal_identity_anchor", architecture="scale_aware_unified", n_passes=8, item_id="halu_05"
    )
    halu05_literal_note_n8 = select_records(
        results["records"], intervention="literal_identity_anchor", architecture="scale_aware_note_aware", n_passes=8, item_id="halu_05"
    )

    lines = [
        "# Verification Round 22",
        "",
        "这个文件是对 actual hallucination identity-micro-split round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Expanded slice includes the four new literal identity/code items",
            LITERAL_IDS.issubset(slice_ids),
            f"expected new ids `{sorted(LITERAL_IDS)}`, observed slice ids include `{sorted(slice_ids & LITERAL_IDS)}`.",
        ),
        check(
            "Old-slice strong-anchor overlap remains consistent with the previous surrogate-split round at N=8",
            hallucination_metrics(overlap_strong_new_n8)["tentative_target_claim_rate"] == baseline_strong_n8["tentative_target_claim_rate"],
            f"previous/current overlap strong unified N=8 tentative_target_claim = `{baseline_strong_n8['tentative_target_claim_rate']:.3f}`/`{hallucination_metrics(overlap_strong_new_n8)['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Old-slice typed overlap remains consistent with the previous surrogate-split round at N=8",
            agg_accuracy(overlap_typed_summary_new_n8) == baseline_typed_summary_n8["accuracy"]
            and hallucination_metrics(overlap_typed_unified_new_n8)["false_present_rate"] == baseline_typed_unified_n8["false_present_rate"]
            and hallucination_metrics(overlap_typed_note_new_n8)["false_present_rate"] == baseline_typed_note_n8["false_present_rate"],
            f"previous/current overlap typed summary_only N=8 accuracy = `{baseline_typed_summary_n8['accuracy']:.3f}`/`{agg_accuracy(overlap_typed_summary_new_n8):.3f}`, unified false_present = `{baseline_typed_unified_n8['false_present_rate']:.3f}`/`{hallucination_metrics(overlap_typed_unified_new_n8)['false_present_rate']:.3f}`, note-aware false_present = `{baseline_typed_note_n8['false_present_rate']:.3f}`/`{hallucination_metrics(overlap_typed_note_new_n8)['false_present_rate']:.3f}`.",
        ),
        check(
            "Old-slice identity/preference overlap remains consistent with the previous surrogate-split round at N=8",
            hallucination_metrics(overlap_identity_new_n8)["false_present_rate"] == baseline_identity_n8["false_present_rate"]
            and hallucination_metrics(overlap_identity_note_new_n8)["false_present_rate"] == baseline_identity_note_n8["false_present_rate"]
            and hallucination_metrics(overlap_preference_new_n8)["false_present_rate"] == baseline_preference_n8["false_present_rate"],
            f"previous/current overlap identity unified false_present = `{baseline_identity_n8['false_present_rate']:.3f}`/`{hallucination_metrics(overlap_identity_new_n8)['false_present_rate']:.3f}`, identity note-aware = `{baseline_identity_note_n8['false_present_rate']:.3f}`/`{hallucination_metrics(overlap_identity_note_new_n8)['false_present_rate']:.3f}`, preference unified = `{baseline_preference_n8['false_present_rate']:.3f}`/`{hallucination_metrics(overlap_preference_new_n8)['false_present_rate']:.3f}`.",
        ),
        check(
            "Relation branch keeps more high-N clue survival than the literal branch on relation-style items",
            clue_count(relation_unified_n8) > clue_count(literal_on_relation_unified_n8),
            f"relation/literal clue counts on `{sorted(RELATION_IDS)}` at N=8 = `{clue_count(relation_unified_n8)}`/`{clue_count(literal_on_relation_unified_n8)}`.",
        ),
        check(
            "Literal branch keeps more high-N clue survival than the relation branch on literal-overlap items",
            clue_count(literal_unified_n8) > clue_count(relation_on_literal_unified_n8),
            f"literal/relation clue counts on `{sorted(LITERAL_IDS)}` at N=8 = `{clue_count(literal_unified_n8)}`/`{clue_count(relation_on_literal_unified_n8)}`.",
        ),
        check(
            "Relation and literal note-aware branches do not increase false-present at high N",
            hallucination_metrics(relation_note_n8)["false_present_rate"] <= hallucination_metrics(relation_unified_all_n8)["false_present_rate"]
            and hallucination_metrics(literal_note_n8)["false_present_rate"] <= hallucination_metrics(literal_unified_all_n8)["false_present_rate"],
            f"relation unified/note-aware false_present at N=8 = `{hallucination_metrics(relation_unified_all_n8)['false_present_rate']:.3f}`/`{hallucination_metrics(relation_note_n8)['false_present_rate']:.3f}`, literal unified/note-aware = `{hallucination_metrics(literal_unified_all_n8)['false_present_rate']:.3f}`/`{hallucination_metrics(literal_note_n8)['false_present_rate']:.3f}`.",
        ),
        check(
            "Both identity micro-split branches keep the halu_05 high-N fix in cleanup architectures",
            all(record["answer"] == "ABSTAIN" for record in halu05_relation_unified_n8)
            and all(record["answer"] == "ABSTAIN" for record in halu05_relation_note_n8)
            and all(record["answer"] == "ABSTAIN" for record in halu05_literal_unified_n8)
            and all(record["answer"] == "ABSTAIN" for record in halu05_literal_note_n8),
            f"relation unified/note-aware halu_05 answers = {[record['answer'] for record in halu05_relation_unified_n8]}/{[record['answer'] for record in halu05_relation_note_n8]}; literal unified/note-aware = {[record['answer'] for record in halu05_literal_unified_n8]}/{[record['answer'] for record in halu05_literal_note_n8]}.",
        ),
        check(
            "Relation and literal note-aware branches keep zero residual contamination at N=8",
            results["aggregate"]["relation_identity_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["literal_identity_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"relation/literal note-aware residual at N=8 = `{results['aggregate']['relation_identity_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`/`{results['aggregate']['literal_identity_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 expanded slice 没有破坏旧 frontier，而且新的 literal name/code-overlap item 的确把 identity branch 再拆开了一层：relation-style 和 literal-style clue 至少在高-N persistence 上已经可被分开观察。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
