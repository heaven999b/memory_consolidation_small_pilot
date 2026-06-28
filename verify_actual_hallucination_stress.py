from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_hallucination_stress_results.json"
VERIFY_PATH = "reviews/verification_round12.md"


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

    unified_n1 = results["hallucination_metrics"]["scale_aware_unified"]["1"]
    unified_n4 = results["hallucination_metrics"]["scale_aware_unified"]["4"]
    note_n1 = results["hallucination_metrics"]["scale_aware_note_aware"]["1"]
    note_n4 = results["hallucination_metrics"]["scale_aware_note_aware"]["4"]
    note_n8 = results["hallucination_metrics"]["scale_aware_note_aware"]["8"]
    summary_n1 = results["hallucination_metrics"]["summary_only"]["1"]
    note_row_n8 = results["aggregate"]["scale_aware_note_aware"]["8"]
    unified_row_n8 = results["aggregate"]["scale_aware_unified"]["8"]

    lines = [
        "# Verification Round 12",
        "",
        "这个文件是对 actual hallucination stress round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Stress slice triggers tentative hallucination behavior at N=1",
            summary_n1["tentative_guess_note_rate"] > 0.0,
            f"N=1 tentative_guess_note_rate = `{summary_n1['tentative_guess_note_rate']:.3f}`.",
        ),
        check(
            "Note-aware detector lowers false-present at N=1 under actual stress",
            note_n1["false_present_rate"] < unified_n1["false_present_rate"],
            f"`scale_aware_note_aware` = {note_n1['false_present_rate']:.3f}; `scale_aware_unified` = {unified_n1['false_present_rate']:.3f}.",
        ),
        check(
            "Tentative clue pressure does not persist to high N in the actual stress slice",
            note_n4["tentative_guess_note_rate"] == 0.0 and note_n8["tentative_guess_note_rate"] == 0.0,
            f"N=4/N=8 tentative_guess_note_rate = {note_n4['tentative_guess_note_rate']:.3f}/{note_n8['tentative_guess_note_rate']:.3f}.",
        ),
        check(
            "Note-aware detector keeps zero residual contamination at N=8",
            note_row_n8["residual_bad_memory_rate"] == 0.0,
            f"`scale_aware_note_aware` residual = {note_row_n8['residual_bad_memory_rate']:.3f}.",
        ),
        check(
            "Note-aware detector does not underperform unified on accuracy at N=8",
            note_row_n8["accuracy"] >= unified_row_n8["accuracy"],
            f"`scale_aware_note_aware` accuracy = {note_row_n8['accuracy']:.3f}; `scale_aware_unified` = {unified_row_n8['accuracy']:.3f}.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，更准确的结论是：detector transfer 已经在真实模型-backed stress 下被局部触发，但这个 stress signal 在更高 N 会被 compaction 自己洗掉，因此下一轮要么扩大 N=1/2 hallucination slice，要么设计更持久的 actual hallucination cue。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
