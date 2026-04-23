from typing import Any, Dict, Optional, List
from client.dojoClient  import get_client
from schemas.engagements import Engagement, EngagementUpdate
import json
# --- Engagement Tool Definitions ---

async def list_engagements(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    filters = {"limit": limit}
    if offset:
        filters["offset"] = offset
    client = get_client()
    result = await client.get_engagements(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def get_engagement(engagement_id: int) -> Dict[str, Any]:
    """Get a specific engagement by ID.

    Args:
        engagement_id: ID of the engagement to retrieve

    Returns:
        Dictionary with status and data/error
    """
    client = get_client()
    result = await client.get_engagement(engagement_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def update_engagement(engagement_id: int, data: EngagementUpdate) -> Dict[str, Any]:
    client = get_client()
    result = await client.update_engagement(product_id, data)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}

async def delete_engagement(engagement_id: int) -> Dict[str, Any]:
    client = get_client()
    result = await client.delete_engagement(engagement_id)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}

async def run_engagement_pipeline(product_id: int, engagement_data: Engagement) -> Dict[str, Any]:
    print(f"Type of engagement_data: {type(engagement_data)}") # Add this line
    client = get_client()
    summary ={}
    eng_result = await client.get_engagements({"product": product_id})
    if "error" in eng_result:
        return {"status": "error", "step": "get_engagement", "error": eng_result["error"]}

    if eng_result.get("count", 0) > 0:
        engagement_id = eng_result["results"][0]["id"]
        summary["engagement"] = {"action": "reused", "id": engagement_id , "name":engagement_data.name}
    else:
        create_payload = json.loads(engagement_data.json(exclude_none=True)) 
        create_payload["product"] = product_id
        create_result = await client.create_engagement(create_payload)
        if "error" in create_result:
            return {"status": "error", "step": "create_engagement", "error": create_result["error"]}
        engagement_id = create_result.get("id")
        summary["engagement"] = {"action": "created", "id": engagement_id}
    return {"status": "success", "data": summary , "engagement_id": engagement_id}
    
# --- Registration Function ---

def register_tools(mcp):
    """Register engagement-related tools with the MCP server instance."""
    mcp.tool(name="run_engagement_pipeline", description="Runs the engagement pipeline for a given product and engagement data.")(run_engagement_pipeline)
    mcp.tool(name="list_engagements", description="List engagements with optional filtering and pagination support")(list_engagements)
    mcp.tool(name="get_engagement", description="Get a specific engagement by ID")(get_engagement)
    mcp.tool(name="update_engagement", description="Update an existing engagement")(update_engagement)
    mcp.tool(name="delete_engagement", description="Delete an engagement")(delete_engagement)