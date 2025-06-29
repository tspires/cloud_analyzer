"""Check for Azure Storage logging and metrics optimization."""

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


class AzureStorageLoggingCheck(Check):
    """Check for Azure Storage logging and metrics optimization.
    
    Storage Analytics logging and minute metrics can generate significant costs
    for high-traffic storage accounts. This check identifies opportunities to
    optimize logging settings for cost savings.
    """
    
    def __init__(self) -> None:
        """Initialize the check."""
        self.logger = logging.getLogger(__name__)
        
        # Cost per GB for analytics storage (approximate)
        self.analytics_cost_per_gb = Decimal("0.02")
        
        # Thresholds
        self.high_logging_gb = 100  # GB of logs per month
        self.high_metrics_count = 1000000  # Number of minute metrics
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.LOG_RETENTION
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure Storage Analytics Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            "Identifies storage accounts with excessive logging or minute metrics "
            "that could be optimized to reduce analytics storage costs"
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
                # Get storage analytics info
                storage_info = await provider.get_storage_info(resource.id, resource.region)
                analytics_info = storage_info.get("analytics", {})
                
                # Check if analytics is enabled
                logging_enabled = analytics_info.get("logging_enabled", False)
                minute_metrics_enabled = analytics_info.get("minute_metrics_enabled", False)
                
                if not logging_enabled and not minute_metrics_enabled:
                    continue
                
                # Get analytics data size
                logging_size_gb = analytics_info.get("logging_size_gb", 0)
                metrics_size_gb = analytics_info.get("metrics_size_gb", 0)
                total_analytics_gb = logging_size_gb + metrics_size_gb
                
                # Get retention settings
                logging_retention_days = analytics_info.get("logging_retention_days", 0)
                metrics_retention_days = analytics_info.get("metrics_retention_days", 0)
                
                # Check for optimization opportunities
                recommendations = []
                estimated_savings_percent = 0
                
                # Check if it's a non-production environment
                is_non_prod = False
                if resource.tags:
                    env_tag = resource.tags.get("environment", "").lower()
                    is_non_prod = env_tag in ["dev", "test", "staging", "qa"]
                
                # Logging recommendations
                if logging_enabled:
                    if logging_size_gb > self.high_logging_gb:
                        recommendations.append("High logging volume detected")
                        if logging_retention_days > 30:
                            recommendations.append(f"Reduce logging retention from {logging_retention_days} to 30 days")
                            estimated_savings_percent += 20
                        if is_non_prod:
                            recommendations.append("Consider disabling logging for non-production")
                            estimated_savings_percent += 30
                    elif is_non_prod:
                        recommendations.append("Disable logging for non-production environment")
                        estimated_savings_percent += 20
                
                # Minute metrics recommendations
                if minute_metrics_enabled:
                    if is_non_prod:
                        recommendations.append("Disable minute metrics for non-production")
                        estimated_savings_percent += 20
                    elif metrics_retention_days > 30:
                        recommendations.append(f"Reduce metrics retention from {metrics_retention_days} to 30 days")
                        estimated_savings_percent += 15
                    
                    # Check if hour metrics would be sufficient
                    transaction_count = storage_info.get("monthly_transactions", 0)
                    if transaction_count < 1000000:  # Low traffic
                        recommendations.append("Switch from minute metrics to hour metrics")
                        estimated_savings_percent += 25
                
                if not recommendations:
                    continue
                
                # Calculate savings
                analytics_monthly_cost = total_analytics_gb * self.analytics_cost_per_gb
                
                # Add a portion of the storage account cost for high analytics usage
                if total_analytics_gb > 50:
                    analytics_monthly_cost += resource.monthly_cost * Decimal("0.1")
                
                monthly_savings = analytics_monthly_cost * Decimal(estimated_savings_percent) / Decimal(100)
                annual_savings = monthly_savings * 12
                optimized_cost = analytics_monthly_cost - monthly_savings
                
                if monthly_savings < Decimal("5"):
                    continue
                
                # Determine severity
                if total_analytics_gb > 500 or (is_non_prod and total_analytics_gb > 50):
                    severity = CheckSeverity.HIGH
                elif total_analytics_gb > 100:
                    severity = CheckSeverity.MEDIUM
                else:
                    severity = CheckSeverity.LOW
                
                result = CheckResult(
                    id=f"storage-logging-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Storage Analytics Optimization: {resource.name}",
                    description=(
                        f"Storage analytics using {total_analytics_gb:.1f} GB "
                        f"(Logging: {logging_size_gb:.1f} GB, Metrics: {metrics_size_gb:.1f} GB). "
                        f"Environment: {resource.tags.get('environment', 'production')}"
                    ),
                    impact=(
                        "Storage Analytics can generate significant data volume and costs for busy storage accounts. "
                        "Optimizing retention periods and disabling unnecessary analytics for non-production "
                        "environments can reduce costs without impacting operations."
                    ),
                    current_cost=analytics_monthly_cost,
                    optimized_cost=optimized_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=float(estimated_savings_percent),
                    effort_level="low",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review current analytics usage and requirements",
                        "2. Navigate to Storage Account > Monitoring > Diagnostic settings",
                        "3. For logging optimization:",
                        "   - Adjust retention period to 30 days or less",
                        "   - Disable verbose logging levels if not needed",
                        "   - Turn off logging for non-production environments",
                        "4. For metrics optimization:",
                        "   - Switch from minute to hour metrics for low-traffic accounts",
                        "   - Reduce retention period to 30 days",
                        "   - Disable for non-production environments",
                        "5. Set up alerts for critical operations instead of extensive logging",
                        "6. Use Azure Monitor Logs for centralized logging if needed",
                        "7. Implement log analytics queries for troubleshooting instead of raw logs",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "logging_enabled": logging_enabled,
                        "minute_metrics_enabled": minute_metrics_enabled,
                        "logging_size_gb": round(logging_size_gb, 2),
                        "metrics_size_gb": round(metrics_size_gb, 2),
                        "total_analytics_gb": round(total_analytics_gb, 2),
                        "logging_retention_days": logging_retention_days,
                        "metrics_retention_days": metrics_retention_days,
                        "is_non_production": is_non_prod,
                        "recommendations": recommendations,
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to check storage logging for {resource.id}: {str(e)}"
                )
                continue
        
        return results