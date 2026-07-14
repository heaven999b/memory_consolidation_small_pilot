#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"
DEFAULT_WEEK1_ROOT = DEFAULT_OUTPUT_DIR / "week1_sanity_live_20260702"
DEFAULT_WEEK1_LINKED_VIEW = DEFAULT_WEEK1_ROOT / "tiny_synth" / "linked_view"
DEFAULT_WEEK1_PAGE_STORE = DEFAULT_WEEK1_ROOT / "page_store"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a local-only mini panel that aligns the closed-loop memory "
            "baseline trio, model-backed sanity slices, benchmark-grounded "
            "family rollups, and simple page-store occupancy proxies."
        )
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Base outputs directory under memory_consolidation_small_pilot.",
    )
    parser.add_argument(
        "--week1-root",
        default=str(DEFAULT_WEEK1_ROOT),
        help="Root directory for the week1 live sanity runs.",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Optional explicit JSON output path.",
    )
    parser.add_argument(
        "--md-out",
        default=None,
        help="Optional explicit Markdown output path.",
    )
    return parser


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _safe_round(value: float | int | None, digits: int = 3) -> float | int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    return round(value, digits)


def _pct(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _direction_for_architecture(architecture: str) -> str:
    mapping = {
        "raw_only": "raw_control",
        "summary_only": "compression_only",
        "summary_plus_raw": "hierarchical_reopen",
        "tiered": "hierarchical_reopen",
        "scale_aware_unified": "policy_gated_reopen",
        "scale_aware_note_aware": "policy_gated_reopen",
        "psu_no_carry": "policy_scaffold_ablation",
        "psu": "provenance_scaffolded_policy",
    }
    return mapping.get(architecture, architecture)


def _display_name(architecture: str) -> str:
    mapping = {
        "summary_plus_raw": "tiered_week1",
        "scale_aware_unified": "scale-aware unified",
        "scale_aware_note_aware": "scale-aware note-aware",
        "psu_no_carry": "psu (no carry)",
    }
    return mapping.get(architecture, architecture)


def _collect_week1_smoke(week1_root: Path) -> list[dict[str, Any]]:
    linked_view_dir = week1_root / "tiny_synth" / "linked_view"
    page_store_dir = week1_root / "page_store"
    rows: list[dict[str, Any]] = []
    if not linked_view_dir.exists():
        return rows

    for run_dir in sorted(linked_view_dir.iterdir()):
        if not run_dir.is_dir():
            continue
        summary_path = run_dir / "summary.json"
        if not summary_path.exists():
            continue
        summary = _load_json(summary_path)
        config = summary.get("config", {})
        cost_summary = summary.get("cost_summary", {})
        qa_phase = cost_summary.get("qa_phase", {})
        page_dir = page_store_dir / run_dir.name
        occupancy = _page_store_occupancy(page_dir)
        route_counts = _route_counts_for_run(run_dir)

        architecture = str(config.get("architecture") or "unknown")
        n_passes = int(config.get("consolidation_passes") or 0)

        rows.append(
            {
                "run_id": run_dir.name,
                "source": "week1_live_smoke",
                "benchmark": summary.get("benchmark"),
                "architecture": architecture,
                "display_architecture": _display_name(architecture),
                "direction": _direction_for_architecture(architecture),
                "n": n_passes,
                "num_samples": int(summary.get("num_qa_logs") or 0),
                "mean_exact_match_reference": _safe_round(_mean_exact_match(run_dir), 3),
                "summary_f1": _safe_round((summary.get("metrics") or {}).get("f1"), 3),
                "summary_bleu1": _safe_round((summary.get("metrics") or {}).get("bleu1"), 3),
                "avg_online_tokens_in": _safe_round(qa_phase.get("avg_tokens_in_per_qa"), 1),
                "avg_online_tokens_out": _safe_round(qa_phase.get("avg_tokens_out_per_qa"), 1),
                "avg_online_latency_ms": _safe_round(qa_phase.get("avg_latency_per_qa_ms"), 1),
                "route_counts": route_counts,
                "raw_route_rate": _safe_round(_pct(route_counts.get("R", 0), max(sum(route_counts.values()), 1)), 3),
                "page_store_bytes": occupancy["page_store_bytes"],
                "page_store_files": occupancy["page_store_files"],
                "page_count": occupancy["page_count"],
                "summary_chars": occupancy["summary_chars"],
                "content_chars": occupancy["content_chars"],
                "memory_items": occupancy["memory_items"],
                "summary_to_content_char_ratio": _safe_round(
                    _pct(occupancy["summary_chars"], max(occupancy["content_chars"], 1)),
                    3,
                ),
            }
        )

    rows.sort(key=lambda row: (row["architecture"], row["n"]))
    return rows


def _route_counts_for_run(run_dir: Path) -> dict[str, int]:
    route_counts: Counter[str] = Counter()
    sessions_dir = run_dir / "sessions"
    for qa_path in sorted(sessions_dir.glob("*_qa.jsonl")):
        for row in _load_jsonl(qa_path):
            route = ((row.get("mechanism_trace") or {}).get("route") or "UNKNOWN")
            route_counts[str(route)] += 1
    return dict(route_counts)


def _mean_exact_match(run_dir: Path) -> float | None:
    scores: list[float] = []
    sessions_dir = run_dir / "sessions"
    for qa_path in sorted(sessions_dir.glob("*_qa.jsonl")):
        for row in _load_jsonl(qa_path):
            score = row.get("score")
            if score is None:
                continue
            scores.append(float(score))
    if not scores:
        return None
    return sum(scores) / len(scores)


def _page_store_occupancy(page_dir: Path) -> dict[str, int]:
    result = {
        "page_store_bytes": 0,
        "page_store_files": 0,
        "page_count": 0,
        "summary_chars": 0,
        "content_chars": 0,
        "memory_items": 0,
    }
    if not page_dir.exists():
        return result

    for path in sorted(page_dir.glob("*.json")):
        result["page_store_files"] += 1
        result["page_store_bytes"] += path.stat().st_size
        payload = _load_json(path)
        pages = []
        current_page = payload.get("current_page")
        if isinstance(current_page, dict):
            pages.append(current_page)
        pages.extend(payload.get("completed_pages") or [])
        result["page_count"] += len(pages)
        for page in pages:
            result["summary_chars"] += len(page.get("summary") or "")
            result["content_chars"] += len(page.get("content") or "")
            result["memory_items"] += len(page.get("memories") or [])
    return result


def _collect_synthetic_core(packet: dict[str, Any]) -> list[dict[str, Any]]:
    panel = packet["synthetic_core_panel"]
    rows: list[dict[str, Any]] = []
    for architecture in panel["baseline_methods"]:
        snapshots = panel["snapshots"][architecture]
        for n_key in sorted(snapshots, key=lambda value: int(value)):
            snap = snapshots[n_key]
            rows.append(
                {
                    "source": "synthetic_control_trio",
                    "architecture": architecture,
                    "display_architecture": _display_name(architecture),
                    "direction": _direction_for_architecture(architecture),
                    "n": int(n_key),
                    "accuracy": _safe_round(snap.get("accuracy")),
                    "propagation_rate": _safe_round(snap.get("propagation_rate")),
                    "residual_bad_memory_rate": _safe_round(snap.get("residual_bad_memory_rate")),
                    "raw_escalation_rate": _safe_round(snap.get("raw_escalation_rate")),
                    "mean_cost": _safe_round(snap.get("mean_cost")),
                }
            )
    return rows


def _collect_model_backed_sanity(packet: dict[str, Any], focus_n: int = 8) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for panel_name, panel in packet["model_backed_sanity"].items():
        rows: list[dict[str, Any]] = []
        for architecture in panel["architectures"]:
            snapshots = panel["snapshots"][architecture]
            if str(focus_n) not in snapshots:
                continue
            snap = snapshots[str(focus_n)]
            row = {
                "source": panel_name,
                "architecture": architecture,
                "display_architecture": _display_name(architecture),
                "direction": _direction_for_architecture(architecture),
                "n": focus_n,
                "accuracy": _safe_round(snap.get("accuracy")),
                "propagation_rate": _safe_round(snap.get("propagation_rate")),
                "residual_bad_memory_rate": _safe_round(snap.get("residual_bad_memory_rate")),
                "raw_escalation_rate": _safe_round(snap.get("raw_escalation_rate")),
                "mean_llm_cost_usd": _safe_round(snap.get("mean_llm_cost_usd"), 6),
            }
            if "history_loss_rate" in snap:
                row["history_loss_rate"] = _safe_round(snap.get("history_loss_rate"))
            if "false_present_rate" in snap:
                row["false_present_rate"] = _safe_round(snap.get("false_present_rate"))
            rows.append(row)
        result[panel_name] = rows
    return result


def _collect_benchmark_rollups(stage_large: dict[str, Any], focus_n: int = 8) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for family_name in ["benign_utility_expanded_pool", "hallucination_expanded_pool"]:
        family = stage_large["family_rollups"][family_name]
        rows: list[dict[str, Any]] = []
        for architecture in family["snapshots"]:
            snapshots = family["snapshots"][architecture]
            if str(focus_n) not in snapshots:
                continue
            snap = snapshots[str(focus_n)]
            row = {
                "source": family_name,
                "architecture": architecture,
                "display_architecture": _display_name(architecture),
                "direction": _direction_for_architecture(architecture),
                "n": focus_n,
                "count": int(snap.get("count") or 0),
                "accuracy": _safe_round(snap.get("accuracy")),
                "propagation_rate": _safe_round(snap.get("propagation_rate")),
                "residual_bad_memory_rate": _safe_round(snap.get("residual_bad_memory_rate")),
                "raw_escalation_rate": _safe_round(snap.get("raw_escalation_rate")),
                "mean_cost": _safe_round(snap.get("mean_cost")),
                "mean_llm_cost_usd": _safe_round(snap.get("mean_llm_cost_usd"), 6),
            }
            if "history_loss_rate" in snap:
                row["history_loss_rate"] = _safe_round(snap.get("history_loss_rate"))
            if "false_present_rate" in snap:
                row["false_present_rate"] = _safe_round(snap.get("false_present_rate"))
            rows.append(row)
        rows.sort(key=lambda row: row["display_architecture"])
        result[family_name] = rows
    return result


def _collect_psu_recall(psu_panel: dict[str, Any], focus_n: int = 8) -> list[dict[str, Any]]:
    rows = list(psu_panel["panel_rows"].get(str(focus_n), []))
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized.append(
            {
                "source": "psu_recall_main_panel",
                "architecture": row["label"],
                "display_architecture": _display_name(row["label"]),
                "direction": _direction_for_architecture(row["label"]),
                "n": int(row["n_passes"]),
                "count": int(row["count"]),
                "accuracy": _safe_round(row.get("accuracy")),
                "propagation_rate": _safe_round(row.get("propagation")),
                "history_loss_rate": _safe_round(row.get("history_loss")),
                "raw_escalation_rate": _safe_round(row.get("raw_escalation")),
                "unsafe_error_rate": _safe_round(row.get("unsafe_error")),
                "mean_llm_cost_usd": _safe_round(row.get("mean_llm_cost_usd"), 6),
            }
        )
    return normalized


def _collect_cost_pareto(cost_pareto: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for section in cost_pareto["sections"]:
        title = str(section["title"])
        quality_label = str(section["quality_label"])
        for row in section["rows"]:
            rows.append(
                {
                    "section_title": title,
                    "quality_label": quality_label,
                    "architecture": row["architecture"],
                    "display_architecture": _display_name(row["architecture"]),
                    "direction": _direction_for_architecture(row["architecture"]),
                    "quality": _safe_round(row.get("quality")),
                    "mean_cost": _safe_round(row.get("mean_cost")),
                    "mean_llm_cost_usd": _safe_round(row.get("mean_llm_cost_usd"), 6),
                    "raw_escalation_rate": _safe_round(row.get("raw_escalation_rate")),
                }
            )
    return rows


def _derive_signal_board(
    week1_smoke: list[dict[str, Any]],
    benchmark_rollups: dict[str, list[dict[str, Any]]],
    psu_rows: list[dict[str, Any]],
) -> list[str]:
    signals: list[str] = []

    smoke_by_key = {(row["architecture"], row["n"]): row for row in week1_smoke}
    raw_n0 = smoke_by_key.get(("raw_only", 0))
    summary_n0 = smoke_by_key.get(("summary_only", 0))
    tiered_n1 = smoke_by_key.get(("summary_plus_raw", 1))
    summary_n1 = smoke_by_key.get(("summary_only", 1))

    if raw_n0 and summary_n0:
        token_ratio = _pct(
            float(summary_n0["avg_online_tokens_in"]),
            float(raw_n0["avg_online_tokens_in"]),
        )
        signals.append(
            "Compression-only has a real efficiency signal on the live smoke slice: "
            f"`summary_only@N=0` uses {summary_n0['avg_online_tokens_in']} avg input tokens "
            f"vs `{raw_n0['avg_online_tokens_in']}` for `raw_only@N=0` "
            f"({round((token_ratio or 0.0) * 100, 1)}%), but exact-match drops from "
            f"{raw_n0['mean_exact_match_reference']} to {summary_n0['mean_exact_match_reference']}."
        )

    if tiered_n1 and summary_n1:
        signals.append(
            "Hierarchical reopen shows a modest recovery signal on the same live slice: "
            f"`tiered_week1@N=1` reaches exact-match {tiered_n1['mean_exact_match_reference']} "
            f"vs `{summary_n1['mean_exact_match_reference']}` for `summary_only@N=1`, "
            f"with raw reopen rate {tiered_n1['raw_route_rate']}."
        )

    benign_rows = {row["architecture"]: row for row in benchmark_rollups["benign_utility_expanded_pool"]}
    halluc_rows = {row["architecture"]: row for row in benchmark_rollups["hallucination_expanded_pool"]}
    if "summary_only" in benign_rows and "tiered" in benign_rows:
        signals.append(
            "On the expanded benign-utility pool at `N=8`, plain reopening is not optional for utility: "
            f"`summary_only` accuracy is {benign_rows['summary_only']['accuracy']}, "
            f"while `tiered` reaches {benign_rows['tiered']['accuracy']}."
        )
    if "tiered" in halluc_rows and "scale_aware_note_aware" in halluc_rows:
        signals.append(
            "Ungated reopening looks unsafe on the hallucination pool: "
            f"`tiered` has false-present rate {halluc_rows['tiered'].get('false_present_rate')} "
            f"at raw escalation {halluc_rows['tiered']['raw_escalation_rate']}, while "
            "`scale_aware_note_aware` cuts false-present to "
            f"{halluc_rows['scale_aware_note_aware'].get('false_present_rate')}."
        )
    if "psu" in benign_rows and "psu" in halluc_rows:
        signals.append(
            "The strongest current local signal is the provenance/policy line: "
            f"`psu@N=8` keeps benign accuracy at {benign_rows['psu']['accuracy']} with "
            f"history-loss {benign_rows['psu'].get('history_loss_rate')} and raw escalation "
            f"{benign_rows['psu']['raw_escalation_rate']}, while also keeping hallucination "
            f"false-present at {halluc_rows['psu'].get('false_present_rate')}."
        )

    if psu_rows:
        best_psu = next((row for row in psu_rows if row["architecture"] == "psu"), None)
        note_aware = next((row for row in psu_rows if row["architecture"] == "scale_aware_note_aware"), None)
        if best_psu and note_aware:
            signals.append(
                "Within the recall-heavy panel, `psu` improves over `scale_aware_note_aware` at the same `N=8`: "
                f"accuracy {best_psu['accuracy']} vs {note_aware['accuracy']}, "
                f"history-loss {best_psu['history_loss_rate']} vs {note_aware['history_loss_rate']}, "
                f"raw escalation {best_psu['raw_escalation_rate']} vs {note_aware['raw_escalation_rate']}."
            )

    return signals


def _render_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> list[str]:
    if not rows:
        return ["_No rows._"]
    headers = [label for _, label in columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for key, _ in columns:
            value = row.get(key, "")
            if isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False, sort_keys=True)
            values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def _render_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Memory Architecture Mini Panel",
        "",
        "- source: local frozen artifacts only",
        "- note: no fresh external API rerun in this packet",
        f"- generated_at_utc: `{payload['generated_at_utc']}`",
        "",
        "## Closed-loop Live Smoke",
        "",
    ]
    lines.extend(
        _render_table(
            payload["closed_loop_live_smoke"],
            [
                ("display_architecture", "architecture"),
                ("direction", "direction"),
                ("n", "N"),
                ("mean_exact_match_reference", "exact_match"),
                ("summary_f1", "f1"),
                ("avg_online_tokens_in", "avg_tokens_in"),
                ("avg_online_latency_ms", "avg_latency_ms"),
                ("raw_route_rate", "raw_route_rate"),
                ("page_store_bytes", "page_store_bytes"),
                ("summary_chars", "summary_chars"),
                ("content_chars", "content_chars"),
                ("memory_items", "memory_items"),
            ],
        )
    )

    lines.extend(["", "## Synthetic Control Trio", ""])
    lines.extend(
        _render_table(
            payload["synthetic_control_trio"],
            [
                ("display_architecture", "architecture"),
                ("direction", "direction"),
                ("n", "N"),
                ("accuracy", "accuracy"),
                ("propagation_rate", "propagation"),
                ("residual_bad_memory_rate", "residual_bad_memory"),
                ("raw_escalation_rate", "raw_escalation"),
                ("mean_cost", "mean_cost"),
            ],
        )
    )

    for panel_name, rows in payload["model_backed_sanity"].items():
        lines.extend(["", f"## Model-backed Sanity: {panel_name}", ""])
        columns = [
            ("display_architecture", "architecture"),
            ("direction", "direction"),
            ("n", "N"),
            ("accuracy", "accuracy"),
            ("propagation_rate", "propagation"),
            ("residual_bad_memory_rate", "residual_bad_memory"),
            ("raw_escalation_rate", "raw_escalation"),
            ("mean_llm_cost_usd", "mean_llm_cost_usd"),
        ]
        if any("history_loss_rate" in row for row in rows):
            columns.insert(6, ("history_loss_rate", "history_loss"))
        if any("false_present_rate" in row for row in rows):
            columns.insert(6, ("false_present_rate", "false_present"))
        lines.extend(_render_table(rows, columns))

    for family_name, rows in payload["benchmark_grounded_rollups"].items():
        lines.extend(["", f"## Benchmark-grounded Rollup: {family_name}", ""])
        columns = [
            ("display_architecture", "architecture"),
            ("direction", "direction"),
            ("n", "N"),
            ("accuracy", "accuracy"),
            ("propagation_rate", "propagation"),
            ("residual_bad_memory_rate", "residual_bad_memory"),
            ("raw_escalation_rate", "raw_escalation"),
            ("mean_cost", "mean_cost"),
            ("mean_llm_cost_usd", "mean_llm_cost_usd"),
        ]
        if any("history_loss_rate" in row for row in rows):
            columns.insert(6, ("history_loss_rate", "history_loss"))
        if any("false_present_rate" in row for row in rows):
            columns.insert(6, ("false_present_rate", "false_present"))
        lines.extend(_render_table(rows, columns))

    lines.extend(["", "## PSU Recall Panel", ""])
    lines.extend(
        _render_table(
            payload["psu_recall_panel"],
            [
                ("display_architecture", "architecture"),
                ("direction", "direction"),
                ("n", "N"),
                ("accuracy", "accuracy"),
                ("propagation_rate", "propagation"),
                ("history_loss_rate", "history_loss"),
                ("raw_escalation_rate", "raw_escalation"),
                ("unsafe_error_rate", "unsafe_error"),
                ("mean_llm_cost_usd", "mean_llm_cost_usd"),
            ],
        )
    )

    lines.extend(["", "## Cost Pareto Snapshot", ""])
    lines.extend(
        _render_table(
            payload["cost_pareto"],
            [
                ("section_title", "section"),
                ("display_architecture", "architecture"),
                ("direction", "direction"),
                ("quality", "quality"),
                ("mean_cost", "mean_cost"),
                ("mean_llm_cost_usd", "mean_llm_cost_usd"),
                ("raw_escalation_rate", "raw_escalation"),
            ],
        )
    )

    lines.extend(["", "## Signal Board", ""])
    for signal in payload["signal_board"]:
        lines.append(f"- {signal}")

    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- This packet aggregates existing local artifacts; it does not add a fresh benchmark rerun.",
            "- Occupancy proxies currently come from the week1 live smoke runs where page-store JSON is directly available.",
            "- The strongest policy result (`psu`) is still a local frozen panel and should be treated as a positive signal, not final closure.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = _build_parser().parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    week1_root = Path(args.week1_root).expanduser().resolve()

    packet = _load_json(output_dir / "paper_baseline_packet.json")
    stage_large = _load_json(output_dir / "expanded_benchmark_stage_large.json")
    cost_pareto = _load_json(output_dir / "expanded_benchmark_stage_main_cost_pareto.json")
    psu_panel = _load_json(output_dir / "psu_recall_main_panel.json")

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "closed_loop_live_smoke": _collect_week1_smoke(week1_root),
        "synthetic_control_trio": _collect_synthetic_core(packet),
        "model_backed_sanity": _collect_model_backed_sanity(packet, focus_n=8),
        "benchmark_grounded_rollups": _collect_benchmark_rollups(stage_large, focus_n=8),
        "psu_recall_panel": _collect_psu_recall(psu_panel, focus_n=8),
        "cost_pareto": _collect_cost_pareto(cost_pareto),
    }
    payload["signal_board"] = _derive_signal_board(
        payload["closed_loop_live_smoke"],
        payload["benchmark_grounded_rollups"],
        payload["psu_recall_panel"],
    )

    json_out = Path(args.json_out).expanduser().resolve() if args.json_out else output_dir / "memory_architecture_minipanel.json"
    md_out = Path(args.md_out).expanduser().resolve() if args.md_out else output_dir / "memory_architecture_minipanel.md"

    json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_out.write_text(_render_markdown(payload), encoding="utf-8")

    print(f"Wrote {json_out}")
    print(f"Wrote {md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
