from typing import Any, Dict, List, Optional
from client.dojoClient  import get_client

# --- Finding Tool Definitions ---

async def get_findings(product_name: Optional[str] = None, status: Optional[str] = None,
                       severity: Optional[str] = None, limit: int = 20,
                       offset: int = 0) -> Dict[str, Any]:
    """Get findings with optional filters and pagination.

    Args:
        product_name: Optional product name filter
        status: Optional status filter
        severity: Optional severity filter
        limit: Maximum number of findings to return per page (default: 20)
        offset: Number of records to skip (default: 0)

    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {}
    if product_name:
        filters["product_name"] = product_name
    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
    if limit:
        filters["limit"] = limit
    if offset:
        filters["offset"] = offset

    client = get_client()
    result = await client.get_findings(filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


# --- Registration Function ---

def register_tools(mcp):
    """Register finding-related tools with the MCP server instance."""
    mcp.tool(name="get_findings", description="Get findings with filtering options and pagination support")(get_findings)
    mcp.tool(name="search_findings", description="Search for findings using a text query with pagination support")(search_findings)
    mcp.tool(name="update_finding_status", description="Update the status of a finding (Active, Verified, False Positive, Mitigated, Inactive)")(update_finding_status)
    mcp.tool(name="add_finding_note", description="Add a note to a finding")(add_finding_note)
    mcp.tool(name="create_finding", description="Create a new finding")(create_finding)


async def search_findings(query: str, product_name: Optional[str] = None,
                         status: Optional[str] = None, severity: Optional[str] = None,
                         limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Search for findings using a text query with pagination.

    Args:
        query: Text to search for in findings
        product_name: Optional product name filter
        status: Optional status filter
        severity: Optional severity filter
        limit: Maximum number of findings to return per page (default: 20)
        offset: Number of records to skip (default: 0)

    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {}
    if product_name:
        filters["product_name"] = product_name
    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
    if limit:
        filters["limit"] = limit
    if offset:
        filters["offset"] = offset

    client = get_client()
    result = await client.search_findings(query, filters)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


async def update_finding_status(finding_id: int, status: str) -> Dict[str, Any]:
    """Update the status of a finding.

    Args:
        finding_id: ID of the finding to update
        status: New status for the finding (Active, Verified, False Positive, Mitigated, Inactive)

    Returns:
        Dictionary with status and data/error
    """
    data = {"active": True}  # Default to active

    # Map common status values to API fields
    status_lower = status.lower()
    if status_lower == "false positive":
        data["false_p"] = True
    elif status_lower == "verified":
        data["verified"] = True
    elif status_lower == "mitigated":
        data["active"] = False
        data["mitigated"] = True # Assuming API uses 'mitigated' boolean field
    elif status_lower == "inactive":
        data["active"] = False
    elif status_lower != "active":
        # Check against API specific values if needed, or raise error for unsupported input
        return {"status": "error", "error": f"Unsupported status: {status}. Use Active, Verified, False Positive, Mitigated, or Inactive."}

    # Clear conflicting flags if setting a specific status
    if data.get("false_p"):
        data.pop("verified", None)
        data.pop("active", None)
        data.pop("mitigated", None)
    elif data.get("verified"):
         data.pop("false_p", None)
         # Verified implies active usually, but check API docs if explicit setting is needed
         data["active"] = True
         data.pop("mitigated", None)
    elif data.get("mitigated"):
         data.pop("false_p", None)
         data.pop("verified", None)
         data["active"] = False # Mitigated implies inactive
    elif not data.get("active", True): # Handling "Inactive" case
         data.pop("false_p", None)
         data.pop("verified", None)
         data.pop("mitigated", None)
         data["active"] = False
    else: # Handling "Active" case (default or explicit)
         data.pop("false_p", None)
         data.pop("verified", None)
         data.pop("mitigated", None)
         data["active"] = True

    client = get_client()
    result = await client.update_finding(finding_id, data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


async def add_finding_note(finding_id: int, note: str) -> Dict[str, Any]:
    """Add a note to a finding.

    Args:
        finding_id: ID of the finding to add a note to
        note: Text content of the note

    Returns:
        Dictionary with status and data/error
    """
    if not note.strip():
        return {"status": "error", "error": "Note content cannot be empty"}

    client = get_client()
    result = await client.add_note_to_finding(finding_id, note)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}


async def create_finding(title: str, test_id: int, severity: str, description: str,
                        cwe: Optional[int] = None, cvssv3: Optional[str] = None,
                        mitigation: Optional[str] = None, impact: Optional[str] = None,
                        steps_to_reproduce: Optional[str] = None) -> Dict[str, Any]:
    """Create a new finding.

    Args:
        title: Title of the finding
        test_id: ID of the test to associate the finding with
        severity: Severity level (Critical, High, Medium, Low, Info)
        description: Description of the finding
        cwe: Optional CWE identifier
        cvssv3: Optional CVSS v3 score string
        mitigation: Optional mitigation steps
        impact: Optional impact description
        steps_to_reproduce: Optional steps to reproduce

    Returns:
        Dictionary with status and data/error
    """
    # Validate severity (case-insensitive check, but send capitalized)
    valid_severities = ["critical", "high", "medium", "low", "info"]
    normalized_severity = severity.lower()
    if normalized_severity not in valid_severities:
        # Use title case for user-facing error message
        valid_display = [s.title() for s in valid_severities]
        return {"status": "error", "error": f"Invalid severity '{severity}'. Must be one of: {', '.join(valid_display)}"}

    # Use title case for API
    api_severity = severity.title()

    data = {
        "title": title,
        "test": test_id,
        "severity": api_severity,
        "description": description,
        # Set defaults expected by API if not provided explicitly by user?
        # e.g., "active": True, "verified": False? Check API docs.
        "active": True,
        "verified": False,
    }

    # Add optional fields if provided
    if cwe is not None:
        data["cwe"] = cwe
    if cvssv3:
        data["cvssv3"] = cvssv3 # Assuming API accepts the string directly
    if mitigation:
        data["mitigation"] = mitigation
    if impact:
        data["impact"] = impact
    if steps_to_reproduce:
        data["steps_to_reproduce"] = steps_to_reproduce

    client = get_client()
    result = await client.create_finding(data)

    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}

    return {"status": "success", "data": result}