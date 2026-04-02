import httpx
import os
from typing import Any, Dict, Optional

class ProductTypeClient(BaseClient):
    #product type endpoints
    async def get_product_types(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get all product types."""
        return await self._request("GET", "/api/v2/product_types/", params=filters)

    async def create_product_type(self , name: str, description: Optional[str] = None, critical_product: Optional[bool] = False, key_product: Optional[bool] = False) -> Dict[str, Any]:
        """Create a new product type """
        data = {
            "name": name,
            "description": description,
            "critical_product": critical_product,
            "key_product": key_product
        }
        return await self._request("POST", "/api/v2/product_types/", json=data)
    
    async def get_product_type(self, product_type_id: int) -> Dict[str, Any]:
        """Get a specific product type by ID."""
        return await self._request("GET", f"/api/v2/product_types/{product_type_id}/")
    
    async def update_product_type(self, product_type_id: int, name: Optional[str] = None, description: Optional[str] = None, critical_product: Optional[bool] = None, key_product: Optional[bool] = None) -> Dict[str, Any]:
        """Update an existing product type."""
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if critical_product is not None:
            data["critical_product"] = critical_product
        if key_product is not None:
            data["key_product"] = key_product
        
        return await self._request("PATCH", f"/api/v2/product_types/{product_type_id}/", json=data)

    async def delete_product_type(self, product_type_id: int) -> Dict[str, Any]:
        """Delete a product type by ID."""
        return await self._request("DELETE", f"/api/v2/product_types/{product_type_id}/")
