import os
import sys
import time
import numpy as np
import pyaudio
from faster_whisper import WhisperModel


if sys.platform == "win32":
        try:
            import nvidia.cublas
            import nvidia.cudnn
            os.add_dll_directory(os.path.join(list(nvidia.cublas.__path__)[0], 'bin'))
            os.add_dll_directory(os.path.join(list(nvidia.cudnn.__path__)[0], 'bin'))
        except ImportError:
            print("NVIDIA libraries not found. GPU acceleration might fail.")

model_size = "medium"

model = WhisperModel(model_size, device="cuda", compute_type="float16")



RATE = 16000
CHUNK_DURATION = 0.5 
CHUNK = int(RATE * CHUNK_DURATION) 
TRANSCRIPTION_INTERVAL = 3 
SILENCE_THRESHOLD = 0.03
SILENCE_LIMIT = 2  

def transcription():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")

    silence_start_time = None
    audio_buffer = []
    full_transcript = ""

    try:
        while True:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_np = np.frombuffer(data, dtype=np.float32)
                
                # Check for silence on this small chunk
                rms = np.sqrt(np.mean(audio_np**2))
                if rms < SILENCE_THRESHOLD:
                    if silence_start_time is None:
                        silence_start_time = time.time()
                    elif time.time() - silence_start_time > SILENCE_LIMIT:
                        print("\n...")
                        break
                else:
                    silence_start_time = None

             
                audio_buffer.append(audio_np)
                
                current_buffer_duration = len(audio_buffer) * CHUNK_DURATION
                
                if current_buffer_duration >= TRANSCRIPTION_INTERVAL:
                    
                    full_audio = np.concatenate(audio_buffer)
                    audio_buffer = [] 
                    
                    rms_full = np.sqrt(np.mean(full_audio**2))
                    if rms_full < SILENCE_THRESHOLD * 0.8: 
                        continue

                    segments, info = model.transcribe(
                        full_audio, 
                        beam_size=5,
                        vad_filter=True,
                        vad_parameters=dict(min_silence_duration_ms=500),
                        condition_on_previous_text=False
                    )

                    for segment in segments:
                        text = segment.text + " "
                        sys.stdout.write(text)
                        sys.stdout.flush()
                        full_transcript += text
                    
            except Exception as e:
                print(f"Error: {e}")
                
    except KeyboardInterrupt:
        print("\n...")

    finally:
        if audio_buffer:
            try:
                full_audio = np.concatenate(audio_buffer)
                segments, info = model.transcribe(full_audio, beam_size=5, vad_filter=True, condition_on_previous_text=False)
                for segment in segments:
                    text = segment.text + " "
                    sys.stdout.write(text)
                    sys.stdout.flush()
                    full_transcript += text
            except:
                pass

    stream.stop_stream()
    stream.close()
    p.terminate()

    return full_transcript.strip()


if __name__ == "__main__":
    transcription()
