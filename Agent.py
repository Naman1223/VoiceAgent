from langgraph.graph import StateGraph , END, START
import listner
from listner import transcription
from typing import Dict, Any , Annotated
from typing_extensions import TypedDict
from operator import add
from langchain_ollama import ChatOllama
import os
from Server import stop , server

from tools.basic_tools import tools
from langgraph.prebuilt import ToolNode, tools_condition

server()
transcribe = listner.transcription


from operator import add
from typing import Annotated, List

class state(TypedDict):
    messages: Annotated[List[Any], add]
    response: str


def ollama_node(state: state):
    if not state.get("messages"):
        user_input = transcription()
        if not user_input:
             return {"response": "No input detected"}
        messages = [{"role": "user", "content": user_input}]
    else:
        messages = state["messages"]

    chat = ChatOllama(model="llama3.1")
    model_with_tools = chat.bind_tools(tools)
    response = model_with_tools.invoke(messages)
    print(f"Punisher :{response.content}")
    return {"messages": [response], "response": response.content}

graph = StateGraph(state)
graph.add_node("ollama", ollama_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "ollama")
graph.add_conditional_edges("ollama", tools_condition)
graph.add_edge("tools", "ollama")

app = graph.compile()
app.invoke({"messages": [], "response": ""})

stop()