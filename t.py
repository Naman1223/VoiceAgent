import os
import sys

# Add NVIDIA libraries to the DLL search path for Windows
if sys.platform == "win32":
    import nvidia.cublas
    import nvidia.cudnn
    os.add_dll_directory(os.path.join(list(nvidia.cublas.__path__)[0], 'bin'))
    os.add_dll_directory(os.path.join(list(nvidia.cudnn.__path__)[0], 'bin'))

from faster_whisper import WhisperModel

model_size = "small.en"

model = WhisperModel(model_size, device="cuda", compute_type="float16")

segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print("{} ({} -> {})".format(segment.text, segment.start, segment.end))