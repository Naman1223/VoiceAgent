from langchain_community.tools import tool
import os 
import shutil
from pathlib import Path
import asyncio
from langchain_core.tools import tool
from langchain_community.chat_models import ChatOllama
from browser_use import Agent, Browser
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from VectorDB import get_relevant_memory, ingest_documents, doc_db
import subprocess
import platform

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def sub(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

@tool
def mul(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def div(a: int, b: int) -> int:
    """Divide two numbers."""
    return a / b

@tool
def open_file(file_path: str) -> str:
    """Open a file. Supports shortcuts: 'downloads/file.pdf', 'desktop/file.txt', 'documents/file.docx'."""
    try:
        from pathlib import Path
        import platform
        import os
        import subprocess
        
        # Normalize and expand user paths
        if file_path.lower().startswith("downloads"):
            file_path = str(Path.home() / "Downloads" / file_path[len("downloads"):].lstrip("\\/"))
        elif file_path.lower().startswith("desktop"):
            file_path = str(Path.home() / "Desktop" / file_path[len("desktop"):].lstrip("\\/"))
        elif file_path.lower().startswith("documents"):
            file_path = str(Path.home() / "Documents" / file_path[len("documents"):].lstrip("\\/"))
        else:
            file_path = str(Path(file_path).expanduser().resolve())
            
        if not os.path.exists(file_path):
            return f"Error: The file {file_path} does not exist."

        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", file_path])
        else:
            subprocess.call(["xdg-open", file_path])
        return f"File '{file_path}' opened successfully."
    except Exception as e:
        return f"Failed to open file: {str(e)}"


@tool
def create_folder(folder_name: str, directory_path: str = "Desktop") -> str:
    """Create a folder. 'directory_path' can be 'Desktop', 'Documents', or an absolute path."""
    try:
        base = Path.home()
        if directory_path.lower() == "desktop":
            target_dir = base / "Desktop"
        elif directory_path.lower() == "documents":
            target_dir = base / "Documents"
        else:
            target_dir = Path(directory_path).expanduser()

        full_path = target_dir / folder_name
        full_path.mkdir(parents=True, exist_ok=True)
        
        return f"Folder '{folder_name}' successfully created at {full_path.resolve()}"
    except Exception as e:
        return f"Failed to create folder: {str(e)}"

@tool
def delete_file(file_path: str) -> str:
    """Delete a folder or file."""
    try:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                return f"Folder '{file_path}' deleted successfully."
            else:
                os.remove(file_path)
                return f"File '{file_path}' deleted successfully."
        else:
            return f"Error: Path '{file_path}' does not exist."
    except Exception as e:
        return f"Error deleting '{file_path}': {str(e)}"

@tool
def terminal(command: str) -> str:
    """Run a terminal command."""
    try:
        result = os.system(command)
        return f"Command '{command}' executed successfully."
    except Exception as e:
        return f"Failed to execute command: {str(e)}"

@tool
def ChatHistory(query: str):
    """Get the chat history from the ChromaDataBase given a query."""
    return get_relevant_memory(query)

@tool
def IngestDocuments(directory_path: str):
    """Ingest a .txt file from a directory into the knowledge base."""
    return ingest_documents(directory_path)

@tool
def search_knowledge_base(query: str) -> str:
    """Search the user's personal documents and knowledge base for an answer."""
    results = doc_db.similarity_search(query, k=3)
    if not results:
        return "Nothing found in the knowledge base regarding this topic."
    
    context = "\n---\n".join([res.page_content for res in results])
    return f"Retrieved Context:\n{context}"


# Tool groups — bind only what's needed per intent to minimize token overhead
MATH_TOOLS = [add, sub, mul, div]
FILE_TOOLS = [open_file, create_folder, delete_file, terminal]
MEMORY_TOOLS = [ChatHistory, IngestDocuments, search_knowledge_base]

# Full list (fallback / import convenience)
tools = MATH_TOOLS + FILE_TOOLS + MEMORY_TOOLS