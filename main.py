from dotenv import load_dotenv
from core.Models import get_chat_model

# Load environment variables (like GOOGLE_API_KEY) from .env
load_dotenv() 

try:
    model = get_chat_model("groq/llama-3.1-8b-instant")
    response = model.invoke("Hello, Llama! Do you have tool calling capablities?")
    print(response)
except Exception as e:
    print(f"Failed to run: {e}")
