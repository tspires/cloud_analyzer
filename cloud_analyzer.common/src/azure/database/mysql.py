"""Azure MySQL database metrics collection implementation."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.rdbms.mysql_flexibleservers import MySQLManagementClient as FlexibleMySQLClient

from .base import AzureDatabaseMetricsClient, DatabaseMetrics


logger = logging.getLogger(__name__)


class MySQLMetricsClient(AzureDatabaseMetricsClient):
    """Client for collecting Azure MySQL metrics (Single Server and Flexible Server)."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None,
        mysql_client: Optional[MySQLManagementClient] = None,
        flexible_mysql_client: Optional[FlexibleMySQLClient] = None
    ):
        """Initialize MySQL metrics client.
        
        Args:
            credential: Azure credential for authentication
            subscription_id: Azure subscription ID
            monitor_client: Optional pre-configured monitor client
            mysql_client: Optional pre-configured MySQL client
            flexible_mysql_client: Optional pre-configured Flexible MySQL client
        """
        super().__init__(credential, subscription_id, monitor_client)
        self._mysql_client = mysql_client
        self._flexible_mysql_client = flexible_mysql_client
    
    @property
    def mysql_client(self) -> MySQLManagementClient:
        """Get or create the MySQL management client."""
        if not self._mysql_client:
            self._mysql_client = MySQLManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._mysql_client
    
    @property
    def flexible_mysql_client(self) -> FlexibleMySQLClient:
        """Get or create the Flexible MySQL management client."""
        if not self._flexible_mysql_client:
            self._flexible_mysql_client = FlexibleMySQLClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._flexible_mysql_client
    
    async def get_database_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> DatabaseMetrics:
        """Get utilization metrics for an Azure MySQL database.
        
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
            'database_name': server_name,  # For MySQL, we track at server level
            'server_name': server_name,
            'resource_group': resource_info['resource_group'],
            'database_type': 'Azure MySQL Flexible Server' if is_flexible else 'Azure MySQL Single Server',
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
                    resource_id, 'io_percent', time_range, aggregation, interval
                )
                metrics['io_percent_avg'] = io_avg
                metrics['io_percent_max'] = io_max
                
                # Connection metrics
                connections_avg, connections_max = await self._fetch_metric(
                    resource_id, 'total_connections', time_range, aggregation, interval
                )
                aborted_connections_avg, aborted_connections_max = await self._fetch_metric(
                    resource_id, 'aborted_connections', time_range, aggregation, interval
                )
                
                # Query performance metrics
                queries_avg, queries_max = await self._fetch_metric(
                    resource_id, 'Queries', time_range, aggregation, interval
                )
                slow_queries_avg, slow_queries_max = await self._fetch_metric(
                    resource_id, 'slow_queries', time_range, aggregation, interval
                )
                
                metrics['additional_metrics'] = {
                    'total_connections_avg': connections_avg,
                    'total_connections_max': connections_max,
                    'aborted_connections_avg': aborted_connections_avg,
                    'aborted_connections_max': aborted_connections_max,
                    'queries_per_second_avg': queries_avg,
                    'queries_per_second_max': queries_max,
                    'slow_queries_avg': slow_queries_avg,
                    'slow_queries_max': slow_queries_max
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
                
                # Replication lag (if applicable)
                replication_lag_avg, replication_lag_max = await self._fetch_metric(
                    resource_id, 'seconds_behind_master', time_range, aggregation, interval
                )
                
                metrics['additional_metrics'] = {
                    'active_connections_avg': connections_avg,
                    'active_connections_max': connections_max,
                    'failed_connections_avg': failed_connections_avg,
                    'failed_connections_max': failed_connections_max,
                    'replication_lag_seconds_avg': replication_lag_avg,
                    'replication_lag_seconds_max': replication_lag_max
                }
            
        except AzureError as e:
            logger.error(f"Failed to fetch metrics for MySQL server {server_name}: {str(e)}")
            raise
        
        return DatabaseMetrics(**metrics)
    
    async def list_databases(self) -> List[Dict[str, Any]]:
        """List all MySQL servers in the subscription.
        
        Returns:
            List of server information dictionaries
        """
        databases = []
        
        try:
            # List Single Servers
            single_servers = self.mysql_client.servers.list()
            
            for server in single_servers:
                server_info = {
                    'id': server.id,
                    'name': server.name,
                    'type': 'MySQL Single Server',
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
                    'geo_redundant_backup': server.storage_profile.geo_redundant_backup if server.storage_profile else None,
                    'ssl_enforcement': server.ssl_enforcement,
                    'administrator_login': server.administrator_login,
                    'earliest_restore_date': server.earliest_restore_date.isoformat() if server.earliest_restore_date else None,
                    'replication_role': server.replication_role
                }
                databases.append(server_info)
            
            # List Flexible Servers
            flexible_servers = self.flexible_mysql_client.servers.list()
            
            for server in flexible_servers:
                server_info = {
                    'id': server.id,
                    'name': server.name,
                    'type': 'MySQL Flexible Server',
                    'resource_group': server.id.split('/')[4],
                    'location': server.location,
                    'version': server.version,
                    'state': server.state,
                    'sku': {
                        'name': server.sku.name if server.sku else None,
                        'tier': server.sku.tier if server.sku else None
                    },
                    'storage_size_gb': server.storage.storage_size_gb if server.storage else None,
                    'storage_iops': server.storage.iops if server.storage else None,
                    'backup_retention_days': server.backup.backup_retention_days if server.backup else None,
                    'geo_redundant_backup': server.backup.geo_redundant_backup if server.backup else None,
                    'high_availability': server.high_availability.mode if server.high_availability else None,
                    'administrator_login': server.administrator_login,
                    'availability_zone': server.availability_zone,
                    'replication_role': server.replication_role
                }
                databases.append(server_info)
            
        except AzureError as e:
            logger.error(f"Failed to list MySQL servers: {str(e)}")
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
                'description': f'MySQL server has low CPU utilization ({metrics.cpu_percent_avg:.1f}% avg, {metrics.cpu_percent_max:.1f}% max)',
                'impact': 'cost_savings',
                'action': 'Consider downsizing to a smaller compute tier'
            })
        
        if metrics.memory_percent_avg and metrics.memory_percent_avg < threshold_memory:
            recommendations.append({
                'type': 'downsize',
                'severity': 'low',
                'description': f'MySQL server has low memory utilization ({metrics.memory_percent_avg:.1f}%)',
                'impact': 'cost_savings',
                'action': 'Review memory configuration and consider downsizing'
            })
        
        if metrics.io_percent_avg and metrics.io_percent_avg < threshold_io:
            recommendations.append({
                'type': 'optimize',
                'severity': 'low',
                'description': f'MySQL server has low IO utilization ({metrics.io_percent_avg:.1f}%)',
                'impact': 'cost_savings',
                'action': 'Consider reducing provisioned IOPS if using flexible server'
            })
        
        # Check for high utilization
        if metrics.cpu_percent_max > 90:
            recommendations.append({
                'type': 'upsize',
                'severity': 'high',
                'description': f'MySQL server reached high CPU utilization ({metrics.cpu_percent_max:.1f}%)',
                'impact': 'performance',
                'action': 'Consider scaling up compute resources'
            })
        
        if metrics.memory_percent_max and metrics.memory_percent_max > 90:
            recommendations.append({
                'type': 'upsize',
                'severity': 'high',
                'description': f'MySQL server reached high memory utilization ({metrics.memory_percent_max:.1f}%)',
                'impact': 'performance',
                'action': 'Consider increasing memory allocation or optimizing queries'
            })
        
        if metrics.storage_percent_avg and metrics.storage_percent_avg > threshold_storage:
            recommendations.append({
                'type': 'storage',
                'severity': 'medium' if metrics.storage_percent_avg < 90 else 'high',
                'description': f'MySQL server storage is {metrics.storage_percent_avg:.1f}% full',
                'impact': 'availability',
                'action': 'Increase storage size or implement data archiving/cleanup'
            })
        
        # Check additional metrics if available
        if metrics.additional_metrics:
            # Check for high number of aborted connections
            if 'aborted_connections_avg' in metrics.additional_metrics:
                if metrics.additional_metrics['aborted_connections_avg'] > 10:
                    recommendations.append({
                        'type': 'configuration',
                        'severity': 'medium',
                        'description': 'High number of aborted connections detected',
                        'impact': 'reliability',
                        'action': 'Review connection timeout settings and client configurations'
                    })
            
            # Check for slow queries
            if 'slow_queries_avg' in metrics.additional_metrics:
                if metrics.additional_metrics['slow_queries_avg'] > 5:
                    recommendations.append({
                        'type': 'performance',
                        'severity': 'medium',
                        'description': 'High number of slow queries detected',
                        'impact': 'performance',
                        'action': 'Enable slow query log and optimize problematic queries'
                    })
            
            # Check replication lag
            if 'replication_lag_seconds_avg' in metrics.additional_metrics:
                lag = metrics.additional_metrics['replication_lag_seconds_avg']
                if lag > 60:  # More than 1 minute lag
                    recommendations.append({
                        'type': 'replication',
                        'severity': 'high' if lag > 300 else 'medium',
                        'description': f'Replication lag detected ({lag:.0f} seconds)',
                        'impact': 'data_consistency',
                        'action': 'Investigate replication performance and network connectivity'
                    })
        
        return recommendations