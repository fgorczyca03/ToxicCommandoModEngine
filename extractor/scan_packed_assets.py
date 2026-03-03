#!/usr/bin/env python3
"""Scan a game installation for packed asset containers and export metadata.

This script is intentionally metadata-only. It does not unpack or copy any
in-game files, which helps keep the workflow compatible with a no-redistribution
modding setup.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

# Common container-like file extensions used by commercial games.
# This list is easy to extend as format research progresses.
DEFAULT_PACKED_EXTENSIONS = {
    ".arc",
    ".assets",
    ".ba2",
    ".big",
    ".bin",
    ".bundle",
    ".cat",
    ".dat",
    ".idx",
    ".pak",
    ".pck",
    ".pk3",
    ".pk4",
    ".rpf",
    ".vpk",
    ".wad",
    ".xp3",
}


@dataclass(frozen=True)
class PackedAsset:
    """Metadata for a potential packed asset file."""

    file_name: str
    relative_path: str
    size_bytes: int
    file_type: str


def parse_extensions(value: str) -> set[str]:
    """Convert a comma-separated extension list to normalized set values."""
    extensions: set[str] = set()
    for item in value.split(","):
        ext = item.strip().lower()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        extensions.add(ext)
    if not extensions:
        raise argparse.ArgumentTypeError("At least one extension is required.")
    return extensions


def detect_type(file_path: Path) -> str:
    """Return a basic file type label inferred from extension."""
    suffix = file_path.suffix.lower()
    return suffix[1:] if suffix.startswith(".") else suffix or "unknown"


def iter_packed_files(root: Path, extensions: set[str]) -> Iterable[PackedAsset]:
    """Yield packed asset metadata for files with matching extensions."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in extensions:
            continue

        stat = path.stat()
        yield PackedAsset(
            file_name=path.name,
            relative_path=str(path.relative_to(root)),
            size_bytes=stat.st_size,
            file_type=detect_type(path),
        )


def build_parser() -> argparse.ArgumentParser:
    """Create command-line interface."""
    parser = argparse.ArgumentParser(
        description=(
            "Scan a game directory for packed asset containers and export "
            "metadata as JSON."
        )
    )
    parser.add_argument(
        "game_dir",
        type=Path,
        help="Path to the game installation directory to scan.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("packed_asset_index.json"),
        help="Output JSON file path (default: packed_asset_index.json).",
    )
    parser.add_argument(
        "--extensions",
        type=parse_extensions,
        default=DEFAULT_PACKED_EXTENSIONS,
        help=(
            "Comma-separated extension list to scan (default: a curated set of "
            "common package/container formats)."
        ),
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    game_dir: Path = args.game_dir.expanduser().resolve()
    output_path: Path = args.output.expanduser().resolve()
    extensions: set[str] = args.extensions

    if not game_dir.exists() or not game_dir.is_dir():
        parser.error(f"Game directory does not exist or is not a directory: {game_dir}")

    assets = [asdict(item) for item in iter_packed_files(game_dir, extensions)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(assets, indent=2), encoding="utf-8")

    print(f"Scanned: {game_dir}")
    print(f"Found packed files: {len(assets)}")
    print(f"Metadata JSON written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
