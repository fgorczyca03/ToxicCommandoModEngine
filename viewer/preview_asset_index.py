#!/usr/bin/env python3
"""Simple metadata viewer for packed asset index JSON.

Reads the JSON output from extractor/scan_packed_assets.py and prints
an easy-to-read table in the terminal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview packed asset metadata.")
    parser.add_argument("index_json", type=Path, help="Path to metadata JSON file.")
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum rows to display (default: 50).",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = args.index_json.expanduser().resolve()

    data = json.loads(source.read_text(encoding="utf-8"))
    rows = data[: args.limit]

    print(f"Loaded {len(data)} packed assets from {source}")
    print(f"Showing first {len(rows)} entries")
    print("-" * 100)
    print(f"{'type':<10} {'size_bytes':>12}  relative_path")
    print("-" * 100)
    for item in rows:
        print(f"{item['file_type']:<10} {item['size_bytes']:>12}  {item['relative_path']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
