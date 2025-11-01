# generate_audio.py
import os
import numpy as np
import soundfile as sf

print("🎙️ Generating Kokoro TTS Audio (TESTING VOICES)...\n")

# Setup paths
output_dir = "storage/outputs/test_audio"
os.makedirs(output_dir, exist_ok=True)

# Simple clear narration
narration = "Welcome to our professional video production system. This is cutting-edge artificial intelligence technology combined with human-quality voice generation."

try:
    print("📍 Loading Kokoro pipeline...")
    from kokoro import KPipeline
    pipeline = KPipeline(lang_code="en-us")
    print("✅ Pipeline loaded\n")
    
    # Test ALL available voices
    print("📍 Testing all available voices...\n")
    voices = ['af_heart', 'bf_emma', 'bf_isabella', 'af_bella']  # Different voice options
    
    for voice in voices:
        print(f"🎤 Testing voice: {voice}")
        try:
            generator = pipeline(narration, voice=voice)
            
            audio_chunks = []
            for gs, ps, audio in generator:
                audio_chunks.append(audio)
            
            full_audio = np.concatenate(audio_chunks)
            sr = 24000
            
            wav_path = os.path.join(output_dir, f"test_{voice}.wav")
            sf.write(wav_path, full_audio, sr)
            
            duration = len(full_audio) / sr
            size = os.path.getsize(wav_path)
            print(f"   ✅ Saved: {wav_path} ({duration:.1f}s, {size} bytes)\n")
            
        except Exception as e:
            print(f"   ❌ {voice} failed: {e}\n")
    
    print("=" * 70)
    print("✅ Voice samples created!")
    print("=" * 70)
    print("\nListen to test files in: storage/outputs/test_audio/")
    print("Choose the best sounding voice for your final video!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
