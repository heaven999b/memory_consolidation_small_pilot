from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_STAGE = "large"
DEFAULT_TARGET_ARCHITECTURE = "psu"
DEFAULT_BASE_ARCHITECTURES = ["scale_aware_unified", "scale_aware_note_aware"]
DEFAULT_TARGET_N = 8
DEFAULT_MAX_CASES = 5

JSON_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}.json"
OUTPUT_JSON_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}_error_analysis.json"
OUTPUT_MD_TEMPLATE = "outputs/expanded_benchmark_stage_{stage}_error_analysis.md"


def selected_stage() -> str:
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        return sys.argv[1].strip().lower()
    return os.environ.get("EXPANDED_BENCHMARK_ERROR_ANALYSIS_STAGE", DEFAULT_STAGE).strip().lower()


def selected_target_architecture() -> str:
    return os.environ.get("EXPANDED_BENCHMARK_ERROR_ANALYSIS_TARGET", DEFAULT_TARGET_ARCHITECTURE).strip()


def selected_base_architectures() -> list[str]:
    env_value = os.environ.get("EXPANDED_BENCHMARK_ERROR_ANALYSIS_BASES", "").strip()
    if not env_value:
        return list(DEFAULT_BASE_ARCHITECTURES)
    return [part.strip() for part in env_value.split(",") if part.strip()]


def selected_target_n() -> int:
    return int(os.environ.get("EXPANDED_BENCHMARK_ERROR_ANALYSIS_N", str(DEFAULT_TARGET_N)).strip())


def selected_max_cases() -> int:
    return int(os.environ.get("EXPANDED_BENCHMARK_ERROR_ANALYSIS_MAX_CASES", str(DEFAULT_MAX_CASES)).strip())


def load_payload(stage: str) -> dict[str, Any]:
    base_dir = Path(__file__).resolve().parent
    path = base_dir / JSON_TEMPLATE.format(stage=stage)
    if not path.exists():
        raise RuntimeError(f"Missing expanded benchmark artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def is_history_loss(record: dict[str, Any]) -> bool:
    return record.get("compact_answer") == "ABSTAIN"


def is_false_present(record: dict[str, Any]) -> bool:
    return bool(record.get("raw_escalated"))


def family_focus_error(record: dict[str, Any], family_kind: str) -> bool:
    if family_kind == "benign":
        return is_history_loss(record)
    if family_kind == "hallucination":
        return is_false_present(record)
    raise RuntimeError(f"Unknown family kind: {family_kind}")


def family_focus_label(family_kind: str) -> str:
    if family_kind == "benign":
        return "history_loss"
    if family_kind == "hallucination":
        return "false_present"
    raise RuntimeError(f"Unknown family kind: {family_kind}")


def classify_delta(
    base_record: dict[str, Any],
    target_record: dict[str, Any],
    family_kind: str,
) -> tuple[str, dict[str, int]]:
    base_focus = int(family_focus_error(base_record, family_kind))
    target_focus = int(family_focus_error(target_record, family_kind))
    base_raw = int(bool(base_record.get("raw_escalated")))
    target_raw = int(bool(target_record.get("raw_escalated")))
    base_correct = int(bool(base_record.get("correct")))
    target_correct = int(bool(target_record.get("correct")))

    deltas = {
        "correct_gain": target_correct - base_correct,
        "focus_gain": base_focus - target_focus,
        "raw_gain": base_raw - target_raw,
    }

    if deltas["correct_gain"] > 0:
        verdict = "target_better"
    elif deltas["correct_gain"] < 0:
        verdict = "target_worse"
    elif deltas["focus_gain"] > 0:
        verdict = "target_better"
    elif deltas["focus_gain"] < 0:
        verdict = "target_worse"
    elif deltas["raw_gain"] > 0:
        verdict = "target_better"
    elif deltas["raw_gain"] < 0:
        verdict = "target_worse"
    else:
        verdict = "tie"

    return verdict, deltas


def snippet(text: str | None, limit: int = 180) -> str:
    raw = (text or "").strip().replace("\n", " ")
    if len(raw) <= limit:
        return raw
    return raw[: limit - 3].rstrip() + "..."


def compact_record_view(record: dict[str, Any], family_kind: str) -> dict[str, Any]:
    return {
        "correct": bool(record.get("correct")),
        "answer": record.get("answer"),
        "compact_answer": record.get("compact_answer"),
        "route": record.get("route"),
        "raw_escalated": bool(record.get("raw_escalated")),
        family_focus_label(family_kind): family_focus_error(record, family_kind),
        "probe_status": record.get("probe_status"),
        "probe_score": record.get("probe_score"),
        "first_failing_stage": record.get("first_failing_stage"),
        "judge_label": record.get("judge_label"),
        "target_supported_clean": record.get("target_supported_clean"),
        "note_summary": snippet(record.get("final_note")),
    }


def case_sort_key(case: dict[str, Any], direction: str) -> tuple[int, int, int, str]:
    deltas = case["deltas"]
    if direction == "better":
        return (
            deltas["correct_gain"],
            deltas["focus_gain"],
            deltas["raw_gain"],
            case["item_id"],
        )
    return (
        -deltas["correct_gain"],
        -deltas["focus_gain"],
        -deltas["raw_gain"],
        case["item_id"],
    )


def build_case(
    panel_id: str,
    family_kind: str,
    item_meta: dict[str, Any],
    base_architecture: str,
    target_architecture: str,
    base_record: dict[str, Any],
    target_record: dict[str, Any],
) -> dict[str, Any]:
    verdict, deltas = classify_delta(base_record, target_record, family_kind)
    source = item_meta.get("source_provenance", {})
    return {
        "panel_id": panel_id,
        "family_kind": family_kind,
        "focus_label": family_focus_label(family_kind),
        "item_id": item_meta["id"],
        "seed": target_record["seed"],
        "n_passes": target_record["n_passes"],
        "evaluation_stratum": item_meta.get("evaluation_stratum"),
        "complexity_band": item_meta.get("complexity_band"),
        "criticality": item_meta.get("criticality"),
        "subject": item_meta.get("subject"),
        "query_text": item_meta.get("query_text"),
        "gold_answer": item_meta.get("gold_answer"),
        "benchmark_family": source.get("benchmark_family"),
        "selection_bucket": source.get("selection_bucket"),
        "evidence_ids": source.get("evidence_ids", []),
        "verdict": verdict,
        "deltas": deltas,
        "base_architecture": base_architecture,
        "target_architecture": target_architecture,
        "base": compact_record_view(base_record, family_kind),
        "target": compact_record_view(target_record, family_kind),
    }


def analyze_payload(
    payload: dict[str, Any],
    stage: str,
    target_architecture: str,
    base_architectures: list[str],
    target_n: int,
    max_cases: int,
) -> dict[str, Any]:
    aggregate: dict[str, dict[str, Any]] = {
        "benign": {},
        "hallucination": {},
    }
    cases: dict[str, dict[str, Any]] = {
        "benign": {},
        "hallucination": {},
    }

    for family_kind in aggregate:
        for architecture in base_architectures:
            aggregate[family_kind][architecture] = {
                "paired_cases": 0,
                "target_better": 0,
                "tie": 0,
                "target_worse": 0,
                "base_accuracy": 0,
                "target_accuracy": 0,
                "base_focus_error": 0,
                "target_focus_error": 0,
                "base_raw_escalation": 0,
                "target_raw_escalation": 0,
            }
            cases[family_kind][architecture] = {
                "target_better": [],
                "target_worse": [],
            }

    for panel_id, panel in payload["slice_panels"].items():
        family_kind = "hallucination" if panel["family_rollup"] == "hallucination_expanded_pool" else "benign"
        selected_items = {item["id"]: item for item in panel["selected_items"]}
        by_key: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
        for record in panel["records"]:
            if record["n_passes"] != target_n:
                continue
            architecture = record["architecture"]
            if architecture != target_architecture and architecture not in base_architectures:
                continue
            by_key[(record["item_id"], record["seed"])][architecture] = record

        for (item_id, seed), pair_records in by_key.items():
            if target_architecture not in pair_records:
                continue
            if item_id not in selected_items:
                continue
            item_meta = selected_items[item_id]
            target_record = pair_records[target_architecture]
            for base_architecture in base_architectures:
                base_record = pair_records.get(base_architecture)
                if base_record is None:
                    continue

                verdict, _ = classify_delta(base_record, target_record, family_kind)
                row = aggregate[family_kind][base_architecture]
                row["paired_cases"] += 1
                row[verdict] += 1
                row["base_accuracy"] += int(bool(base_record.get("correct")))
                row["target_accuracy"] += int(bool(target_record.get("correct")))
                row["base_focus_error"] += int(family_focus_error(base_record, family_kind))
                row["target_focus_error"] += int(family_focus_error(target_record, family_kind))
                row["base_raw_escalation"] += int(bool(base_record.get("raw_escalated")))
                row["target_raw_escalation"] += int(bool(target_record.get("raw_escalated")))

                case = build_case(
                    panel_id,
                    family_kind,
                    item_meta,
                    base_architecture,
                    target_architecture,
                    base_record,
                    target_record,
                )
                if verdict == "target_better":
                    cases[family_kind][base_architecture]["target_better"].append(case)
                elif verdict == "target_worse":
                    cases[family_kind][base_architecture]["target_worse"].append(case)

    normalized_aggregate: dict[str, dict[str, Any]] = {"benign": {}, "hallucination": {}}
    normalized_cases: dict[str, dict[str, Any]] = {"benign": {}, "hallucination": {}}
    for family_kind, rows in aggregate.items():
        for architecture, row in rows.items():
            total = max(1, row["paired_cases"])
            normalized_aggregate[family_kind][architecture] = {
                **row,
                "base_accuracy_rate": round(row["base_accuracy"] / total, 3),
                "target_accuracy_rate": round(row["target_accuracy"] / total, 3),
                "base_focus_error_rate": round(row["base_focus_error"] / total, 3),
                "target_focus_error_rate": round(row["target_focus_error"] / total, 3),
                "base_raw_escalation_rate": round(row["base_raw_escalation"] / total, 3),
                "target_raw_escalation_rate": round(row["target_raw_escalation"] / total, 3),
            }
            normalized_cases[family_kind][architecture] = {
                "target_better": sorted(
                    cases[family_kind][architecture]["target_better"],
                    key=lambda case: case_sort_key(case, "better"),
                    reverse=True,
                )[:max_cases],
                "target_worse": sorted(
                    cases[family_kind][architecture]["target_worse"],
                    key=lambda case: case_sort_key(case, "worse"),
                    reverse=True,
                )[:max_cases],
            }

    return {
        "stage": stage,
        "source_artifact": JSON_TEMPLATE.format(stage=stage),
        "target_architecture": target_architecture,
        "base_architectures": base_architectures,
        "target_n": target_n,
        "seeds": payload["seeds"],
        "aggregate": normalized_aggregate,
        "cases": normalized_cases,
    }


def case_markdown(case: dict[str, Any]) -> list[str]:
    focus_label = case["focus_label"]
    base = case["base"]
    target = case["target"]
    lines = [
        f"- `{case['item_id']}` seed={case['seed']} stratum=`{case['evaluation_stratum']}` subject=`{case['subject']}`",
        f"  query: {case['query_text']}",
        f"  gold: `{case['gold_answer']}`",
        f"  {case['base_architecture']}: correct={int(base['correct'])}, {focus_label}={int(base[focus_label])}, raw={int(base['raw_escalated'])}, route=`{base['route']}`, answer=`{base['answer']}`",
        f"  {case['target_architecture']}: correct={int(target['correct'])}, {focus_label}={int(target[focus_label])}, raw={int(target['raw_escalated'])}, route=`{target['route']}`, answer=`{target['answer']}`",
    ]
    if base["note_summary"] or target["note_summary"]:
        lines.append(f"  note delta: base=`{base['note_summary']}` | target=`{target['note_summary']}`")
    return lines


def build_summary(report: dict[str, Any]) -> str:
    lines = [
        f"# Expanded Benchmark Stage {report['stage'].title()} Error Analysis",
        "",
        "这份分析不再只看 family-level 均值，而是做 item-level paired comparison，专门检查 `PSU` 相比 `scale_aware_*` 到底救回了哪些样本、又在哪些地方仍有弱点。",
        "",
        f"- source artifact: `{report['source_artifact']}`",
        f"- target architecture: `{report['target_architecture']}`",
        f"- base architectures: `{', '.join(report['base_architectures'])}`",
        f"- N: `{report['target_n']}`",
        f"- seeds: `{report['seeds']}`",
        "",
    ]

    for family_kind in ["benign", "hallucination"]:
        focus_label = family_focus_label(family_kind)
        lines.append(f"## {family_kind.title()} Aggregate")
        lines.append("")
        lines.append("| Base | Paired | PSU better | Tie | PSU worse | Base acc | PSU acc | Base " + focus_label + " | PSU " + focus_label + " | Base raw | PSU raw |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for architecture in report["base_architectures"]:
            row = report["aggregate"][family_kind][architecture]
            lines.append(
                f"| {architecture} | {row['paired_cases']} | {row['target_better']} | {row['tie']} | {row['target_worse']} | "
                f"{row['base_accuracy_rate']:.3f} | {row['target_accuracy_rate']:.3f} | {row['base_focus_error_rate']:.3f} | "
                f"{row['target_focus_error_rate']:.3f} | {row['base_raw_escalation_rate']:.3f} | {row['target_raw_escalation_rate']:.3f} |"
            )
        lines.append("")

        for direction, title in [("target_better", "Representative PSU Wins"), ("target_worse", "Representative PSU Regressions")]:
            lines.append(f"### {title}")
            lines.append("")
            emitted = False
            for architecture in report["base_architectures"]:
                rows = report["cases"][family_kind][architecture][direction]
                if not rows:
                    continue
                emitted = True
                lines.append(f"#### vs {architecture}")
                lines.append("")
                for case in rows:
                    lines.extend(case_markdown(case))
                lines.append("")
            if not emitted:
                lines.append("- none")
                lines.append("")

    lines.extend(
        [
            "## Readout",
            "",
            "- 如果 benign 侧的主要优势集中在 `compact_answer=ABSTAIN` 被 `PSU` 救回，那就说明目前最核心的改进不是最终路由，而是 carry-forward scaffold 减少了压缩后 answerability 蒸发。",
            "- 如果 hallucination 侧的优势主要体现为 `raw_escalated` 从 1 变 0，则说明 `PSU` 在 unsupported target 上确实更稳定地把 absent signal 固化下来了。",
            "- 如果后续 main run 也复现同样的 paired pattern，这份 artifact 就可以直接作为 paper 里的 error-analysis section 基础材料。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    stage = selected_stage()
    target_architecture = selected_target_architecture()
    base_architectures = selected_base_architectures()
    target_n = selected_target_n()
    max_cases = selected_max_cases()

    payload = load_payload(stage)
    report = analyze_payload(
        payload=payload,
        stage=stage,
        target_architecture=target_architecture,
        base_architectures=base_architectures,
        target_n=target_n,
        max_cases=max_cases,
    )

    base_dir = Path(__file__).resolve().parent
    output_json_path = base_dir / OUTPUT_JSON_TEMPLATE.format(stage=stage)
    output_md_path = base_dir / OUTPUT_MD_TEMPLATE.format(stage=stage)
    output_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md_path.write_text(build_summary(report), encoding="utf-8")
    print(f"Wrote {output_json_path}")
    print(f"Wrote {output_md_path}")


if __name__ == "__main__":
    main()
