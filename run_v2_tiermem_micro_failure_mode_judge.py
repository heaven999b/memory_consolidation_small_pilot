#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional convenience path
    load_dotenv = None

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_JUDGE_MODEL = "gpt-4.1-mini"
DEFAULT_TIMEOUT_SEC = 60.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_WORKERS = 8
VALID_LABELS = {
    "CORRECT",
    "ABSTAIN_FORGETTING",
    "UNSUPPORTED_FABRICATION",
    "FACT_DISTORTION",
    "ERROR",
}
VALID_ANSWERABILITY = {"FACTUAL", "UNKNOWN_ABSTAIN", "ERROR"}

if load_dotenv is not None:
    load_dotenv(PROJECT_ROOT / ".env.v3")
    load_dotenv(PROJECT_ROOT / ".env")

FAILURE_MODE_PROMPT = """You are grading one QA result from a long-memory benchmark.

Return exactly one JSON object with these keys:
- "label": one of ["CORRECT", "ABSTAIN_FORGETTING", "UNSUPPORTED_FABRICATION", "FACT_DISTORTION"]
- "gold_answerability": one of ["FACTUAL", "UNKNOWN_ABSTAIN"]
- "explanation": one short sentence

Definitions:
1. CORRECT
   - The generated answer semantically matches the gold answer.
   - This includes correct abstention when the gold answer is unknown / not provided / not mentioned.
   - This also includes correct factual negation such as "No, he was a director", which is FACTUAL, not UNKNOWN_ABSTAIN.
   - A short answer that captures the key point, such as the correct yes/no polarity,
     counts as CORRECT even if it omits supplementary details from the gold,
     as long as it does not contradict the gold.

2. ABSTAIN_FORGETTING
   - The gold answer contains a concrete answer or supported negation.
   - The generated answer mainly says the information is missing, unknown, not provided, not mentioned, or cannot be determined.
   - Use this when the answer fails by refusing or abstaining instead of retrieving the supported fact.

3. UNSUPPORTED_FABRICATION
   - The gold answer is unknown / not provided / abstain-like.
   - The generated answer asserts a specific fact, number, identity, date, timeline, or other concrete claim instead of abstaining.

4. FACT_DISTORTION
   - The gold answer contains a concrete answer or supported negation.
   - The generated answer gives a substantive but materially wrong or distorted answer.
   - Choose FACT_DISTORTION ONLY when the answer materially contradicts or changes
     the key meaning of the gold, such as a wrong date, wrong role, invented relationship,
     reversed polarity, wrong preference, or wrong timeline.
   - Do NOT use FACT_DISTORTION merely because the answer omits supplementary detail,
     is shorter than the gold, or adds extra context that is consistent with and does not
     contradict the gold.

Important grading rules:
- Be semantic, not lexical.
- "Unknown", "not provided", and similar gold answers mean UNKNOWN_ABSTAIN.
- A gold answer like "No, Martin is a director at Huaxin Consulting" is FACTUAL because it contains a supported fact.
- If the generated answer adds extra invented specifics beyond an unknown gold answer, choose UNSUPPORTED_FABRICATION.
- If the generated answer gives a concrete but wrong interpretation of a factual gold answer, choose FACT_DISTORTION.
- Adding extra specifics that are consistent with the gold is NOT fabrication or distortion.
- Only penalize added specifics when they contradict the gold, or when the gold is
  unknown / abstain-like and the answer asserts a concrete claim.

Question: {question}
Gold answer: {gold_answer}
Generated answer: {generated_answer}
"""


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use an LLM judge to classify micro-slice QA results into failure modes."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--sweep-report", type=str, default=None)
    source_group.add_argument("--run-root", action="append", default=None)
    parser.add_argument("--report-id", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--judge-model", type=str, default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    parser.add_argument("--timeout-sec", type=float, default=DEFAULT_TIMEOUT_SEC)
    parser.add_argument("--client-max-retries", type=int, default=DEFAULT_MAX_RETRIES)
    parser.add_argument("--judge-attempts", type=int, default=3)
    parser.add_argument("--retry-backoff-sec", type=float, default=1.0)
    parser.add_argument("--examples-per-label", type=int, default=2)
    parser.add_argument("--max-trajectory-highlights", type=int, default=8)
    return parser


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _iter_session_qa_logs(run_root: Path) -> Iterable[Path]:
    sessions_dir = run_root / "sessions"
    if not sessions_dir.exists():
        return []
    return sorted(sessions_dir.glob("*_qa.jsonl"))


def _load_qa_rows(run_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for qa_path in _iter_session_qa_logs(run_root):
        rows.extend(_read_jsonl(qa_path))
    return rows


def _sanitize_token(value: str) -> str:
    token = re.sub(r"[^A-Z_]+", "_", value.strip().upper())
    token = re.sub(r"_+", "_", token).strip("_")
    return token


def _normalize_label(value: Any) -> str:
    token = _sanitize_token(str(value or ""))
    aliases = {
        "CORRECT": "CORRECT",
        "RIGHT": "CORRECT",
        "ABSTAIN_FORGETTING": "ABSTAIN_FORGETTING",
        "ABSTAINING_FORGETTING": "ABSTAIN_FORGETTING",
        "FORGETTING": "ABSTAIN_FORGETTING",
        "UNSUPPORTED_FABRICATION": "UNSUPPORTED_FABRICATION",
        "FABRICATION": "UNSUPPORTED_FABRICATION",
        "UNSUPPORTED": "UNSUPPORTED_FABRICATION",
        "FACT_DISTORTION": "FACT_DISTORTION",
        "DISTORTION": "FACT_DISTORTION",
        "WRONG_FACT_DISTORTION": "FACT_DISTORTION",
    }
    return aliases.get(token, token if token in VALID_LABELS else "ERROR")


def _normalize_answerability(value: Any) -> str:
    token = _sanitize_token(str(value or ""))
    aliases = {
        "FACTUAL": "FACTUAL",
        "KNOWN": "FACTUAL",
        "SUPPORTED_FACT": "FACTUAL",
        "UNKNOWN_ABSTAIN": "UNKNOWN_ABSTAIN",
        "UNKNOWN": "UNKNOWN_ABSTAIN",
        "ABSTAIN": "UNKNOWN_ABSTAIN",
        "NOT_PROVIDED": "UNKNOWN_ABSTAIN",
    }
    return aliases.get(token, token if token in VALID_ANSWERABILITY else "ERROR")


def _build_client(args: argparse.Namespace) -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:  # pragma: no cover - surfaced at runtime
        raise RuntimeError(
            "openai package is required for run_v2_tiermem_micro_failure_mode_judge.py"
        ) from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
    client_kwargs: dict[str, Any] = {
        "api_key": api_key,
        "timeout": args.timeout_sec,
        "max_retries": args.client_max_retries,
    }
    if base_url:
        client_kwargs["base_url"] = base_url
    return OpenAI(**client_kwargs)


def _judge_prompt(question: str, gold_answer: str, generated_answer: str) -> str:
    return FAILURE_MODE_PROMPT.format(
        question=str(question or ""),
        gold_answer=str(gold_answer or ""),
        generated_answer=str(generated_answer or ""),
    )


def _judge_row(
    row: dict[str, Any],
    client: Any,
    judge_model: str,
    judge_attempts: int,
    retry_backoff_sec: float,
) -> dict[str, Any]:
    question = str(row.get("question", "") or "")
    gold_answer = str(row.get("ground_truth", "") or "")
    generated_answer = str(row.get("model_response", "") or "")
    last_error = "unknown judge failure"

    for attempt in range(1, max(1, judge_attempts) + 1):
        try:
            response = client.chat.completions.create(
                model=judge_model,
                messages=[{"role": "user", "content": _judge_prompt(question, gold_answer, generated_answer)}],
                response_format={"type": "json_object"},
                temperature=0.0,
            )
            content = response.choices[0].message.content or "{}"
            parsed = json.loads(content)
            label = _normalize_label(parsed.get("label"))
            answerability = _normalize_answerability(parsed.get("gold_answerability"))
            if label == "ERROR":
                raise ValueError(f"invalid label: {parsed.get('label')!r}")
            if answerability == "ERROR":
                raise ValueError(f"invalid gold_answerability: {parsed.get('gold_answerability')!r}")
            return {
                "query_id": row.get("query_id"),
                "session_id": row.get("session_id"),
                "question": question,
                "gold_answer": gold_answer,
                "prediction": generated_answer,
                "route": ((row.get("mechanism_trace") or {}).get("route") or "UNKNOWN"),
                "exact_match_score": float(row.get("score", 0.0) or 0.0),
                "judge_label": label,
                "gold_answerability": answerability,
                "judge_explanation": str(parsed.get("explanation", "") or "").strip(),
            }
        except Exception as exc:  # pragma: no cover - network/runtime dependent
            last_error = str(exc)
            if attempt < max(1, judge_attempts):
                time.sleep(max(0.0, retry_backoff_sec) * attempt)

    return {
        "query_id": row.get("query_id"),
        "session_id": row.get("session_id"),
        "question": question,
        "gold_answer": gold_answer,
        "prediction": generated_answer,
        "route": ((row.get("mechanism_trace") or {}).get("route") or "UNKNOWN"),
        "exact_match_score": float(row.get("score", 0.0) or 0.0),
        "judge_label": "ERROR",
        "gold_answerability": "ERROR",
        "judge_explanation": "",
        "judge_error": last_error,
    }


def _summarize_condition(
    condition: dict[str, Any],
    details: list[dict[str, Any]],
    examples_per_label: int,
) -> dict[str, Any]:
    total = len(details)
    label_counts = Counter(detail.get("judge_label", "ERROR") for detail in details)
    answerability_counts = Counter(detail.get("gold_answerability", "ERROR") for detail in details)
    wrong_total = total - label_counts.get("CORRECT", 0)
    factual_total = answerability_counts.get("FACTUAL", 0)
    unknown_total = answerability_counts.get("UNKNOWN_ABSTAIN", 0)

    examples_by_label: dict[str, list[dict[str, Any]]] = {}
    for label in ("ABSTAIN_FORGETTING", "UNSUPPORTED_FABRICATION", "FACT_DISTORTION", "ERROR"):
        label_examples: list[dict[str, Any]] = []
        for detail in details:
            if detail.get("judge_label") != label:
                continue
            label_examples.append(
                {
                    "query_id": detail.get("query_id"),
                    "question": detail.get("question"),
                    "gold_answer": detail.get("gold_answer"),
                    "prediction": detail.get("prediction"),
                    "explanation": detail.get("judge_explanation") or detail.get("judge_error", ""),
                }
            )
            if len(label_examples) >= examples_per_label:
                break
        examples_by_label[label] = label_examples

    summary = {
        "total": total,
        "correct": label_counts.get("CORRECT", 0),
        "wrong": wrong_total,
        "error": label_counts.get("ERROR", 0),
        "correct_rate": (label_counts.get("CORRECT", 0) / total) if total else 0.0,
        "wrong_rate": (wrong_total / total) if total else 0.0,
        "label_counts": dict(label_counts),
        "label_rates": {
            label: (label_counts.get(label, 0) / total) if total else 0.0
            for label in ("CORRECT", "ABSTAIN_FORGETTING", "UNSUPPORTED_FABRICATION", "FACT_DISTORTION", "ERROR")
        },
        "gold_answerability_counts": dict(answerability_counts),
        "factual_total": factual_total,
        "unknown_abstain_total": unknown_total,
        "abstain_forgetting_rate_on_factual": (
            label_counts.get("ABSTAIN_FORGETTING", 0) / factual_total if factual_total else 0.0
        ),
        "fact_distortion_rate_on_factual": (
            label_counts.get("FACT_DISTORTION", 0) / factual_total if factual_total else 0.0
        ),
        "unsupported_fabrication_rate_on_unknown": (
            label_counts.get("UNSUPPORTED_FABRICATION", 0) / unknown_total if unknown_total else 0.0
        ),
        "examples_by_label": examples_by_label,
    }

    return {
        "run_id": condition.get("run_id"),
        "run_root": condition.get("run_root"),
        "route_mode": condition.get("route_mode"),
        "consolidation_passes": condition.get("consolidation_passes"),
        "summary_f1": float(condition.get("summary_f1", 0.0) or 0.0),
        "summary_bleu1": float(condition.get("summary_bleu1", 0.0) or 0.0),
        "mean_exact_match": float(condition.get("mean_exact_match", 0.0) or 0.0),
        "cost_summary": condition.get("cost_summary", {}),
        "judge_summary": summary,
    }


def _sort_condition_key(condition: dict[str, Any]) -> tuple[Any, ...]:
    return (
        str(condition.get("route_mode") or ""),
        int(condition.get("consolidation_passes", 0) or 0),
        str(condition.get("run_id") or ""),
    )


def _build_trajectory_highlights(
    condition_summaries: list[dict[str, Any]],
    condition_details: dict[str, list[dict[str, Any]]],
    max_items: int,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for condition in condition_summaries:
        run_id = str(condition.get("run_id") or "")
        route_mode = str(condition.get("route_mode") or "")
        for detail in condition_details.get(run_id, []):
            key = (route_mode, str(detail.get("query_id") or detail.get("question") or ""))
            grouped[key].append(
                {
                    "run_id": run_id,
                    "passes": int(condition.get("consolidation_passes", 0) or 0),
                    "question": detail.get("question"),
                    "gold_answer": detail.get("gold_answer"),
                    "prediction": detail.get("prediction"),
                    "judge_label": detail.get("judge_label"),
                }
            )

    changed: list[dict[str, Any]] = []
    for (route_mode, _), entries in grouped.items():
        if len(entries) < 2:
            continue
        entries = sorted(entries, key=lambda item: (item["passes"], item["run_id"]))
        labels = [entry["judge_label"] for entry in entries]
        predictions = [str(entry.get("prediction") or "").strip() for entry in entries]
        if len(set(labels)) == 1 and len(set(predictions)) == 1:
            continue
        changed.append(
            {
                "route_mode": route_mode,
                "question": entries[0].get("question"),
                "gold_answer": entries[0].get("gold_answer"),
                "trajectory": entries,
                "label_change_count": sum(
                    1
                    for left, right in zip(labels, labels[1:])
                    if left != right
                ),
            }
        )

    changed.sort(
        key=lambda item: (
            -int(item["label_change_count"]),
            str(item.get("route_mode") or ""),
            str(item.get("question") or ""),
        )
    )
    return changed[: max(0, max_items)]


def _load_conditions_from_sweep(path: Path) -> tuple[str, list[dict[str, Any]]]:
    payload = _read_json(path)
    conditions = [dict(condition) for condition in payload.get("conditions", [])]
    if not conditions:
        raise RuntimeError(f"No conditions found in sweep report: {path}")
    report_id = str(payload.get("sweep_id") or path.stem)
    return report_id, conditions


def _load_conditions_from_roots(run_roots: list[str]) -> tuple[str, list[dict[str, Any]]]:
    conditions: list[dict[str, Any]] = []
    for raw_root in run_roots:
        run_root = Path(raw_root).expanduser().resolve()
        summary_path = run_root / "summary.json"
        summary_payload = _read_json(summary_path) if summary_path.exists() else {}
        conditions.append(
            {
                "run_id": run_root.name,
                "run_root": str(run_root),
                "route_mode": summary_payload.get("route_mode"),
                "consolidation_passes": summary_payload.get("consolidation_passes", 0),
                "summary_f1": float((summary_payload.get("metrics") or {}).get("f1", 0.0) or 0.0),
                "summary_bleu1": float((summary_payload.get("metrics") or {}).get("bleu1", 0.0) or 0.0),
                "mean_exact_match": float(summary_payload.get("mean_exact_match", 0.0) or 0.0),
                "cost_summary": summary_payload.get("cost_summary", {}),
            }
        )
    if not conditions:
        raise RuntimeError("No run roots were provided.")
    report_id = datetime.now().strftime("micro_failure_mode_%Y%m%d_%H%M%S")
    return report_id, conditions


def _default_output_dir(args: argparse.Namespace, first_run_root: Path) -> Path:
    if args.output_dir:
        return Path(args.output_dir).expanduser().resolve()
    if args.sweep_report:
        sweep_path = Path(args.sweep_report).expanduser().resolve()
        return sweep_path.parent.parent / "judge_reports"
    return first_run_root.parents[2] / "judge_reports"


def _write_condition_details(
    output_dir: Path,
    report_id: str,
    condition_summary: dict[str, Any],
    details: list[dict[str, Any]],
    judge_model: str,
) -> Path:
    detail_dir = output_dir / report_id
    detail_dir.mkdir(parents=True, exist_ok=True)
    detail_path = detail_dir / f"{condition_summary['run_id']}.json"
    payload = {
        "generated_at": datetime.now().isoformat(),
        "judge_model": judge_model,
        "condition": condition_summary,
        "details": details,
    }
    detail_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return detail_path


def _write_report(
    output_dir: Path,
    report_id: str,
    judge_model: str,
    condition_summaries: list[dict[str, Any]],
    detail_paths: dict[str, str],
    trajectory_highlights: list[dict[str, Any]],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{report_id}.json"
    md_path = output_dir / f"{report_id}.md"

    payload = {
        "report_id": report_id,
        "generated_at": datetime.now().isoformat(),
        "judge_model": judge_model,
        "conditions": [
            {
                **condition,
                "detail_json": detail_paths.get(str(condition.get("run_id") or "")),
            }
            for condition in condition_summaries
        ],
        "trajectory_highlights": trajectory_highlights,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# TierMem Micro Failure-Mode Judge: {report_id}",
        "",
        f"- judge_model: `{judge_model}`",
        "",
        "| route_mode | N | total | correct | abstain_forgetting | unsupported_fabrication | fact_distortion | F1 | detail_json |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for condition in condition_summaries:
        judge_summary = condition["judge_summary"]
        lines.append(
            "| {route_mode} | {passes} | {total} | {correct_rate:.3f} | {forgetting_rate:.3f} | {fabrication_rate:.3f} | {distortion_rate:.3f} | {f1:.3f} | `{detail_json}` |".format(
                route_mode=condition.get("route_mode"),
                passes=condition.get("consolidation_passes"),
                total=judge_summary.get("total"),
                correct_rate=judge_summary.get("correct_rate", 0.0),
                forgetting_rate=judge_summary.get("abstain_forgetting_rate_on_factual", 0.0),
                fabrication_rate=judge_summary.get("unsupported_fabrication_rate_on_unknown", 0.0),
                distortion_rate=judge_summary.get("fact_distortion_rate_on_factual", 0.0),
                f1=condition.get("summary_f1", 0.0),
                detail_json=detail_paths.get(str(condition.get("run_id") or ""), ""),
            )
        )

    if trajectory_highlights:
        lines.extend(["", "## Trajectory Highlights", ""])
        for item in trajectory_highlights:
            lines.append(
                f"- route=`{item['route_mode']}` | q=`{item['question']}` | gold=`{item['gold_answer']}`"
            )
            for step in item["trajectory"]:
                lines.append(
                    f"  N={step['passes']}: `{step['judge_label']}` | `{str(step.get('prediction') or '')[:220]}`"
                )

    for condition in condition_summaries:
        judge_summary = condition["judge_summary"]
        lines.extend(
            [
                "",
                f"## {condition['run_id']}",
                "",
                f"- route_mode: `{condition.get('route_mode')}`",
                f"- consolidation_passes: `{condition.get('consolidation_passes')}`",
                f"- summary_f1: `{condition.get('summary_f1', 0.0):.3f}`",
                f"- totals: factual=`{judge_summary.get('factual_total', 0)}`, unknown_abstain=`{judge_summary.get('unknown_abstain_total', 0)}`, total=`{judge_summary.get('total', 0)}`",
            ]
        )
        for label in ("ABSTAIN_FORGETTING", "UNSUPPORTED_FABRICATION", "FACT_DISTORTION", "ERROR"):
            examples = (judge_summary.get("examples_by_label") or {}).get(label) or []
            lines.append(f"- {label}: `{judge_summary['label_counts'].get(label, 0)}`")
            for example in examples:
                lines.append(
                    "  q=`{question}` | gold=`{gold}` | pred=`{pred}` | why=`{why}`".format(
                        question=example.get("question"),
                        gold=example.get("gold_answer"),
                        pred=str(example.get("prediction") or "")[:220],
                        why=example.get("explanation"),
                    )
                )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    args = _build_parser().parse_args()

    if args.sweep_report:
        report_id, conditions = _load_conditions_from_sweep(Path(args.sweep_report).expanduser().resolve())
    else:
        report_id, conditions = _load_conditions_from_roots(args.run_root or [])
    if args.report_id:
        report_id = args.report_id

    for condition in conditions:
        if "run_root" not in condition:
            raise RuntimeError(f"Condition missing run_root: {condition}")

    conditions = sorted(conditions, key=_sort_condition_key)
    first_run_root = Path(str(conditions[0]["run_root"])).expanduser().resolve()
    output_dir = _default_output_dir(args, first_run_root)
    client = _build_client(args)

    condition_summaries: list[dict[str, Any]] = []
    condition_details: dict[str, list[dict[str, Any]]] = {}
    detail_paths: dict[str, str] = {}

    for condition in conditions:
        run_id = str(condition.get("run_id") or "")
        run_root = Path(str(condition.get("run_root"))).expanduser().resolve()
        qa_rows = _load_qa_rows(run_root)
        if not qa_rows:
            raise RuntimeError(f"No QA rows found under {run_root}")
        print(
            f"[judge] run_id={run_id} route={condition.get('route_mode')} "
            f"N={condition.get('consolidation_passes')} qa_rows={len(qa_rows)}"
        )

        details: list[dict[str, Any]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.max_workers)) as executor:
            futures = [
                executor.submit(
                    _judge_row,
                    row,
                    client,
                    args.judge_model,
                    args.judge_attempts,
                    args.retry_backoff_sec,
                )
                for row in qa_rows
            ]
            for future in concurrent.futures.as_completed(futures):
                details.append(future.result())

        details.sort(key=lambda item: (str(item.get("session_id") or ""), str(item.get("query_id") or "")))
        condition_details[run_id] = details
        condition_summary = _summarize_condition(
            condition=condition,
            details=details,
            examples_per_label=max(0, args.examples_per_label),
        )
        condition_summaries.append(condition_summary)
        detail_path = _write_condition_details(
            output_dir=output_dir,
            report_id=report_id,
            condition_summary=condition_summary,
            details=details,
            judge_model=args.judge_model,
        )
        detail_paths[run_id] = str(detail_path)

    trajectory_highlights = _build_trajectory_highlights(
        condition_summaries=condition_summaries,
        condition_details=condition_details,
        max_items=args.max_trajectory_highlights,
    )
    json_path, md_path = _write_report(
        output_dir=output_dir,
        report_id=report_id,
        judge_model=args.judge_model,
        condition_summaries=condition_summaries,
        detail_paths=detail_paths,
        trajectory_highlights=trajectory_highlights,
    )

    print(
        json.dumps(
            {
                "report_id": report_id,
                "judge_model": args.judge_model,
                "report_json": str(json_path),
                "report_md": str(md_path),
                "conditions": len(condition_summaries),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
