# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Tavolozza
Generates standalone executables for Windows, macOS, and Linux
"""

import sys
import os
from pathlib import Path

# Determine the platform
is_windows = sys.platform == 'win32'
is_macos = sys.platform == 'darwin'
is_linux = sys.platform.startswith('linux')

# Application metadata
app_name = 'Tavolozza'
app_version = '1.0.0'

# Get the directory where the spec file is located
spec_dir = Path(SPECPATH)

# Analysis: collect all dependencies
a = Analysis(
    ['main.py'],
    pathex=[str(spec_dir)],
    binaries=[],
    datas=[
        ('web', 'web'),  # Include the web folder with HTML/CSS/JS
    ],
    hiddenimports=[
        'eel',
        'bottle_websocket',
        'PIL',
        'PIL.Image',
        'pyperclip',
        'tkinter',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Remove unnecessary files to reduce size
pyz = PYZ(a.pure)

# Platform-specific executable settings
if is_macos:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=app_name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,  # No terminal window on macOS
        disable_windowed_traceback=False,
        argv_emulation=True,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name=app_name,
    )
    # Create macOS .app bundle
    app = BUNDLE(
        coll,
        name=f'{app_name}.app',
        icon=None,  # Add icon path here if available: 'assets/icon.icns'
        bundle_identifier='com.tavolozza.app',
        info_plist={
            'CFBundleShortVersionString': app_version,
            'CFBundleVersion': app_version,
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
        },
    )
elif is_windows:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name=app_name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # No console window
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=None,  # Add icon path here if available: 'assets/icon.ico'
    )
else:  # Linux
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name=app_name.lower(),  # lowercase for Linux convention
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )

