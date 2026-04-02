from abc import ABC, abstractmethod
from typing import Any, Dict, List
from typing import Any, Dict, Optional

class IEngagementsClient(ABC):
    """Interface defining the contract for Engagements client."""

    @abstractmethod
    def get_engagement(self, engagement_id: int) -> Dict[str, Any]:
        """Retrieve a single engagement by its ID."""
        pass

    @abstractmethod
    def create_engagement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new engagement with the provided data."""
        pass

    @abstractmethod
    def get_engagements(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return a list of all engagements."""
        pass