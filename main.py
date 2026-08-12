from dotenv import load_dotenv
import json
from core.Models import get_chat_model
from tools.chroma_tools import tool_query_tool, tool_execute_tool, TOOL_REGISTRY
import tools.OS_tools
import tools.web_tools 
from Memory.Long_memory import append_message, search_memory_tool
from datetime import datetime
load_dotenv()

SYSTEM_PROMPT = """
You are VoxCode, a helpful AI agent running on Windows.
You have access to a dynamic tool registry.

Guidelines:
- Operating System: Windows (use Windows terminal / PowerShell commands like `start <app>`).
- Once a command to launch/open an application succeeds, STOP calling further tools immediately.
- If a tool call fails, report the error clearly and do not retry endlessly with other platform commands (e.g. do not try Linux or macOS commands on Windows).
- Be concise. Avoid unnecessary commentary.

IMPORTANT - Tool Usage Rules:
- Only call tools when the user's request requires a real action (e.g. opening an app, running a command, searching the web, reading a file, or fetching past memory).
- If the user asks about past interactions, previous context, or personal facts (e.g. "what is my name"), you MUST use the `search_memory` tool to fetch the context before answering.
- Do NOT call any tools for pure chitchat, greetings, or general knowledge questions (e.g. "Hello", "What is Python?").
- If no tool is needed, respond directly with plain text. Do not look up tools, do not call tool_query_tool, do not call tool_execute_tool unless an actual task demands it.
"""


def run_agent(prompt: str):
    model = get_chat_model("groq/llama-3.3-70b-versatile")

    context_prompt = "Current Task:\n" + prompt

    TOOL_REGISTRY[search_memory_tool.name] = search_memory_tool
    CACHED_TOOLS = [tool_query_tool, tool_execute_tool, tools.OS_tools.terminal_tool, search_memory_tool]

    _cached_tools_openai = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.input_schema
            }
        }
        for t in CACHED_TOOLS
    ]

    # In the future, dynamically added tools can be appended here
    _all_tools_openai = list(_cached_tools_openai)


    messages = [{"role": "user", "content": context_prompt}]
    print(f"User: {prompt}\n")

    
    # 2. The Tool-Calling Loop
    while True:
        # Call the LLM via unified provider-agnostic method
        response = model.chat_with_tools(
            messages=messages, 
            tools=_all_tools_openai, 
            cached_tools=_cached_tools_openai,
            system_prompt=SYSTEM_PROMPT
        )
        
        # If the LLM has a normal text response, print it
        if response["content"]:
            print(f"AI: {response['content']}")
        
        # Append the model's raw message object (or a plain dict) to history
        messages.append({"role": "assistant", "content": response["content"], "raw": response["raw"]})
        
        # If no tools were called, the task is finished
        if not response["tool_calls"]:
            break
            
        # 3. Execute the requested tools
        for tool_call in response["tool_calls"]:
            print(f"---> AI is calling tool: '{tool_call['name']}'")
            # arguments may be a dict (Google/Anthropic) or a JSON string (OpenAI)
            args = tool_call["arguments"] if isinstance(tool_call["arguments"], dict) else json.loads(tool_call["arguments"])
            print(f"---> Arguments: {args}")
            
            # Find and execute the tool from our registry
            if tool_call["name"] in TOOL_REGISTRY:
                result = TOOL_REGISTRY[tool_call["name"]].func(**args)
            else:
                result = f"Error: Tool {tool_call['name']} not found."
                
            print(f"---> Result: {result}\n")
            
            # 4. Give the result back to the LLM so it can continue
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": tool_call["name"],
                "content": str(result)
            })
            append_message(prompt, result, datetime.now(), messages, tool_call)

if __name__ == "__main__":
    try:
        run_agent("what is  my name")
    except Exception as e:
        print(f"Failed to run: {e}")
