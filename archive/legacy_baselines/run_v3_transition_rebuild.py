from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    legacy_dir = Path(__file__).resolve().parent
    target = legacy_dir / "v3" / "run_v3_transition_rebuild.py"
    subprocess.run([sys.executable, str(target)], cwd=str(legacy_dir.parents[1]), check=True)


if __name__ == "__main__":
    main()
