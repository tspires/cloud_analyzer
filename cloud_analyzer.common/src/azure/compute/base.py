"""Base classes for Azure compute metrics collection."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import MetricValue


class ComputeResourceType(Enum):
    """Enumeration of Azure compute resource types."""
    
    VIRTUAL_MACHINE = "Microsoft.Compute/virtualMachines"
    VM_SCALE_SET = "Microsoft.Compute/virtualMachineScaleSets"
    APP_SERVICE = "Microsoft.Web/sites"
    FUNCTION_APP = "Microsoft.Web/sites"  # Functions are a type of Web App
    CONTAINER_INSTANCE = "Microsoft.ContainerInstance/containerGroups"
    AKS_CLUSTER = "Microsoft.ContainerService/managedClusters"
    BATCH_ACCOUNT = "Microsoft.Batch/batchAccounts"
    CLOUD_SERVICE = "Microsoft.Compute/cloudServices"
    SERVICE_FABRIC = "Microsoft.ServiceFabric/clusters"
    CONTAINER_APP = "Microsoft.App/containerApps"
    LOGIC_APP = "Microsoft.Logic/workflows"
    SPRING_APP = "Microsoft.AppPlatform/Spring"
    ARC_SERVER = "Microsoft.HybridCompute/machines"


@dataclass
class ComputeMetrics:
    """Container for compute resource utilization metrics."""
    
    resource_id: str
    resource_name: str
    resource_type: ComputeResourceType
    resource_group: str
    location: str
    time_range: Tuple[datetime, datetime]
    
    # Common metrics
    cpu_percent_avg: float
    cpu_percent_max: float
    cpu_percent_p95: Optional[float] = None
    
    memory_percent_avg: Optional[float] = None
    memory_percent_max: Optional[float] = None
    memory_percent_p95: Optional[float] = None
    
    network_in_bytes_total: Optional[float] = None
    network_out_bytes_total: Optional[float] = None
    
    disk_read_bytes_total: Optional[float] = None
    disk_write_bytes_total: Optional[float] = None
    disk_read_ops_total: Optional[float] = None
    disk_write_ops_total: Optional[float] = None
    
    # Resource-specific metrics
    availability_percent: Optional[float] = None
    instance_count: Optional[int] = None
    request_count: Optional[int] = None
    response_time_avg: Optional[float] = None
    error_count: Optional[int] = None
    
    # Additional metrics dictionary for service-specific data
    additional_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Tags and metadata
    tags: Dict[str, str] = field(default_factory=dict)
    sku: Optional[Dict[str, Any]] = None
    state: Optional[str] = None


@dataclass
class ComputeRecommendation:
    """Optimization recommendation for compute resources."""
    
    resource_id: str
    resource_name: str
    recommendation_type: str  # 'resize', 'shutdown', 'schedule', 'reserved_instance'
    severity: str  # 'high', 'medium', 'low'
    description: str
    impact: str  # 'cost', 'performance', 'availability', 'security'
    estimated_monthly_savings: Optional[float] = None
    estimated_annual_savings: Optional[float] = None
    action_details: Optional[Dict[str, Any]] = None


class AzureComputeMetricsClient(ABC):
    """Abstract base class for Azure compute metrics collection."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None
    ):
        """Initialize the compute metrics client.
        
        Args:
            credential: Azure credential for authentication
            subscription_id: Azure subscription ID
            monitor_client: Optional pre-configured monitor client
        """
        self.credential = credential
        self.subscription_id = subscription_id
        self._monitor_client = monitor_client
        self._resource_cache = {}
    
    @property
    def monitor_client(self) -> MonitorManagementClient:
        """Get or create the monitor management client."""
        if not self._monitor_client:
            self._monitor_client = MonitorManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._monitor_client
    
    @abstractmethod
    async def get_compute_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None,
        include_capacity_metrics: bool = True
    ) -> ComputeMetrics:
        """Get utilization metrics for a specific compute resource.
        
        Args:
            resource_id: Azure resource ID of the compute resource
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type (Average, Minimum, Maximum, Total)
            interval: Optional time grain interval
            include_capacity_metrics: Whether to include capacity/scaling metrics
            
        Returns:
            ComputeMetrics object containing utilization data
        """
        ...
    
    @abstractmethod
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all compute resources of this type in the subscription.
        
        Returns:
            List of resource information dictionaries
        """
        ...
    
    @abstractmethod
    async def get_recommendations(
        self,
        resource_id: str,
        metrics: Optional[ComputeMetrics] = None,
        pricing_tier: Optional[str] = None
    ) -> List[ComputeRecommendation]:
        """Get optimization recommendations for a compute resource.
        
        Args:
            resource_id: Azure resource ID
            metrics: Optional pre-collected metrics
            pricing_tier: Optional pricing tier for cost calculations
            
        Returns:
            List of optimization recommendations
        """
        ...
    
    def _get_default_time_range(self, days: int = 7) -> Tuple[datetime, datetime]:
        """Get default time range for metrics collection.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Tuple of (start_time, end_time)
        """
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=days)
        return (start_time, end_time)
    
    def _format_timespan(self, time_range: Tuple[datetime, datetime]) -> str:
        """Format time range for Azure Monitor API.
        
        Args:
            time_range: Tuple of (start_time, end_time)
            
        Returns:
            ISO format timespan string
        """
        start, end = time_range
        return f"{start.isoformat()}Z/{end.isoformat()}Z"
    
    def _calculate_percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile value from a list of values.
        
        Args:
            values: List of numeric values
            percentile: Percentile to calculate (0-100)
            
        Returns:
            Percentile value
        """
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _calculate_metric_aggregates(
        self,
        metric_values: List[MetricValue],
        aggregation: str = "Average",
        include_percentiles: bool = True
    ) -> Dict[str, float]:
        """Calculate various aggregates from metric data.
        
        Args:
            metric_values: List of metric values
            aggregation: Primary aggregation type
            include_percentiles: Whether to calculate percentiles
            
        Returns:
            Dictionary with aggregated values
        """
        if not metric_values:
            return {"avg": 0.0, "max": 0.0, "min": 0.0, "total": 0.0}
        
        values = []
        for value in metric_values:
            if aggregation == "Average" and value.average is not None:
                values.append(value.average)
            elif aggregation == "Maximum" and value.maximum is not None:
                values.append(value.maximum)
            elif aggregation == "Minimum" and value.minimum is not None:
                values.append(value.minimum)
            elif aggregation == "Total" and value.total is not None:
                values.append(value.total)
        
        if not values:
            return {"avg": 0.0, "max": 0.0, "min": 0.0, "total": 0.0}
        
        result = {
            "avg": sum(values) / len(values),
            "max": max(values),
            "min": min(values),
            "total": sum(values)
        }
        
        if include_percentiles and len(values) > 1:
            result["p50"] = self._calculate_percentile(values, 50)
            result["p95"] = self._calculate_percentile(values, 95)
            result["p99"] = self._calculate_percentile(values, 99)
        
        return result
    
    async def _fetch_metric(
        self,
        resource_id: str,
        metric_name: str,
        time_range: Tuple[datetime, datetime],
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> Dict[str, float]:
        """Fetch a single metric from Azure Monitor.
        
        Args:
            resource_id: Azure resource ID
            metric_name: Name of the metric to fetch
            time_range: Time range for the metric
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            
        Returns:
            Dictionary with aggregated values
        """
        try:
            timespan = self._format_timespan(time_range)
            SECONDS_PER_MINUTE = 60
            time_grain = f"PT{int(interval.total_seconds() / SECONDS_PER_MINUTE)}M" if interval else None
            
            result = self.monitor_client.metrics.list(
                resource_uri=resource_id,
                metricnames=metric_name,
                timespan=timespan,
                interval=time_grain,
                aggregation=aggregation
            )
            
            for metric in result.value:
                if metric.name.value == metric_name and metric.timeseries:
                    for timeseries in metric.timeseries:
                        if timeseries.data:
                            return self._calculate_metric_aggregates(
                                timeseries.data,
                                aggregation,
                                include_percentiles=True
                            )
            
            return {"avg": 0.0, "max": 0.0, "min": 0.0, "total": 0.0}
            
        except AzureError as e:
            raise AzureError(f"Failed to fetch metric {metric_name}: {str(e)}")
    
    async def _fetch_multiple_metrics(
        self,
        resource_id: str,
        metric_names: List[str],
        time_range: Tuple[datetime, datetime],
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> Dict[str, Dict[str, float]]:
        """Fetch multiple metrics in a single API call.
        
        Args:
            resource_id: Azure resource ID
            metric_names: List of metric names to fetch
            time_range: Time range for the metrics
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            
        Returns:
            Dictionary mapping metric names to aggregated values
        """
        try:
            timespan = self._format_timespan(time_range)
            SECONDS_PER_MINUTE = 60
            time_grain = f"PT{int(interval.total_seconds() / SECONDS_PER_MINUTE)}M" if interval else None
            
            result = self.monitor_client.metrics.list(
                resource_uri=resource_id,
                metricnames=",".join(metric_names),
                timespan=timespan,
                interval=time_grain,
                aggregation=aggregation
            )
            
            metrics_data = {}
            for metric in result.value:
                if metric.name.value in metric_names and metric.timeseries:
                    for timeseries in metric.timeseries:
                        if timeseries.data:
                            metrics_data[metric.name.value] = self._calculate_metric_aggregates(
                                timeseries.data,
                                aggregation,
                                include_percentiles=True
                            )
            
            # Fill missing metrics with zeros
            for metric_name in metric_names:
                if metric_name not in metrics_data:
                    metrics_data[metric_name] = {"avg": 0.0, "max": 0.0, "min": 0.0, "total": 0.0}
            
            return metrics_data
            
        except AzureError as e:
            raise AzureError(f"Failed to fetch metrics: {str(e)}")
    
    def _parse_resource_id(self, resource_id: str) -> Dict[str, str]:
        """Parse Azure resource ID into components.
        
        Args:
            resource_id: Azure resource ID
            
        Returns:
            Dictionary with parsed components
        """
        parts = resource_id.split('/')
        result = {
            'subscription': '',
            'resource_group': '',
            'provider': '',
            'resource_type': '',
            'resource_name': ''
        }
        
        for i, part in enumerate(parts):
            if part == 'subscriptions' and i + 1 < len(parts):
                result['subscription'] = parts[i + 1]
            elif part == 'resourceGroups' and i + 1 < len(parts):
                result['resource_group'] = parts[i + 1]
            elif part == 'providers' and i + 1 < len(parts):
                result['provider'] = parts[i + 1]
                if i + 2 < len(parts):
                    result['resource_type'] = parts[i + 2]
                if i + 3 < len(parts):
                    result['resource_name'] = parts[i + 3]
        
        return result
    
    def _estimate_cost_savings(
        self,
        current_size: str,
        recommended_size: str,
        resource_type: ComputeResourceType,
        region: str = "eastus"
    ) -> Tuple[float, float]:
        """Estimate cost savings from resizing.
        
        Args:
            current_size: Current resource size/SKU
            recommended_size: Recommended resource size/SKU
            resource_type: Type of compute resource
            region: Azure region
            
        Returns:
            Tuple of (monthly_savings, annual_savings)
        """
        # This is a simplified estimation - in production, use Azure Pricing API
        # Placeholder values for demonstration
        size_costs = {
            "small": 50,
            "medium": 100,
            "large": 200,
            "xlarge": 400
        }
        
        current_cost = size_costs.get(current_size.lower(), 100)
        recommended_cost = size_costs.get(recommended_size.lower(), 50)
        
        monthly_savings = max(0, current_cost - recommended_cost)
        annual_savings = monthly_savings * 12
        
        return (monthly_savings, annual_savings)