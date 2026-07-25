# VoxCode 🎙️🤖

**VoxCode** is a modular, provider-agnostic AI agent framework with a dynamic tool-discovery system powered by ChromaDB vector search. Agents don''t hard-code which tools to use — they *search* for them at runtime. The project also ships a real-time Speech-to-Text (STT) listener powered by [Moonshine](https://github.com/usefulsensors/moonshine), making it trivially extensible into a fully voice-controlled AI assistant.

---

## ✨ Features

- **Provider-Agnostic LLM Backend** — Seamlessly switch between OpenAI, Anthropic, Google Gemini, Grok (xAI), Groq, HuggingFace, OpenRouter, and local `llama.cpp` models with a single string change.
- **Unified Tool-Calling API** — One `chat_with_tools()` method abstracts the different tool-calling APIs across all providers (OpenAI-style, Google `FunctionDeclaration`, Anthropic `tool_use`).
- **Semantic Tool Discovery via ChromaDB** — Tools are stored and retrieved by semantic similarity, not hardcoded lists. The agent asks "what tool can open a website?" and finds it from the vector database.
- **Self-Describing Tools** — Every tool registers itself with a name, description, and JSON schema into ChromaDB on startup. No manual mapping required.
- **Allowlisted Model Registry** — Only models listed in `core/Mod/Model_list.txt` can be loaded, preventing accidental use of unauthorised endpoints.
- **Real-Time STT** — `core/STT.py` uses the Moonshine streaming model to transcribe microphone input continuously, with automatic silence detection and stream pausing.
- **Fully Extendable** — Adding a new tool is a single file + one `register_tool()` call. Adding a new LLM provider is ~10 lines in `Models.py`.

---

## 📁 Project Structure

```
VoxCode/
├── main.py                    # Entry point — runs the agentic tool-calling loop
├── Settings.py                # API key routing + model generation defaults
├── requirements.txt           # Pip dependencies
├── pyproject.toml             # uv/PEP 517 project config (Python >= 3.12)
│
├── core/
│   ├── Models.py              # VanillaChatModel: unified LLM wrapper + tool-calling
│   ├── STT.py                 # Real-time mic transcription via Moonshine
│   └── Mod/
│       └── Model_list.txt     # Allowlist of permitted provider/model identifiers
│
├── tools/
│   ├── tool.py                # Tools dataclass definition
│   ├── schemas.py             # JSON schemas for all tools
│   ├── chroma_tools.py        # ChromaDB registration, semantic search, dynamic execution
│   └── web_tools.py           # open_chrome tool (opens URLs in browser)
│
├── database/
│   └── chroma_db/             # Persisted ChromaDB vector store (auto-created)
│
└── Logs/                      # Rotating log files (auto-created)
    ├── Models.log
    └── Moonshine.log
```

---

## 🏗️ Architecture

### The Agentic Loop (`main.py`)

VoxCode uses a **ReAct-style tool-calling loop**:

```
User Prompt
    │
    ▼
┌─────────────────────────────────┐
│         LLM (any provider)      │
│  always has 2 built-in tools:   │
│  • find_relevant_tools          │  ◄── semantic search in ChromaDB
│  • execute_dynamic_tool         │  ◄── calls the retrieved tool
└──────────────┬──────────────────┘
               │  tool_calls?
        ┌──────┴──────┐
       YES             NO
        │               │
        ▼               ▼
  Execute tool      Final answer
  → append result      (done)
  → loop back
```

The LLM is never given the full tool list. Instead, it uses `find_relevant_tools` to semantically query ChromaDB, then uses `execute_dynamic_tool` to call whatever it found. This means the agent scales to thousands of tools without bloating the context window.

---

### `VanillaChatModel` — Unified LLM Interface

Located in `core/Models.py`, `VanillaChatModel` wraps any supported provider behind two methods:

| Method | Purpose |
|---|---|
| `invoke(prompt)` | Simple single-turn text completion |
| `chat_with_tools(messages, tools)` | Multi-turn agentic loop with tool-calling |

`chat_with_tools()` returns a **unified response dict** regardless of provider:

```python
{
    "content": str | None,          # Text portion of the response
    "tool_calls": [                 # List of tool calls (or None)
        {
            "id":        str,       # Call ID (provider-specific)
            "name":      str,       # Tool name to execute
            "arguments": dict       # Parsed kwargs
        }
    ],
    "raw": <provider object>        # Original response for history replay
}
```

---

### Tool System

#### Defining a Tool

Every tool is a `Tools` dataclass instance (`tools/tool.py`):

```python
from tools.tool import Tools

my_tool = Tools(
    name="my_tool_name",
    description="What this tool does (used for semantic search).",
    input_schema={               # Standard JSON Schema
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "..."}
        },
        "required": ["param"]
    },
    func=my_python_function      # The callable to invoke
)
```

#### Registering a Tool

```python
from tools.chroma_tools import register_tool

register_tool(my_tool)
```

This upserts the tool''s **description as a document** and its **schema as metadata** into ChromaDB. The tool is also added to the in-memory `TOOL_REGISTRY` for execution. Simply importing the file that calls `register_tool()` is enough — see how `main.py` imports `tools.web_tools` to auto-register the browser tool.

#### How Tool Discovery Works

1. The LLM calls `find_relevant_tools(query="open a website")`.
2. ChromaDB performs a **semantic vector search** against all registered tool descriptions.
3. The top-N tools (names + schemas) are returned.
4. The LLM calls `execute_dynamic_tool(tool_name="open_chrome", arguments={"url": "..."})`.
5. The registry dispatches to the actual Python function.

---

## 🤖 Supported LLM Providers

Models are specified as `"provider/model-name"` and must appear in `core/Mod/Model_list.txt`.

| Provider | Example Format | API Key Env Var |
|---|---|---|
| OpenAI | `openai/gpt-4o` | `OPENAI_API_KEY` |
| Anthropic | `anthropic/claude-3-opus-20240229` | `ANTHROPIC_API_KEY` |
| Google Gemini | `google/gemini-2.5-pro` | `GOOGLE_API_KEY` |
| Grok (xAI) | `grok/grok-2-latest` | `XAI_API_KEY` or `GROK_API_KEY` |
| Groq | `groq/llama-3.3-70b-versatile` | `GROQ_API_KEY` |
| HuggingFace | `huggingface/meta-llama/Meta-Llama-3-8B-Instruct` | `HF_TOKEN` |
| OpenRouter | `openrouter/openai/gpt-4o` | `OPENROUTER_API_KEY` |
| Local (llama.cpp) | `local/llama3` | `LOCAL_MODEL_PATH` env var or interactive prompt |

### Adding a New Model

Simply add a line to `core/Mod/Model_list.txt`:

```
openai/gpt-4o-mini
```

### Adding a New Provider

Add a new `elif` branch in `get_chat_model()` and `chat_with_tools()` in `core/Models.py`.

---

## 🎙️ Speech-to-Text (`core/STT.py`)

VoxCode includes a standalone real-time transcription module using [Moonshine](https://github.com/usefulsensors/moonshine), an on-device English ASR model optimised for streaming:

- Streams microphone input continuously.
- Uses Voice Activity Detection (VAD) to detect speech start/end.
- **Auto-pauses** after 3 seconds of silence to release mic hardware.
- Logs all transcripts to `Logs/Moonshine.log`.

> **Note:** `STT.py` is currently a standalone listener. Integration with the agentic loop (so the agent responds to spoken commands) is a planned extension.

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`
- A microphone (for STT features)

### 1. Clone the Repository

```bash
git clone https://github.com/Naman1223/VoiceAgent.git
cd VoiceAgent
```

### 2. Create a Virtual Environment & Install Dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Use only the key(s) for your chosen provider(s)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
XAI_API_KEY=xai-...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
HF_TOKEN=hf_...

# For local llama.cpp models
LOCAL_MODEL_PATH=C:/path/to/your/model.gguf
```

### 4. Run the Agent

```bash
python main.py
```

---

## 💡 Usage Examples

### Switching the Model

Edit the model string in `main.py`:

```python
# Google Gemini
model = get_chat_model("google/gemini-2.5-pro")

# OpenAI
model = get_chat_model("openai/gpt-4o")

# Groq (fast inference)
model = get_chat_model("groq/llama-3.3-70b-versatile")

# Local model via llama.cpp
model = get_chat_model("local/llama3")
```

### Adding a Custom Tool

Create `tools/weather_tool.py`:

```python
from tools.tool import Tools
from tools.chroma_tools import register_tool

def get_weather(city: str) -> str:
    # your implementation
    return f"It is sunny in {city}."

weather_tool = Tools(
    name="get_weather",
    description="Gets the current weather for a given city.",
    input_schema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "The city name."}
        },
        "required": ["city"]
    },
    func=get_weather
)

register_tool(weather_tool)
```

Then import it in `main.py`:

```python
import tools.weather_tool  # importing triggers registration
```

Now the agent can automatically discover and use `get_weather` when asked about the weather — no other changes needed.

### Sample Agent Output

```
User: Find a tool that can open a website, and then use it to open https://github.com/Naman1223

---> AI is calling tool: 'find_relevant_tools'
---> Arguments: {'query': 'open website'}
---> Result: [{'name': 'open_chrome', 'description': "Opens a specified URL in the user's web browser..."}]

---> AI is calling tool: 'execute_dynamic_tool'
---> Arguments: {'tool_name': 'open_chrome', 'arguments': {'url': 'https://github.com/Naman1223'}}
---> Result: Successfully opened https://github.com/Naman1223 in the browser.

AI: I found the tool open_chrome and used it to successfully open the website in your browser.
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `openai` | OpenAI, Grok, Groq, and OpenRouter clients (OpenAI-compatible API) |
| `anthropic` | Anthropic Claude client |
| `google-genai` | Google Gemini client |
| `huggingface-hub` | HuggingFace inference client |
| `llama-cpp-python` | Local GGUF model inference via llama.cpp |
| `chromadb` | Vector database for semantic tool search and storage |
| `moonshine-voice` | Real-time on-device speech-to-text (English) |
| `python-dotenv` | `.env` file loading |
| `pydantic` | Data validation |

---

## 🗺️ Roadmap

- [ ] Voice-to-agent pipeline: pipe STT output directly into `run_agent()`
- [ ] Text-to-speech (TTS) responses for full voice interaction
- [ ] Tool hot-reloading without restarting the agent
- [ ] Web UI / CLI interface
- [ ] More built-in tools (file system, code execution, system info, calendar)
- [ ] Multi-agent orchestration

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.
