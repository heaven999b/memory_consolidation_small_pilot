from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEEK1_TINY_SYNTH_PATH = PROJECT_ROOT / "benchmarks" / "tiny_synth" / "data" / "week1_tiny_synth.json"
WEEK1_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "week1_sanity"
WEEK1_QDRANT_DIR = PROJECT_ROOT / "outputs" / "tiermem_local_qdrant_week1"


@dataclass(frozen=True)
class Week1ArchitecturePreset:
    architecture: str
    route_mode: str
    page_write_mode: str
    max_research_iters: int
    top_k: int
    description: str


WEEK1_ARCHITECTURES: Dict[str, Week1ArchitecturePreset] = {
    "raw_only": Week1ArchitecturePreset(
        architecture="raw_only",
        route_mode="research_only",
        page_write_mode="raw",
        max_research_iters=1,
        top_k=4,
        description="Raw evidence only. No summary-only answer path is allowed.",
    ),
    "summary_only": Week1ArchitecturePreset(
        architecture="summary_only",
        route_mode="summary_only",
        page_write_mode="infer",
        max_research_iters=1,
        top_k=4,
        description="Summary tier only. Answers must come from compact memories.",
    ),
    "summary_plus_raw": Week1ArchitecturePreset(
        architecture="summary_plus_raw",
        route_mode="auto",
        page_write_mode="infer",
        max_research_iters=2,
        top_k=4,
        description="TierMem-style route: start from summaries, escalate to raw only when needed.",
    ),
}


def add_week1_architecture_arg(parser: Any) -> None:
    parser.add_argument(
        "--architecture",
        choices=sorted(WEEK1_ARCHITECTURES.keys()),
        default=None,
        help=(
            "Pinned Week 1 common-memory preset. "
            "raw_only / summary_only / summary_plus_raw override the lower-level route/page-write knobs."
        ),
    )


def get_week1_preset(name: Optional[str]) -> Optional[Week1ArchitecturePreset]:
    if not name:
        return None
    return WEEK1_ARCHITECTURES[name]


def resolve_week1_runtime(args: Any) -> Dict[str, Any]:
    preset = get_week1_preset(getattr(args, "architecture", None))
    if preset is None:
        return {
            "architecture": None,
            "route_mode": getattr(args, "route_mode", "auto"),
            "page_write_mode": getattr(args, "page_write_mode", "raw"),
            "max_research_iters": int(getattr(args, "max_research_iters", 3)),
            "top_k": int(getattr(args, "top_k", 5)),
            "description": "manual_runtime",
        }
    return {
        "architecture": preset.architecture,
        "route_mode": preset.route_mode,
        "page_write_mode": preset.page_write_mode,
        "max_research_iters": preset.max_research_iters,
        "top_k": preset.top_k,
        "description": preset.description,
    }


def week1_run_slug(architecture: Optional[str], consolidation_passes: int) -> str:
    label = architecture or "manual_runtime"
    return f"{label}_n{consolidation_passes}"
