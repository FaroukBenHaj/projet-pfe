import httpx
import os
from typing import Any, Dict, Optional
class BaseClient:
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
