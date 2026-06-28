from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_persistence_results.json"
BASELINE_RESULTS_PATH = "outputs/actual_hallucination_stress_results.json"
VERIFY_PATH = "reviews/verification_round17.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    baseline = json.loads((base_dir / BASELINE_RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["n_values"])
    actual_records = len(results["records"])

    base_unified_n4 = baseline["hallucination_metrics"]["scale_aware_unified"]["4"]
    base_note_n4 = baseline["hallucination_metrics"]["scale_aware_note_aware"]["4"]
    new_unified_n4 = results["hallucination_metrics"]["scale_aware_unified"]["4"]
    new_note_n4 = results["hallucination_metrics"]["scale_aware_note_aware"]["4"]
    new_unified_n8 = results["hallucination_metrics"]["scale_aware_unified"]["8"]
    new_note_n8 = results["hallucination_metrics"]["scale_aware_note_aware"]["8"]
    new_note_row_n8 = results["aggregate"]["scale_aware_note_aware"]["8"]
    new_unified_row_n8 = results["aggregate"]["scale_aware_unified"]["8"]

    lines = [
        "# Verification Round 17",
        "",
        "这个文件是对 actual hallucination persistence round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Stronger contract increases unified N=4 tentative clue persistence versus the old stress baseline",
            new_unified_n4["tentative_guess_note_rate"] > base_unified_n4["tentative_guess_note_rate"],
            f"old/new unified N=4 tentative_guess_note = `{base_unified_n4['tentative_guess_note_rate']:.3f}`/`{new_unified_n4['tentative_guess_note_rate']:.3f}`.",
        ),
        check(
            "Note-aware detector lowers false-present at N=4 under the stronger contract",
            new_note_n4["false_present_rate"] < new_unified_n4["false_present_rate"],
            f"new unified/note-aware N=4 false_present = `{new_unified_n4['false_present_rate']:.3f}`/`{new_note_n4['false_present_rate']:.3f}`.",
        ),
        check(
            "Stronger contract keeps tentative clue alive into at least one high-N setting",
            new_unified_n4["tentative_target_claim_rate"] > 0.0 or new_unified_n8["tentative_target_claim_rate"] > 0.0,
            f"N=4/N=8 tentative_target_claim = `{new_unified_n4['tentative_target_claim_rate']:.3f}`/`{new_unified_n8['tentative_target_claim_rate']:.3f}`.",
        ),
        check(
            "Note-aware detector keeps zero residual contamination at N=8",
            new_note_row_n8["residual_bad_memory_rate"] == 0.0,
            f"`scale_aware_note_aware` residual = `{new_note_row_n8['residual_bad_memory_rate']:.3f}`.",
        ),
        check(
            "Note-aware detector does not underperform unified on accuracy at N=8",
            new_note_row_n8["accuracy"] >= new_unified_row_n8["accuracy"],
            f"new note-aware/unified N=8 accuracy = `{new_note_row_n8['accuracy']:.3f}`/`{new_unified_row_n8['accuracy']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 18 已经把 actual hallucination stress 从局部 N=1 detector transfer 推向了更持久的 contract-level clue persistence 检验。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
