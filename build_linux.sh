#!/usr/bin/env bash
# ============================================================
#  MIB STD2 HMIOFFCLOCKVIEW PATCHER v1.2 - build script (Linux)
#  Result: dist/MST2HocvPatcher_1.2
# ============================================================
set -e
cd "$(dirname "$0")"

echo "[1/3] Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install PySide6 pyinstaller

echo "[2/3] Cleaning old build artifacts..."
rm -rf build dist MST2HocvPatcher_1.2.spec

echo "[3/3] Building binary..."
python3 -m PyInstaller \
    --onefile \
    --windowed \
    --icon=icon.ico \
    --name "MST2HocvPatcher_1.2" \
    --add-data "icon.ico:." \
    MST2HocvPatcher.py

echo "Done. Artifact: $(pwd)/dist/MST2HocvPatcher_1.2"
