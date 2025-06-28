"""Check for right-sizing opportunities."""

from decimal import Decimal
from typing import Dict, List, Optional, Set

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


class RightSizingCheck(Check):
    """Check for compute instance right-sizing opportunities."""
    
    # Instance size mappings for different providers
    AWS_INSTANCE_SIZES = {
        "t3.micro": {"vcpu": 2, "memory": 1, "cost_factor": 1},
        "t3.small": {"vcpu": 2, "memory": 2, "cost_factor": 2},
        "t3.medium": {"vcpu": 2, "memory": 4, "cost_factor": 4},
        "t3.large": {"vcpu": 2, "memory": 8, "cost_factor": 8},
        "t3.xlarge": {"vcpu": 4, "memory": 16, "cost_factor": 16},
        "m5.large": {"vcpu": 2, "memory": 8, "cost_factor": 10},
        "m5.xlarge": {"vcpu": 4, "memory": 16, "cost_factor": 20},
        "m5.2xlarge": {"vcpu": 8, "memory": 32, "cost_factor": 40},
    }
    
    def __init__(
        self,
        cpu_threshold: float = 30.0,
        memory_threshold: float = 30.0,
        days_to_check: int = 14,
    ) -> None:
        """Initialize right-sizing check.
        
        Args:
            cpu_threshold: CPU utilization threshold (%)
            memory_threshold: Memory utilization threshold (%)
            days_to_check: Number of days to analyze
        """
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.days_to_check = days_to_check
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.RIGHT_SIZING
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Instance Right-Sizing"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies overprovisioned instances with CPU utilization below {self.cpu_threshold}% "
            f"or memory utilization below {self.memory_threshold}% that could be downsized"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AWS, CloudProvider.AZURE, CloudProvider.GCP}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only running compute instances."""
        return [
            r for r in resources
            if r.type == ResourceType.INSTANCE and r.is_active
        ]
    
    def _get_recommended_size(
        self, current_size: str, provider: CloudProvider, metrics: Dict[str, float]
    ) -> Optional[Dict[str, any]]:
        """Get recommended instance size based on utilization.
        
        Returns dict with 'size' and 'cost_reduction' keys, or None if no recommendation.
        """
        if provider == CloudProvider.AWS:
            # Simple example - in reality would need more sophisticated mapping
            if current_size.startswith("m5.2xlarge"):
                if metrics.get("max_cpu_percent", 100) < 25:
                    return {"size": "m5.large", "cost_reduction": 0.75}
                elif metrics.get("max_cpu_percent", 100) < 50:
                    return {"size": "m5.xlarge", "cost_reduction": 0.5}
            elif current_size.startswith("m5.xlarge"):
                if metrics.get("max_cpu_percent", 100) < 50:
                    return {"size": "m5.large", "cost_reduction": 0.5}
        
        return None
    
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
            
            # Check utilization
            avg_cpu = metrics.get("avg_cpu_percent", 100)
            max_cpu = metrics.get("max_cpu_percent", 100)
            avg_memory = metrics.get("avg_memory_percent", 100)
            max_memory = metrics.get("max_memory_percent", 100)
            
            # Determine if right-sizing is needed
            if (max_cpu < self.cpu_threshold and max_memory < self.memory_threshold):
                # Get current instance type from metadata
                instance_type = resource.metadata.get("instance_type", "unknown")
                
                # Get recommendation
                recommendation = self._get_recommended_size(
                    instance_type, provider.provider, metrics
                )
                
                if recommendation:
                    # Calculate savings
                    cost_reduction = recommendation["cost_reduction"]
                    monthly_savings = resource.monthly_cost * Decimal(str(cost_reduction))
                    annual_savings = monthly_savings * 12
                    optimized_cost = resource.monthly_cost - monthly_savings
                    
                    # Determine severity based on savings percentage
                    if cost_reduction > 0.5:
                        severity = CheckSeverity.HIGH
                    elif cost_reduction > 0.3:
                        severity = CheckSeverity.MEDIUM
                    else:
                        severity = CheckSeverity.LOW
                    
                    result = CheckResult(
                        id=f"rightsize-{resource.id}",
                        check_type=self.check_type,
                        severity=severity,
                        resource=resource,
                        title=f"Right-size Opportunity: {resource.name}",
                        description=(
                            f"Instance is overprovisioned with peak CPU at {max_cpu:.1f}% "
                            f"and peak memory at {max_memory:.1f}%. "
                            f"Recommend downsizing from {instance_type} to {recommendation['size']}."
                        ),
                        impact=(
                            f"Downsizing this instance will reduce costs by {cost_reduction*100:.0f}% "
                            "while still meeting performance requirements."
                        ),
                        current_cost=resource.monthly_cost,
                        optimized_cost=optimized_cost,
                        monthly_savings=monthly_savings,
                        annual_savings=annual_savings,
                        savings_percentage=cost_reduction * 100,
                        effort_level="medium",
                        risk_level="low",
                        implementation_steps=[
                            "1. Review application performance requirements",
                            "2. Test application on recommended instance size",
                            "3. Schedule maintenance window",
                            "4. Stop instance and change instance type",
                            "5. Start instance and verify performance",
                            "6. Monitor for 24-48 hours",
                        ],
                        confidence_score=0.8,
                        check_metadata={
                            "current_type": instance_type,
                            "recommended_type": recommendation["size"],
                            "avg_cpu_percent": avg_cpu,
                            "max_cpu_percent": max_cpu,
                            "avg_memory_percent": avg_memory,
                            "max_memory_percent": max_memory,
                            "days_analyzed": self.days_to_check,
                        },
                    )
                    
                    results.append(result)
        
        return results