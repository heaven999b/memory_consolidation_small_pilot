from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_typed_selective_results.json"
BASELINE_RESULTS_PATH = "outputs/actual_hallucination_intermediate_contract_results.json"
VERIFY_PATH = "reviews/verification_round20.md"


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
    baseline_selective_summary_n8 = baseline["aggregate"]["selective_anchor"]["summary_only"]["8"]
    baseline_selective_unified_n4 = baseline["hallucination_metrics"]["selective_anchor"]["scale_aware_unified"]["4"]
    baseline_selective_unified_n8 = baseline["hallucination_metrics"]["selective_anchor"]["scale_aware_unified"]["8"]
    baseline_selective_note_n8 = baseline["hallucination_metrics"]["selective_anchor"]["scale_aware_note_aware"]["8"]

    strong_summary_n4 = results["aggregate"]["strong_anchor"]["summary_only"]["4"]
    strong_summary_n8 = results["aggregate"]["strong_anchor"]["summary_only"]["8"]
    selective_summary_n8 = results["aggregate"]["selective_anchor"]["summary_only"]["8"]
    typed_summary_n4 = results["aggregate"]["typed_selective_anchor"]["summary_only"]["4"]
    typed_summary_n8 = results["aggregate"]["typed_selective_anchor"]["summary_only"]["8"]
    strong_unified_n4 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["4"]
    strong_unified_n8 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["8"]
    selective_unified_n4 = results["hallucination_metrics"]["selective_anchor"]["scale_aware_unified"]["4"]
    selective_unified_n8 = results["hallucination_metrics"]["selective_anchor"]["scale_aware_unified"]["8"]
    typed_unified_n4 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_unified"]["4"]
    typed_unified_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_unified"]["8"]
    soft_unified_n4 = results["hallucination_metrics"]["soft_anchor"]["scale_aware_unified"]["4"]
    soft_unified_n8 = results["hallucination_metrics"]["soft_anchor"]["scale_aware_unified"]["8"]
    typed_note_n4 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_note_aware"]["4"]
    typed_note_n8 = results["hallucination_metrics"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]

    halu05_typed_unified_n8 = select_records(
        results["records"], intervention="typed_selective_anchor", architecture="scale_aware_unified", n_passes=8, item_id="halu_05"
    )
    halu05_typed_note_n8 = select_records(
        results["records"], intervention="typed_selective_anchor", architecture="scale_aware_note_aware", n_passes=8, item_id="halu_05"
    )

    lines = [
        "# Verification Round 20",
        "",
        "这个文件是对 actual hallucination typed-selective round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Strong-anchor branch is consistent with the previous robustness round at N=4",
            strong_unified_n4["tentative_target_claim_rate"] == baseline_strong_n4["tentative_target_claim_rate"],
            f"previous/current strong unified N=4 tentative_target_claim = `{baseline_strong_n4['tentative_target_claim_rate']:.3f}`/`{strong_unified_n4['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Strong-anchor branch is consistent with the previous robustness round at N=8",
            strong_unified_n8["tentative_target_claim_rate"] == baseline_strong_n8["tentative_target_claim_rate"],
            f"previous/current strong unified N=8 tentative_target_claim = `{baseline_strong_n8['tentative_target_claim_rate']:.3f}`/`{strong_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Selective-anchor baseline remains consistent with the previous intermediate round at N=4",
            selective_unified_n4["false_present_rate"] == baseline_selective_unified_n4["false_present_rate"],
            f"previous/current selective unified N=4 false_present = `{baseline_selective_unified_n4['false_present_rate']:.3f}`/`{selective_unified_n4['false_present_rate']:.3f}`.",
        ),
        check(
            "Selective-anchor baseline remains consistent with the previous intermediate round at N=8",
            selective_unified_n8["false_present_rate"] == baseline_selective_unified_n8["false_present_rate"]
            and selective_summary_n8["accuracy"] == baseline_selective_summary_n8["accuracy"]
            and results["hallucination_metrics"]["selective_anchor"]["scale_aware_note_aware"]["8"]["false_present_rate"] == baseline_selective_note_n8["false_present_rate"],
            f"previous/current selective summary_only N=8 accuracy = `{baseline_selective_summary_n8['accuracy']:.3f}`/`{selective_summary_n8['accuracy']:.3f}`, unified false_present = `{baseline_selective_unified_n8['false_present_rate']:.3f}`/`{selective_unified_n8['false_present_rate']:.3f}`, note-aware false_present = `{baseline_selective_note_n8['false_present_rate']:.3f}`/`{results['hallucination_metrics']['selective_anchor']['scale_aware_note_aware']['8']['false_present_rate']:.3f}`.",
        ),
        check(
            "Typed selective improves high-N summary-only realism over the prior selective anchor",
            typed_summary_n8["accuracy"] > selective_summary_n8["accuracy"],
            f"selective/typed summary_only N=8 accuracy = `{selective_summary_n8['accuracy']:.3f}`/`{typed_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "Typed selective improves high-N cleanup accuracy over the prior selective anchor",
            results["aggregate"]["typed_selective_anchor"]["scale_aware_unified"]["8"]["accuracy"]
            > results["aggregate"]["selective_anchor"]["scale_aware_unified"]["8"]["accuracy"]
            and results["aggregate"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]["accuracy"]
            > results["aggregate"]["selective_anchor"]["scale_aware_note_aware"]["8"]["accuracy"],
            f"selective/typed unified N=8 accuracy = `{results['aggregate']['selective_anchor']['scale_aware_unified']['8']['accuracy']:.3f}`/`{results['aggregate']['typed_selective_anchor']['scale_aware_unified']['8']['accuracy']:.3f}`, note-aware = `{results['aggregate']['selective_anchor']['scale_aware_note_aware']['8']['accuracy']:.3f}`/`{results['aggregate']['typed_selective_anchor']['scale_aware_note_aware']['8']['accuracy']:.3f}`.",
        ),
        check(
            "Typed selective keeps more clue survival than soft anchor",
            typed_unified_n4["tentative_target_claim_rate"] > soft_unified_n4["tentative_target_claim_rate"]
            or typed_unified_n8["tentative_target_claim_rate"] > soft_unified_n8["tentative_target_claim_rate"],
            f"typed/soft unified tentative_target_claim at N=4 = `{typed_unified_n4['tentative_target_claim_rate']:.3f}`/`{soft_unified_n4['tentative_target_claim_rate']:.3f}`, at N=8 = `{typed_unified_n8['tentative_target_claim_rate']:.3f}`/`{soft_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Typed selective does not increase false-present relative to the prior selective anchor",
            typed_unified_n4["false_present_rate"] <= selective_unified_n4["false_present_rate"]
            and typed_unified_n8["false_present_rate"] <= selective_unified_n8["false_present_rate"],
            f"selective/typed unified false_present at N=4 = `{selective_unified_n4['false_present_rate']:.3f}`/`{typed_unified_n4['false_present_rate']:.3f}`, at N=8 = `{selective_unified_n8['false_present_rate']:.3f}`/`{typed_unified_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Typed note-aware reduces false-present relative to typed unified at at least one high-N setting",
            typed_note_n4["false_present_rate"] < typed_unified_n4["false_present_rate"]
            or typed_note_n8["false_present_rate"] < typed_unified_n8["false_present_rate"],
            f"typed unified/note-aware false_present at N=4 = `{typed_unified_n4['false_present_rate']:.3f}`/`{typed_note_n4['false_present_rate']:.3f}`, at N=8 = `{typed_unified_n8['false_present_rate']:.3f}`/`{typed_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Typed selective fixes the halu_05 high-N over-refusal in both cleanup architectures",
            all(record["answer"] == "ABSTAIN" for record in halu05_typed_unified_n8)
            and all(record["answer"] == "ABSTAIN" for record in halu05_typed_note_n8),
            f"typed halu_05 N=8 unified answers = {[record['answer'] for record in halu05_typed_unified_n8]}, note-aware answers = {[record['answer'] for record in halu05_typed_note_n8]}.",
        ),
        check(
            "Typed note-aware keeps zero residual contamination at N=8",
            results["aggregate"]["typed_selective_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"typed note-aware N=8 residual = `{results['aggregate']['typed_selective_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 20 不只是重复 selective baseline，而是把中间 contract 进一步 typed 化：保住部分 surrogate clue 的同时，修掉 policy-window 型高-N over-refusal。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
