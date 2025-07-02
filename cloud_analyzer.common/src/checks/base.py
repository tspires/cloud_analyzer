"""Base class for optimization checks."""

from abc import ABC, abstractmethod
from typing import List, Optional
import logging

from ..models.base import CloudResource
from ..models.checks import CheckResult, CheckRecommendation

logger = logging.getLogger(__name__)


class CheckBase(ABC):
    """Abstract base class for optimization checks."""
    
    # Override these in subclasses
    CHECK_ID: str = ""
    CHECK_NAME: str = ""
    DESCRIPTION: str = ""
    SUPPORTED_RESOURCE_TYPES: List[str] = []
    
    def __init__(self, config: Optional[dict] = None):
        """Initialize check with optional configuration."""
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def run(self, resource: CloudResource) -> CheckResult:
        """Run the optimization check on a resource."""
        pass
    
    def is_applicable(self, resource: CloudResource) -> bool:
        """Check if this optimization check applies to the given resource."""
        return resource.resource_type in self.SUPPORTED_RESOURCE_TYPES
    
    def create_result(
        self, 
        resource: CloudResource, 
        recommendations: List[CheckRecommendation],
        metadata: dict = None,
        error_message: str = None
    ) -> CheckResult:
        """Create a CheckResult instance."""
        from ..models.checks import CheckStatus
        from datetime import datetime
        
        status = CheckStatus.COMPLETED if not error_message else CheckStatus.FAILED
        
        return CheckResult(
            check_id=self.CHECK_ID,
            check_name=self.CHECK_NAME,
            resource=resource,
            status=status,
            timestamp=datetime.utcnow(),
            recommendations=recommendations,
            metadata=metadata or {},
            error_message=error_message
        )