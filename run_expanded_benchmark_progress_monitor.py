from __future__ import annotations

import argparse
import html
import json
import statistics
import subprocess
import time
import traceback
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any

import run_actual_carry_forward_round as carry_base
import run_expanded_benchmark_staged as staged


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
MAX_PASSES = max(staged.N_VALUES)
PROCESS_QUERY = "run_expanded_benchmark_staged.py main"

TERMINAL_EVENTS = {
    "attempt_success",
    "attempt_failure",
    "attempt_timeout",
    "attempt_bad_json",
    "summarize_failed",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a live monitor page for the expanded benchmark main run.")
    parser.add_argument("--stage", default="main", choices=sorted(staged.STAGE_SPECS))
    parser.add_argument("--seeds", default="", help="Comma-separated seed list. Defaults to the stage default.")
    parser.add_argument("--pid", type=int, default=0, help="Optional benchmark PID to monitor directly.")
    parser.add_argument("--refresh-seconds", type=int, default=20, help="HTML auto-refresh interval.")
    parser.add_argument("--interval", type=int, default=30, help="Watch polling interval.")
    parser.add_argument("--watch", action="store_true", help="Continuously refresh the monitor artifacts.")
    parser.add_argument(
        "--stop-when-finished",
        action="store_true",
        help="Exit watch mode after the main process is gone and the final stage artifacts exist.",
    )
    return parser.parse_args()


def monitor_json_path(stage: str) -> Path:
    return OUTPUT_DIR / f"expanded_benchmark_stage_{stage}_monitor.json"


def monitor_html_path(stage: str) -> Path:
    return OUTPUT_DIR / f"expanded_benchmark_stage_{stage}_monitor.html"


def monitor_md_path(stage: str) -> Path:
    return OUTPUT_DIR / f"expanded_benchmark_stage_{stage}_monitor.md"


def monitor_watch_log_path(stage: str) -> Path:
    return OUTPUT_DIR / f"expanded_benchmark_stage_{stage}_monitor_watch.log"


def selected_seeds(stage: str, seeds_arg: str) -> list[int]:
    if seeds_arg.strip():
        return [int(part.strip()) for part in seeds_arg.split(",") if part.strip()]
    seeds_text = staged.STAGE_SPECS[stage]["default_seeds"]
    return [int(part.strip()) for part in seeds_text.split(",") if part.strip()]


def load_stage_panels(stage: str) -> list[dict[str, Any]]:
    panels: list[dict[str, Any]] = []
    for spec in staged.panel_specs():
        manifest = staged.load_json(BASE_DIR / spec["manifest_path"])
        selected_items = staged.select_items_for_stage(manifest["items"], stage)
        panels.append(
            {
                "panel_id": spec["panel_id"],
                "cache_dir": OUTPUT_DIR / spec["cache_dir_name"],
                "prompt_version": spec["prompt_version"],
                "item_ids": [item["id"] for item in selected_items],
            }
        )
    return panels


def psu_cache_prefix() -> str:
    source_intervention = carry_base.SOURCE_INTERVENTION["tiny_carry_forward_scaffold"]
    return f"{carry_base.hard_base.refine_base.cache_prefix(source_intervention)}_{source_intervention}"


def cache_file_name(method: str, prompt_version: str, item_id: str, seed: int, pass_idx: int) -> str:
    if method == "base":
        prefix = prompt_version
    elif method == "psu":
        prefix = psu_cache_prefix()
    else:
        raise RuntimeError(f"Unknown monitor method: {method}")
    return f"{prefix}_{item_id}_seed{seed}_pass{pass_idx}.json"


def item_progress(cache_dir: Path, method: str, prompt_version: str, item_id: str, seed: int) -> dict[str, Any]:
    pass_count = 0
    for pass_idx in range(1, MAX_PASSES + 1):
        if (cache_dir / cache_file_name(method, prompt_version, item_id, seed, pass_idx)).exists():
            pass_count += 1
    return {
        "item_id": item_id,
        "pass_count": pass_count,
        "complete": pass_count >= MAX_PASSES,
        "started": pass_count > 0,
    }


def summarize_cell(panel: dict[str, Any], method: str, seed: int) -> dict[str, Any]:
    rows = [
        item_progress(panel["cache_dir"], method, panel["prompt_version"], item_id, seed)
        for item_id in panel["item_ids"]
    ]
    total_items = len(rows)
    completed_items = sum(1 for row in rows if row["complete"])
    started_items = sum(1 for row in rows if row["started"])
    completed_passes = sum(row["pass_count"] for row in rows)
    partial_items = [row for row in rows if 0 < row["pass_count"] < MAX_PASSES]
    unstarted_items = [row for row in rows if row["pass_count"] == 0]
    latest_partial = partial_items[-1] if partial_items else None
    return {
        "total_items": total_items,
        "completed_items": completed_items,
        "started_items": started_items,
        "completed_passes": completed_passes,
        "total_passes": total_items * MAX_PASSES,
        "item_completion_rate": round(completed_items / max(1, total_items), 4),
        "pass_completion_rate": round(completed_passes / max(1, total_items * MAX_PASSES), 4),
        "latest_partial": latest_partial,
        "next_unstarted": unstarted_items[0]["item_id"] if unstarted_items else None,
    }


def aggregate_cells(cells: list[dict[str, Any]]) -> dict[str, Any]:
    total_items = sum(cell["total_items"] for cell in cells)
    completed_items = sum(cell["completed_items"] for cell in cells)
    started_items = sum(cell["started_items"] for cell in cells)
    completed_passes = sum(cell["completed_passes"] for cell in cells)
    total_passes = sum(cell["total_passes"] for cell in cells)
    return {
        "total_items": total_items,
        "completed_items": completed_items,
        "started_items": started_items,
        "completed_passes": completed_passes,
        "total_passes": total_passes,
        "item_completion_rate": round(completed_items / max(1, total_items), 4),
        "pass_completion_rate": round(completed_passes / max(1, total_passes), 4),
    }


def tail_jsonl(path: Path, limit: int = 120) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    window: deque[str] = deque(maxlen=limit)
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                window.append(line)
    events: list[dict[str, Any]] = []
    for line in window:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def active_attempt(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    open_attempts: dict[tuple[str, int], dict[str, Any]] = {}
    for event in events:
        cache_key = event.get("cache_key")
        attempt = int(event.get("attempt", 0) or 0)
        key = (cache_key, attempt)
        if event.get("event") == "attempt_start":
            open_attempts[key] = event
        elif event.get("event") in TERMINAL_EVENTS:
            open_attempts.pop(key, None)
    if not open_attempts:
        return None
    return max(open_attempts.values(), key=lambda row: float(row.get("timestamp", 0.0) or 0.0))


def format_timestamp(epoch_s: float | None) -> str | None:
    if not epoch_s:
        return None
    return datetime.fromtimestamp(epoch_s).strftime("%Y-%m-%d %H:%M:%S")


def summarize_log(path: Path) -> dict[str, Any]:
    events = tail_jsonl(path)
    success_events = [event for event in events if event.get("event") == "attempt_success"]
    durations = [
        float(event["duration_s"])
        for event in success_events
        if event.get("duration_s") is not None
    ]
    active = active_attempt(events)
    last_event = events[-1] if events else None
    last_success = success_events[-1] if success_events else None
    median_duration = round(statistics.median(durations), 3) if durations else None
    return {
        "path": str(path),
        "exists": path.exists(),
        "last_event": last_event,
        "last_success": last_success,
        "active_attempt": active,
        "recent_median_duration_s": median_duration,
        "recent_success_count": len(success_events),
    }


def elapsed_to_seconds(raw: str) -> int | None:
    if not raw:
        return None
    day_count = 0
    clock = raw
    if "-" in raw:
        day_text, clock = raw.split("-", 1)
        day_count = int(day_text)
    parts = [int(part) for part in clock.split(":")]
    if len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    elif len(parts) == 3:
        hours, minutes, seconds = parts
    else:
        return None
    return day_count * 86400 + hours * 3600 + minutes * 60 + seconds


def probe_process(pid: int) -> dict[str, Any]:
    if pid > 0:
        command = ["ps", "-p", str(pid), "-o", "pid=", "-o", "etime=", "-o", "command="]
    else:
        command = ["ps", "-axo", "pid=", "-o", "etime=", "-o", "command="]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=False, timeout=10)
    except Exception as exc:
        return {
            "alive": None,
            "pid": pid or None,
            "elapsed": None,
            "elapsed_seconds": None,
            "command": None,
            "error": str(exc),
        }
    lines = [line.rstrip() for line in proc.stdout.splitlines() if line.strip()]
    if pid > 0:
        if not lines:
            return {"alive": False, "pid": pid, "elapsed": None, "elapsed_seconds": None, "command": None, "error": None}
        line = lines[0]
    else:
        matches = [line for line in lines if PROCESS_QUERY in line]
        if not matches:
            return {"alive": False, "pid": None, "elapsed": None, "elapsed_seconds": None, "command": None, "error": None}
        line = matches[-1]
    parts = line.strip().split(None, 2)
    if len(parts) < 3:
        return {"alive": True, "pid": pid or None, "elapsed": None, "elapsed_seconds": None, "command": line.strip(), "error": "unexpected_ps_format"}
    pid_text, elapsed, command_text = parts
    return {
        "alive": True,
        "pid": int(pid_text),
        "elapsed": elapsed,
        "elapsed_seconds": elapsed_to_seconds(elapsed),
        "command": command_text,
        "error": None,
    }


def estimate_eta_seconds(total_remaining_passes: int, logs: list[dict[str, Any]]) -> int | None:
    durations: list[float] = []
    for log in logs:
        last_success = log.get("last_success")
        if last_success and last_success.get("duration_s") is not None:
            durations.append(float(last_success["duration_s"]))
        median_duration = log.get("recent_median_duration_s")
        if median_duration is not None:
            durations.append(float(median_duration))
    if not durations or total_remaining_passes <= 0:
        return None
    estimate = statistics.median(durations) * total_remaining_passes
    return int(round(estimate))


def human_duration(total_seconds: int | None) -> str | None:
    if total_seconds is None:
        return None
    minutes, seconds = divmod(max(0, total_seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours}h")
    if minutes or hours or days:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)


def event_age_seconds(event: dict[str, Any] | None, now_epoch: float) -> int | None:
    if not event:
        return None
    timestamp = event.get("timestamp")
    if timestamp is None:
        return None
    return max(0, int(round(float(now_epoch) - float(timestamp))))


def assess_log_health(log: dict[str, Any], now_epoch: float) -> dict[str, Any]:
    active = log.get("active_attempt")
    last_success = log.get("last_success")
    last_event = log.get("last_event")
    active_age_seconds = event_age_seconds(active, now_epoch)
    success_age_seconds = event_age_seconds(last_success, now_epoch)
    last_event_age_seconds = event_age_seconds(last_event, now_epoch)

    if active_age_seconds is not None and active_age_seconds <= 300:
        status = "moving"
        summary = f"active attempt for {human_duration(active_age_seconds)}"
    elif success_age_seconds is not None and success_age_seconds <= 180:
        status = "moving"
        summary = f"last success {human_duration(success_age_seconds)} ago"
    elif active_age_seconds is not None and active_age_seconds <= 900:
        status = "slow"
        summary = f"long active attempt for {human_duration(active_age_seconds)}"
    elif success_age_seconds is not None and success_age_seconds <= 900:
        status = "slow"
        summary = f"no new success for {human_duration(success_age_seconds)}"
    elif last_event_age_seconds is not None and last_event_age_seconds <= 1800:
        status = "quiet"
        summary = f"last log event {human_duration(last_event_age_seconds)} ago"
    else:
        status = "stalled"
        summary = "no recent cache activity"

    return {
        "status": status,
        "summary": summary,
        "active_age_seconds": active_age_seconds,
        "success_age_seconds": success_age_seconds,
        "last_event_age_seconds": last_event_age_seconds,
    }


def combine_activity_health(logs: dict[str, dict[str, Any]], now_epoch: float) -> dict[str, Any]:
    latest_active: dict[str, Any] | None = None
    latest_success: dict[str, Any] | None = None
    latest_event: dict[str, Any] | None = None

    for log in logs.values():
        active = log.get("active_attempt")
        if active and (latest_active is None or float(active.get("timestamp", 0.0) or 0.0) > float(latest_active.get("timestamp", 0.0) or 0.0)):
            latest_active = active
        success = log.get("last_success")
        if success and (latest_success is None or float(success.get("timestamp", 0.0) or 0.0) > float(latest_success.get("timestamp", 0.0) or 0.0)):
            latest_success = success
        event = log.get("last_event")
        if event and (latest_event is None or float(event.get("timestamp", 0.0) or 0.0) > float(latest_event.get("timestamp", 0.0) or 0.0)):
            latest_event = event

    active_age_seconds = event_age_seconds(latest_active, now_epoch)
    success_age_seconds = event_age_seconds(latest_success, now_epoch)
    last_event_age_seconds = event_age_seconds(latest_event, now_epoch)

    if active_age_seconds is not None and active_age_seconds <= 300:
        status = "moving"
        summary = f"active cache call running for {human_duration(active_age_seconds)}"
    elif success_age_seconds is not None and success_age_seconds <= 180:
        status = "moving"
        summary = f"new cache write {human_duration(success_age_seconds)} ago"
    elif active_age_seconds is not None and active_age_seconds <= 900:
        status = "slow"
        summary = f"current cache call has been open for {human_duration(active_age_seconds)}"
    elif success_age_seconds is not None and success_age_seconds <= 900:
        status = "slow"
        summary = f"last cache write was {human_duration(success_age_seconds)} ago"
    elif last_event_age_seconds is not None and last_event_age_seconds <= 1800:
        status = "quiet"
        summary = f"last cache log event was {human_duration(last_event_age_seconds)} ago"
    else:
        status = "stalled"
        summary = "no recent cache activity detected"

    return {
        "status": status,
        "summary": summary,
        "active_age_seconds": active_age_seconds,
        "success_age_seconds": success_age_seconds,
        "last_event_age_seconds": last_event_age_seconds,
        "latest_active": latest_active,
        "latest_success": latest_success,
        "latest_event": latest_event,
    }


def log_watch_event(stage: str, event: str, message: str) -> None:
    payload = {
        "timestamp": round(time.time(), 3),
        "formatted_time": format_timestamp(time.time()),
        "event": event,
        "message": message,
    }
    with monitor_watch_log_path(stage).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def build_payload(stage: str, seeds: list[int], pid: int) -> dict[str, Any]:
    now = time.time()
    panels = load_stage_panels(stage)
    matrix: dict[str, dict[str, dict[str, Any]]] = {"base": {}, "psu": {}}
    panel_rows: list[dict[str, Any]] = []

    for panel in panels:
        panel_row = {
            "panel_id": panel["panel_id"],
            "total_items": len(panel["item_ids"]),
            "base": {},
            "psu": {},
        }
        for method in ("base", "psu"):
            cells = []
            matrix[method][panel["panel_id"]] = {}
            for seed in seeds:
                cell = summarize_cell(panel, method, seed)
                matrix[method][panel["panel_id"]][str(seed)] = cell
                panel_row[method][str(seed)] = cell
                cells.append(cell)
            panel_row[method]["aggregate"] = aggregate_cells(cells)
        panel_rows.append(panel_row)

    method_summary = {}
    for method in ("base", "psu"):
        method_cells = [
            matrix[method][panel["panel_id"]][str(seed)]
            for panel in panels
            for seed in seeds
        ]
        method_summary[method] = aggregate_cells(method_cells)

    overall = aggregate_cells([method_summary["base"], method_summary["psu"]])
    process_status = probe_process(pid)

    halu_log = summarize_log(OUTPUT_DIR / "external_benchmark_halumem_cache_summarizer_log.jsonl")
    locomo_log = summarize_log(OUTPUT_DIR / "external_benchmark_locomo_cache_summarizer_log.jsonl")
    logs = {"halumem": halu_log, "locomo": locomo_log}
    log_health = {name: assess_log_health(log, now) for name, log in logs.items()}
    activity_health = combine_activity_health(logs, now)
    eta_seconds = estimate_eta_seconds(overall["total_passes"] - overall["completed_passes"], [halu_log, locomo_log])

    stage_outputs = {
        "json": str(OUTPUT_DIR / f"expanded_benchmark_stage_{stage}.json"),
        "summary": str(OUTPUT_DIR / f"expanded_benchmark_stage_{stage}.md"),
        "traces": str(OUTPUT_DIR / f"expanded_benchmark_stage_{stage}_traces.md"),
    }
    stage_output_status = {key: Path(path).exists() for key, path in stage_outputs.items()}
    return {
        "stage": stage,
        "stage_description": staged.STAGE_SPECS[stage]["description"],
        "generated_at_epoch": round(now, 3),
        "generated_at": format_timestamp(now),
        "seeds": seeds,
        "max_passes": MAX_PASSES,
        "n_values": staged.N_VALUES,
        "process": process_status,
        "overall": overall,
        "method_summary": method_summary,
        "panel_rows": panel_rows,
        "logs": logs,
        "log_health": log_health,
        "activity_health": activity_health,
        "eta_seconds": eta_seconds,
        "eta_human": human_duration(eta_seconds),
        "stage_outputs": stage_outputs,
        "stage_output_status": stage_output_status,
        "watch_log_path": str(monitor_watch_log_path(stage)),
        "monitor_note": "Progress counts the actual expensive cache-building work: one shared base cache plus one shared PSU scaffold cache, not duplicated architecture cells.",
    }


def progress_bar(ratio: float) -> str:
    width = 18
    filled = max(0, min(width, round(ratio * width)))
    return "█" * filled + "░" * (width - filled)


def build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Expanded Benchmark {payload['stage']} Monitor",
        "",
        payload["stage_description"],
        "",
        f"- updated_at: `{payload['generated_at']}`",
        f"- seeds: `{payload['seeds']}`",
        f"- process_alive: `{payload['process']['alive']}`",
        f"- process_pid: `{payload['process']['pid']}`",
        f"- process_elapsed: `{payload['process']['elapsed']}`",
        f"- heuristic_eta: `{payload['eta_human']}`",
        "",
        "## Overall",
        "",
        f"- item_units: `{payload['overall']['completed_items']}/{payload['overall']['total_items']}`",
        f"- pass_units: `{payload['overall']['completed_passes']}/{payload['overall']['total_passes']}`",
        f"- note: {payload['monitor_note']}",
        "",
        "## Method Summary",
        "",
        "| Method | Completed item-units | Completed passes |",
        "|---|---:|---:|",
    ]
    for method in ("base", "psu"):
        row = payload["method_summary"][method]
        lines.append(
            f"| {method} | {row['completed_items']}/{row['total_items']} | {row['completed_passes']}/{row['total_passes']} |"
        )
    lines.extend(["", "## Panels", "", "| Panel | Method | Seed | Item units | Pass units | Latest partial | Next unstarted |", "|---|---|---:|---:|---:|---|---|"])
    for panel in payload["panel_rows"]:
        for method in ("base", "psu"):
            for seed in payload["seeds"]:
                cell = panel[method][str(seed)]
                latest_partial = "-"
                if cell["latest_partial"] is not None:
                    latest_partial = f"{cell['latest_partial']['item_id']} ({cell['latest_partial']['pass_count']}/{payload['max_passes']})"
                next_unstarted = cell["next_unstarted"] or "-"
                lines.append(
                    f"| {panel['panel_id']} | {method} | {seed} | "
                    f"{cell['completed_items']}/{cell['total_items']} | "
                    f"{cell['completed_passes']}/{cell['total_passes']} | "
                    f"{latest_partial} | {next_unstarted} |"
                )
    return "\n".join(lines) + "\n"


def rate_badge(ratio: float) -> str:
    percent = ratio * 100.0
    return f"{percent:.1f}%"


def render_cell(cell: dict[str, Any], max_passes: int) -> str:
    latest = "-"
    if cell["latest_partial"] is not None:
        latest = f"{cell['latest_partial']['item_id']} ({cell['latest_partial']['pass_count']}/{max_passes})"
    next_unstarted = cell["next_unstarted"] or "-"
    return (
        f"<div><strong>{cell['completed_items']}/{cell['total_items']}</strong> item-units</div>"
        f"<div>{progress_bar(cell['pass_completion_rate'])} {rate_badge(cell['pass_completion_rate'])}</div>"
        f"<div class='subtle'>passes {cell['completed_passes']}/{cell['total_passes']}</div>"
        f"<div class='subtle'>latest partial: {html.escape(latest)}</div>"
        f"<div class='subtle'>next: {html.escape(next_unstarted)}</div>"
    )


def render_log_card(label: str, payload: dict[str, Any]) -> str:
    if not payload["exists"]:
        return f"<div class='card'><h3>{html.escape(label)}</h3><p class='subtle'>log missing</p></div>"
    active = payload["active_attempt"]
    last_success = payload["last_success"]
    last_event = payload["last_event"]
    lines = [f"<div class='card'><h3>{html.escape(label)}</h3>"]
    if active:
        lines.append(
            "<p><strong>running:</strong> "
            + html.escape(active.get("cache_key", "unknown"))
            + "</p>"
        )
    else:
        lines.append("<p><strong>running:</strong> none detected in recent window</p>")
    if last_success:
        lines.append(
            "<p><strong>last success:</strong> "
            + html.escape(last_success.get("cache_key", "unknown"))
            + f" ({last_success.get('duration_s', '?')}s)"
            + "</p>"
        )
    if payload.get("success_age_seconds") is not None:
        lines.append(
            f"<p class='subtle'><strong>success age:</strong> {html.escape(human_duration(payload['success_age_seconds']) or 'unknown')}</p>"
        )
    if payload.get("active_age_seconds") is not None:
        lines.append(
            f"<p class='subtle'><strong>active age:</strong> {html.escape(human_duration(payload['active_age_seconds']) or 'unknown')}</p>"
        )
    if last_event:
        lines.append(
            "<p class='subtle'><strong>last event:</strong> "
            + html.escape(last_event.get("event", "unknown"))
            + " @ "
            + html.escape(format_timestamp(last_event.get("timestamp")) or "unknown")
            + "</p>"
        )
    if payload["recent_median_duration_s"] is not None:
        lines.append(
            f"<p class='subtle'><strong>recent median duration:</strong> {payload['recent_median_duration_s']}s</p>"
        )
    lines.append("</div>")
    return "".join(lines)


def chip_class(status: str) -> str:
    if status == "moving":
        return "chip ok"
    if status in {"slow", "quiet"}:
        return "chip warn"
    return "chip stale"


def build_html(payload: dict[str, Any], refresh_seconds: int) -> str:
    process = payload["process"]
    process_status = "alive" if process["alive"] else "not detected"
    process_line = f"PID {process['pid']} | elapsed {process['elapsed']}" if process["pid"] else "PID unavailable"
    if process.get("error"):
        process_line = f"{process_line} | ps error: {process['error']}"
    stage_outputs_ready = all(payload["stage_output_status"].values())
    generated_at_epoch_ms = int(float(payload["generated_at_epoch"]) * 1000)
    activity_health = payload["activity_health"]
    cards = []
    cards.append(
        "<div class='metric-card'>"
        "<div class='label'>Overall expensive work</div>"
        f"<div class='value'>{payload['overall']['completed_passes']}/{payload['overall']['total_passes']}</div>"
        f"<div class='subtle'>{rate_badge(payload['overall']['pass_completion_rate'])} of pass units</div>"
        "</div>"
    )
    cards.append(
        "<div class='metric-card'>"
        "<div class='label'>Base cache</div>"
        f"<div class='value'>{payload['method_summary']['base']['completed_items']}/{payload['method_summary']['base']['total_items']}</div>"
        f"<div class='subtle'>{rate_badge(payload['method_summary']['base']['item_completion_rate'])} item units</div>"
        "</div>"
    )
    cards.append(
        "<div class='metric-card'>"
        "<div class='label'>PSU cache</div>"
        f"<div class='value'>{payload['method_summary']['psu']['completed_items']}/{payload['method_summary']['psu']['total_items']}</div>"
        f"<div class='subtle'>{rate_badge(payload['method_summary']['psu']['item_completion_rate'])} item units</div>"
        "</div>"
    )
    cards.append(
        "<div class='metric-card'>"
        "<div class='label'>Heuristic ETA</div>"
        f"<div class='value'>{html.escape(payload['eta_human'] or 'unknown')}</div>"
        f"<div class='subtle'>main artifacts ready: {stage_outputs_ready}</div>"
        "</div>"
    )
    cards.append(
        "<div class='metric-card'>"
        "<div class='label'>Cache Heartbeat</div>"
        f"<div class='value'>{html.escape(activity_health['status'])}</div>"
        f"<div class='subtle'>{html.escape(activity_health['summary'])}</div>"
        "</div>"
    )
    cards.append(
        "<div class='metric-card'>"
        "<div class='label'>Watch Log</div>"
        f"<div class='value'>{html.escape(Path(payload['watch_log_path']).name)}</div>"
        f"<div class='subtle'>{html.escape(payload['watch_log_path'])}</div>"
        "</div>"
    )

    table_rows: list[str] = []
    for panel in payload["panel_rows"]:
        for method in ("base", "psu"):
            seed_cells = "".join(
                f"<td>{render_cell(panel[method][str(seed)], payload['max_passes'])}</td>"
                for seed in payload["seeds"]
            )
            table_rows.append(
                "<tr>"
                f"<td>{html.escape(panel['panel_id'])}</td>"
                f"<td>{method}</td>"
                f"<td>{panel[method]['aggregate']['completed_items']}/{panel[method]['aggregate']['total_items']}</td>"
                f"{seed_cells}"
                "</tr>"
            )

    output_rows = "".join(
        "<tr>"
        f"<td>{html.escape(key)}</td>"
        f"<td>{html.escape(path)}</td>"
        f"<td>{'ready' if ready else 'pending'}</td>"
        "</tr>"
        for key, path, ready in (
            (key, payload["stage_outputs"][key], payload["stage_output_status"][key])
            for key in ("json", "summary", "traces")
        )
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="{refresh_seconds}">
  <title>Expanded Benchmark {html.escape(payload['stage'])} Monitor</title>
  <style>
    :root {{
      --bg: #f6f3ec;
      --panel: #fffdf8;
      --ink: #1b1b18;
      --muted: #6b6a63;
      --line: #d7d1c5;
      --accent: #0f766e;
      --accent-soft: #d7f3ef;
      --warn: #8a3b12;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 28px;
      background:
        radial-gradient(circle at top left, #fdf4d9 0, transparent 30%),
        radial-gradient(circle at top right, #d7f3ef 0, transparent 25%),
        var(--bg);
      color: var(--ink);
      font: 15px/1.5 "Avenir Next", "Helvetica Neue", sans-serif;
    }}
    h1, h2, h3 {{ margin: 0 0 10px; }}
    p {{ margin: 0 0 10px; }}
    .wrap {{ max-width: 1380px; margin: 0 auto; }}
    .hero {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 24px;
      box-shadow: 0 18px 36px rgba(27, 27, 24, 0.05);
      margin-bottom: 18px;
    }}
    .eyebrow {{
      display: inline-block;
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 8px;
    }}
    .subtle {{ color: var(--muted); font-size: 13px; }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin: 18px 0 8px;
    }}
    .heartbeat {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      margin-top: 12px;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      background: #f4efe4;
    }}
    .chip.ok {{
      color: #0f766e;
      background: #d7f3ef;
      border-color: #99ddd5;
    }}
    .chip.warn {{
      color: #9a6700;
      background: #fff1cc;
      border-color: #f0d48b;
    }}
    .chip.stale {{
      color: #b42318;
      background: #fee4e2;
      border-color: #f7b4ae;
    }}
    .metric-card, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 16px;
    }}
    .metric-card {{
      background: linear-gradient(180deg, var(--panel), var(--accent-soft));
    }}
    .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; }}
    .value {{ font-size: 28px; font-weight: 700; margin: 6px 0; }}
    .section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 20px;
      margin-bottom: 18px;
      box-shadow: 0 18px 36px rgba(27, 27, 24, 0.04);
    }}
    .log-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      border-top: 1px solid var(--line);
      padding: 12px 10px;
      vertical-align: top;
      text-align: left;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    code {{
      background: rgba(15, 118, 110, 0.08);
      padding: 2px 6px;
      border-radius: 999px;
      font-size: 12px;
    }}
    .warn {{
      color: var(--warn);
      font-weight: 600;
    }}
    @media (max-width: 1120px) {{
      .metric-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .log-grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 720px) {{
      body {{ padding: 14px; }}
      .metric-grid {{ grid-template-columns: 1fr; }}
      .hero, .section {{ padding: 16px; border-radius: 16px; }}
      .value {{ font-size: 22px; }}
      table, thead, tbody, th, td, tr {{ display: block; }}
      thead {{ display: none; }}
      tr {{ border-top: 1px solid var(--line); padding: 8px 0; }}
      td {{ border-top: none; padding: 6px 0; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <div class="eyebrow">Expanded Benchmark Live Monitor</div>
      <h1>Stage: {html.escape(payload['stage'])}</h1>
      <p>{html.escape(payload['stage_description'])}</p>
      <p><strong>Updated:</strong> {html.escape(payload['generated_at'])} | <strong>Auto refresh:</strong> every {refresh_seconds}s</p>
      <p><strong>Process:</strong> {process_status} | {html.escape(process_line)}</p>
      <div class="heartbeat">
        <span id="heartbeat-chip" class="chip ok">fresh</span>
        <span id="heartbeat-text" class="subtle">render age 0s</span>
        <span class="{chip_class(activity_health['status'])}">{html.escape(activity_health['status'])}</span>
        <span class="subtle">{html.escape(activity_health['summary'])}</span>
      </div>
      <p class="subtle">{html.escape(payload['monitor_note'])}</p>
      <div class="metric-grid">
        {''.join(cards)}
      </div>
    </section>

    <section class="section">
      <h2>Per-Panel Progress</h2>
      <p class="subtle">Each seed cell shows completed item-units, pass coverage, the latest partially built item, and the next untouched item.</p>
      <table>
        <thead>
          <tr>
            <th>Panel</th>
            <th>Method</th>
            <th>Aggregate</th>
            {''.join(f'<th>Seed {seed}</th>' for seed in payload['seeds'])}
          </tr>
        </thead>
        <tbody>
          {''.join(table_rows)}
        </tbody>
      </table>
    </section>

    <section class="section">
      <h2>Recent Activity</h2>
      <div class="log-grid">
        {render_log_card('HaluMem cache log', payload['logs']['halumem'])}
        {render_log_card('LoCoMo / LongMemEval cache log', payload['logs']['locomo'])}
      </div>
    </section>

    <section class="section">
      <h2>Stage Output Status</h2>
      <table>
        <thead>
          <tr>
            <th>Artifact</th>
            <th>Path</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {output_rows}
        </tbody>
      </table>
      <p class="subtle">If these stay pending after the process stops, the run likely ended early and needs inspection.</p>
    </section>
  </div>
  <script>
    const generatedAtMs = {generated_at_epoch_ms};
    const chip = document.getElementById("heartbeat-chip");
    const text = document.getElementById("heartbeat-text");

    function updateHeartbeat() {{
      const ageSeconds = Math.max(0, Math.floor((Date.now() - generatedAtMs) / 1000));
      let label = "fresh";
      let chipClass = "chip ok";
      if (ageSeconds >= 300) {{
        label = "stale";
        chipClass = "chip stale";
      }} else if (ageSeconds >= 120) {{
        label = "lagging";
        chipClass = "chip warn";
      }}
      chip.textContent = label;
      chip.className = chipClass;
      text.textContent = `render age ${{ageSeconds}}s`;
    }}

    updateHeartbeat();
    window.setInterval(updateHeartbeat, 1000);
  </script>
</body>
</html>
"""


def write_outputs(payload: dict[str, Any], refresh_seconds: int) -> None:
    monitor_json_path(payload["stage"]).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    monitor_html_path(payload["stage"]).write_text(build_html(payload, refresh_seconds), encoding="utf-8")
    monitor_md_path(payload["stage"]).write_text(build_markdown(payload), encoding="utf-8")


def run_once(args: argparse.Namespace) -> dict[str, Any]:
    payload = build_payload(args.stage, selected_seeds(args.stage, args.seeds), args.pid)
    write_outputs(payload, args.refresh_seconds)
    return payload


def main() -> None:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not args.watch:
        run_once(args)
        return

    log_watch_event(args.stage, "watch_started", f"interval={args.interval}s refresh={args.refresh_seconds}s pid={args.pid}")
    while True:
        try:
            payload = run_once(args)
            log_watch_event(
                args.stage,
                "watch_tick",
                f"generated_at={payload['generated_at']} completed_passes={payload['overall']['completed_passes']}/{payload['overall']['total_passes']} activity={payload['activity_health']['status']}",
            )
        except KeyboardInterrupt:
            log_watch_event(args.stage, "watch_stopped", "KeyboardInterrupt")
            break
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            log_watch_event(args.stage, "watch_error", message)
            log_watch_event(args.stage, "watch_traceback", traceback.format_exc())
            time.sleep(max(5, args.interval))
            continue
        process = payload["process"]
        stage_outputs_ready = all(payload["stage_output_status"].values())
        if args.stop_when_finished and process["alive"] is False and stage_outputs_ready:
            log_watch_event(args.stage, "watch_finished", "Process gone and final stage artifacts are ready.")
            break
        time.sleep(max(5, args.interval))


if __name__ == "__main__":
    main()
