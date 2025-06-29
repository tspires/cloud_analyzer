"""Check for Azure VMs not using Azure Hybrid Benefit."""

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


class AzureVMHybridBenefitCheck(Check):
    """Check for Azure VMs that could benefit from Azure Hybrid Benefit.
    
    Azure Hybrid Benefit allows customers with Software Assurance to use their
    on-premises Windows Server and SQL Server licenses in Azure, providing up to
    40% savings on Windows VMs and up to 55% on SQL Server.
    """
    
    def __init__(self) -> None:
        """Initialize the check."""
        self.logger = logging.getLogger(__name__)
        # Approximate savings percentages
        self.windows_savings_percent = 40
        self.sql_savings_percent = 55
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.LICENSE_OPTIMIZATION
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure Hybrid Benefit Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            "Identifies Azure VMs running Windows or SQL Server that are not using "
            "Azure Hybrid Benefit, which could provide significant license cost savings"
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
            
            # Skip if VM is not running
            if resource.state.lower() != "succeeded" or not resource.is_active:
                continue
            
            try:
                # Check if VM is running Windows
                os_type = resource.metadata.get("os_type", "").lower()
                if os_type != "windows":
                    continue
                
                # Get detailed VM info to check for hybrid benefit
                vm_info = await provider.get_instance_info(resource.id, resource.region)
                
                # Check if hybrid benefit is already enabled
                license_type = vm_info.get("license_type", "").lower()
                if license_type in ["windows_server", "windows_client"]:
                    continue  # Already using hybrid benefit
                
                # Check for SQL Server
                has_sql_server = False
                vm_size = resource.metadata.get("vm_size", "").lower()
                # SQL Server VMs typically have specific naming patterns
                if "sql" in vm_size or vm_info.get("has_sql_server", False):
                    has_sql_server = True
                
                # Calculate potential savings
                savings_percent = self.sql_savings_percent if has_sql_server else self.windows_savings_percent
                monthly_savings = resource.monthly_cost * Decimal(savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                # Only report if savings are significant
                if monthly_savings < Decimal("10"):
                    continue
                
                # Determine severity based on savings
                severity = self._calculate_severity(monthly_savings)
                
                license_type_str = "SQL Server" if has_sql_server else "Windows Server"
                
                result = CheckResult(
                    id=f"vm-hybrid-benefit-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Azure Hybrid Benefit Not Enabled: {resource.name}",
                    description=(
                        f"{license_type_str} VM not using Azure Hybrid Benefit. "
                        f"Size: {resource.metadata.get('vm_size', 'Unknown')}, "
                        f"Potential savings: {savings_percent}%"
                    ),
                    impact=(
                        f"Azure Hybrid Benefit can reduce {license_type_str} VM costs by up to {savings_percent}% "
                        "for customers with Software Assurance. This benefit allows you to use existing "
                        "on-premises licenses in Azure."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float(savings_percent),
                    effort_level="low",
                    risk_level="low",
                    implementation_steps=[
                        "1. Verify you have eligible Software Assurance licenses",
                        "2. Count the number of licenses needed (1 license = up to 8 vCPUs)",
                        "3. Enable Azure Hybrid Benefit in Azure Portal VM settings",
                        "4. Or use Azure CLI: az vm update --resource-group <rg> --name <vm> --license-type Windows_Server",
                        "5. The change takes effect immediately with no VM restart required",
                        "6. Track license usage in Azure Portal to ensure compliance",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE * 0.9,  # Slightly lower as we assume eligibility
                    check_metadata={
                        "os_type": os_type,
                        "vm_size": resource.metadata.get("vm_size"),
                        "current_license_type": license_type or "none",
                        "license_type_recommended": license_type_str,
                        "has_sql_server": has_sql_server,
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check VM hybrid benefit for {resource.id}: {str(e)}"
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