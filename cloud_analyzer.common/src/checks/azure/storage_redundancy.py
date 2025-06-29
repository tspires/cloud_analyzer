"""Check for Azure Storage redundancy optimization opportunities."""

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


class AzureStorageRedundancyCheck(Check):
    """Check for Azure Storage redundancy optimization opportunities.
    
    Azure offers multiple redundancy options: LRS, ZRS, GRS, RA-GRS, GZRS, RA-GZRS.
    Many non-critical workloads can use LRS (Locally Redundant Storage) instead of
    geo-redundant options for significant cost savings.
    """
    
    def __init__(self) -> None:
        """Initialize the check."""
        self.logger = logging.getLogger(__name__)
        
        # Relative costs (LRS = 1.0)
        self.redundancy_cost_multipliers = {
            "LRS": 1.0,      # Locally redundant storage (3 copies in 1 datacenter)
            "ZRS": 1.25,     # Zone redundant storage (3 copies across zones)
            "GRS": 2.0,      # Geo-redundant storage (6 copies, 2 regions)
            "RA-GRS": 2.5,   # Read-access geo-redundant storage
            "GZRS": 2.5,     # Geo-zone-redundant storage
            "RA-GZRS": 3.125 # Read-access geo-zone-redundant storage
        }
        
        # Patterns indicating non-critical data
        self.non_critical_patterns = [
            "dev", "test", "temp", "staging", "backup", "archive",
            "log", "diagnostic", "metric", "telemetry", "sandbox"
        ]
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.STORAGE_TIER
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure Storage Redundancy Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            "Identifies storage accounts using expensive geo-redundant storage "
            "for non-critical workloads that could use locally redundant storage"
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
    
    def _is_non_critical(self, resource: Resource, storage_info: dict) -> bool:
        """Determine if storage account likely contains non-critical data."""
        # Check resource name
        name_lower = resource.name.lower()
        for pattern in self.non_critical_patterns:
            if pattern in name_lower:
                return True
        
        # Check tags
        if resource.tags:
            env_tag = resource.tags.get("environment", "").lower()
            if env_tag in ["dev", "test", "staging", "qa", "development"]:
                return True
            
            criticality_tag = resource.tags.get("criticality", "").lower()
            if criticality_tag in ["low", "non-critical"]:
                return True
        
        # Check container names
        container_names = storage_info.get("container_names", [])
        for container in container_names:
            for pattern in self.non_critical_patterns:
                if pattern in container.lower():
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
                # Get storage account details
                storage_info = await provider.get_storage_info(resource.id, resource.region)
                
                current_redundancy = storage_info.get("redundancy", "LRS").upper()
                
                # Skip if already using LRS
                if current_redundancy == "LRS":
                    continue
                
                # Check if it's non-critical data
                is_non_critical = self._is_non_critical(resource, storage_info)
                
                # For critical data, only suggest downgrading from RA- variants
                if not is_non_critical and not current_redundancy.startswith("RA-"):
                    continue
                
                # Determine recommended redundancy
                if is_non_critical:
                    recommended_redundancy = "LRS"
                elif current_redundancy.startswith("RA-"):
                    # Downgrade from read-access to regular geo-redundant
                    recommended_redundancy = current_redundancy.replace("RA-", "")
                else:
                    continue
                
                # Calculate savings
                current_multiplier = self.redundancy_cost_multipliers.get(current_redundancy, 2.0)
                recommended_multiplier = self.redundancy_cost_multipliers.get(recommended_redundancy, 1.0)
                
                savings_percent = ((current_multiplier - recommended_multiplier) / current_multiplier) * 100
                
                monthly_savings = resource.monthly_cost * Decimal(savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                if monthly_savings < Decimal("10"):
                    continue
                
                # Determine severity
                severity = self._calculate_severity(monthly_savings)
                
                result = CheckResult(
                    id=f"storage-redundancy-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Storage Redundancy Optimization: {resource.name}",
                    description=(
                        f"Storage account using {current_redundancy} redundancy. "
                        f"Could switch to {recommended_redundancy} for {savings_percent:.0f}% savings. "
                        f"Storage size: {storage_info.get('total_size_gb', 0):.1f} GB"
                    ),
                    impact=(
                        f"{'This appears to be non-critical data that' if is_non_critical else 'This storage has read-access geo-redundancy which'} "
                        f"may not require {current_redundancy} level redundancy. "
                        f"{recommended_redundancy} provides {'3 copies within a single datacenter' if recommended_redundancy == 'LRS' else 'geo-redundancy without read access'}, "
                        "which is sufficient for many workloads."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=savings_percent,
                    effort_level="low",
                    risk_level="medium" if is_non_critical else "low",
                    implementation_steps=[
                        "1. Verify data criticality and backup requirements",
                        "2. Ensure you have backups if downgrading redundancy",
                        "3. Plan for a maintenance window (brief unavailability during change)",
                        f"4. In Azure Portal: Storage Account > Configuration > Replication = {recommended_redundancy}",
                        f"5. Or Azure CLI: az storage account update --name <name> --sku Standard_{recommended_redundancy}",
                        "6. Monitor for any issues after the change",
                        "7. Document the redundancy level for disaster recovery planning",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE * (0.9 if is_non_critical else 0.8),
                    check_metadata={
                        "current_redundancy": current_redundancy,
                        "recommended_redundancy": recommended_redundancy,
                        "is_non_critical": is_non_critical,
                        "total_size_gb": storage_info.get("total_size_gb", 0),
                        "account_kind": storage_info.get("account_kind", "StorageV2"),
                        "indicators": {
                            "name_match": any(p in resource.name.lower() for p in self.non_critical_patterns),
                            "tag_match": bool(resource.tags.get("environment", "").lower() in ["dev", "test", "staging"]),
                        }
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check storage redundancy for {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > Decimal("200"):
            return CheckSeverity.HIGH
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.MEDIUM
        else:
            return CheckSeverity.LOW