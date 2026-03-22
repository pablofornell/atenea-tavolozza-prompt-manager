#!/bin/bash
# Build script for Linux
# Generates a standalone executable for Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "========================================"
echo "Tavolozza - Linux Build"
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
echo "Building executable..."
python -m PyInstaller tavolozza.spec --noconfirm

# Check result
if [ -f "dist/tavolozza" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "  Output: $(pwd)/dist/tavolozza"
    echo ""
    echo "To run: ./dist/tavolozza"
else
    echo "Build failed!"
    exit 1
fi

deactivate

