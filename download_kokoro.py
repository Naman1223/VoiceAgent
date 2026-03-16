import os
import requests

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192*4):
                    f.write(chunk)
            print(f"Finished downloading {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"

download_file(MODEL_URL, "kokoro-v1.0.onnx")
download_file(VOICES_URL, "voices-v1.0.bin")
