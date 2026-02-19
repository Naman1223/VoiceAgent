from langgraph.graph import StateGraph , END, START
import listner
from listner import transcription
from typing import Dict, Any , Annotated
from typing_extensions import TypedDict
from operator import add
from langchain_ollama import ChatOllama


transcribe = listner.transcription
class state(TypedDict):
    message: Annotated[str, add]
    

def ollama_node(state:state):
    user_input = transcription()
    if user_input:
        chat = ChatOllama(model="llama3.1")
        response = chat.invoke(user_input)
        print(f"Punisher :{response.content}")
    return {"message": response.content}

ollama_node(state)