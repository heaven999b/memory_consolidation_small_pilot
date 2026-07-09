#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Clone a suite JSON and prefix every item id.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--prefix", required=True)
    args = ap.parse_args()

    in_path = Path(args.input).expanduser().resolve()
    out_path = Path(args.output).expanduser().resolve()
    data = json.loads(in_path.read_text(encoding="utf-8"))

    cloned = dict(data)
    cloned["suite_id"] = f"{data.get('suite_id', in_path.stem)}_{args.prefix.rstrip('_')}"

    items = []
    for item in data.get("items", []):
        row = dict(item)
        row["id"] = f"{args.prefix}{item['id']}"
        items.append(row)
    cloned["items"] = items

    out_path.write_text(json.dumps(cloned, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "input": str(in_path),
        "output": str(out_path),
        "prefix": args.prefix,
        "n_items": len(items),
        "suite_id": cloned["suite_id"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
