"""Base interfaces for cloud providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set

from models.base import CloudProvider, Resource, ResourceType


class CloudProviderInterface(ABC):
    """Abstract interface for cloud provider implementations."""
    
    def __init__(self, credentials: Optional[Dict[str, Any]] = None) -> None:
        """Initialize provider with credentials.
        
        Args:
            credentials: Provider-specific credentials (optional)
        """
        self.credentials = credentials or {}
        self._client: Optional[Any] = None
    
    @property
    @abstractmethod
    def provider(self) -> CloudProvider:
        """Return the cloud provider type."""
        pass
    
    @abstractmethod
    async def validate_credentials(self) -> bool:
        """Validate that credentials are valid.
        
        Returns:
            True if credentials are valid
        """
        pass
    
    @abstractmethod
    async def list_regions(self) -> List[str]:
        """List available regions for this provider.
        
        Returns:
            List of region identifiers
        """
        pass
    
    # Resource discovery methods
    
    @abstractmethod
    async def list_instances(self, region: str) -> List[Resource]:
        """List compute instances in a region.
        
        Args:
            region: Region identifier
            
        Returns:
            List of compute instance resources
        """
        pass
    
    @abstractmethod
    async def list_volumes(self, region: str) -> List[Resource]:
        """List storage volumes in a region.
        
        Args:
            region: Region identifier
            
        Returns:
            List of storage volume resources
        """
        pass
    
    @abstractmethod
    async def list_snapshots(self, region: str) -> List[Resource]:
        """List snapshots in a region.
        
        Args:
            region: Region identifier
            
        Returns:
            List of snapshot resources
        """
        pass
    
    @abstractmethod
    async def list_databases(self, region: str) -> List[Resource]:
        """List database instances in a region.
        
        Args:
            region: Region identifier
            
        Returns:
            List of database resources
        """
        pass
    
    @abstractmethod
    async def list_load_balancers(self, region: str) -> List[Resource]:
        """List load balancers in a region.
        
        Args:
            region: Region identifier
            
        Returns:
            List of load balancer resources
        """
        pass
    
    @abstractmethod
    async def list_ip_addresses(self, region: str) -> List[Resource]:
        """List IP addresses in a region.
        
        Args:
            region: Region identifier
            
        Returns:
            List of IP address resources
        """
        pass
    
    # Metrics and utilization methods
    
    @abstractmethod
    async def get_instance_metrics(
        self, instance_id: str, region: str, days: int = 7
    ) -> Dict[str, Any]:
        """Get utilization metrics for an instance.
        
        Args:
            instance_id: Instance identifier
            region: Region identifier
            days: Number of days of metrics to retrieve
            
        Returns:
            Dictionary with metric data
        """
        pass
    
    @abstractmethod
    async def get_volume_metrics(
        self, volume_id: str, region: str, days: int = 7
    ) -> Dict[str, Any]:
        """Get utilization metrics for a volume.
        
        Args:
            volume_id: Volume identifier
            region: Region identifier
            days: Number of days of metrics to retrieve
            
        Returns:
            Dictionary with metric data
        """
        pass
    
    # Cost and pricing methods
    
    @abstractmethod
    async def estimate_monthly_cost(self, resource: Resource) -> float:
        """Estimate monthly cost for a resource.
        
        Args:
            resource: Resource to estimate cost for
            
        Returns:
            Estimated monthly cost in USD
        """
        pass
    
    # Additional methods for specific checks
    
    @abstractmethod
    async def get_volume_info(self, volume_id: str, region: str) -> Dict[str, Any]:
        """Get detailed information about a volume.
        
        Args:
            volume_id: Volume identifier
            region: Region identifier
            
        Returns:
            Dictionary with volume information including attachment status
        """
        pass
    
    @abstractmethod
    async def get_snapshot_info(self, snapshot_id: str, region: str) -> Dict[str, Any]:
        """Get detailed information about a snapshot.
        
        Args:
            snapshot_id: Snapshot identifier
            region: Region identifier
            
        Returns:
            Dictionary with snapshot information
        """
        pass
    
    @abstractmethod
    async def get_database_metrics(
        self, database_id: str, region: str, days: int = 7
    ) -> Dict[str, Any]:
        """Get utilization metrics for a database.
        
        Args:
            database_id: Database identifier
            region: Region identifier
            days: Number of days of metrics to retrieve
            
        Returns:
            Dictionary with metric data
        """
        pass
    
    @abstractmethod
    async def get_database_info(self, database_id: str, region: str) -> Dict[str, Any]:
        """Get detailed information about a database instance.
        
        Args:
            database_id: Database identifier
            region: Region identifier
            
        Returns:
            Dictionary with database information
        """
        pass
    
    @abstractmethod
    async def get_database_sizing_recommendations(
        self, database_id: str, region: str, metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get database sizing recommendations.
        
        Args:
            database_id: Database identifier
            region: Region identifier
            metrics: Current metrics data
            
        Returns:
            List of sizing recommendations
        """
        pass
    
    @abstractmethod
    async def get_reserved_instances_utilization(
        self, region: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get reserved instances utilization data.
        
        Args:
            region: Optional region filter
            
        Returns:
            Dictionary with RI utilization data
        """
        pass
    
    @abstractmethod
    async def get_on_demand_ri_opportunities(
        self, resources: List[Resource], region: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get on-demand instances that could use reserved instances.
        
        Args:
            resources: List of resources to analyze
            region: Optional region filter
            
        Returns:
            List of RI purchase opportunities
        """
        pass
    
    @abstractmethod
    async def get_savings_plans_coverage(
        self, region: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get savings plans coverage data.
        
        Args:
            region: Optional region filter (unused for savings plans)
            
        Returns:
            Dictionary with savings plans coverage data
        """
        pass
    
    @abstractmethod
    async def list_resources(
        self, resource_types: Optional[Set[ResourceType]] = None,
        regions: Optional[Set[str]] = None
    ) -> List[Resource]:
        """List all resources.
        
        Args:
            resource_types: Optional set of resource types to filter
            regions: Optional set of regions to filter
            
        Returns:
            List of resources
        """
        pass


class ProviderFactory:
    """Factory for creating provider instances."""
    
    _providers: Dict[CloudProvider, type[CloudProviderInterface]] = {}
    
    @classmethod
    def register(
        cls, provider: CloudProvider, implementation: type[CloudProviderInterface]
    ) -> None:
        """Register a provider implementation.
        
        Args:
            provider: Cloud provider type
            implementation: Provider implementation class
        """
        cls._providers[provider] = implementation
    
    @classmethod
    def create(
        cls, provider: CloudProvider, credentials: Dict[str, Any]
    ) -> CloudProviderInterface:
        """Create a provider instance.
        
        Args:
            provider: Cloud provider type
            credentials: Provider credentials
            
        Returns:
            Provider implementation instance
            
        Raises:
            ValueError: If provider is not registered
        """
        if provider not in cls._providers:
            raise ValueError(f"Provider {provider} not registered")
        
        return cls._providers[provider](credentials)