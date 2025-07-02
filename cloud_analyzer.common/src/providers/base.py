"""Abstract base class for cloud providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from datetime import datetime

from ..models.base import CloudResource, ResourceFilter
from ..models.checks import CheckResult
from ..models.metrics import MetricDefinition, MetricData, CollectionRun


class CloudProviderBase(ABC):
    """Abstract base class for cloud providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize provider with configuration."""
        self.config = config
        self._authenticated = False
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the cloud provider."""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test connection to the cloud provider."""
        pass
    
    @property
    def is_authenticated(self) -> bool:
        """Check if provider is authenticated."""
        return self._authenticated
    
    @abstractmethod
    async def discover_resources(
        self, 
        resource_filter: Optional[ResourceFilter] = None
    ) -> AsyncIterator[CloudResource]:
        """Discover cloud resources."""
        pass
    
    @abstractmethod
    async def get_resource_by_id(self, resource_id: str) -> Optional[CloudResource]:
        """Get a specific resource by ID."""
        pass
    
    @abstractmethod
    async def get_available_metrics(
        self, 
        resource_type: str
    ) -> List[MetricDefinition]:
        """Get available metrics for a resource type."""
        pass
    
    @abstractmethod
    async def collect_metrics(
        self,
        resource: CloudResource,
        metric_names: List[str],
        start_time: datetime,
        end_time: datetime,
        aggregation_interval: str = "PT15M"
    ) -> List[MetricData]:
        """Collect metrics for a resource."""
        pass
    
    @abstractmethod
    async def run_checks(
        self, 
        resources: List[CloudResource]
    ) -> List[CheckResult]:
        """Run optimization checks on resources."""
        pass
    
    async def cleanup(self):
        """Cleanup provider resources."""
        pass