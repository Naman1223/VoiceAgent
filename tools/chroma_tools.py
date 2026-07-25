import chromadb
import json
from typing import Any, List, Dict
from tools.tool import Tools
from tools.schemas import FIND_RELEVANT_TOOLS_SCHEMA, EXECUTE_DYNAMIC_TOOL_SCHEMA

# Setup ChromaDB Client and Collection
chroma_client = chromadb.PersistentClient(path="./database/chroma_db")
tool_collection = chroma_client.get_or_create_collection(name="tools_collection")

# A memory registry of the actual callable tools mapped by name.
TOOL_REGISTRY: Dict[str, Tools] = {}

def register_tool(tool: Tools):
    """
    Registers a tool in both the memory registry (so it can be executed)
    and ChromaDB (so it can be searched by the LLM).
    """
    TOOL_REGISTRY[tool.name] = tool
    
    # Store the input schema in metadata so the LLM knows how to use it when found.
    metadata = {
        "input_schema": json.dumps(tool.input_schema)
    }
    
    tool_collection.upsert(
        documents=[tool.description],
        metadatas=[metadata],
        ids=[tool.name]
    )

def query_chromadb_for_tools(query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """
    Searches ChromaDB for the most relevant tools based on the user's query.
    Returns the tool names, descriptions, and schemas so the LLM knows how to call them.
    """
    results = tool_collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    retrieved_tools = []
    if results['documents'] and len(results['documents']) > 0:
        for i in range(len(results['documents'][0])):
            retrieved_tools.append({
                "name": results['ids'][0][i],
                "description": results['documents'][0][i],
                "schema": results['metadatas'][0][i].get("input_schema", "{}") if results['metadatas'] else "{}"
            })
            
    return retrieved_tools

def execute_dynamic_tool(tool_name: str, arguments: dict) -> Any:
    """
    Executes a tool that was dynamically retrieved from ChromaDB.
    """
    if tool_name not in TOOL_REGISTRY:
        return f"Error: Tool '{tool_name}' is not registered or does not exist."
    
    tool = TOOL_REGISTRY[tool_name]
    try:
        # Pass the dictionary of arguments to the tool's function
        return tool.func(**arguments)
    except Exception as e:
        return f"Error executing '{tool_name}': {str(e)}"

# Tool that lets the LLM search for tools
tool_query_tool = Tools(
    name="find_relevant_tools",
    description="Queries the database to find the most appropriate tools for a given task, returning their names and input schemas.",
    input_schema=FIND_RELEVANT_TOOLS_SCHEMA,
    func=query_chromadb_for_tools
)

# Tool that lets the LLM execute a tool it just found
tool_execute_tool = Tools(
    name="execute_dynamic_tool",
    description="Executes a tool retrieved by find_relevant_tools using its exact name and a dictionary of arguments.",
    input_schema=EXECUTE_DYNAMIC_TOOL_SCHEMA,
    func=execute_dynamic_tool
)
