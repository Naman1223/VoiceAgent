import os
from llama_cpp import Llama

def local_model_Settings(model_path: str, **kwargs):
    settings = {
        "model_path": model_path,
        "n_ctx": 4096,
        "n_batch": 512,
        "n_gpu_layers": -1,
        "verbose": False,
        "temperature": 0.3,
        "repeat_penalty": 1.1,
    }
    # Separate Llama instantiation parameters from generation parameters if needed,
    # but Llama constructor takes model_path, n_ctx, n_batch, n_gpu_layers, verbose, etc.
    # We will pass relevant kwargs to Llama and return it.
    settings.update(kwargs)
    
    # max_tokens and streaming are typically generation params, we can store them separately or ignore here.
    if "max_tokens" in settings:
        del settings["max_tokens"]
    if "streaming" in settings:
        del settings["streaming"]
    if "temperature" in settings:
        del settings["temperature"]
    if "repeat_penalty" in settings:
        del settings["repeat_penalty"]

    llm = Llama(**settings)
    return llm

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
