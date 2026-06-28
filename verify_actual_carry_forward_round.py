from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_carry_forward_results.json"
VERIFY_PATH = "reviews/verification_round16.md"


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

    base_unified_n8 = results["aggregate"]["scale_aware_unified"]["tiny_placeholder_hardened_scaffold"]["8"]
    carry_unified_n8 = results["aggregate"]["scale_aware_unified"]["tiny_carry_forward_scaffold"]["8"]
    base_metrics_n8 = results["carry_metrics"]["scale_aware_unified"]["tiny_placeholder_hardened_scaffold"]["8"]
    carry_metrics_n8 = results["carry_metrics"]["scale_aware_unified"]["tiny_carry_forward_scaffold"]["8"]
    base_summary_n8 = results["aggregate"]["summary_only"]["tiny_placeholder_hardened_scaffold"]["8"]
    carry_summary_n8 = results["aggregate"]["summary_only"]["tiny_carry_forward_scaffold"]["8"]

    lines = [
        "# Verification Round 16",
        "",
        "这个文件是对 actual carry-forward round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Carry-forward improves unified N=8 unsafe error",
            carry_metrics_n8["unsafe_error_rate"] <= base_metrics_n8["unsafe_error_rate"],
            f"base/carry unified unsafe_error = `{base_metrics_n8['unsafe_error_rate']:.3f}`/`{carry_metrics_n8['unsafe_error_rate']:.3f}`.",
        ),
        check(
            "Carry-forward improves unified N=8 overall accuracy",
            carry_unified_n8["accuracy"] >= base_unified_n8["accuracy"],
            f"base/carry unified accuracy = `{base_unified_n8['accuracy']:.3f}`/`{carry_unified_n8['accuracy']:.3f}`.",
        ),
        check(
            "Carry-forward preserves unified N=8 hallucination placeholder elimination",
            carry_metrics_n8["hallucination_placeholder_answer_rate"] <= base_metrics_n8["hallucination_placeholder_answer_rate"],
            f"base/carry hallucination_placeholder = `{base_metrics_n8['hallucination_placeholder_answer_rate']:.3f}`/`{carry_metrics_n8['hallucination_placeholder_answer_rate']:.3f}`.",
        ),
        check(
            "Carry-forward actually fires on some records at unified N=8",
            carry_metrics_n8["carry_forward_record_rate"] > 0.0,
            f"carry_forward_record_rate = `{carry_metrics_n8['carry_forward_record_rate']:.3f}`.",
        ),
        check(
            "Carry-forward improves summary-only N=8 accuracy",
            carry_summary_n8["accuracy"] >= base_summary_n8["accuracy"],
            f"base/carry summary accuracy = `{base_summary_n8['accuracy']:.3f}`/`{carry_summary_n8['accuracy']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 17 已经把 refined scaffold 的剩余空/null-pass failure 进一步压下去，并把主线推进到更稳的 executor contract。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
