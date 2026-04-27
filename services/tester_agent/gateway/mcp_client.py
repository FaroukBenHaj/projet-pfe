import requests
from typing import Any, Dict


class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def call_tool(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/tools/{tool_name}"

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            raise Exception(f"MCP error: {response.text}")

        return response.json()