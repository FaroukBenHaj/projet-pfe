import httpx
import os
from typing import Any, Dict, Optional 

class FindingsClient(BaseClient):
    # findings endpoints
    async def get_findings(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get findings with optional filters."""
        return await self._request("GET", "/api/v2/findings/", params=filters)
    
    async def search_findings(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for findings using a text query."""
        params = filters or {}
        params["search"] = query
        return await self._request("GET", "/api/v2/findings/", params=params)
    
    async def update_finding(self, finding_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a finding by ID."""
        return await self._request("PATCH", f"/api/v2/findings/{finding_id}/", json=data)
    
    async def add_note_to_finding(self, finding_id: int, note: str) -> Dict[str, Any]:
        """Add a note to a finding."""
        data = {"entry": note, "finding": finding_id}
        return await self._request("POST", "/api/v2/notes/", json=data)
    
    async def create_finding(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new finding."""
        return await self._request("POST", "/api/v2/findings/", json=data)
    