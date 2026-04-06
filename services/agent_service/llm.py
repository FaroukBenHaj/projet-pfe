from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
from config import settings

load_dotenv()
def get_llm():
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )