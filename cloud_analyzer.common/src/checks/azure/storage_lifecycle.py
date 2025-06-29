"""Check for Azure Storage Account lifecycle management opportunities."""

import logging
from datetime import datetime, timedelta, timezone
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


class AzureStorageLifecycleCheck(Check):
    """Check for Azure Storage lifecycle management opportunities.
    
    Identifies storage accounts with data that could be moved to cooler tiers
    or deleted based on access patterns. Azure offers Hot, Cool, and Archive
    tiers with significant cost differences.
    
    Attributes:
        cool_tier_days: Days without access before recommending Cool tier
        archive_tier_days: Days without access before recommending Archive tier
    """
    
    def __init__(
        self, 
        cool_tier_days: int = 30,
        archive_tier_days: int = 180
    ) -> None:
        """Initialize the check.
        
        Args:
            cool_tier_days: Days before recommending Cool tier
            archive_tier_days: Days before recommending Archive tier
        """
        self.cool_tier_days = cool_tier_days
        self.archive_tier_days = archive_tier_days
        self.logger = logging.getLogger(__name__)
        
        # Approximate savings percentages compared to Hot tier
        self.tier_savings = {
            "cool": 50,      # ~50% cheaper than Hot
            "archive": 95    # ~95% cheaper than Hot
        }
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.STORAGE_TIER
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure Storage Lifecycle Management"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies storage accounts with infrequently accessed data that could be moved "
            f"to Cool tier (>{self.cool_tier_days} days) or Archive tier (>{self.archive_tier_days} days)"
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
                # Get storage account info including blob inventory
                storage_info = await provider.get_storage_info(resource.id, resource.region)
                
                # Check if lifecycle policies are already configured
                if storage_info.get("has_lifecycle_policies"):
                    continue
                
                # Get access tier distribution
                tier_distribution = storage_info.get("tier_distribution", {})
                total_size_gb = sum(tier_distribution.get(tier, {}).get("size_gb", 0) 
                                  for tier in ["hot", "cool", "archive"])
                
                if total_size_gb == 0:
                    continue
                
                # Analyze access patterns
                access_patterns = storage_info.get("access_patterns", {})
                
                # Calculate data eligible for tiering
                cool_eligible_gb = 0
                archive_eligible_gb = 0
                
                # Check Hot tier data for tiering opportunities
                hot_data = tier_distribution.get("hot", {})
                hot_size_gb = hot_data.get("size_gb", 0)
                
                if hot_size_gb > 0:
                    # Analyze last access times
                    for days_range, size_gb in access_patterns.items():
                        if "+" in days_range:  # e.g., "180+"
                            days = int(days_range.replace("+", ""))
                            if days >= self.archive_tier_days:
                                archive_eligible_gb += size_gb
                            elif days >= self.cool_tier_days:
                                cool_eligible_gb += size_gb
                        elif "-" in days_range:  # e.g., "30-90"
                            start, end = map(int, days_range.split("-"))
                            if start >= self.cool_tier_days:
                                cool_eligible_gb += size_gb
                
                # Skip if no tiering opportunities
                if cool_eligible_gb == 0 and archive_eligible_gb == 0:
                    continue
                
                # Calculate savings
                hot_cost_per_gb = Decimal("0.0184")  # Approximate Hot tier cost per GB
                cool_cost_per_gb = Decimal("0.01")   # Approximate Cool tier cost per GB
                archive_cost_per_gb = Decimal("0.00099")  # Approximate Archive tier cost per GB
                
                current_hot_cost = Decimal(hot_size_gb) * hot_cost_per_gb
                
                # Calculate optimized costs
                optimized_hot_gb = hot_size_gb - cool_eligible_gb - archive_eligible_gb
                optimized_cost = (
                    Decimal(optimized_hot_gb) * hot_cost_per_gb +
                    Decimal(cool_eligible_gb) * cool_cost_per_gb +
                    Decimal(archive_eligible_gb) * archive_cost_per_gb
                )
                
                monthly_savings = current_hot_cost - optimized_cost
                annual_savings = monthly_savings * 12
                
                if monthly_savings < Decimal("10"):
                    continue
                
                # Calculate percentage savings
                savings_percentage = float((monthly_savings / current_hot_cost) * 100) if current_hot_cost > 0 else 0
                
                # Determine severity
                severity = self._calculate_severity(monthly_savings)
                
                result = CheckResult(
                    id=f"storage-lifecycle-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Storage Lifecycle Opportunity: {resource.name}",
                    description=(
                        f"Storage account has {cool_eligible_gb:.1f} GB eligible for Cool tier "
                        f"and {archive_eligible_gb:.1f} GB eligible for Archive tier. "
                        f"Total size: {total_size_gb:.1f} GB"
                    ),
                    impact=(
                        "Implementing lifecycle management policies can automatically move data to "
                        "cheaper tiers based on access patterns. Cool tier is ideal for data accessed "
                        "monthly, Archive tier for yearly access or compliance storage."
                    ),
                    current_cost=current_hot_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=savings_percentage,
                    effort_level="low",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review data access patterns to confirm tiering eligibility",
                        "2. Navigate to Storage Account > Lifecycle Management in Azure Portal",
                        "3. Create rule: Move to Cool after 30 days without access",
                        "4. Create rule: Move to Archive after 180 days without access",
                        "5. Optional: Delete blobs after specific period (e.g., 2 years)",
                        "6. Enable versioning if not already enabled for data protection",
                        "7. Monitor tier transitions and access patterns",
                        "8. Note: Archive tier has early deletion fees and rehydration costs",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "total_size_gb": round(total_size_gb, 2),
                        "hot_size_gb": round(hot_size_gb, 2),
                        "cool_eligible_gb": round(cool_eligible_gb, 2),
                        "archive_eligible_gb": round(archive_eligible_gb, 2),
                        "has_lifecycle_policies": False,
                        "storage_account_kind": storage_info.get("account_kind", "StorageV2"),
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check storage lifecycle for {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > Decimal("500"):
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM