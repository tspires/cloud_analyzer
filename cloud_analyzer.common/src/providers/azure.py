"""Azure cloud provider implementation."""

import logging
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional, Set

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.mgmt.reservations import AzureReservationAPI
from azure.core.exceptions import AzureError

from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface


class AzureProvider(CloudProviderInterface):
    """Azure cloud provider implementation."""
    
    def __init__(self, subscription_id: Optional[str] = None) -> None:
        """Initialize Azure provider.
        
        Args:
            subscription_id: Azure subscription ID. If not provided, will use 
                           AZURE_SUBSCRIPTION_ID environment variable.
        """
        self.logger = logging.getLogger(__name__)
        self._subscription_id = subscription_id
        self._credential = None
        self._compute_client = None
        self._resource_client = None
        self._storage_client = None
        self._sql_client = None
        self._monitor_client = None
        self._consumption_client = None
        self._reservations_client = None
    
    @property
    def provider(self) -> CloudProvider:
        """Return the cloud provider type."""
        return CloudProvider.AZURE
    
    async def initialize(self) -> None:
        """Initialize Azure clients."""
        import os
        
        # Get subscription ID from environment if not provided
        if not self._subscription_id:
            self._subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
            if not self._subscription_id:
                raise ValueError("Azure subscription ID not provided")
        
        # Initialize credential
        self._credential = DefaultAzureCredential()
        
        # Initialize clients
        self._compute_client = ComputeManagementClient(
            self._credential, self._subscription_id
        )
        self._resource_client = ResourceManagementClient(
            self._credential, self._subscription_id
        )
        self._storage_client = StorageManagementClient(
            self._credential, self._subscription_id
        )
        self._sql_client = SqlManagementClient(
            self._credential, self._subscription_id
        )
        self._monitor_client = MonitorManagementClient(
            self._credential, self._subscription_id
        )
        self._consumption_client = ConsumptionManagementClient(
            self._credential, self._subscription_id
        )
        self._reservations_client = AzureReservationAPI(
            self._credential
        )
    
    async def list_resources(
        self, 
        resource_types: Optional[Set[ResourceType]] = None,
        regions: Optional[Set[str]] = None
    ) -> List[Resource]:
        """List all resources in the Azure subscription."""
        resources = []
        
        try:
            # List VMs
            if not resource_types or ResourceType.INSTANCE in resource_types:
                for vm in self._compute_client.virtual_machines.list_all():
                    if regions and vm.location not in regions:
                        continue
                    
                    # Get VM size for pricing estimation
                    vm_size = vm.hardware_profile.vm_size
                    monthly_cost = self._estimate_vm_cost(vm_size, vm.location)
                    
                    resources.append(Resource(
                        id=vm.id,
                        name=vm.name,
                        type=ResourceType.INSTANCE,
                        provider=CloudProvider.AZURE,
                        region=vm.location,
                        state=vm.provisioning_state.lower(),
                        monthly_cost=monthly_cost,
                        is_active=vm.provisioning_state == "Succeeded",
                        tags=vm.tags or {},
                        metadata={
                            "vm_size": vm_size,
                            "os_type": vm.storage_profile.os_disk.os_type,
                        }
                    ))
            
            # List Managed Disks (Volumes)
            if not resource_types or ResourceType.VOLUME in resource_types:
                for disk in self._compute_client.disks.list():
                    if regions and disk.location not in regions:
                        continue
                    
                    monthly_cost = self._estimate_disk_cost(
                        disk.disk_size_gb, disk.sku.name, disk.location
                    )
                    
                    resources.append(Resource(
                        id=disk.id,
                        name=disk.name,
                        type=ResourceType.VOLUME,
                        provider=CloudProvider.AZURE,
                        region=disk.location,
                        state=disk.disk_state.lower() if disk.disk_state else "unknown",
                        monthly_cost=monthly_cost,
                        is_active=disk.disk_state == "Attached",
                        tags=disk.tags or {},
                        metadata={
                            "size_gb": disk.disk_size_gb,
                            "sku": disk.sku.name,
                            "managed_by": disk.managed_by,
                        }
                    ))
            
            # List Snapshots
            if not resource_types or ResourceType.SNAPSHOT in resource_types:
                for snapshot in self._compute_client.snapshots.list():
                    if regions and snapshot.location not in regions:
                        continue
                    
                    monthly_cost = self._estimate_snapshot_cost(
                        snapshot.disk_size_gb, snapshot.location
                    )
                    
                    resources.append(Resource(
                        id=snapshot.id,
                        name=snapshot.name,
                        type=ResourceType.SNAPSHOT,
                        provider=CloudProvider.AZURE,
                        region=snapshot.location,
                        state="completed",
                        monthly_cost=monthly_cost,
                        is_active=True,
                        created_at=snapshot.time_created,
                        tags=snapshot.tags or {},
                        metadata={
                            "size_gb": snapshot.disk_size_gb,
                            "source_disk_id": snapshot.creation_data.source_resource_id,
                        }
                    ))
            
            # List SQL Databases
            if not resource_types or ResourceType.DATABASE in resource_types:
                for server in self._sql_client.servers.list():
                    for db in self._sql_client.databases.list_by_server(
                        resource_group_name=server.id.split('/')[4],
                        server_name=server.name
                    ):
                        if regions and db.location not in regions:
                            continue
                        
                        if db.name == "master":  # Skip system database
                            continue
                        
                        monthly_cost = self._estimate_sql_database_cost(
                            db.sku.name, db.sku.tier, db.location
                        )
                        
                        resources.append(Resource(
                            id=db.id,
                            name=db.name,
                            type=ResourceType.DATABASE,
                            provider=CloudProvider.AZURE,
                            region=db.location,
                            state=db.status.lower() if db.status else "unknown",
                            monthly_cost=monthly_cost,
                            is_active=db.status == "Online",
                            tags=db.tags or {},
                            metadata={
                                "sku": db.sku.name,
                                "tier": db.sku.tier,
                                "max_size_gb": db.max_size_bytes / (1024**3) if db.max_size_bytes else 0,
                                "server_name": server.name,
                            }
                        ))
            
        except AzureError as e:
            self.logger.error(f"Error listing Azure resources: {str(e)}")
            raise
        
        return resources
    
    async def get_volume_info(self, volume_id: str, region: str) -> Dict[str, Any]:
        """Get detailed information about a volume (managed disk)."""
        try:
            # Extract resource group and disk name from volume ID
            parts = volume_id.split('/')
            resource_group = parts[4]
            disk_name = parts[-1]
            
            disk = self._compute_client.disks.get(resource_group, disk_name)
            
            # Check if disk is attached
            attached = disk.managed_by is not None
            detached_at = None
            
            if not attached:
                # Try to get detach time from activity logs
                detached_at = await self._get_disk_detach_time(resource_group, disk_name)
            
            return {
                "attached": attached,
                "detached_at": detached_at,
                "size_gb": disk.disk_size_gb,
                "sku": disk.sku.name,
                "encryption": disk.encryption is not None,
                "managed_by": disk.managed_by,
            }
        except Exception as e:
            self.logger.error(f"Error getting volume info for {volume_id}: {str(e)}")
            raise
    
    async def get_snapshot_info(self, snapshot_id: str, region: str) -> Dict[str, Any]:
        """Get detailed information about a snapshot."""
        try:
            # Extract resource group and snapshot name
            parts = snapshot_id.split('/')
            resource_group = parts[4]
            snapshot_name = parts[-1]
            
            snapshot = self._compute_client.snapshots.get(resource_group, snapshot_name)
            
            # Check if snapshot is from an image
            is_image_snapshot = False
            if snapshot.creation_data.image_reference:
                is_image_snapshot = True
            
            return {
                "created_at": snapshot.time_created,
                "size_gb": snapshot.disk_size_gb,
                "is_ami_snapshot": is_image_snapshot,  # Using AMI term for consistency
                "has_backup_policy": False,  # Would need to check backup policies
                "source_disk_id": snapshot.creation_data.source_resource_id,
                "incremental": snapshot.incremental,
            }
        except Exception as e:
            self.logger.error(f"Error getting snapshot info for {snapshot_id}: {str(e)}")
            raise
    
    async def get_database_metrics(
        self, database_id: str, region: str, days: int = 7
    ) -> Dict[str, Any]:
        """Get database performance metrics."""
        try:
            # Extract identifiers from database ID
            parts = database_id.split('/')
            resource_group = parts[4]
            server_name = parts[8]
            database_name = parts[10]
            
            # Define time range
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=days)
            
            # Define metrics to fetch
            metrics = {
                'cpu_percent': 'cpu_percent',
                'memory_percent': 'memory_percentage',
                'dtu_percent': 'dtu_consumption_percent',  # For DTU-based
            }
            
            results = {
                'avg_cpu_percent': 0,
                'avg_memory_percent': 0,
                'max_cpu_percent': 0,
                'max_memory_percent': 0,
            }
            
            for metric_key, metric_name in metrics.items():
                try:
                    # Format timespan correctly for Azure Monitor API
                    timespan = f"{start_time.strftime('%Y-%m-%dT%H:%M:%SZ')}/{end_time.strftime('%Y-%m-%dT%H:%M:%SZ')}"
                    
                    metric_data = self._monitor_client.metrics.list(
                        resource_uri=database_id,
                        timespan=timespan,
                        interval='PT1H',
                        metricnames=metric_name,
                        aggregation='Average,Maximum'
                    )
                    
                    # Process metric data
                    for metric in metric_data.value:
                        if metric.name.value == metric_name:
                            avg_values = []
                            max_values = []
                            
                            for timeseries in metric.timeseries:
                                for data in timeseries.data:
                                    if data.average is not None:
                                        avg_values.append(data.average)
                                    if data.maximum is not None:
                                        max_values.append(data.maximum)
                            
                            if 'cpu' in metric_key and avg_values:
                                results['avg_cpu_percent'] = sum(avg_values) / len(avg_values)
                                results['max_cpu_percent'] = max(max_values) if max_values else 0
                            elif 'memory' in metric_key and avg_values:
                                results['avg_memory_percent'] = sum(avg_values) / len(avg_values)
                                results['max_memory_percent'] = max(max_values) if max_values else 0
                            elif 'dtu' in metric_key and avg_values:
                                # Map DTU to CPU for DTU-based databases
                                results['avg_cpu_percent'] = sum(avg_values) / len(avg_values)
                                results['max_cpu_percent'] = max(max_values) if max_values else 0
                
                except Exception as e:
                    self.logger.warning(f"Failed to get metric {metric_name}: {str(e)}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error getting database metrics for {database_id}: {str(e)}")
            raise
    
    async def get_database_info(self, database_id: str, region: str) -> Dict[str, Any]:
        """Get database configuration information."""
        try:
            # Extract identifiers
            parts = database_id.split('/')
            resource_group = parts[4]
            server_name = parts[8]
            database_name = parts[10]
            
            db = self._sql_client.databases.get(resource_group, server_name, database_name)
            
            return {
                "instance_type": f"{db.sku.tier}_{db.sku.name}",
                "engine": "SQL Database",
                "engine_version": "12.0",  # Azure SQL is always latest
                "allocated_storage_gb": db.max_size_bytes / (1024**3) if db.max_size_bytes else 0,
                "multi_az": db.zone_redundant if hasattr(db, 'zone_redundant') else False,
                "storage_type": "Premium SSD",  # Azure SQL uses premium storage
            }
        except Exception as e:
            self.logger.error(f"Error getting database info for {database_id}: {str(e)}")
            raise
    
    async def get_database_sizing_recommendations(
        self, database_id: str, region: str, metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get database sizing recommendations based on metrics."""
        try:
            # Extract current configuration
            parts = database_id.split('/')
            resource_group = parts[4]
            server_name = parts[8]
            database_name = parts[10]
            
            db = self._sql_client.databases.get(resource_group, server_name, database_name)
            current_sku = db.sku
            
            recommendations = []
            
            # Define SKU downsizing options
            sku_downsize_map = {
                # General Purpose
                'GP_Gen5_8': ['GP_Gen5_4', 'GP_Gen5_2'],
                'GP_Gen5_4': ['GP_Gen5_2'],
                'GP_Gen5_16': ['GP_Gen5_8', 'GP_Gen5_4'],
                # Business Critical
                'BC_Gen5_8': ['BC_Gen5_4', 'BC_Gen5_2'],
                'BC_Gen5_4': ['BC_Gen5_2'],
                # DTU-based
                'P6': ['P4', 'P2', 'P1'],
                'P4': ['P2', 'P1'],
                'P2': ['P1'],
                'S7': ['S4', 'S3', 'S2'],
                'S4': ['S3', 'S2'],
                'S3': ['S2', 'S1'],
            }
            
            # Check if we can downsize based on metrics
            avg_cpu = metrics.get('avg_cpu_percent', 0)
            if avg_cpu < 40 and current_sku.name in sku_downsize_map:
                for smaller_sku in sku_downsize_map[current_sku.name]:
                    # Estimate cost for smaller SKU
                    new_cost = self._estimate_sql_database_cost(
                        smaller_sku, current_sku.tier, region
                    )
                    current_cost = self._estimate_sql_database_cost(
                        current_sku.name, current_sku.tier, region
                    )
                    
                    if new_cost < current_cost:
                        recommendations.append({
                            "instance_type": f"{current_sku.tier}_{smaller_sku}",
                            "monthly_cost": float(new_cost),
                            "cpu_baseline": self._get_sku_cpu_baseline(smaller_sku),
                            "memory_gb": self._get_sku_memory_gb(smaller_sku),
                            "reason": f"Current CPU usage ({avg_cpu:.1f}%) allows downsizing"
                        })
                        break  # Only recommend one size down
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting sizing recommendations for {database_id}: {str(e)}")
            return []
    
    async def get_reserved_instances_utilization(
        self, region: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get reserved instances utilization data."""
        try:
            underutilized = []
            
            # List all reservations
            reservations = self._reservations_client.reservation.list_all()
            
            for reservation in reservations:
                if reservation.properties.provisioning_state == "Succeeded":
                    # Get utilization data
                    utilization = self._reservations_client.reservation_utilization.list(
                        reservation_order_id=reservation.properties.reservation_order_id,
                        reservation_id=reservation.name,
                        filter="properties/usageDate ge 2024-01-01"
                    )
                    
                    # Calculate average utilization
                    total_util = 0
                    count = 0
                    for util_record in utilization:
                        if util_record.properties.utilization_percentage:
                            total_util += util_record.properties.utilization_percentage
                            count += 1
                    
                    avg_utilization = total_util / count if count > 0 else 0
                    
                    # Check if underutilized
                    if avg_utilization < 80:
                        # Get reservation details
                        sku_name = reservation.sku.name
                        location = reservation.location
                        
                        if region and location != region:
                            continue
                        
                        # Estimate monthly cost (simplified)
                        monthly_cost = self._estimate_reservation_cost(
                            sku_name, location, reservation.properties.term
                        )
                        
                        underutilized.append({
                            "reservation_id": reservation.name,
                            "instance_type": sku_name,
                            "region": location,
                            "utilization_percentage": avg_utilization,
                            "monthly_cost": float(monthly_cost),
                            "instance_count": reservation.properties.quantity,
                            "term": reservation.properties.term,
                            "expiration_date": reservation.properties.expiry_date.isoformat() if reservation.properties.expiry_date else None,
                        })
            
            return {"underutilized": underutilized}
            
        except Exception as e:
            self.logger.error(f"Error getting reserved instances utilization: {str(e)}")
            return {"underutilized": []}
    
    async def get_on_demand_ri_opportunities(
        self, instances: List[Resource], region: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Identify on-demand instances that could benefit from reservations."""
        opportunities = []
        
        try:
            # Group instances by size and region
            instance_groups = {}
            for instance in instances:
                if instance.type == ResourceType.INSTANCE and instance.is_active:
                    if region and instance.region != region:
                        continue
                    
                    key = (instance.metadata.get('vm_size'), instance.region)
                    if key not in instance_groups:
                        instance_groups[key] = []
                    instance_groups[key].append(instance)
            
            # Check for RI opportunities (3+ instances of same type)
            for (vm_size, location), instances in instance_groups.items():
                if len(instances) >= 3:
                    # Calculate potential savings
                    total_monthly_cost = sum(i.monthly_cost for i in instances)
                    estimated_savings = total_monthly_cost * Decimal('0.3')  # 30% savings estimate
                    
                    opportunities.append({
                        "instance_type": vm_size,
                        "region": location,
                        "instance_count": len(instances),
                        "on_demand_monthly_cost": float(total_monthly_cost),
                        "estimated_monthly_savings": float(estimated_savings),
                        "savings_percentage": 30.0,
                        "recommended_term": "1-year",
                        "break_even_months": 8,
                    })
            
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Error identifying RI opportunities: {str(e)}")
            return []
    
    async def get_savings_plans_coverage(
        self, region: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get savings plans coverage data."""
        # Note: Azure doesn't have AWS-style savings plans, but has reservations
        # We'll adapt this to show reservation coverage
        try:
            # Get total compute spend
            end_date = datetime.now(timezone.utc).date()
            start_date = end_date - timedelta(days=30)
            
            usage_details = self._consumption_client.usage_details.list(
                scope=f"/subscriptions/{self._subscription_id}",
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
            
            total_compute_spend = Decimal('0')
            covered_spend = Decimal('0')
            
            for usage in usage_details:
                if usage.properties.consumed_service in ['Microsoft.Compute', 'Microsoft.Sql']:
                    cost = Decimal(str(usage.properties.cost or 0))
                    total_compute_spend += cost
                    
                    # Check if covered by reservation
                    if usage.properties.reservation_id:
                        covered_spend += cost
            
            coverage_percentage = float(
                (covered_spend / total_compute_spend * 100) if total_compute_spend > 0 else 0
            )
            
            # Check for expiring reservations
            expiring_plans = []
            reservations = self._reservations_client.reservation.list_all()
            
            for reservation in reservations:
                if reservation.properties.expiry_date:
                    days_until_expiry = (
                        reservation.properties.expiry_date.date() - datetime.now(timezone.utc).date()
                    ).days
                    
                    if days_until_expiry <= 90:
                        monthly_commitment = self._estimate_reservation_cost(
                            reservation.sku.name,
                            reservation.location,
                            reservation.properties.term
                        )
                        
                        expiring_plans.append({
                            "plan_id": reservation.name,
                            "plan_type": f"Azure Reservation - {reservation.sku.name}",
                            "days_until_expiry": days_until_expiry,
                            "expiry_date": reservation.properties.expiry_date.isoformat(),
                            "monthly_commitment": float(monthly_commitment),
                            "utilization_percentage": 80.0,  # Placeholder
                        })
            
            return {
                "coverage_percentage": coverage_percentage,
                "total_compute_spend": float(total_compute_spend),
                "covered_spend": float(covered_spend),
                "on_demand_spend": float(total_compute_spend - covered_spend),
                "expiring_plans": expiring_plans,
            }
            
        except Exception as e:
            self.logger.error(f"Error getting savings plans coverage: {str(e)}")
            return {
                "coverage_percentage": 0,
                "total_compute_spend": 0,
                "covered_spend": 0,
                "expiring_plans": [],
            }
    
    # Helper methods for cost estimation
    def _estimate_vm_cost(self, vm_size: str, region: str) -> Decimal:
        """Estimate monthly cost for a VM size."""
        # Simplified pricing map (would use Pricing API in production)
        base_prices = {
            'Standard_B1s': 10,
            'Standard_B2s': 40,
            'Standard_D2s_v3': 70,
            'Standard_D4s_v3': 140,
            'Standard_D8s_v3': 280,
            'Standard_E2s_v3': 80,
            'Standard_E4s_v3': 160,
            'Standard_E8s_v3': 320,
        }
        
        base_price = base_prices.get(vm_size, 100)  # Default to $100
        return Decimal(str(base_price * 730 / 24))  # Convert hourly to monthly
    
    def _estimate_disk_cost(self, size_gb: int, sku: str, region: str) -> Decimal:
        """Estimate monthly cost for a managed disk."""
        # Simplified pricing
        price_per_gb = {
            'Premium_LRS': 0.15,
            'Standard_LRS': 0.05,
            'StandardSSD_LRS': 0.075,
        }
        
        rate = price_per_gb.get(sku, 0.05)
        return Decimal(str(size_gb * rate))
    
    def _estimate_snapshot_cost(self, size_gb: int, region: str) -> Decimal:
        """Estimate monthly cost for a snapshot."""
        # Azure snapshots: ~$0.05 per GB per month
        return Decimal(str(size_gb * 0.05))
    
    def _estimate_sql_database_cost(self, sku: str, tier: str, region: str) -> Decimal:
        """Estimate monthly cost for a SQL database."""
        # Simplified pricing map
        base_prices = {
            'GP_Gen5_2': 250,
            'GP_Gen5_4': 500,
            'GP_Gen5_8': 1000,
            'BC_Gen5_2': 500,
            'BC_Gen5_4': 1000,
            'S0': 15,
            'S1': 30,
            'S2': 75,
            'S3': 150,
            'P1': 465,
            'P2': 930,
            'P4': 1860,
        }
        
        return Decimal(str(base_prices.get(sku, 200)))
    
    def _estimate_reservation_cost(self, sku: str, region: str, term: str) -> Decimal:
        """Estimate monthly cost for a reservation."""
        # Simplified - would calculate based on VM size and term
        base_cost = self._estimate_vm_cost(sku, region)
        discount = Decimal('0.7') if term == '3 Years' else Decimal('0.85')
        return base_cost * discount
    
    def _get_sku_cpu_baseline(self, sku: str) -> int:
        """Get baseline CPU for a SKU."""
        cpu_map = {
            'GP_Gen5_2': 2,
            'GP_Gen5_4': 4,
            'GP_Gen5_8': 8,
            'BC_Gen5_2': 2,
            'BC_Gen5_4': 4,
        }
        return cpu_map.get(sku, 2)
    
    def _get_sku_memory_gb(self, sku: str) -> int:
        """Get memory in GB for a SKU."""
        memory_map = {
            'GP_Gen5_2': 10,
            'GP_Gen5_4': 20,
            'GP_Gen5_8': 40,
            'BC_Gen5_2': 10,
            'BC_Gen5_4': 20,
        }
        return memory_map.get(sku, 10)
    
    async def _get_disk_detach_time(self, resource_group: str, disk_name: str) -> Optional[datetime]:
        """Try to get disk detach time from activity logs."""
        try:
            # Query activity logs for disk detach events
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=90)
            
            filter_string = (
                f"eventTimestamp ge '{start_time.isoformat()}' and "
                f"eventTimestamp le '{end_time.isoformat()}' and "
                f"resourceId eq '/subscriptions/{self._subscription_id}/resourceGroups/"
                f"{resource_group}/providers/Microsoft.Compute/disks/{disk_name}'"
            )
            
            activities = self._monitor_client.activity_logs.list(
                filter=filter_string,
                select="eventTimestamp,operationName"
            )
            
            for activity in activities:
                if activity.operation_name.value == "Microsoft.Compute/disks/detach/action":
                    return activity.event_timestamp
            
            # If no detach event found, assume it's been detached for a while
            return datetime.now(timezone.utc) - timedelta(days=30)
            
        except Exception as e:
            self.logger.warning(f"Failed to get disk detach time: {str(e)}")
            return None
    
    # Implement remaining abstract methods
    
    async def validate_credentials(self) -> bool:
        """Validate that credentials are valid."""
        try:
            # Try to list resource groups to validate credentials
            list(self._resource_client.resource_groups.list())
            return True
        except Exception:
            return False
    
    async def list_regions(self) -> List[str]:
        """List available regions for Azure."""
        # Common Azure regions
        return [
            "eastus", "eastus2", "westus", "westus2", "centralus",
            "northeurope", "westeurope", "uksouth", "ukwest",
            "australiaeast", "australiasoutheast", "japaneast", "japanwest",
            "canadacentral", "canadaeast", "southindia", "centralindia",
            "westindia", "koreacentral", "koreasouth"
        ]
    
    async def list_instances(self, region: str) -> List[Resource]:
        """List compute instances in a region."""
        resources = await self.list_resources(
            resource_types={ResourceType.INSTANCE},
            regions={region}
        )
        return resources
    
    async def list_volumes(self, region: str) -> List[Resource]:
        """List storage volumes in a region."""
        resources = await self.list_resources(
            resource_types={ResourceType.VOLUME},
            regions={region}
        )
        return resources
    
    async def list_snapshots(self, region: str) -> List[Resource]:
        """List snapshots in a region."""
        resources = await self.list_resources(
            resource_types={ResourceType.SNAPSHOT},
            regions={region}
        )
        return resources
    
    async def list_databases(self, region: str) -> List[Resource]:
        """List database instances in a region."""
        resources = await self.list_resources(
            resource_types={ResourceType.DATABASE},
            regions={region}
        )
        return resources
    
    async def list_load_balancers(self, region: str) -> List[Resource]:
        """List load balancers in a region."""
        # Not implemented for initial version
        return []
    
    async def list_ip_addresses(self, region: str) -> List[Resource]:
        """List IP addresses in a region."""
        # Not implemented for initial version
        return []
    
    async def get_instance_metrics(
        self, instance_id: str, region: str, days: int = 7
    ) -> Dict[str, Any]:
        """Get utilization metrics for an instance."""
        try:
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=days)
            
            metrics = {
                'avg_cpu_percent': 0,
                'max_cpu_percent': 0,
                'avg_memory_percent': 0,
                'max_memory_percent': 0,
            }
            
            # Get CPU metrics
            # Format timespan correctly for Azure Monitor API
            timespan = f"{start_time.strftime('%Y-%m-%dT%H:%M:%SZ')}/{end_time.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            
            cpu_data = self._monitor_client.metrics.list(
                resource_uri=instance_id,
                timespan=timespan,
                interval='PT1H',
                metricnames='Percentage CPU',
                aggregation='Average,Maximum'
            )
            
            for metric in cpu_data.value:
                if metric.name.value == 'Percentage CPU':
                    cpu_values = []
                    max_cpu = 0
                    for timeseries in metric.timeseries:
                        for data in timeseries.data:
                            if data.average is not None:
                                cpu_values.append(data.average)
                            if data.maximum is not None:
                                max_cpu = max(max_cpu, data.maximum)
                    
                    if cpu_values:
                        metrics['avg_cpu_percent'] = sum(cpu_values) / len(cpu_values)
                        metrics['max_cpu_percent'] = max_cpu
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error getting instance metrics: {str(e)}")
            return {
                'avg_cpu_percent': 0,
                'max_cpu_percent': 0,
                'avg_memory_percent': 0,
                'max_memory_percent': 0,
            }
    
    async def get_volume_metrics(
        self, volume_id: str, region: str, days: int = 7
    ) -> Dict[str, Any]:
        """Get utilization metrics for a volume."""
        # Azure doesn't provide detailed volume metrics in the same way
        return {
            'avg_read_ops': 0,
            'avg_write_ops': 0,
            'avg_read_bytes': 0,
            'avg_write_bytes': 0,
        }
    
    async def estimate_monthly_cost(self, resource: Resource) -> float:
        """Estimate monthly cost for a resource."""
        # This would typically use the Azure Pricing API
        # For now, return the cost already set on the resource
        return float(resource.monthly_cost)