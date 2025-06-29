"""Unified Azure compute metrics wrapper client with error handling."""
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError, ClientAuthenticationError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

from .app_services import AppServiceMetricsClient
from .base import ComputeMetrics, ComputeRecommendation, ComputeResourceType
from .virtual_machines import VirtualMachineMetricsClient


logger = logging.getLogger(__name__)


class AzureComputeMetricsWrapper:
    """Unified wrapper for Azure compute metrics collection with comprehensive error handling."""
    
    def __init__(
        self,
        credential: Optional[TokenCredential] = None,
        subscription_id: Optional[str] = None,
        retry_count: int = 3,
        retry_delay: float = 1.0,
        timeout: float = 30.0,
        concurrent_requests: int = 10
    ):
        """Initialize the Azure compute metrics wrapper.
        
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
        self._vm_client = None
        self._app_service_client = None
        # Add more clients as implemented
        
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
        self._vm_client = None
        self._app_service_client = None
    
    def _validate_subscription(self):
        """Validate that subscription ID is set."""
        if not self.subscription_id:
            raise ValueError("Subscription ID not set. Call set_subscription() first.")
    
    def _get_resource_type(self, resource_id: str) -> ComputeResourceType:
        """Determine compute resource type from resource ID.
        
        Args:
            resource_id: Azure resource ID
            
        Returns:
            ComputeResourceType enum value
        """
        resource_id_lower = resource_id.lower()
        
        if '/microsoft.compute/virtualmachines/' in resource_id_lower:
            return ComputeResourceType.VIRTUAL_MACHINE
        elif '/microsoft.compute/virtualmachinescalesets/' in resource_id_lower:
            return ComputeResourceType.VM_SCALE_SET
        elif '/microsoft.web/sites/' in resource_id_lower:
            return ComputeResourceType.APP_SERVICE
        elif '/microsoft.containerinstance/containergroups/' in resource_id_lower:
            return ComputeResourceType.CONTAINER_INSTANCE
        elif '/microsoft.containerservice/managedclusters/' in resource_id_lower:
            return ComputeResourceType.AKS_CLUSTER
        elif '/microsoft.batch/batchaccounts/' in resource_id_lower:
            return ComputeResourceType.BATCH_ACCOUNT
        else:
            raise ValueError(f"Unknown compute resource type in resource ID: {resource_id}")
    
    @property
    def vm_metrics_client(self) -> VirtualMachineMetricsClient:
        """Get or create VM metrics client."""
        if not self._vm_client:
            self._validate_subscription()
            self._vm_client = VirtualMachineMetricsClient(
                credential=self.credential,
                subscription_id=self.subscription_id,
                monitor_client=self._monitor_client
            )
        return self._vm_client
    
    @property
    def app_service_metrics_client(self) -> AppServiceMetricsClient:
        """Get or create App Service metrics client."""
        if not self._app_service_client:
            self._validate_subscription()
            self._app_service_client = AppServiceMetricsClient(
                credential=self.credential,
                subscription_id=self.subscription_id,
                monitor_client=self._monitor_client
            )
        return self._app_service_client
    
    async def get_compute_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None,
        include_capacity_metrics: bool = True
    ) -> ComputeMetrics:
        """Get metrics for any Azure compute resource type.
        
        Args:
            resource_id: Azure resource ID of the compute resource
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            include_capacity_metrics: Whether to include capacity metrics
            
        Returns:
            ComputeMetrics object
        """
        async with self._error_handler("get_compute_metrics", resource_id):
            resource_type = self._get_resource_type(resource_id)
            
            if resource_type == ComputeResourceType.VIRTUAL_MACHINE:
                client = self.vm_metrics_client
            elif resource_type == ComputeResourceType.APP_SERVICE:
                client = self.app_service_metrics_client
            # Add more resource types as implemented
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
            
            return await self._retry_operation(
                client.get_compute_metrics,
                resource_id,
                time_range,
                aggregation,
                interval,
                include_capacity_metrics
            )
    
    async def list_all_compute_resources(self) -> Dict[str, List[Dict[str, Any]]]:
        """List all compute resources across all supported types.
        
        Returns:
            Dictionary with resource type as key and list of resources as value
        """
        self._validate_subscription()
        results = {
            'virtual_machines': [],
            'app_services': [],
            # Add more resource types as implemented
        }
        
        # Collect all resources concurrently
        tasks = []
        
        async def collect_vms():
            async with self._error_handler("list_virtual_machines"):
                results['virtual_machines'] = await self._retry_operation(
                    self.vm_metrics_client.list_resources
                )
        
        async def collect_app_services():
            async with self._error_handler("list_app_services"):
                results['app_services'] = await self._retry_operation(
                    self.app_service_metrics_client.list_resources
                )
        
        tasks = [collect_vms(), collect_app_services()]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    async def get_all_compute_metrics(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None,
        resource_types: Optional[List[str]] = None,
        resource_filter: Optional[Dict[str, Any]] = None
    ) -> List[ComputeMetrics]:
        """Get metrics for all compute resources in the subscription.
        
        Args:
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            resource_types: Optional list of resource types to include
            resource_filter: Optional filter criteria (tags, resource groups, etc.)
            
        Returns:
            List of ComputeMetrics objects
        """
        if not resource_types:
            resource_types = ['virtual_machines', 'app_services']
        
        # First, list all resources
        all_resources = await self.list_all_compute_resources()
        
        # Apply filters if provided
        filtered_resources = []
        for resource_type, resources in all_resources.items():
            if resource_type not in resource_types:
                continue
            
            for resource in resources:
                # Apply resource filter
                if resource_filter:
                    # Filter by resource group
                    if 'resource_groups' in resource_filter:
                        if resource.get('resource_group') not in resource_filter['resource_groups']:
                            continue
                    
                    # Filter by tags
                    if 'tags' in resource_filter:
                        resource_tags = resource.get('tags', {})
                        if not all(
                            resource_tags.get(k) == v 
                            for k, v in resource_filter['tags'].items()
                        ):
                            continue
                    
                    # Filter by location
                    if 'locations' in resource_filter:
                        if resource.get('location') not in resource_filter['locations']:
                            continue
                
                filtered_resources.append(resource)
        
        # Collect metrics for all filtered resources
        metrics_tasks = []
        for resource in filtered_resources:
            resource_id = resource.get('id')
            if resource_id:
                task = self.get_compute_metrics(
                    resource_id,
                    time_range,
                    aggregation,
                    interval
                )
                metrics_tasks.append(task)
        
        # Gather all metrics concurrently with rate limiting
        results = await asyncio.gather(*metrics_tasks, return_exceptions=True)
        
        # Filter out exceptions and return successful results
        metrics = []
        for result in results:
            if isinstance(result, ComputeMetrics):
                metrics.append(result)
            elif isinstance(result, Exception):
                logger.warning(f"Failed to get metrics for a resource: {str(result)}")
        
        return metrics
    
    async def get_optimization_recommendations(
        self,
        resource_id: Optional[str] = None,
        metrics: Optional[Union[ComputeMetrics, List[ComputeMetrics]]] = None,
        include_all: bool = False,
        recommendation_types: Optional[List[str]] = None
    ) -> Union[List[ComputeRecommendation], Dict[str, List[ComputeRecommendation]]]:
        """Get optimization recommendations for compute resources.
        
        Args:
            resource_id: Optional specific resource ID
            metrics: Optional pre-collected metrics
            include_all: If True, analyze all resources in subscription
            recommendation_types: Optional list of recommendation types to include
            
        Returns:
            List of recommendations for single resource or dict for multiple
        """
        if include_all or (not resource_id and not metrics):
            # Get recommendations for all resources
            all_metrics = await self.get_all_compute_metrics()
            all_recommendations = {}
            
            for metric in all_metrics:
                resource_type = self._get_resource_type(metric.resource_id)
                
                if resource_type == ComputeResourceType.VIRTUAL_MACHINE:
                    client = self.vm_metrics_client
                elif resource_type == ComputeResourceType.APP_SERVICE:
                    client = self.app_service_metrics_client
                else:
                    continue
                
                try:
                    recommendations = await client.get_recommendations(
                        metric.resource_id,
                        metric
                    )
                    
                    # Filter by recommendation types if specified
                    if recommendation_types:
                        recommendations = [
                            r for r in recommendations
                            if r.recommendation_type in recommendation_types
                        ]
                    
                    if recommendations:
                        all_recommendations[metric.resource_name] = recommendations
                        
                except Exception as e:
                    logger.warning(f"Failed to get recommendations for {metric.resource_name}: {str(e)}")
            
            return all_recommendations
        
        elif resource_id:
            # Get recommendations for specific resource
            async with self._error_handler("get_recommendations", resource_id):
                resource_type = self._get_resource_type(resource_id)
                
                if resource_type == ComputeResourceType.VIRTUAL_MACHINE:
                    client = self.vm_metrics_client
                elif resource_type == ComputeResourceType.APP_SERVICE:
                    client = self.app_service_metrics_client
                else:
                    raise ValueError(f"Unsupported resource type: {resource_type}")
                
                recommendations = await self._retry_operation(
                    client.get_recommendations,
                    resource_id,
                    metrics
                )
                
                # Filter by recommendation types if specified
                if recommendation_types:
                    recommendations = [
                        r for r in recommendations
                        if r.recommendation_type in recommendation_types
                    ]
                
                return recommendations
        
        else:
            raise ValueError("Either resource_id or include_all must be specified")
    
    async def get_cost_optimization_summary(self) -> Dict[str, Any]:
        """Get a summary of cost optimization opportunities across all compute resources.
        
        Returns:
            Dictionary with cost optimization summary
        """
        all_recommendations = await self.get_optimization_recommendations(
            include_all=True,
            recommendation_types=['resize', 'shutdown', 'reserved_instance']
        )
        
        summary = {
            'total_resources_analyzed': 0,
            'resources_with_recommendations': len(all_recommendations),
            'total_recommendations': 0,
            'estimated_monthly_savings': 0.0,
            'estimated_annual_savings': 0.0,
            'recommendations_by_type': {},
            'recommendations_by_severity': {'high': 0, 'medium': 0, 'low': 0},
            'top_opportunities': []
        }
        
        all_opportunities = []
        
        for resource_name, recommendations in all_recommendations.items():
            summary['total_recommendations'] += len(recommendations)
            
            for rec in recommendations:
                # Count by type
                rec_type = rec.recommendation_type
                summary['recommendations_by_type'][rec_type] = \
                    summary['recommendations_by_type'].get(rec_type, 0) + 1
                
                # Count by severity
                summary['recommendations_by_severity'][rec.severity] += 1
                
                # Sum savings
                if rec.estimated_monthly_savings:
                    summary['estimated_monthly_savings'] += rec.estimated_monthly_savings
                if rec.estimated_annual_savings:
                    summary['estimated_annual_savings'] += rec.estimated_annual_savings
                
                # Collect opportunities for sorting
                if rec.estimated_annual_savings:
                    all_opportunities.append({
                        'resource_name': resource_name,
                        'recommendation': rec.description,
                        'annual_savings': rec.estimated_annual_savings,
                        'severity': rec.severity
                    })
        
        # Get top opportunities by savings
        all_opportunities.sort(key=lambda x: x['annual_savings'], reverse=True)
        summary['top_opportunities'] = all_opportunities[:10]
        
        # Add resource type breakdown
        all_metrics = await self.get_all_compute_metrics()
        summary['total_resources_analyzed'] = len(all_metrics)
        
        resource_type_counts = {}
        for metric in all_metrics:
            type_name = metric.resource_type.value
            resource_type_counts[type_name] = resource_type_counts.get(type_name, 0) + 1
        
        summary['resources_by_type'] = resource_type_counts
        
        return summary
    
    async def close(self):
        """Close all client connections."""
        # Azure SDK clients handle connection cleanup automatically
        logger.info("Closed Azure compute metrics wrapper")