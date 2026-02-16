import faster_whisper
import pyaudio
import numpy as np


import pyaudio
import time

# 1. Define the callback function
def callback(in_data, frame_count, time_info, status):
    model = faster_whisper.download_model("tiny")
    result = model.transcribe("audio.mp3")
    print(result["text"])
    return (in_data, pyaudio.paContinue)

p = pyaudio.PyAudio()

# 2. Open the stream in callback mode
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                output=True,
                stream_callback=callback)

# 3. Start the stream
stream.start_stream()

# 4. Keep the main thread alive while streaming
try:
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

# 5. Clean up
stream.stop_stream()
stream.close()
p.terminate()



