"""Check for Azure Premium Storage optimization opportunities."""

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


class AzurePremiumStorageCheck(Check):
    """Check for Premium Storage optimization opportunities.
    
    Premium Storage (SSD) is significantly more expensive than Standard Storage.
    This check identifies Premium Storage accounts that could use Standard Storage
    based on performance requirements and usage patterns.
    """
    
    def __init__(self, iops_threshold: int = 500) -> None:
        """Initialize the check.
        
        Args:
            iops_threshold: IOPS threshold below which Standard might be sufficient
        """
        self.iops_threshold = iops_threshold
        self.logger = logging.getLogger(__name__)
        
        # Premium is roughly 4-10x more expensive than Standard
        self.premium_to_standard_savings_percent = 75
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.STORAGE_TIER
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure Premium Storage Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies Premium Storage accounts with low IOPS (<{self.iops_threshold}) "
            "that could use Standard Storage for significant cost savings"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only Azure storage accounts."""
        return [
            r for r in resources
            if r.type == ResourceType.BUCKET and r.provider == CloudProvider.AZURE
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
                # Get storage account details
                storage_info = await provider.get_storage_info(resource.id, resource.region)
                
                # Check if it's Premium storage
                sku_tier = storage_info.get("sku_tier", "").lower()
                if sku_tier != "premium":
                    continue
                
                # Get performance metrics
                performance_metrics = storage_info.get("performance_metrics", {})
                avg_iops = performance_metrics.get("avg_iops", 0)
                max_iops = performance_metrics.get("max_iops", 0)
                avg_throughput_mbps = performance_metrics.get("avg_throughput_mbps", 0)
                
                # Check if performance requirements are low
                if avg_iops >= self.iops_threshold or max_iops >= self.iops_threshold * 2:
                    continue
                
                # Check usage patterns
                account_kind = storage_info.get("account_kind", "")
                total_size_gb = storage_info.get("total_size_gb", 0)
                
                # Determine if suitable for Standard storage
                suitable_for_standard = True
                reasons = []
                
                if avg_iops < self.iops_threshold / 2:
                    reasons.append(f"Very low IOPS: {avg_iops:.0f} average")
                elif avg_iops < self.iops_threshold:
                    reasons.append(f"Low IOPS: {avg_iops:.0f} average")
                
                if avg_throughput_mbps < 60:  # Standard can handle up to 60 MB/s
                    reasons.append(f"Low throughput: {avg_throughput_mbps:.1f} MB/s")
                
                # Check if it's being used for non-performance-critical workloads
                is_non_critical = False
                if resource.tags:
                    env_tag = resource.tags.get("environment", "").lower()
                    if env_tag in ["dev", "test", "staging", "backup"]:
                        is_non_critical = True
                        reasons.append(f"Non-production environment: {env_tag}")
                
                # Page blobs (used for VHDs) might need Premium for VMs
                if account_kind == "BlobStorage" and storage_info.get("page_blob_count", 0) > 0:
                    suitable_for_standard = False
                
                if not suitable_for_standard or not reasons:
                    continue
                
                # Calculate savings
                monthly_savings = resource.monthly_cost * Decimal(self.premium_to_standard_savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                if monthly_savings < Decimal("20"):
                    continue
                
                # Determine severity
                severity = self._calculate_severity(monthly_savings, is_non_critical)
                
                # Adjust confidence based on workload
                confidence = DEFAULT_CHECK_CONFIDENCE
                if is_non_critical:
                    confidence *= 0.95
                else:
                    confidence *= 0.8  # Lower confidence for production workloads
                
                result = CheckResult(
                    id=f"storage-premium-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Premium Storage Overprovisioning: {resource.name}",
                    description=(
                        f"Premium Storage account showing low performance utilization. "
                        f"IOPS: {avg_iops:.0f} avg, {max_iops:.0f} max. "
                        f"Size: {total_size_gb:.1f} GB"
                    ),
                    impact=(
                        "Premium Storage provides high IOPS and low latency but costs significantly more. "
                        "Based on current usage patterns, Standard Storage with SSD option could provide "
                        "sufficient performance at a fraction of the cost. " + 
                        (" ".join(reasons))
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float(self.premium_to_standard_savings_percent),
                    effort_level="medium",
                    risk_level="medium" if not is_non_critical else "low",
                    implementation_steps=[
                        "1. Analyze peak performance requirements over 30 days",
                        "2. Verify no applications require Premium Storage features",
                        "3. Create a new Standard Storage account (with Standard SSD if needed)",
                        "4. Test application performance with Standard Storage",
                        "5. Plan migration during maintenance window",
                        "6. Use AzCopy or Azure Data Factory to migrate data",
                        "7. Update application connection strings",
                        "8. Monitor performance for 1 week after migration",
                        "9. Keep Premium Storage account for 30 days before deletion",
                        "10. Consider Standard SSD for balanced price/performance",
                    ],
                    confidence_score=confidence,
                    check_metadata={
                        "sku_tier": sku_tier,
                        "account_kind": account_kind,
                        "avg_iops": round(avg_iops, 0),
                        "max_iops": round(max_iops, 0),
                        "avg_throughput_mbps": round(avg_throughput_mbps, 2),
                        "total_size_gb": round(total_size_gb, 2),
                        "is_non_critical": is_non_critical,
                        "optimization_reasons": reasons,
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check premium storage for {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal, is_non_critical: bool) -> CheckSeverity:
        """Calculate severity based on savings and criticality."""
        if is_non_critical and monthly_savings > Decimal("100"):
            return CheckSeverity.HIGH
        elif monthly_savings > Decimal("500"):
            return CheckSeverity.HIGH
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.MEDIUM
        else:
            return CheckSeverity.LOW