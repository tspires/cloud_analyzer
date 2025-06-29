"""Check for Azure SQL Database serverless tier opportunities."""

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


class AzureSQLServerlessTierCheck(Check):
    """Check for SQL Database serverless tier opportunities.
    
    Serverless compute tier automatically pauses databases during inactive periods
    and resumes when activity returns. Ideal for intermittent, unpredictable workloads.
    
    Attributes:
        activity_hours_threshold: Max active hours per day for serverless recommendation
        cpu_variance_threshold: CPU usage variance threshold
    """
    
    def __init__(
        self,
        activity_hours_threshold: int = 12,
        cpu_variance_threshold: float = 50.0
    ) -> None:
        """Initialize the check.
        
        Args:
            activity_hours_threshold: Max active hours/day for serverless
            cpu_variance_threshold: Min CPU variance for serverless benefit
        """
        self.activity_hours_threshold = activity_hours_threshold
        self.cpu_variance_threshold = cpu_variance_threshold
        self.logger = logging.getLogger(__name__)
        
        # Serverless can save 60-90% for appropriate workloads
        self.serverless_savings_percent = 60
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.RIGHT_SIZING
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure SQL Serverless Tier Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies provisioned SQL databases with <{self.activity_hours_threshold} active hours/day "
            "that could benefit from serverless compute tier with auto-pause"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only provisioned Azure SQL databases."""
        return [
            r for r in resources
            if r.type == ResourceType.DATABASE 
            and r.provider == CloudProvider.AZURE
            and r.is_active
            and r.metadata.get("tier") not in ["Serverless", "Hyperscale", "Basic"]  # Already serverless or not supported
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
            
            # Skip if database is too large (serverless has size limits)
            if resource.metadata.get("max_size_gb", 0) > 1024:  # 1TB limit
                continue
            
            try:
                # Get database metrics and activity patterns
                metrics = await provider.get_database_metrics(
                    resource.id, 
                    resource.region, 
                    days=30
                )
                
                db_info = await provider.get_database_info(resource.id, resource.region)
                
                # Analyze activity patterns
                activity_hours = db_info.get("avg_daily_active_hours", 24)
                cpu_variance = metrics.get("cpu_variance", 0)
                avg_cpu = metrics.get("avg_cpu_percent", 100)
                connection_pattern = db_info.get("connection_pattern", "continuous")
                
                # Check if suitable for serverless
                if activity_hours >= self.activity_hours_threshold:
                    continue
                
                # High CPU variance indicates burst workloads (good for serverless)
                if cpu_variance < self.cpu_variance_threshold and connection_pattern == "continuous":
                    continue
                
                # Check environment
                environment = "production"
                if resource.tags:
                    env_tag = resource.tags.get("environment", "").lower()
                    if env_tag in ["dev", "test", "staging", "qa"]:
                        environment = env_tag
                
                # Calculate potential savings
                # Serverless saves more for databases with fewer active hours
                inactive_hours = 24 - activity_hours
                actual_savings_percent = min(
                    self.serverless_savings_percent * (inactive_hours / 24),
                    80  # Cap at 80% savings
                )
                
                monthly_savings = resource.monthly_cost * Decimal(actual_savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                # Only report significant savings
                if monthly_savings < Decimal("30"):
                    continue
                
                # Determine severity
                severity = self._calculate_severity(monthly_savings, environment, activity_hours)
                
                # Adjust confidence based on workload
                confidence = DEFAULT_CHECK_CONFIDENCE
                if environment in ["dev", "test"]:
                    confidence *= 0.95
                elif activity_hours < 4:
                    confidence *= 0.9
                else:
                    confidence *= 0.85
                
                result = CheckResult(
                    id=f"sql-serverless-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Serverless Tier Opportunity: {resource.name}",
                    description=(
                        f"Database active only {activity_hours:.1f} hours/day with "
                        f"{cpu_variance:.0f}% CPU variance. Current tier: {resource.metadata.get('tier')}. "
                        f"Environment: {environment}"
                    ),
                    impact=(
                        f"This database shows intermittent usage patterns ideal for serverless compute. "
                        f"Serverless auto-pauses after 1 hour of inactivity, stopping compute charges. "
                        f"It auto-resumes within seconds on new connections. "
                        f"Perfect for {environment} workloads with variable or unpredictable usage."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float(actual_savings_percent),
                    effort_level="low",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review database workload patterns and peak usage requirements",
                        "2. Ensure applications handle connection retry (for auto-resume)",
                        "3. In Azure Portal: SQL Database > Compute + storage",
                        "4. Change service tier to 'General Purpose - Serverless'",
                        "5. Configure serverless settings:",
                        f"   - Min vCores: 0.5 (allows full pause)",
                        f"   - Max vCores: {self._get_serverless_vcores(resource.metadata.get('sku', 'S1'))}",
                        "   - Auto-pause delay: 1 hour (minimum)",
                        "6. Apply changes (requires brief downtime)",
                        "7. Monitor first resume times (typically 20-30 seconds)",
                        "8. Adjust min/max vCores based on performance needs",
                    ],
                    confidence_score=confidence,
                    check_metadata={
                        "current_tier": resource.metadata.get("tier"),
                        "current_sku": resource.metadata.get("sku"),
                        "avg_daily_active_hours": round(activity_hours, 1),
                        "cpu_variance_percent": round(cpu_variance, 1),
                        "avg_cpu_percent": round(avg_cpu, 1),
                        "connection_pattern": connection_pattern,
                        "environment": environment,
                        "max_size_gb": resource.metadata.get("max_size_gb", 0),
                        "serverless_suitable": True,
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check serverless opportunity for {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _get_serverless_vcores(self, current_sku: str) -> int:
        """Map current SKU to recommended serverless max vCores."""
        # Map DTU-based SKUs to vCores
        sku_to_vcores = {
            "S0": 1,
            "S1": 1,
            "S2": 2,
            "S3": 4,
            "S4": 8,
            "S6": 12,
            "S7": 16,
            "S9": 20,
            "S12": 24,
            "P1": 8,
            "P2": 16,
            "P4": 24,
            "P6": 32,
        }
        
        # If already vCore-based
        if "Gen5" in current_sku:
            try:
                return int(current_sku.split("_")[-1])
            except:
                return 4
        
        return sku_to_vcores.get(current_sku, 4)
    
    def _calculate_severity(
        self, 
        monthly_savings: Decimal, 
        environment: str,
        activity_hours: float
    ) -> CheckSeverity:
        """Calculate severity based on savings and usage patterns."""
        if environment in ["dev", "test"] and activity_hours < 6:
            return CheckSeverity.HIGH
        elif monthly_savings > Decimal("500"):
            return CheckSeverity.HIGH
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.MEDIUM
        else:
            return CheckSeverity.LOW