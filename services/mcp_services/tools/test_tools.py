from typing import Any, Dict, Optional
from client.dojoClient import get_client 
from schemas.test import Test, TestUpdate
import json 
# --- Test Tool Definitions ---

async def list_tests(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    filters = {"limit": limit}
    # Use __icontains for case-insensitive partial match if API supports it
    if offset:
        filters["offset"] = offset
    client = get_client()
    result = await client.get_tests(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def get_test(test_id: int) -> Dict[str, Any]:
    """Get a specific Test by ID."""
    client = get_client()
    result = await client.get_test(test_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def update_test(test_id: int, data: TestUpdate) -> Dict[str, Any]:
    """Update an existing Test."""
    client = get_client()
    return await client.update_test(test_id, data)

async def delete_test(test_id: int) -> Dict[str, Any]:
    """Delete a Test by ID."""
    client = get_client()
    result = await client.delete_test(test_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}


async def run_test_pipeline(engagement_id: int, test_data: Test) -> dict[str, Any]:
    client = get_client()
    summary ={}
    p_result = await client.get_test_by_title_and_engagement(test_data.title, engagement_id)
    if "error" in p_result:
        return {"status": "error", "step": "get_test", "error": p_result["error"]}

    if p_result.get("count", 0) > 0:
        test_id = p_result["results"][0]["id"]
        summary["test"] = {"action": "reused", "id": test_id , "title": test_data.title}
    else:
        create_payload = json.loads(test_data.json(exclude_none=True))
        create_payload["engagement"] = engagement_id
        created = await client.create_test(create_payload)

        if "error" in created:
            return {"status": "error", "step": "create_test", "error": created["error"]}
        test_id = created["id"]
        summary["test"] = {"action": "created", "id": test_id}
    return {"status": "success", "data": summary , "Test_id": test_id}


def register_tools(mcp):
    """Register Test-related tools with the MCP server instance."""
    mcp.tool(name="list_tests", description="List all Tests with optional filtering and pagination support")(list_tests)
    mcp.tool(name="run_test_pipeline", description="Ensures a Test exists by title, creating it if necessary, and returns its details.")(run_test_pipeline)
    mcp.tool(name="get_test", description="Get a specific Test by ID")(get_test)
    mcp.tool(name="update_test", description="Update an existing Test")(update_test)
    mcp.tool(name="delete_test", description="Delete a Test by ID")(delete_test)