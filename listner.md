### 1. Imports and DLL Setup

```python
import os
import sys
import time
import numpy as np
import pyaudio
from faster_whisper import WhisperModel

```

* **`os` / `sys**`: Used for system-level operations and path handling.
* **`time`**: Used to track how long silence has lasted.
* **`numpy` (np)**: Essential for handling the audio data as numerical arrays.
* **`pyaudio`**: The library that interfaces with your microphone.
* **`WhisperModel`**: The core AI engine that turns audio into text.

```python
if sys.platform == "win32":
    try:
        import nvidia.cublas
        import nvidia.cudnn
        os.add_dll_directory(os.path.join(list(nvidia.cublas.__path__)[0], 'bin'))
        os.add_dll_directory(os.path.join(list(nvidia.cudnn.__path__)[0], 'bin'))

```

* **The Windows GPU Fix**: On Windows, Python often can't find the NVIDIA CUDA libraries even if they are installed. This block manually locates the `cublas` and `cudnn` directories and tells Windows, "Look for the GPU acceleration files here."

---

### 2. Model Initialization

```python
model_size = "small.en"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

```

* **`model_size`**: Uses the "small" English-only model. It’s a balance between speed and accuracy.
* **`device="cuda"`**: Tells the model to run on your **NVIDIA GPU**.
* **`compute_type="float16"`**: Uses half-precision numbers. This makes the model run significantly faster and use less VRAM without losing much accuracy.

---

### 3. Audio Configuration Constants

```python
RATE = 16000                # Sample rate (Whisper requires 16kHz)
CHUNK_DURATION = 0.5        # Read 0.5 seconds of audio at a time
CHUNK = int(RATE * CHUNK_DURATION) 
TRANSCRIPTION_INTERVAL = 3  # Wait until we have 3 seconds of audio before transcribing
SILENCE_THRESHOLD = 0.03    # Volume level below which we consider it "silence"
SILENCE_LIMIT = 2           # If silent for 2 seconds, stop the program

```

These settings define the "feel" of the app. It waits for 3 seconds of speech, processes it, and shuts down if you stop talking for 2 seconds.

---

### 4. PyAudio Stream Setup

```python
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

```

* **`paFloat32`**: Whisper expects audio normalized between -1.0 and 1.0.
* **`channels=1`**: Mono audio (Whisper doesn't need stereo).
* **`input=True`**: This tells PyAudio to open the microphone, not the speakers.

---

### 5. The Main Listening Loop

```python
try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_np = np.frombuffer(data, dtype=np.float32)

```

* The code enters an infinite loop, constantly reading `CHUNK` (0.5s) of audio and converting the raw bytes into a **Numpy array** that the AI can understand.

#### A. Silence Detection Logic

```python
rms = np.sqrt(np.mean(audio_np**2)) # Calculate "volume" (Root Mean Square)
if rms < SILENCE_THRESHOLD:
    if silence_start_time is None:
        silence_start_time = time.time()
    elif time.time() - silence_start_time > SILENCE_LIMIT:
        print("\nSilence detected. Stopping...")
        break
else:
    silence_start_time = None

```

* It calculates the **RMS** (average volume). If it's below the threshold, a timer starts. If that timer hits 2 seconds, the `break` command exits the loop.

#### B. Buffering and Transcribing

```python
audio_buffer.append(audio_np)
current_buffer_duration = len(audio_buffer) * CHUNK_DURATION

if current_buffer_duration >= TRANSCRIPTION_INTERVAL:
    full_audio = np.concatenate(audio_buffer)
    audio_buffer = [] # Clear buffer for next round

```

* It adds the 0.5s chunks to a list (`audio_buffer`).
* Once that list reaches 3 seconds of audio, it "glues" them together into one array (`full_audio`) and clears the list to make room for new speech.

```python
segments, info = model.transcribe(
    full_audio, 
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
    condition_on_previous_text=False
)

```

* **`model.transcribe`**: This is where the magic happens.
* **`beam_size=5`**: A search algorithm that looks for the 5 most likely word sequences to ensure accuracy.
* **`vad_filter=True`**: **Voice Activity Detection**. It filters out non-speech noise before sending it to the AI.
* **`condition_on_previous_text=False`**: Prevents the AI from getting "stuck" in a loop by repeating words from the previous 3-second window.

```python
for segment in segments:
    print(segment.text, end=" ", flush=True)

```

* This loops through the results and prints just the words. `flush=True` ensures the text appears immediately on the screen rather than waiting for a line break.

---

### 6. Cleanup and Final Transcription

```python
finally:
    if audio_buffer:
        # Transcribe any leftover audio in the buffer before closing
        ...
    stream.stop_stream()
    stream.close()
    p.terminate()

```

* The `finally` block is the "safety net." If you press **Ctrl+C** or the program breaks due to silence, it:

1. Checks if there is any "unprocessed" audio left in the buffer and transcribes it so you don't lose the last few words.
2. Safely shuts down the microphone hardware and releases the memory.

---
