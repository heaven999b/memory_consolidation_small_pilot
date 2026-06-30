from __future__ import annotations

import json
from pathlib import Path
from typing import Any


JSON_PATH = "outputs/v3_halumem_dataset_preflight.json"
SUMMARY_PATH = "outputs/v3_halumem_dataset_preflight.md"
OFFICIAL_SOURCE_URL = "https://huggingface.co/datasets/IAAR-Shanghai/HaluMem"


def rel(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def file_size_mb(path: Path) -> float | None:
    if not path.exists() or not path.is_file():
        return None
    return round(path.stat().st_size / (1024 * 1024), 2)


def line_count(path: Path) -> int | None:
    if not path.exists() or not path.is_file():
        return None
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        return sum(1 for _ in handle)


def build_payload(repo_root: Path) -> dict[str, Any]:
    expected_path = (
        repo_root
        / "benchmarks"
        / "halumem"
        / "official_repo"
        / "data"
        / "HaluMem-Medium.jsonl"
    )
    data_dir = expected_path.parent
    official_readme = repo_root / "benchmarks" / "halumem" / "official_repo" / "README.md"
    eval_readme = repo_root / "benchmarks" / "halumem" / "official_repo" / "eval" / "README.md"

    candidates = sorted(
        path for path in repo_root.rglob("*HaluMem*") if path.is_file() and path.suffix in {".jsonl", ".json"}
    )
    candidate_rows = [
        {
            "path": rel(repo_root, path),
            "size_mb": file_size_mb(path),
        }
        for path in candidates
    ]

    readme_text = official_readme.read_text(encoding="utf-8", errors="ignore") if official_readme.exists() else ""
    status = "ready" if expected_path.exists() else "partial"
    return {
        "repo_root": ".",
        "description": "Canonical-path preflight for the HaluMem-Medium file required by TierMem and the mirrored official eval harness.",
        "status": status,
        "expected_path": rel(repo_root, expected_path),
        "expected_filename": expected_path.name,
        "expected_present": expected_path.exists(),
        "expected_size_mb": file_size_mb(expected_path),
        "expected_line_count": line_count(expected_path),
        "official_source_url": OFFICIAL_SOURCE_URL,
        "official_readme_present": official_readme.exists(),
        "eval_readme_present": eval_readme.exists(),
        "license_signal": "CC-BY-NC-ND-4.0" if "CC-BY-NC-ND-4.0" in readme_text else "missing",
        "candidate_count": len(candidate_rows),
        "candidates": candidate_rows,
        "next_action": (
            "Dataset already present at the canonical path."
            if expected_path.exists()
            else (
                "Download HaluMem-Medium from the official Hugging Face dataset and place it at "
                f"{rel(repo_root, expected_path)}."
            )
        ),
        "copy_hint": (
            None
            if expected_path.exists()
            else f"cp /path/to/HaluMem-Medium.jsonl '{expected_path}'"
        ),
        "data_dir_exists": data_dir.exists(),
    }


def build_summary(payload: dict[str, Any]) -> str:
    lines = [
        "# V3 HaluMem Dataset Preflight",
        "",
        payload["description"],
        "",
        f"- status: `{payload['status']}`",
        f"- expected path: `{payload['expected_path']}`",
        f"- expected present: `{payload['expected_present']}`",
        f"- expected size MB: `{payload['expected_size_mb']}`",
        f"- expected line count: `{payload['expected_line_count']}`",
        f"- official source: {payload['official_source_url']}",
        f"- license signal: `{payload['license_signal']}`",
        f"- workspace candidate count: `{payload['candidate_count']}`",
        "",
        "## Candidate Files",
        "",
        "| Path | Size MB |",
        "|---|---:|",
    ]
    for row in payload["candidates"]:
        lines.append(f"| `{row['path']}` | {row['size_mb']} |")
    if not payload["candidates"]:
        lines.append("| none found | - |")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            f"- {payload['next_action']}",
        ]
    )
    if payload["copy_hint"]:
        lines.append(f"- copy hint: `{payload['copy_hint']}`")
    return "\n".join(lines)


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    payload = build_payload(repo_root)
    (repo_root / JSON_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (repo_root / SUMMARY_PATH).write_text(build_summary(payload) + "\n", encoding="utf-8")
    print(f"[v3-halumem-preflight] wrote {repo_root / JSON_PATH}")
    print(f"[v3-halumem-preflight] wrote {repo_root / SUMMARY_PATH}")


if __name__ == "__main__":
    main()
