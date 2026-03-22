@echo off
REM Build script for Windows
REM Generates a standalone .exe for Windows

setlocal enabledelayedexpansion

cd /d "%~dp0\.."

echo ========================================
echo Tavolozza - Windows Build
echo ========================================

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Clean previous builds if --clean flag is passed
if "%1"=="--clean" (
    echo Cleaning previous builds...
    if exist "build" rmdir /s /q build
    if exist "dist" rmdir /s /q dist
)

REM Run PyInstaller
echo Building executable...
python -m PyInstaller tavolozza.spec --noconfirm

REM Check result
if exist "dist\Tavolozza.exe" (
    echo.
    echo Build successful!
    echo   Output: %cd%\dist\Tavolozza.exe
    echo.
    echo To run: dist\Tavolozza.exe
) else (
    echo Build failed!
    exit /b 1
)

call venv\Scripts\deactivate.bat

