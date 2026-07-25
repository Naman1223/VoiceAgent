from dotenv import load_dotenv
import json
from core.Models import get_chat_model
from tools.chroma_tools import tool_query_tool, tool_execute_tool, TOOL_REGISTRY

import tools.web_tools 

load_dotenv() 

def run_agent(prompt: str):
    model = get_chat_model("google/gemini-3.5-flash")
    
    available_tools = [tool_query_tool, tool_execute_tool]
    openai_tools = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.input_schema
            }
        }
        for t in available_tools
    ]

    messages = [{"role": "user", "content": prompt}]
    print(f"User: {prompt}\n")
    
    # 2. The Tool-Calling Loop
    while True:
        # Call the LLM via unified provider-agnostic method
        response = model.chat_with_tools(messages=messages, tools=openai_tools)
        
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

if __name__ == "__main__":
    try:
        # Let's test if the AI can use the Chroma tools to find the Chrome tool and run it!
        run_agent("Find a tool that can open a website, and then use it to open https://github.com/Naman1223")
    except Exception as e:
        print(f"Failed to run: {e}")
