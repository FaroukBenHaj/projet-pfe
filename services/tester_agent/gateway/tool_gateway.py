from typing import Dict, Any
from .mcp_client import MCPClient


class ToolGateway:
    def __init__(self, client: MCPClient):
        self.client = client

    # ---- FINDINGS ----
    def create_finding(self, data: Dict[str, Any]):
        return self.client.call_tool("create_finding", data)

    # ---- ENGAGEMENTS ----
    def create_engagement(self, data: Dict[str, Any]):
        return self.client.call_tool("create_engagement", data)

    # ---- PRODUCTS ----
    def create_product(self, data: Dict[str, Any]):
        return self.client.call_tool("create_product", data)

    def list_products(self):
        return self.client.call_tool("list_products", {})