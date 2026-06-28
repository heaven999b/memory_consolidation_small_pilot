from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_intermediate_contract_results.json"
BASELINE_RESULTS_PATH = "outputs/actual_hallucination_robustness_results.json"
VERIFY_PATH = "reviews/verification_round19.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    baseline = json.loads((base_dir / BASELINE_RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["n_values"]) * len(results["interventions"])
    actual_records = len(results["records"])

    strong_summary_n4 = results["aggregate"]["strong_anchor"]["summary_only"]["4"]
    strong_summary_n8 = results["aggregate"]["strong_anchor"]["summary_only"]["8"]
    selective_summary_n4 = results["aggregate"]["selective_anchor"]["summary_only"]["4"]
    selective_summary_n8 = results["aggregate"]["selective_anchor"]["summary_only"]["8"]

    strong_unified_n4 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["4"]
    strong_unified_n8 = results["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["8"]
    selective_unified_n4 = results["hallucination_metrics"]["selective_anchor"]["scale_aware_unified"]["4"]
    selective_unified_n8 = results["hallucination_metrics"]["selective_anchor"]["scale_aware_unified"]["8"]
    soft_unified_n4 = results["hallucination_metrics"]["soft_anchor"]["scale_aware_unified"]["4"]
    soft_unified_n8 = results["hallucination_metrics"]["soft_anchor"]["scale_aware_unified"]["8"]
    selective_note_n4 = results["hallucination_metrics"]["selective_anchor"]["scale_aware_note_aware"]["4"]
    selective_note_n8 = results["hallucination_metrics"]["selective_anchor"]["scale_aware_note_aware"]["8"]

    baseline_strong_n4 = baseline["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["4"]
    baseline_strong_n8 = baseline["hallucination_metrics"]["strong_anchor"]["scale_aware_unified"]["8"]

    lines = [
        "# Verification Round 19",
        "",
        "这个文件是对 actual hallucination intermediate-contract round 的机械核对，不引入新的主张。",
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
            "Selective anchor improves summary-only realism over strong anchor at N=4 or N=8",
            selective_summary_n4["accuracy"] > strong_summary_n4["accuracy"] or selective_summary_n8["accuracy"] > strong_summary_n8["accuracy"],
            f"summary_only strong/selective accuracy at N=4 = `{strong_summary_n4['accuracy']:.3f}`/`{selective_summary_n4['accuracy']:.3f}`, at N=8 = `{strong_summary_n8['accuracy']:.3f}`/`{selective_summary_n8['accuracy']:.3f}`.",
        ),
        check(
            "Selective anchor keeps more clue survival than soft anchor at N=4 or N=8",
            selective_unified_n4["tentative_target_claim_rate"] > soft_unified_n4["tentative_target_claim_rate"] or selective_unified_n8["tentative_target_claim_rate"] > soft_unified_n8["tentative_target_claim_rate"],
            f"selective/soft unified tentative_target_claim at N=4 = `{selective_unified_n4['tentative_target_claim_rate']:.3f}`/`{soft_unified_n4['tentative_target_claim_rate']:.3f}`, at N=8 = `{selective_unified_n8['tentative_target_claim_rate']:.3f}`/`{soft_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Selective anchor remains weaker than strong anchor on clue survival",
            selective_unified_n4["tentative_target_claim_rate"] < strong_unified_n4["tentative_target_claim_rate"] or selective_unified_n8["tentative_target_claim_rate"] < strong_unified_n8["tentative_target_claim_rate"],
            f"strong/selective unified tentative_target_claim at N=4 = `{strong_unified_n4['tentative_target_claim_rate']:.3f}`/`{selective_unified_n4['tentative_target_claim_rate']:.3f}`, at N=8 = `{strong_unified_n8['tentative_target_claim_rate']:.3f}`/`{selective_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Selective anchor still leaves detector work at at least one high-N setting",
            selective_unified_n4["false_present_rate"] > 0.0 or selective_unified_n8["false_present_rate"] > 0.0,
            f"selective unified false_present at N=4/N=8 = `{selective_unified_n4['false_present_rate']:.3f}`/`{selective_unified_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Selective note-aware reduces false-present relative to selective unified at at least one high-N setting",
            selective_note_n4["false_present_rate"] < selective_unified_n4["false_present_rate"] or selective_note_n8["false_present_rate"] < selective_unified_n8["false_present_rate"],
            f"selective unified/note-aware false_present at N=4 = `{selective_unified_n4['false_present_rate']:.3f}`/`{selective_note_n4['false_present_rate']:.3f}`, at N=8 = `{selective_unified_n8['false_present_rate']:.3f}`/`{selective_note_n8['false_present_rate']:.3f}`.",
        ),
        check(
            "Selective note-aware keeps zero residual contamination at N=8",
            results["aggregate"]["selective_anchor"]["scale_aware_note_aware"]["8"]["residual_bad_memory_rate"] == 0.0,
            f"selective note-aware N=8 residual = `{results['aggregate']['selective_anchor']['scale_aware_note_aware']['8']['residual_bad_memory_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 19 已经把 realism frontier 往前推了一步：selective_anchor 不再像 strong_anchor 那样极端，但也没有像 soft_anchor 那样完全失去 clue survival。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
