#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

from build_rq3_readtime_dashboard_data import DEFAULT_OUTPUT_DIR, DEFAULT_STATE_DIR, build_snapshot


def main() -> int:
    p = argparse.ArgumentParser(description="Refresh the RQ3 dashboard data until the sweep finishes.")
    p.add_argument("--run-tag", required=True)
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    p.add_argument("--interval-sec", type=int, default=20)
    args = p.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve()
    state_dir.mkdir(parents=True, exist_ok=True)
    out_path = state_dir / f"{args.run_tag}_dashboard_data.json"

    while True:
      snapshot = build_snapshot(args.run_tag, output_dir, state_dir)
      out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
      counts = snapshot["counts"]
      print(
          f"[{datetime.now().isoformat(timespec='seconds')}] "
          f"dashboard refreshed: completed={counts['completed_jobs']} "
          f"running={counts['running_jobs']} pending={counts['pending_jobs']}"
      )
      if counts["running_jobs"] == 0 and counts["pending_jobs"] == 0:
          break
      time.sleep(args.interval_sec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
