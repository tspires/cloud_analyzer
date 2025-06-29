"""Check for Azure Spot VM opportunities."""

import logging
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class AzureSpotVMCheck(Check):
    """Check for opportunities to use Azure Spot VMs.
    
    Azure Spot VMs offer up to 90% discount compared to regular VMs by using
    unused Azure capacity. They're ideal for workloads that can handle interruptions
    like batch processing, dev/test, and stateless applications.
    """
    
    def __init__(self) -> None:
        """Initialize the check."""
        self.logger = logging.getLogger(__name__)
        
        # Typical spot savings percentage (conservative estimate)
        self.spot_savings_percent = 70
        
        # Workload patterns suitable for spot
        self.spot_suitable_tags = [
            "dev", "test", "staging", "batch", "processing", 
            "worker", "compute", "analysis", "non-prod"
        ]
        
        # VM name patterns that might indicate spot suitability
        self.spot_suitable_patterns = [
            "dev", "test", "stg", "batch", "worker", 
            "process", "compute", "temp", "sandbox"
        ]
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.SPOT_OPPORTUNITY
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure Spot VM Opportunities"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            "Identifies Azure VMs that could potentially use Spot instances "
            "for up to 90% cost savings based on workload characteristics"
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
    
    def _is_spot_suitable(self, resource: Resource) -> bool:
        """Determine if a VM might be suitable for spot instances."""
        # Check tags
        if resource.tags:
            for tag_key, tag_value in resource.tags.items():
                # Check tag keys and values
                for pattern in self.spot_suitable_tags:
                    if pattern in tag_key.lower() or pattern in str(tag_value).lower():
                        return True
        
        # Check resource name
        resource_name = resource.name.lower()
        for pattern in self.spot_suitable_patterns:
            if pattern in resource_name:
                return True
        
        # Check if it's already marked as non-production
        env_tag = resource.tags.get("environment", "").lower()
        if env_tag in ["dev", "test", "staging", "qa", "development"]:
            return True
        
        return False
    
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
                # Get VM info to check if already using spot
                vm_info = await provider.get_instance_info(resource.id, resource.region)
                
                # Skip if already using spot
                if vm_info.get("priority", "").lower() == "spot":
                    continue
                
                # Check if VM is suitable for spot
                if not self._is_spot_suitable(resource):
                    continue
                
                # Check VM size availability for spot
                vm_size = resource.metadata.get("vm_size", "")
                
                # Some VM sizes aren't available as spot
                if vm_size.startswith(("Basic", "Promo")):
                    continue
                
                # Calculate potential savings
                monthly_savings = resource.monthly_cost * Decimal(self.spot_savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                # Only report if savings are significant
                if monthly_savings < Decimal("20"):
                    continue
                
                # Determine severity based on savings
                severity = self._calculate_severity(monthly_savings)
                
                # Determine confidence based on workload indicators
                confidence = DEFAULT_CHECK_CONFIDENCE
                if self._is_spot_suitable(resource):
                    confidence *= 0.9  # High confidence for clearly suitable workloads
                else:
                    confidence *= 0.7  # Lower confidence otherwise
                
                result = CheckResult(
                    id=f"vm-spot-opportunity-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Spot VM Opportunity: {resource.name}",
                    description=(
                        f"VM appears suitable for Spot pricing based on workload type. "
                        f"Size: {vm_size}, Current type: Regular, "
                        f"Potential savings: up to {self.spot_savings_percent}%"
                    ),
                    impact=(
                        "Azure Spot VMs use unused capacity at significant discounts. "
                        "Suitable for interruptible workloads like batch processing, "
                        "dev/test environments, and stateless applications. "
                        "VMs may be evicted when Azure needs capacity back."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float(self.spot_savings_percent),
                    effort_level="medium",
                    risk_level="medium",
                    implementation_steps=[
                        "1. Verify workload can handle interruptions (evictions)",
                        "2. Implement eviction handling (save state, graceful shutdown)",
                        "3. Create new Spot VM or convert existing VM",
                        "4. Set maximum price (recommend 'pay up to standard prices')",
                        "5. For conversion: Deallocate VM, change to Spot, restart",
                        "6. Use availability sets or zones for better availability",
                        "7. Monitor eviction rates and adjust if needed",
                        "8. Consider VM Scale Sets with mixed Spot/Regular instances",
                    ],
                    confidence_score=confidence,
                    check_metadata={
                        "vm_size": vm_size,
                        "current_priority": vm_info.get("priority", "Regular"),
                        "environment": resource.tags.get("environment", "unknown"),
                        "workload_type": "interruptible",
                        "spot_suitable_indicators": {
                            "has_suitable_tags": bool([t for t in self.spot_suitable_tags 
                                                     if any(t in str(v).lower() for v in resource.tags.values())]),
                            "has_suitable_name": any(p in resource.name.lower() for p in self.spot_suitable_patterns),
                        }
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check spot opportunities for VM {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > Decimal("500"):
            return CheckSeverity.HIGH
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.MEDIUM
        else:
            return CheckSeverity.LOW