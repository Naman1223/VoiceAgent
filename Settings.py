import os
from llama_cpp import Llama

def local_model_Settings(model_path: str, **kwargs):
    settings = {
        "model_path": model_path,
        "n_ctx": 4096,
        "n_batch": 512,
        "n_gpu_layers": -1,
        "verbose": False,
    }
    # Only update with kwargs that are meant for Llama initialization
    for key in ["n_ctx", "n_batch", "n_gpu_layers", "verbose"]:
        if key in kwargs:
            settings[key] = kwargs[key]

    llm = Llama(**settings)
    return llm

def local_generation_settings(**kwargs):
    settings = {
        "temperature": 0.3,
        "max_tokens": 256,
        "repeat_penalty": 1.1,
    }
    settings.update(kwargs)
    return settings

def get_api_key(provider: str) -> str:
    """Router for API keys based on the provider."""
    if not provider:
        return None
    
    provider = provider.lower()
    if provider == "openai":
        return os.environ.get("OPENAI_API_KEY")
    elif provider == "anthropic":
        return os.environ.get("ANTHROPIC_API_KEY")
    elif provider == "google":
        return os.environ.get("GOOGLE_API_KEY") or os.environ.get("google_api_key")
    elif provider == "huggingface":
        return os.environ.get("HUGGINGFACEHUB_API_TOKEN") or os.environ.get("HF_TOKEN")
    elif provider == "openrouter":
        return os.environ.get("OPENROUTER_API_KEY")
    elif provider == "grok":
        return os.environ.get("XAI_API_KEY") or os.environ.get("GROK_API_KEY")
    elif provider == "groq":
        return os.environ.get("GROQ_API_KEY")
    return None

def closed_model_settings(provider: str = None):
    settings = {
        "temperature": 0.2,
        "max_tokens": 256,
        "max_retries": 3
    }
    
    if provider:
        api_key = get_api_key(provider)
        if api_key:
            if provider.lower() == "google":
                settings["api_key"] = api_key
            elif provider.lower() == "huggingface":
                settings["api_key"] = api_key
            else:
                settings["api_key"] = api_key
    return settings
