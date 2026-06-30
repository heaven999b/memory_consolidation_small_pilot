from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_local_evidence_packet.json"
SUMMARY_PATH = "outputs/v3_local_evidence_packet.md"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_status(feasibility: dict[str, Any], name: str) -> str:
    for entry in feasibility.get("checks", []):
        if entry.get("name") == name:
            return entry.get("status", "missing")
    return "missing"


def select_rows(stats: dict[str, Any], comparison: str, n_passes: int) -> list[dict[str, Any]]:
    return [
        row
        for row in stats.get("rows", [])
        if row.get("comparison") == comparison and row.get("n_passes") == n_passes
    ]


def select_pareto_section(pareto: dict[str, Any], n_passes: int) -> dict[str, Any]:
    for section in pareto.get("sections", []):
        if section.get("n_passes") == n_passes:
            return section
    return {}


def build_payload(repo_root: Path) -> dict[str, Any]:
    feasibility = load_json(repo_root / "outputs" / "v3_feasibility_gate.json")
    readiness = load_json(repo_root / "outputs" / "v3_public_baseline_readiness.json")
    audit = load_json(repo_root / "outputs" / "v3_no_rewrite_policy_audit.json")
    comparison = load_json(repo_root / "outputs" / "v3_no_rewrite_comparison.json")
    stats = load_json(repo_root / "outputs" / "v3_no_rewrite_statistics.json")
    surface_audit = load_json(repo_root / "outputs" / "v3_no_rewrite_surface_audit.json")
    pareto = load_json(repo_root / "outputs" / "v3_no_rewrite_pareto.json")
    capability = load_json(repo_root / "outputs" / "v3_local_capability_matrix.json")

    available_n = sorted({int(row.get("n_passes", 0)) for row in stats.get("rows", [])})
    focus_n = max(available_n) if available_n else 16
    focus_rows = select_rows(stats, "Main: blind -> no-rewrite", focus_n)
    return {
        "description": "Consolidated local synthetic dry-run packet for the current V3 transition state.",
        "evidence_class": surface_audit.get("evidence_class", stats.get("evidence_class", "synthetic_dry_run")),
        "paper_safe": surface_audit.get("paper_safe", False),
        "do_not_mix_with_real_results": surface_audit.get("do_not_mix_with_real_results", True),
        "tiermem_week0_gate": check_status(feasibility, "TierMem usable"),
        "public_baseline_readiness": readiness,
        "no_rewrite_audit": audit.get("overall", {}),
        "no_rewrite_comparison_item_count": comparison.get("item_count"),
        "n_values": comparison.get("n_values", []),
        "seeds": comparison.get("seeds", []),
        "architectures": comparison.get("architectures", []),
        "focus_n": focus_n,
        "no_rewrite_focus_statistics": focus_rows,
        "fairness_focus_statistics": select_rows(stats, "Fairness: blind -> query-aware", focus_n),
        "mechanism_focus_statistics": select_rows(stats, "Mechanism: query-aware -> no-rewrite", focus_n),
        "pareto_n8": select_pareto_section(pareto, 8),
        "pareto": pareto.get("sections", []),
        "capability_counts": capability.get("counts", {}),
    }


def build_summary(payload: dict[str, Any]) -> str:
    fairness_map = {
        row["family"]: row for row in payload.get("fairness_focus_statistics", [])
    }
    mechanism_map = {
        row["family"]: row for row in payload.get("mechanism_focus_statistics", [])
    }
    main_map = {
        row["family"]: row for row in payload.get("no_rewrite_focus_statistics", [])
    }
    safety_rows_n8 = {
        row["architecture"]: row
        for row in payload.get("pareto_n8", {}).get("safety_rows", [])
    }

    lines = [
        "# V3 Local Evidence Packet",
        "",
        payload["description"],
        "",
        "## Current State",
        "",
        f"- Evidence class: `{payload.get('evidence_class', 'unknown')}`",
        f"- Paper safe: `{payload.get('paper_safe')}`",
        f"- Do-not-mix-with-real-results: `{payload.get('do_not_mix_with_real_results')}`",
        f"- TierMem week-0 gate: `{payload.get('tiermem_week0_gate', 'missing')}`",
        f"- Public baseline readiness: `{payload['public_baseline_readiness'].get('overall_status', 'missing')}`",
        f"- No-rewrite audit N=8 blocked protected rate: `{payload['no_rewrite_audit'].get('n8_blocked_protected_case_rate', 'missing')}`",
        f"- No-rewrite comparison item count: `{payload['no_rewrite_comparison_item_count']}`",
        f"- Local N sweep: `{payload.get('n_values', [])}`",
        f"- Local seeds: `{payload.get('seeds', [])}`",
        f"- Local architectures: `{payload.get('architectures', [])}`",
        f"- Capability counts: `{payload['capability_counts']}`",
        "",
        f"## Main Synthetic Statistical Readout (blind -> no-rewrite at N={payload.get('focus_n')})",
        "",
        "| Family | Left | Right | Delta | 95% CI | McNemar p |",
        "|---|---:|---:|---:|---|---:|",
    ]
    for row in payload["no_rewrite_focus_statistics"]:
        lines.append(
            f"| {row['family']} | {row['left_mean']:.3f} | {row['right_mean']:.3f} | "
            f"{row['delta']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | {row['mcnemar_p']:.6f} |"
        )
    lines.extend(
        [
            "",
            "## Mechanism Decomposition",
            "",
            (
                "- On this synthetic proxy surface, `query-aware` alone fixes the current local `conflict` collapse and restores "
                f"`benign` accuracy (`{fairness_map.get('benign', {}).get('left_mean', 0.0):.3f}` -> "
                f"`{fairness_map.get('benign', {}).get('right_mean', 0.0):.3f}` at `N={payload.get('focus_n')}`), "
                "but it does not reduce `hallucination` or `unsafe` risk in this dry-run surface."
            ),
            (
                "- On the same synthetic surface, `no-rewrite` is the part that removes the local `hallucination` and `unsafe` failures: "
                f"`hallucination` risk `{mechanism_map.get('hallucination', {}).get('left_mean', 0.0):.3f}` -> "
                f"`{mechanism_map.get('hallucination', {}).get('right_mean', 0.0):.3f}`, "
                f"`unsafe` risk `{mechanism_map.get('unsafe', {}).get('left_mean', 0.0):.3f}` -> "
                f"`{mechanism_map.get('unsafe', {}).get('right_mean', 0.0):.3f}` at `N={payload.get('focus_n')}`."
            ),
            (
                "- Relative to the blind summary baseline, `summary_only_no_rewrite` gives a smaller but still synthetic-only "
                f"significant `benign` gain (`{main_map.get('benign', {}).get('left_mean', 0.0):.3f}` -> "
                f"`{main_map.get('benign', {}).get('right_mean', 0.0):.3f}`), while fully removing the three local risk-family failures."
            ),
            "",
            "## Cost Readout",
            "",
            (
                "- At `N=8`, `summary_only_no_rewrite` reaches local safety score `"
                f"{safety_rows_n8.get('summary_only_no_rewrite', {}).get('quality', 'missing')}` at mean proxy cost `"
                f"{safety_rows_n8.get('summary_only_no_rewrite', {}).get('mean_cost', 'missing')}`, "
                f"versus `raw_only` cost `{safety_rows_n8.get('raw_only', {}).get('mean_cost', 'missing')}` "
                f"and `tiered` cost `{safety_rows_n8.get('tiered', {}).get('mean_cost', 'missing')}`."
            ),
            (
                "- At the same `N=8`, `summary_query_aware` is cheap and recall-friendly "
                f"(mean cost `{safety_rows_n8.get('summary_query_aware', {}).get('mean_cost', 'missing')}`), "
                "but it still leaves hallucination and unsafe risk untouched in this local proxy setting."
            ),
        ]
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This packet is useful for local mechanism instantiation, fairness pairing, and audit scaffolding, but it is still synthetic dry-run evidence.",
            "- The strongest safe conclusion here is narrow: in the legacy simulator, query awareness aligns with conflict/benign recovery, while the no-rewrite rule aligns with hallucination/unsafe suppression.",
            "- The decisive remaining gap is empirical: real TierMem runs, real public baselines, real benchmark data placement, and real external credentials.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-local-packet] wrote {repo_root / JSON_PATH}")
    print(f"[v3-local-packet] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
