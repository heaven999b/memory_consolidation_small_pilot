from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/tiermem_style_primary_surface.json"
VERIFY_PATH = "reviews/verification_round34_primary_surface.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    surface = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    status = surface["primary_surface_status"]
    benchmark_core = surface["benchmark_grounded_core"]
    support = surface["model_backed_support"]

    lines = [
        "# Verification Round 34 Primary Surface",
        "",
        "这个文件只做机械核对：确认 repo 现在确实有一个 benchmark-first 的 primary surface，而不是继续只靠 packet 文字说明。",
        "",
        check(
            "Primary surface is explicitly marked benchmark-first ready",
            status["benchmark_first_surface_ready"] is True,
            f"observed status block = `{status}`.",
        ),
        check(
            "TierMem-style primary base is now marked pass",
            status["tiermem_style_primary_base_status"] == "pass",
            f"observed primary-base status = `{status['tiermem_style_primary_base_status']}`.",
        ),
        check(
            "Full TierMem-native grounding remains explicitly false",
            status["full_tiermem_native_grounding"] is False,
            f"observed full-native flag = `{status['full_tiermem_native_grounding']}`.",
        ),
        check(
            "Reviewer sequence starts from the benchmark-native primary base",
            bool(surface["reviewer_sequence"]) and "benchmark-native primary base" in surface["reviewer_sequence"][0],
            f"observed reviewer sequence = `{surface['reviewer_sequence']}`.",
        ),
        check(
            "Benchmark core now uses the broader reviewer section rather than the minimal starter panel",
            benchmark_core["source_kind"] == "broader_reviewer_section",
            f"observed source kind = `{benchmark_core['source_kind']}`.",
        ),
        check(
            "Benchmark core exposes both broader family rollups",
            benchmark_core["panel_names"] == ["benign_utility_benchmark_section", "hallucination_benchmark_section"],
            f"observed panel names = `{benchmark_core['panel_names']}`.",
        ),
        check(
            "Benchmark core references four slice panels behind the family rollups",
            benchmark_core["slice_panel_names"] == ["halumem_core_v2", "halumem_holdout_v1", "locomo_core_v2", "longmemeval_direct_v1"],
            f"observed slice panel names = `{benchmark_core['slice_panel_names']}`.",
        ),
        check(
            "Benchmark core keeps 16-item family rollups on both sides",
            benchmark_core["panels"]["hallucination_benchmark_section"]["num_items"] == 16
            and benchmark_core["panels"]["benign_utility_benchmark_section"]["num_items"] == 16,
            (
                f"observed counts = `{benchmark_core['panels']['hallucination_benchmark_section']['num_items']}`, "
                f"`{benchmark_core['panels']['benign_utility_benchmark_section']['num_items']}`."
            ),
        ),
        check(
            "Benchmark core keeps all four architectures at N=8",
            sorted(benchmark_core["panels"]["hallucination_benchmark_section"]["n8_rows"].keys()) == ["scale_aware_note_aware", "scale_aware_unified", "summary_only", "tiered"]
            and sorted(benchmark_core["panels"]["benign_utility_benchmark_section"]["n8_rows"].keys()) == ["scale_aware_note_aware", "scale_aware_unified", "summary_only", "tiered"],
            f"observed HaluMem methods = `{sorted(benchmark_core['panels']['hallucination_benchmark_section']['n8_rows'].keys())}`.",
        ),
        check(
            "Benchmark-first entrypoint is explicitly surfaced and marked ready",
            status["benchmark_first_entrypoint_path"] == "run_benchmark_first_primary_entrypoint.py"
            and status["benchmark_first_entrypoint_ready"] is True,
            (
                f"observed entrypoint = `{status['benchmark_first_entrypoint_path']}`, "
                f"ready = `{status['benchmark_first_entrypoint_ready']}`."
            ),
        ),
        check(
            "Primary surface now explicitly marks the benchmark-first proxy base complete",
            status["benchmark_first_proxy_base_path"] == "outputs/benchmark_first_proxy_base.json"
            and status["benchmark_first_proxy_base_complete"] is True,
            (
                f"observed proxy-base path = `{status['benchmark_first_proxy_base_path']}`, "
                f"complete = `{status['benchmark_first_proxy_base_complete']}`."
            ),
        ),
        check(
            "Primary surface explicitly marks the benchmark-native primary base ready",
            status["benchmark_native_primary_base_path"] == "outputs/benchmark_native_primary_base.json"
            and status["benchmark_native_primary_base_ready"] is True
            and status["benchmark_native_primary_base_status"] == "pass",
            (
                f"observed native-base path = `{status['benchmark_native_primary_base_path']}`, "
                f"ready = `{status['benchmark_native_primary_base_ready']}`, "
                f"status = `{status['benchmark_native_primary_base_status']}`."
            ),
        ),
        check(
            "Primary surface explicitly marks the frontier as proxy-free",
            status["exact_non_proxy_frontier_ready"] is True,
            f"observed exact-frontier flag = `{status['exact_non_proxy_frontier_ready']}`.",
        ),
        check(
            "Model-backed support layers are attached",
            sorted(support.keys()) == ["actual_hallucination_stress", "actual_recall_expansion"],
            f"observed support layers = `{sorted(support.keys())}`.",
        ),
        check(
            "Synthetic reference still exists but is no longer the only top-level surface",
            "synthetic_reference" in surface and benchmark_core["panel_names"] != [],
            f"synthetic reference present = `{'synthetic_reference' in surface}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 repo 的主表面已经不只是 minimal starter panel，也不再只是 proxy-first surface，而是升级成了 benchmark-native primary base；同时它仍然诚实地区分了“baseline 已过”和“还没到最终 paper 版本”。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
