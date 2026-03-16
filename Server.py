import os
import requests
import subprocess
import time

def server():
    url = "http://127.0.0.1:11434"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200 and "Ollama is running" in response.text:
            return
    except requests.exceptions.ConnectionError:
        subprocess.Popen(
    ["ollama", "serve"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
)
        time.sleep(2) 

def stop_model(model_name="Punisher:latest"):
    try:
        subprocess.run(["ollama", "stop", model_name], check=True)
    except subprocess.CalledProcessError:
        pass

