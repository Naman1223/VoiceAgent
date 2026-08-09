import chromadb
import json
from datetime import datetime

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