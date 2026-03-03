# Toxic Commando Mod Toolset (Metadata-Only Foundation)

This repository starts a **safe, metadata-only** toolchain for researching packed
assets in *John Carpenter's Toxic Commando* without redistributing copyrighted game data.

## Folder layout

- `extractor/` — scripts that inspect game files and emit metadata indexes.
- `viewer/` — scripts to review metadata outputs in terminal-friendly format.
- `docs/` — notes about reverse engineering progress and format research.

## First script

`extractor/scan_packed_assets.py` recursively scans a game folder and outputs JSON entries containing:

- `file_name`
- `relative_path`
- `size_bytes`
- `file_type`

The script only stores metadata and never copies file contents.

### Usage

```bash
python3 extractor/scan_packed_assets.py /path/to/game -o outputs/packed_asset_index.json
```

Optional custom extension list:

```bash
python3 extractor/scan_packed_assets.py /path/to/game \
  -o outputs/packed_asset_index.json \
  --extensions pak,pck,bin,dat
```

Then preview results:

```bash
python3 viewer/preview_asset_index.py outputs/packed_asset_index.json --limit 30
```

## Extensibility roadmap

1. Add per-format readers in `extractor/parsers/` (e.g., `.pak`, `.pck`) that decode internal tables only.
2. Emit optional CSV summaries and hash indexes for differential analysis between game updates.
3. Add future patch/swap workflow modules that reference local user-owned files only.
4. Keep all workflows content-agnostic by default to avoid shipping proprietary assets.
