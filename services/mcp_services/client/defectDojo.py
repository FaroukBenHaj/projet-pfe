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