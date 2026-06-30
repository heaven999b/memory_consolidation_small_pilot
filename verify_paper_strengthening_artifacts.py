from __future__ import annotations

import json
from pathlib import Path


METHOD_PATH = "outputs/provenance_scaffolded_method_report.json"
STATS_PATH = "outputs/paper_strengthening_stats.json"
ARTIFACT_PATH = "outputs/paper_artifact_contract_report.json"
VERIFY_PATH = "reviews/verification_round38_strengthening.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    method = json.loads((base_dir / METHOD_PATH).read_text(encoding="utf-8"))
    stats = json.loads((base_dir / STATS_PATH).read_text(encoding="utf-8"))
    artifact = json.loads((base_dir / ARTIFACT_PATH).read_text(encoding="utf-8"))

    method_name = method["method_spec"]["name"]
    axis_rows = method["defense_axis_projection"]
    comparison_map = {row["label"]: row for row in stats["comparisons"]}
    artifact_panels = artifact["panels"]

    lines = [
        "# Verification Round 38",
        "",
        "这个文件是对 paper-strengthening artifacts 的机械核对，不引入新的主张。",
        "",
        check(
            "Formal method name is frozen",
            method_name == "Provenance-Scaffolded Unified",
            f"observed method name = `{method_name}`.",
        ),
        check(
            "Formal method exposes four core rules",
            len(method["method_spec"]["rules"]) == 4,
            f"observed rule count = `{len(method['method_spec']['rules'])}`.",
        ),
        check(
            "Defense-axis projection includes the full method row",
            any(row["axis"] == "full_method" for row in axis_rows),
            f"observed axes = `{[row['axis'] for row in axis_rows]}`.",
        ),
        check(
            "Stats artifact reports at least eight paired comparisons",
            len(stats["comparisons"]) >= 8,
            f"observed comparison count = `{len(stats['comparisons'])}`.",
        ),
        check(
            "Scaffolded note persistence improves high-N history-loss over baseline",
            comparison_map["Note persistence N=8 history loss: baseline -> tiny_fixed_scaffold"]["improvement_delta"] > 0,
            f"observed delta = `{comparison_map['Note persistence N=8 history loss: baseline -> tiny_fixed_scaffold']['improvement_delta']}`.",
        ),
        check(
            "Carry-forward lowers unsafe error relative to placeholder hardening alone",
            comparison_map["Carry-forward N=8 unsafe error: tiny_placeholder_hardened_scaffold -> tiny_carry_forward_scaffold"]["improvement_delta"] > 0,
            f"observed delta = `{comparison_map['Carry-forward N=8 unsafe error: tiny_placeholder_hardened_scaffold -> tiny_carry_forward_scaffold']['improvement_delta']}`.",
        ),
        check(
            "Primary model-backed panels now expose per-pass artifact traces",
            all(panel["pass_trace_coverage"] > 0 for panel in artifact_panels.values()),
            f"observed pass-trace coverage = `{artifact_panels}`.",
        ),
        check(
            "Primary model-backed panels now expose stage attribution",
            all(panel["stage_attribution_coverage"] > 0 for panel in artifact_panels.values()),
            f"observed stage coverage = `{artifact_panels}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明我们已经把前面分散的 scaffold/provenance/statistics/artifact work 收束成了一个 reviewer 可读、可审计的 strengthening layer。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
