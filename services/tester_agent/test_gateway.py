from gateway.mcp_client import MCPClient
from gateway.tool_gateway import ToolGateway
from config import settings

mcp_client = MCPClient(settings.mcp_service_base_url)
gateway = ToolGateway(mcp_client)
print(f"DEBUG: MCP Service Base URL from settings: {settings.mcp_service_base_url}") # ADD THIS
print("Testing list product types...")
print(gateway.list_products())
