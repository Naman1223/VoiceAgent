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
    """Open a file with file path. If the llm mentions a file anywhere on the system, just pass the filename (e.g., 'resume.pdf') and the code will find it."""
    try:
        from pathlib import Path
        import platform
        import os
        import subprocess
        
        original_path = file_path
        
        # 1. Try if file exists directly
        if not os.path.exists(file_path):
            # 2. Extract just the filename to search for
            search_filename = os.path.basename(original_path)
            if not search_filename:
                search_filename = original_path
                
            found_path = None
            
            # Prioritize fast user directories first, then all other drives
            import string
            drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
            
            search_dirs = [
                str(Path.home() / "Desktop"),
                str(Path.home() / "Downloads"),
                str(Path.home() / "Documents"),
                str(Path.home() / "Pictures")
            ] + drives
            
            for s_dir in search_dirs:
                if found_path:
                    break
                if not os.path.exists(s_dir):
                    continue
                
                for root, dirs, files in os.walk(s_dir):
                    # Skip massive hidden/system folders to keep the search lightning fast
                    skip_dirs = {"AppData", "node_modules", ".venv", "Windows", "Program Files", "Program Files (x86)", "$Recycle.Bin", "ProgramData"}
                    dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
                    
                    # Case insensitive match for the file
                    for f in files:
                        if f.lower() == search_filename.lower() or f.lower() == original_path.lower():
                            found_path = os.path.join(root, f)
                            break
                    if found_path:
                        break
            
            if found_path:
                file_path = found_path
            else:
                file_path = str(Path(original_path).expanduser().resolve())

        if not os.path.exists(file_path):
            return f"Error: The file '{original_path}' could not be found anywhere on the system."

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
    """
    Creates a folder with a specific name at a desired location.
    'directory_path' can be an absolute path, or shorthand like 'Desktop' or 'Documents'.
    """
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


tools = [add, sub, mul, div, create_folder, delete_file, terminal, ChatHistory, IngestDocuments,search_knowledge_base, open_file]