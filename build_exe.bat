@echo off
REM Build a standalone Windows EXE for the GUI scanner using PyInstaller.
REM Run from repository root in a Python environment where pyinstaller is installed.

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name ToxicCommandoAssetScanner ^
  viewer\asset_scanner_gui.py

echo.
echo Build finished. Check dist\ToxicCommandoAssetScanner.exe
