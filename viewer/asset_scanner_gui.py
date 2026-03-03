#!/usr/bin/env python3
"""Desktop GUI for scanning packed assets and exporting metadata JSON.

This app wraps extractor/scan_packed_assets.py functionality with a folder picker,
output chooser, and simple status area. Intended for building a Windows .exe via
PyInstaller so non-technical users can run scans easily.
"""

from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from extractor.scan_packed_assets import (
    DEFAULT_PACKED_EXTENSIONS,
    parse_extensions,
    scan_game_directory,
    write_index_json,
)


class AssetScannerGUI(tk.Tk):
    """Main Tk app for scanning and exporting packed-file metadata."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Toxic Commando Packed Asset Scanner")
        self.geometry("840x520")
        self.minsize(760, 460)

        self.game_dir_var = tk.StringVar()
        self.output_var = tk.StringVar(value=str(Path.cwd() / "packed_asset_index.json"))
        self.extensions_var = tk.StringVar(
            value=",".join(sorted(ext.lstrip(".") for ext in DEFAULT_PACKED_EXTENSIONS))
        )

        self._build_layout()

    def _build_layout(self) -> None:
        container = ttk.Frame(self, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Game Folder:").grid(row=0, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.game_dir_var).grid(
            row=1, column=0, sticky="ew", padx=(0, 8)
        )
        ttk.Button(container, text="Browse...", command=self._select_game_folder).grid(
            row=1, column=1, sticky="ew"
        )

        ttk.Label(container, text="Output JSON:").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(container, textvariable=self.output_var).grid(
            row=3, column=0, sticky="ew", padx=(0, 8)
        )
        ttk.Button(container, text="Save As...", command=self._select_output_file).grid(
            row=3, column=1, sticky="ew"
        )

        ttk.Label(container, text="Extensions (comma-separated, no dots needed):").grid(
            row=4, column=0, sticky="w", pady=(12, 0)
        )
        ttk.Entry(container, textvariable=self.extensions_var).grid(
            row=5, column=0, columnspan=2, sticky="ew"
        )

        ttk.Button(container, text="Scan Folder", command=self._run_scan).grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=(12, 8)
        )

        ttk.Label(container, text="Status:").grid(row=7, column=0, sticky="w")
        self.status = tk.Text(container, height=14, wrap="word")
        self.status.grid(row=8, column=0, columnspan=2, sticky="nsew")

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=0)
        container.rowconfigure(8, weight=1)

    def _select_game_folder(self) -> None:
        path = filedialog.askdirectory(title="Select game installation folder")
        if path:
            self.game_dir_var.set(path)

    def _select_output_file(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save metadata JSON as",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if path:
            self.output_var.set(path)

    def _append_status(self, message: str) -> None:
        self.status.insert(tk.END, f"{message}\n")
        self.status.see(tk.END)

    def _run_scan(self) -> None:
        self.status.delete("1.0", tk.END)

        game_dir_text = self.game_dir_var.get().strip()
        output_text = self.output_var.get().strip()
        extension_text = self.extensions_var.get().strip()

        if not game_dir_text:
            messagebox.showerror("Missing input", "Please select a game folder.")
            return
        if not output_text:
            messagebox.showerror("Missing input", "Please set an output JSON path.")
            return

        try:
            extensions = parse_extensions(extension_text)
            assets = scan_game_directory(Path(game_dir_text), extensions)
            output_path = write_index_json(Path(output_text), assets)
        except Exception as exc:  # user-facing GUI error path
            messagebox.showerror("Scan failed", str(exc))
            self._append_status(f"Error: {exc}")
            return

        self._append_status(f"Scanned: {Path(game_dir_text).expanduser().resolve()}")
        self._append_status(f"Extensions: {', '.join(sorted(extensions))}")
        self._append_status(f"Found packed files: {len(assets)}")
        self._append_status(f"JSON output: {output_path}")

        preview_rows = [
            {
                "file_name": item.file_name,
                "relative_path": item.relative_path,
                "size_bytes": item.size_bytes,
                "file_type": item.file_type,
            }
            for item in assets[:10]
        ]
        self._append_status("Preview (first 10 rows):")
        self._append_status(json.dumps(preview_rows, indent=2))

        messagebox.showinfo("Scan complete", f"Found {len(assets)} packed files.")


def main() -> int:
    app = AssetScannerGUI()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
