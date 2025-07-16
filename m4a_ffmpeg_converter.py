#!/usr/bin/env python3
"""
M4A to WAV converter with installation instructions
"""

import os
import sys
import subprocess
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ffmpeg_instructions():
    """Print installation instructions for ffmpeg"""
    print("\n" + "="*50)
    print("FFmpeg is required for M4A conversion")
    print("="*50)
    print("\nInstallation options:")
    print("\n1. Using conda:")
    print("   conda install -c conda-forge ffmpeg")
    print("\n2. Using apt (Ubuntu/Debian):")
    print("   sudo apt update && sudo apt install ffmpeg")
    print("\n3. Using homebrew (macOS):")
    print("   brew install ffmpeg")
    print("\n4. Download from: https://ffmpeg.org/download.html")
    print("\n" + "="*50)

def convert_m4a_to_wav(input_path, output_path=None, sample_rate=16000):
    """Convert M4A to WAV using ffmpeg"""
    if not check_ffmpeg():
        install_ffmpeg_instructions()
        return False
    
    # Set output path if not provided
    if output_path is None:
        output_path = str(Path(input_path).with_suffix('.wav'))
    
    try:
        print(f"Converting {input_path} to {output_path}...")
        
        # Run ffmpeg command
        result = subprocess.run([
            'ffmpeg', '-i', input_path,
            '-ar', str(sample_rate),  # Sample rate
            '-ac', '1',               # Mono
            '-y',                     # Overwrite existing file
            output_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully converted: {input_path} -> {output_path}")
            return True
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python m4a_ffmpeg_converter.py <input.m4a> [output.wav]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    success = convert_m4a_to_wav(input_file, output_file)
    
    if success:
        print(f"\n✅ Conversion complete!")
        print(f"📁 Output file: {output_file or Path(input_file).with_suffix('.wav')}")
    else:
        print(f"\n❌ Conversion failed!")

if __name__ == "__main__":
    main()
