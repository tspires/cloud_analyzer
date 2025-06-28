"""Check for reserved instances utilization."""

import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    CRITICAL_MONTHLY_SAVINGS_THRESHOLD,
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
    MIN_RESERVED_INSTANCE_UTILIZATION_PERCENT,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class ReservedInstancesUtilizationCheck(Check):
    """Check for underutilized reserved instances.
    
    This check analyzes reserved instance utilization to identify underused
    reservations and opportunities to purchase new RIs for on-demand workloads.
    It helps optimize RI investments by ensuring proper allocation and identifying
    cost-saving opportunities through better coverage.
    
    Attributes:
        min_utilization_percent: Minimum utilization percentage threshold
    """
    
    def __init__(self, min_utilization_percent: float = MIN_RESERVED_INSTANCE_UTILIZATION_PERCENT) -> None:
        """Initialize reserved instances utilization check.
        
        Args:
            min_utilization_percent: Minimum utilization percentage threshold
        """
        self.min_utilization_percent = min_utilization_percent
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.RESERVED_INSTANCE_OPTIMIZATION
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Reserved Instances Utilization"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies reserved instances with utilization below {self.min_utilization_percent}% "
            f"and opportunities to purchase new reserved instances for on-demand workloads"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AWS}  # Initially AWS only, can be extended
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only instances."""
        return [
            r for r in resources
            if r.type == ResourceType.INSTANCE
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
        
        try:
            # Get reserved instances utilization
            ri_utilization = await provider.get_reserved_instances_utilization(region)
        except Exception as e:
            logger.error(
                f"Failed to get reserved instances utilization: {str(e)}"
            )
            return results
        
        # Check for underutilized RIs
        for ri in ri_utilization.get("underutilized", []):
            utilization_percent = ri.get("utilization_percentage", 0)
            if utilization_percent < self.min_utilization_percent:
                # Calculate waste
                monthly_cost = Decimal(str(ri.get("monthly_cost", 0)))
                utilized_cost = monthly_cost * Decimal(str(utilization_percent / 100))
                monthly_waste = monthly_cost - utilized_cost
                annual_waste = monthly_waste * 12
                
                result = CheckResult(
                    id=f"ri-underutilized-{ri.get('reservation_id')}",
                    check_type=self.check_type,
                    severity=self._calculate_severity(monthly_waste),
                    resource=Resource(
                        id=ri.get("reservation_id", "unknown"),
                        name=f"RI: {ri.get('instance_type', 'Unknown')}",
                        type=ResourceType.RESERVED_INSTANCE,
                        provider=CloudProvider.AWS,
                        region=ri.get("region", "unknown"),
                        state="active",
                        monthly_cost=monthly_cost,
                        is_active=True,
                        metadata=ri,
                    ),
                    title=f"Underutilized Reserved Instance: {ri.get('instance_type')}",
                    description=(
                        f"Reserved instance is only {utilization_percent:.1f}% utilized. "
                        f"Instance Type: {ri.get('instance_type')}, "
                        f"Count: {ri.get('instance_count', 1)}"
                    ),
                    impact=(
                        "You're paying for reserved capacity that isn't being fully used. "
                        "Consider modifying the reservation or ensuring workloads are properly tagged."
                    ),
                    current_cost=monthly_cost,
                    optimized_cost=utilized_cost,
                    monthly_savings=monthly_waste,
                    annual_savings=annual_waste,
                    savings_percentage=float(monthly_waste / monthly_cost * 100) if monthly_cost > 0 else 0,
                    effort_level="medium",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review workloads that should be using this reservation",
                        "2. Ensure instances are properly tagged for RI allocation",
                        "3. Consider modifying the reservation to match actual usage",
                        "4. Exchange for different instance types if needed",
                        "5. Monitor utilization after changes",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "utilization_percentage": utilization_percent,
                        "instance_type": ri.get("instance_type"),
                        "instance_count": ri.get("instance_count"),
                        "platform": ri.get("platform"),
                        "expiration_date": ri.get("expiration_date"),
                    },
                )
                results.append(result)
        
        # Check for on-demand instances that could use RIs
        try:
            on_demand_opportunities = await provider.get_on_demand_ri_opportunities(resources, region)
        except Exception as e:
            logger.warning(
                f"Failed to get on-demand RI opportunities: {str(e)}"
            )
            on_demand_opportunities = []
        
        for opportunity in on_demand_opportunities:
            monthly_savings = Decimal(str(opportunity.get("estimated_monthly_savings", 0)))
            annual_savings = monthly_savings * 12
            on_demand_cost = Decimal(str(opportunity.get("on_demand_monthly_cost", 0)))
            ri_cost = on_demand_cost - monthly_savings
            
            result = CheckResult(
                id=f"ri-opportunity-{opportunity.get('instance_type')}-{opportunity.get('region')}",
                check_type=self.check_type,
                severity=self._calculate_severity(monthly_savings),
                resource=Resource(
                    id=f"opportunity-{opportunity.get('instance_type')}",
                    name=f"RI Opportunity: {opportunity.get('instance_type')}",
                    type=ResourceType.INSTANCE,
                    provider=CloudProvider.AWS,
                    region=opportunity.get("region", "unknown"),
                    state="running",
                    monthly_cost=on_demand_cost,
                    is_active=True,
                    metadata=opportunity,
                ),
                title=f"Reserved Instance Purchase Opportunity: {opportunity.get('instance_type')}",
                description=(
                    f"You have {opportunity.get('instance_count', 0)} on-demand instances "
                    f"that could save {opportunity.get('savings_percentage', 0):.0f}% with RIs"
                ),
                impact=(
                    "Purchasing reserved instances for these steady-state workloads "
                    "can provide significant cost savings with no operational changes."
                ),
                current_cost=on_demand_cost,
                optimized_cost=ri_cost,
                monthly_savings=monthly_savings,
                annual_savings=annual_savings,
                savings_percentage=float(opportunity.get("savings_percentage", 0)),
                effort_level="low",
                risk_level="low",
                implementation_steps=[
                    "1. Verify these instances run continuously",
                    "2. Choose appropriate RI term (1 or 3 years)",
                    "3. Select payment option (All Upfront, Partial, No Upfront)",
                    "4. Purchase reserved instances through AWS Console",
                    "5. Monitor utilization to ensure proper allocation",
                ],
                confidence_score=DEFAULT_CHECK_CONFIDENCE,
                check_metadata={
                    "instance_type": opportunity.get("instance_type"),
                    "instance_count": opportunity.get("instance_count"),
                    "recommended_term": opportunity.get("recommended_term", "1-year"),
                    "break_even_months": opportunity.get("break_even_months"),
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