import httpx
import os
from typing import Any, Dict, Optional
from schemas.productType import ProductType , ProductTypeUpdate
from schemas.product import Product , ProductUpdate
from schemas.engagements import Engagement, EngagementUpdate
from schemas.test import Test, TestUpdate
from schemas.test_type import TestType, TestTypeUpdate
class DefectDojoClient:
    """Client for interacting with the DefectDojo API."""
    def __init__(self, base_url: str, api_token: str):
        """Initialize the DefectDojo API client.
        
        Args:
            base_url: Base URL for the DefectDojo API
            api_token: API token for authentication
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }
        # Consider adding timeout configuration
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0) 

    ## requests 
    async def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Helper method to make API requests."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.request(method, url, params=params, json=json)
            response.raise_for_status()
            # Handle cases where response might be empty (e.g., 204 No Content)
            if response.status_code == 204:
                return {} 
            return response.json()
        except httpx.HTTPStatusError as e:
            # Log or handle specific status codes if needed
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except httpx.RequestError as e:
            # Handle network errors, timeouts, etc.
            return {"error": f"Request error: {str(e)}"}
        except Exception as e:
            # Catch unexpected errors
            return {"error": f"An unexpected error occurred: {str(e)}"}

#product type endpoints
    async def get_product_types(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get all product types."""
        return await self._request("GET", "/api/v2/product_types/", params=filters)
    
    async def get_product_type(self, product_type_id: int) -> Dict[str, Any]:
        """Get a specific product type by ID."""
        return await self._request("GET", f"/api/v2/product_types/{product_type_id}/")
    
    async def create_product_type(self , data: ProductType) -> Dict[str, Any]:
        """Create a new product type """
        return await self._request("POST", "/api/v2/product_types/", json=data.model_dump())
    
    async def update_product_type(self, product_type_id: int , data: ProductTypeUpdate ) -> Dict[str, Any]:
        """Update an existing product type."""        
        return await self._request("PATCH", f"/api/v2/product_types/{product_type_id}/", json=data.model_dump(exclude_none=True))

    async def delete_product_type(self, product_type_id: int) -> Dict[str, Any]:
        """Delete a product type by ID."""
        return await self._request("DELETE", f"/api/v2/product_types/{product_type_id}/")

#products endpoints
    async def get_products(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get products with optional filters."""
        return await self._request("GET", "/api/v2/products/", params=filters)

    async def get_product(self, product_id: int) -> Dict[str, Any]:
        """Get a specific product by ID."""
        return await self._request("GET", f"/api/v2/products/{product_id}/")
    
    async def create_product(self, data: Product) -> Dict[str, Any]:
        """Create a new product."""
        return await self._request("POST", "/api/v2/products/", json=data.model_dump())

    async def update_product(self, product_id: int, data: ProductUpdate) -> Dict[str, Any]:
        """Update an existing product."""
        return await self._request("PATCH", f"/api/v2/products/{product_id}/", json=data.model_dump(exclude_none=True))

    async def delete_product(self, product_id: int) -> Dict[str, Any]:
        """Delete a product by ID."""
        return await self._request("DELETE", f"/api/v2/products/{product_id}/")
    
    async def get_product_by_name_and_type(self, name: str, product_type_id: int) -> Dict[str, Any]:
     filters = {"name": name, "prod_type": product_type_id}
     return await self.get_products(filters=filters)

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
     
# engagements endpoints
    async def get_engagements(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get engagements with optional filters."""
        return await self._request("GET", "/api/v2/engagements/", params=filters)
    
    async def get_engagement(self, engagement_id: int) -> Dict[str, Any]:
        """Get a specific engagement by ID."""
        return await self._request("GET", f"/api/v2/engagements/{engagement_id}/")
    
    async def create_engagement(self, data: Engagement) -> Dict[str, Any]:
        """Create a new engagement."""
        return await self._request("POST", "/api/v2/engagements/", json=data)
    
    async def update_engagement(self, engagement_id: int, data: EngagementUpdate) -> Dict[str, Any]:
        """Update an existing engagement."""
        return await self._request("PATCH", f"/api/v2/engagements/{engagement_id}/", json=data.model_dump(exclude_none=True))

    async def delete_engagement(self, engagement_id: int) -> Dict[str, Any]:
        """Delete an engagement by ID."""
        return await self._request("DELETE", f"/api/v2/engagements/{engagement_id}/")

    async def get_engagement_by_name_and_product(self, name: str, product_id: int) -> Dict[str, Any]:
        filters = {"name": name, "product": product_id}
        return await self.get_engagements(filters=filters)

   
# test endpoints
    async def get_tests(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get tests with optional filters."""
        return await self._request("GET", "/api/v2/tests/", params=filters)
    
    async def get_test(self, test_id: int) -> Dict[str, Any]:
        """Get a specific test by ID."""
        return await self._request("GET", f"/api/v2/tests/{test_id}/")
    
    async def create_test(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new test."""
        return await self._request("POST", "/api/v2/tests/", json=data)

    async def update_test(self, test_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing test."""
        return await self._request("PATCH", f"/api/v2/tests/{test_id}/", json=data.model_dump(exclude_none=True))

    async def delete_test(self, test_id: int) -> Dict[str, Any]:
        """Delete a test by ID."""
        return await self._request("DELETE", f"/api/v2/tests/{test_id}/")

    async def get_test_by_title_and_engagement(self, title: str, engagement_id: int) -> Dict[str, Any]:
        filters = {"title": title, "engagement": engagement_id}
        return await self.get_tests(filters=filters)

#Test Type endpoints
    async def get_test_types(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("GET", "/api/v2/test_types/", params=filters)
    
    async def get_test_type(self, test_type_id: int) -> Dict[str, Any]:
        return await self._request("GET", f"/api/v2/test_types/{test_type_id}/")
    
    async def create_test_type(self, data: TestType) -> Dict[str, Any]:
        return await self._request("POST", "/api/v2/test_types/", json=data.model_dump())

    async def update_test_type(self, test_type_id: int, data: TestTypeUpdate) -> Dict[str, Any]:
        return await self._request("PATCH", f"/api/v2/test_types/{test_type_id}/", json=data.model_dump(exclude_none=True))
# --- Client Factory ---

def get_client(validate_token=True, base_url=None, token=None) -> DefectDojoClient:
    """Get a configured DefectDojo client.
    
    Args:
        validate_token: Whether to validate that the token is set (default: True)
        base_url: Optional base URL override for testing
        token: Optional token override for testing
        
    Returns:
        A configured DefectDojoClient instance
        
    Raises:
        ValueError: If DEFECTDOJO_API_TOKEN environment variable is not set and validate_token is True
    """
    # Use provided values or get from environment variables.
    # Ensure DEFECTDOJO_API_BASE and DEFECTDOJO_API_TOKEN are set in your environment.
    actual_token = token if token is not None else os.environ.get("DEFECTDOJO_API_KEY")
    actual_base_url = base_url if base_url is not None else os.environ.get("DEFECTDOJO_API_URL")

    if not actual_base_url:
         raise ValueError("DEFECTDOJO_API_URL environment variable or base_url argument must be provided and cannot be empty.")
    
    # Only validate token if requested (e.g., skipped for tests)
    if validate_token and not actual_token:
        raise ValueError("DEFECTDOJO_API_KEY environment variable or token argument must be provided")
    
    return DefectDojoClient(actual_base_url, actual_token)