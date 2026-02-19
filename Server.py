import os
import requests

def server():
   response = requests.get("http://localhost:11434/")
   if response.status_code == 200 and "Ollama is running" in response.text:
        pass
   else:
        os.system("ollama serve")

        
   

def stop():
    os.system("ollama stop llama3.1")