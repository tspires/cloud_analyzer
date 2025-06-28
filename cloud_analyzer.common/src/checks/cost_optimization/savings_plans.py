"""Check for savings plans coverage and opportunities."""

import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    CRITICAL_MONTHLY_SAVINGS_THRESHOLD,
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
    TARGET_SAVINGS_PLAN_COVERAGE_PERCENT,
    SAVINGS_PLAN_EXPIRY_WARNING_DAYS,
    RESERVED_INSTANCE_SAVINGS_ESTIMATE_PERCENT,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class SavingsPlansCoverageCheck(Check):
    """Check for savings plans coverage and opportunities.
    
    This check analyzes current savings plans coverage against a target threshold
    and identifies opportunities to increase coverage for better cost optimization.
    It also monitors expiring plans to prevent unexpected cost increases when
    plans expire.
    
    Attributes:
        target_coverage_percent: Target coverage percentage for savings plans
    """
    
    def __init__(self, target_coverage_percent: float = TARGET_SAVINGS_PLAN_COVERAGE_PERCENT) -> None:
        """Initialize savings plans coverage check.
        
        Args:
            target_coverage_percent: Target coverage percentage for savings plans
        """
        self.target_coverage_percent = target_coverage_percent
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.SAVINGS_PLAN_OPTIMIZATION
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Savings Plans Coverage Analysis"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Analyzes current savings plans coverage and identifies opportunities "
            f"to increase coverage to the target of {self.target_coverage_percent}%"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AWS}  # Savings Plans are AWS-specific
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to compute resources that can use savings plans."""
        eligible_types = [ResourceType.INSTANCE, ResourceType.FUNCTION, ResourceType.CONTAINER]
        return [
            r for r in resources
            if r.type in eligible_types and r.is_active
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
            # Get current savings plans coverage
            sp_coverage = await provider.get_savings_plans_coverage(region)
        except Exception as e:
            logger.error(
                f"Failed to get savings plans coverage: {str(e)}"
            )
            return results
        
        current_coverage = sp_coverage.get("coverage_percentage", 0)
        
        # Check if coverage is below target
        if current_coverage < self.target_coverage_percent:
            # Calculate potential savings
            total_compute_spend = Decimal(str(sp_coverage.get("total_compute_spend", 0)))
            covered_spend = Decimal(str(sp_coverage.get("covered_spend", 0)))
            on_demand_spend = total_compute_spend - covered_spend
            
            # Estimate savings (typically 20-30% for compute savings plans)
            estimated_savings_rate = RESERVED_INSTANCE_SAVINGS_ESTIMATE_PERCENT / 100.0
            additional_coverage_needed = (self.target_coverage_percent - current_coverage) / 100
            additional_spend_to_cover = total_compute_spend * Decimal(str(additional_coverage_needed))
            monthly_savings = additional_spend_to_cover * Decimal(str(estimated_savings_rate))
            annual_savings = monthly_savings * 12
            
            result = CheckResult(
                id=f"sp-coverage-opportunity",
                check_type=self.check_type,
                severity=self._calculate_severity(monthly_savings),
                resource=Resource(
                    id="savings-plans-coverage",
                    name="Savings Plans Coverage Opportunity",
                    type=ResourceType.INSTANCE,  # Generic compute
                    provider=CloudProvider.AWS,
                    region="global",
                    state="active",
                    monthly_cost=total_compute_spend,
                    is_active=True,
                    metadata=sp_coverage,
                ),
                title="Low Savings Plans Coverage",
                description=(
                    f"Current savings plans coverage is {current_coverage:.1f}%, "
                    f"below the target of {self.target_coverage_percent}%. "
                    f"On-demand spend: ${on_demand_spend:,.2f}/month"
                ),
                impact=(
                    "Increasing savings plans coverage can provide significant cost savings "
                    "on compute resources without any operational changes."
                ),
                current_cost=total_compute_spend,
                optimized_cost=total_compute_spend - monthly_savings,
                monthly_savings=monthly_savings,
                annual_savings=annual_savings,
                savings_percentage=float(monthly_savings / total_compute_spend * 100) if total_compute_spend > 0 else 0,
                effort_level="low",
                risk_level="low",
                implementation_steps=[
                    "1. Analyze compute usage patterns over the last 30 days",
                    "2. Identify stable workloads suitable for savings plans",
                    "3. Choose between Compute or EC2 Instance savings plans",
                    "4. Select commitment term (1 or 3 years)",
                    "5. Purchase savings plans through AWS Cost Explorer",
                    "6. Monitor coverage and utilization monthly",
                ],
                confidence_score=DEFAULT_CHECK_CONFIDENCE,
                check_metadata={
                    "current_coverage_percentage": current_coverage,
                    "target_coverage_percentage": self.target_coverage_percent,
                    "total_compute_spend": float(total_compute_spend),
                    "on_demand_spend": float(on_demand_spend),
                    "covered_spend": float(covered_spend),
                    "estimated_savings_rate": estimated_savings_rate,
                },
            )
            results.append(result)
        
        # Check for expiring savings plans
        expiring_plans = sp_coverage.get("expiring_plans", [])
        for plan in expiring_plans:
            days_until_expiry = plan.get("days_until_expiry", 0)
            if days_until_expiry <= SAVINGS_PLAN_EXPIRY_WARNING_DAYS:
                plan_monthly_commitment = Decimal(str(plan.get("monthly_commitment", 0)))
                
                result = CheckResult(
                    id=f"sp-expiring-{plan.get('plan_id')}",
                    check_type=self.check_type,
                    severity=CheckSeverity.HIGH if days_until_expiry <= 30 else CheckSeverity.MEDIUM,
                    resource=Resource(
                        id=plan.get("plan_id", "unknown"),
                        name=f"Savings Plan: {plan.get('plan_type', 'Unknown')}",
                        type=ResourceType.INSTANCE,
                        provider=CloudProvider.AWS,
                        region="global",
                        state="active",
                        monthly_cost=plan_monthly_commitment,
                        is_active=True,
                        metadata=plan,
                    ),
                    title=f"Expiring Savings Plan: {plan.get('plan_type')}",
                    description=(
                        f"Savings plan expires in {days_until_expiry} days. "
                        f"Monthly commitment: ${plan_monthly_commitment:,.2f}"
                    ),
                    impact=(
                        "When this savings plan expires, the covered usage will revert to "
                        "on-demand pricing, resulting in higher costs."
                    ),
                    current_cost=plan_monthly_commitment,
                    optimized_cost=plan_monthly_commitment,  # No direct savings, but prevents cost increase
                    monthly_savings=Decimal("0"),  # Preventative measure
                    annual_savings=Decimal("0"),
                    savings_percentage=0,
                    effort_level="medium",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review current utilization of the expiring plan",
                        "2. Analyze if workloads still require coverage",
                        "3. Calculate optimal commitment amount for renewal",
                        "4. Purchase new savings plan before expiration",
                        "5. Consider longer term for better discounts",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "plan_id": plan.get("plan_id"),
                        "plan_type": plan.get("plan_type"),
                        "days_until_expiry": days_until_expiry,
                        "expiry_date": plan.get("expiry_date"),
                        "utilization_percentage": plan.get("utilization_percentage"),
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