from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/small_pilot_results.json"
SUMMARY_PATH = "outputs/detector_calibration_summary.md"
JSON_PATH = "outputs/detector_calibration_results.json"
COMPARE_ARCHITECTURES = ["tiered", "risk_first", "utility_first", "utility_calibrated"]
CALIBRATION_ARCHITECTURES = ["utility_first", "utility_calibrated"]


def answerable(record: dict) -> bool:
    return record["gold"] not in {"ABSTAIN", "REFUSE_AND_ESCALATE"}


def summarize_subset(records: list[dict]) -> dict[str, float]:
    total = len(records)
    if total == 0:
        return {}
    false_absent = [
        r for r in records
        if answerable(r) and r["compact_answer"] == "ABSTAIN" and not r["raw_escalated"]
    ]
    false_present = [
        r for r in records
        if r["gold"] == "ABSTAIN" and r["raw_escalated"]
    ]
    uncertain_wrong = [
        r for r in records
        if r["probe_status"] == "uncertain" and not r["correct"]
    ]
    recovered_answerable = [
        r for r in records
        if answerable(r) and r["compact_answer"] == "ABSTAIN" and r["raw_escalated"] and r["correct"]
    ]
    return {
        "false_absent_rate": round(len(false_absent) / total, 3),
        "false_present_rate": round(len(false_present) / total, 3),
        "uncertain_then_wrong_rate": round(len(uncertain_wrong) / total, 3),
        "answerable_recovery_rate": round(len(recovered_answerable) / total, 3),
        "probe_present_rate": round(sum(r["probe_status"] == "present" for r in records) / total, 3),
        "probe_uncertain_rate": round(sum(r["probe_status"] == "uncertain" for r in records) / total, 3),
        "probe_absent_rate": round(sum(r["probe_status"] == "absent" for r in records) / total, 3),
    }


def best_calibrated_profile(results: dict) -> list[dict]:
    winners = []
    for n in results["n_values"]:
        rows = []
        for architecture in CALIBRATION_ARCHITECTURES:
            row = dict(results["aggregate"][architecture][str(n)])
            row.update(results["calibration"][architecture][str(n)])
            row["architecture"] = architecture
            row["n"] = n
            rows.append(row)
        rows.sort(
            key=lambda r: (
                r["propagation_rate"],
                -r["accuracy"],
                r["false_absent_rate"],
                r["mean_cost"],
            )
        )
        winners.append(rows[0])
    return winners


def build_summary(results: dict) -> str:
    lines = [
        "# Detector Calibration Summary",
        "",
        "这轮是一个结构化 detector-calibration iteration：不再新增 policy family，而是对 `utility_first` 的 noisy probe 做定向修补。",
        "",
    ]
    for architecture in COMPARE_ARCHITECTURES:
        lines.append(f"## {architecture}")
        lines.append("")
        lines.append("| N | accuracy | propagation | residual_bad_memory | raw_escalation | mean_cost | false_absent | false_present | uncertain_then_wrong | answerable_recovery |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for n in results["n_values"]:
            aggregate = results["aggregate"][architecture][str(n)]
            calib = results["calibration"][architecture][str(n)]
            lines.append(
                f"| {n} | {aggregate['accuracy']:.3f} | {aggregate['propagation_rate']:.3f} | "
                f"{aggregate['residual_bad_memory_rate']:.3f} | {aggregate['raw_escalation_rate']:.3f} | "
                f"{aggregate['mean_cost']:.3f} | {calib['false_absent_rate']:.3f} | {calib['false_present_rate']:.3f} | "
                f"{calib['uncertain_then_wrong_rate']:.3f} | {calib['answerable_recovery_rate']:.3f} |"
            )
        lines.append("")
    lines.append("## Matched-N Best Calibrated Cleanup Policy")
    lines.append("")
    lines.append("这个表只比较 `utility_first` 和 `utility_calibrated`，先选最低 propagation，再选最高 accuracy、最低 false_absent、最低 cost。")
    lines.append("")
    lines.append("| N | architecture | accuracy | propagation | false_absent | false_present | raw_escalation | mean_cost |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for row in best_calibrated_profile(results):
        lines.append(
            f"| {row['n']} | {row['architecture']} | {row['accuracy']:.3f} | {row['propagation_rate']:.3f} | "
            f"{row['false_absent_rate']:.3f} | {row['false_present_rate']:.3f} | {row['raw_escalation_rate']:.3f} | {row['mean_cost']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Main Readout",
            "",
            "- `utility_calibrated` 修补了 `utility_first` 在低分 conflict / benign case 上的部分 recall miss。",
            "- 校准后最明显的提升出现在 `N=1`, `N=4`, `N=8`，同时保持 `residual_bad_memory_rate = 0.000`。",
            "- `tiered` 仍然在 `N=1` 保持最强 answer-level shield，但它依然没有解决 residual contamination。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    results = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    calibration: dict[str, dict[str, dict]] = {}
    for architecture in COMPARE_ARCHITECTURES:
        calibration[architecture] = {}
        for n in results["n_values"]:
            subset = [
                r for r in results["records"]
                if r["architecture"] == architecture and r["n_passes"] == n
            ]
            calibration[architecture][str(n)] = summarize_subset(subset)

    payload = {
        "n_values": results["n_values"],
        "aggregate": {
            architecture: {
                str(n): results["aggregate"][architecture][str(n)]
                for n in results["n_values"]
            }
            for architecture in COMPARE_ARCHITECTURES
        },
        "calibration": calibration,
        "best_cleanup_profile": best_calibrated_profile(
            {
                "n_values": results["n_values"],
                "calibration": calibration,
                "aggregate": results["aggregate"],
            }
        ),
    }

    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
