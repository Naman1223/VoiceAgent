import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.schemas import TERMINAL_SCHEMA
from tools.chroma_tools import register_tool
from tools.tool import Tools

def run_terminal_commands(command: str) -> str:
    """
    Runs a command in the terminal and returns its output.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        return output.strip() if output.strip() else f"Command '{command}' executed successfully."
    except Exception as e:
        return f"Error executing command: {str(e)}"

terminal_tool = Tools(
    name="run_terminal_commands",
    description="Runs a command in the terminal.",
    input_schema=TERMINAL_SCHEMA,
    func=run_terminal_commands
)

register_tool(terminal_tool)
