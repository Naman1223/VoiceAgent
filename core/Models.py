from dotenv import load_dotenv
import os
import logging
import sys
from pathlib import Path

# Add project root to sys.path to allow importing Settings when running directly
sys.path.append(str(Path(__file__).resolve().parent.parent))
import Settings

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

class VanillaChatModel:
    """A minimal wrapper to unify the interface of various model providers without LangChain."""
    def __init__(self, provider, client, model, model_kwargs):
        self.provider = provider.lower()
        self.client = client
        self.model = model
        self.model_kwargs = model_kwargs

    def invoke(self, prompt: str) -> str:
        temperature = self.model_kwargs.get("temperature", 0.2)
        max_tokens = self.model_kwargs.get("max_tokens", 256)

        if self.provider in ["openai", "openrouter"]:
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
            # For Google, the client is actually the GenerativeModel instance
            response = self.client.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens
                }
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
    allowed_models = Models_loader()

    if requested_model_name not in allowed_models:
        logging.error(f"'{requested_model_name}' is unauthorized or missing from Model_list.txt")
        raise ValueError(f"'{requested_model_name}' is unauthorized or missing from Model_list.txt")
    
    if "/" not in requested_model_name:
        logging.error(f"Invalid format inside file: '{requested_model_name}'. Must use 'provider/model'.")
        raise ValueError(f"Invalid format inside file: '{requested_model_name}'. Must use 'provider/model'.")

    provider, actual_model = requested_model_name.split("/", 1)
    
    if provider.lower() == "local":
        local_model_path = kwargs.pop("model_path", None) or os.environ.get("LOCAL_MODEL_PATH")
        if not local_model_path:
            local_model_path = input("Enter the full path to your local model: \n")
        llm = Settings.local_model_Settings(local_model_path, **kwargs)
        return VanillaChatModel("local", llm, actual_model, kwargs)
    
    model_kwargs = Settings.closed_model_settings(provider)
    model_kwargs.update(kwargs)
    
    api_key = model_kwargs.get("api_key")

    if provider.lower() == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        return VanillaChatModel("openai", client, actual_model, model_kwargs)

    elif provider.lower() == "anthropic":
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        return VanillaChatModel("anthropic", client, actual_model, model_kwargs)

    elif provider.lower() == "google":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        client = genai.GenerativeModel(actual_model)
        return VanillaChatModel("google", client, actual_model, model_kwargs)

    elif provider.lower() == "huggingface":
        from huggingface_hub import InferenceClient
        client = InferenceClient(model=actual_model, token=api_key)
        return VanillaChatModel("huggingface", client, actual_model, model_kwargs)

    elif provider.lower() == "openrouter":
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        return VanillaChatModel("openrouter", client, actual_model, model_kwargs)

    else:
        logging.error(f"No handler found for provider: '{provider}'")
        raise ValueError(f"No handler found for provider: '{provider}'")


