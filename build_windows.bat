@echo off
setlocal
chcp 65001 >nul

REM ============================================================
REM  MIB STD2 HMIOFFCLOCKVIEW PATCHER v1.2 - build script (Windows)
REM  Result: dist\MST2HocvPatcher_1.2.exe
REM ============================================================

cd /d "%~dp0"

echo [1/3] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install PySide6 pyinstaller
if errorlevel 1 (
    echo ERROR: pip install failed
    pause
    exit /b 1
)

echo [2/3] Cleaning old build artifacts...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist
if exist MST2HocvPatcher_1.2.spec del /q MST2HocvPatcher_1.2.spec

echo [3/3] Building exe...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --name "MST2HocvPatcher_1.2" ^
    --add-data "icon.ico;." ^
    MST2HocvPatcher.py
if errorlevel 1 (
    echo ERROR: build failed
    pause
    exit /b 1
)

echo Done. Artifact: %cd%\dist\MST2HocvPatcher_1.2.exe
pause
