from langchain_community.llms import LlamaCpp

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
    settings.update(kwargs)
    
    LLM = LlamaCpp(**settings)
    return LLM

def closed_model_settings():
    settings =  {
        "temperature": 0.2,
        "max_tokens": 256,
        "max_retries": 3
    }
    return settings

