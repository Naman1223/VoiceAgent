from langgraph.graph import StateGraph , END, START
from listner import transcription
from typing import Dict, Any , Annotated
from typing_extensions import TypedDict
from operator import add
from langchain_ollama import ChatOllama
import os
from Server import server
import threading
from tools.basic_tools import tools, MATH_TOOLS, FILE_TOOLS, MEMORY_TOOLS
from langgraph.prebuilt import ToolNode, tools_condition
from kokoro_onnx import Kokoro
import sounddevice as sd
import soundfile as sf
import subprocess
from VectorDB import save_to_memory , get_relevant_memory
import uuid

t = threading.Thread(target=server)
t.start()


from operator import add
from typing import Annotated, List

class state(TypedDict):
    messages: Annotated[List[Any], add]
    response: str


from langchain_core.messages import HumanMessage, SystemMessage
import queue

# ---------------------------------------------------------------------------
# Pre-cached model bindings — computed once, reused on every turn.
# Binding only the relevant tool group keeps the schema payload small.
# ---------------------------------------------------------------------------
chat = ChatOllama(model="Punisher:latest", temperature=0.3, keep_alive=-1)

model_plain   = chat
model_math    = chat.bind_tools(MATH_TOOLS)
model_file    = chat.bind_tools(FILE_TOOLS)
model_memory  = chat.bind_tools(MEMORY_TOOLS)
model_all     = chat.bind_tools(tools)   # fallback when intent is ambiguous

# Keyword sets per group
_MATH_KWS   = {"add", "subtract", "multiply", "divide", "calculate", "plus", "minus", "times", "convert"}
_FILE_KWS   = {"open", "file", "folder", "create", "delete", "run", "terminal", "command"}
_MEMORY_KWS = {"memory", "history", "remember", "search", "knowledge", "ingest", "database", "recall", "find", "look up"}

def _get_model_for_intent(messages: list):
    """Return the tightest pre-cached model binding that covers the user's intent."""
    # If we are re-entering after a tool result, find out which group ran and reuse it.
    # This avoids binding all tools on the follow-up turn.
    last_tool_name = None
    for m in reversed(messages):
        if m.type == "tool":
            last_tool_name = getattr(m, "name", None)
            break
        if m.type == "human":
            break

    if last_tool_name:
        if any(t.name == last_tool_name for t in MATH_TOOLS):   return model_math
        if any(t.name == last_tool_name for t in FILE_TOOLS):   return model_file
        if any(t.name == last_tool_name for t in MEMORY_TOOLS): return model_memory
        return model_all

    # First turn — classify from the human message text
    last_human = next((m for m in reversed(messages) if m.type == "human"), None)
    if not last_human:
        return model_plain

    text = last_human.content.lower()
    wants_math   = any(k in text for k in _MATH_KWS)
    wants_file   = any(k in text for k in _FILE_KWS)
    wants_memory = any(k in text for k in _MEMORY_KWS)

    active = sum([wants_math, wants_file, wants_memory])
    if active == 0:  return model_plain    # pure conversation — zero schema overhead
    if active == 1:
        if wants_math:   return model_math
        if wants_file:   return model_file
        if wants_memory: return model_memory
    return model_all   # multi-intent — bind everything


def transcribe_node(state: state):
    user_input = transcription()
    if not user_input:
        return {"response": "No input detected"}
    user_msg = HumanMessage(content=user_input)
    return {"messages": [user_msg]}

def ollama_node(state: state):
    messages = state.get("messages", [])
    if not messages:
        return {"response": "No messages to process"}
    recent_messages = messages[-10:]
    
    # Ensure we don't start with an orphaned ToolMessage (which lacks its calling AIMessage).
    while recent_messages and recent_messages[0].type == "tool":
        recent_messages.pop(0)

    model = _get_model_for_intent(recent_messages)

    sys_prompt = SystemMessage(content="You are Punisher, a friendly, intelligent, and conversational AI voice assistant. You love to chat and answer questions openly. You also have access to tools. If the user asks you to perform a task, use the appropriate tool. IMPORTANT: Tool execution must be done behind the scenes! NEVER output raw JSON, markdown blocks, {\"name\": ...} payloads, or raw tool schemas in your spoken response. Just confirm what you did naturally and concisely.")
    
    response_stream = model.stream([sys_prompt] + recent_messages)
    response_text = ""
    accumulated_message = None

    audio_queue = queue.Queue()

    def audio_worker():
        while True:
            text_chunk = audio_queue.get()
            if text_chunk is None:
                break
            if text_chunk.strip():
                try:
                    audio, sample_rate = kokoro.create(text_chunk.strip(), voice='af_heart', speed=1.3, lang="en-us")
                    sd.play(audio, samplerate=sample_rate)
                    sd.wait()
                except Exception as e:
                    pass
            audio_queue.task_done()

    # Start background thread to process audio
    audio_thread = threading.Thread(target=audio_worker)
    audio_thread.start()

    current_sentence = ""
    print("Punisher: ", end="", flush=True)

    for chunk in response_stream:
        if chunk.content:
            text_piece = chunk.content
            print(text_piece, end="", flush=True)
            response_text += text_piece
            current_sentence += text_piece
            
            # If we hit punctuation, send the chunk to the audio thread
            punctuations = ['.', '!', '?']
            if any(p in text_piece for p in punctuations):
                last_punct_idx = max([current_sentence.rfind(p) for p in punctuations])
                if last_punct_idx != -1:
                    chunk_to_play = current_sentence[:last_punct_idx+1]
                    
                    # Avoid sending empty chunks or chunks that are just punctuation
                    if len(chunk_to_play.strip()) > 1:
                        audio_queue.put(chunk_to_play)
                        
                    current_sentence = current_sentence[last_punct_idx+1:]

        if accumulated_message is None:
            accumulated_message = chunk
        else:
            accumulated_message += chunk

    print() # Newline after response

    # Send any remaining words
    if current_sentence.strip():
        audio_queue.put(current_sentence)

    # Gracefully stop the audio worker and wait for it to finish speaking
    audio_queue.put(None)
    audio_thread.join()
    
    if response_text.strip():
        # Find the last actual human message (not a tool result)
        last_human = next((m for m in reversed(messages) if m.type == "human"), None)
        user_text = last_human.content if last_human else ""
        save_to_memory(user_text, response_text)
    
    return {"messages": [accumulated_message], "response": response_text}

def should_continue(state: state):
    messages = state.get("messages", [])
    if not messages:
        return END
    last_message = messages[-1]
    # Check if there are tool calls to invoke
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # Safety net: catch edge cases where intent check missed a tool need
    # and the model emitted a raw JSON-like tool attempt in its content.
    if hasattr(last_message, "content") and '{"name"' in str(last_message.content):
        return "tools"
    return END

graph = StateGraph(state)
graph.add_node("transcribe", transcribe_node)
graph.add_node("ollama", ollama_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "transcribe")
graph.add_edge("transcribe", "ollama")
graph.add_conditional_edges("ollama", should_continue)
graph.add_edge("tools", "ollama")

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
try:
    kokoro.create("Hello.", voice='af_heart', speed=1.5, lang="en-us")
except Exception:
    pass

app = graph.compile()



conversation_state = {"messages": [], "response": ""}

print("Starting conversation loop. Say 'exit', 'bye', or 'quit' to end.")

while True:
    result = app.invoke(conversation_state)
    
    conversation_state["messages"] = result["messages"][-20:]
    
    user_msgs = [m for m in result["messages"] if isinstance(m, HumanMessage)]
    if user_msgs:
        last_user_text = user_msgs[-1].content.lower().strip()
        if any(word in last_user_text for word in ["exit", "bye", "goodbye", "quit"]):
            print("Exiting conversation.")
            subprocess.Popen(["ollama", "stop", "Punisher:latest"], stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            break
