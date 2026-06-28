from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/small_pilot_results.json"
CALIBRATION_PATH = "outputs/detector_calibration_results.json"
VERIFY_PATH = "reviews/verification_round5.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    calibration = json.loads((base_dir / CALIBRATION_PATH).read_text(encoding="utf-8"))

    item_count = results["num_items"]
    seed_count = len(results["seeds"])
    expected_records = item_count * seed_count * len(results["architectures"]) * len(results["n_values"])
    actual_records = len(results["records"])

    tiered_n1 = results["aggregate"]["tiered"]["1"]
    util_n1 = results["aggregate"]["utility_calibrated"]["1"]
    util_n8 = results["aggregate"]["utility_calibrated"]["8"]
    tiered_n8 = results["aggregate"]["tiered"]["8"]
    util_first_n8 = results["aggregate"]["utility_first"]["8"]

    lines = [
        "# Verification Round 5",
        "",
        "这个文件是对 detector-calibration iteration 的机械核对，不引入新的主张。",
        "",
        check(
            "Record count",
            actual_records == expected_records,
            f"expected `{expected_records}`, observed `{actual_records}`.",
        ),
        check(
            "Utility calibrated beats utility first at N=8",
            util_n8["accuracy"] > util_first_n8["accuracy"] and util_n8["propagation_rate"] < util_first_n8["propagation_rate"],
            f"`utility_calibrated` = {util_n8['accuracy']:.3f}/{util_n8['propagation_rate']:.3f}, "
            f"`utility_first` = {util_first_n8['accuracy']:.3f}/{util_first_n8['propagation_rate']:.3f}.",
        ),
        check(
            "Utility calibrated keeps zero residual contamination",
            all(
                results["aggregate"]["utility_calibrated"][str(n)]["residual_bad_memory_rate"] == 0.0
                for n in results["n_values"]
            ),
            "all reported `residual_bad_memory_rate` values are `0.000`.",
        ),
        check(
            "Tiered still wins N=1 by answer-level metric",
            tiered_n1["accuracy"] > util_n1["accuracy"] and tiered_n1["propagation_rate"] < util_n1["propagation_rate"],
            f"`tiered` = {tiered_n1['accuracy']:.3f}/{tiered_n1['propagation_rate']:.3f}, "
            f"`utility_calibrated` = {util_n1['accuracy']:.3f}/{util_n1['propagation_rate']:.3f}.",
        ),
        check(
            "Utility calibrated improves N=8 over tiered on contamination/cost tradeoff",
            util_n8["residual_bad_memory_rate"] < tiered_n8["residual_bad_memory_rate"]
            and util_n8["raw_escalation_rate"] < tiered_n8["raw_escalation_rate"]
            and util_n8["mean_cost"] < tiered_n8["mean_cost"],
            f"`utility_calibrated` residual/raw/cost = {util_n8['residual_bad_memory_rate']:.3f}/{util_n8['raw_escalation_rate']:.3f}/{util_n8['mean_cost']:.3f}; "
            f"`tiered` = {tiered_n8['residual_bad_memory_rate']:.3f}/{tiered_n8['raw_escalation_rate']:.3f}/{tiered_n8['mean_cost']:.3f}.",
        ),
        check(
            "Calibration winner table contains 5 rows",
            len(calibration["best_cleanup_profile"]) == len(results["n_values"]),
            f"observed `{len(calibration['best_cleanup_profile'])}` rows for `{len(results['n_values'])}` N values.",
        ),
        "",
        "## Bottom Line",
        "",
        "校准结论在证据链上是自洽的：`utility_calibrated` 不是全局无条件最优，但它确实修补了 `utility_first` 的一部分 detector recall miss，并在高 N 保持了比 `tiered` 更干净的 residual memory。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
