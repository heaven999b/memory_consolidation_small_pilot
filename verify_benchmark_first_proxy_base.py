from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/benchmark_first_proxy_base.json"
VERIFY_PATH = "reviews/verification_round35_proxy_base.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    proxy_base = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    verdict = proxy_base["verdict"]
    components = proxy_base["component_status"]

    lines = [
        "# Verification Round 35 Proxy Base",
        "",
        "这个文件只做机械核对：确认 benchmark-first proxy base 现在真的已经被补成一份独立、可核对的总工件。",
        "",
        check(
            "Proxy-base verdict is explicitly ready",
            verdict["benchmark_first_proxy_base_ready"] is True,
            f"observed verdict = `{verdict}`.",
        ),
        check(
            "Proxy-base status is pass rather than partial",
            verdict["benchmark_first_proxy_base_status"] == "pass",
            f"observed status = `{verdict['benchmark_first_proxy_base_status']}`.",
        ),
        check(
            "Full TierMem-native grounding remains explicitly false",
            verdict["full_tiermem_native_grounding"] is False,
            f"observed full-native flag = `{verdict['full_tiermem_native_grounding']}`.",
        ),
        check(
            "External benchmark adapter is fully grounded",
            components["external_benchmark_adapter"]["grounding_status"] == "pass",
            f"observed adapter block = `{components['external_benchmark_adapter']}`.",
        ),
        check(
            "Minimal benchmark panel is present and ready",
            components["external_benchmark_minimal_panel"]["ready"] is True
            and components["external_benchmark_minimal_panel"]["panel_names"] == ["halumem_hallucination", "locomo_benign_utility"],
            f"observed minimal-panel block = `{components['external_benchmark_minimal_panel']}`.",
        ),
        check(
            "Broader reviewer section is present and ready",
            components["external_benchmark_reviewer_section"]["ready"] is True
            and components["external_benchmark_reviewer_section"]["family_rollups"] == ["benign_utility_benchmark_section", "hallucination_benchmark_section"],
            f"observed reviewer-section block = `{components['external_benchmark_reviewer_section']}`.",
        ),
        check(
            "Benchmark-first entrypoint exists and is marked ready",
            components["benchmark_first_entrypoint"]["path"] == "run_benchmark_first_primary_entrypoint.py"
            and components["benchmark_first_entrypoint"]["ready"] is True,
            f"observed entrypoint block = `{components['benchmark_first_entrypoint']}`.",
        ),
        check(
            "Primary surface keeps the proxy base complete even after the native-base upgrade",
            components["primary_surface"]["tiermem_style_primary_base_status"] == "pass"
            and components["primary_surface"]["benchmark_first_surface_ready"] is True
            and components["primary_surface"]["benchmark_first_proxy_base_complete"] is True,
            f"observed primary-surface block = `{components['primary_surface']}`.",
        ),
        check(
            "Proxy base explicitly records that the native primary base is now ready",
            components["primary_surface"]["benchmark_native_primary_base_ready"] is True,
            f"observed primary-surface block = `{components['primary_surface']}`.",
        ),
        check(
            "Frontier closure is exact and proxy-free",
            components["frontier_closure"]["exact_non_proxy_frontier_ready"] is True
            and components["frontier_closure"]["proxy_rows"] == 0,
            f"observed frontier block = `{components['frontier_closure']}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 benchmark-first proxy base 这一层已经稳定保留下来，但它不再是主 blocker；主 baseline 现在已经往 benchmark-native primary base 升上去了。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
