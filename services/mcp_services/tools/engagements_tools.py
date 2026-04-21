from typing import Any, Dict, Optional, List
from client.dojoClient  import get_client

# --- Engagement Tool Definitions ---

async def list_engagements(product_id: Optional[int] = None,
                          status: Optional[str] = None,
                          name: Optional[str] = None,
                          limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """List engagements with optional filtering and pagination.

    Args:
        product_id: Optional product ID filter
        status: Optional status filter (e.g., 'Not Started', 'In Progress', 'Completed')
        name: Optional name filter (partial match)
        limit: Maximum number of engagements to return per page (default: 20)
        offset: Number of records to skip (default: 0)

    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {"limit": limit}
    if product_id:
        filters["product"] = product_id
    if status:
         # Validate against known API statuses if necessary
        valid_statuses = ["Not Started", "Blocked", "Cancelled", "Completed", "In Progress", "On Hold", "Waiting for Resource"]
        if status not in valid_statuses:
             return {"status": "error", "error": f"Invalid status filter '{status}'. Must be one of: {', '.join(valid_statuses)}"}
        filters["status"] = status
    if name:
        filters["name"] = name # Or name__icontains if supported
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


async def create_engagement(product_id: int, name: str, target_start: str, target_end: str, status: str, lead_id: int = None, description: str = None, version: str = None, build_id: str = None, commit_hash: str = None, branch_tag: str = None, engagement_type: str = None, deduplication_on_engagement: bool = None, tags: list = None):
    """
    Creates a new engagement in DefectDojo.

    Args:
        product_id: ID of the product.
        name: Name of the engagement.
        target_start: Start date (YYYY-MM-DD).
        target_end: End date (YYYY-MM-DD).
        status: Engagement status ('Not Started', 'Blocked', 'Cancelled', 'Completed', 'In Progress', 'On Hold', 'Waiting for Resource').
        lead_id: Optional ID of the engagement lead (user ID).
        description: Optional engagement description.
        version: Optional product version tested.
        build_id: Optional build ID.
        commit_hash: Optional commit hash.
        branch_tag: Optional branch or tag.
        engagement_type: Optional engagement type ('Interactive' or 'CI/CD').
        deduplication_on_engagement: Optional flag to enable deduplication within this engagement.
        tags: Optional list of tags.

    Returns:
        JSON response from the API.
    """
    # endpoint = "/api/v2/engagements/" # Endpoint handled by client method
    valid_statuses = ["Not Started", "Blocked", "Cancelled", "Completed", "In Progress", "On Hold", "Waiting for Resource"]
    if status not in valid_statuses:
        # Use raise ValueError for internal validation errors
        raise ValueError(f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}")

    # Validate engagement_type if provided
    if engagement_type and engagement_type not in ["Interactive", "CI/CD"]:
         raise ValueError(f"Invalid engagement_type '{engagement_type}'. Must be 'Interactive' or 'CI/CD'.")

    data = {
        "product": product_id,
        "name": name,
        "target_start": target_start,
        "target_end": target_end,
        "status": status, # Use API expected casing directly
    }
    # Add optional fields cleanly
    if lead_id is not None: data["lead"] = lead_id
    if description is not None: data["description"] = description
    if version is not None: data["version"] = version
    if build_id is not None: data["build_id"] = build_id
    if commit_hash is not None: data["commit_hash"] = commit_hash
    if branch_tag is not None: data["branch_tag"] = branch_tag
    if engagement_type is not None: data["engagement_type"] = engagement_type
    if deduplication_on_engagement is not None: data["deduplication_on_engagement"] = deduplication_on_engagement
    if tags is not None: data["tags"] = tags # Assumes API accepts list directly

    client = get_client()
    result = await client.create_engagement(data)

    # Return structured response
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


async def update_engagement(engagement_id: int, name: Optional[str] = None,
                           target_start: Optional[str] = None, # Renamed from start_date
                           target_end: Optional[str] = None,   # Renamed from end_date
                           status: Optional[str] = None,
                           description: Optional[str] = None,
                           # Add other updatable fields from API schema if needed
                           lead_id: Optional[int] = None,
                           version: Optional[str] = None,
                           build_id: Optional[str] = None,
                           commit_hash: Optional[str] = None,
                           branch_tag: Optional[str] = None,
                           engagement_type: Optional[str] = None,
                           deduplication_on_engagement: Optional[bool] = None,
                           tags: Optional[list] = None
                           ) -> Dict[str, Any]:
    """Update an existing engagement. Only provided fields are updated.

    Args:
        engagement_id: ID of the engagement to update.
        name: Optional new name.
        target_start: Optional new start date (YYYY-MM-DD).
        target_end: Optional new end date (YYYY-MM-DD).
        status: Optional new status ('Not Started', 'Blocked', 'Cancelled', 'Completed', 'In Progress', 'On Hold', 'Waiting for Resource').
        description: Optional new description.
        lead_id: Optional new lead ID.
        version: Optional new version.
        build_id: Optional new build ID.
        commit_hash: Optional new commit hash.
        branch_tag: Optional new branch/tag.
        engagement_type: Optional new engagement type ('Interactive', 'CI/CD').
        deduplication_on_engagement: Optional new deduplication setting.
        tags: Optional new list of tags (will replace existing tags).

    Returns:
        Dictionary with status and data/error.
    """
    # Validate status if provided
    if status:
        valid_statuses = ["Not Started", "Blocked", "Cancelled", "Completed", "In Progress", "On Hold", "Waiting for Resource"]
        if status not in valid_statuses:
             return {"status": "error", "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"}

    # Validate engagement_type if provided
    if engagement_type and engagement_type not in ["Interactive", "CI/CD"]:
         return {"status": "error", "error": f"Invalid engagement_type '{engagement_type}'. Must be 'Interactive' or 'CI/CD'."}

    # Prepare data payload with only provided fields
    data = {}
    if name is not None: data["name"] = name
    if target_start is not None: data["target_start"] = target_start
    if target_end is not None: data["target_end"] = target_end
    if status is not None: data["status"] = status # Send as is after validation
    if description is not None: data["description"] = description
    if lead_id is not None: data["lead"] = lead_id
    if version is not None: data["version"] = version
    if build_id is not None: data["build_id"] = build_id
    if commit_hash is not None: data["commit_hash"] = commit_hash
    if branch_tag is not None: data["branch_tag"] = branch_tag
    if engagement_type is not None: data["engagement_type"] = engagement_type
    if deduplication_on_engagement is not None: data["deduplication_on_engagement"] = deduplication_on_engagement
    if tags is not None: data["tags"] = tags # PATCH usually replaces arrays

    # If no fields were provided, return an error
    if not data:
        return {"status": "error", "error": "At least one field must be provided for update"}

    client = get_client()
    result = await client.update_engagement(engagement_id, data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


async def close_engagement(engagement_id: int) -> Dict[str, Any]:
    """Close an engagement by setting its status to completed.

    Args:
        engagement_id: ID of the engagement to close

    Returns:
        Dictionary with status and data/error
    """
    # Use the specific status string from the API schema
    data = {
        "status": "Completed"
    }

    client = get_client()
    # Use the update_engagement client method
    result = await client.update_engagement(engagement_id, data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    # Check if the update was successful (API might return updated object or just status)
    # Assuming success if no error is present
    return {"status": "success", "data": result}


# --- Registration Function ---

def register_tools(mcp):
    """Register engagement-related tools with the MCP server instance."""
    mcp.tool(name="list_engagements", description="List engagements with optional filtering and pagination support")(list_engagements)
    mcp.tool(name="get_engagement", description="Get a specific engagement by ID")(get_engagement)
    mcp.tool(name="create_engagement", description="Create a new engagement")(create_engagement)
    mcp.tool(name="update_engagement", description="Update an existing engagement")(update_engagement)
    mcp.tool(name="close_engagement", description="Close an engagement")(close_engagement)