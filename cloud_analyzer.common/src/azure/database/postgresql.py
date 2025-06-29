"""Azure PostgreSQL database metrics collection implementation."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient as FlexiblePostgreSQLClient

from .base import AzureDatabaseMetricsClient, DatabaseMetrics


logger = logging.getLogger(__name__)


class PostgreSQLMetricsClient(AzureDatabaseMetricsClient):
    """Client for collecting Azure PostgreSQL metrics (Single Server and Flexible Server)."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None,
        postgresql_client: Optional[PostgreSQLManagementClient] = None,
        flexible_postgresql_client: Optional[FlexiblePostgreSQLClient] = None
    ):
        """Initialize PostgreSQL metrics client.
        
        Args:
            credential: Azure credential for authentication
            subscription_id: Azure subscription ID
            monitor_client: Optional pre-configured monitor client
            postgresql_client: Optional pre-configured PostgreSQL client
            flexible_postgresql_client: Optional pre-configured Flexible PostgreSQL client
        """
        super().__init__(credential, subscription_id, monitor_client)
        self._postgresql_client = postgresql_client
        self._flexible_postgresql_client = flexible_postgresql_client
    
    @property
    def postgresql_client(self) -> PostgreSQLManagementClient:
        """Get or create the PostgreSQL management client."""
        if not self._postgresql_client:
            self._postgresql_client = PostgreSQLManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._postgresql_client
    
    @property
    def flexible_postgresql_client(self) -> FlexiblePostgreSQLClient:
        """Get or create the Flexible PostgreSQL management client."""
        if not self._flexible_postgresql_client:
            self._flexible_postgresql_client = FlexiblePostgreSQLClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._flexible_postgresql_client
    
    async def get_database_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> DatabaseMetrics:
        """Get utilization metrics for an Azure PostgreSQL database.
        
        Args:
            resource_id: Azure resource ID of the database server
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type (Average, Minimum, Maximum, Total)
            interval: Optional time grain interval
            
        Returns:
            DatabaseMetrics object containing utilization data
        """
        if not time_range:
            time_range = self._get_default_time_range()
        
        # Parse resource information
        resource_info = self._parse_resource_id(resource_id)
        server_name = resource_info['resource_name']
        is_flexible = 'flexibleServers' in resource_id
        
        metrics = {
            'resource_id': resource_id,
            'database_name': server_name,  # For PostgreSQL, we track at server level
            'server_name': server_name,
            'resource_group': resource_info['resource_group'],
            'database_type': 'Azure PostgreSQL Flexible Server' if is_flexible else 'Azure PostgreSQL Single Server',
            'time_range': time_range
        }
        
        try:
            if is_flexible:
                # Flexible Server metrics
                cpu_avg, cpu_max = await self._fetch_metric(
                    resource_id, 'cpu_percent', time_range, aggregation, interval
                )
                metrics['cpu_percent_avg'] = cpu_avg
                metrics['cpu_percent_max'] = cpu_max
                
                memory_avg, memory_max = await self._fetch_metric(
                    resource_id, 'memory_percent', time_range, aggregation, interval
                )
                metrics['memory_percent_avg'] = memory_avg
                metrics['memory_percent_max'] = memory_max
                
                storage_avg, storage_max = await self._fetch_metric(
                    resource_id, 'storage_percent', time_range, aggregation, interval
                )
                metrics['storage_percent_avg'] = storage_avg
                metrics['storage_percent_max'] = storage_max
                
                io_avg, io_max = await self._fetch_metric(
                    resource_id, 'disk_iops_consumed_percentage', time_range, aggregation, interval
                )
                metrics['io_percent_avg'] = io_avg
                metrics['io_percent_max'] = io_max
                
                # Active connections
                connections_avg, connections_max = await self._fetch_metric(
                    resource_id, 'active_connections', time_range, aggregation, interval
                )
                
                # Network throughput
                network_in_avg, network_in_max = await self._fetch_metric(
                    resource_id, 'network_bytes_ingress', time_range, aggregation, interval
                )
                network_out_avg, network_out_max = await self._fetch_metric(
                    resource_id, 'network_bytes_egress', time_range, aggregation, interval
                )
                
                metrics['additional_metrics'] = {
                    'active_connections_avg': connections_avg,
                    'active_connections_max': connections_max,
                    'network_in_bytes_avg': network_in_avg,
                    'network_out_bytes_avg': network_out_avg
                }
                
            else:
                # Single Server metrics
                cpu_avg, cpu_max = await self._fetch_metric(
                    resource_id, 'cpu_percent', time_range, aggregation, interval
                )
                metrics['cpu_percent_avg'] = cpu_avg
                metrics['cpu_percent_max'] = cpu_max
                
                memory_avg, memory_max = await self._fetch_metric(
                    resource_id, 'memory_percent', time_range, aggregation, interval
                )
                metrics['memory_percent_avg'] = memory_avg
                metrics['memory_percent_max'] = memory_max
                
                storage_avg, storage_max = await self._fetch_metric(
                    resource_id, 'storage_percent', time_range, aggregation, interval
                )
                metrics['storage_percent_avg'] = storage_avg
                metrics['storage_percent_max'] = storage_max
                
                # IO percent for single server
                io_avg, io_max = await self._fetch_metric(
                    resource_id, 'io_consumption_percent', time_range, aggregation, interval
                )
                metrics['io_percent_avg'] = io_avg
                metrics['io_percent_max'] = io_max
                
                # Connection metrics
                connections_avg, connections_max = await self._fetch_metric(
                    resource_id, 'active_connections', time_range, aggregation, interval
                )
                failed_connections_avg, failed_connections_max = await self._fetch_metric(
                    resource_id, 'connections_failed', time_range, aggregation, interval
                )
                
                metrics['additional_metrics'] = {
                    'active_connections_avg': connections_avg,
                    'active_connections_max': connections_max,
                    'failed_connections_avg': failed_connections_avg,
                    'failed_connections_max': failed_connections_max
                }
            
        except AzureError as e:
            logger.error(f"Failed to fetch metrics for PostgreSQL server {server_name}: {str(e)}")
            raise
        
        return DatabaseMetrics(**metrics)
    
    async def list_databases(self) -> List[Dict[str, Any]]:
        """List all PostgreSQL servers in the subscription.
        
        Returns:
            List of server information dictionaries
        """
        databases = []
        
        try:
            # List Single Servers
            single_servers = self.postgresql_client.servers.list()
            
            for server in single_servers:
                server_info = {
                    'id': server.id,
                    'name': server.name,
                    'type': 'PostgreSQL Single Server',
                    'resource_group': server.id.split('/')[4],
                    'location': server.location,
                    'version': server.version,
                    'state': server.user_visible_state,
                    'sku': {
                        'name': server.sku.name if server.sku else None,
                        'tier': server.sku.tier if server.sku else None,
                        'capacity': server.sku.capacity if server.sku else None,
                        'family': server.sku.family if server.sku else None
                    },
                    'storage_mb': server.storage_profile.storage_mb if server.storage_profile else None,
                    'backup_retention_days': server.storage_profile.backup_retention_days if server.storage_profile else None,
                    'ssl_enforcement': server.ssl_enforcement,
                    'administrator_login': server.administrator_login,
                    'earliest_restore_date': server.earliest_restore_date.isoformat() if server.earliest_restore_date else None
                }
                databases.append(server_info)
            
            # List Flexible Servers
            flexible_servers = self.flexible_postgresql_client.servers.list()
            
            for server in flexible_servers:
                server_info = {
                    'id': server.id,
                    'name': server.name,
                    'type': 'PostgreSQL Flexible Server',
                    'resource_group': server.id.split('/')[4],
                    'location': server.location,
                    'version': server.version,
                    'state': server.state,
                    'sku': {
                        'name': server.sku.name if server.sku else None,
                        'tier': server.sku.tier if server.sku else None
                    },
                    'storage_size_gb': server.storage.storage_size_gb if server.storage else None,
                    'backup_retention_days': server.backup.backup_retention_days if server.backup else None,
                    'high_availability': server.high_availability.mode if server.high_availability else None,
                    'administrator_login': server.administrator_login,
                    'availability_zone': server.availability_zone
                }
                databases.append(server_info)
            
        except AzureError as e:
            logger.error(f"Failed to list PostgreSQL servers: {str(e)}")
            raise
        
        return databases
    
    async def get_database_recommendations(
        self,
        resource_id: str,
        metrics: Optional[DatabaseMetrics] = None,
        threshold_cpu: float = 40.0,
        threshold_memory: float = 40.0,
        threshold_storage: float = 80.0,
        threshold_io: float = 40.0
    ) -> List[Dict[str, Any]]:
        """Get optimization recommendations based on metrics.
        
        Args:
            resource_id: Azure resource ID of the database
            metrics: Optional pre-collected metrics
            threshold_cpu: CPU usage threshold for downsizing
            threshold_memory: Memory usage threshold for downsizing
            threshold_storage: Storage usage threshold for warnings
            threshold_io: IO usage threshold for optimization
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        if not metrics:
            metrics = await self.get_database_metrics(resource_id)
        
        # Check for low utilization
        if metrics.cpu_percent_avg < threshold_cpu and metrics.cpu_percent_max < threshold_cpu * 1.5:
            recommendations.append({
                'type': 'downsize',
                'severity': 'medium',
                'description': f'PostgreSQL server has low CPU utilization ({metrics.cpu_percent_avg:.1f}% avg, {metrics.cpu_percent_max:.1f}% max)',
                'impact': 'cost_savings',
                'action': 'Consider downsizing to a smaller compute tier'
            })
        
        if metrics.memory_percent_avg and metrics.memory_percent_avg < threshold_memory:
            recommendations.append({
                'type': 'downsize',
                'severity': 'low',
                'description': f'PostgreSQL server has low memory utilization ({metrics.memory_percent_avg:.1f}%)',
                'impact': 'cost_savings',
                'action': 'Review memory configuration and consider downsizing'
            })
        
        if metrics.io_percent_avg and metrics.io_percent_avg < threshold_io:
            recommendations.append({
                'type': 'optimize',
                'severity': 'low',
                'description': f'PostgreSQL server has low IO utilization ({metrics.io_percent_avg:.1f}%)',
                'impact': 'cost_savings',
                'action': 'Consider moving to a lower IOPS tier if using premium storage'
            })
        
        # Check for high utilization
        if metrics.cpu_percent_max > 90:
            recommendations.append({
                'type': 'upsize',
                'severity': 'high',
                'description': f'PostgreSQL server reached high CPU utilization ({metrics.cpu_percent_max:.1f}%)',
                'impact': 'performance',
                'action': 'Consider scaling up compute resources'
            })
        
        if metrics.memory_percent_max and metrics.memory_percent_max > 90:
            recommendations.append({
                'type': 'upsize',
                'severity': 'high',
                'description': f'PostgreSQL server reached high memory utilization ({metrics.memory_percent_max:.1f}%)',
                'impact': 'performance',
                'action': 'Consider increasing memory allocation'
            })
        
        if metrics.storage_percent_avg and metrics.storage_percent_avg > threshold_storage:
            recommendations.append({
                'type': 'storage',
                'severity': 'medium' if metrics.storage_percent_avg < 90 else 'high',
                'description': f'PostgreSQL server storage is {metrics.storage_percent_avg:.1f}% full',
                'impact': 'availability',
                'action': 'Increase storage size or implement data archiving'
            })
        
        # Check connection metrics if available
        if metrics.additional_metrics:
            if 'failed_connections_avg' in metrics.additional_metrics:
                if metrics.additional_metrics['failed_connections_avg'] > 10:
                    recommendations.append({
                        'type': 'configuration',
                        'severity': 'medium',
                        'description': f'High number of failed connections detected',
                        'impact': 'availability',
                        'action': 'Review connection pooling and authentication settings'
                    })
        
        return recommendations