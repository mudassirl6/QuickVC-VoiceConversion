#!/usr/bin/env python3
"""
Convert M4A files to WAV using alternative methods
"""

import os
import argparse
import librosa
import soundfile as sf
from pathlib import Path

def convert_m4a_with_audioread(input_path, output_path=None, sample_rate=16000):
    """
    Convert M4A file to WAV using audioread backend
    """
    try:
        # Force audioread backend for M4A files
        import audioread
        
        # Set output path if not provided
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.wav'))
        
        print(f"Converting M4A using audioread: {input_path}")
        
        # Load with audioread backend
        with audioread.audio_open(input_path) as f:
            sr_native = f.samplerate
            duration = f.duration
            
            # Read all frames
            audio_data = []
            for frame in f:
                audio_data.append(frame)
            
            # Convert to numpy array
            import numpy as np
            audio_bytes = b''.join(audio_data)
            
            # Convert bytes to float32 audio
            if f.channels == 2:
                audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                audio = audio.reshape((-1, 2))
                audio = audio.mean(axis=1)  # Convert to mono
            else:
                audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Resample if needed
            if sr_native != sample_rate:
                audio = librosa.resample(audio, orig_sr=sr_native, target_sr=sample_rate)
            
            # Save as WAV
            sf.write(output_path, audio, sample_rate)
            print(f"Converted: {input_path} -> {output_path}")
            return output_path
            
    except Exception as e:
        print(f"Audioread conversion failed: {e}")
        return None

def convert_with_simple_fallback(input_path, output_path=None, sample_rate=16000):
    """
    Simple conversion with multiple fallback methods
    """
    # Set output path if not provided
    if output_path is None:
        output_path = str(Path(input_path).with_suffix('.wav'))
    
    # Method 1: Try librosa with different backends
    backends = ['soundfile', 'audioread']
    
    for backend in backends:
        try:
            print(f"Trying librosa with {backend} backend...")
            
            # Try to load with specific backend
            audio, sr = librosa.load(input_path, sr=sample_rate, mono=True)
            
            # Save as WAV
            sf.write(output_path, audio, sample_rate)
            print(f"Converted: {input_path} -> {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Backend {backend} failed: {e}")
            continue
    
    # Method 2: Try audioread directly
    result = convert_m4a_with_audioread(input_path, output_path, sample_rate)
    if result:
        return result
    
    print(f"All methods failed for {input_path}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Convert M4A files to WAV with fallback methods")
    parser.add_argument("input", help="Input M4A file")
    parser.add_argument("-o", "--output", help="Output WAV file")
    parser.add_argument("-r", "--sample-rate", type=int, default=16000, 
                       help="Target sample rate (default: 16000)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        convert_with_simple_fallback(args.input, args.output, args.sample_rate)
    else:
        print(f"Error: {args.input} is not a valid file")

if __name__ == "__main__":
    main()
