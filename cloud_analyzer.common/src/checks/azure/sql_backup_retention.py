"""Check for Azure SQL Database backup retention optimization."""

import logging
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    DEFAULT_CHECK_CONFIDENCE,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class AzureSQLBackupRetentionCheck(Check):
    """Check for SQL Database backup retention optimization opportunities.
    
    Azure SQL Database includes automated backups with configurable retention.
    Long-term retention (LTR) beyond the default can significantly increase costs.
    This check identifies over-provisioned backup retention.
    """
    
    def __init__(self) -> None:
        """Initialize the check."""
        self.logger = logging.getLogger(__name__)
        
        # Default retention recommendations by environment
        self.retention_recommendations = {
            "production": {"pitr_days": 7, "ltr_weekly": 4, "ltr_monthly": 12, "ltr_yearly": 5},
            "staging": {"pitr_days": 7, "ltr_weekly": 2, "ltr_monthly": 3, "ltr_yearly": 0},
            "development": {"pitr_days": 1, "ltr_weekly": 0, "ltr_monthly": 0, "ltr_yearly": 0},
            "test": {"pitr_days": 1, "ltr_weekly": 0, "ltr_monthly": 0, "ltr_yearly": 0},
        }
        
        # Cost per GB for LTR (approximate)
        self.ltr_cost_per_gb_month = Decimal("0.05")
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.BACKUP_RETENTION
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure SQL Backup Retention Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            "Identifies SQL databases with excessive backup retention periods "
            "that could be reduced based on environment and compliance requirements"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only Azure SQL databases."""
        return [
            r for r in resources
            if r.type == ResourceType.DATABASE 
            and r.provider == CloudProvider.AZURE
            and r.is_active
        ]
    
    def _get_environment(self, resource: Resource) -> str:
        """Determine environment from tags and naming."""
        # Check tags first
        if resource.tags:
            env_tag = resource.tags.get("environment", "").lower()
            if env_tag in self.retention_recommendations:
                return env_tag
        
        # Check name patterns
        name_lower = resource.name.lower()
        for env in ["dev", "test", "stg", "staging"]:
            if env in name_lower:
                return "development" if env in ["dev", "test"] else "staging"
        
        return "production"  # Default to production for safety
    
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
                # Get database backup configuration
                db_info = await provider.get_database_info(resource.id, resource.region)
                
                # Get current retention settings
                current_pitr_days = db_info.get("pitr_retention_days", 7)
                current_ltr_config = db_info.get("ltr_config", {})
                
                # Current LTR settings
                current_ltr_weekly = current_ltr_config.get("weekly_retention", 0)
                current_ltr_monthly = current_ltr_config.get("monthly_retention", 0)
                current_ltr_yearly = current_ltr_config.get("yearly_retention", 0)
                
                # Determine environment and recommendations
                environment = self._get_environment(resource)
                recommended = self.retention_recommendations[environment]
                
                # Check if any retention is excessive
                excessive_retention = []
                
                if current_pitr_days > recommended["pitr_days"]:
                    excessive_retention.append(
                        f"PITR: {current_pitr_days} days (recommended: {recommended['pitr_days']})"
                    )
                
                if current_ltr_weekly > recommended["ltr_weekly"]:
                    excessive_retention.append(
                        f"Weekly LTR: {current_ltr_weekly} weeks (recommended: {recommended['ltr_weekly']})"
                    )
                
                if current_ltr_monthly > recommended["ltr_monthly"]:
                    excessive_retention.append(
                        f"Monthly LTR: {current_ltr_monthly} months (recommended: {recommended['ltr_monthly']})"
                    )
                
                if current_ltr_yearly > recommended["ltr_yearly"]:
                    excessive_retention.append(
                        f"Yearly LTR: {current_ltr_yearly} years (recommended: {recommended['ltr_yearly']})"
                    )
                
                if not excessive_retention:
                    continue
                
                # Estimate savings
                # PITR savings (included in base price up to 7 days)
                pitr_extra_days = max(0, current_pitr_days - 7)
                pitr_savings = Decimal("0")
                if pitr_extra_days > 0 and current_pitr_days > recommended["pitr_days"]:
                    # Estimate 5% of database cost per extra week
                    pitr_savings = resource.monthly_cost * Decimal("0.05") * Decimal(pitr_extra_days) / Decimal("7")
                
                # LTR savings estimation
                db_size_gb = resource.metadata.get("max_size_gb", 10)
                
                # Calculate retention reduction in months
                current_retention_months = (
                    current_ltr_weekly / 4 +
                    current_ltr_monthly +
                    current_ltr_yearly * 12
                )
                recommended_retention_months = (
                    recommended["ltr_weekly"] / 4 +
                    recommended["ltr_monthly"] +
                    recommended["ltr_yearly"] * 12
                )
                
                retention_reduction_months = max(0, current_retention_months - recommended_retention_months)
                ltr_savings = Decimal(str(db_size_gb)) * self.ltr_cost_per_gb_month * Decimal(str(retention_reduction_months))
                
                monthly_savings = pitr_savings + ltr_savings
                
                # Skip if savings are minimal
                if monthly_savings < Decimal("5"):
                    continue
                
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                # Determine severity
                if environment in ["development", "test"] and current_ltr_yearly > 0:
                    severity = CheckSeverity.HIGH
                elif monthly_savings > Decimal("100"):
                    severity = CheckSeverity.MEDIUM
                else:
                    severity = CheckSeverity.LOW
                
                result = CheckResult(
                    id=f"sql-backup-retention-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Excessive Backup Retention: {resource.name}",
                    description=(
                        f"{environment.title()} database with excessive retention: "
                        f"{', '.join(excessive_retention)}. "
                        f"Database size: {db_size_gb} GB"
                    ),
                    impact=(
                        f"This {environment} database has backup retention beyond typical requirements. "
                        "Reducing retention to recommended levels can save on storage costs while maintaining "
                        "adequate recovery capabilities. Ensure retention meets your compliance requirements."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float((monthly_savings / resource.monthly_cost) * 100) if resource.monthly_cost > 0 else 0,
                    effort_level="low",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review compliance and business requirements for backup retention",
                        "2. Document any regulatory requirements that mandate specific retention",
                        "3. In Azure Portal: SQL Database > Backups > Retention policies",
                        f"4. Adjust PITR retention to {recommended['pitr_days']} days for {environment}",
                        "5. Configure LTR policies:",
                        f"   - Weekly: {recommended['ltr_weekly']} weeks",
                        f"   - Monthly: {recommended['ltr_monthly']} months",
                        f"   - Yearly: {recommended['ltr_yearly']} years",
                        "6. Apply changes (no downtime required)",
                        "7. Document the retention policy for compliance",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "environment": environment,
                        "current_pitr_days": current_pitr_days,
                        "current_ltr_weekly": current_ltr_weekly,
                        "current_ltr_monthly": current_ltr_monthly,
                        "current_ltr_yearly": current_ltr_yearly,
                        "recommended_pitr_days": recommended["pitr_days"],
                        "recommended_ltr_weekly": recommended["ltr_weekly"],
                        "recommended_ltr_monthly": recommended["ltr_monthly"],
                        "recommended_ltr_yearly": recommended["ltr_yearly"],
                        "database_size_gb": db_size_gb,
                        "excessive_policies": excessive_retention,
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check backup retention for {resource.id}: {str(e)}"
                )
                continue
        
        return results