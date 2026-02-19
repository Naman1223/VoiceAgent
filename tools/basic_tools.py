from langchain_community.tools import tool

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
def create_folder(folder_name: str) -> str:
    """Create a folder."""
    import os
    os.makedirs(folder_name, exist_ok=True)
    return f"Folder '{folder_name}' created successfully."



@tool
def delete_file(file_path: str) -> str:
    """Delete a file."""
    os.remove(file_path)
    return f"File '{file_path}' deleted successfully."

tools = [add, sub, mul, div, create_folder, delete_file]