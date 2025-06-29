"""Check for Azure SQL Database geo-replication optimization."""

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


class AzureSQLGeoReplicationCheck(Check):
    """Check for SQL Database geo-replication optimization opportunities.
    
    Active geo-replication creates readable secondary databases in other regions,
    doubling costs. This check identifies non-critical databases with geo-replication
    that might not need it.
    """
    
    def __init__(self) -> None:
        """Initialize the check."""
        self.logger = logging.getLogger(__name__)
        
        # Geo-replication typically doubles the cost
        self.geo_replication_cost_multiplier = 2.0
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.MULTI_AZ_OVERUSE
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure SQL Geo-Replication Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            "Identifies non-production SQL databases with active geo-replication "
            "that may not require this level of disaster recovery"
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
    
    def _is_critical_database(self, resource: Resource, db_info: dict) -> bool:
        """Determine if database is critical and needs geo-replication."""
        # Check tags
        if resource.tags:
            criticality = resource.tags.get("criticality", "").lower()
            if criticality in ["high", "critical"]:
                return True
            
            env_tag = resource.tags.get("environment", "").lower()
            if env_tag in ["dev", "test", "staging", "qa"]:
                return False
        
        # Check name patterns
        name_lower = resource.name.lower()
        for pattern in ["dev", "test", "stg", "staging", "qa", "demo", "sandbox"]:
            if pattern in name_lower:
                return False
        
        # Check size and tier
        if resource.metadata.get("tier") == "Basic":
            return False
        
        if resource.metadata.get("max_size_gb", 0) < 50:  # Small database
            return False
        
        # Default to critical for production databases
        return True
    
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
                # Get database information including replication status
                db_info = await provider.get_database_info(resource.id, resource.region)
                
                # Check if geo-replication is enabled
                geo_replicas = db_info.get("geo_replicas", [])
                if not geo_replicas:
                    continue
                
                # Check if this is a critical database
                is_critical = self._is_critical_database(resource, db_info)
                if is_critical:
                    continue
                
                # Calculate cost of geo-replication
                # Each replica costs approximately the same as the primary
                replica_count = len(geo_replicas)
                replica_cost = resource.monthly_cost * Decimal(replica_count)
                
                # Potential savings by removing geo-replication
                monthly_savings = replica_cost
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost
                
                # Skip if savings are minimal
                if monthly_savings < Decimal("50"):
                    continue
                
                # Determine environment
                environment = "production"
                if resource.tags:
                    env_tag = resource.tags.get("environment", "").lower()
                    if env_tag:
                        environment = env_tag
                
                # Determine severity
                if environment in ["dev", "test"] and replica_count > 0:
                    severity = CheckSeverity.HIGH
                elif monthly_savings > Decimal("500"):
                    severity = CheckSeverity.HIGH
                else:
                    severity = CheckSeverity.MEDIUM
                
                # Build replica details
                replica_details = []
                for replica in geo_replicas:
                    replica_details.append(
                        f"{replica.get('region', 'unknown')} ({replica.get('status', 'unknown')})"
                    )
                
                result = CheckResult(
                    id=f"sql-geo-replication-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Unnecessary Geo-Replication: {resource.name}",
                    description=(
                        f"{environment.title()} database with {replica_count} geo-replica(s): "
                        f"{', '.join(replica_details)}. "
                        f"Database size: {resource.metadata.get('max_size_gb', 0)} GB"
                    ),
                    impact=(
                        f"This {environment} database has active geo-replication which doubles the cost. "
                        "For non-production environments, geo-replication is typically unnecessary. "
                        "Consider using automated backups with geo-redundant storage instead, "
                        "which provides disaster recovery at a fraction of the cost."
                    ),
                    current_cost=resource.monthly_cost + replica_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=50.0,  # Geo-replication typically doubles cost
                    effort_level="low",
                    risk_level="medium" if environment == "production" else "low",
                    implementation_steps=[
                        "1. Verify this database doesn't require real-time DR",
                        "2. Ensure automated backups are configured with geo-redundancy",
                        "3. Document the decision to remove geo-replication",
                        "4. Remove each secondary replica:",
                        "   - In Azure Portal: SQL Database > Replicas",
                        "   - Select each replica and click 'Delete'",
                        "   - Or use Azure CLI: az sql db replica delete",
                        "5. Verify primary database remains accessible",
                        "6. Test backup restoration procedure",
                        "7. Consider geo-replication only for truly critical databases",
                        "8. For read scaling, consider read replicas in the same region",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE * (0.95 if environment != "production" else 0.8),
                    check_metadata={
                        "environment": environment,
                        "is_critical": is_critical,
                        "replica_count": replica_count,
                        "replica_regions": [r.get("region") for r in geo_replicas],
                        "replica_cost_monthly": float(replica_cost),
                        "database_tier": resource.metadata.get("tier"),
                        "database_size_gb": resource.metadata.get("max_size_gb", 0),
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check geo-replication for {resource.id}: {str(e)}"
                )
                continue
        
        return results