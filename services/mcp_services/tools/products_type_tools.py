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

async def create_product_type(name: str, description: Optional[str] = None, critical_product: Optional[bool] = False, key_product: Optional[bool] = False) -> Dict[str, Any]:
    """Create a new product type."""
    client = get_client()
    data = {
        "name": name,
        "description": description,
        "critical_product": critical_product,
        "key_product": key_product
    }
    result = await client.create_product_type(**data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}
    
async def get_product_type(product_type_id: int) -> Dict[str, Any]:
    """Get a specific product type by ID."""
    client = get_client()
    result = await client.get_product_type(product_type_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def update_product_type(product_type_id: int, name: Optional[str] = None, description: Optional[str] = None, critical_product: Optional[bool] = None, key_product: Optional[bool] = None) -> Dict[str, Any]:
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
    
    result = await client.update_product_type(product_type_id, **data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def delete_product_type(product_type_id: int) -> Dict[str, Any]:
    """Delete a product type by ID."""
    client = get_client()
    result = await client.delete_product_type(product_type_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


def register_tools(mcp):
    """Register product-related tools with the MCP server instance."""
    mcp.tool(name="list_product_types", description="List all product types with pagination support")(list_product_types)
    mcp.tool(name="create_product_type", description="Create a new product type")(create_product_type)
    mcp.tool(name="get_product_type", description="Get a specific product type by ID")(get_product_type)
    mcp.tool(name="update_product_type", description="Update an existing product type")(update_product_type)
    mcp.tool(name="delete_product_type", description="Delete a product type by ID")(delete_product_type)