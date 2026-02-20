from langchain_community.tools import tool
import os 
import shutil
from pathlib import Path

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

    """Create a folder or file an a Location on the Drive"""
    try:
        os.makedirs(folder_name_path, exist_ok=True)
        return f"Folder '{folder_name_path}' created successfully."
    except Exception as e:
        return f"Error creating '{folder_name_path}': {str(e)}"



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
def apps(command:str) -> str:
    """open apps."""
    try:
        result = os.system("start " + command)
        return f"Command '{command}' executed successfully."
    except Exception as e:
        return f"Failed to execute command: {str(e)}"

tools = [add, sub, mul, div, create_folder, delete_file, terminal, apps]