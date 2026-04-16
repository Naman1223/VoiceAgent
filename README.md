# VoiceAgent

VoiceAgent is a real-time, conversational AI voice assistant running locally on your machine. It features low-latency Speech-to-Text (STT), a robust Language Model (LLM) for processing, and high-performance Text-to-Speech (TTS) capabilities, integrated with tool-calling for executing operating system and browser commands.

## Features

* **Real-time Speech-to-Text**: Utilizes `faster-whisper` for fast, local audio transcription with Voice Activity Detection (VAD) to minimize latency.
* **Conversational Engine**: Powered by LangGraph and Ollama (defaulting to the `hermes3:8b` model), allowing for memory management and conversational context.
* **High-Speed Text-to-Speech**: Uses `kokoro-onnx` for incredibly fast and natural text-to-speech synthesis. 
* **Dynamic Chunking**: The agent splits its spoken responses dynamically based on punctuation, delivering a real-time response feel instead of waiting for full sentences to generate.
* **Tool Calling Capabilities**: The agent is equipped with several tools, including:
  * Browser automation using `browser-use`
  * System terminal command execution
  * File and folder management
  * Basic calculations
  * Application launching

## Prerequisites

* Python 3.10+
* [Ollama](https://ollama.com/) installed and running locally
* The `hermes3:8b` model pulled via Ollama (`ollama pull hermes3:8b`)
* NVIDIA GPU (Recommended for CUDA acceleration in STT) 

## Installation

1. Clone the repository and navigate into the directory:
```bash
git clone https://github.com/Naman1223/VoiceAgent.git
cd VoiceAgent
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Download the Kokoro ONNX model files. (You can download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from the kokoro-onnx releases and place them in the root directory). Note: These files are tracked using Git LFS due to their large size.

## Usage

Ensure Ollama is running in the background. If it isn't, `Server.py` will attempt to start it automatically.

Start the voice agent by running:
```bash
python Agent.py
```

Speak into your microphone. The agent will detect your speech automatically, process it through the LLM, use tools if necessary, and reply with generated audio. To exit the conversation, simply say "exit", "quit", or "bye".

## Architecture

* **`listner.py`**: Handles microphone input, Voice Activity Detection, and transcription via Faster Whisper.
* **`Agent.py`**: The main LangGraph execution loop. Handles tool binding, prompt management, and streams responses to the Kokoro-ONNX TTS engine.
* **`Server.py`**: Checks if the local Ollama server is running and starts it if necessary.
* **`tools/basic_tools.py`**: Defines the LangChain tools available to the assistant.