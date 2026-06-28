from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ADAPTER_RESULTS = "outputs/external_benchmark_adapter_layer.json"
MINIMAL_RESULTS = "outputs/external_benchmark_minimal_baseline.json"
REVIEWER_SECTION_RESULTS = "outputs/external_benchmark_reviewer_section.json"
PRIMARY_SURFACE_RESULTS = "outputs/tiermem_style_primary_surface.json"
REINTEGRATION_RESULTS = "outputs/actual_hallucination_claim_reintegration_pilot_results.json"

ENTRYPOINT_PATH = "run_benchmark_first_primary_entrypoint.py"
JSON_PATH = "outputs/benchmark_first_proxy_base.json"
SUMMARY_PATH = "outputs/benchmark_first_proxy_base.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_payload(
    *,
    adapter: dict[str, Any],
    minimal: dict[str, Any],
    reviewer_section: dict[str, Any],
    primary_surface: dict[str, Any],
    reintegration: dict[str, Any],
    base_dir: Path,
) -> dict[str, Any]:
    adapter_pass = adapter.get("grounding_status") == "pass"
    minimal_ready = minimal.get("verdict", {}).get("minimal_benchmark_grounded_panel_ready") is True
    reviewer_ready = reviewer_section.get("verdict", {}).get("benchmark_reviewer_section_ready") is True

    primary_status = primary_surface.get("primary_surface_status", {})
    benchmark_first_ready = primary_status.get("benchmark_first_surface_ready") is True
    primary_base_status = primary_status.get("tiermem_style_primary_base_status", "gap")
    primary_ready = primary_base_status in {"partial", "pass"}
    proxy_complete_in_surface = primary_status.get("benchmark_first_proxy_base_complete") is True
    native_primary_ready = primary_status.get("benchmark_native_primary_base_ready") is True

    exact_proxy_rows = reintegration.get("proxy_counts", {}).get("mode_equivalent_proxy", 0)
    exact_frontier_ready = (
        reintegration.get("mode") == "exact_stress_closure_reintegration" and exact_proxy_rows == 0
    )

    entrypoint_exists = (base_dir / ENTRYPOINT_PATH).exists()
    entrypoint_ready = entrypoint_exists and benchmark_first_ready and reviewer_ready

    proxy_base_ready = all(
        [
            adapter_pass,
            minimal_ready,
            reviewer_ready,
            benchmark_first_ready,
            primary_ready,
            proxy_complete_in_surface,
            exact_frontier_ready,
            entrypoint_ready,
        ]
    )
    proxy_base_status = "pass" if proxy_base_ready else "partial"

    return {
        "description": "Frozen benchmark-first proxy base that turns the current reviewer-facing benchmark stack into one end-to-end proxy baseline artifact.",
        "verdict": {
            "benchmark_first_proxy_base_ready": proxy_base_ready,
            "benchmark_first_proxy_base_status": proxy_base_status,
            "full_tiermem_native_grounding": False,
            "note": (
                "The local benchmark-first proxy base is now complete and remains frozen as a support layer: adapter grounding, minimal external panel, broader reviewer section, benchmark-first primary surface, and exact non-proxy frontier closure are all still explicit, even though the main blocker has now moved up to a benchmark-native primary base."
                if proxy_base_ready and native_primary_ready
                else "The local benchmark-first proxy base is now complete: adapter grounding, minimal external panel, broader reviewer section, benchmark-first primary surface, and exact non-proxy frontier closure are all frozen together, but the implementation underneath is still not TierMem-native."
                if proxy_base_ready
                else "The repo has moved toward a benchmark-first proxy base, but some parts of the end-to-end proxy chain are still missing."
            ),
        },
        "component_status": {
            "external_benchmark_adapter": {
                "grounding_status": adapter.get("grounding_status"),
                "adapter_ready_count": adapter.get("adapter_ready_count"),
                "slice_ready_count": adapter.get("slice_ready_count"),
            },
            "external_benchmark_minimal_panel": {
                "ready": minimal_ready,
                "panel_names": sorted((minimal.get("benchmark_panels") or {}).keys()),
                "seeds": minimal.get("seeds", []),
            },
            "external_benchmark_reviewer_section": {
                "ready": reviewer_ready,
                "family_rollups": sorted((reviewer_section.get("family_rollups") or {}).keys()),
                "slice_panels": sorted((reviewer_section.get("slice_panels") or {}).keys()),
                "seeds": reviewer_section.get("seeds", []),
            },
            "benchmark_first_entrypoint": {
                "path": ENTRYPOINT_PATH,
                "exists": entrypoint_exists,
                "ready": entrypoint_ready,
            },
            "primary_surface": {
                "benchmark_first_surface_ready": benchmark_first_ready,
                "tiermem_style_primary_base_status": primary_base_status,
                "benchmark_source_kind": primary_status.get("benchmark_source_kind"),
                "benchmark_first_proxy_base_complete": proxy_complete_in_surface,
                "benchmark_native_primary_base_ready": native_primary_ready,
            },
            "frontier_closure": {
                "mode": reintegration.get("mode"),
                "proxy_rows": exact_proxy_rows,
                "total_rows": len(reintegration.get("records", [])),
                "exact_non_proxy_frontier_ready": exact_frontier_ready,
            },
        },
        "reviewer_sequence": [
            "Start from the broader reviewer-facing benchmark section rather than the synthetic trio.",
            "Treat the benchmark-first primary surface as the local proxy presentation layer that now feeds into the native primary base."
            if native_primary_ready
            else "Treat the benchmark-first primary surface as the main local proxy presentation layer.",
            "Use the exact non-proxy frontier closure as evidence that the current stress frontier is no longer held together by proxy rows.",
        ],
        "remaining_gaps": [
            "Expand the broader benchmark reviewer section into more slice families and larger frozen coverage once the current proxy base stays stable."
            if native_primary_ready
            else "Replace the remaining local proxy-stack internals with a TierMem-native benchmark implementation so the primary-base status can move from partial to pass.",
            "Reduce how much reviewer-facing interpretation still depends on synthetic-reference support artifacts.",
        ],
    }


def build_summary(payload: dict[str, Any]) -> str:
    verdict = payload["verdict"]
    components = payload["component_status"]
    lines = [
        "# Benchmark-First Proxy Base",
        "",
        "这个 artifact 冻结的不是 TierMem-native 主实现，而是我们当前已经补齐的 benchmark-first proxy base：adapter、minimal benchmark panel、broader reviewer section、primary surface 和 exact frontier closure 现在被收束到同一份工件里。",
        "",
        "## Verdict",
        "",
        f"- benchmark-first proxy base ready: `{verdict['benchmark_first_proxy_base_ready']}`",
        f"- benchmark-first proxy base status: `{verdict['benchmark_first_proxy_base_status']}`",
        f"- full TierMem-native grounding: `{verdict['full_tiermem_native_grounding']}`",
        f"- note: {verdict['note']}",
        "",
        "## Component Status",
        "",
        f"- external benchmark adapter: grounding `{components['external_benchmark_adapter']['grounding_status']}`, slice-ready `{components['external_benchmark_adapter']['slice_ready_count']}/{components['external_benchmark_adapter']['adapter_ready_count']}`",
        f"- minimal benchmark panel: ready `{components['external_benchmark_minimal_panel']['ready']}`, panels `{components['external_benchmark_minimal_panel']['panel_names']}`",
        f"- broader reviewer section: ready `{components['external_benchmark_reviewer_section']['ready']}`, families `{components['external_benchmark_reviewer_section']['family_rollups']}`",
        f"- benchmark-first entrypoint: `{components['benchmark_first_entrypoint']['path']}`, ready `{components['benchmark_first_entrypoint']['ready']}`",
        f"- primary surface: status `{components['primary_surface']['tiermem_style_primary_base_status']}`, proxy-complete `{components['primary_surface']['benchmark_first_proxy_base_complete']}`",
        f"- frontier closure: mode `{components['frontier_closure']['mode']}`, proxy rows `{components['frontier_closure']['proxy_rows']}/{components['frontier_closure']['total_rows']}`",
        "",
        "## What This Means",
        "",
        "- 现在 reviewer-facing 主链路已经不只是“有几个 benchmark artifact”，而是可以被当作一套完整的本地 proxy baseline 来讲述和核对。",
        "- 这套基线已经 benchmark-first，而且 exact frontier closure 也已经去掉 proxy rows，所以 remaining gap 不再是“proxy 没做完”，而是“实现仍不是 TierMem-native”。",
        "",
        "## Remaining Gaps",
        "",
    ]
    for gap in payload["remaining_gaps"]:
        lines.append(f"- {gap}")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    adapter = load_json(base_dir / ADAPTER_RESULTS)
    minimal = load_json(base_dir / MINIMAL_RESULTS)
    reviewer_section = load_json(base_dir / REVIEWER_SECTION_RESULTS)
    primary_surface = load_json(base_dir / PRIMARY_SURFACE_RESULTS)
    reintegration = load_json(base_dir / REINTEGRATION_RESULTS)

    payload = build_payload(
        adapter=adapter,
        minimal=minimal,
        reviewer_section=reviewer_section,
        primary_surface=primary_surface,
        reintegration=reintegration,
        base_dir=base_dir,
    )
    (base_dir / JSON_PATH).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (base_dir / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"Wrote {base_dir / JSON_PATH}")
    print(f"Wrote {base_dir / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
