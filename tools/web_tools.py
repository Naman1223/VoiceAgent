import webbrowser
from tools.tool import Tools
from tools.schemas import OPEN_CHROME_SCHEMA
from tools.chroma_tools import register_tool

def open_in_chrome(url: str) -> str:
    """
    Opens the provided URL in the default web browser (which is usually Chrome).
    """
    try:
        # webbrowser.open returns True if a browser was successfully launched
        success = webbrowser.open(url)
        if success:
            return f"Successfully opened {url} in the browser."
        else:
            return f"Failed to open {url}. Check if a default browser is set."
    except Exception as e:
        return f"Error opening browser: {str(e)}"

# Create the tool instance
open_chrome_tool = Tools(
    name="open_chrome",
    description="Opens a specified URL in the user's web browser. Use this when the user asks to open a website, search the web, or view a specific link.",
    input_schema=OPEN_CHROME_SCHEMA,
    func=open_in_chrome
)

# Register the tool into ChromaDB and our execution registry
register_tool(open_chrome_tool)
