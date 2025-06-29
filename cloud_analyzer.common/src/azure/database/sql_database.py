"""Azure SQL Database metrics collection implementation."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.sql import SqlManagementClient

from .base import AzureDatabaseMetricsClient, DatabaseMetrics


logger = logging.getLogger(__name__)


class SqlDatabaseMetricsClient(AzureDatabaseMetricsClient):
    """Client for collecting Azure SQL Database metrics."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None,
        sql_client: Optional[SqlManagementClient] = None
    ):
        """Initialize SQL Database metrics client.
        
        Args:
            credential: Azure credential for authentication
            subscription_id: Azure subscription ID
            monitor_client: Optional pre-configured monitor client
            sql_client: Optional pre-configured SQL client
        """
        super().__init__(credential, subscription_id, monitor_client)
        self._sql_client = sql_client
    
    @property
    def sql_client(self) -> SqlManagementClient:
        """Get or create the SQL management client."""
        if not self._sql_client:
            self._sql_client = SqlManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._sql_client
    
    async def get_database_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> DatabaseMetrics:
        """Get utilization metrics for an Azure SQL Database.
        
        Args:
            resource_id: Azure resource ID of the database
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
        parts = resource_id.split('/')
        server_name = parts[-3] if len(parts) >= 3 else ""
        database_name = parts[-1]
        
        # Determine if this is a DTU or vCore database
        is_dtu_based = await self._is_dtu_based_database(resource_id)
        
        # Collect common metrics
        metrics = {
            'resource_id': resource_id,
            'database_name': database_name,
            'server_name': server_name,
            'resource_group': resource_info['resource_group'],
            'database_type': 'Azure SQL Database',
            'time_range': time_range
        }
        
        try:
            # CPU metrics (available for all SQL databases)
            cpu_avg, cpu_max = await self._fetch_metric(
                resource_id, 'cpu_percent', time_range, aggregation, interval
            )
            metrics['cpu_percent_avg'] = cpu_avg
            metrics['cpu_percent_max'] = cpu_max
            
            # Storage metrics
            storage_avg, storage_max = await self._fetch_metric(
                resource_id, 'storage_percent', time_range, aggregation, interval
            )
            metrics['storage_percent_avg'] = storage_avg
            metrics['storage_percent_max'] = storage_max
            
            if is_dtu_based:
                # DTU-specific metrics
                dtu_avg, dtu_max = await self._fetch_metric(
                    resource_id, 'dtu_consumption_percent', time_range, aggregation, interval
                )
                metrics['dtu_percent_avg'] = dtu_avg
                metrics['dtu_percent_max'] = dtu_max
            else:
                # vCore-specific metrics
                memory_avg, memory_max = await self._fetch_metric(
                    resource_id, 'memory_percent', time_range, aggregation, interval
                )
                metrics['memory_percent_avg'] = memory_avg
                metrics['memory_percent_max'] = memory_max
                
                # Data IO percentage
                io_avg, io_max = await self._fetch_metric(
                    resource_id, 'data_io_percent', time_range, aggregation, interval
                )
                metrics['io_percent_avg'] = io_avg
                metrics['io_percent_max'] = io_max
                
                # Log IO percentage
                log_io_avg, log_io_max = await self._fetch_metric(
                    resource_id, 'log_write_percent', time_range, aggregation, interval
                )
                
                # Sessions percentage
                sessions_avg, sessions_max = await self._fetch_metric(
                    resource_id, 'sessions_percent', time_range, aggregation, interval
                )
                metrics['sessions_percent_avg'] = sessions_avg
                metrics['sessions_percent_max'] = sessions_max
                
                # Workers percentage
                workers_avg, workers_max = await self._fetch_metric(
                    resource_id, 'workers_percent', time_range, aggregation, interval
                )
                metrics['workers_percent_avg'] = workers_avg
                metrics['workers_percent_max'] = workers_max
                
                # Additional metrics
                metrics['additional_metrics'] = {
                    'log_io_percent_avg': log_io_avg,
                    'log_io_percent_max': log_io_max
                }
            
        except AzureError as e:
            logger.error(f"Failed to fetch metrics for database {database_name}: {str(e)}")
            raise
        
        return DatabaseMetrics(**metrics)
    
    async def list_databases(self) -> List[Dict[str, Any]]:
        """List all SQL databases in the subscription.
        
        Returns:
            List of database information dictionaries
        """
        databases = []
        
        try:
            # List all SQL servers first
            servers = self.sql_client.servers.list()
            
            for server in servers:
                # List databases for each server
                server_databases = self.sql_client.databases.list_by_server(
                    resource_group_name=server.id.split('/')[4],
                    server_name=server.name
                )
                
                for db in server_databases:
                    # Skip system databases
                    if db.name.lower() in ['master', 'tempdb', 'model', 'msdb']:
                        continue
                    
                    database_info = {
                        'id': db.id,
                        'name': db.name,
                        'server_name': server.name,
                        'resource_group': db.id.split('/')[4],
                        'location': db.location,
                        'status': db.status,
                        'service_tier': db.current_service_objective_name,
                        'sku': {
                            'name': db.current_sku.name if db.current_sku else None,
                            'tier': db.current_sku.tier if db.current_sku else None,
                            'capacity': db.current_sku.capacity if db.current_sku else None
                        },
                        'max_size_bytes': db.max_size_bytes,
                        'collation': db.collation,
                        'create_date': db.creation_date.isoformat() if db.creation_date else None,
                        'earliest_restore_date': db.earliest_restore_date.isoformat() if db.earliest_restore_date else None
                    }
                    databases.append(database_info)
            
        except AzureError as e:
            logger.error(f"Failed to list SQL databases: {str(e)}")
            raise
        
        return databases
    
    async def _is_dtu_based_database(self, resource_id: str) -> bool:
        """Check if a database uses DTU pricing model.
        
        Args:
            resource_id: Azure resource ID of the database
            
        Returns:
            True if DTU-based, False if vCore-based
        """
        try:
            parts = resource_id.split('/')
            resource_group = parts[4]
            server_name = parts[-3]
            database_name = parts[-1]
            
            database = self.sql_client.databases.get(
                resource_group_name=resource_group,
                server_name=server_name,
                database_name=database_name
            )
            
            # DTU-based tiers
            dtu_tiers = ['Basic', 'Standard', 'Premium']
            
            if database.current_sku and database.current_sku.tier:
                return database.current_sku.tier in dtu_tiers
            
            # Default to vCore if we can't determine
            return False
            
        except Exception as e:
            logger.warning(f"Could not determine database pricing model: {str(e)}")
            return False
    
    async def get_database_recommendations(
        self,
        resource_id: str,
        metrics: Optional[DatabaseMetrics] = None,
        threshold_cpu: float = 40.0,
        threshold_memory: float = 40.0,
        threshold_dtu: float = 40.0
    ) -> List[Dict[str, Any]]:
        """Get optimization recommendations based on metrics.
        
        Args:
            resource_id: Azure resource ID of the database
            metrics: Optional pre-collected metrics
            threshold_cpu: CPU usage threshold for downsizing
            threshold_memory: Memory usage threshold for downsizing
            threshold_dtu: DTU usage threshold for downsizing
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        if not metrics:
            metrics = await self.get_database_metrics(resource_id)
        
        # Check for low utilization
        if metrics.dtu_percent_avg and metrics.dtu_percent_avg < threshold_dtu:
            recommendations.append({
                'type': 'downsize',
                'severity': 'medium',
                'description': f'Database has low DTU utilization ({metrics.dtu_percent_avg:.1f}%)',
                'impact': 'cost_savings',
                'action': 'Consider moving to a lower DTU tier'
            })
        
        if metrics.cpu_percent_avg < threshold_cpu:
            if not metrics.dtu_percent_avg:  # vCore model
                recommendations.append({
                    'type': 'downsize',
                    'severity': 'medium',
                    'description': f'Database has low CPU utilization ({metrics.cpu_percent_avg:.1f}%)',
                    'impact': 'cost_savings',
                    'action': 'Consider reducing vCore count'
                })
        
        if metrics.memory_percent_avg and metrics.memory_percent_avg < threshold_memory:
            recommendations.append({
                'type': 'optimize',
                'severity': 'low',
                'description': f'Database has low memory utilization ({metrics.memory_percent_avg:.1f}%)',
                'impact': 'cost_savings',
                'action': 'Review memory-intensive operations'
            })
        
        # Check for high utilization
        if metrics.cpu_percent_max > 90:
            recommendations.append({
                'type': 'upsize',
                'severity': 'high',
                'description': f'Database reached high CPU utilization ({metrics.cpu_percent_max:.1f}%)',
                'impact': 'performance',
                'action': 'Consider scaling up to prevent performance issues'
            })
        
        if metrics.storage_percent_avg and metrics.storage_percent_avg > 80:
            recommendations.append({
                'type': 'storage',
                'severity': 'medium',
                'description': f'Database storage is {metrics.storage_percent_avg:.1f}% full',
                'impact': 'availability',
                'action': 'Consider increasing database max size or archiving old data'
            })
        
        return recommendations