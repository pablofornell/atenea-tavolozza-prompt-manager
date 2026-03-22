#!/usr/bin/env python3
"""
Tavolozza Build Script
Cross-platform build script that generates executables for the current OS.

Usage:
    python build.py          # Build for current platform
    python build.py --clean  # Clean build artifacts before building
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path


def get_platform_info():
    """Get current platform information."""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos', 'Tavolozza.app'
    elif system == 'windows':
        return 'windows', 'Tavolozza.exe'
    else:
        return 'linux', 'tavolozza'


def clean_build():
    """Remove previous build artifacts."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"Removing {dir_name}/...")
            shutil.rmtree(dir_path)
    print("Clean complete.")


def install_dependencies():
    """Ensure all dependencies are installed."""
    print("Installing dependencies...")
    subprocess.run([
        sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'
    ], check=True)


def build_executable():
    """Build the executable using PyInstaller."""
    platform_name, output_name = get_platform_info()
    print(f"Building Tavolozza for {platform_name}...")
    
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller',
        'tavolozza.spec',
        '--noconfirm',
    ], capture_output=False)
    
    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)
    
    # Report success and output location
    dist_path = Path('dist')
    if platform_name == 'macos':
        output_path = dist_path / 'Tavolozza.app'
    else:
        output_path = dist_path / output_name
    
    if output_path.exists():
        print(f"\n✓ Build successful!")
        print(f"  Output: {output_path.absolute()}")
    else:
        print(f"\n⚠ Build completed but output not found at expected location.")
        print(f"  Check the 'dist' folder for the executable.")


def main():
    """Main entry point."""
    # Parse arguments
    clean_first = '--clean' in sys.argv
    
    print("=" * 50)
    print("Tavolozza Build System")
    print("=" * 50)
    
    if clean_first:
        clean_build()
    
    install_dependencies()
    build_executable()


if __name__ == '__main__':
    main()

