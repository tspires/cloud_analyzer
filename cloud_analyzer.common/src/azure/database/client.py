"""Unified Azure database metrics wrapper client with error handling."""
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError, ClientAuthenticationError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

from .base import DatabaseMetrics
from .mysql import MySQLMetricsClient
from .postgresql import PostgreSQLMetricsClient
from .sql_database import SqlDatabaseMetricsClient


logger = logging.getLogger(__name__)


class AzureDatabaseMetricsWrapper:
    """Unified wrapper for Azure database metrics collection with comprehensive error handling."""
    
    def __init__(
        self,
        credential: Optional[TokenCredential] = None,
        subscription_id: Optional[str] = None,
        retry_count: int = 3,
        retry_delay: float = 1.0,
        timeout: float = 30.0,
        concurrent_requests: int = 10
    ):
        """Initialize the Azure database metrics wrapper.
        
        Args:
            credential: Azure credential for authentication (defaults to DefaultAzureCredential)
            subscription_id: Azure subscription ID (can be set later)
            retry_count: Number of retries for failed operations
            retry_delay: Delay between retries in seconds
            timeout: Timeout for operations in seconds
            concurrent_requests: Maximum concurrent API requests
        """
        self.credential = credential or DefaultAzureCredential()
        self.subscription_id = subscription_id
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.concurrent_requests = concurrent_requests
        
        self._monitor_client = None
        self._sql_client = None
        self._postgresql_client = None
        self._mysql_client = None
        
        # Configure logging
        self._setup_logging()
        
        # Semaphore for rate limiting
        self._semaphore = asyncio.Semaphore(concurrent_requests)
    
    def _setup_logging(self):
        """Configure logging for the metrics wrapper."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        if not logger.handlers:
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    @asynccontextmanager
    async def _error_handler(self, operation: str, resource: str = ""):
        """Context manager for consistent error handling.
        
        Args:
            operation: Description of the operation being performed
            resource: Optional resource identifier
        """
        try:
            yield
        except ClientAuthenticationError as e:
            logger.error(f"Authentication failed for {operation} on {resource}: {str(e)}")
            raise AzureError(f"Authentication failed. Please check your credentials: {str(e)}")
        except ResourceNotFoundError as e:
            logger.error(f"Resource not found for {operation} on {resource}: {str(e)}")
            raise AzureError(f"Resource not found: {resource}")
        except AzureError as e:
            logger.error(f"Azure error during {operation} on {resource}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during {operation} on {resource}: {str(e)}")
            raise AzureError(f"Unexpected error: {str(e)}")
    
    async def _retry_operation(self, operation, *args, **kwargs):
        """Retry an operation with exponential backoff.
        
        Args:
            operation: The async function to retry
            *args: Positional arguments for the operation
            **kwargs: Keyword arguments for the operation
            
        Returns:
            The result of the operation
        """
        last_error = None
        
        for attempt in range(self.retry_count):
            try:
                async with self._semaphore:  # Rate limiting
                    return await asyncio.wait_for(
                        operation(*args, **kwargs),
                        timeout=self.timeout
                    )
            except asyncio.TimeoutError:
                last_error = TimeoutError(f"Operation timed out after {self.timeout} seconds")
                logger.warning(f"Attempt {attempt + 1} timed out, retrying...")
            except Exception as e:
                last_error = e
                if attempt < self.retry_count - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}, retrying in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {self.retry_count} attempts failed")
        
        raise last_error
    
    def set_subscription(self, subscription_id: str):
        """Set or update the Azure subscription ID.
        
        Args:
            subscription_id: Azure subscription ID
        """
        self.subscription_id = subscription_id
        # Reset clients to force recreation with new subscription
        self._monitor_client = None
        self._sql_client = None
        self._postgresql_client = None
        self._mysql_client = None
    
    def _validate_subscription(self):
        """Validate that subscription ID is set."""
        if not self.subscription_id:
            raise ValueError("Subscription ID not set. Call set_subscription() first.")
    
    def _get_database_type(self, resource_id: str) -> str:
        """Determine database type from resource ID.
        
        Args:
            resource_id: Azure resource ID
            
        Returns:
            Database type string
        """
        resource_id_lower = resource_id.lower()
        
        if '/microsoft.sql/' in resource_id_lower:
            return 'sql'
        elif '/microsoft.dbforpostgresql/' in resource_id_lower:
            return 'postgresql'
        elif '/microsoft.dbformysql/' in resource_id_lower:
            return 'mysql'
        else:
            raise ValueError(f"Unknown database type in resource ID: {resource_id}")
    
    @property
    def sql_metrics_client(self) -> SqlDatabaseMetricsClient:
        """Get or create SQL Database metrics client."""
        if not self._sql_client:
            self._validate_subscription()
            self._sql_client = SqlDatabaseMetricsClient(
                credential=self.credential,
                subscription_id=self.subscription_id,
                monitor_client=self._monitor_client
            )
        return self._sql_client
    
    @property
    def postgresql_metrics_client(self) -> PostgreSQLMetricsClient:
        """Get or create PostgreSQL metrics client."""
        if not self._postgresql_client:
            self._validate_subscription()
            self._postgresql_client = PostgreSQLMetricsClient(
                credential=self.credential,
                subscription_id=self.subscription_id,
                monitor_client=self._monitor_client
            )
        return self._postgresql_client
    
    @property
    def mysql_metrics_client(self) -> MySQLMetricsClient:
        """Get or create MySQL metrics client."""
        if not self._mysql_client:
            self._validate_subscription()
            self._mysql_client = MySQLMetricsClient(
                credential=self.credential,
                subscription_id=self.subscription_id,
                monitor_client=self._monitor_client
            )
        return self._mysql_client
    
    async def get_database_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None
    ) -> DatabaseMetrics:
        """Get metrics for any Azure database type.
        
        Args:
            resource_id: Azure resource ID of the database
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            
        Returns:
            DatabaseMetrics object
        """
        async with self._error_handler("get_database_metrics", resource_id):
            db_type = self._get_database_type(resource_id)
            
            if db_type == 'sql':
                client = self.sql_metrics_client
            elif db_type == 'postgresql':
                client = self.postgresql_metrics_client
            elif db_type == 'mysql':
                client = self.mysql_metrics_client
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
            
            return await self._retry_operation(
                client.get_database_metrics,
                resource_id,
                time_range,
                aggregation,
                interval
            )
    
    async def list_all_databases(self) -> Dict[str, List[Dict[str, Any]]]:
        """List all databases across all supported types.
        
        Returns:
            Dictionary with database type as key and list of databases as value
        """
        self._validate_subscription()
        results = {
            'sql': [],
            'postgresql': [],
            'mysql': []
        }
        
        # Collect all databases concurrently
        tasks = []
        
        async def collect_sql():
            async with self._error_handler("list_sql_databases"):
                results['sql'] = await self._retry_operation(
                    self.sql_metrics_client.list_databases
                )
        
        async def collect_postgresql():
            async with self._error_handler("list_postgresql_databases"):
                results['postgresql'] = await self._retry_operation(
                    self.postgresql_metrics_client.list_databases
                )
        
        async def collect_mysql():
            async with self._error_handler("list_mysql_databases"):
                results['mysql'] = await self._retry_operation(
                    self.mysql_metrics_client.list_databases
                )
        
        tasks = [collect_sql(), collect_postgresql(), collect_mysql()]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    async def get_all_database_metrics(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None,
        database_types: Optional[List[str]] = None
    ) -> List[DatabaseMetrics]:
        """Get metrics for all databases in the subscription.
        
        Args:
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            database_types: Optional list of database types to include
            
        Returns:
            List of DatabaseMetrics objects
        """
        if not database_types:
            database_types = ['sql', 'postgresql', 'mysql']
        
        # First, list all databases
        all_databases = await self.list_all_databases()
        
        # Collect metrics for all databases
        metrics_tasks = []
        
        for db_type, databases in all_databases.items():
            if db_type not in database_types:
                continue
            
            for db in databases:
                resource_id = db.get('id')
                if resource_id:
                    task = self.get_database_metrics(
                        resource_id,
                        time_range,
                        aggregation,
                        interval
                    )
                    metrics_tasks.append(task)
        
        # Gather all metrics concurrently
        results = await asyncio.gather(*metrics_tasks, return_exceptions=True)
        
        # Filter out exceptions and return successful results
        metrics = []
        for result in results:
            if isinstance(result, DatabaseMetrics):
                metrics.append(result)
            elif isinstance(result, Exception):
                logger.warning(f"Failed to get metrics for a database: {str(result)}")
        
        return metrics
    
    async def get_optimization_recommendations(
        self,
        resource_id: Optional[str] = None,
        metrics: Optional[Union[DatabaseMetrics, List[DatabaseMetrics]]] = None,
        include_all: bool = False
    ) -> Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]:
        """Get optimization recommendations for databases.
        
        Args:
            resource_id: Optional specific database resource ID
            metrics: Optional pre-collected metrics
            include_all: If True, analyze all databases in subscription
            
        Returns:
            List of recommendations for single database or dict for multiple
        """
        if include_all or (not resource_id and not metrics):
            # Get recommendations for all databases
            all_metrics = await self.get_all_database_metrics()
            all_recommendations = {}
            
            for metric in all_metrics:
                db_type = self._get_database_type(metric.resource_id)
                
                if db_type == 'sql':
                    client = self.sql_metrics_client
                elif db_type == 'postgresql':
                    client = self.postgresql_metrics_client
                elif db_type == 'mysql':
                    client = self.mysql_metrics_client
                else:
                    continue
                
                try:
                    recommendations = await client.get_database_recommendations(
                        metric.resource_id,
                        metric
                    )
                    if recommendations:
                        all_recommendations[metric.database_name] = recommendations
                except Exception as e:
                    logger.warning(f"Failed to get recommendations for {metric.database_name}: {str(e)}")
            
            return all_recommendations
        
        elif resource_id:
            # Get recommendations for specific database
            async with self._error_handler("get_recommendations", resource_id):
                db_type = self._get_database_type(resource_id)
                
                if db_type == 'sql':
                    client = self.sql_metrics_client
                elif db_type == 'postgresql':
                    client = self.postgresql_metrics_client
                elif db_type == 'mysql':
                    client = self.mysql_metrics_client
                else:
                    raise ValueError(f"Unsupported database type: {db_type}")
                
                return await self._retry_operation(
                    client.get_database_recommendations,
                    resource_id,
                    metrics
                )
        
        else:
            raise ValueError("Either resource_id or include_all must be specified")
    
    async def close(self):
        """Close all client connections."""
        # Azure SDK clients handle connection cleanup automatically
        logger.info("Closed Azure database metrics wrapper")