"""Check for old snapshots that can be deleted."""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional, Set

from constants import (
    CRITICAL_MONTHLY_SAVINGS_THRESHOLD,
    DEFAULT_CHECK_CONFIDENCE,
    HIGH_MONTHLY_SAVINGS_THRESHOLD,
    MAX_SNAPSHOT_AGE_DAYS,
)
from models.checks import CheckResult, CheckSeverity, CheckType
from models.base import CloudProvider, Resource, ResourceType
from providers.base import CloudProviderInterface
from checks.base import Check


class OldSnapshotsCheck(Check):
    """Check for old snapshots that can be deleted.
    
    This check identifies snapshots that exceed a configurable age threshold and may
    no longer be needed for recovery or compliance. It considers factors like AMI
    associations and backup policies when assessing risk levels for deletion.
    
    Attributes:
        max_age_days: Maximum age in days before a snapshot is considered old
    """
    
    def __init__(self, max_age_days: int = MAX_SNAPSHOT_AGE_DAYS) -> None:
        """Initialize old snapshots check.
        
        Args:
            max_age_days: Maximum age in days before a snapshot is considered old
        """
        self.max_age_days = max_age_days
    
    @property
    def check_type(self) -> CheckType:
        """Return the type of check."""
        return CheckType.OLD_SNAPSHOT
    
    @property
    def name(self) -> str:
        """Return human-readable name of the check."""
        return "Old Snapshot Detection"
    
    @property
    def description(self) -> str:
        """Return description of what this check does."""
        return (
            f"Identifies snapshots older than {self.max_age_days} days that may no longer "
            f"be needed and can be deleted to reduce storage costs"
        )
    
    @property
    def supported_providers(self) -> Set[CloudProvider]:
        """Return set of providers this check supports."""
        return {CloudProvider.AZURE}
    
    def filter_resources(self, resources: List[Resource]) -> List[Resource]:
        """Filter to only snapshots."""
        return [
            r for r in resources
            if r.type == ResourceType.SNAPSHOT
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
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.max_age_days)
        
        for resource in resources:
            if region and resource.region != region:
                continue
            
            try:
                # Get snapshot details
                snapshot_info = await provider.get_snapshot_info(resource.id, resource.region)
            except Exception as e:
                logger.warning(
                    f"Failed to get snapshot info for {resource.id}: {str(e)}"
                )
                continue
            
            created_at = snapshot_info.get("created_at")
            # Parse datetime if it's a string
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except ValueError:
                    logger.warning(f"Invalid datetime format for snapshot {resource.id}: {created_at}")
                    continue
            
            if created_at and created_at < cutoff_date:
                age_days = (datetime.now(timezone.utc) - created_at).days
                
                # Calculate savings (100% of snapshot cost)
                monthly_savings = resource.monthly_cost
                annual_savings = monthly_savings * 12
                
                # Determine severity based on cost and age
                severity = self._calculate_severity(monthly_savings, age_days)
                
                # Check if snapshot is associated with an AMI or backup policy
                is_ami_snapshot = snapshot_info.get("is_ami_snapshot", False)
                has_backup_policy = snapshot_info.get("has_backup_policy", False)
                
                risk_level = "low"
                if is_ami_snapshot or has_backup_policy:
                    risk_level = "medium"
                
                result = CheckResult(
                    id=f"old-snapshot-{resource.id}",
                    check_type=self.check_type,
                    severity=severity,
                    resource=resource,
                    title=f"Old Snapshot: {resource.name}",
                    description=(
                        f"Snapshot is {age_days} days old. "
                        f"Size: {snapshot_info.get('size_gb', 'Unknown')} GB"
                        + (", Associated with AMI" if is_ami_snapshot else "")
                        + (", Part of backup policy" if has_backup_policy else "")
                    ),
                    impact=(
                        "Old snapshots consume storage and incur costs. "
                        "Review and delete snapshots that are no longer needed for recovery or compliance."
                    ),
                    current_cost=resource.monthly_cost,
                    optimized_cost=Decimal("0"),
                    monthly_savings=monthly_savings,
                    annual_savings=annual_savings,
                    savings_percentage=100.0,
                    effort_level="low",
                    risk_level=risk_level,
                    implementation_steps=[
                        "1. Verify the snapshot is not needed for recovery",
                        "2. Check if snapshot is required for compliance/retention policies",
                        "3. Ensure no dependencies on the snapshot (AMIs, volumes)",
                        "4. Delete the snapshot",
                        "5. Update backup policies if needed",
                    ],
                    confidence_score=DEFAULT_CHECK_CONFIDENCE,
                    check_metadata={
                        "age_days": age_days,
                        "snapshot_size_gb": snapshot_info.get("size_gb"),
                        "is_ami_snapshot": is_ami_snapshot,
                        "has_backup_policy": has_backup_policy,
                        "created_at": created_at.isoformat() if created_at else None,
                        "volume_id": snapshot_info.get("volume_id"),
                    },
                )
                
                results.append(result)
        
        return results
    
    def _calculate_severity(self, monthly_savings: Decimal, age_days: int) -> CheckSeverity:
        """Calculate severity based on monthly savings and age."""
        # Increase severity for very old snapshots
        if age_days > 180:  # 6 months
            if monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
                return CheckSeverity.CRITICAL
            else:
                return CheckSeverity.HIGH
        elif age_days > 90:  # 3 months
            if monthly_savings > CRITICAL_MONTHLY_SAVINGS_THRESHOLD:
                return CheckSeverity.CRITICAL
            elif monthly_savings > HIGH_MONTHLY_SAVINGS_THRESHOLD:
                return CheckSeverity.HIGH
            else:
                return CheckSeverity.MEDIUM
        else:
            if monthly_savings > CRITICAL_MONTHLY_SAVINGS_THRESHOLD:
                return CheckSeverity.HIGH
            else:
                return CheckSeverity.MEDIUM