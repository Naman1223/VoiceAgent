FIND_RELEVANT_TOOLS_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "The search query describing what kind of tool is needed."
        },
        "n_results": {
            "type": "integer",
            "description": "The number of top tools to retrieve.",
            "default": 2
        }
    },
    "required": ["query"]
}

EXECUTE_DYNAMIC_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "tool_name": {
            "type": "string",
            "description": "The name of the tool to execute, exactly as returned by find_relevant_tools."
        },
        "arguments": {
            "type": "object",
            "description": "A dictionary of arguments to pass to the tool."
        }
    },
    "required": ["tool_name", "arguments"]
}

OPEN_CHROME_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "description": "The full URL of the website to open (e.g., https://www.google.com)."
        }
    },
    "required": ["url"]
}

TERMINAL_SCHEMA ={
    "type": "object",
    "properties": {
        "command":{
            "type": "string",
            "description": "The command to execute in the terminal."
        }
    },
    "required": ["command"]
}
