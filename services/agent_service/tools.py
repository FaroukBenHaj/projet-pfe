# agent/tools.py
import httpx
from langchain.tools import tool
from config import settings
from typing import Optional


class DefectDojoClient:
    def __init__(self):
        self.base_url = settings.defectdojo_url.rstrip("/")
        self.headers = {
            "Authorization": f"Token {settings.defectdojo_api_key}",
            "Content-Type": "application/json",
        }

    def get_product_types(self, params: dict) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/product_types/",
                headers=self.headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def get_product_type(self, product_type_id: int) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/api/v2/product_types/{product_type_id}/",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def create_product_type(self, **data) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/v2/product_types/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def update_product_type(self, product_type_id: int, **data) -> dict:
        try:
            response = httpx.patch(
                f"{self.base_url}/api/v2/product_types/{product_type_id}/",
                headers=self.headers,
                json=data,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    def delete_product_type(self, product_type_id: int) -> dict:
        try:
            response = httpx.delete(
                f"{self.base_url}/api/v2/product_types/{product_type_id}/",
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return {"deleted": True, "id": product_type_id}
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}


def get_client() -> DefectDojoClient:
    return DefectDojoClient()


# ✅ All tools are now sync (no async def)
@tool
def list_product_types(limit: int = 50, offset: int = 0) -> dict:
    """List all product types with pagination."""
    filters = {"limit": limit}
    if offset:
        filters["offset"] = offset
    client = get_client()
    result = client.get_product_types(filters)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def create_product_type(
    name: str,
    description: Optional[str] = None,
    critical_product: Optional[bool] = False,
    key_product: Optional[bool] = False,
) -> dict:
    """Create a new product type."""
    client = get_client()
    data = {
        "name": name,
        "description": description,
        "critical_product": critical_product,
        "key_product": key_product,
    }
    result = client.create_product_type(**data)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def get_product_type(product_type_id: int) -> dict:
    """Get a specific product type by ID."""
    client = get_client()
    result = client.get_product_type(product_type_id)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def update_product_type(
    product_type_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    critical_product: Optional[bool] = None,
    key_product: Optional[bool] = None,
) -> dict:
    """Update an existing product type."""
    client = get_client()
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if critical_product is not None:
        data["critical_product"] = critical_product
    if key_product is not None:
        data["key_product"] = key_product
    result = client.update_product_type(product_type_id, **data)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


@tool
def delete_product_type(product_type_id: int) -> dict:
    """Delete a product type by ID."""
    client = get_client()
    result = client.delete_product_type(product_type_id)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


# ✅ list_product_types is now included
tools = [list_product_types, create_product_type, get_product_type, update_product_type, delete_product_type]