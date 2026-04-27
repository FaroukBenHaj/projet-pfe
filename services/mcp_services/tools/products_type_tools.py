from typing import Any, Dict, Optional
from client.dojoClient import get_client 
from schemas.productType import ProductType, ProductTypeUpdate, ProductTypeResponse

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
    
async def get_product_type(product_type_id: int) -> Dict[str, Any]:
    """Get a specific product type by ID."""
    client = get_client()
    result = await client.get_product_type(product_type_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def update_product_type(product_type_id: int, data: ProductTypeUpdate) -> Dict[str, Any]:
    """Update an existing product type."""
    client = get_client()
    return await client.update_product_type(product_type_id, data)

async def delete_product_type(product_type_id: int) -> Dict[str, Any]:
    """Delete a product type by ID."""
    client = get_client()
    result = await client.delete_product_type(product_type_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


async def run_product_type_pipeline(product_type_name:str) -> dict[str, Any]:
    client = get_client()
    summary ={}
    pt_result = await  client.get_product_types({"name": product_type_name})
    if "error" in pt_result:
        return {"status": "error", "error": pt_result["error"], "details": pt_result.get("details", "")}
    if pt_result.get("count", 0) > 0:
        product_type_id = pt_result["results"][0]["id"]
        summary["product_type"] = {"action": "reused", "id": product_type_id}
    else:
        created = await client.create_product_type(ProductType(name=product_type_name))
        if "error" in created:
            return {"status": "error", "error": created["error"], "details": created.get("details", "")}
        product_type_id = created["id"]
        summary["product_type"] = {"action": "created", "id": product_type_id}
    return {"status": "success", "data": summary}
    
def register_tools(mcp):
    """Register product-related tools with the MCP server instance."""
    mcp.tool(name="list_product_types", description="List all product types ")(list_product_types)
    mcp.tool(name="run_product_type_pipeline", description="Ensures a Product Type exists by name, creating it if necessary, and returns its details.")(run_product_type_pipeline)
    mcp.tool(name="get_product_type", description="Retrieves the full details of a specific Product Type.")(get_product_type)
    mcp.tool(name="update_product_type", description="Updates specific fields of an existing Product Type.")(update_product_type)
    mcp.tool(name="delete_product_type", description="Deletes a specific Product Type.")(delete_product_type)