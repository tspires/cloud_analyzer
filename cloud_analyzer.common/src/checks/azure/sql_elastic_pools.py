"""Check for Azure SQL Database elastic pool opportunities."""

import logging
from collections import defaultdict
from decimal import Decimal
from typing import Dict, List, Optional, Set, Tuple

from constants import (
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class AzureSQLElasticPoolCheck(Check):
    """Check for SQL Database elastic pool opportunities.
    
    Elastic pools allow multiple databases to share resources at a lower cost
    than individual database pricing. This check identifies databases that could
    benefit from pooling.
    
    Attributes:
        min_databases: Minimum databases needed for pool recommendation
        utilization_variance_threshold: Threshold for workload variance
    """
    
    def __init__(
        self,
        min_databases: int = 2,
        utilization_variance_threshold: float = 30.0
    ) -> None:
        """Initialize the check.
        
        Args:
            min_databases: Minimum databases for pool
            utilization_variance_threshold: Variance threshold for pooling benefit
        """
        self.min_databases = min_databases
        self.utilization_variance_threshold = utilization_variance_threshold
        self.logger = logging.getLogger(__name__)
        
        # Elastic pool can save 30-50% for appropriate workloads
        self.pool_savings_percent = 35
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.RIGHT_SIZING
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Azure SQL Elastic Pool Optimization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies groups of {self.min_databases}+ SQL databases on the same server "
            "that could benefit from elastic pooling for cost savings"
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
            and r.metadata.get("tier") not in ["Serverless", "Hyperscale"]  # These don't support pools
        ]
    
    async def run(
        self,
        provider: CloudProviderInterface,
        resources: List[Resource],
        region: Optional[str] = None,
    ) -> List[CheckResult]:
        """Run the check against provided resources."""
        results = []
        
        # Group databases by server and region
        server_databases: Dict[Tuple[str, str], List[Resource]] = defaultdict(list)
        
        for resource in resources:
            if region and resource.region != region:
                continue
            
            server_name = resource.metadata.get("server_name", "unknown")
            server_key = (server_name, resource.region)
            server_databases[server_key].append(resource)
        
        # Analyze each server's databases
        for (server_name, server_region), databases in server_databases.items():
            if len(databases) < self.min_databases:
                continue
            
            try:
                # Get metrics for all databases
                database_metrics = []
                total_monthly_cost = Decimal("0")
                total_dtu_needed = 0
                peak_dtu_times = defaultdict(float)
                
                for db in databases:
                    metrics = await provider.get_database_metrics(
                        db.id, db.region, days=30
                    )
                    
                    avg_dtu = metrics.get("avg_dtu_percent", 0) * self._get_dtu_from_sku(db.metadata.get("sku", "S0")) / 100
                    max_dtu = metrics.get("max_dtu_percent", 0) * self._get_dtu_from_sku(db.metadata.get("sku", "S0")) / 100
                    
                    database_metrics.append({
                        "db": db,
                        "avg_dtu": avg_dtu,
                        "max_dtu": max_dtu,
                        "metrics": metrics,
                    })
                    
                    total_monthly_cost += db.monthly_cost
                    total_dtu_needed += max_dtu
                    
                    # Track peak usage times (simplified - would analyze hourly data)
                    peak_hour = metrics.get("peak_usage_hour", 14)  # Default 2 PM
                    peak_dtu_times[peak_hour] += max_dtu
                
                # Check if databases have complementary workloads
                # (peaks at different times = good for pooling)
                max_concurrent_dtu = max(peak_dtu_times.values()) if peak_dtu_times else total_dtu_needed
                workload_variance = ((total_dtu_needed - max_concurrent_dtu) / total_dtu_needed * 100) if total_dtu_needed > 0 else 0
                
                # Skip if workloads are too similar (all peak at same time)
                if workload_variance < self.utilization_variance_threshold:
                    continue
                
                # Calculate elastic pool sizing
                # Pool eDTU should be ~1.5x max concurrent DTU for headroom
                recommended_pool_edtu = int(max_concurrent_dtu * 1.5)
                recommended_pool_edtu = max(50, min(recommended_pool_edtu, 4000))  # Pool limits
                
                # Estimate pool cost
                pool_monthly_cost = self._estimate_pool_cost(recommended_pool_edtu, server_region)
                
                # Only recommend if there are savings
                if pool_monthly_cost >= total_monthly_cost:
                    continue
                
                monthly_savings = total_monthly_cost - pool_monthly_cost
                annual_savings = monthly_savings * 12
                savings_percentage = float((monthly_savings / total_monthly_cost) * 100)
                
                # Determine severity
                severity = self._calculate_severity(monthly_savings)
                
                result = CheckResult(
                    id=f"sql-elastic-pool-{server_name}-{server_region}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=databases[0],  # Representative database
                    related_resources=databases[1:],
                    title=f"Elastic Pool Opportunity: {len(databases)} databases on {server_name}",
                    description=(
                        f"{len(databases)} databases could share {recommended_pool_edtu} eDTU pool. "
                        f"Current total: {int(total_dtu_needed)} DTU, Peak concurrent: {int(max_concurrent_dtu)} DTU. "
                        f"Workload variance: {workload_variance:.0f}%"
                    ),
                    impact=(
                        f"These databases have complementary workload patterns with peaks at different times. "
                        f"An elastic pool would allow them to share resources, reducing costs by {savings_percentage:.0f}% "
                        "while maintaining performance. Databases can burst above their allocated resources when needed."
                    ),
                    current_cost=total_monthly_cost,
                    optimized_cost=pool_monthly_cost,
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=savings_percentage,
                    effort_level="medium",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review database workload patterns to confirm pooling suitability",
                        "2. Create elastic pool in Azure Portal on the same server",
                        f"3. Recommended pool size: {recommended_pool_edtu} eDTU",
                        f"4. Set per-database min/max eDTU limits (e.g., min: 0, max: {recommended_pool_edtu // len(databases) * 2})",
                        "5. Move databases to pool one by one during low-usage periods",
                        "6. Monitor pool utilization for first week",
                        "7. Adjust pool size or per-database limits as needed",
                        "8. Consider adding more databases to the pool in the future",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE * 0.85,  # Slightly lower due to workload estimation
                    check_metadata={
                        "server_name": server_name,
                        "database_count": len(databases),
                        "total_dtu_needed": int(total_dtu_needed),
                        "max_concurrent_dtu": int(max_concurrent_dtu),
                        "recommended_pool_edtu": recommended_pool_edtu,
                        "workload_variance_percent": round(workload_variance, 1),
                        "database_names": [db.name for db in databases],
                    },
                )
                
                results.append(result)
                
            except Exception as e:
                self.logger.warning(
                    f"Failed to analyze elastic pool opportunity for {server_name}: {str(e)}"
                )
                continue
        
        return results
    
    def _get_dtu_from_sku(self, sku: str) -> int:
        """Get DTU value from database SKU."""
        dtu_map = {
            "S0": 10,
            "S1": 20,
            "S2": 50,
            "S3": 100,
            "S4": 200,
            "S6": 400,
            "S7": 800,
            "S9": 1600,
            "S12": 3000,
            "P1": 125,
            "P2": 250,
            "P4": 500,
            "P6": 1000,
            "P11": 1750,
            "P15": 4000,
        }
        return dtu_map.get(sku, 50)
    
    def _estimate_pool_cost(self, edtu: int, region: str) -> Decimal:
        """Estimate monthly cost for elastic pool."""
        # Simplified pricing (~$1.50 per eDTU/month)
        cost_per_edtu = Decimal("1.50")
        return Decimal(str(edtu)) * cost_per_edtu * Decimal("730") / Decimal("24")  # Monthly
    
    def _calculate_severity(self, monthly_savings: Decimal) -> CheckSeverity:
        """Calculate severity based on monthly savings amount."""
        if monthly_savings > Decimal("1000"):
            return CheckSeverity.CRITICAL
        elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
            return CheckSeverity.HIGH
        else:
            return CheckSeverity.MEDIUM