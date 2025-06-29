"""Check for database instance sizing optimization."""

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    CPU_RIGHTSIZE_THRESHOLD_PERCENT,
    CRITICAL_MONTHLY_SAVINGS_THRESHOLD,
    DATABASE_TARGET_CPU_UTILIZATION,
    DATABASE_TARGET_MEMORY_UTILIZATION,
    DEFAULT_CHECK_CONFIDENCE,
    DEFAULT_METRICS_DAYS,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
    HIGH_PEAK_CPU_THRESHOLD,
    HIGH_PEAK_MEMORY_THRESHOLD,
    MEDIUM_PEAK_CPU_THRESHOLD,
    MEDIUM_PEAK_MEMORY_THRESHOLD,
    MEMORY_RIGHTSIZE_THRESHOLD_PERCENT,
    MIN_SAVINGS_PERCENTAGE_THRESHOLD,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class DatabaseSizingCheck(Check):
    """Check for database instances that can be downsized.
    
    This check analyzes database CPU and memory utilization over a configurable
    period to identify oversized instances. It provides sizing recommendations
    that maintain performance while reducing costs, considering both average
    and peak utilization to assess risk levels.
    
    Attributes:
        cpu_threshold: CPU utilization threshold below which downsizing is considered
        memory_threshold: Memory utilization threshold below which downsizing is considered
        days_to_check: Number of days of metrics to analyze
    """
    
    def __init__(
        self,
        cpu_threshold: float = CPU_RIGHTSIZE_THRESHOLD_PERCENT,
        memory_threshold: float = MEMORY_RIGHTSIZE_THRESHOLD_PERCENT,
        days_to_check: int = DEFAULT_METRICS_DAYS,
    ) -> None:
        """Initialize database sizing check.
        
        Args:
            cpu_threshold: CPU utilization threshold (%)
            memory_threshold: Memory utilization threshold (%)
            days_to_check: Number of days to analyze
        """
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.days_to_check = days_to_check
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.RIGHT_SIZING
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Database Right-Sizing"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies database instances with CPU utilization below {self.cpu_threshold}% "
            f"and memory utilization below {self.memory_threshold}% that can be downsized"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only database instances."""
        return [
            r for r in resources
            if r.type == ResourceType.DATABASE and r.is_active
        ]
    
    async def run(
        self,
        provider: CloudProviderInterface,
        resources: List[Resource],
        region: Optional[str] = None,
    ) -> List[CheckResult]:
        """Run the check against provided resources."""
        results = []
        logger = logging.getLogger(__name__)
        
        for resource in resources:
            if region and resource.region != region:
                continue
            
            try:
                # Get database metrics
                metrics = await provider.get_database_metrics(
                    resource.id, resource.region, self.days_to_check
                )
            except Exception as e:
                logger.warning(
                    f"Failed to get database metrics for {resource.id}: {str(e)}"
                )
                continue
            
            avg_cpu = metrics.get("avg_cpu_percent", 100)
            avg_memory = metrics.get("avg_memory_percent", 100)
            max_cpu = metrics.get("max_cpu_percent", 100)
            max_memory = metrics.get("max_memory_percent", 100)
            
            # Check if database can be downsized
            if avg_cpu < self.cpu_threshold and avg_memory < self.memory_threshold:
                try:
                    # Get current instance details
                    db_info = await provider.get_database_info(resource.id, resource.region)
                    current_instance_type = db_info.get("instance_type", "Unknown")
                except Exception as e:
                    logger.warning(
                        f"Failed to get database info for {resource.id}: {str(e)}"
                    )
                    continue
                
                try:
                    # Get recommended instance type
                    recommendations = await provider.get_database_sizing_recommendations(
                        resource.id,
                        resource.region,
                        metrics
                    )
                except Exception as e:
                    logger.warning(
                        f"Failed to get database sizing recommendations for {resource.id}: {str(e)}"
                    )
                    continue
                
                if recommendations:
                    recommended = recommendations[0]  # Take the top recommendation
                    recommended_type = recommended.get("instance_type")
                    recommended_cost = Decimal(str(recommended.get("monthly_cost", 0)))
                    
                    monthly_savings = resource.monthly_cost - recommended_cost
                    annual_savings = monthly_savings * 12
                    
                    # Only recommend if there are significant savings
                    if monthly_savings > 0 and (monthly_savings / resource.monthly_cost) > (MIN_SAVINGS_PERCENTAGE_THRESHOLD / 100):
                        severity = self._calculate_severity(monthly_savings)
                        
                        # Determine risk level based on peak utilization
                        risk_level = "low"
                        if max_cpu > HIGH_PEAK_CPU_THRESHOLD or max_memory > HIGH_PEAK_MEMORY_THRESHOLD:
                            risk_level = "high"
                        elif max_cpu > MEDIUM_PEAK_CPU_THRESHOLD or max_memory > MEDIUM_PEAK_MEMORY_THRESHOLD:
                            risk_level = "medium"
                        
                        result = CheckResult(
                            id=f"db-rightsize-{resource.id}",
                            check_type=self.check_type,
                            severity=severity,
                            resource=resource,
                            title=f"Oversized Database: {resource.name}",
                            description=(
                                f"Database instance {current_instance_type} has low utilization: "
                                f"CPU {avg_cpu:.1f}% (max {max_cpu:.1f}%), "
                                f"Memory {avg_memory:.1f}% (max {max_memory:.1f}%). "
                                f"Recommend downsizing to {recommended_type}"
                            ),
                            impact=(
                                "This database instance is oversized for its workload. "
                                "Downsizing can reduce costs while maintaining performance."
                            ),
                            current_cost=resource.monthly_cost,
                            optimized_cost=recommended_cost,
                            monthly_savings=monthly_savings,
                            annual_savings=annual_savings,
                            savings_percentage=float(monthly_savings / resource.monthly_cost * 100),
                            effort_level="medium",
                            risk_level=risk_level,
                            implementation_steps=[
                                "1. Review database workload patterns during peak times",
                                "2. Create a backup of the database",
                                "3. Test the workload on a smaller instance (if possible)",
                                "4. Schedule downtime for the resize operation",
                                "5. Modify the database instance to the recommended type",
                                "6. Monitor performance after resizing",
                                "7. Keep the backup for 7 days to ensure stability",
                            ],
                            confidence_score=DEFAULT_CHECK_CONFIDENCE,
                            check_metadata={
                                "current_instance_type": current_instance_type,
                                "recommended_instance_type": recommended_type,
                                "avg_cpu_percent": avg_cpu,
                                "max_cpu_percent": max_cpu,
                                "avg_memory_percent": avg_memory,
                                "max_memory_percent": max_memory,
                                "days_analyzed": self.days_to_check,
                                "engine": db_info.get("engine"),
                                "engine_version": db_info.get("engine_version"),
                                "multi_az": db_info.get("multi_az", False),
                                "storage_type": db_info.get("storage_type"),
                                "allocated_storage_gb": db_info.get("allocated_storage_gb"),
                            },
                        )
                        
                        results.append(result)
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > CRITICAL_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM