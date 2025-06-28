"""Tests for unattached volumes check."""

import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from src.checks.storage.unattached_volumes import UnattachedVolumesCheck
from src.models.base import CloudProvider, Resource, ResourceType
from src.models.checks import CheckSeverity


@pytest.fixture
def unattached_volumes_check():
    """Create an unattached volumes check instance."""
    return UnattachedVolumesCheck(min_days_unattached=7)


@pytest.fixture
def mock_provider():
    """Create a mock cloud provider."""
    provider = AsyncMock()
    provider.provider = CloudProvider.AWS
    return provider


@pytest.fixture
def sample_volumes():
    """Create sample volume resources."""
    return [
        Resource(
            id="vol-1234",
            name="DataVolume",
            type=ResourceType.VOLUME,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="available",
            monthly_cost=Decimal("50.00"),
            is_active=True,
        ),
        Resource(
            id="vol-5678",
            name="BackupVolume",
            type=ResourceType.VOLUME,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="in-use",
            monthly_cost=Decimal("100.00"),
            is_active=True,
        ),
        Resource(
            id="vol-9012",
            name="OldVolume",
            type=ResourceType.VOLUME,
            provider=CloudProvider.AWS,
            region="us-west-2",
            state="available",
            monthly_cost=Decimal("200.00"),
            is_active=True,
        ),
    ]


class TestUnattachedVolumesCheck:
    """Test unattached volumes check."""

    def test_check_properties(self, unattached_volumes_check):
        """Test check properties."""
        assert unattached_volumes_check.name == "Unattached Volume Detection"
        assert unattached_volumes_check.check_type.value == "unattached_volume"
        assert CloudProvider.AWS in unattached_volumes_check.supported_providers

    def test_filter_resources(self, unattached_volumes_check, sample_volumes):
        """Test resource filtering."""
        # Add non-volume resources
        resources = sample_volumes + [
            Resource(
                id="i-1234",
                name="Instance",
                type=ResourceType.INSTANCE,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="running",
                monthly_cost=Decimal("100.00"),
                is_active=True,
            )
        ]
        
        filtered = unattached_volumes_check.filter_resources(resources)
        assert len(filtered) == 3
        assert all(r.type == ResourceType.VOLUME for r in filtered)

    @pytest.mark.asyncio
    async def test_run_with_unattached_volumes(
        self, unattached_volumes_check, mock_provider, sample_volumes
    ):
        """Test running check with unattached volumes."""
        # Mock volume info responses
        mock_provider.get_volume_info.side_effect = [
            {
                "attached": False,
                "detached_at": datetime.now(timezone.utc) - timedelta(days=10),
                "size_gb": 100,
                "volume_type": "gp3",
            },
            {
                "attached": True,  # This one is attached
            },
            {
                "attached": False,
                "detached_at": datetime.now(timezone.utc) - timedelta(days=30),
                "size_gb": 200,
                "volume_type": "gp2",
            },
        ]
        
        results = await unattached_volumes_check.run(mock_provider, sample_volumes)
        
        assert len(results) == 2  # Two unattached volumes
        
        # Check first result
        result1 = results[0]
        assert result1.resource.id == "vol-1234"
        assert result1.monthly_savings == Decimal("50.00")
        assert result1.annual_savings == Decimal("600.00")
        assert result1.savings_percentage == 100.0
        assert result1.severity == CheckSeverity.MEDIUM
        assert "10 days" in result1.description
        
        # Check second result
        result2 = results[1]
        assert result2.resource.id == "vol-9012"
        assert result2.monthly_savings == Decimal("200.00")
        assert result2.annual_savings == Decimal("2400.00")
        assert result2.severity == CheckSeverity.HIGH
        assert "30 days" in result2.description

    @pytest.mark.asyncio
    async def test_run_with_recently_detached_volumes(
        self, unattached_volumes_check, mock_provider, sample_volumes
    ):
        """Test that recently detached volumes are not flagged."""
        # Mock volume info - detached only 3 days ago
        mock_provider.get_volume_info.return_value = {
            "attached": False,
            "detached_at": datetime.now(timezone.utc) - timedelta(days=3),
            "size_gb": 100,
            "volume_type": "gp3",
        }
        
        results = await unattached_volumes_check.run(
            mock_provider, [sample_volumes[0]]
        )
        
        assert len(results) == 0  # Should not flag volumes detached < 7 days

    @pytest.mark.asyncio
    async def test_run_with_region_filter(
        self, unattached_volumes_check, mock_provider, sample_volumes
    ):
        """Test running check with region filter."""
        mock_provider.get_volume_info.return_value = {
            "attached": False,
            "detached_at": datetime.now(timezone.utc) - timedelta(days=10),
            "size_gb": 100,
            "volume_type": "gp3",
        }
        
        results = await unattached_volumes_check.run(
            mock_provider, sample_volumes, region="us-west-2"
        )
        
        # Should only check volumes in us-west-2
        assert len(results) == 1
        assert results[0].resource.id == "vol-9012"

    def test_calculate_severity(self, unattached_volumes_check):
        """Test severity calculation."""
        assert (
            unattached_volumes_check._calculate_severity(Decimal("600"))
            == CheckSeverity.CRITICAL
        )
        assert (
            unattached_volumes_check._calculate_severity(Decimal("200"))
            == CheckSeverity.HIGH
        )
        assert (
            unattached_volumes_check._calculate_severity(Decimal("50"))
            == CheckSeverity.MEDIUM
        )