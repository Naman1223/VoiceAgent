from langgraph.graph import StateGraph , END, START
from listner import transcription
from typing import Dict, Any , Annotated
from typing_extensions import TypedDict
from operator import add
from langchain_ollama import ChatOllama
import os
from Server import server
import threading
from tools.basic_tools import tools
from langgraph.prebuilt import ToolNode, tools_condition
from kokoro import KPipeline
import sounddevice as sd
import soundfile as sf

t = threading.Thread(target=server())
t.start()


from operator import add
from typing import Annotated, List

class state(TypedDict):
    messages: Annotated[List[Any], add]
    response: str


from langchain_core.messages import HumanMessage, SystemMessage

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

    chat = ChatOllama(model="llama3.1", temperature=0.3)
    model_with_tools = chat.bind_tools(tools)
    
    sys_prompt = SystemMessage(content="You are Punisher, a friendly, intelligent, and conversational AI voice assistant. You love to chat and answer questions openly. You also have access to tools. If the user asks you to perform a task, use the appropriate tool. IMPORTANT: Tool execution must be done behind the scenes! NEVER output raw JSON, markdown blocks, {\"name\": ...} payloads, or raw tool schemas in your spoken response. Just confirm what you did naturally and concisely.")
    response = model_with_tools.invoke([sys_prompt] + messages)
    
    if response.content:
        print(f"Punisher :{response.content}")
    
    return {"messages": [response], "response": response.content}

def should_continue(state: state):
    messages = state.get("messages", [])
    if not messages:
        return END
    last_message = messages[-1]
    # Check if there are tool calls to invoke
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
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

app = graph.compile()

pipeline = KPipeline(lang_code='a')

conversation_state = {"messages": [], "response": ""}

print("Starting conversation loop. Say 'exit', 'bye', or 'quit' to end.")

while True:
    # Run one pass of the graph
    result = app.invoke(conversation_state)
    
    # Update conversation history
    conversation_state["messages"] = result["messages"]
    
    # Check if user wanted to exit
    user_msgs = [m for m in result["messages"] if isinstance(m, HumanMessage)]
    if user_msgs:
        last_user_text = user_msgs[-1].content.lower().strip()
        if any(word in last_user_text for word in ["exit", "bye", "goodbye", "quit"]):
            print("Exiting conversation.")
            break
            
    # Speak the response
    response_text = result.get('response', '')
    if response_text:
        generator = pipeline(response_text, voice='af_heart')
        for i, (gs, ps, audio) in enumerate(generator):
            sd.play(audio, samplerate=24000)
            sd.wait()