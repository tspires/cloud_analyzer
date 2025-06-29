"""Check for Azure VM Reserved Instance opportunities."""

import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Dict, List, Optional, Set, Tuple

from constants import (
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class AzureVMReservedInstancesCheck(Check):
    """Check for Azure VM Reserved Instance opportunities.
    
    Azure Reserved VM Instances provide up to 72% savings compared to pay-as-you-go
    pricing in exchange for a 1 or 3 year commitment. This check identifies VMs that
    have been running consistently and could benefit from reservations.
    
    Attributes:
        min_runtime_days: Minimum days a VM must be running to consider for RI
        min_savings_threshold: Minimum monthly savings to report
    """
    
    def __init__(
        self, 
        min_runtime_days: int = 30,
        min_savings_threshold: Decimal = Decimal("50")
    ) -> None:
        """Initialize the check.
        
        Args:
            min_runtime_days: Minimum days VM must be running
            min_savings_threshold: Minimum monthly savings to report
        """
        self.min_runtime_days = min_runtime_days
        self.min_savings_threshold = min_savings_threshold
        self.logger = logging.getLogger(__name__)
        
        # Typical RI savings percentages by term
        self.savings_percentages = {
            "1year": 40,  # ~40% savings for 1-year term
            "3year": 60,  # ~60% savings for 3-year term
        }
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.RESERVED_INSTANCE_OPTIMIZATION
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure VM Reserved Instances Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies Azure VMs running consistently for {self.min_runtime_days}+ days "
            "that could benefit from Reserved Instance pricing"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only running Azure VMs."""
        return [
            r for r in resources
            if r.type == ResourceType.INSTANCE 
            and r.provider == CloudProvider.AZURE
            and r.is_active
            and r.state.lower() == "succeeded"
        ]
    
    async def run(
        self,
        provider: CloudProviderInterface,
        resources: List[Resource],
        region: Optional[str] = None,
    ) -> List[CheckResult]:
        """Run the check against provided resources."""
        results = []
        
        # Group VMs by size and region for RI recommendations
        vm_groups: Dict[Tuple[str, str], List[Resource]] = defaultdict(list)
        
        for resource in resources:
            if region and resource.region != region:
                continue
            
            vm_size = resource.metadata.get("vm_size", "unknown")
            vm_groups[(vm_size, resource.region)].append(resource)
        
        # Check existing reservations
        try:
            existing_reservations = await provider.get_reserved_instances()
        except Exception as e:
            self.logger.warning(f"Failed to get existing reservations: {str(e)}")
            existing_reservations = []
        
        # Analyze each group
        for (vm_size, vm_region), vms in vm_groups.items():
            try:
                # Skip if too few instances
                if len(vms) < 1:
                    continue
                
                # Check how long VMs have been running
                long_running_vms = []
                total_monthly_cost = Decimal("0")
                
                for vm in vms:
                    # Get VM metrics to check runtime
                    vm_info = await provider.get_instance_info(vm.id, vm.region)
                    
                    # Check if VM has been running long enough
                    launch_time = vm.created_at or vm_info.get("launch_time")
                    if launch_time:
                        if isinstance(launch_time, str):
                            launch_time = datetime.fromisoformat(launch_time.replace('Z', '+00:00'))
                        
                        days_running = (datetime.now(timezone.utc) - launch_time).days
                        
                        if days_running >= self.min_runtime_days:
                            long_running_vms.append(vm)
                            total_monthly_cost += vm.monthly_cost
                
                if not long_running_vms:
                    continue
                
                # Check if we already have reservations for this size/region
                covered_count = sum(
                    r.get("quantity", 0) for r in existing_reservations
                    if r.get("vm_size") == vm_size and r.get("region") == vm_region
                )
                
                uncovered_vms = len(long_running_vms) - covered_count
                if uncovered_vms <= 0:
                    continue
                
                # Calculate savings for different terms
                for term, savings_percent in self.savings_percentages.items():
                    # Calculate per-VM costs
                    per_vm_monthly_cost = total_monthly_cost / len(long_running_vms)
                    monthly_savings_per_vm = per_vm_monthly_cost * Decimal(savings_percent) / Decimal(100)
                    
                    # Total savings for uncovered VMs
                    total_monthly_savings = monthly_savings_per_vm * uncovered_vms
                    
                    if total_monthly_savings < self.min_savings_threshold:
                        continue
                    
                    annual_savings = total_monthly_savings * 12
                    optimized_cost = (per_vm_monthly_cost - monthly_savings_per_vm) * uncovered_vms
                    
                    # Determine severity
                    severity = self._calculate_severity(total_monthly_savings)
                    
                    # Create result for the group
                    result = CheckResult(
                        id=f"vm-ri-{vm_size}-{vm_region}-{term}",
                        check_type=self.check_type,
                        severity=severity,
                        resource=long_running_vms[0],  # Representative VM
                        related_resources=long_running_vms[1:] if len(long_running_vms) > 1 else [],
                        title=f"Reserved Instance Opportunity: {uncovered_vms} x {vm_size}",
                        description=(
                            f"{uncovered_vms} VM(s) of size {vm_size} in {vm_region} running consistently. "
                            f"{term} Reserved Instance could save {savings_percent}%"
                        ),
                        impact=(
                            f"These VMs have been running for {self.min_runtime_days}+ days and show consistent usage. "
                            f"Purchasing {term} Reserved Instances would provide {savings_percent}% savings with "
                            "upfront or monthly payment options available."
                        ),
                        current_cost=per_vm_monthly_cost * uncovered_vms,
                        optimized_cost=optimized_cost,
                        monthly_savings=total_monthly_savings,
                        annual_savings=annual_savings,
                        savings_percentage=float(savings_percent),
                        effort_level="low",
                        risk_level="low",
                        implementation_steps=[
                            "1. Review VM usage patterns to confirm consistent runtime",
                            "2. Determine payment option: All Upfront, Partial Upfront, or Monthly",
                            "3. Purchase Reserved Instances in Azure Portal > Reservations",
                            f"4. Select: Size={vm_size}, Region={vm_region}, Term={term}, Quantity={uncovered_vms}",
                            "5. Reservations apply automatically to matching VMs",
                            "6. Monitor usage in Cost Management to ensure utilization",
                            "7. Consider Azure Hybrid Benefit for additional Windows/SQL savings",
                        ],
                        confidence_score=DEFAULT_CHECK_CONFIDENCE,
                        check_metadata={
                            "vm_size": vm_size,
                            "region": vm_region,
                            "term": term,
                            "uncovered_count": uncovered_vms,
                            "covered_count": covered_count,
                            "total_vms": len(long_running_vms),
                            "savings_percent": savings_percent,
                        },
                    )
                    
                    results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to analyze RI opportunities for {vm_size} in {vm_region}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > Decimal("1000"):
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM