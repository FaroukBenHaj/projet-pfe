import httpx
import os 
from dotenv import load_dotenv

load_dotenv()
DEFECTDOJO_API_URL = os.getenv("DEFECTDOJO_API_URL")
DEFECTDOJO_API_KEY = os.getenv("DEFECTDOJO_API_KEY")
BASE_URL = os.getenv("BASE_URL")

_client = httpx.AsyncClient(
    base_url=DEFECTDOJO_API_URL+BASE_URL,
    headers={
        "Authorization": f"Token {DEFECTDOJO_API_KEY}",
        "Content-Type": "application/json"
    }
)
async def request(method: str, path: str, **kwargs) -> dict:
    response = await _client.request(method, path, **kwargs)
    response.raise_for_status()
    return response.json() if response.content else {}


