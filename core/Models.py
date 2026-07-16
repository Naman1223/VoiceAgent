from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_ROUTER = {
"openai":ChatOpenAI,
"anthropic":ChatAnthropic,
"google":ChatGoogleGenerativeAI,
"huggingface":ChatHuggingFace,
"openrouter":ChatOpenRouter
}

def Models_loader(Model_name):
    try:
        with open(f'core/Models/Model_list.txt', 'r') as file:
            model_id = [models.strip() for models in file.read().split("\n")]
            for names in model_id:
                if names == Model_name:
                    return MODEL_ROUTER[names]
            return "No Model Found"
    except FileNotFoundError:
        print(f"Error: Model list file not found.")
        return "No Model Found"

    
    