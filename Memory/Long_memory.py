import chromadb
import json
from datetime import datetime
from tools.tool import Tools
from tools.schemas import SEARCH_MEMORY_SCHEMA

chroma_client = chromadb.PersistentClient(path="./database/chroma_db")
Long_memory = chroma_client.get_or_create_collection(name="Long_Memory")


def append_message(prompt: str, result, timestamp: datetime, messages: list, tool_call: dict):

    """Persist a tool interaction to long-term ChromaDB memory."""
    doc = json.dumps({
        "prompt": prompt,
        "tool": tool_call.get("name"),
        "arguments": tool_call.get("arguments"),
        "result": str(result),
        "message_count": len(messages),
    })
    doc_id = f"{timestamp.isoformat()}_{tool_call.get('id', 'unknown')}"
    Long_memory.add(
        documents=[doc],
        ids=[doc_id],
        metadatas=[{"timestamp": timestamp.isoformat(), "tool": tool_call.get("name")}],
    )

def fetch_long_memory(query: str, n_results: int = 5):
    """Fetch relevant past tool interactions using ChromaDB."""
    results = Long_memory.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return results

def search_memory_tool_func(query: str, n_results: int = 3) -> str:
    """Tool function to search memory and return formatted string."""
    history_results = fetch_long_memory(query, n_results=n_results)
    relevant_history = []
    if history_results and history_results.get("documents"):
        for doc, meta in zip(history_results["documents"][0], history_results["metadatas"][0]):
            relevant_history.append(f"[MEMORY - {meta['tool']} - {meta['timestamp']}]: {doc}")
    
    if relevant_history:
        return "Relevant previous interactions:\n" + "\n".join(relevant_history)
    return "No relevant past memories found."

search_memory_tool = Tools(
    name="search_memory",
    description="Searches the AI's long-term memory for past interactions and context. Use this when you need to recall previous conversations or actions.",
    input_schema=SEARCH_MEMORY_SCHEMA,
    func=search_memory_tool_func
)