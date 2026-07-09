#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from week1_surface import WEEK1_OUTPUT_DIR, WEEK1_QDRANT_DIR, week1_run_slug

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional convenience path
    load_dotenv = None


PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = PROJECT_ROOT / "configs" / "week1"
DEFAULT_PYTHON = PROJECT_ROOT / ".venv_tiermem_v2" / "bin" / "python"


def _load_local_dotenv() -> None:
    for path in (PROJECT_ROOT / ".env.v3", PROJECT_ROOT / ".env"):
        if not path.exists():
            continue
        if load_dotenv is not None:
            load_dotenv(path)
            continue
        for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            os.environ.setdefault(key, value)


def _openai_ready() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def _python_bin() -> Path:
    return DEFAULT_PYTHON if DEFAULT_PYTHON.exists() else Path(sys.executable)


def _config_paths() -> List[Path]:
    return sorted(CONFIG_DIR.glob("*.json"))


def _load_config(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_run_id(architecture: str, passes: int, run_tag: str | None = None) -> str:
    prefix = f"{run_tag}_" if run_tag else ""
    return f"{prefix}week1_tiny_synth_{week1_run_slug(architecture, passes)}"


def _build_common_args(
    config: Dict[str, Any],
    passes: int,
    *,
    output_dir: Path,
    qdrant_path: Path,
) -> List[str]:
    return [
        "--benchmark",
        str(config["benchmark"]),
        "--architecture",
        str(config["architecture"]),
        "--consolidation-passes",
        str(passes),
        "--top-k",
        str(config["top_k"]),
        "--max-research-iters",
        str(config["max_research_iters"]),
        "--page-size",
        str(config["page_size"]),
        "--max-workers",
        str(config["max_workers"]),
        "--write-max-workers",
        str(config["write_max_workers"]),
        "--qa-max-workers",
        str(config["qa_max_workers"]),
        "--output-dir",
        str(output_dir),
        "--qdrant-path",
        str(qdrant_path),
    ]


def _smoke_command(
    config: Dict[str, Any],
    passes: int,
    *,
    output_dir: Path,
    qdrant_path: Path,
    run_tag: str | None,
) -> List[str]:
    return [
        str(_python_bin()),
        str(PROJECT_ROOT / "run_v2_tiermem_local_bridge.py"),
        "--pre-api-smoke",
        "--run-id",
        _build_run_id(str(config["architecture"]), passes, run_tag),
        *_build_common_args(config, passes, output_dir=output_dir, qdrant_path=qdrant_path),
    ]


def _live_command(
    config: Dict[str, Any],
    passes: int,
    *,
    output_dir: Path,
    qdrant_path: Path,
    run_tag: str | None,
) -> List[str]:
    return [
        str(_python_bin()),
        str(PROJECT_ROOT / "run_v2_tiermem_micro_slice.py"),
        "--session-limit",
        str(config["session_limit"]),
        "--qa-limit",
        str(config["qa_limit"]),
        "--run-id",
        _build_run_id(str(config["architecture"]), passes, run_tag),
        *_build_common_args(config, passes, output_dir=output_dir, qdrant_path=qdrant_path),
    ]


def _run_command(cmd: List[str]) -> Dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def _load_micro_report(output_dir: Path, run_id: str) -> Dict[str, Any] | None:
    report_path = output_dir / "micro_reports" / f"{run_id}.json"
    if not report_path.exists():
        return None
    return json.loads(report_path.read_text(encoding="utf-8"))


def _render_matrix_md(mode: str, rows: List[Dict[str, Any]]) -> str:
    lines = [
        "# Week 1 TierMem Sanity Matrix",
        "",
        f"- mode: `{mode}`",
        f"- python: `{_python_bin()}`",
        f"- openai_api_key_present: `{_openai_ready()}`",
        "",
        "| architecture | N | status | returncode | report |",
        "| --- | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        report = row.get("report_json") or "-"
        lines.append(
            f"| {row['architecture']} | {row['consolidation_passes']} | {row['status']} | "
            f"{row['returncode']} | {report} |"
        )
    lines.extend(
        [
            "",
            "## Commands",
            "",
        ]
    )
    for row in rows:
        lines.append(f"- `{ ' '.join(row['command']) }`")
    return "\n".join(lines) + "\n"


def _write_matrix(output_dir: Path, mode: str, rows: List[Dict[str, Any]]) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "mode": mode,
        "python": str(_python_bin()),
        "openai_api_key_present": _openai_ready(),
        "rows": rows,
    }
    json_path = output_dir / "week1_sanity_matrix.json"
    md_path = output_dir / "week1_sanity_matrix.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_render_matrix_md(mode, rows), encoding="utf-8")
    return {"json": str(json_path), "md": str(md_path)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run or preflight the Week 1 TierMem common-memory sanity matrix.")
    parser.add_argument("--mode", choices=["plan", "pre_api_smoke", "run"], default="pre_api_smoke")
    parser.add_argument(
        "--architectures",
        nargs="*",
        default=None,
        help="Optional subset of architecture config basenames, e.g. raw_only summary_only.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(WEEK1_OUTPUT_DIR),
        help="Output directory for matrix artifacts and run outputs.",
    )
    parser.add_argument(
        "--qdrant-path",
        type=str,
        default=str(WEEK1_QDRANT_DIR),
        help="Qdrant local-path storage directory for the run.",
    )
    parser.add_argument(
        "--run-tag",
        type=str,
        default=None,
        help="Optional tag prepended to each generated run_id.",
    )
    return parser


def main() -> int:
    _load_local_dotenv()
    args = build_parser().parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    qdrant_path = Path(args.qdrant_path).expanduser().resolve()
    configs = []
    selected = set(args.architectures or [])
    for path in _config_paths():
        name = path.stem
        if selected and name not in selected:
            continue
        configs.append(_load_config(path))
    if not configs:
        raise SystemExit("No Week 1 configs selected.")

    rows: List[Dict[str, Any]] = []
    for config in configs:
        for passes in config["consolidation_passes"]:
            run_id = _build_run_id(str(config["architecture"]), int(passes), args.run_tag)
            if args.mode == "plan":
                cmd = _live_command(
                    config,
                    int(passes),
                    output_dir=output_dir,
                    qdrant_path=qdrant_path,
                    run_tag=args.run_tag,
                )
                result = {"command": cmd, "returncode": 0, "stdout": "", "stderr": ""}
            elif args.mode == "pre_api_smoke":
                result = _run_command(
                    _smoke_command(
                        config,
                        int(passes),
                        output_dir=output_dir,
                        qdrant_path=qdrant_path,
                        run_tag=args.run_tag,
                    )
                )
            else:
                if not _openai_ready():
                    raise SystemExit("OPENAI_API_KEY is required for --mode run.")
                result = _run_command(
                    _live_command(
                        config,
                        int(passes),
                        output_dir=output_dir,
                        qdrant_path=qdrant_path,
                        run_tag=args.run_tag,
                    )
                )

            report = _load_micro_report(output_dir, run_id) if args.mode == "run" else None
            rows.append(
                {
                    "architecture": config["architecture"],
                    "consolidation_passes": int(passes),
                    "status": "ok" if result["returncode"] == 0 else "failed",
                    "returncode": int(result["returncode"]),
                    "command": result["command"],
                    "stdout_tail": (result["stdout"] or "")[-1000:],
                    "stderr_tail": (result["stderr"] or "")[-1000:],
                    "report_json": str(output_dir / "micro_reports" / f"{run_id}.json") if report else None,
                }
            )

    matrix_paths = _write_matrix(output_dir, args.mode, rows)
    print(
        json.dumps(
            {
                "mode": args.mode,
                "matrix_json": matrix_paths["json"],
                "matrix_md": matrix_paths["md"],
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all(row["returncode"] == 0 for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
