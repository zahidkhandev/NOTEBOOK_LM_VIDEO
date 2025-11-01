# test_setup.py
import subprocess
import os
import numpy as np

print("✅ Testing setup...\n")

# Test 1: FFmpeg - use full path or system
try:
    # Try system ffmpeg first
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, 
                          text=True,
                          timeout=5)
    if result.returncode == 0:
        print(f"✅ FFmpeg: {result.stdout.split()[2]}")
    else:
        raise Exception("ffmpeg not in PATH")
except:
    try:
        # Try full path
        ffmpeg_path = r"C:\Program Files\FFmpeg\bin\ffmpeg.exe"
        result = subprocess.run([ffmpeg_path, '-version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        print(f"✅ FFmpeg: Found at {ffmpeg_path}")
    except Exception as e:
        print(f"❌ FFmpeg failed: {e}")

# Test 2: espeak-ng
try:
    espeak_path = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
    result = subprocess.run([espeak_path, "Hello"], capture_output=True, text=True, timeout=5)
    print(f"✅ espeak-ng: Working")
except Exception as e:
    print(f"❌ espeak-ng failed: {e}")

# Test 3: Kokoro - GENERATOR FIX
try:
    from kokoro import KPipeline
    print("Loading Kokoro pipeline...")
    pipeline = KPipeline(lang_code="en-us")
    
    print("Generating audio...")
    generator = pipeline("Hello world, this is a test.", voice="af_heart")
    
    # Kokoro returns a GENERATOR - collect all audio chunks
    audio_chunks = []
    for i, (gs, ps, audio) in enumerate(generator):
        audio_chunks.append(audio)
        print(f"  Chunk {i}: {audio.shape if hasattr(audio, 'shape') else len(audio)}")
    
    # Concatenate all chunks
    full_audio = np.concatenate(audio_chunks)
    sr = 24000
    
    print(f"✅ Kokoro: Working (audio shape: {full_audio.shape}, sample rate: {sr}Hz)")
except Exception as e:
    print(f"❌ Kokoro failed: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ All systems ready!")
