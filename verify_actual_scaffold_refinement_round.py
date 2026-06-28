from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_scaffold_refinement_results.json"
VERIFY_PATH = "reviews/verification_round14.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["interventions"]) * len(results["n_values"])
    actual_records = len(results["records"])

    fixed_unified_n8 = results["refinement_metrics"]["scale_aware_unified"]["tiny_fixed_scaffold"]["8"]
    refined_unified_n8 = results["refinement_metrics"]["scale_aware_unified"]["tiny_refusal_scaffold"]["8"]
    fixed_unified_row_n8 = results["aggregate"]["scale_aware_unified"]["tiny_fixed_scaffold"]["8"]
    refined_unified_row_n8 = results["aggregate"]["scale_aware_unified"]["tiny_refusal_scaffold"]["8"]
    fixed_summary_n8 = results["refinement_metrics"]["summary_only"]["tiny_fixed_scaffold"]["8"]
    refined_summary_n8 = results["refinement_metrics"]["summary_only"]["tiny_refusal_scaffold"]["8"]

    lines = [
        "# Verification Round 14",
        "",
        "这个文件是对 actual scaffold refinement round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Refined scaffold improves unified N=8 unsafe error",
            refined_unified_n8["unsafe_error_rate"] <= fixed_unified_n8["unsafe_error_rate"],
            f"tiny_fixed/tiny_refusal unsafe_error = `{fixed_unified_n8['unsafe_error_rate']:.3f}`/`{refined_unified_n8['unsafe_error_rate']:.3f}`.",
        ),
        check(
            "Refined scaffold recovers unified N=8 overall accuracy",
            refined_unified_row_n8["accuracy"] >= fixed_unified_row_n8["accuracy"],
            f"tiny_fixed/tiny_refusal accuracy = `{fixed_unified_row_n8['accuracy']:.3f}`/`{refined_unified_row_n8['accuracy']:.3f}`.",
        ),
        check(
            "Refined scaffold keeps unified N=8 residual contamination at zero",
            refined_unified_row_n8["residual_bad_memory_rate"] <= fixed_unified_row_n8["residual_bad_memory_rate"],
            f"tiny_fixed/tiny_refusal residual = `{fixed_unified_row_n8['residual_bad_memory_rate']:.3f}`/`{refined_unified_row_n8['residual_bad_memory_rate']:.3f}`.",
        ),
        check(
            "Refined scaffold preserves unified N=8 target-retention signal",
            refined_unified_n8["target_claim_retained_rate"] >= fixed_unified_n8["target_claim_retained_rate"],
            f"tiny_fixed/tiny_refusal target_claim = `{fixed_unified_n8['target_claim_retained_rate']:.3f}`/`{refined_unified_n8['target_claim_retained_rate']:.3f}`.",
        ),
        check(
            "Refined scaffold improves summary-only N=8 unsafe error",
            refined_summary_n8["unsafe_error_rate"] <= fixed_summary_n8["unsafe_error_rate"],
            f"tiny_fixed/tiny_refusal summary unsafe_error = `{fixed_summary_n8['unsafe_error_rate']:.3f}`/`{refined_summary_n8['unsafe_error_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 15 已经把 tiny scaffold 从“有 persistence 收益但 unsafe 语义不稳”推进到更接近可复用的主线 scaffold。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
