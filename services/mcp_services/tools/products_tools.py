from typing import Any, Dict, Optional
from client.dojoClient import get_client 
from schemas.product import Product, ProductUpdate
# --- Product Tool Definitions ---

async def list_products(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
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
    if offset:
        filters["offset"] = offset
    client = get_client()
    result = await client.get_products(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def create_product(data: Product) -> Dict[str, Any]:
    """Create a new product."""
    client = get_client()
    result = await client.create_product(data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}

async def get_product(product_id: int) -> Dict[str, Any]:
    """Get a specific product by ID."""
    client = get_client()
    result = await client.get_product(product_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def update_product(product_id: int, data: ProductUpdate) -> Dict[str, Any]:
    """Update an existing product."""
    client = get_client()
    return await client.update_product(product_id, data)

async def delete_product(product_id: int) -> Dict[str, Any]:
    """Delete a product by ID."""
    client = get_client()
    result = await client.delete_product(product_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


async def run_product_pipeline(product_type_id: int, product_data: Product) -> dict[str, Any]:
    client = get_client()
    summary ={}
    p_result = await client.get_product_by_name_and_type(product_data.name, product_type_id)
    if "error" in p_result:
        return {"status": "error", "step": "get_product", "error": p_result["error"]}

    if p_result.get("count", 0) > 0:
        product_id = p_result["results"][0]["id"]
        summary["product"] = {"action": "reused", "id": product_id , "name": product_data.name}
    else:
        create_payload = product_data.model_dump(exclude_none=True)
        create_payload["prod_type"] = product_type_id
        created = await client.create_product(product_data)
       
        if "error" in created:
            return {"status": "error", "step": "create_product", "error": created["error"]}
        product_id = created["id"]
        summary["product"] = {"action": "created", "id": product_id}
    return {"status": "success", "data": summary , "product_id": product_id}

# --- Registration Function ---

def register_tools(mcp):
    """Register product-related tools with the MCP server instance."""
    mcp.tool(name="list_products", description="List all products with optional filtering and pagination support")(list_products)
    mcp.tool(name="run_product_pipeline", description="Ensures a Product exists by name, creating it if necessary, and returns its details.")(run_product_pipeline)
    mcp.tool(name="get_product", description="Get a specific product by ID")(get_product)
    mcp.tool(name="update_product", description="Update an existing product")(update_product)
    mcp.tool(name="delete_product", description="Delete a product by ID")(delete_product)