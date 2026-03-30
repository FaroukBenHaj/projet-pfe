import httpx
import os 
from dotenv import load_dotenv

load_dotenv()

DEFECTDOJO_API_URL = os.getenv("DEFECTDOJO_API_URL","http://localhost:8080")
DEFECTDOJO_API_KEY = os.getenv("DEFECTDOJO_API_KEY")

headers = {
    "Authorization": f"Token {DEFECTDOJO_API_KEY}",
    "Content-Type": "application/json"
}

async def create_product_type(name: str, description: str = "",
    critical_product: bool = False,
    key_product: bool = False):
    data ={
        "name": name,
        "description": description,
        "critical_product": critical_product,
        "key_product": key_product
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DEFECTDOJO_API_URL}/api/v2/product_types/",
            headers=headers,
            json=data
        )
        return response.json()
       
async def get_product_type_list():
     async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DEFECTDOJO_API_URL}/api/v2/product_types/",
            headers=headers,
        )
        return response.json()
       

async def get_product_type(id: int):
     async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DEFECTDOJO_API_URL}/api/v2/product_types/{id}/",
            headers=headers,
        )
        return response.json()

async def delete_product_type(id: int):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{DEFECTDOJO_API_URL}/api/v2/product_types/{id}/",
                headers=headers,
            )
            return response.json()

async def update_product_type(id, data):
    url = f"{DEFECTDOJO_API_URL}/api/v2/product_types/{id}/"

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            url,
            headers=headers,
            json=data
        )
        return response.json()


async def full_update_product_type(id, data):
    url = f"{DEFECTDOJO_API_URL}/api/v2/product_types/{id}/"

    async with httpx.AsyncClient() as client:
        response = await client.put(
            url,
            headers=headers,
            json=data
        )
        return response.json()
