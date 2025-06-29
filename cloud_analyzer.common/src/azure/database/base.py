"""Base classes for Azure database metrics collection."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import MetricValue


@dataclass
class DatabaseMetrics:
    """Container for database utilization metrics."""
    
    resource_id: str
    database_name: str
    server_name: str
    resource_group: str
    database_type: str
    time_range: Tuple[datetime, datetime]
    cpu_percent_avg: float
    cpu_percent_max: float
    memory_percent_avg: Optional[float] = None
    memory_percent_max: Optional[float] = None
    dtu_percent_avg: Optional[float] = None
    dtu_percent_max: Optional[float] = None
    storage_percent_avg: Optional[float] = None
    storage_percent_max: Optional[float] = None
    io_percent_avg: Optional[float] = None
    io_percent_max: Optional[float] = None
    sessions_percent_avg: Optional[float] = None
    sessions_percent_max: Optional[float] = None
    workers_percent_avg: Optional[float] = None
    workers_percent_max: Optional[float] = None
    additional_metrics: Optional[Dict[str, Any]] = None


class AzureDatabaseMetricsClient(ABC):
    """Abstract base class for Azure database metrics collection."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None
    ):
        """Initialize the database metrics client.
        
        Args:
            credential: Azure credential for authentication
            subscription_id: Azure subscription ID
            monitor_client: Optional pre-configured monitor client
        """
        self.credential = credential
        self.subscription_id = subscription_id
        self._monitor_client = monitor_client
    
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
    async def get_database_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> DatabaseMetrics:
        """Get utilization metrics for a specific database.
        
        Args:
            resource_id: Azure resource ID of the database
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type (Average, Minimum, Maximum, Total)
            interval: Optional time grain interval
            
        Returns:
            DatabaseMetrics object containing utilization data
        """
        ...
    
    @abstractmethod
    async def list_databases(self) -> List[Dict[str, Any]]:
        """List all databases of this type in the subscription.
        
        Returns:
            List of database information dictionaries
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
    
    def _calculate_metric_aggregates(
        self,
        metric_values: List[MetricValue],
        aggregation: str = "Average"
    ) -> Tuple[float, float]:
        """Calculate average and maximum values from metric data.
        
        Args:
            metric_values: List of metric values
            aggregation: Primary aggregation type
            
        Returns:
            Tuple of (average, maximum) values
        """
        if not metric_values:
            return (0.0, 0.0)
        
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
            return (0.0, 0.0)
        
        return (sum(values) / len(values), max(values))
    
    async def _fetch_metric(
        self,
        resource_id: str,
        metric_name: str,
        time_range: Tuple[datetime, datetime],
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> Tuple[float, float]:
        """Fetch a single metric from Azure Monitor.
        
        Args:
            resource_id: Azure resource ID
            metric_name: Name of the metric to fetch
            time_range: Time range for the metric
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            
        Returns:
            Tuple of (average, maximum) values
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
                                aggregation
                            )
            
            return (0.0, 0.0)
            
        except AzureError as e:
            raise AzureError(f"Failed to fetch metric {metric_name}: {str(e)}")
    
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