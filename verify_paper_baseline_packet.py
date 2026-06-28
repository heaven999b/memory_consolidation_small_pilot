from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = "outputs/paper_baseline_packet.json"
VERIFY_PATH = "reviews/verification_round34.md"


def check(label: str, passed: bool, detail: str) -> str:
    status = "PASS" if passed else "FAIL"
    return f"- [{status}] {label}: {detail}"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    packet = json.loads((base_dir / RESULTS_PATH).read_text(encoding="utf-8"))
    reqs = {row["key"]: row for row in packet["requirements"]}
    synthetic = packet["synthetic_core_panel"]["snapshots"]
    frontier = packet["frontier_status"]
    benchmark_adapter = packet.get("benchmark_adapter") or {}
    benchmark_panel = packet.get("benchmark_grounded_panel") or {}
    benchmark_section = packet.get("benchmark_reviewer_section") or {}
    primary_surface = packet.get("primary_surface") or {}
    proxy_base = packet.get("benchmark_first_proxy_base") or {}
    native_primary_base = packet.get("benchmark_native_primary_base") or {}

    lines = [
        "# Verification Round 34",
        "",
        "这个文件是对 paper baseline packet 的机械核对，不引入新的主张。",
        "",
        check(
            "Minimal closed-loop baseline is explicitly marked ready",
            packet["verdict"]["minimal_closed_loop_baseline_ready"] is True,
            f"observed verdict = `{packet['verdict']}`.",
        ),
        check(
            "Paper-level baseline is still explicitly marked not ready",
            packet["verdict"]["paper_level_baseline_ready"] is False,
            f"observed verdict = `{packet['verdict']}`.",
        ),
        check(
            "Baseline trio is frozen in the synthetic core panel",
            all(name in synthetic for name in ["raw_only", "summary_only", "tiered"]),
            f"observed synthetic methods = `{sorted(synthetic.keys())}`.",
        ),
        check(
            "Best method is still included beside the baseline trio",
            "scale_aware_unified" in synthetic,
            f"observed synthetic methods = `{sorted(synthetic.keys())}`.",
        ),
        check(
            "Closed-loop trio requirement is marked pass",
            reqs["closed_loop_baseline_trio"]["status"] == "pass",
            f"observed status = `{reqs['closed_loop_baseline_trio']['status']}`.",
        ),
        check(
            "Real-model recall sanity requirement is marked pass",
            reqs["real_model_benign_conflict_sanity"]["status"] == "pass",
            f"observed status = `{reqs['real_model_benign_conflict_sanity']['status']}`.",
        ),
        check(
            "Real-model hallucination sanity requirement is marked pass",
            reqs["real_model_hallucination_sanity"]["status"] == "pass",
            f"observed status = `{reqs['real_model_hallucination_sanity']['status']}`.",
        ),
        check(
            "External benchmark grounding is no longer a pure gap",
            reqs["primary_external_benchmark_grounding"]["status"] in {"partial", "pass"},
            f"observed status = `{reqs['primary_external_benchmark_grounding']['status']}`.",
        ),
        check(
            "TierMem-style primary grounding is now marked pass",
            reqs["tiermem_style_primary_base"]["status"] == "pass",
            f"observed status = `{reqs['tiermem_style_primary_base']['status']}`.",
        ),
        check(
            "Primary surface artifact is attached when TierMem-style grounding rises above gap",
            (reqs["tiermem_style_primary_base"]["status"] == "gap") or bool(primary_surface),
            f"observed primary surface keys = `{sorted(primary_surface.keys())}`.",
        ),
        check(
            "Benchmark-native primary-base artifact is attached when primary grounding reaches pass",
            (reqs["tiermem_style_primary_base"]["status"] != "pass") or bool(native_primary_base),
            f"observed native-primary-base keys = `{sorted(native_primary_base.keys())}`.",
        ),
        check(
            "Broader reviewer section is attached when external grounding reaches pass",
            (reqs["primary_external_benchmark_grounding"]["status"] != "pass") or bool(benchmark_section),
            f"observed reviewer section keys = `{sorted(benchmark_section.keys())}`.",
        ),
        check(
            "Primary surface status matches the packet requirement",
            (not primary_surface) or primary_surface["primary_surface_status"]["tiermem_style_primary_base_status"] == reqs["tiermem_style_primary_base"]["status"],
            (
                f"observed surface status = `{None if not primary_surface else primary_surface['primary_surface_status']['tiermem_style_primary_base_status']}`, "
                f"packet status = `{reqs['tiermem_style_primary_base']['status']}`."
            ),
        ),
        check(
            "Benchmark-first proxy-base requirement is no longer a pure gap",
            reqs["benchmark_first_proxy_base_complete"]["status"] in {"partial", "pass"},
            f"observed status = `{reqs['benchmark_first_proxy_base_complete']['status']}`.",
        ),
        check(
            "Proxy-base artifact is attached when the proxy-base requirement rises above gap",
            (reqs["benchmark_first_proxy_base_complete"]["status"] == "gap") or bool(proxy_base),
            f"observed proxy-base keys = `{sorted(proxy_base.keys())}`.",
        ),
        check(
            "Primary surface pass still honestly reports non-literal-full-native grounding",
            (reqs["tiermem_style_primary_base"]["status"] != "pass")
            or (
                primary_surface["primary_surface_status"]["benchmark_first_surface_ready"] is True
                and primary_surface["primary_surface_status"]["full_tiermem_native_grounding"] is False
                and primary_surface["primary_surface_status"]["benchmark_native_primary_base_ready"] is True
                and primary_surface["primary_surface_status"]["benchmark_source_kind"] in {"broader_reviewer_section", "minimal_starter_panel"}
            ),
            f"observed primary surface block = `{primary_surface.get('primary_surface_status')}`.",
        ),
        check(
            "Primary surface now prefers the broader reviewer section",
            (not primary_surface) or primary_surface["primary_surface_status"]["benchmark_source_kind"] == "broader_reviewer_section",
            f"observed source kind = `{None if not primary_surface else primary_surface['primary_surface_status']['benchmark_source_kind']}`.",
        ),
        check(
            "Proxy-base artifact says the local proxy baseline is complete but still non-native",
            (not proxy_base)
            or (
                proxy_base["verdict"]["benchmark_first_proxy_base_ready"] is True
                and proxy_base["verdict"]["benchmark_first_proxy_base_status"] == "pass"
                and proxy_base["verdict"]["full_tiermem_native_grounding"] is False
            ),
            f"observed proxy-base verdict = `{proxy_base.get('verdict')}`.",
        ),
        check(
            "Native primary-base artifact says the blocker is resolved while full literal parity remains false",
            (not native_primary_base)
            or (
                native_primary_base["verdict"]["benchmark_native_primary_base_ready"] is True
                and native_primary_base["verdict"]["tiermem_style_primary_base_status"] == "pass"
                and native_primary_base["verdict"]["full_tiermem_native_grounding"] is False
            ),
            f"observed native-primary-base verdict = `{native_primary_base.get('verdict')}`.",
        ),
        check(
            "Model-backed panel multi-seed status matches the frozen seeds",
            (reqs["multi_seed_model_backed_panel"]["status"] == "pass") == (len(packet["model_backed_sanity"]["actual_recall_expansion"]["seeds"]) > 1 and len(packet["model_backed_sanity"]["actual_hallucination_stress"]["seeds"]) > 1),
            f"observed status = `{reqs['multi_seed_model_backed_panel']['status']}`.",
        ),
        check(
            "Frontier exact-closure status matches reintegration mode",
            (
                (reqs["exact_non_proxy_frontier_closure"]["status"] == "pass" and frontier["claim_reintegration_mode"] == "exact_stress_closure_reintegration" and frontier["claim_reintegration_proxy_rows"] == 0)
                or (reqs["exact_non_proxy_frontier_closure"]["status"] == "gap" and frontier["claim_reintegration_mode"] == "proxy_expanded_stitch")
            ),
            f"observed frontier mode = `{frontier['claim_reintegration_mode']}`, proxy rows = `{frontier['claim_reintegration_proxy_rows']}`.",
        ),
        check(
            "Benchmark adapter packet is attached when external grounding is above pure gap",
            (reqs["primary_external_benchmark_grounding"]["status"] == "gap") or bool(benchmark_adapter),
            f"observed benchmark adapter keys = `{sorted(benchmark_adapter.keys())}`.",
        ),
        check(
            "Benchmark grounded panel is attached when external grounding reaches pass",
            (reqs["primary_external_benchmark_grounding"]["status"] != "pass") or bool(benchmark_panel),
            f"observed benchmark panel keys = `{sorted(benchmark_panel.keys())}`.",
        ),
        check(
            "Broader reviewer section keeps both family rollups at 16 items",
            (not benchmark_section)
            or (
                benchmark_section["family_rollups"]["hallucination_benchmark_section"]["num_items"] == 16
                and benchmark_section["family_rollups"]["benign_utility_benchmark_section"]["num_items"] == 16
            ),
            (
                f"observed counts = `{None if not benchmark_section else benchmark_section['family_rollups']['hallucination_benchmark_section']['num_items']}`, "
                f"`{None if not benchmark_section else benchmark_section['family_rollups']['benign_utility_benchmark_section']['num_items']}`."
            ),
        ),
        check(
            "Scale strengthening is still not yet full paper-ready pass",
            reqs["broader_benchmark_section_scale"]["status"] == "partial",
            f"observed scale status = `{reqs['broader_benchmark_section_scale']['status']}`.",
        ),
        check(
            "Synthetic reference is explicitly demoted to support-only",
            reqs["synthetic_reference_demotion"]["status"] == "pass",
            f"observed synthetic demotion status = `{reqs['synthetic_reference_demotion']['status']}`.",
        ),
        check(
            "Synthetic summary-only still shows high-N collapse in the frozen packet",
            synthetic["summary_only"]["8"]["propagation_rate"] > synthetic["tiered"]["8"]["propagation_rate"],
            f"summary/tiered N=8 propagation = `{synthetic['summary_only']['8']['propagation_rate']:.3f}`/`{synthetic['tiered']['8']['propagation_rate']:.3f}`.",
        ),
        "",
        "## Bottom Line",
        "",
        "如果这些检查通过，说明 paper baseline packet 现在冻结的是一个更强的状态：primary-base blocker 已经补掉，但 paper-ready 仍然因为 coverage scale 还不够大而暂时保留为 `False`。",
    ]

    (base_dir / VERIFY_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {base_dir / VERIFY_PATH}")


if __name__ == "__main__":
    main()
