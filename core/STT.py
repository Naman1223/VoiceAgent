import logging
import time
from moonshine_voice import (
    MicTranscriber,
    TranscriptEventListener,
    get_model_for_language,
    ModelArch,
)
log = logging.basicConfig(
    filename="Logs/Moonshine.log", 
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


# Fetch the model
model_path, model_arch = get_model_for_language("en", ModelArch.MEDIUM_STREAMING)

# Initialize the transcriber
mic_transcriber = MicTranscriber(
    model_path=model_path,
    model_arch=model_arch,
)

# We use a global tracking variable for the last activity epoch time
last_speech_time = time.time()
is_paused = False

class TimeoutVADListener(TranscriptEventListener):
    def on_line_started(self, event):
        global last_speech_time
        last_speech_time = time.time()  # Reset timer immediately when speech begins
        print("🎙️ Listening...")

    def on_line_completed(self, event):
        global last_speech_time
        last_speech_time = time.time()  # Reset timer when a segment concludes
        print(f"Text: {event.line.text}")
        logging.debug(f"Text: {event.line.text}")
        return event.line.text


listener = TimeoutVADListener()
mic_transcriber.add_listener(listener)
mic_transcriber.start()
print("Listening to microphone. Remaining silent for 3 seconds will pause the instance...\n")

try:
    while True:
        time.sleep(0.1)
        
        # Calculate how long it has been since the last activity event
        silence_duration = time.time() - last_speech_time
        
        if silence_duration >= 3.0 and not is_paused:
            print("\n🤫 3 seconds of silence detected. Pausing Moonshine stream...")
            mic_transcriber.stop()  # Effectively pauses processing and releases mic hardware
            is_paused = True
except Exception as e:
    print(e)
finally:
    if not is_paused:
        mic_transcriber.stop()