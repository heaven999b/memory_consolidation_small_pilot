from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


TEXT_SUFFIXES = {".md", ".py", ".json", ".html", ".txt", ".yml", ".yaml"}
SKIP_PARTS = {".git", "__pycache__", ".venv", ".venv312", ".venv_tiermem_v2"}
PATH_PATTERNS = ["/Users/", "\\Users\\"]
SKIP_SUBSTRINGS = [
    "study/",
    "reviews/",
    "AGENT_MEMORY_METHOD_SUMMARY.md",
    "state/v2_mac_feasibility_report.md",
    "benchmarks/halumem/official_repo/data/",
    "benchmarks/locomo/locomo_official/data/",
    "benchmarks/locomo/longmemeval_official/data/",
    "outputs/actual_",
    "outputs/expanded_",
    "outputs/external_benchmark_halumem_cache/",
    "outputs/external_benchmark_locomo_cache/",
    "outputs/external_benchmark_halumem_cache_summarizer_log.jsonl",
    "outputs/external_benchmark_locomo_cache_summarizer_log.jsonl",
    "outputs/halumem_official_baseline_matrix_status.json",
    "outputs/halumem_official_baseline_matrix_status.md",
    "outputs/tiermem_local_mem0/",
    "outputs/v3_hygiene_audit.json",
    "outputs/v3_hygiene_audit.md",
    "run_v3_hygiene_audit.py",
]


@dataclass
class LeakRecord:
    path: str
    hit_count: int
    sample: str


def should_scan(path: Path) -> bool:
    if any(part in SKIP_PARTS for part in path.parts):
        return False
    relative_text = path.as_posix()
    if any(fragment in relative_text for fragment in SKIP_SUBSTRINGS):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES


def find_absolute_path_leaks(repo_root: Path) -> list[LeakRecord]:
    leaks: list[LeakRecord] = []
    for path in repo_root.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        hit_count = sum(text.count(pattern) for pattern in PATH_PATTERNS)
        if hit_count <= 0:
            continue
        sample = ""
        for line in text.splitlines():
            if any(pattern in line for pattern in PATH_PATTERNS):
                sample = line.strip()
                break
        leaks.append(
            LeakRecord(
                path=str(path.relative_to(repo_root)),
                hit_count=hit_count,
                sample=sample[:240],
            )
        )
    return sorted(leaks, key=lambda item: (-item.hit_count, item.path))


def outputs_inventory(repo_root: Path) -> dict[str, int]:
    outputs_dir = repo_root / "outputs"
    total_bytes = 0
    total_files = 0
    if outputs_dir.exists():
        for path in outputs_dir.rglob("*"):
            if path.is_file():
                total_files += 1
                total_bytes += path.stat().st_size
    return {
        "file_count": total_files,
        "total_bytes": total_bytes,
    }


def main() -> None:
    repo_root = Path(__file__).resolve().parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    leaks = find_absolute_path_leaks(repo_root)
    inventory = outputs_inventory(repo_root)
    payload = {
        "repo_root": ".",
        "absolute_path_leaks": [asdict(record) for record in leaks],
        "outputs_inventory": inventory,
        "recommendations": [
            "Strip /Users/ absolute paths from README, monitor HTML, and release-facing markdown before submission.",
            "Keep only headline CSV/MD artifacts in the public release surface if the outputs tree grows too large.",
            "Treat outputs/*.json and outputs/*.html as reviewer-facing only after a double-blind pass.",
        ],
    }

    json_path = outputs_dir / "v3_hygiene_audit.json"
    md_path = outputs_dir / "v3_hygiene_audit.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# V3 Hygiene Audit",
        "",
        "| Check | Value |",
        "|---|---|",
        f"| absolute path leak files | `{len(leaks)}` |",
        f"| outputs file count | `{inventory['file_count']}` |",
        f"| outputs total bytes | `{inventory['total_bytes']}` |",
        "",
        "## Absolute Path Leaks",
        "",
        "| Path | Hits | Sample |",
        "|---|---|---|",
    ]
    for record in leaks[:100]:
        sample = record.sample.replace("|", "\\|")
        lines.append(f"| {record.path} | `{record.hit_count}` | {sample} |")
    if not leaks:
        lines.append("| none | `0` | no `/Users/` style leaks detected in scanned text files |")
    lines.extend(
        [
            "",
            "## Recommendations",
            "",
            "- Strip `/Users/` absolute paths from submission-facing docs and HTML before any external release.",
            "- Treat the current outputs tree as an internal working surface until a double-blind cleanup pass is complete.",
            "- Prefer the new V3 reports and snapshots over older legacy packet artifacts when preparing paper-facing materials.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[v3-hygiene] wrote {json_path}")
    print(f"[v3-hygiene] wrote {md_path}")


if __name__ == "__main__":
    main()
