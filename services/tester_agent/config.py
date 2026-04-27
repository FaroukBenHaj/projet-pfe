# agent/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()
class Settings(BaseSettings):
    # DefectDojo
    defectdojo_url : str = os.getenv("DEFECTDOJO_API_URL")
    defectdojo_api_key : str = os.getenv("DEFECTDOJO_API_KEY")

    # Ollama / LangChain
    ollama_model : str = os.getenv("OLLAMA_MODEL")
    ollama_base_url  : str = os.getenv("OLLAMA_BASE_URL")

    # Agent behavior
    agent_max_iterations: int = 10


settings = Settings()