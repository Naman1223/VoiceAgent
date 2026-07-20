from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
import logging
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
import Settings
from pathlib import Path

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

MODEL_ROUTER = {
"openai":ChatOpenAI,
"anthropic":ChatAnthropic,
"google":ChatGoogleGenerativeAI,
"huggingface":ChatHuggingFace,
"openrouter":ChatOpenRouter,
"local":LlamaCpp
}

def Models_loader():
    try:
        logging.info("Loading models from Model_list.txt")
        with open(os.path.dirname(__file__)+"/Mod/Model_list.txt", 'r') as file:
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

    LLMClass = MODEL_ROUTER.get(provider.lower())

    if not LLMClass:
        logging.error(f"No LangChain handler found for provider: '{provider}'")
        raise ValueError(f"No LangChain handler found for provider: '{provider}'")
    
    if provider.lower() == "local":
        local_model_path = kwargs.pop("model_path", None) or os.environ.get("LOCAL_MODEL_PATH")
        if not local_model_path:
            local_model_path = input("Enter the full path to your local model: \n")
        return Settings.local_model_Settings(local_model_path, **kwargs)
    
    model_kwargs = Settings.closed_model_settings()
    model_kwargs.update(kwargs)

    if provider.lower() == "google":
        return LLMClass(model=actual_model, **model_kwargs)
    elif provider.lower() == "anthropic":
        return LLMClass(model_name=actual_model, **model_kwargs)
    else:
        return LLMClass(model=actual_model, **model_kwargs)
