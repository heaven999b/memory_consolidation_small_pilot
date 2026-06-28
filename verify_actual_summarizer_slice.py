from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_summarizer_slice_results.json"
VERIFY_PATH = "reviews/verification_round10.md"


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

    summary_n1 = results["aggregate"]["summary_only"]["1"]
    summary_n8 = results["aggregate"]["summary_only"]["8"]
    tiered_n8 = results["aggregate"]["tiered"]["8"]
    unified_n8 = results["aggregate"]["scale_aware_unified"]["8"]
    note_n8 = results["aggregate"]["scale_aware_note_aware"]["8"]
    note_metrics_n8 = results["slice_metrics"]["scale_aware_note_aware"]["8"]
    unified_metrics_n8 = results["slice_metrics"]["scale_aware_unified"]["8"]

    lines = [
        "# Verification Round 10",
        "",
        "这个文件是对 actual summarizer slice 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Summary-only still worsens with deeper consolidation under the actual summarizer",
            summary_n8["propagation_rate"] > summary_n1["propagation_rate"],
            f"N=1 `{summary_n1['propagation_rate']:.3f}` vs N=8 `{summary_n8['propagation_rate']:.3f}`.",
        ),
        check(
            "Unified beats tiered on high-N contamination and raw fallback under the actual summarizer",
            unified_n8["residual_bad_memory_rate"] < tiered_n8["residual_bad_memory_rate"]
            and unified_n8["raw_escalation_rate"] < tiered_n8["raw_escalation_rate"],
            f"`scale_aware_unified` residual/raw = {unified_n8['residual_bad_memory_rate']:.3f}/{unified_n8['raw_escalation_rate']:.3f}; "
            f"`tiered` = {tiered_n8['residual_bad_memory_rate']:.3f}/{tiered_n8['raw_escalation_rate']:.3f}.",
        ),
        check(
            "Actual slice does not reintroduce hallucination false-present under the cleanup family at N=8",
            note_metrics_n8["hallucination_false_present_rate"] <= unified_metrics_n8["hallucination_false_present_rate"],
            f"`scale_aware_note_aware` = {note_metrics_n8['hallucination_false_present_rate']:.3f}; "
            f"`scale_aware_unified` = {unified_metrics_n8['hallucination_false_present_rate']:.3f}.",
        ),
        check(
            "Note-aware detector keeps zero residual contamination at N=8",
            note_n8["residual_bad_memory_rate"] == 0.0,
            f"`scale_aware_note_aware` residual = {note_n8['residual_bad_memory_rate']:.3f}.",
        ),
        check(
            "Note-aware detector does not underperform unified at N=8 on accuracy",
            note_n8["accuracy"] >= unified_n8["accuracy"],
            f"`scale_aware_note_aware` accuracy = {note_n8['accuracy']:.3f}; `scale_aware_unified` = {unified_n8['accuracy']:.3f}.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明真实 summarizer slice 已经保留住主线趋势；至于 detector gain，本轮更准确的结论是它没有被 actual slice 反驳，但也还没有在这个更保守的真实 summarizer 上再次被强力触发。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
