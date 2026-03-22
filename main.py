#!/usr/bin/env python3
"""
Travolozza - A lightweight desktop application for Prompt Engineering.
Allows users to build complex prompts modularly and copy them to clipboard.
"""

import eel
import os
import sys
import platform
import base64
import subprocess
import tempfile
from pathlib import Path
from tkinter import Tk, filedialog

# Initialize Eel with the web folder
eel.init('web')


@eel.expose
def select_images():
    """Open file dialog to select images and return their paths."""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
            ("All files", "*.*")
        ]
    )
    root.destroy()
    
    # Convert to list and return with base64 encoded thumbnails
    images = []
    for path in file_paths:
        try:
            with open(path, 'rb') as f:
                data = base64.b64encode(f.read()).decode('utf-8')
                ext = Path(path).suffix.lower()
                mime_type = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.bmp': 'image/bmp',
                    '.webp': 'image/webp'
                }.get(ext, 'image/png')
                images.append({
                    'path': path,
                    'data': f'data:{mime_type};base64,{data}'
                })
        except Exception as e:
            print(f"Error loading image {path}: {e}")
    
    return images


@eel.expose
def copy_to_clipboard(text_blocks, image_paths):
    """
    Copy text and images to system clipboard.
    
    Args:
        text_blocks: List of text strings to concatenate
        image_paths: List of image file paths
    """
    # Concatenate all text blocks with double newline
    combined_text = '\n\n'.join([block.strip() for block in text_blocks if block.strip()])
    
    system = platform.system()
    
    try:
        if system == 'Windows':
            return _copy_windows(combined_text, image_paths)
        elif system == 'Darwin':
            return _copy_macos(combined_text, image_paths)
        else:  # Linux
            return _copy_linux(combined_text, image_paths)
    except Exception as e:
        print(f"Clipboard error: {e}")
        return {'success': False, 'error': str(e)}


def _copy_windows(text, image_paths):
    """Copy to clipboard on Windows using win32clipboard."""
    try:
        import win32clipboard
        from PIL import Image
        import io
        
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        
        # Copy text
        if text:
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
        
        # Copy first image if available (Windows clipboard supports one image)
        if image_paths:
            img = Image.open(image_paths[0])
            output = io.BytesIO()
            img.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]  # Remove BMP header
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        
        win32clipboard.CloseClipboard()
        return {'success': True}
    except ImportError:
        # Fallback to pyperclip for text only
        import pyperclip
        pyperclip.copy(text)
        return {'success': True, 'warning': 'Images not copied - install pywin32 for image support'}


def _copy_macos(text, image_paths):
    """Copy to clipboard on macOS using pbcopy and osascript."""
    try:
        # For text, use pbcopy
        if text:
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
        
        # For images, use osascript with pasteboard
        if image_paths:
            # Use NSPasteboard via osascript for image
            script = f'''
            use framework "AppKit"
            set imagePath to "{image_paths[0]}"
            set imageData to (current application's NSData's dataWithContentsOfFile:imagePath)
            set theImage to (current application's NSImage's alloc()'s initWithData:imageData)
            set thePasteboard to current application's NSPasteboard's generalPasteboard()
            thePasteboard's clearContents()
            thePasteboard's writeObjects:{{theImage}}
            '''
            subprocess.run(['osascript', '-e', script], check=True)
        
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _copy_linux(text, image_paths):
    """Copy to clipboard on Linux using xclip with MIME types."""
    from PIL import Image
    import io

    try:
        # If we have text, always copy text (priority for prompt engineering)
        if text:
            process = subprocess.Popen(
                ['xclip', '-selection', 'clipboard'],
                stdin=subprocess.PIPE
            )
            process.communicate(text.encode('utf-8'))

            if image_paths:
                return {
                    'success': True,
                    'warning': f'Text copied. {len(image_paths)} image(s) need to be uploaded manually.'
                }
            return {'success': True}

        # Copy image only if no text
        if image_paths:
            img = Image.open(image_paths[0])
            png_buffer = io.BytesIO()
            img.convert('RGBA').save(png_buffer, format='PNG')
            png_data = png_buffer.getvalue()

            process = subprocess.Popen(
                ['xclip', '-selection', 'clipboard', '-t', 'image/png'],
                stdin=subprocess.PIPE
            )
            process.communicate(png_data)
            return {'success': True}

        return {'success': True}
    except FileNotFoundError:
        return {'success': False, 'error': 'xclip not installed. Install with: sudo apt install xclip'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    """Start the Travolozza application."""
    try:
        # Try Chrome/Chromium first, then fall back to default browser
        eel.start(
            'index.html',
            size=(900, 700),
            port=0,
            mode='chrome',
            cmdline_args=['--disable-gpu']
        )
    except EnvironmentError:
        # If Chrome not available, try default browser
        print("Chrome not found, trying default browser...")
        eel.start(
            'index.html',
            size=(900, 700),
            port=8080,
            mode='default'
        )


if __name__ == '__main__':
    main()

