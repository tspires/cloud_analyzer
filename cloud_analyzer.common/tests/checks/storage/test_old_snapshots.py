"""Tests for old snapshots check."""

import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import AsyncMock

from src.checks.storage.old_snapshots import OldSnapshotsCheck
from src.models.base import CloudProvider, Resource, ResourceType
from src.models.checks import CheckSeverity


@pytest.fixture
def old_snapshots_check():
    """Create an old snapshots check instance."""
    return OldSnapshotsCheck(max_age_days=30)


@pytest.fixture
def mock_provider():
    """Create a mock cloud provider."""
    provider = AsyncMock()
    provider.provider = CloudProvider.AWS
    return provider


@pytest.fixture
def sample_snapshots():
    """Create sample snapshot resources."""
    return [
        Resource(
            id="snap-1234",
            name="Daily Backup",
            type=ResourceType.SNAPSHOT,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="completed",
            monthly_cost=Decimal("10.00"),
            is_active=True,
        ),
        Resource(
            id="snap-5678",
            name="Weekly Backup",
            type=ResourceType.SNAPSHOT,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="completed",
            monthly_cost=Decimal("20.00"),
            is_active=True,
        ),
        Resource(
            id="snap-9012",
            name="Old AMI Snapshot",
            type=ResourceType.SNAPSHOT,
            provider=CloudProvider.AWS,
            region="us-west-2",
            state="completed",
            monthly_cost=Decimal("150.00"),
            is_active=True,
        ),
    ]


class TestOldSnapshotsCheck:
    """Test old snapshots check."""

    def test_check_properties(self, old_snapshots_check):
        """Test check properties."""
        assert old_snapshots_check.name == "Old Snapshot Detection"
        assert old_snapshots_check.check_type.value == "old_snapshot"
        assert CloudProvider.AWS in old_snapshots_check.supported_providers

    def test_filter_resources(self, old_snapshots_check, sample_snapshots):
        """Test resource filtering."""
        # Add non-snapshot resources
        resources = sample_snapshots + [
            Resource(
                id="vol-1234",
                name="Volume",
                type=ResourceType.VOLUME,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="available",
                monthly_cost=Decimal("50.00"),
                is_active=True,
            )
        ]
        
        filtered = old_snapshots_check.filter_resources(resources)
        assert len(filtered) == 3
        assert all(r.type == ResourceType.SNAPSHOT for r in filtered)

    @pytest.mark.asyncio
    async def test_run_with_old_snapshots(
        self, old_snapshots_check, mock_provider, sample_snapshots
    ):
        """Test running check with old snapshots."""
        # Mock snapshot info responses
        mock_provider.get_snapshot_info.side_effect = [
            {
                "created_at": datetime.now(timezone.utc) - timedelta(days=10),  # Recent
                "size_gb": 50,
                "is_ami_snapshot": False,
                "has_backup_policy": False,
            },
            {
                "created_at": datetime.now(timezone.utc) - timedelta(days=45),  # Old
                "size_gb": 100,
                "is_ami_snapshot": False,
                "has_backup_policy": True,
                "volume_id": "vol-abc123",
            },
            {
                "created_at": datetime.now(timezone.utc) - timedelta(days=200),  # Very old
                "size_gb": 500,
                "is_ami_snapshot": True,
                "has_backup_policy": False,
            },
        ]
        
        results = await old_snapshots_check.run(mock_provider, sample_snapshots)
        
        assert len(results) == 2  # Two old snapshots
        
        # Check first old snapshot
        result1 = results[0]
        assert result1.resource.id == "snap-5678"
        assert result1.monthly_savings == Decimal("20.00")
        assert result1.severity == CheckSeverity.MEDIUM
        assert "45 days old" in result1.description
        assert "Part of backup policy" in result1.description
        assert result1.risk_level == "medium"  # Has backup policy
        
        # Check second old snapshot
        result2 = results[1]
        assert result2.resource.id == "snap-9012"
        assert result2.monthly_savings == Decimal("150.00")
        assert result2.severity == CheckSeverity.CRITICAL  # Very old and high cost
        assert "200 days old" in result2.description
        assert "Associated with AMI" in result2.description
        assert result2.risk_level == "medium"  # AMI snapshot

    @pytest.mark.asyncio
    async def test_run_with_recent_snapshots(
        self, old_snapshots_check, mock_provider, sample_snapshots
    ):
        """Test that recent snapshots are not flagged."""
        # Mock snapshot info - created 20 days ago
        mock_provider.get_snapshot_info.return_value = {
            "created_at": datetime.now(timezone.utc) - timedelta(days=20),
            "size_gb": 100,
            "is_ami_snapshot": False,
            "has_backup_policy": False,
        }
        
        results = await old_snapshots_check.run(
            mock_provider, [sample_snapshots[0]]
        )
        
        assert len(results) == 0  # Should not flag snapshots < 30 days old

    @pytest.mark.asyncio
    async def test_run_with_region_filter(
        self, old_snapshots_check, mock_provider, sample_snapshots
    ):
        """Test running check with region filter."""
        mock_provider.get_snapshot_info.return_value = {
            "created_at": datetime.now(timezone.utc) - timedelta(days=60),
            "size_gb": 100,
            "is_ami_snapshot": False,
            "has_backup_policy": False,
        }
        
        results = await old_snapshots_check.run(
            mock_provider, sample_snapshots, region="us-west-2"
        )
        
        # Should only check snapshots in us-west-2
        assert len(results) == 1
        assert results[0].resource.id == "snap-9012"

    def test_calculate_severity(self, old_snapshots_check):
        """Test severity calculation based on age and cost."""
        # Very old (> 180 days)
        assert (
            old_snapshots_check._calculate_severity(Decimal("200"), 200)
            == CheckSeverity.CRITICAL
        )
        assert (
            old_snapshots_check._calculate_severity(Decimal("50"), 200)
            == CheckSeverity.HIGH
        )
        
        # Moderately old (> 90 days)
        assert (
            old_snapshots_check._calculate_severity(Decimal("600"), 100)
            == CheckSeverity.CRITICAL
        )
        assert (
            old_snapshots_check._calculate_severity(Decimal("200"), 100)
            == CheckSeverity.HIGH
        )
        assert (
            old_snapshots_check._calculate_severity(Decimal("50"), 100)
            == CheckSeverity.MEDIUM
        )
        
        # Less old (< 90 days)
        assert (
            old_snapshots_check._calculate_severity(Decimal("600"), 40)
            == CheckSeverity.HIGH
        )
        assert (
            old_snapshots_check._calculate_severity(Decimal("50"), 40)
            == CheckSeverity.MEDIUM
        )