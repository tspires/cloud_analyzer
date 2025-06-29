"""Azure Virtual Machines metrics collection implementation."""
import logging
from datetime import datetime, timedelta
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


class VirtualMachineMetricsClient(AzureComputeMetricsClient):
    """Client for collecting Azure Virtual Machine metrics."""
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        monitor_client: Optional[MonitorManagementClient] = None,
        compute_client: Optional[ComputeManagementClient] = None
    ):
        """Initialize Virtual Machine metrics client.
        
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
        """Get utilization metrics for an Azure Virtual Machine.
        
        Args:
            resource_id: Azure resource ID of the VM
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
        vm_name = resource_info['resource_name']
        resource_group = resource_info['resource_group']
        
        # Get VM details
        try:
            vm = self.compute_client.virtual_machines.get(
                resource_group_name=resource_group,
                vm_name=vm_name,
                expand='instanceView'
            )
        except Exception as e:
            logger.error(f"Failed to get VM details: {str(e)}")
            vm = None
        
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
        
        # Fetch all metrics in one call
        try:
            metrics_data = await self._fetch_multiple_metrics(
                resource_id,
                metric_names,
                time_range,
                aggregation,
                interval
            )
        except AzureError as e:
            logger.error(f"Failed to fetch metrics for VM {vm_name}: {str(e)}")
            raise
        
        # Calculate memory percentage if VM size info is available
        memory_percent_avg = None
        memory_percent_max = None
        memory_percent_p95 = None
        
        if vm and vm.hardware_profile and vm.hardware_profile.vm_size:
            # Get VM size memory (simplified - in production use size API)
            vm_memory_gb = self._get_vm_memory_gb(vm.hardware_profile.vm_size)
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
            resource_name=vm_name,
            resource_type=ComputeResourceType.VIRTUAL_MACHINE,
            resource_group=resource_group,
            location=vm.location if vm else "unknown",
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
            tags=dict(vm.tags) if vm and vm.tags else {},
            state=self._get_vm_power_state(vm) if vm else "unknown"
        )
        
        # Add VM-specific information
        if vm:
            metrics.sku = {
                "size": vm.hardware_profile.vm_size if vm.hardware_profile else None,
                "tier": "Standard",  # Can be enhanced with actual tier detection
            }
            
            # Add availability information
            if vm.instance_view and vm.instance_view.statuses:
                for status in vm.instance_view.statuses:
                    if status.code and "ProvisioningState" in status.code:
                        metrics.additional_metrics["provisioning_state"] = status.display_status
                    elif status.code and "PowerState" in status.code:
                        metrics.additional_metrics["power_state"] = status.display_status
            
            # OS information
            if vm.storage_profile:
                if vm.storage_profile.os_disk:
                    metrics.additional_metrics["os_type"] = vm.storage_profile.os_disk.os_type
                    metrics.additional_metrics["os_disk_size_gb"] = vm.storage_profile.os_disk.disk_size_gb
                
                if vm.storage_profile.data_disks:
                    metrics.additional_metrics["data_disk_count"] = len(vm.storage_profile.data_disks)
                    total_data_disk_size = sum(
                        disk.disk_size_gb for disk in vm.storage_profile.data_disks
                        if disk.disk_size_gb
                    )
                    metrics.additional_metrics["total_data_disk_size_gb"] = total_data_disk_size
        
        return metrics
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all Virtual Machines in the subscription.
        
        Returns:
            List of VM information dictionaries
        """
        vms = []
        
        try:
            vm_list = self.compute_client.virtual_machines.list_all()
            
            for vm in vm_list:
                vm_info = {
                    'id': vm.id,
                    'name': vm.name,
                    'resource_group': vm.id.split('/')[4],
                    'location': vm.location,
                    'vm_size': vm.hardware_profile.vm_size if vm.hardware_profile else None,
                    'provisioning_state': vm.provisioning_state,
                    'vm_id': vm.vm_id,
                    'tags': dict(vm.tags) if vm.tags else {},
                    'zones': list(vm.zones) if vm.zones else [],
                    'os_type': None,
                    'os_disk_size_gb': None,
                    'data_disk_count': 0
                }
                
                # Add storage information
                if vm.storage_profile:
                    if vm.storage_profile.os_disk:
                        vm_info['os_type'] = vm.storage_profile.os_disk.os_type
                        vm_info['os_disk_size_gb'] = vm.storage_profile.os_disk.disk_size_gb
                    
                    if vm.storage_profile.data_disks:
                        vm_info['data_disk_count'] = len(vm.storage_profile.data_disks)
                
                # Add network interface count
                if vm.network_profile and vm.network_profile.network_interfaces:
                    vm_info['network_interface_count'] = len(vm.network_profile.network_interfaces)
                
                vms.append(vm_info)
        
        except AzureError as e:
            logger.error(f"Failed to list virtual machines: {str(e)}")
            raise
        
        return vms
    
    async def get_recommendations(
        self,
        resource_id: str,
        metrics: Optional[ComputeMetrics] = None,
        pricing_tier: Optional[str] = None
    ) -> List[ComputeRecommendation]:
        """Get optimization recommendations for a Virtual Machine.
        
        Args:
            resource_id: Azure resource ID of the VM
            metrics: Optional pre-collected metrics
            pricing_tier: Optional pricing tier for cost calculations
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        if not metrics:
            metrics = await self.get_compute_metrics(resource_id)
        
        # Parse resource info for detailed recommendations
        resource_info = self._parse_resource_id(resource_id)
        
        # Check for low CPU utilization
        if metrics.cpu_percent_avg < 10 and metrics.cpu_percent_max < 30:
            monthly_savings, annual_savings = self._estimate_cost_savings(
                metrics.sku.get('size', 'unknown') if metrics.sku else 'unknown',
                'smaller_size',
                ComputeResourceType.VIRTUAL_MACHINE
            )
            
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='resize',
                severity='high',
                description=f'VM has very low CPU utilization (avg: {metrics.cpu_percent_avg:.1f}%, max: {metrics.cpu_percent_max:.1f}%)',
                impact='cost',
                estimated_monthly_savings=monthly_savings,
                estimated_annual_savings=annual_savings,
                action_details={
                    'current_size': metrics.sku.get('size') if metrics.sku else 'unknown',
                    'recommended_action': 'Consider downsizing to a smaller VM size',
                    'alternative_action': 'Consider using Azure Spot VMs for non-critical workloads'
                }
            ))
        
        # Check for deallocated VMs
        if metrics.state and metrics.state.lower() in ['stopped', 'deallocated']:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='shutdown',
                severity='high',
                description='VM is currently deallocated but still incurring storage costs',
                impact='cost',
                action_details={
                    'recommendation': 'Delete the VM if no longer needed, or set up auto-shutdown schedules'
                }
            ))
        
        # Check for high memory utilization
        if metrics.memory_percent_avg and metrics.memory_percent_avg > 85:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='resize',
                severity='medium',
                description=f'VM has high memory utilization ({metrics.memory_percent_avg:.1f}%)',
                impact='performance',
                action_details={
                    'current_size': metrics.sku.get('size') if metrics.sku else 'unknown',
                    'recommendation': 'Consider upgrading to a memory-optimized VM size'
                }
            ))
        
        # Check for untagged resources
        if not metrics.tags:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='governance',
                severity='low',
                description='VM has no tags for cost allocation and management',
                impact='governance',
                action_details={
                    'recommendation': 'Add tags for environment, owner, project, and cost center'
                }
            ))
        
        # Check for VMs without availability zones
        if 'availability_zone' not in metrics.additional_metrics:
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='availability',
                severity='medium',
                description='VM is not deployed in an availability zone',
                impact='availability',
                action_details={
                    'recommendation': 'Consider redeploying to availability zones for higher SLA'
                }
            ))
        
        # Reserved instance recommendation for consistently running VMs
        if metrics.cpu_percent_avg > 20:  # Consistently used VM
            recommendations.append(ComputeRecommendation(
                resource_id=resource_id,
                resource_name=metrics.resource_name,
                recommendation_type='reserved_instance',
                severity='medium',
                description='VM appears to be consistently running',
                impact='cost',
                estimated_monthly_savings=monthly_savings * 0.4,  # Approximate 40% savings
                estimated_annual_savings=annual_savings * 0.4,
                action_details={
                    'recommendation': 'Consider purchasing Reserved Instances for up to 72% savings',
                    'commitment_options': ['1-year', '3-year']
                }
            ))
        
        return recommendations
    
    def _get_vm_power_state(self, vm) -> Optional[str]:
        """Extract power state from VM instance view.
        
        Args:
            vm: Virtual machine object
            
        Returns:
            Power state string or None
        """
        if not vm or not vm.instance_view or not vm.instance_view.statuses:
            return None
        
        for status in vm.instance_view.statuses:
            if status.code and "PowerState" in status.code:
                return status.code.split('/')[-1]
        
        return None
    
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