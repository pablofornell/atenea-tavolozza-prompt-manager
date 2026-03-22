#!/bin/bash
# Build script for macOS
# Generates a .app bundle for macOS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "========================================"
echo "Tavolozza - macOS Build"
echo "========================================"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Clean previous builds if --clean flag is passed
if [ "$1" == "--clean" ]; then
    echo "Cleaning previous builds..."
    rm -rf build dist
fi

# Run PyInstaller
echo "Building .app bundle..."
python -m PyInstaller tavolozza.spec --noconfirm

# Check result
if [ -d "dist/Tavolozza.app" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "  Output: $(pwd)/dist/Tavolozza.app"
    echo ""
    echo "To install: drag Tavolozza.app to your Applications folder"
    echo "To run: open dist/Tavolozza.app"
else
    echo "Build failed!"
    exit 1
fi

deactivate

