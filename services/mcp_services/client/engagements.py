import httpx
import os
from typing import Any, Dict, Optional

class engagementsClient(BaseClient):
    # engagements endpoints
    async def get_engagements(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get engagements with optional filters."""
        return await self._request("GET", "/api/v2/engagements/", params=filters)
    
    async def get_engagement(self, engagement_id: int) -> Dict[str, Any]:
        """Get a specific engagement by ID."""
        return await self._request("GET", f"/api/v2/engagements/{engagement_id}/")
    
    async def create_engagement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new engagement."""
        return await self._request("POST", "/api/v2/engagements/", json=data)
    
    async def update_engagement(self, engagement_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing engagement."""
        return await self._request("PATCH", f"/api/v2/engagements/{engagement_id}/", json=data)