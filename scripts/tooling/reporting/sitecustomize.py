from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
CANDIDATES = [
    REPO_ROOT,
    SCRIPTS_ROOT / "core",
    SCRIPTS_ROOT / "run",
    SCRIPTS_ROOT / "build",
    SCRIPTS_ROOT / "freeze",
    SCRIPTS_ROOT / "analysis",
    SCRIPTS_ROOT / "watch",
    SCRIPTS_ROOT / "tooling" / "reporting",
]

for candidate in CANDIDATES:
    text = str(candidate)
    if candidate.exists() and text not in sys.path:
        sys.path.insert(0, text)
