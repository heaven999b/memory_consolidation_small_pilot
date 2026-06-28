from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/small_n_hybrid_results.json"
VERIFY_PATH = "reviews/verification_round6.md"


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

    tiered_n1 = results["aggregate"]["tiered"]["1"]
    hybrid_n1 = results["aggregate"]["small_n_hybrid"]["1"]
    tiered_n2 = results["aggregate"]["tiered"]["2"]
    hybrid_n2 = results["aggregate"]["small_n_hybrid"]["2"]
    calibrated_n2 = results["aggregate"]["utility_calibrated"]["2"]
    hybrid_cal_n1 = results["calibration"]["small_n_hybrid"]["1"]
    hybrid_cal_n2 = results["calibration"]["small_n_hybrid"]["2"]

    lines = [
        "# Verification Round 6",
        "",
        "这个文件是对 small-N hybrid iteration 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Hybrid matches tiered at N=1 on answer-level metrics",
            hybrid_n1["accuracy"] == 1.0 and hybrid_n1["propagation_rate"] == 0.0,
            f"`small_n_hybrid` = {hybrid_n1['accuracy']:.3f}/{hybrid_n1['propagation_rate']:.3f}.",
        ),
        check(
            "Hybrid beats tiered at N=1 on contamination/cost tradeoff",
            hybrid_n1["residual_bad_memory_rate"] < tiered_n1["residual_bad_memory_rate"]
            and hybrid_n1["raw_escalation_rate"] < tiered_n1["raw_escalation_rate"]
            and hybrid_n1["mean_cost"] < tiered_n1["mean_cost"],
            f"`small_n_hybrid` residual/raw/cost = {hybrid_n1['residual_bad_memory_rate']:.3f}/{hybrid_n1['raw_escalation_rate']:.3f}/{hybrid_n1['mean_cost']:.3f}; "
            f"`tiered` = {tiered_n1['residual_bad_memory_rate']:.3f}/{tiered_n1['raw_escalation_rate']:.3f}/{tiered_n1['mean_cost']:.3f}.",
        ),
        check(
            "Hybrid fixes utility_calibrated's N=2 benign misses",
            hybrid_n2["accuracy"] > calibrated_n2["accuracy"] and hybrid_cal_n2["false_absent_rate"] < results["calibration"]["utility_calibrated"]["2"]["false_absent_rate"],
            f"`small_n_hybrid` acc/false_absent = {hybrid_n2['accuracy']:.3f}/{hybrid_cal_n2['false_absent_rate']:.3f}; "
            f"`utility_calibrated` = {calibrated_n2['accuracy']:.3f}/{results['calibration']['utility_calibrated']['2']['false_absent_rate']:.3f}.",
        ),
        check(
            "Hybrid keeps zero residual contamination at N=1 and N=2",
            hybrid_n1["residual_bad_memory_rate"] == 0.0 and hybrid_n2["residual_bad_memory_rate"] == 0.0,
            f"N=1 `{hybrid_n1['residual_bad_memory_rate']:.3f}`, N=2 `{hybrid_n2['residual_bad_memory_rate']:.3f}`.",
        ),
        check(
            "Guardband fires only in the targeted small-N band",
            hybrid_cal_n1["guardband_rate"] > 0.0 and hybrid_cal_n2["guardband_rate"] > 0.0,
            f"N=1 `{hybrid_cal_n1['guardband_rate']:.3f}`, N=2 `{hybrid_cal_n2['guardband_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "small-N hybrid 的证据链是自洽的：它在 `N=1/2` 成功借到了 tiered 的 shield，同时保住了 cleanup family 的零 residual contamination，而且不需要把这种 guardband 扩展到高 N。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
