from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_recall_expansion_results.json"
VERIFY_PATH = "reviews/verification_round11.md"


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

    summary_n1 = results["recall_metrics"]["summary_only"]["1"]
    summary_n8 = results["recall_metrics"]["summary_only"]["8"]
    tiered_n8 = results["aggregate"]["tiered"]["8"]
    unified_n8 = results["aggregate"]["scale_aware_unified"]["8"]
    unified_metrics_n8 = results["recall_metrics"]["scale_aware_unified"]["8"]
    note_n8 = results["aggregate"]["scale_aware_note_aware"]["8"]

    lines = [
        "# Verification Round 11",
        "",
        "这个文件是对 actual recall expansion round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Summary-only benign/conflict errors worsen with deeper real-model compaction",
            summary_n8["benign_conflict_error_rate"] > summary_n1["benign_conflict_error_rate"],
            f"N=1 `{summary_n1['benign_conflict_error_rate']:.3f}` vs N=8 `{summary_n8['benign_conflict_error_rate']:.3f}`.",
        ),
        check(
            "High-N empty-note-then-abstain emerges in the expanded recall slice",
            summary_n8["empty_note_then_abstain_rate"] > 0.0,
            f"N=8 empty_note_then_abstain = `{summary_n8['empty_note_then_abstain_rate']:.3f}`.",
        ),
        check(
            "Unified still beats tiered on high-N contamination and raw fallback in the recall slice",
            unified_n8["residual_bad_memory_rate"] < tiered_n8["residual_bad_memory_rate"]
            and unified_n8["raw_escalation_rate"] < tiered_n8["raw_escalation_rate"],
            f"`scale_aware_unified` residual/raw = {unified_n8['residual_bad_memory_rate']:.3f}/{unified_n8['raw_escalation_rate']:.3f}; "
            f"`tiered` = {tiered_n8['residual_bad_memory_rate']:.3f}/{tiered_n8['raw_escalation_rate']:.3f}.",
        ),
        check(
            "Unified keeps zero residual contamination even when history loss rises",
            unified_n8["residual_bad_memory_rate"] == 0.0 and unified_metrics_n8["history_loss_rate"] > 0.0,
            f"residual/history_loss = {unified_n8['residual_bad_memory_rate']:.3f}/{unified_metrics_n8['history_loss_rate']:.3f}.",
        ),
        check(
            "Note-aware detector does not underperform unified on the recall slice at N=8",
            note_n8["accuracy"] >= unified_n8["accuracy"],
            f"`scale_aware_note_aware` accuracy = {note_n8['accuracy']:.3f}; `scale_aware_unified` = {unified_n8['accuracy']:.3f}.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明扩大的真实 slice 已经把 bottleneck 指向 benign/conflict answerability loss，而不是把我们带回更早的污染传播问题。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
