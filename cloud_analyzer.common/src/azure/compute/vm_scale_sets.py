"""Azure VM Scale Sets metrics collection implementation."""
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from azure.core.credentials import TokenCredential
from azure.core.exceptions import AzureError
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.monitor import MonitorManagementClient

from .base import (
    AzureComputeMetricsClient,
    ComputeMetrics,
    ComputeRecommendation,
    ComputeResourceType,
)


logger = logging.getLogger(__name__)


class VMScaleSetMetricsClient(AzureComputeMetricsClient):
    """Client for collecting Azure VM Scale Set metrics."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None,
        compute_client: Optional[ComputeManagementClient] = None
    ):
        """Initialize VM Scale Set metrics client.
        
        Args:
            credential: Azure credential for authentication
            subscription_id: Azure subscription ID
            monitor_client: Optional pre-configured monitor client
            compute_client: Optional pre-configured compute client
        """
        super().__init__(credential, subscription_id, monitor_client)
        self._compute_client = compute_client
    
    @property
    def compute_client(self) -> ComputeManagementClient:
        """Get or create the compute management client."""
        if not self._compute_client:
            self._compute_client = ComputeManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
        return self._compute_client
    
    async def get_compute_metrics(
        self,
        resource_id: str,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        aggregation: str = "Average",
        interval: Optional[timedelta] = None,
        include_capacity_metrics: bool = True
    ) -> ComputeMetrics:
        """Get utilization metrics for an Azure VM Scale Set.
        
        Args:
            resource_id: Azure resource ID of the VMSS
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
        vmss_name = resource_info['resource_name']
        resource_group = resource_info['resource_group']
        
        # Get VMSS details
        try:
            vmss = self.compute_client.virtual_machine_scale_sets.get(
                resource_group_name=resource_group,
                vm_scale_set_name=vmss_name
            )
        except Exception as e:
            logger.error(f"Failed to get VMSS details: {str(e)}")
            vmss = None
        
        # Define metrics to collect
        metric_names = [
            "Percentage CPU",
            "Available Memory Bytes",
            "Network In Total",
            "Network Out Total",
            "Disk Read Bytes",
            "Disk Write Bytes",
            "Disk Read Operations/Sec",
            "Disk Write Operations/Sec"
        ]
        
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
            logger.error(f"Failed to fetch metrics for VMSS {vmss_name}: {str(e)}")
            raise
        
        # Get instance count and capacity info
        instance_count = 0
        if include_capacity_metrics and vmss:
            try:
                instances = self.compute_client.virtual_machine_scale_set_vms.list(
                    resource_group_name=resource_group,
                    virtual_machine_scale_set_name=vmss_name
                )
                instance_count = sum(1 for _ in instances)
            except Exception as e:
                logger.warning(f"Failed to get instance count: {str(e)}")
        
        # Calculate memory percentage if SKU info is available
        memory_percent_avg = None
        memory_percent_max = None
        memory_percent_p95 = None
        
        if vmss and vmss.sku:
            # Get VM size memory (simplified - in production use size API)
            vm_memory_gb = self._get_vm_memory_gb(vmss.sku.name)
            if vm_memory_gb and "Available Memory Bytes" in metrics_data:
                memory_data = metrics_data["Available Memory Bytes"]
                total_memory_bytes = vm_memory_gb * 1024 * 1024 * 1024
                
                # Calculate used memory percentage
                if memory_data["avg"] > 0:
                    used_memory_avg = total_memory_bytes - memory_data["avg"]
                    memory_percent_avg = (used_memory_avg / total_memory_bytes) * 100
                
                if memory_data["min"] > 0:
                    used_memory_max = total_memory_bytes - memory_data["min"]
                    memory_percent_max = (used_memory_max / total_memory_bytes) * 100
                
                if "p95" in memory_data and memory_data["p95"] > 0:
                    used_memory_p95 = total_memory_bytes - memory_data["p95"]
                    memory_percent_p95 = (used_memory_p95 / total_memory_bytes) * 100
        
        # Build ComputeMetrics object
        metrics = ComputeMetrics(
            resource_id=resource_id,
            resource_name=vmss_name,
            resource_type=ComputeResourceType.VM_SCALE_SET,
            resource_group=resource_group,
            location=vmss.location if vmss else "unknown",
            time_range=time_range,
            cpu_percent_avg=metrics_data.get("Percentage CPU", {}).get("avg", 0.0),
            cpu_percent_max=metrics_data.get("Percentage CPU", {}).get("max", 0.0),
            cpu_percent_p95=metrics_data.get("Percentage CPU", {}).get("p95"),
            memory_percent_avg=memory_percent_avg,
            memory_percent_max=memory_percent_max,
            memory_percent_p95=memory_percent_p95,
            network_in_bytes_total=metrics_data.get("Network In Total", {}).get("total", 0.0),
            network_out_bytes_total=metrics_data.get("Network Out Total", {}).get("total", 0.0),
            disk_read_bytes_total=metrics_data.get("Disk Read Bytes", {}).get("total", 0.0),
            disk_write_bytes_total=metrics_data.get("Disk Write Bytes", {}).get("total", 0.0),
            disk_read_ops_total=metrics_data.get("Disk Read Operations/Sec", {}).get("total", 0.0),
            disk_write_ops_total=metrics_data.get("Disk Write Operations/Sec", {}).get("total", 0.0),
            instance_count=instance_count,
            tags=dict(vmss.tags) if vmss and vmss.tags else {},
            state="running" if vmss else "unknown"
        )
        
        # Add VMSS-specific information
        if vmss:
            metrics.sku = {
                "name": vmss.sku.name if vmss.sku else None,
                "tier": vmss.sku.tier if vmss.sku else None,
                "capacity": vmss.sku.capacity if vmss.sku else None
            }
            
            metrics.additional_metrics.update({
                "overprovision": vmss.overprovision,
                "unique_id": vmss.unique_id,
                "platform_fault_domain_count": vmss.platform_fault_domain_count,
                "single_placement_group": vmss.single_placement_group,
                "zone_balance": vmss.zone_balance if hasattr(vmss, 'zone_balance') else None,
                "provisioning_state": vmss.provisioning_state
            })
            
            # Add upgrade policy info
            if vmss.upgrade_policy:
                metrics.additional_metrics["upgrade_mode"] = vmss.upgrade_policy.mode
                
            # Add auto-scale info if available
            if vmss.sku and vmss.sku.capacity:
                metrics.additional_metrics["current_capacity"] = vmss.sku.capacity
        
        return metrics
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all VM Scale Sets in the subscription.
        
        Returns:
            List of VMSS information dictionaries
        """
        vmss_list = []
        
        try:
            scale_sets = self.compute_client.virtual_machine_scale_sets.list_all()
            
            for vmss in scale_sets:
                vmss_info = {
                    'id': vmss.id,
                    'name': vmss.name,
                    'resource_group': vmss.id.split('/')[4],
                    'location': vmss.location,
                    'sku_name': vmss.sku.name if vmss.sku else None,
                    'sku_tier': vmss.sku.tier if vmss.sku else None,
                    'capacity': vmss.sku.capacity if vmss.sku else 0,
                    'provisioning_state': vmss.provisioning_state,
                    'unique_id': vmss.unique_id,
                    'tags': dict(vmss.tags) if vmss.tags else {},
                    'zones': list(vmss.zones) if vmss.zones else [],
                    'overprovision': vmss.overprovision,
                    'upgrade_mode': vmss.upgrade_policy.mode if vmss.upgrade_policy else None
                }
                
                vmss_list.append(vmss_info)
        
        except AzureError as e:
            logger.error(f"Failed to list VM Scale Sets: {str(e)}")
            raise
        
        return vmss_list
    
    async def get_recommendations(
        self,
        resource_id: str,
        metrics: Optional[ComputeMetrics] = None,
        pricing_tier: Optional[str] = None
    ) -> List[ComputeRecommendation]:
        """Get optimization recommendations for a VM Scale Set.
        
        Args:
            resource_id: Azure resource ID of the VMSS
            metrics: Optional pre-collected metrics
            pricing_tier: Optional pricing tier for cost calculations
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        if not metrics:
            metrics = await self.get_compute_metrics(resource_id)
        
        # Check for low CPU utilization
        if metrics.cpu_percent_avg < 20 and metrics.cpu_percent_max < 40:
            monthly_savings, annual_savings = self._estimate_cost_savings(
                metrics.sku.get('name', 'unknown') if metrics.sku else 'unknown',
                'smaller_size',
                ComputeResourceType.VM_SCALE_SET
            )
            
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='resize',
                severity='high',
                description=f'VMSS has low CPU utilization (avg: {metrics.cpu_percent_avg:.1f}%, max: {metrics.cpu_percent_max:.1f}%)',
                impact='cost',
                estimated_monthly_savings=monthly_savings * (metrics.instance_count or 1),
                estimated_annual_savings=annual_savings * (metrics.instance_count or 1),
                action_details={
                    'current_size': metrics.sku.get('name') if metrics.sku else 'unknown',
                    'current_instances': metrics.instance_count,
                    'recommendation': 'Consider using a smaller VM size or reducing instance count'
                }
            ))
        
        # Check for over-provisioning with low usage
        if metrics.instance_count and metrics.instance_count > 2:
            if metrics.cpu_percent_avg < 30 and metrics.memory_percent_avg and metrics.memory_percent_avg < 30:
                recommendations.append(ComputeRecommendation(
                    resource_id=resource_id,
                    resource_name=metrics.resource_name,
                    recommendation_type='scale',
                    severity='medium',
                    description=f'VMSS may be over-provisioned with {metrics.instance_count} instances at low utilization',
                    impact='cost',
                    action_details={
                        'current_instances': metrics.instance_count,
                        'recommendation': 'Review auto-scale rules to reduce minimum instance count'
                    }
                ))
        
        # Check for high memory utilization
        if metrics.memory_percent_avg and metrics.memory_percent_avg > 85:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='resize',
                severity='high',
                description=f'VMSS has high memory utilization ({metrics.memory_percent_avg:.1f}%)',
                impact='performance',
                action_details={
                    'current_size': metrics.sku.get('name') if metrics.sku else 'unknown',
                    'recommendation': 'Consider upgrading to a memory-optimized VM size'
                }
            ))
        
        # Check for single placement group limitations
        if metrics.additional_metrics.get('single_placement_group') and metrics.instance_count and metrics.instance_count > 80:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='architecture',
                severity='medium',
                description='VMSS approaching single placement group limit (100 instances)',
                impact='scalability',
                action_details={
                    'recommendation': 'Consider disabling single placement group for larger scale'
                }
            ))
        
        # Check for availability zones
        if not metrics.additional_metrics.get('zone_balance'):
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='availability',
                severity='medium',
                description='VMSS not using availability zones',
                impact='availability',
                action_details={
                    'recommendation': 'Deploy across availability zones for higher availability'
                }
            ))
        
        # Check upgrade policy
        upgrade_mode = metrics.additional_metrics.get('upgrade_mode')
        if upgrade_mode and upgrade_mode.lower() == 'manual':
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='maintenance',
                severity='low',
                description='VMSS using manual upgrade mode',
                impact='maintenance',
                action_details={
                    'current_mode': upgrade_mode,
                    'recommendation': 'Consider automatic or rolling upgrade mode for easier maintenance'
                }
            ))
        
        return recommendations
    
    def _get_vm_memory_gb(self, vm_size: str) -> Optional[int]:
        """Get VM memory in GB based on size.
        
        Args:
            vm_size: VM size string
            
        Returns:
            Memory in GB or None
        """
        # Simplified mapping - in production use Azure VM sizes API
        size_memory_map = {
            # General purpose
            "Standard_B1s": 1,
            "Standard_B1ms": 2,
            "Standard_B2s": 4,
            "Standard_B2ms": 8,
            "Standard_B4ms": 16,
            "Standard_B8ms": 32,
            # D-series
            "Standard_D2s_v3": 8,
            "Standard_D4s_v3": 16,
            "Standard_D8s_v3": 32,
            "Standard_D16s_v3": 64,
            "Standard_D32s_v3": 128,
            # E-series (memory optimized)
            "Standard_E2s_v3": 16,
            "Standard_E4s_v3": 32,
            "Standard_E8s_v3": 64,
            "Standard_E16s_v3": 128,
            # F-series (compute optimized)
            "Standard_F2s_v2": 4,
            "Standard_F4s_v2": 8,
            "Standard_F8s_v2": 16,
            "Standard_F16s_v2": 32,
        }
        
        return size_memory_map.get(vm_size)