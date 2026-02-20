from langgraph.graph import StateGraph , END, START
import listner
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

t = threading.Thread(target=server())
t.start()
transcribe = listner.transcription


from operator import add
from typing import Annotated, List

class state(TypedDict):
    messages: Annotated[List[Any], add]
    response: str


from langchain_core.messages import HumanMessage, SystemMessage

def ollama_node(state: state):
    is_first_message = not state.get("messages")
    
    if is_first_message:
        user_input = transcription()
        if not user_input:
             return {"response": "No input detected"}
        user_msg = HumanMessage(content=user_input)
        messages = [user_msg]
    else:
        messages = state["messages"]

    chat = ChatOllama(model="llama3.1", temperature=0)
    model_with_tools = chat.bind_tools(tools)
    
    sys_prompt = SystemMessage(content="You are a helpful voice assistant. You perform tasks using tools. If you have just used a tool, briefly confirm the action to the user in plain English (e.g., 'I have deleted the folder.'). NEVER output JSON, raw tool responses, or tool schemas in your final response. Just speak conversationally and concisely.")
    response = model_with_tools.invoke([sys_prompt] + messages)
    
    if response.content:
        print(f"Punisher :{response.content}")
    

    if is_first_message:
        return {"messages": [user_msg, response], "response": response.content}
    else:
        return {"messages": [response], "response": response.content}

graph = StateGraph(state)
graph.add_node("ollama", ollama_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "ollama")
def should_continue(state: state):
    messages = state.get("messages", [])
    if not messages:
        return END
    last_message = messages[-1]
    # Check if there are tool calls to invoke
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

graph.add_conditional_edges("ollama", should_continue)
graph.add_edge("tools", "ollama")

app = graph.compile()
app.invoke({"messages": [], "response": ""})

