from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
import time

embeddings = OllamaEmbeddings(model="nomic-embed-text")
memory_db = Chroma(
    collection_name="conversational_memory",
    embedding_function=embeddings,
    persist_directory="./chroma_memory"
)


def save_to_memory(user_text, ai_text):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    doc = Document(
        page_content=f"User said: {user_text}\nAI responded: {ai_text}",
        metadata={"timestamp": timestamp}
    )
    memory_db.add_documents([doc])


def get_relevant_memory(current_user_text):
    results = memory_db.similarity_search(current_user_text, k=3)
    memory_context = "\n".join([res.page_content for res in results])
    return memory_context
