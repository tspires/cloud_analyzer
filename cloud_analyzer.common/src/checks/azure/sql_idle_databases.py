"""Check for idle or underutilized Azure SQL Databases."""

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


class AzureSQLIdleDatabaseCheck(Check):
    """Check for idle or underutilized Azure SQL Databases.
    
    Identifies SQL databases with very low activity that could be paused,
    deleted, or moved to serverless tier for cost savings.
    
    Attributes:
        cpu_threshold: CPU usage threshold to consider idle
        connection_threshold: Daily connection threshold
        days_to_analyze: Number of days to analyze metrics
    """
    
    def __init__(
        self,
        cpu_threshold: float = 5.0,
        connection_threshold: int = 10,
        days_to_analyze: int = 14
    ) -> None:
        """Initialize the check.
        
        Args:
            cpu_threshold: Max avg CPU to consider idle
            connection_threshold: Max daily connections to consider idle
            days_to_analyze: Days of metrics to analyze
        """
        self.cpu_threshold = cpu_threshold
        self.connection_threshold = connection_threshold
        self.days_to_analyze = days_to_analyze
        self.logger = logging.getLogger(__name__)
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.IDLE_DATABASE
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure SQL Idle Database Detection"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies SQL databases with <{self.cpu_threshold}% CPU usage and "
            f"<{self.connection_threshold} daily connections over {self.days_to_analyze} days"
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
                # Get database metrics
                metrics = await provider.get_database_metrics(
                    resource.id, 
                    resource.region, 
                    days=self.days_to_analyze
                )
                
                # Get database info for connection count
                db_info = await provider.get_database_info(resource.id, resource.region)
                
                avg_cpu = metrics.get("avg_cpu_percent", 100)
                avg_connections = db_info.get("avg_daily_connections", 100)
                max_cpu = metrics.get("max_cpu_percent", 100)
                
                # Check if database is idle
                if avg_cpu >= self.cpu_threshold:
                    continue
                
                if avg_connections >= self.connection_threshold:
                    continue
                
                # Determine recommendation based on usage pattern
                if avg_cpu < 1 and avg_connections < 1:
                    recommendation = "delete"
                    savings_percent = 100
                    effort = "low"
                    risk = "medium"
                elif resource.metadata.get("tier") != "Serverless":
                    recommendation = "serverless"
                    savings_percent = 70  # Serverless can save up to 70%
                    effort = "low"
                    risk = "low"
                else:
                    recommendation = "pause"
                    savings_percent = 90  # Pausing saves most costs
                    effort = "low"
                    risk = "low"
                
                # Calculate savings
                monthly_savings = resource.monthly_cost * Decimal(savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = resource.monthly_cost - monthly_savings
                
                # Determine severity
                severity = self._calculate_severity(monthly_savings, avg_cpu)
                
                # Build recommendation steps
                if recommendation == "delete":
                    steps = [
                        "1. Verify database is truly not needed",
                        "2. Take a final backup using Azure Portal or CLI",
                        "3. Export data if needed for compliance",
                        "4. Check for any dependent applications",
                        "5. Delete the database",
                        "6. Delete the server if no other databases exist",
                    ]
                    title = f"Idle Database - Consider Deletion: {resource.name}"
                elif recommendation == "serverless":
                    steps = [
                        "1. Review database workload patterns",
                        "2. In Azure Portal: SQL Database > Compute + storage",
                        "3. Change service tier to 'Serverless'",
                        "4. Configure auto-pause delay (1 hour recommended)",
                        "5. Set min/max vCores based on peak usage",
                        "6. Apply changes (brief downtime required)",
                        "7. Monitor performance after migration",
                    ]
                    title = f"Idle Database - Switch to Serverless: {resource.name}"
                else:
                    steps = [
                        "1. Enable auto-pause for serverless database",
                        "2. Set auto-pause delay to 1 hour",
                        "3. Or manually pause when not in use",
                        "4. Database auto-resumes on connection",
                        "5. Consider scheduling pause/resume",
                    ]
                    title = f"Idle Database - Enable Auto-Pause: {resource.name}"
                
                result = CheckResult(
                    id=f"sql-idle-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=title,
                    description=(
                        f"Database showing minimal activity - CPU: {avg_cpu:.1f}% avg, {max_cpu:.1f}% max; "
                        f"Connections: {avg_connections:.0f} daily avg. "
                        f"Current tier: {resource.metadata.get('tier', 'Unknown')}"
                    ),
                    impact=(
                        f"This database has very low utilization over the past {self.days_to_analyze} days. "
                        f"{'It appears to be completely unused and could be deleted.' if recommendation == 'delete' else ''}"
                        f"{'Serverless tier with auto-pause would significantly reduce costs during idle periods.' if recommendation == 'serverless' else ''}"
                        f"{'Auto-pause would stop compute charges when database is not in use.' if recommendation == 'pause' else ''}"
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float(savings_percent),
                    effort_level=effort,
                    risk_level=risk,
                    implementation_steps=steps,
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "avg_cpu_percent": round(avg_cpu, 2),
                        "max_cpu_percent": round(max_cpu, 2),
                        "avg_daily_connections": avg_connections,
                        "current_tier": resource.metadata.get("tier"),
                        "recommendation": recommendation,
                        "sku": resource.metadata.get("sku"),
                        "analysis_days": self.days_to_analyze,
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check idle database {resource.id}: {str(e)}"
                )
                continue
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal, avg_cpu: float) -> CheckSeverity:
        """Calculate severity based on savings and usage."""
        if avg_cpu < 1 and monthly_savings > Decimal("200"):
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM