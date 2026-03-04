# Toxic Commando Mod Toolset (Metadata-Only Foundation)

This repository starts a **safe, metadata-only** toolchain for researching packed
assets in *John Carpenter's Toxic Commando* without redistributing copyrighted game data.

## Folder layout

- `extractor/` — scripts that inspect game files and emit metadata indexes.
- `viewer/` — scripts to review metadata outputs and run the desktop GUI scanner.
- `docs/` — notes about reverse engineering progress and format research.

## Scripts

### 1) CLI scanner (first working extractor)

`extractor/scan_packed_assets.py` recursively scans a game folder and outputs a JSON document with:

- `schema_version`
- `generated_at_utc`
- `scanned_root`
- `asset_count`
- `assets[]` entries containing:
  - `file_name`
  - `relative_path`
  - `size_bytes`
  - `file_type`

The script only stores metadata and never copies file contents.

**Usage**

```bash
python3 extractor/scan_packed_assets.py /path/to/game -o outputs/packed_asset_index.json
```

Optional custom extension list:

```bash
python3 extractor/scan_packed_assets.py /path/to/game \
  -o outputs/packed_asset_index.json \
  --extensions pak,pck,bin,dat
```

### 2) CLI metadata viewer

```bash
python3 viewer/preview_asset_index.py outputs/packed_asset_index.json --limit 30
```

### 3) Desktop GUI scanner

The GUI lets you browse for folders/files instead of typing paths manually.

```bash
python3 viewer/asset_scanner_gui.py
```

GUI features:
- Folder picker for the game install path.
- Save dialog for output JSON location.
- Editable extension list.
- Status area with scan results and a preview of the first 10 rows.

## Build a Windows EXE release

To distribute as a standalone executable, package the GUI with PyInstaller.

### Option A: direct command

```bash
pyinstaller --noconfirm --clean --onefile --windowed \
  --name ToxicCommandoAssetScanner viewer/asset_scanner_gui.py
```

### Option B: batch helper script (Windows)

Run from repo root:

```bat
build_exe.bat
```

Output artifact:
- `dist/ToxicCommandoAssetScanner.exe`

> The EXE contains only the scanner tool; it does **not** bundle game assets.

## Extensibility roadmap

1. Add per-format readers in `extractor/parsers/` (e.g., `.pak`, `.pck`) that decode internal tables only.
2. Emit optional CSV summaries and hash indexes for differential analysis between game updates.
3. Add future patch/swap workflow modules that reference local user-owned files only.
4. Keep all workflows content-agnostic by default to avoid shipping proprietary assets.
