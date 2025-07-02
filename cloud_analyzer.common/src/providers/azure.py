"""Azure cloud provider implementation."""

import asyncio
from typing import List, Dict, Any, Optional, AsyncIterator
from datetime import datetime, timedelta
import logging

from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.core.exceptions import AzureError

from .base import CloudProviderBase
from ..models.base import CloudProvider, CloudResource, ResourceFilter, ResourceType
from ..models.checks import CheckResult
from ..models.metrics import MetricDefinition, MetricData, MetricAggregationType, CollectionRun

logger = logging.getLogger(__name__)


class AzureProvider(CloudProviderBase):
    """Azure cloud provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Azure provider."""
        super().__init__(config)
        self.credential = None
        self.resource_client = None
        self.monitor_client = None
        self.subscription_id = config.get('subscription_id')
        
    async def authenticate(self) -> bool:
        """Authenticate with Azure."""
        try:
            # Try different authentication methods
            if all(key in self.config for key in ['tenant_id', 'client_id', 'client_secret']):
                # Service principal authentication
                self.credential = ClientSecretCredential(
                    tenant_id=self.config['tenant_id'],
                    client_id=self.config['client_id'],
                    client_secret=self.config['client_secret']
                )
            else:
                # Default credential chain (CLI, managed identity, etc.)
                self.credential = DefaultAzureCredential()
            
            # Initialize clients
            self.resource_client = ResourceManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
            self.monitor_client = MonitorManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
            
            self._authenticated = True
            logger.info("Successfully authenticated with Azure")
            return True
            
        except Exception as e:
            logger.error(f"Azure authentication failed: {e}")
            self._authenticated = False
            return False
    
    async def test_connection(self) -> bool:
        """Test connection to Azure."""
        if not self.is_authenticated:
            return False
        
        try:
            # Test by listing resource groups
            list(self.resource_client.resource_groups.list())
            return True
        except Exception as e:
            logger.error(f"Azure connection test failed: {e}")
            return False
    
    async def discover_resources(
        self, 
        resource_filter: Optional[ResourceFilter] = None
    ) -> AsyncIterator[CloudResource]:
        """Discover Azure resources."""
        if not self.is_authenticated:
            raise RuntimeError("Not authenticated with Azure")
        
        try:
            # Apply filters
            resource_groups = resource_filter.resource_groups if resource_filter else None
            resource_types = resource_filter.resource_types if resource_filter else None
            
            if resource_groups:
                # Filter by specific resource groups
                for rg_name in resource_groups:
                    async for resource in self._discover_resources_in_group(rg_name, resource_types):
                        yield resource
            else:
                # Discover in all resource groups
                for rg in self.resource_client.resource_groups.list():
                    async for resource in self._discover_resources_in_group(rg.name, resource_types):
                        yield resource
                        
        except Exception as e:
            logger.error(f"Resource discovery failed: {e}")
            raise
    
    async def _discover_resources_in_group(
        self, 
        resource_group: str, 
        resource_types: Optional[List[str]] = None
    ) -> AsyncIterator[CloudResource]:
        """Discover resources in a specific resource group."""
        try:
            resources = self.resource_client.resources.list_by_resource_group(resource_group)
            
            for resource in resources:
                # Filter by resource type if specified
                if resource_types and resource.type not in resource_types:
                    continue
                
                cloud_resource = CloudResource(
                    id=resource.id,
                    name=resource.name,
                    resource_type=resource.type,
                    location=resource.location,
                    resource_group=resource_group,
                    subscription_id=self.subscription_id,
                    provider=CloudProvider.AZURE,
                    tags=resource.tags or {},
                    properties={}
                )
                
                yield cloud_resource
                
        except Exception as e:
            logger.error(f"Failed to discover resources in group {resource_group}: {e}")
            raise
    
    async def get_resource_by_id(self, resource_id: str) -> Optional[CloudResource]:
        """Get a specific Azure resource by ID."""
        if not self.is_authenticated:
            return None
        
        try:
            # Parse resource ID to extract components
            parts = resource_id.split('/')
            if len(parts) < 5:
                return None
            
            resource_group = parts[4]
            resource_name = parts[-1]
            resource_type = '/'.join(parts[-3:-1])
            
            resource = self.resource_client.resources.get_by_id(
                resource_id, 
                api_version="2021-04-01"
            )
            
            return CloudResource(
                id=resource.id,
                name=resource.name,
                resource_type=resource.type,
                location=resource.location,
                resource_group=resource_group,
                subscription_id=self.subscription_id,
                provider=CloudProvider.AZURE,
                tags=resource.tags or {},
                properties={}
            )
            
        except Exception as e:
            logger.error(f"Failed to get resource {resource_id}: {e}")
            return None
    
    async def get_available_metrics(self, resource_type: str) -> List[MetricDefinition]:
        """Get available metrics for an Azure resource type."""
        # This would typically query Azure Monitor API for metric definitions
        # For now, return common metrics based on resource type
        return self._get_common_metrics_for_type(resource_type)
    
    def _get_common_metrics_for_type(self, resource_type: str) -> List[MetricDefinition]:
        """Get common metrics for Azure resource types."""
        metrics_map = {
            ResourceType.VIRTUAL_MACHINE.value: [
                MetricDefinition(
                    id="vm_cpu_percent",
                    name="Percentage CPU",
                    display_name="CPU Percentage",
                    description="The percentage of allocated compute units that are currently in use",
                    resource_type=resource_type,
                    unit="Percent",
                    aggregation_types=[MetricAggregationType.AVERAGE, MetricAggregationType.MAXIMUM],
                    dimensions=[]
                ),
                MetricDefinition(
                    id="vm_network_in",
                    name="Network In Total",
                    display_name="Network In",
                    description="The number of bytes received on all network interfaces",
                    resource_type=resource_type,
                    unit="Bytes",
                    aggregation_types=[MetricAggregationType.TOTAL],
                    dimensions=[]
                )
            ],
            ResourceType.APP_SERVICE.value: [
                MetricDefinition(
                    id="app_requests",
                    name="Requests",
                    display_name="Requests",
                    description="The total number of requests",
                    resource_type=resource_type,
                    unit="Count",
                    aggregation_types=[MetricAggregationType.TOTAL, MetricAggregationType.COUNT],
                    dimensions=[]
                ),
                MetricDefinition(
                    id="app_response_time",
                    name="Response Time",
                    display_name="Response Time",
                    description="The time taken for the app to serve requests",
                    resource_type=resource_type,
                    unit="Seconds",
                    aggregation_types=[MetricAggregationType.AVERAGE],
                    dimensions=[]
                )
            ]
        }
        
        return metrics_map.get(resource_type, [])
    
    async def collect_metrics(
        self,
        resource: CloudResource,
        metric_names: List[str],
        start_time: datetime,
        end_time: datetime,
        aggregation_interval: str = "PT15M"
    ) -> List[MetricData]:
        """Collect metrics for an Azure resource."""
        if not self.is_authenticated:
            raise RuntimeError("Not authenticated with Azure")
        
        metrics_data = []
        
        try:
            for metric_name in metric_names:
                # Query Azure Monitor for metric data
                metrics = self.monitor_client.metrics.list(
                    resource_uri=resource.id,
                    timespan=f"{start_time.isoformat()}/{end_time.isoformat()}",
                    interval=aggregation_interval,
                    metricnames=metric_name,
                    aggregation="Average"
                )
                
                for metric in metrics.value:
                    for timeseries in metric.timeseries:
                        for data_point in timeseries.data:
                            if data_point.average is not None:
                                metric_data = MetricData(
                                    id="",  # Will be generated in __post_init__
                                    resource_id=resource.id,
                                    metric_name=metric_name,
                                    timestamp=data_point.time_stamp,
                                    value=data_point.average,
                                    aggregation_type=MetricAggregationType.AVERAGE,
                                    dimensions={},
                                    unit=metric.unit.value if metric.unit else "",
                                    collection_run_id=""  # Will be set by collection service
                                )
                                metrics_data.append(metric_data)
                
        except Exception as e:
            logger.error(f"Failed to collect metrics for {resource.id}: {e}")
            raise
        
        return metrics_data
    
    async def run_checks(self, resources: List[CloudResource]) -> List[CheckResult]:
        """Run optimization checks on Azure resources."""
        # This would integrate with the existing check system
        # For now, return empty list
        return []