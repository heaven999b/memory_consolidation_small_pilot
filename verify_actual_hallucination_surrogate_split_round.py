from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_surrogate_split_results.json"
BASELINE_RESULTS_PATH = "outputs/actual_hallucination_typed_selective_results.json"
VERIFY_PATH = "reviews/verification_round21.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def select_records(
    records: list[dict],
    *,
    intervention: str,
    architecture: str,
    n_passes: int,
    item_id: str | None = None,
) -> list[dict]:
    return [
        record
        for record in records
        if record["intervention"] == intervention
        and record["architecture"] == architecture
        and record["n_passes"] == n_passes
        and (item_id is None or record["item_id"] == item_id)
    ]


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    baseline = json.loads((base_dir / BASELINE_RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["n_values"]) * len(results["interventions"])
    actual_records = len(results["records"])

    baseline_strong_n4 = baseline["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["4"]
    baseline_strong_n8 = baseline["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["8"]
    baseline_typed_summary_n8 = baseline["aggregate"]["typed_selective_anchor"]["summary_only"]["8"]
    baseline_typed_unified_n8 = baseline["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_unified"]["8"]
    baseline_typed_note_n8 = baseline["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]

    strong_unified_n4 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["4"]
    strong_unified_n8 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["8"]
    typed_summary_n8 = results["aggregate"]["typed_selective_anchor"]["summary_only"]["8"]
    typed_unified_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_unified"]["8"]
    typed_note_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]
    identity_summary_n8 = results["aggregate"]["identity_selective_anchor"]["summary_only"]["8"]
    identity_unified_n4 = results["hallucination_metrics"]["identity_selective_anchor"]["scale_aware_unified"]["4"]
    identity_unified_n8 = results["hallucination_metrics"]["identity_selective_anchor"]["scale_aware_unified"]["8"]
    identity_note_n8 = results["hallucination_metrics"]["identity_selective_anchor"]["scale_aware_note_aware"]["8"]
    preference_summary_n8 = results["aggregate"]["preference_selective_anchor"]["summary_only"]["8"]
    preference_unified_n4 = results["hallucination_metrics"]["preference_selective_anchor"]["scale_aware_unified"]["4"]
    preference_unified_n8 = results["hallucination_metrics"]["preference_selective_anchor"]["scale_aware_unified"]["8"]
    preference_note_n8 = results["hallucination_metrics"]["preference_selective_anchor"]["scale_aware_note_aware"]["8"]
    soft_unified_n8 = results["hallucination_metrics"]["soft_anchor"]["scale_aware_unified"]["8"]

    halu05_identity_unified_n8 = select_records(
        results["records"], intervention="identity_selective_anchor", architecture="scale_aware_unified", n_passes=8, item_id="halu_05"
    )
    halu05_identity_note_n8 = select_records(
        results["records"], intervention="identity_selective_anchor", architecture="scale_aware_note_aware", n_passes=8, item_id="halu_05"
    )
    halu05_preference_unified_n8 = select_records(
        results["records"], intervention="preference_selective_anchor", architecture="scale_aware_unified", n_passes=8, item_id="halu_05"
    )
    halu05_preference_note_n8 = select_records(
        results["records"], intervention="preference_selective_anchor", architecture="scale_aware_note_aware", n_passes=8, item_id="halu_05"
    )

    lines = [
        "# Verification Round 21",
        "",
        "这个文件是对 actual hallucination surrogate-split round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Strong-anchor branch is consistent with the previous typed-selective round at N=4",
            strong_unified_n4["tentative_target_claim_rate"] == baseline_strong_n4["tentative_target_claim_rate"],
            f"previous/current strong unified N=4 tentative_target_claim = `{baseline_strong_n4['tentative_target_claim_rate']:.3f}`/`{strong_unified_n4['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Strong-anchor branch is consistent with the previous typed-selective round at N=8",
            strong_unified_n8["tentative_target_claim_rate"] == baseline_strong_n8["tentative_target_claim_rate"],
            f"previous/current strong unified N=8 tentative_target_claim = `{baseline_strong_n8['tentative_target_claim_rate']:.3f}`/`{strong_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Typed-selective baseline remains consistent with the previous typed round at N=8",
            typed_summary_n8["accuracy"] == baseline_typed_summary_n8["accuracy"]
            and typed_unified_n8["false_present_rate"] == baseline_typed_unified_n8["false_present_rate"]
            and typed_note_n8["false_present_rate"] == baseline_typed_note_n8["false_present_rate"],
            f"previous/current typed summary_only N=8 accuracy = `{baseline_typed_summary_n8['accuracy']:.3f}`/`{typed_summary_n8['accuracy']:.3f}`, unified false_present = `{baseline_typed_unified_n8['false_present_rate']:.3f}`/`{typed_unified_n8['false_present_rate']:.3f}`, note-aware false_present = `{baseline_typed_note_n8['false_present_rate']:.3f}`/`{typed_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Identity split keeps more high-N clue survival than the preference split",
            identity_unified_n8["tentative_target_claim_rate"] > preference_unified_n8["tentative_target_claim_rate"],
            f"identity/preference unified tentative_target_claim at N=8 = `{identity_unified_n8['tentative_target_claim_rate']:.3f}`/`{preference_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Identity split keeps more high-N clue survival than soft anchor",
            identity_unified_n8["tentative_target_claim_rate"] > soft_unified_n8["tentative_target_claim_rate"],
            f"identity/soft unified tentative_target_claim at N=8 = `{identity_unified_n8['tentative_target_claim_rate']:.3f}`/`{soft_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Identity split still leaves detector work at high N",
            identity_unified_n8["false_present_rate"] > 0.0,
            f"identity unified false_present at N=8 = `{identity_unified_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Identity note-aware reduces false-present relative to identity unified at high N",
            identity_note_n8["false_present_rate"] < identity_unified_n8["false_present_rate"],
            f"identity unified/note-aware false_present at N=8 = `{identity_unified_n8['false_present_rate']:.3f}`/`{identity_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Preference split removes high-N detector work",
            preference_unified_n8["false_present_rate"] == 0.0 and preference_note_n8["false_present_rate"] == 0.0,
            f"preference unified/note-aware false_present at N=8 = `{preference_unified_n8['false_present_rate']:.3f}`/`{preference_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Preference split buys more high-N summary-only realism than the identity split",
            preference_summary_n8["accuracy"] > identity_summary_n8["accuracy"],
            f"identity/preference summary_only N=8 accuracy = `{identity_summary_n8['accuracy']:.3f}`/`{preference_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "Both split variants keep the halu_05 high-N fix in cleanup architectures",
            all(record["answer"] == "ABSTAIN" for record in halu05_identity_unified_n8)
            and all(record["answer"] == "ABSTAIN" for record in halu05_identity_note_n8)
            and all(record["answer"] == "ABSTAIN" for record in halu05_preference_unified_n8)
            and all(record["answer"] == "ABSTAIN" for record in halu05_preference_note_n8),
            f"identity unified/note-aware halu_05 answers = {[record['answer'] for record in halu05_identity_unified_n8]}/{[record['answer'] for record in halu05_identity_note_n8]}; preference unified/note-aware = {[record['answer'] for record in halu05_preference_unified_n8]}/{[record['answer'] for record in halu05_preference_note_n8]}.",
        ),
        check(
            "Identity and preference note-aware branches keep zero residual contamination at N=8",
            results["aggregate"]["identity_selective_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0
            and results["aggregate"]["preference_selective_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"identity/preference note-aware residual at N=8 = `{results['aggregate']['identity_selective_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`/`{results['aggregate']['preference_selective_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 21 已经把 typed midpoint 再往前拆开了一层：高-N detector signal 主要由 identity-like surrogate 支撑，而 preference-style surrogate 更像 realism-friendly 但 detector-light 的分支。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
