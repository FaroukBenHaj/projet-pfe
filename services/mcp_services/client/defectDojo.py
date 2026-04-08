import httpx
from typing import Any, Dict, Optional
import os


class DefectDojoClient:
    """DefectDojo API client."""
    
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