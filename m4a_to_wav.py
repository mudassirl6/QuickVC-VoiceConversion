#!/usr/bin/env python3
"""
Convert M4A and other audio formats to WAV using librosa
"""

import os
import argparse
import librosa
import soundfile as sf
from pathlib import Path

def convert_m4a_to_wav_librosa(input_path, output_path=None, sample_rate=16000):
    """
    Convert M4A file to WAV format using librosa
    
    Args:
        input_path: Path to input M4A file
        output_path: Path to output WAV file (optional)
        sample_rate: Target sample rate (default: 16000 Hz for voice conversion)
    """
    try:
        # Load M4A file - librosa can handle M4A format
        audio, sr = librosa.load(input_path, sr=sample_rate, mono=True)
        
        # Set output path if not provided
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.wav'))
        
        # Save as WAV
        sf.write(output_path, audio, sample_rate)
        print(f"Converted: {input_path} -> {output_path}")
        
        return output_path
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return None

def convert_any_audio_to_wav(input_path, output_path=None, sample_rate=16000):
    """
    Convert any supported audio format to WAV using librosa with fallback options
    
    Supported formats: MP3, M4A, FLAC, OGG, WAV, etc.
    """
    # Set output path if not provided
    if output_path is None:
        output_path = str(Path(input_path).with_suffix('.wav'))
    
    # Try multiple methods for M4A files
    file_ext = Path(input_path).suffix.lower()
    
    # Method 1: Try librosa first (works for most formats)
    try:
        print(f"Trying librosa for {input_path}...")
        audio, sr = librosa.load(input_path, sr=sample_rate, mono=True)
        sf.write(output_path, audio, sample_rate)
        print(f"Converted: {input_path} -> {output_path}")
        return output_path
    except Exception as e:
        print(f"Librosa failed: {e}")
    
    # Method 2: Try pydub for M4A files (better M4A support)
    if file_ext == '.m4a':
        try:
            print(f"Trying pydub for M4A file: {input_path}...")
            from pydub import AudioSegment
            
            # Load M4A with pydub
            audio = AudioSegment.from_file(input_path, format="m4a")
            audio = audio.set_channels(1)  # Mono
            audio = audio.set_frame_rate(sample_rate)  # Set sample rate
            
            # Export as WAV
            audio.export(output_path, format="wav")
            print(f"Converted: {input_path} -> {output_path}")
            return output_path
        except Exception as e:
            print(f"Pydub failed: {e}")
    
    # Method 3: Try ffmpeg as fallback
    try:
        print(f"Trying ffmpeg for {input_path}...")
        import subprocess
        
        result = subprocess.run([
            "ffmpeg", "-i", input_path,
            "-ar", str(sample_rate),  # Sample rate
            "-ac", "1",               # Mono
            "-y",                     # Overwrite
            output_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Converted: {input_path} -> {output_path}")
            return output_path
        else:
            print(f"FFmpeg failed: {result.stderr}")
    except Exception as e:
        print(f"FFmpeg not available: {e}")
    
    print(f"All conversion methods failed for {input_path}")
    return None

def convert_directory_librosa(input_dir, output_dir=None, sample_rate=16000):
    """
    Convert all supported audio files in a directory to WAV format using librosa
    """
    input_path = Path(input_dir)
    
    if output_dir is None:
        output_path = input_path
    else:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Common audio formats that librosa can handle
    supported_formats = ['*.mp3', '*.m4a', '*.flac', '*.ogg', '*.wav', '*.aac']
    
    audio_files = []
    for format_pattern in supported_formats:
        audio_files.extend(input_path.glob(format_pattern))
    
    if not audio_files:
        print(f"No supported audio files found in {input_dir}")
        return
    
    print(f"Found {len(audio_files)} audio files to convert...")
    
    for audio_file in audio_files:
        wav_file = output_path / f"{audio_file.stem}.wav"
        convert_any_audio_to_wav(str(audio_file), str(wav_file), sample_rate)

def main():
    parser = argparse.ArgumentParser(description="Convert audio files to WAV format using librosa")
    parser.add_argument("input", help="Input audio file or directory")
    parser.add_argument("-o", "--output", help="Output WAV file or directory")
    parser.add_argument("-r", "--sample-rate", type=int, default=16000, 
                       help="Target sample rate (default: 16000)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Convert single file
        convert_any_audio_to_wav(args.input, args.output, args.sample_rate)
    elif input_path.is_dir():
        # Convert directory
        convert_directory_librosa(args.input, args.output, args.sample_rate)
    else:
        print(f"Error: {args.input} is not a valid file or directory")

if __name__ == "__main__":
    main()
