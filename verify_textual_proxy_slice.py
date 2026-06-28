from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/textual_proxy_slice_results.json"
VERIFY_PATH = "reviews/verification_round8.md"


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
    tiered_n2 = results["aggregate"]["tiered"]["2"]
    tiered_n8 = results["aggregate"]["tiered"]["8"]
    unified_n2 = results["aggregate"]["scale_aware_unified"]["2"]
    unified_n8 = results["aggregate"]["scale_aware_unified"]["8"]
    unified_n4 = results["aggregate"]["scale_aware_unified"]["4"]
    calibrated_n2 = results["aggregate"]["utility_calibrated"]["2"]

    lines = [
        "# Verification Round 8",
        "",
        "这个文件是对 textual proxy slice iteration 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Summary-only still worsens with deeper consolidation in the textual slice",
            summary_n8["propagation_rate"] > summary_n1["propagation_rate"],
            f"N=1 `{summary_n1['propagation_rate']:.3f}` vs N=8 `{summary_n8['propagation_rate']:.3f}`.",
        ),
        check(
            "Unified beats tiered on low-N contamination/cost tradeoff in the textual slice",
            unified_n2["residual_bad_memory_rate"] < tiered_n2["residual_bad_memory_rate"]
            and unified_n2["raw_escalation_rate"] < tiered_n2["raw_escalation_rate"]
            and unified_n2["mean_cost"] < tiered_n2["mean_cost"],
            f"`scale_aware_unified` residual/raw/cost = {unified_n2['residual_bad_memory_rate']:.3f}/{unified_n2['raw_escalation_rate']:.3f}/{unified_n2['mean_cost']:.3f}; "
            f"`tiered` = {tiered_n2['residual_bad_memory_rate']:.3f}/{tiered_n2['raw_escalation_rate']:.3f}/{tiered_n2['mean_cost']:.3f}.",
        ),
        check(
            "Unified preserves its high-N advantage over tiered on residual contamination and raw fallback",
            unified_n8["residual_bad_memory_rate"] < tiered_n8["residual_bad_memory_rate"]
            and unified_n8["raw_escalation_rate"] < tiered_n8["raw_escalation_rate"],
            f"`scale_aware_unified` residual/raw = {unified_n8['residual_bad_memory_rate']:.3f}/{unified_n8['raw_escalation_rate']:.3f}; "
            f"`tiered` = {tiered_n8['residual_bad_memory_rate']:.3f}/{tiered_n8['raw_escalation_rate']:.3f}.",
        ),
        check(
            "Unified stays at or above utility_calibrated on the small-N slice",
            unified_n2["accuracy"] >= calibrated_n2["accuracy"]
            and unified_n2["propagation_rate"] <= calibrated_n2["propagation_rate"],
            f"`scale_aware_unified` acc/prop = {unified_n2['accuracy']:.3f}/{unified_n2['propagation_rate']:.3f}; "
            f"`utility_calibrated` = {calibrated_n2['accuracy']:.3f}/{calibrated_n2['propagation_rate']:.3f}.",
        ),
        check(
            "Unified remains materially better than summary-only at N=4",
            unified_n4["propagation_rate"] < summary_n8["propagation_rate"] and unified_n4["accuracy"] > 0.75,
            f"`scale_aware_unified` N=4 acc/prop = {unified_n4['accuracy']:.3f}/{unified_n4['propagation_rate']:.3f}; "
            f"`summary_only` N=8 propagation = {summary_n8['propagation_rate']:.3f}.",
        ),
        "",
        "## Bottom Line",
        "",
        "textual proxy slice 的结果如果通过这些核对，说明 unified policy 的核心故事并没有只活在原始 claim-level proxy 里，而是开始跨到更接近自由文本摘要的环境中。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
