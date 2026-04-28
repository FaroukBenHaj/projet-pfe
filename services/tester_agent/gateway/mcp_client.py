import requests
from typing import Any, Dict


class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def call_tool(self, tool_name: str, payload: Dict[str, Any], method: str = "POST") -> Dict[str, Any]:
        url = f"{self.base_url}/{tool_name}" # tool_name here should be the API path segment, e.g., "products"

        if method.upper() == "GET":
            response = requests.get(url, params=payload) # Use params for GET requests
        elif method.upper() == "POST":
            response = requests.post(url, json=payload)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.status_code != 200:
            raise Exception(f"MCP error (status {response.status_code}): {response.text}")

        return response.json()

    # Add a specific method for GET requests, or use call_tool with method='GET'
    def get(self, path: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        url = f"{self.base_url}/{path}"
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"MCP error (status {response.status_code}): {response.text}")
        return response.json()