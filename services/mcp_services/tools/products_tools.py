from typing import Any, Dict, Optional
from client.dojoClient import get_client 

# --- Product Tool Definitions ---

async def list_products(name: Optional[str] = None, prod_type: Optional[int] = None,
                       limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """List all products with optional filtering and pagination.

    Args:
        name: Optional name filter (partial match)
        prod_type: Optional product type ID filter
        limit: Maximum number of products to return per page (default: 50)
        offset: Number of records to skip (default: 0)

    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {"limit": limit}
    # Use __icontains for case-insensitive partial match if API supports it
    if name:
        filters["name"] = name # Or name__icontains if supported
    if prod_type:
        filters["prod_type"] = prod_type
    if offset:
        filters["offset"] = offset

    client = get_client()
    result = await client.get_products(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


# --- Registration Function ---

def register_tools(mcp):
    """Register product-related tools with the MCP server instance."""
    mcp.tool(name="list_products", description="List all products with optional filtering and pagination support")(list_products)