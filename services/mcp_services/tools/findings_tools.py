from typing import Any, Dict, Optional, List
from client.dojoClient  import get_client
from schemas.findings import Finding, FindingUpdate
import json
from fastapi import APIRouter

router = APIRouter()
# --- finding Tool Definitions ---
@router.get("/findings", summary="List findings with optional filtering and pagination support")
async def list_findings(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    filters = {"limit": limit}
    if offset:
        filters["offset"] = offset
    client = get_client()
    result = await client.get_findings(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

@router.get("/findings/{finding_id}", summary="Get a specific finding by ID")
async def get_finding(finding_id: int) -> Dict[str, Any]:
    client = get_client()
    result = await client.get_finding(finding_id)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}

@router.put("/findings/{finding_id}", summary="Update an existing finding")
async def update_finding(finding_id: int, data: FindingUpdate) -> Dict[str, Any]:
    client = get_client()
    result = await client.update_finding(finding_id, data)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}

@router.delete("/findings/{finding_id}", summary="Delete a finding")
async def delete_finding(finding_id: int) -> Dict[str, Any]:
    client = get_client()
    result = await client.delete_finding(finding_id)
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    return {"status": "success", "data": result}

@router.post("/findings/pipeline", summary="Runs the finding pipeline for a given test and finding data.")
async def run_finding_pipeline(test_id: int, finding_data: Finding) -> Dict[str, Any]:
    client = get_client()
    summary ={}
    eng_result = await client.get_finding_by_title_and_test(finding_data.title, test_id)
    if "error" in eng_result:
        return {"status": "error", "step": "get_finding", "error": eng_result["error"]}

    if eng_result.get("count", 0) > 0:
        finding_id = eng_result["results"][0]["id"]
        summary["finding"] = {"action": "reused", "id": finding_id , "name":finding_data.name}
    else:
        create_payload = json.loads(finding_data.json(exclude_none=True)) 
        create_payload["test"] = test_id
        create_result = await client.create_finding(create_payload)
        if "error" in create_result:
            return {"status": "error", "step": "create_finding", "error": create_result["error"]}
        finding_id = create_result.get("id")
        summary["finding"] = {"action": "created", "id": finding_id}
    return {"status": "success", "data": summary , "finding_id": finding_id}
    
# --- Registration Function ---

def register_tools(mcp):
    """Register finding-related tools with the MCP server instance."""
    mcp.tool(name="run_finding_pipeline", description="Runs the finding pipeline for a given test and finding data.")(run_finding_pipeline)
    mcp.tool(name="list_findings", description="List findings with optional filtering and pagination support")(list_findings)
    mcp.tool(name="get_finding", description="Get a specific finding by ID")(get_finding)
    mcp.tool(name="update_finding", description="Update an existing finding")(update_finding)
    mcp.tool(name="delete_finding", description="Delete an finding")(delete_finding)