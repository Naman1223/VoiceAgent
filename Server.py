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
        subprocess.Popen(["ollama", "serve"], shell=True)
        time.sleep(5) 

def stop_model(model_name="llama3.1"):
    try:
        subprocess.run(["ollama", "stop", model_name], check=True)
    except subprocess.CalledProcessError:
        pass

