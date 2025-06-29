"""Check for unattached storage volumes."""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    CRITICAL_MONTHLY_SAVINGS_THRESHOLD,
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
    MIN_DAYS_VOLUME_UNATTACHED,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class UnattachedVolumesCheck(Check):
    """Check for unattached storage volumes.
    
    This check identifies storage volumes that have been detached from instances
    for a configurable period and can be safely deleted to reduce costs. It analyzes
    volume attachment status and calculates potential savings from removing unused
    volumes.
    
    Attributes:
        min_days_unattached: Minimum days a volume must be unattached before flagging
    """
    
    def __init__(self, min_days_unattached: int = MIN_DAYS_VOLUME_UNATTACHED) -> None:
        """Initialize unattached volumes check.
        
        Args:
            min_days_unattached: Minimum days a volume must be unattached to be flagged
        """
        self.min_days_unattached = min_days_unattached
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.UNATTACHED_VOLUME
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Unattached Volume Detection"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies storage volumes that have been unattached for more than "
            f"{self.min_days_unattached} days and can be deleted to save costs"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only storage volumes."""
        return [
            r for r in resources
            if r.type == ResourceType.VOLUME
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
                # Check if volume is attached
                volume_info = await provider.get_volume_info(resource.id, resource.region)
            except Exception as e:
                logger.warning(
                    f"Failed to get volume info for {resource.id}: {str(e)}"
                )
                continue
            
            if not volume_info.get("attached", True):
                # Get the time when volume was detached
                detached_time = volume_info.get("detached_at")
                if detached_time:
                    # Parse datetime if it's a string
                    if isinstance(detached_time, str):
                        try:
                            detached_time = datetime.fromisoformat(detached_time.replace('Z', '+00:00'))
                        except ValueError:
                            logger.warning(f"Invalid datetime format for volume {resource.id}: {detached_time}")
                            continue
                    
                    days_unattached = (datetime.now(timezone.utc) - detached_time).days
                    
                    if days_unattached >= self.min_days_unattached:
                        # Calculate savings (100% of volume cost)
                        monthly_savings = resource.monthly_cost
                        annual_savings = monthly_savings * 12
                        
                        # Determine severity based on cost
                        severity = self._calculate_severity(monthly_savings)
                        
                        result = CheckResult(
                            id=f"unattached-{resource.id}",
                            check_type=self.check_type,
                            severity=severity,
                            resource=resource,
                            title=f"Unattached Volume: {resource.name}",
                            description=(
                                f"Volume has been unattached for {days_unattached} days. "
                                f"Size: {volume_info.get('size_gb', 'Unknown')} GB, "
                                f"Type: {volume_info.get('volume_type', 'Unknown')}"
                            ),
                            impact=(
                                "This unattached volume is incurring storage costs without being used. "
                                "Consider creating a snapshot and deleting the volume, or reattaching it if needed."
                            ),
                            current_cost=resource.monthly_cost,
                            optimized_cost=Decimal("0"),
                            monthly_savings=monthly_savings,
                            annual_savings=annual_savings,
                            savings_percentage=100.0,
                            effort_level="low",
                            risk_level="low",
                            implementation_steps=[
                                "1. Verify the volume is not needed",
                                "2. Create a snapshot of the volume for backup (if data is needed)",
                                "3. Delete the unattached volume",
                                "4. Monitor for any issues after deletion",
                            ],
                            confidence_score=DEFAULT_CHECK_CONFIDENCE,
                            check_metadata={
                                "days_unattached": days_unattached,
                                "volume_size_gb": volume_info.get("size_gb"),
                                "volume_type": volume_info.get("volume_type"),
                                "detached_at": detached_time.isoformat() if detached_time else None,
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