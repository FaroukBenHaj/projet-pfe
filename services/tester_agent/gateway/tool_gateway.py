from typing import Dict, Any
from .mcp_client import MCPClient


class ToolGateway:
    def __init__(self, client: MCPClient):
        self.client = client

    # ---- FINDINGS ----
    def create_finding(self, data: Dict[str, Any]):
        """Create a new finding in defectdojo"""
        return self.client.call_tool("create_finding", data)

    # ---- ENGAGEMENTS ----
    def create_engagement(self, data: Dict[str, Any]):
        """Create a new engagement in defectdojo"""
        return self.client.call_tool("create_engagement", data)

    # ---- PRODUCTS ----
    def create_product(self, data: Dict[str, Any]):
        """Create a new product in defectdojo"""
        return self.client.call_tool("create_product", data)

    def list_products(self , limit: int=50 , offset: int=0):
        """List products currently configured in DefectDojo with optional pagination."""
        params = {"limit": limit, "offset": offset}
        return self.client.call_tool("products",params, method="GET")
    