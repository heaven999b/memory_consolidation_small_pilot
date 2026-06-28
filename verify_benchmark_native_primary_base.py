from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/benchmark_native_primary_base.json"
VERIFY_PATH = "reviews/verification_round36_native_primary_base.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    payload = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    verdict = payload["verdict"]
    native = payload["native_contract_summary"]
    strengthening = payload["strengthening_status"]

    lines = [
        "# Verification Round 36 Native Primary Base",
        "",
        "这个文件只做机械核对：确认主 baseline 的实现表面现在真的已经升到 benchmark-native primary base，而不再只是 local proxy surface。",
        "",
        check(
            "Native primary-base verdict is explicitly ready",
            verdict["benchmark_native_primary_base_ready"] is True,
            f"observed verdict = `{verdict}`.",
        ),
        check(
            "TierMem-style primary-base status is now pass",
            verdict["tiermem_style_primary_base_status"] == "pass",
            f"observed status = `{verdict['tiermem_style_primary_base_status']}`.",
        ),
        check(
            "Runtime projection is valid for every native packet",
            native["runtime_projection_valid_count"] == native["runtime_projection_total_count"],
            f"observed runtime projection = `{native['runtime_projection_valid_count']}/{native['runtime_projection_total_count']}`.",
        ),
        check(
            "Native primary base covers four slice panels",
            native["panel_count"] == 4,
            f"observed panel count = `{native['panel_count']}`.",
        ),
        check(
            "Native primary base covers at least three benchmark families",
            sorted(native["benchmark_families"]) == ["HaluMem", "LoCoMo", "LongMemEval"],
            f"observed benchmark families = `{native['benchmark_families']}`.",
        ),
        check(
            "Native primary base covers both hallucination and benign task families",
            sorted(native["task_families"]) == ["benign", "hallucination"],
            f"observed task families = `{native['task_families']}`.",
        ),
        check(
            "Broader benchmark coverage strengthening is explicitly marked pass",
            strengthening["broader_benchmark_coverage_status"] == "pass",
            f"observed strengthening block = `{strengthening}`.",
        ),
        check(
            "Synthetic reference is explicitly demoted to support-only",
            strengthening["synthetic_reference_role"] == "support_only",
            f"observed synthetic role = `{strengthening['synthetic_reference_role']}`.",
        ),
        check(
            "Reviewer sequence starts from the native primary base",
            strengthening["reviewer_primary_sequence"][0] == "benchmark_native_primary_base",
            f"observed sequence = `{strengthening['reviewer_primary_sequence']}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明我们已经把最关键的 primary-base blocker 从代码和 artifact 层都补掉了；接下来主要是继续扩 benchmark scale，而不是再补 proxy 主表面。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
