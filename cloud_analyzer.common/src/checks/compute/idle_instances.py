"""Check for idle compute instances."""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    CPU_IDLE_THRESHOLD_PERCENT,
    CRITICAL_MONTHLY_SAVINGS_THRESHOLD,
    DEFAULT_CHECK_CONFIDENCE,
    DEFAULT_METRICS_DAYS,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
    NETWORK_IDLE_THRESHOLD_BYTES,
)
from models import (
    CheckResult,
    CheckSeverity,
    CheckType,
    CloudProvider,
    Resource,
    ResourceType,
)
from providers.base import CloudProviderInterface
from checks.base import Check


class IdleInstanceCheck(Check):
    """Check for idle compute instances."""
    
    def __init__(
        self,
        cpu_threshold: float = CPU_IDLE_THRESHOLD_PERCENT,
        network_threshold: float = NETWORK_IDLE_THRESHOLD_BYTES,
        days_to_check: int = DEFAULT_METRICS_DAYS,
    ) -> None:
        """Initialize idle instance check.
        
        Args:
            cpu_threshold: CPU utilization threshold (%)
            network_threshold: Network traffic threshold (bytes)
            days_to_check: Number of days to analyze
        """
        self.cpu_threshold = cpu_threshold
        self.network_threshold = network_threshold
        self.days_to_check = days_to_check
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.IDLE_RESOURCE
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Idle Instance Detection"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies compute instances with CPU utilization below {self.cpu_threshold}% "
            f"and network traffic below {self.network_threshold/1e6:.1f}MB over the last "
            f"{self.days_to_check} days"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only running compute instances."""
        return [
            r for r in resources
            if r.type == ResourceType.INSTANCE and r.is_active
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
            
            # Get instance metrics
            metrics = await provider.get_instance_metrics(
                resource.id, resource.region, self.days_to_check
            )
            
            # Check if instance is idle
            avg_cpu = metrics.get("avg_cpu_percent", 100)
            avg_network = metrics.get("avg_network_bytes", float("inf"))
            
            if avg_cpu < self.cpu_threshold and avg_network < self.network_threshold:
                # Calculate savings (100% of instance cost)
                monthly_savings = resource.monthly_cost
                annual_savings = monthly_savings * 12
                
                # Determine severity based on cost
                severity = self._calculate_severity(monthly_savings)
                
                result = CheckResult(
                    id=f"idle-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Idle Instance: {resource.name}",
                    description=(
                        f"Instance has been idle for the past {self.days_to_check} days with "
                        f"average CPU utilization of {avg_cpu:.1f}% and network traffic of "
                        f"{avg_network/1e6:.1f}MB"
                    ),
                    impact=(
                        "This instance appears to be unused and is incurring unnecessary costs. "
                        "Consider terminating or stopping it."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=Decimal("0"),
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=100.0,
                    effort_level="low",
                    risk_level="low",
                    implementation_steps=[
                        "1. Verify the instance is truly not needed",
                        "2. Create a snapshot/backup if needed",
                        "3. Stop or terminate the instance",
                        "4. Monitor for any issues after termination",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "avg_cpu_percent": avg_cpu,
                        "avg_network_mb": avg_network / 1e6,
                        "threshold_cpu_percent": self.cpu_threshold,
                        "threshold_network_mb": self.network_threshold / 1e6,
                        "days_analyzed": self.days_to_check,
                    },
                )
                
                results.append(result)
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > CRITICAL_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM