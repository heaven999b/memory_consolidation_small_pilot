from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/actual_placeholder_hardening_results.json"
VERIFY_PATH = "reviews/verification_round15.md"


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

    refined_unified_n8 = results["aggregate"]["scale_aware_unified"]["tiny_refusal_scaffold"]["8"]
    hardened_unified_n8 = results["aggregate"]["scale_aware_unified"]["tiny_placeholder_hardened_scaffold"]["8"]
    refined_metrics_n8 = results["hardening_metrics"]["scale_aware_unified"]["tiny_refusal_scaffold"]["8"]
    hardened_metrics_n8 = results["hardening_metrics"]["scale_aware_unified"]["tiny_placeholder_hardened_scaffold"]["8"]
    refined_summary_n8 = results["aggregate"]["summary_only"]["tiny_refusal_scaffold"]["8"]
    hardened_summary_n8 = results["aggregate"]["summary_only"]["tiny_placeholder_hardened_scaffold"]["8"]

    lines = [
        "# Verification Round 15",
        "",
        "这个文件是对 actual placeholder hardening round 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Hardened parser improves unified N=8 overall accuracy",
            hardened_unified_n8["accuracy"] >= refined_unified_n8["accuracy"],
            f"refined/hardened unified accuracy = `{refined_unified_n8['accuracy']:.3f}`/`{hardened_unified_n8['accuracy']:.3f}`.",
        ),
        check(
            "Hardened parser eliminates unified N=8 hallucination placeholder answers",
            hardened_metrics_n8["hallucination_placeholder_answer_rate"] <= refined_metrics_n8["hallucination_placeholder_answer_rate"],
            f"refined/hardened hallucination_placeholder = `{refined_metrics_n8['hallucination_placeholder_answer_rate']:.3f}`/`{hardened_metrics_n8['hallucination_placeholder_answer_rate']:.3f}`.",
        ),
        check(
            "Hardened parser preserves unified N=8 unsafe error",
            hardened_metrics_n8["unsafe_error_rate"] <= refined_metrics_n8["unsafe_error_rate"],
            f"refined/hardened unsafe_error = `{refined_metrics_n8['unsafe_error_rate']:.3f}`/`{hardened_metrics_n8['unsafe_error_rate']:.3f}`.",
        ),
        check(
            "Hardened parser preserves unified N=8 target retention",
            hardened_metrics_n8["target_claim_retained_rate"] >= refined_metrics_n8["target_claim_retained_rate"],
            f"refined/hardened target_claim = `{refined_metrics_n8['target_claim_retained_rate']:.3f}`/`{hardened_metrics_n8['target_claim_retained_rate']:.3f}`.",
        ),
        check(
            "Hardened parser improves summary-only N=8 accuracy",
            hardened_summary_n8["accuracy"] >= refined_summary_n8["accuracy"],
            f"refined/hardened summary accuracy = `{refined_summary_n8['accuracy']:.3f}`/`{hardened_summary_n8['accuracy']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 round 16 已经把 refined scaffold 的 frontier 从 placeholder leakage 向更稳定的 reusable parser contract 推进了一步。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
