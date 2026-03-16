from langchain_community.tools import tool
import os 
import shutil
from pathlib import Path
import asyncio
from langchain_core.tools import tool
from langchain_community.chat_models import ChatOllama
from browser_use import Agent, Browser

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

import asyncio
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from browser_use import Agent, Browser

import asyncio
from langchain_ollama import ChatOllama
from browser_use import Agent, Browser

@tool
def browser_tool(url: str):
    """
    Opens a visible Chrome window and navigates to a URL using a local LLM.
    """
    # Initialize the LLM
    llm = ChatOllama(model="hermes3:8b", temperature=0.3)
    
    # Ensure provider attribute exists for compatibility
    try:
        if not hasattr(llm, 'provider'):
            setattr(llm, 'provider', 'ollama')
    except ValueError:
        pass

    async def run_browser():
        # Initialize browser within the async function to manage lifecycle
        browser_inst = Browser(headless=False, disable_security=True)
        try:
            agent = Agent(
                task=f"Go to {url}, wait for the page to load, and summarize the top headline or main content.",
                llm=llm,
                browser=browser_inst
            )
            result = await agent.run()
            return result
        finally:
            await browser_inst.close()

    try:
        # Handling the event loop for various environments
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            # If the loop is already running, we run the coroutine directly
            return asyncio.gather(run_browser()) 
        else:
            return asyncio.run(run_browser())

    except Exception as e:
        return f"Error accessing the browser: {str(e)}"

tools = [add, sub, mul, div, create_folder, delete_file, terminal, apps, browser_tool]