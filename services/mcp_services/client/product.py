import httpx
import os
from typing import Any, Dict, Optional
class ProductClient(BaseClient):
    #products endpoints
    async def get_products(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get products with optional filters."""
        return await self._request("GET", "/api/v2/products/", params=filters)
