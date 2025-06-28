"""Simple test to verify check functionality."""

import sys
import os

# Add the source directories to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../cloud_analyzer.common/src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from datetime import datetime, timedelta
from decimal import Decimal
import pytest

from checks.storage.unattached_volumes import UnattachedVolumesCheck
from models.base import CloudProvider, Resource, ResourceType
from models.checks import CheckSeverity


class TestSimpleCheck:
    """Simple test for check functionality."""
    
    @pytest.mark.asyncio
    async def test_unattached_volume_check(self):
        """Test unattached volume check."""
        from unittest.mock import AsyncMock
        
        # Create a mock provider
        mock_provider = AsyncMock()
        mock_provider.provider = CloudProvider.AWS
        
        # Create test resources
        resources = [
            Resource(
                id="vol-1234",
                name="TestVolume",
                type=ResourceType.VOLUME,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="available",
                monthly_cost=Decimal("50.00"),
                is_active=True,
            )
        ]
        
        # Mock volume info
        mock_provider.get_volume_info.return_value = {
            "attached": False,
            "detached_at": datetime.utcnow() - timedelta(days=10),
            "size_gb": 100,
            "volume_type": "gp3",
        }
        
        # Run the check
        check = UnattachedVolumesCheck()
        results = await check.run(mock_provider, resources)
        
        # Verify results
        assert len(results) == 1
        assert results[0].check_type.value == "unattached_volume"
        assert results[0].monthly_savings == Decimal("50.00")
        assert results[0].severity == CheckSeverity.MEDIUM
        print(f"✓ Unattached volume check passed: {results[0].title}")
    
    @pytest.mark.asyncio
    async def test_check_properties(self):
        """Test check properties."""
        check = UnattachedVolumesCheck()
        
        assert check.name == "Unattached Volume Detection"
        assert CloudProvider.AWS in check.supported_providers
        assert CloudProvider.AZURE in check.supported_providers
        assert CloudProvider.GCP in check.supported_providers
        print("✓ Check properties verified")