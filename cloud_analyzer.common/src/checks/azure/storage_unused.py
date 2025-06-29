"""Check for unused or empty Azure Storage accounts."""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    DEFAULT_CHECK_CONFIDENCE,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class AzureUnusedStorageCheck(Check):
    """Check for unused or empty Azure Storage accounts.
    
    Identifies storage accounts that are empty or have very low usage,
    which can be deleted to save on the base storage account charges.
    
    Attributes:
        min_days_empty: Minimum days account must be empty/low usage
        size_threshold_gb: Size below which account is considered "empty"
    """
    
    def __init__(
        self, 
        min_days_empty: int = 30,
        size_threshold_gb: float = 1.0
    ) -> None:
        """Initialize the check.
        
        Args:
            min_days_empty: Minimum days of being empty/low usage
            size_threshold_gb: Size threshold to consider "empty"
        """
        self.min_days_empty = min_days_empty
        self.size_threshold_gb = size_threshold_gb
        self.logger = logging.getLogger(__name__)
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.IDLE_RESOURCE
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure Unused Storage Account Detection"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies storage accounts that are empty or contain less than {self.size_threshold_gb} GB "
            f"of data for {self.min_days_empty}+ days"
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
                
                total_size_gb = storage_info.get("total_size_gb", 0)
                container_count = storage_info.get("container_count", 0)
                
                # Check if account is essentially empty
                if total_size_gb > self.size_threshold_gb:
                    continue
                
                # Get transaction metrics to see if it's being used
                transaction_count = storage_info.get("monthly_transactions", 0)
                last_modified = storage_info.get("last_modified_date")
                
                # Calculate days since last modification
                days_inactive = self.min_days_empty  # Default
                if last_modified:
                    if isinstance(last_modified, str):
                        last_modified = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
                    days_inactive = (datetime.now(timezone.utc) - last_modified).days
                
                # Skip if recently active
                if days_inactive < self.min_days_empty:
                    continue
                
                # Skip if there's significant transaction activity
                if transaction_count > 1000:  # More than 1000 transactions per month suggests active use
                    continue
                
                # Storage accounts have a base cost regardless of data stored
                # Estimate base cost (varies by redundancy and features)
                base_monthly_cost = Decimal("5")  # Conservative estimate
                if resource.monthly_cost > base_monthly_cost:
                    monthly_savings = base_monthly_cost
                else:
                    monthly_savings = resource.monthly_cost
                
                annual_savings = monthly_savings * 12
                
                # Determine severity based on various factors
                if total_size_gb == 0 and container_count == 0:
                    severity = CheckSeverity.HIGH
                    description = "Storage account is completely empty"
                elif total_size_gb < 0.001:  # Less than 1 MB
                    severity = CheckSeverity.HIGH
                    description = f"Storage account contains only {total_size_gb*1000:.2f} MB of data"
                else:
                    severity = CheckSeverity.MEDIUM
                    description = f"Storage account contains only {total_size_gb:.2f} GB of data"
                
                result = CheckResult(
                    id=f"storage-unused-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Unused Storage Account: {resource.name}",
                    description=(
                        f"{description} and has been inactive for {days_inactive} days. "
                        f"Containers: {container_count}, Monthly transactions: {transaction_count}"
                    ),
                    impact=(
                        "Empty or nearly empty storage accounts still incur base charges for the account itself. "
                        "If this storage is no longer needed, deleting it can eliminate these recurring costs. "
                        "Ensure any important data is backed up before deletion."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=Decimal("0"),
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=100.0,
                    effort_level="low",
                    risk_level="low" if total_size_gb == 0 else "medium",
                    implementation_steps=[
                        "1. Verify the storage account is truly not needed",
                        "2. Check for any automation or applications using the account",
                        "3. If data exists, review and backup if needed",
                        "4. Check for any dependent resources (e.g., VMs using diagnostics)",
                        "5. Delete storage account in Azure Portal or CLI",
                        "6. Azure CLI: az storage account delete --name <name> --resource-group <rg>",
                        "7. Confirm deletion (this action cannot be undone)",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE * (0.95 if total_size_gb == 0 else 0.85),
                    check_metadata={
                        "total_size_gb": round(total_size_gb, 4),
                        "container_count": container_count,
                        "days_inactive": days_inactive,
                        "monthly_transactions": transaction_count,
                        "redundancy": storage_info.get("redundancy", "unknown"),
                        "account_kind": storage_info.get("account_kind", "StorageV2"),
                        "has_lifecycle_policies": storage_info.get("has_lifecycle_policies", False),
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check unused storage for {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        # For unused resources, severity is more about the waste than the amount
        return CheckSeverity.HIGH