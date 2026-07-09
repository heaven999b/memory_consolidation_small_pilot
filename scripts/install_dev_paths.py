#!/usr/bin/env python3
"""One-time path installer for the reorganized layout.

Background: the repo was reorganized so framework modules live under
``scripts/core`` and run scripts under ``scripts/run``, but the scripts still use
flat, bare imports (``import safety_metrics`` etc.). Rather than edit every
script, this writes a single ``.pth`` file into the *active* interpreter's
site-packages that puts the needed directories on ``sys.path`` at startup. A
``.pth`` is read by ``site`` for every interpreter launch (including the
subprocesses that the RQ launchers spawn), so no per-script edits or PYTHONPATH
exports are needed.

Run ONCE per virtualenv, e.g.:

    .venv_tiermem_v2/bin/python scripts/install_dev_paths.py

Re-run it after recreating the venv or moving the repo.
"""
from __future__ import annotations

import sysconfig
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "scripts" / "core",
    ROOT / "scripts" / "run",
    ROOT,
    ROOT.parent / "tiermem_upstream",
]


def main() -> int:
    site_packages = Path(sysconfig.get_paths()["purelib"])
    pth = site_packages / "_mcp_repo_paths.pth"
    lines = [str(p) for p in TARGETS if p.exists()]
    pth.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {pth}")
    for p in TARGETS:
        print(("  ok   " if p.exists() else "  MISS ") + str(p))
    print("\nDone. New python processes for this venv now resolve the flat imports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
