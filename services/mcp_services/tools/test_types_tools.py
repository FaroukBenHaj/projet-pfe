from typing import Any, Dict, Optional
from client.dojoClient import get_client 
from schemas.test_type import TestType, TestTypeUpdate
import json 


async def list_test_types(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    filters = {"limit": limit}
    if offset:
        filters["offset"] = offset
    client = get_client()
    result = await client.get_test_types(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def get_test_type(test_type_id: int) -> Dict[str, Any]:
    client = get_client()
    result = await client.get_test_type(test_type_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def create_test_type(test_type_data: TestType) -> Dict[str, Any]:
    client = get_client()
    result = await client.create_test_type(test_type_data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

async def run_test_type_pipeline(test_type_data: TestType) -> dict[str, Any]:
    client = get_client()
    summary ={}
    input_name = test_type_data.name.strip().title()    
    p_result = await client.get_test_types(filters={"name": input_name})
    if "error" in p_result:
        return {"status": "error", "step": "get_test_type", "error": p_result["error"]}

    if p_result.get("count", 0) > 0:
        test_type_id = p_result["results"][0]["id"]
        summary["test_type"] = {"action": "reused", "id": test_type_id , "name": input_name}
    else:
        created = await client.create_test_type(test_type_data)

        if "error" in created:
            return {"status": "error", "step": "create_test_type", "error": created["error"]}

        summary["test_type"] = {"action": "created", "id": created.get("id"), "name": input_name}

    return {"status": "success", "summary": summary}


def register_tools(mcp):
    mcp.tool(name="list_test_types", description="List all Test Types with optional filtering and pagination support")(list_test_types)
    mcp.tool(name="get_test_type", description="Get a specific Test Type by ID")(get_test_type)
    mcp.tool(name="create_test_type", description="Create a new Test Type")(create_test_type)
    mcp.tool(name="run_test_type_pipeline", description="Ensures a Test Type exists by name, creating it if necessary, and returns its details.")(run_test_type_pipeline)
