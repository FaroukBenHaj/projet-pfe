import os
from ..client.defect_dojo import DefectDojoClient

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