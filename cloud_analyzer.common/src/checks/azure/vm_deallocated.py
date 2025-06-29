"""Check for stopped but not deallocated Azure VMs."""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    CRITICAL_MONTHLY_SAVINGS_THRESHOLD,
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class AzureVMDeallocatedCheck(Check):
    """Check for Azure VMs that are stopped but not deallocated.
    
    In Azure, VMs in 'Stopped' state still incur compute charges. They must be
    'Stopped (Deallocated)' to avoid charges. This check identifies VMs that are
    stopped but not deallocated.
    
    Attributes:
        min_days_stopped: Minimum days a VM must be stopped before flagging
    """
    
    def __init__(self, min_days_stopped: int = 7) -> None:
        """Initialize the check.
        
        Args:
            min_days_stopped: Minimum days a VM must be stopped to be flagged
        """
        self.min_days_stopped = min_days_stopped
        self.logger = logging.getLogger(__name__)
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.IDLE_RESOURCE
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure VM Deallocation Check"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies Azure VMs that have been stopped for more than "
            f"{self.min_days_stopped} days but are not deallocated, continuing to incur charges"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only Azure VMs."""
        return [
            r for r in resources
            if r.type == ResourceType.INSTANCE and r.provider == CloudProvider.AZURE
        ]
    
    async def run(
        self,
        provider: CloudProviderInterface,
        resources: List[Resource],
        region: Optional[str] = None,
    ) -> List[CheckResult]:
        """Run the check against provided resources."""
        results = []
        
        for resource in resources:
            if region and resource.region != region:
                continue
            
            try:
                # Check VM state from metadata
                vm_state = resource.state.lower()
                
                # In Azure, "stopped" means VM is stopped but still allocated
                # "deallocated" means VM is stopped and deallocated (no charges)
                if vm_state == "stopped" and resource.metadata.get("power_state") != "deallocated":
                    # Get instance metrics to determine how long it's been stopped
                    instance_info = await provider.get_instance_info(resource.id, resource.region)
                    
                    # Calculate days stopped (using last state change time if available)
                    days_stopped = self.min_days_stopped  # Default if we can't determine
                    if instance_info.get("state_transition_time"):
                        transition_time = instance_info["state_transition_time"]
                        if isinstance(transition_time, str):
                            transition_time = datetime.fromisoformat(transition_time.replace('Z', '+00:00'))
                        days_stopped = (datetime.now(timezone.utc) - transition_time).days
                    
                    if days_stopped >= self.min_days_stopped:
                        # Calculate savings (100% of compute cost)
                        monthly_savings = resource.monthly_cost
                        annual_savings = monthly_savings * 12
                        
                        # Determine severity based on cost
                        severity = self._calculate_severity(monthly_savings)
                        
                        result = CheckResult(
                            id=f"vm-not-deallocated-{resource.id}",
                            check_type=self.check_type,
                            severity=severity,
                            resource=resource,
                            title=f"Stopped VM Not Deallocated: {resource.name}",
                            description=(
                                f"VM has been stopped for {days_stopped} days but is not deallocated. "
                                f"Size: {resource.metadata.get('vm_size', 'Unknown')}, "
                                f"Still incurring compute charges."
                            ),
                            impact=(
                                "Stopped VMs in Azure continue to incur compute charges unless deallocated. "
                                "Deallocating the VM will stop compute charges while preserving the VM configuration."
                            ),
                            current_cost=resource.monthly_cost,
                            optimized_cost=Decimal("0"),
                            monthly_savings=monthly_savings,
                            annual_savings=annual_savings,
                            savings_percentage=100.0,
                            effort_level="low",
                            risk_level="low",
                            implementation_steps=[
                                "1. Verify the VM is not needed in its current state",
                                "2. Stop and deallocate the VM using Azure Portal or CLI",
                                "3. For Azure CLI: az vm deallocate --resource-group <rg> --name <vm-name>",
                                "4. To restart later: az vm start --resource-group <rg> --name <vm-name>",
                                "5. Consider automation for dev/test VMs to deallocate outside business hours",
                            ],
                            confidence_score=DEFAULT_CHECK_CONFIDENCE,
                            check_metadata={
                                "days_stopped": days_stopped,
                                "vm_size": resource.metadata.get("vm_size"),
                                "current_state": vm_state,
                                "os_type": resource.metadata.get("os_type"),
                            },
                        )
                        
                        results.append(result)
                        
            except Exception as e:
                self.logger.warning(
                    f"Failed to check VM {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > CRITICAL_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM