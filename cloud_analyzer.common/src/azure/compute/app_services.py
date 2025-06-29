"""Azure App Services metrics collection implementation."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.web import WebSiteManagementClient

from .base import (
    AzureComputeMetricsClient,
    ComputeMetrics,
    ComputeRecommendation,
    ComputeResourceType,
)


logger = logging.getLogger(__name__)


class AppServiceMetricsClient(AzureComputeMetricsClient):
    """Client for collecting Azure App Service metrics."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None,
        web_client: Optional[WebSiteManagementClient] = None
    ):
        """Initialize App Service metrics client.
        
        Args:
            credential: Azure credential for authentication
            subscription_id: Azure subscription ID
            monitor_client: Optional pre-configured monitor client
            web_client: Optional pre-configured web client
        """
        super().__init__(credential, subscription_id, monitor_client)
        self._web_client = web_client
    
    @property
    def web_client(self) -> WebSiteManagementClient:
        """Get or create the web management client."""
        if not self._web_client:
            self._web_client = WebSiteManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._web_client
    
    async def get_compute_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None,
        include_capacity_metrics: bool = True
    ) -> ComputeMetrics:
        """Get utilization metrics for an Azure App Service.
        
        Args:
            resource_id: Azure resource ID of the App Service
            time_range: Optional time range tuple (start, end)
            aggregation: Metric aggregation type
            interval: Optional time grain interval
            include_capacity_metrics: Whether to include capacity metrics
            
        Returns:
            ComputeMetrics object containing utilization data
        """
        if not time_range:
            time_range = self._get_default_time_range()
        
        # Parse resource information
        resource_info = self._parse_resource_id(resource_id)
        site_name = resource_info['resource_name']
        resource_group = resource_info['resource_group']
        
        # Get App Service details
        try:
            site = self.web_client.web_apps.get(
                resource_group_name=resource_group,
                name=site_name
            )
        except Exception as e:
            logger.error(f"Failed to get App Service details: {str(e)}")
            site = None
        
        # Define metrics to collect
        metric_names = [
            "CpuPercentage",
            "MemoryPercentage",
            "BytesReceived",
            "BytesSent",
            "Http2xx",
            "Http3xx",
            "Http4xx",
            "Http5xx",
            "HttpResponseTime",
            "Requests",
            "AverageResponseTime"
        ]
        
        # Add App Service Plan metrics if needed
        if include_capacity_metrics and site and site.server_farm_id:
            plan_metric_names = [
                "CpuPercentage",
                "MemoryPercentage",
                "DiskQueueLength",
                "HttpQueueLength"
            ]
            # Note: These would be fetched from the App Service Plan resource
        
        # Fetch all metrics
        try:
            metrics_data = await self._fetch_multiple_metrics(
                resource_id,
                metric_names,
                time_range,
                aggregation,
                interval
            )
        except AzureError as e:
            logger.error(f"Failed to fetch metrics for App Service {site_name}: {str(e)}")
            raise
        
        # Calculate total requests and errors
        total_requests = sum([
            metrics_data.get("Http2xx", {}).get("total", 0),
            metrics_data.get("Http3xx", {}).get("total", 0),
            metrics_data.get("Http4xx", {}).get("total", 0),
            metrics_data.get("Http5xx", {}).get("total", 0)
        ])
        
        total_errors = sum([
            metrics_data.get("Http4xx", {}).get("total", 0),
            metrics_data.get("Http5xx", {}).get("total", 0)
        ])
        
        # Build ComputeMetrics object
        metrics = ComputeMetrics(
            resource_id=resource_id,
            resource_name=site_name,
            resource_type=ComputeResourceType.APP_SERVICE,
            resource_group=resource_group,
            location=site.location if site else "unknown",
            time_range=time_range,
            cpu_percent_avg=metrics_data.get("CpuPercentage", {}).get("avg", 0.0),
            cpu_percent_max=metrics_data.get("CpuPercentage", {}).get("max", 0.0),
            cpu_percent_p95=metrics_data.get("CpuPercentage", {}).get("p95"),
            memory_percent_avg=metrics_data.get("MemoryPercentage", {}).get("avg", 0.0),
            memory_percent_max=metrics_data.get("MemoryPercentage", {}).get("max", 0.0),
            memory_percent_p95=metrics_data.get("MemoryPercentage", {}).get("p95"),
            network_in_bytes_total=metrics_data.get("BytesReceived", {}).get("total", 0.0),
            network_out_bytes_total=metrics_data.get("BytesSent", {}).get("total", 0.0),
            request_count=int(total_requests),
            error_count=int(total_errors),
            response_time_avg=metrics_data.get("AverageResponseTime", {}).get("avg", 0.0),
            tags=dict(site.tags) if site and site.tags else {},
            state=site.state if site else "unknown"
        )
        
        # Add App Service specific information
        if site:
            metrics.sku = {
                "tier": site.sku.tier if site.sku else None,
                "size": site.sku.size if site.sku else None,
                "family": site.sku.family if site.sku else None,
                "capacity": site.sku.capacity if site.sku else None
            }
            
            metrics.additional_metrics.update({
                "enabled": site.enabled,
                "availability_state": site.availability_state,
                "host_names": list(site.host_names) if site.host_names else [],
                "outbound_ip_addresses": site.outbound_ip_addresses,
                "default_host_name": site.default_host_name,
                "kind": site.kind,  # e.g., 'app', 'functionapp', 'app,linux'
                "reserved": site.reserved,  # True for Linux
                "https_only": site.https_only,
                "client_cert_enabled": site.client_cert_enabled
            })
            
            # Add HTTP status code breakdown
            metrics.additional_metrics.update({
                "http_2xx_count": int(metrics_data.get("Http2xx", {}).get("total", 0)),
                "http_3xx_count": int(metrics_data.get("Http3xx", {}).get("total", 0)),
                "http_4xx_count": int(metrics_data.get("Http4xx", {}).get("total", 0)),
                "http_5xx_count": int(metrics_data.get("Http5xx", {}).get("total", 0)),
                "http_response_time_avg": metrics_data.get("HttpResponseTime", {}).get("avg", 0.0),
                "http_response_time_max": metrics_data.get("HttpResponseTime", {}).get("max", 0.0)
            })
            
            # Add App Service Plan info if available
            if site.server_farm_id:
                metrics.additional_metrics["app_service_plan_id"] = site.server_farm_id
                metrics.additional_metrics["app_service_plan_name"] = site.server_farm_id.split('/')[-1]
        
        return metrics
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all App Services in the subscription.
        
        Returns:
            List of App Service information dictionaries
        """
        apps = []
        
        try:
            app_list = self.web_client.web_apps.list()
            
            for app in app_list:
                app_info = {
                    'id': app.id,
                    'name': app.name,
                    'resource_group': app.id.split('/')[4],
                    'location': app.location,
                    'kind': app.kind,
                    'state': app.state,
                    'enabled': app.enabled,
                    'availability_state': app.availability_state,
                    'default_host_name': app.default_host_name,
                    'tags': dict(app.tags) if app.tags else {},
                    'sku_tier': app.sku.tier if app.sku else None,
                    'sku_size': app.sku.size if app.sku else None,
                    'server_farm_id': app.server_farm_id,
                    'reserved': app.reserved,  # Linux
                    'https_only': app.https_only,
                    'site_config': {
                        'always_on': app.site_config.always_on if app.site_config else None,
                        'http20_enabled': app.site_config.http20_enabled if app.site_config else None,
                        'min_tls_version': app.site_config.min_tls_version if app.site_config else None,
                        'ftps_state': app.site_config.ftps_state if app.site_config else None
                    }
                }
                
                apps.append(app_info)
        
        except AzureError as e:
            logger.error(f"Failed to list App Services: {str(e)}")
            raise
        
        return apps
    
    async def get_recommendations(
        self,
        resource_id: str,
        metrics: Optional[ComputeMetrics] = None,
        pricing_tier: Optional[str] = None
    ) -> List[ComputeRecommendation]:
        """Get optimization recommendations for an App Service.
        
        Args:
            resource_id: Azure resource ID of the App Service
            metrics: Optional pre-collected metrics
            pricing_tier: Optional pricing tier for cost calculations
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        if not metrics:
            metrics = await self.get_compute_metrics(resource_id)
        
        # Check for low CPU utilization
        if metrics.cpu_percent_avg < 10 and metrics.cpu_percent_max < 30:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='resize',
                severity='high',
                description=f'App Service has low CPU utilization (avg: {metrics.cpu_percent_avg:.1f}%, max: {metrics.cpu_percent_max:.1f}%)',
                impact='cost',
                action_details={
                    'current_tier': metrics.sku.get('tier') if metrics.sku else 'unknown',
                    'recommendation': 'Consider scaling down to a lower pricing tier or using consumption-based Azure Functions'
                }
            ))
        
        # Check for high response times
        if metrics.response_time_avg and metrics.response_time_avg > 1000:  # > 1 second
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='performance',
                severity='high',
                description=f'High average response time ({metrics.response_time_avg:.0f}ms)',
                impact='performance',
                action_details={
                    'recommendation': 'Enable Application Insights for detailed diagnostics',
                    'suggestions': [
                        'Review application code for performance issues',
                        'Enable autoscaling',
                        'Consider using Azure CDN for static content'
                    ]
                }
            ))
        
        # Check for high error rates
        if metrics.request_count and metrics.error_count:
            error_rate = (metrics.error_count / metrics.request_count) * 100
            if error_rate > 5:
                recommendations.append(ComputeRecommendation(
                    resource_id=resource_id,
                    resource_name=metrics.resource_name,
                    recommendation_type='reliability',
                    severity='high',
                    description=f'High error rate ({error_rate:.1f}%)',
                    impact='availability',
                    action_details={
                        'http_4xx_errors': metrics.additional_metrics.get('http_4xx_count', 0),
                        'http_5xx_errors': metrics.additional_metrics.get('http_5xx_count', 0),
                        'recommendation': 'Review application logs and enable detailed error tracking'
                    }
                ))
        
        # Check for always-on setting
        if metrics.additional_metrics.get('kind') != 'functionapp':
            always_on = metrics.additional_metrics.get('always_on', False)
            if not always_on and metrics.sku and metrics.sku.get('tier') not in ['Free', 'Shared']:
                recommendations.append(ComputeRecommendation(
                    resource_id=resource_id,
                    resource_name=metrics.resource_name,
                    recommendation_type='performance',
                    severity='medium',
                    description='Always On is not enabled',
                    impact='performance',
                    action_details={
                        'recommendation': 'Enable Always On to prevent cold starts and improve response times'
                    }
                ))
        
        # Check for HTTPS enforcement
        if not metrics.additional_metrics.get('https_only', False):
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='security',
                severity='high',
                description='HTTPS Only is not enforced',
                impact='security',
                action_details={
                    'recommendation': 'Enable HTTPS Only to ensure all traffic is encrypted'
                }
            ))
        
        # Check for autoscaling
        if metrics.sku and metrics.sku.get('tier') in ['Standard', 'Premium']:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='scalability',
                severity='medium',
                description='Consider enabling autoscaling',
                impact='cost',
                action_details={
                    'recommendation': 'Configure autoscaling rules based on CPU, memory, or request metrics',
                    'benefits': ['Cost optimization', 'Automatic handling of traffic spikes']
                }
            ))
        
        # Check for staging slots in production apps
        if metrics.sku and metrics.sku.get('tier') in ['Standard', 'Premium', 'Isolated']:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='deployment',
                severity='low',
                description='Consider using deployment slots',
                impact='availability',
                action_details={
                    'recommendation': 'Use deployment slots for zero-downtime deployments and testing'
                }
            ))
        
        return recommendations