from langgraph.graph import StateGraph , END, START
import listner
from listner import transcription
from typing import Dict, Any , Annotated
from typing_extensions import TypedDict
from operator import add
from langchain_ollama import ChatOllama
import os
from Server import stop , server
server()
transcribe = listner.transcription

class state(TypedDict):
    message: Dict[str, Any] 
    response: str
    


def ollama_node(state: state):
    user_input = transcription()
    if user_input:
        chat = ChatOllama(model="llama3.1")
        response = chat.invoke(user_input)
        print(f"Punisher :{response.content}")
        return {"response": response.content}
    return {"response": "No input detected"}

graph = StateGraph(state)
graph.add_node("ollama", ollama_node)
graph.add_edge(START, "ollama")
graph.add_edge("ollama", END)
app = graph.compile()
app.invoke({"message": {}, "response": {}})

stop()