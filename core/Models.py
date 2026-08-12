from dotenv import load_dotenv
import os
import logging
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional
import Settings

sys.path.append(str(Path(__file__).resolve().parent.parent))


load_dotenv()

try:
    base_dir = Path(__file__).resolve().parent.parent
    folder = base_dir / "Logs"
    folder.mkdir(parents=True, exist_ok=True)
    log_kwargs = {"filename": str(folder / "Models.log"), "filemode": "a"}
except Exception as e:
    print(f"Warning: Could not create Logs folder. Logging to console instead.")
    log_kwargs = {}

logging.basicConfig(
    **log_kwargs,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

# --- Schema & Message Conversion Helpers ---

def openai_to_gemini_schema(tools: list) -> list:
    """Converts OpenAI tool schemas to Google Gemini Tool declarations."""
    from google.genai import types as genai_types
    google_tools = []
    for t in tools:
        fn = t["function"]
        google_tools.append(
            genai_types.Tool(
                function_declarations=[
                    genai_types.FunctionDeclaration(
                        name=fn["name"],
                        description=fn["description"],
                        parameters=fn.get("parameters", {}),
                    )
                ]
            )
        )
    return google_tools

def openai_to_anthropic_schema(tools: list, cache_cutoff_name: Optional[str] = None) -> list:
    """Converts OpenAI tool schemas to Anthropic tool declarations, with optional caching."""
    anthropic_tools = []
    for t in tools:
        anth_t = {
            "name": t["function"]["name"],
            "description": t["function"]["description"],
            "input_schema": t["function"].get("parameters", {})
        }
        if cache_cutoff_name and t["function"]["name"] == cache_cutoff_name:
            anth_t["cache_control"] = {"type": "ephemeral"}
        anthropic_tools.append(anth_t)
    return anthropic_tools

def openai_to_gemini_messages(messages: list) -> list:
    """Converts standard conversation messages to Google Gemini Content format."""
    from google.genai import types as genai_types
    google_contents = []
    for m in messages:
        role = m["role"]
        if role == "user":
            google_contents.append(genai_types.Content(role="user", parts=[genai_types.Part(text=m["content"])]))
        elif role in ("assistant", "model"):
            raw = m.get("raw")
            if raw is not None:
                google_contents.append(raw)  # Already a Google Content object
            else:
                google_contents.append(genai_types.Content(role="model", parts=[genai_types.Part(text=m.get("content", ""))]))
        elif role == "tool":
            google_contents.append(
                genai_types.Content(
                    role="user",
                    parts=[genai_types.Part(
                        function_response=genai_types.FunctionResponse(
                            name=m["name"],
                            response={"result": m["content"]}
                        )
                    )]
                )
            )
    return google_contents

def clean_openai_messages(messages: list, system_prompt: Optional[str] = None) -> list:
    """Strips internal keys and readies standard messages for OpenAI's API."""
    final_messages = []
    if system_prompt:
        final_messages.append({"role": "system", "content": system_prompt})
        
    for m in messages:
        if m["role"] == "assistant" and m.get("raw") is not None and hasattr(m["raw"], "model_dump"):
            # OpenAI's SDK returns a Pydantic model for messages, dump it back to dict
            final_messages.append(m["raw"].model_dump(exclude_none=True))
        else:
            # Strip internal keys like 'raw' and empty optional fields
            cleaned_msg = {}
            for k, v in m.items():
                if k == "raw":
                    continue
                if k == "tool_calls" and not v:
                    continue
                cleaned_msg[k] = v
            final_messages.append(cleaned_msg)
    return final_messages


@dataclass
class VanillaChatModel:
    """A minimal wrapper to unify the interface of various model providers without LangChain."""
    provider: str
    client: Any
    model: str
    model_kwargs: dict
    # Internal cache name for Google CachedContent; managed automatically.
    _google_cache_name: Optional[str] = field(default=None, repr=False)
    # Token count to keep in llama.cpp KV cache
    _local_n_keep: int = field(default=0, repr=False)

    def __post_init__(self):
        self.provider = self.provider.lower()

    def chat_with_tools(self, messages: list, tools: list, cached_tools: Optional[list] = None, system_prompt: Optional[str] = None) -> dict:
        """
        Calls the model with tool-calling support and returns a unified response dict.
        Routes the request to the appropriate provider handler.
        """
        if self.provider in ["openai", "openrouter", "grok", "groq"]:
            return self._chat_openai(messages, tools, system_prompt)
        elif self.provider == "google":
            return self._chat_google(messages, tools, cached_tools, system_prompt)
        elif self.provider == "anthropic":
            return self._chat_anthropic(messages, tools, cached_tools, system_prompt)
        elif self.provider == "local":
            return self._chat_local(messages, tools, cached_tools, system_prompt)
        else:
            raise ValueError(f"Tool-calling not supported for provider: {self.provider}")

    def _chat_openai(self, messages: list, tools: list, system_prompt: Optional[str]) -> dict:
        final_messages = clean_openai_messages(messages, system_prompt)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=final_messages,
            tools=tools,
            tool_choice="auto",
            temperature=self.model_kwargs.get("temperature", 0.1),
        )
        msg = response.choices[0].message
        tool_calls = None
        if msg.tool_calls:
            tool_calls = [
                {"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments}
                for tc in msg.tool_calls
            ]
        elif msg.content:
            import re
            pattern = r"<function[=/](\w+)>(.*?)</function>"
            matches = re.findall(pattern, msg.content, re.DOTALL)
            if matches:
                tool_calls = []
                for i, (func_name, func_args) in enumerate(matches):
                    tool_calls.append({
                        "id": f"call_{func_name}_{i}",
                        "name": func_name,
                        "arguments": func_args.strip()
                    })
                cleaned_content = re.sub(pattern, "", msg.content, flags=re.DOTALL).strip()
                return {"content": cleaned_content if cleaned_content else None, "tool_calls": tool_calls, "raw": msg}

        return {"content": msg.content, "tool_calls": tool_calls, "raw": msg}

    def _chat_google(self, messages: list, tools: list, cached_tools: Optional[list], system_prompt: Optional[str]) -> dict:
        from google.genai import types as genai_types

        google_tools = openai_to_gemini_schema(tools)
        _tools_to_cache = cached_tools if cached_tools is not None else tools
        google_cached_tools = openai_to_gemini_schema(_tools_to_cache)

        gen_config_kwargs: dict = {"temperature": self.model_kwargs.get("temperature", 0.1)}

        if system_prompt and not self._google_cache_name:
            try:
                cached = self.client.caches.create(
                    model=self.model,
                    config=genai_types.CreateCachedContentConfig(
                        system_instruction=system_prompt,
                        tools=google_cached_tools,
                        ttl="600s",
                    )
                )
                self._google_cache_name = cached.name
                logging.info(f"Google CachedContent created: {cached.name}")
            except Exception as e:
                logging.warning(f"Google CachedContent creation failed (token minimum not met?), falling back to uncached: {e}")

        if self._google_cache_name:
            gen_config_kwargs["cached_content"] = self._google_cache_name
        else:
            gen_config_kwargs["tools"] = google_tools
            if system_prompt:
                gen_config_kwargs["system_instruction"] = system_prompt

        google_contents = openai_to_gemini_messages(messages)

        response = self.client.models.generate_content(
            model=self.model,
            contents=google_contents,
            config=genai_types.GenerateContentConfig(**gen_config_kwargs)
        )

        candidate = response.candidates[0]
        content_text = None
        tool_calls = None

        for part in candidate.content.parts:
            if hasattr(part, "function_call") and part.function_call:
                fc = part.function_call
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append({
                    "id": fc.name,
                    "name": fc.name,
                    "arguments": dict(fc.args) if fc.args else {}
                })
            elif hasattr(part, "text") and part.text:
                content_text = part.text

        return {"content": content_text, "tool_calls": tool_calls, "raw": candidate.content}

    def _chat_anthropic(self, messages: list, tools: list, cached_tools: Optional[list], system_prompt: Optional[str]) -> dict:
        _tools_to_cache = cached_tools if cached_tools is not None else tools
        cache_cutoff_name = _tools_to_cache[-1]["function"]["name"] if _tools_to_cache else None
        
        anthropic_tools = openai_to_anthropic_schema(tools, cache_cutoff_name)

        system_msg = system_prompt
        filtered = []
        for m in messages:
            if m["role"] == "system" and not system_msg:
                system_msg = m["content"]
            else:
                filtered.append({"role": m["role"], "content": m["content"]})

        kwargs: dict = {
            "model": self.model,
            "messages": filtered,
            "tools": anthropic_tools,
            "max_tokens": self.model_kwargs.get("max_tokens", 4096),
        }
        if system_msg:
            kwargs["system"] = [
                {"type": "text", "text": system_msg, "cache_control": {"type": "ephemeral"}}
            ]

        response = self.client.messages.create(**kwargs)

        content_text = None
        tool_calls = None
        for block in response.content:
            if block.type == "text":
                content_text = block.text
            elif block.type == "tool_use":
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append({"id": block.id, "name": block.name, "arguments": block.input})
        return {"content": content_text, "tool_calls": tool_calls, "raw": response}

    def _chat_local(self, messages: list, tools: list, cached_tools: Optional[list], system_prompt: Optional[str]) -> dict:
        import json
        final_messages = messages
        if system_prompt:
            final_messages = [{"role": "system", "content": system_prompt}] + messages
        
        kwargs = {
            "messages": final_messages,
            "temperature": self.model_kwargs.get("temperature", 0.1)
        }
        if tools:
            kwargs["tools"] = tools

        if self._local_n_keep == 0 and system_prompt:
            _tools_to_cache = cached_tools if cached_tools is not None else tools
            prefix_str = f"<system>\n{system_prompt}\nTools:\n{json.dumps(_tools_to_cache)}\n</system>\n"
            tokens = self.client.tokenize(prefix_str.encode("utf-8"))
            self._local_n_keep = len(tokens)
            logging.info(f"llama.cpp KV cache initialized with n_keep={self._local_n_keep}")

        if self._local_n_keep > 0:
            kwargs["extra_body"] = {"n_keep": self._local_n_keep}

        response = self.client.create_chat_completion(**kwargs)
        
        msg = response["choices"][0]["message"]
        content = msg.get("content")
        
        tool_calls = None
        if "tool_calls" in msg and msg["tool_calls"]:
            tool_calls = [
                {"id": tc["id"], "name": tc["function"]["name"], "arguments": tc["function"]["arguments"]}
                for tc in msg["tool_calls"]
            ]
        
        return {"content": content, "tool_calls": tool_calls, "raw": msg}

    def invoke(self, prompt: str) -> str:
        temperature = self.model_kwargs.get("temperature")
        max_tokens = self.model_kwargs.get("max_tokens")

        if self.provider in ["openai", "openrouter", "grok", "groq"]:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.content[0].text

        elif self.provider == "google":
            from google import genai
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text

        elif self.provider == "huggingface":
            response = self.client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

        elif self.provider == "local":
            # For local, the client is the Llama instance
            response = self.client(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response["choices"][0]["text"]
        
        else:
            raise ValueError(f"Unsupported provider for invoke: {self.provider}")

def Models_loader():
    try:
        logging.info("Loading models from Model_list.txt")
        file_path = Path(__file__).parent / "Mod" / "Model_list.txt"
        with open(file_path, 'r', encoding='utf-8') as file:
            return [model.strip() for model in file.read().split("\n") if model.strip()]
    except FileNotFoundError:
        logging.error("Error: Model list file not found.")
        return []

def get_chat_model(requested_model_name: str, **kwargs):
    """
    Model router: Initializes the appropriate client for the requested provider.
    """
    allowed_models = Models_loader()

    if requested_model_name not in allowed_models:
        logging.error(f"'{requested_model_name}' is unauthorized or missing from Model_list.txt")
        raise ValueError(f"'{requested_model_name}' is unauthorized or missing from Model_list.txt")
    
    if "/" not in requested_model_name:
        logging.error(f"Invalid format inside file: '{requested_model_name}'. Must use 'provider/model'.")
        raise ValueError(f"Invalid format inside file: '{requested_model_name}'. Must use 'provider/model'.")

    provider, actual_model = requested_model_name.split("/", 1)
    provider = provider.lower()
    
    if provider == "local":
        local_model_path = kwargs.pop("model_path", None) or os.environ.get("LOCAL_MODEL_PATH")
        if not local_model_path:
            local_model_path = input("Enter the full path to your local model: \n")
        llm = Settings.local_model_Settings(local_model_path, **kwargs)
        gen_kwargs = Settings.local_generation_settings(**kwargs)
        return VanillaChatModel("local", llm, actual_model, gen_kwargs)
    
    model_kwargs = Settings.closed_model_settings(provider)
    model_kwargs.update(kwargs)
    api_key = model_kwargs.get("api_key")

    client_builders = {
        "openai": lambda key: __import__('openai').OpenAI(api_key=key),
        "anthropic": lambda key: __import__('anthropic').Anthropic(api_key=key),
        "google": lambda key: __import__('google.genai').genai.Client(api_key=key),
        "huggingface": lambda key: __import__('huggingface_hub').InferenceClient(model=actual_model, token=key),
        "openrouter": lambda key: __import__('openai').OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key),
        "grok": lambda key: __import__('openai').OpenAI(base_url="https://api.x.ai/v1", api_key=key),
        "groq": lambda key: __import__('openai').OpenAI(base_url="https://api.groq.com/openai/v1", api_key=key),
    }

    if provider in client_builders:
        client = client_builders[provider](api_key)
        return VanillaChatModel(provider, client, actual_model, model_kwargs)
    
    logging.error(f"No handler found for provider: '{provider}'")
    raise ValueError(f"No handler found for provider: '{provider}'")
