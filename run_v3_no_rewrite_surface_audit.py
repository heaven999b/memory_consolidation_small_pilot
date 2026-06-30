from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_no_rewrite_surface_audit.json"
SUMMARY_PATH = "outputs/v3_no_rewrite_surface_audit.md"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def row_is_deterministic(row: dict[str, Any]) -> bool:
    delta = float(row.get("delta", 0.0))
    ci_low = float(row.get("ci_low", 0.0))
    ci_high = float(row.get("ci_high", 0.0))
    return ci_low == ci_high and delta in {0.0, 1.0, -1.0}


def row_is_perfect_tie(row: dict[str, Any]) -> bool:
    return (
        int(row.get("left_win", 0)) == 0
        and int(row.get("right_win", 0)) == 0
        and int(row.get("ties", 0)) == int(row.get("pair_count", 0))
    )


def build_payload(repo_root: Path) -> dict[str, Any]:
    comparison = load_json(repo_root / "outputs" / "v3_no_rewrite_comparison.json")
    statistics = load_json(repo_root / "outputs" / "v3_no_rewrite_statistics.json")

    rows = statistics.get("rows", [])
    deterministic_rows = [row for row in rows if row_is_deterministic(row)]
    perfect_tie_rows = [row for row in rows if row_is_perfect_tie(row)]
    stats_n_values = sorted({int(row.get("n_passes", 0)) for row in rows})

    tie_focus = [
        row
        for row in perfect_tie_rows
        if row.get("comparison") == "Fairness: blind -> query-aware"
    ]
    deterministic_focus = [
        row
        for row in deterministic_rows
        if row.get("comparison") in {"Mechanism: query-aware -> no-rewrite", "Main: blind -> no-rewrite"}
    ]

    return {
        "description": "Audit of the synthetic no-rewrite surface, focused on evidence class, N coverage, deterministic rows, and tie-heavy slices.",
        "evidence_class": statistics.get("evidence_class", comparison.get("evidence_class", "synthetic_dry_run")),
        "surface_runtime": statistics.get("surface_runtime", comparison.get("surface_runtime", "legacy_compaction_simulator")),
        "paper_safe": False,
        "do_not_mix_with_real_results": True,
        "comparison_n_values": comparison.get("n_values", []),
        "statistics_n_values": stats_n_values,
        "row_count": len(rows),
        "deterministic_row_count": len(deterministic_rows),
        "perfect_tie_row_count": len(perfect_tie_rows),
        "deterministic_rows": deterministic_rows,
        "perfect_tie_rows": perfect_tie_rows,
        "tie_focus_rows": tie_focus,
        "deterministic_focus_rows": deterministic_focus,
        "overall_conclusion": (
            "This surface is a synthetic dry-run over a legacy simulator. It is useful for mechanism instantiation and audit, "
            "but it is not real-model evidence and should not appear in the same result layer as TierMem or official public-baseline tables."
        ),
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 No-Rewrite Surface Audit",
        "",
        payload["description"],
        "",
        f"- evidence class: `{payload.get('evidence_class', 'unknown')}`",
        f"- runtime: `{payload.get('surface_runtime', 'unknown')}`",
        f"- paper safe: `{payload.get('paper_safe')}`",
        f"- do_not_mix_with_real_results: `{payload.get('do_not_mix_with_real_results')}`",
        f"- comparison depths: `{payload.get('comparison_n_values', [])}`",
        f"- statistics depths: `{payload.get('statistics_n_values', [])}`",
        f"- statistics rows: `{payload.get('row_count', 0)}`",
        f"- deterministic rows: `{payload.get('deterministic_row_count', 0)}`",
        f"- perfect tie rows: `{payload.get('perfect_tie_row_count', 0)}`",
        "",
        "## Deterministic Warning",
        "",
        "- Exact `0.000` / `+/-1.000` deltas with zero-width confidence intervals are present on this surface.",
        "- That pattern is consistent with rule-constrained or by-construction dry-run behavior, not with ordinary stochastic LLM output.",
        "",
        "## Tie Warning",
        "",
        "- Some blind-vs-query-aware rows are perfect ties across all paired items.",
        "- That means those family metrics are not expressing useful sensitivity on this surface and should be treated as proxy diagnostics only.",
        "",
        "## Focus Rows",
        "",
        "| Comparison | Family | N | Delta | 95% CI | Left-win | Right-win | Ties |",
        "|---|---|---:|---:|---|---:|---:|---:|",
    ]
    seen: set[tuple[str, str, int]] = set()
    for row in payload.get("tie_focus_rows", []) + payload.get("deterministic_focus_rows", []):
        key = (str(row.get("comparison")), str(row.get("family")), int(row.get("n_passes", 0)))
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            f"| {row.get('comparison')} | {row.get('family')} | {row.get('n_passes')} | {float(row.get('delta', 0.0)):.3f} | "
            f"[{float(row.get('ci_low', 0.0)):.3f}, {float(row.get('ci_high', 0.0)):.3f}] | "
            f"{row.get('left_win', 0)} | {row.get('right_win', 0)} | {row.get('ties', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            payload["overall_conclusion"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload), encoding="utf-8")
    print(f"[v3-no-rewrite-surface-audit] wrote {repo_root / JSON_PATH}")
    print(f"[v3-no-rewrite-surface-audit] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
