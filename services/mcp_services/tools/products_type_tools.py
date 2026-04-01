from typing import Any, Dict, Optional
from client.dojoClient import get_client 

# --- Product type Tool Definitions ---
async def list_product_types(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """List all product types with pagination.

    Args:
        limit: Maximum number of product types to return per page (default: 50)
        offset: Number of records to skip (default: 0)

    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {"limit": limit}
    if offset:
        filters["offset"] = offset
    
    client = get_client()
    result = await client.get_product_types(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

    # --- Registration Function ---

def register_tools(mcp):
    """Register product-related tools with the MCP server instance."""
    mcp.tool(name="list_product_types", description="List all product types with pagination support")(list_product_types)