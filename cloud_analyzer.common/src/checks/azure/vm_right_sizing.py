"""Check for Azure VM right-sizing opportunities."""

import logging
from decimal import Decimal
from typing import Dict, List, Optional, Set

from constants import (
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class AzureVMRightSizingCheck(Check):
    """Check for Azure VM right-sizing opportunities based on utilization.
    
    Analyzes CPU and memory utilization metrics to identify oversized VMs
    that can be downsized to save costs without impacting performance.
    
    Attributes:
        cpu_threshold: CPU utilization threshold (default 40%)
        memory_threshold: Memory utilization threshold (default 40%)
        days_to_analyze: Number of days of metrics to analyze
    """
    
    def __init__(
        self,
        cpu_threshold: float = 40.0,
        memory_threshold: float = 40.0,
        days_to_analyze: int = 14
    ) -> None:
        """Initialize the check.
        
        Args:
            cpu_threshold: Max CPU utilization to consider for downsizing
            memory_threshold: Max memory utilization to consider for downsizing
            days_to_analyze: Number of days of metrics to analyze
        """
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.days_to_analyze = days_to_analyze
        self.logger = logging.getLogger(__name__)
        
        # Azure VM size families and their typical sizing options
        self.vm_size_families = {
            "Standard_B": ["Standard_B1s", "Standard_B1ms", "Standard_B2s", "Standard_B2ms", "Standard_B4ms", "Standard_B8ms"],
            "Standard_D": ["Standard_D2s_v3", "Standard_D4s_v3", "Standard_D8s_v3", "Standard_D16s_v3", "Standard_D32s_v3"],
            "Standard_E": ["Standard_E2s_v3", "Standard_E4s_v3", "Standard_E8s_v3", "Standard_E16s_v3", "Standard_E32s_v3"],
            "Standard_F": ["Standard_F2s_v2", "Standard_F4s_v2", "Standard_F8s_v2", "Standard_F16s_v2", "Standard_F32s_v2"],
        }
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.RIGHT_SIZING
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure VM Right-Sizing Analysis"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Analyzes VM CPU and memory utilization over {self.days_to_analyze} days "
            f"to identify oversized VMs with <{self.cpu_threshold}% CPU and <{self.memory_threshold}% memory usage"
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
    
    def _get_vm_family(self, vm_size: str) -> str:
        """Extract VM family from size name."""
        # E.g., "Standard_D4s_v3" -> "Standard_D"
        parts = vm_size.split("_")
        if len(parts) >= 2:
            return f"{parts[0]}_{parts[1][0]}"
        return ""
    
    def _get_smaller_size(self, current_size: str) -> Optional[str]:
        """Get the next smaller size in the same family."""
        family = self._get_vm_family(current_size)
        
        # Look for family in our mapping
        for fam_prefix, sizes in self.vm_size_families.items():
            if family.startswith(fam_prefix) and current_size in sizes:
                current_index = sizes.index(current_size)
                if current_index > 0:
                    return sizes[current_index - 1]
        
        # Fallback: try to determine smaller size by pattern
        # E.g., D8s -> D4s, D16s -> D8s
        import re
        match = re.search(r'(\d+)', current_size)
        if match:
            current_num = int(match.group(1))
            if current_num > 2:
                smaller_num = current_num // 2
                return current_size.replace(str(current_num), str(smaller_num), 1)
        
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
            
            try:
                # Get VM metrics
                metrics = await provider.get_instance_metrics(
                    resource.id, 
                    resource.region, 
                    days=self.days_to_analyze
                )
                
                # Check if metrics are available
                if not metrics:
                    self.logger.warning(f"No metrics available for VM {resource.id}")
                    continue
                
                avg_cpu = metrics.get("avg_cpu_percent", 100)
                avg_memory = metrics.get("avg_memory_percent", 100)
                max_cpu = metrics.get("max_cpu_percent", 100)
                max_memory = metrics.get("max_memory_percent", 100)
                
                # Check if VM is underutilized
                if avg_cpu >= self.cpu_threshold or avg_memory >= self.memory_threshold:
                    continue
                
                # Also check max utilization to avoid sizing based on low average
                if max_cpu >= self.cpu_threshold * 2 or max_memory >= self.memory_threshold * 2:
                    continue
                
                current_size = resource.metadata.get("vm_size", "")
                smaller_size = self._get_smaller_size(current_size)
                
                if not smaller_size:
                    continue
                
                # Estimate savings (assume ~40% cost reduction for one size down)
                savings_percent = 40
                monthly_savings = resource.monthly_cost * Decimal(savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                # Only report if savings are significant
                if monthly_savings < Decimal("30"):
                    continue
                
                # Determine severity based on utilization and savings
                severity = self._calculate_severity(monthly_savings, avg_cpu, avg_memory)
                
                result = CheckResult(
                    id=f"vm-rightsizing-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Oversized VM: {resource.name}",
                    description=(
                        f"VM showing low utilization - CPU: {avg_cpu:.1f}% avg, {max_cpu:.1f}% max; "
                        f"Memory: {avg_memory:.1f}% avg, {max_memory:.1f}% max. "
                        f"Current: {current_size}, Recommended: {smaller_size}"
                    ),
                    impact=(
                        f"This VM has consistently low resource utilization over the past {self.days_to_analyze} days. "
                        "Downsizing to a smaller VM size can reduce costs while maintaining performance. "
                        "The recommended size provides adequate headroom for peak usage."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float(savings_percent),
                    effort_level="medium",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review VM workload patterns during peak hours",
                        "2. Create a snapshot or backup of the VM",
                        "3. Schedule downtime window (resize requires VM restart)",
                        "4. Resize VM in Azure Portal or CLI",
                        f"5. Azure CLI: az vm resize --resource-group <rg> --name <vm> --size {smaller_size}",
                        "6. Monitor performance after resize for 24-48 hours",
                        "7. Keep snapshot for 7 days in case rollback is needed",
                        "8. If performance issues occur, resize back to original size",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE * 0.85,  # Slightly lower due to metrics uncertainty
                    check_metadata={
                        "current_size": current_size,
                        "recommended_size": smaller_size,
                        "avg_cpu_percent": round(avg_cpu, 2),
                        "max_cpu_percent": round(max_cpu, 2),
                        "avg_memory_percent": round(avg_memory, 2),
                        "max_memory_percent": round(max_memory, 2),
                        "analysis_days": self.days_to_analyze,
                        "cpu_threshold": self.cpu_threshold,
                        "memory_threshold": self.memory_threshold,
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to analyze right-sizing for VM {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(
        self, 
        monthly_savings: Decimal, 
        avg_cpu: float, 
        avg_memory: float
    ) -> CheckSeverity:
        """Calculate severity based on savings and utilization."""
        # Lower utilization = higher severity
        utilization_factor = max(avg_cpu, avg_memory) / 100.0
        
        if monthly_savings > Decimal("500") and utilization_factor < 0.2:
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM