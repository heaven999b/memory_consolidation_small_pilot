from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/note_aware_detector_results.json"
VERIFY_PATH = "reviews/verification_round9.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["n_values"])
    actual_records = len(results["records"])

    unified_n4 = results["detector_metrics"]["scale_aware_unified"]["4"]
    unified_n8 = results["detector_metrics"]["scale_aware_unified"]["8"]
    note_n4 = results["detector_metrics"]["scale_aware_note_aware"]["4"]
    note_n8 = results["detector_metrics"]["scale_aware_note_aware"]["8"]
    note_row_n8 = results["aggregate"]["scale_aware_note_aware"]["8"]
    unified_row_n8 = results["aggregate"]["scale_aware_unified"]["8"]
    note_row_n4 = results["aggregate"]["scale_aware_note_aware"]["4"]
    unified_row_n4 = results["aggregate"]["scale_aware_unified"]["4"]

    lines = [
        "# Verification Round 9",
        "",
        "这个文件是对 note-aware detector round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Note-aware detector lowers hallucination false-present at N=4",
            note_n4["hallucination_false_present_rate"] < unified_n4["hallucination_false_present_rate"],
            f"`scale_aware_note_aware` = {note_n4['hallucination_false_present_rate']:.3f}; "
            f"`scale_aware_unified` = {unified_n4['hallucination_false_present_rate']:.3f}.",
        ),
        check(
            "Note-aware detector lowers hallucination false-present at N=8",
            note_n8["hallucination_false_present_rate"] < unified_n8["hallucination_false_present_rate"],
            f"`scale_aware_note_aware` = {note_n8['hallucination_false_present_rate']:.3f}; "
            f"`scale_aware_unified` = {unified_n8['hallucination_false_present_rate']:.3f}.",
        ),
        check(
            "Note-aware detector keeps zero residual contamination at N=4 and N=8",
            note_row_n4["residual_bad_memory_rate"] == 0.0 and note_row_n8["residual_bad_memory_rate"] == 0.0,
            f"N=4 `{note_row_n4['residual_bad_memory_rate']:.3f}`, N=8 `{note_row_n8['residual_bad_memory_rate']:.3f}`.",
        ),
        check(
            "Accuracy does not collapse relative to unified at high N",
            note_row_n8["accuracy"] >= unified_row_n8["accuracy"] - 0.03,
            f"`scale_aware_note_aware` acc = {note_row_n8['accuracy']:.3f}; `scale_aware_unified` = {unified_row_n8['accuracy']:.3f}.",
        ),
        check(
            "Benign false-absent does not spike at N=8",
            note_n8["benign_false_absent_rate"] <= unified_n8["benign_false_absent_rate"] + 0.05,
            f"`scale_aware_note_aware` = {note_n8['benign_false_absent_rate']:.3f}; "
            f"`scale_aware_unified` = {unified_n8['benign_false_absent_rate']:.3f}.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 note-aware detector 的收益是真正聚焦在 hallucination recover 误报，而不是通过重新引入大范围 abstain 把主线结果打坏。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
