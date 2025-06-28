"""Tests for reserved instances utilization check."""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock

from src.checks.cost_optimization.reserved_instances import ReservedInstancesUtilizationCheck
from src.models.base import CloudProvider, Resource, ResourceType
from src.models.checks import CheckSeverity


@pytest.fixture
def ri_check():
    """Create a reserved instances check instance."""
    return ReservedInstancesUtilizationCheck(min_utilization_percent=80.0)


@pytest.fixture
def mock_provider():
    """Create a mock cloud provider."""
    provider = AsyncMock()
    provider.provider = CloudProvider.AWS
    return provider


@pytest.fixture
def sample_instances():
    """Create sample instance resources."""
    return [
        Resource(
            id="i-1234",
            name="WebServer1",
            type=ResourceType.INSTANCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="running",
            monthly_cost=Decimal("100.00"),
            is_active=True,
        ),
        Resource(
            id="i-5678",
            name="WebServer2",
            type=ResourceType.INSTANCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="running",
            monthly_cost=Decimal("100.00"),
            is_active=True,
        ),
    ]


class TestReservedInstancesUtilizationCheck:
    """Test reserved instances utilization check."""

    def test_check_properties(self, ri_check):
        """Test check properties."""
        assert ri_check.name == "Reserved Instances Utilization"
        assert ri_check.check_type.value == "reserved_instance_optimization"
        assert CloudProvider.AWS in ri_check.supported_providers

    def test_filter_resources(self, ri_check, sample_instances):
        """Test resource filtering."""
        # Add non-instance resources
        resources = sample_instances + [
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
        
        filtered = ri_check.filter_resources(resources)
        assert len(filtered) == 2
        assert all(r.type == ResourceType.INSTANCE for r in filtered)

    @pytest.mark.asyncio
    async def test_run_with_underutilized_ris(
        self, ri_check, mock_provider, sample_instances
    ):
        """Test running check with underutilized reserved instances."""
        # Mock RI utilization data
        mock_provider.get_reserved_instances_utilization.return_value = {
            "underutilized": [
                {
                    "reservation_id": "ri-1234",
                    "instance_type": "m5.large",
                    "region": "us-east-1",
                    "utilization_percentage": 60.0,
                    "monthly_cost": 1000.0,
                    "instance_count": 10,
                    "platform": "Linux/UNIX",
                    "expiration_date": "2024-12-31",
                },
                {
                    "reservation_id": "ri-5678",
                    "instance_type": "t3.medium",
                    "region": "us-west-2",
                    "utilization_percentage": 40.0,
                    "monthly_cost": 500.0,
                    "instance_count": 5,
                    "platform": "Linux/UNIX",
                },
            ]
        }
        
        # Mock on-demand opportunities
        mock_provider.get_on_demand_ri_opportunities.return_value = []
        
        results = await ri_check.run(mock_provider, sample_instances)
        
        assert len(results) == 2
        
        # Check first underutilized RI
        result1 = results[0]
        assert "ri-1234" in result1.id
        assert result1.monthly_savings == Decimal("400.00")  # 40% waste
        assert result1.severity == CheckSeverity.HIGH
        assert "60.0% utilized" in result1.description
        assert result1.effort_level == "medium"
        
        # Check second underutilized RI
        result2 = results[1]
        assert "ri-5678" in result2.id
        assert result2.monthly_savings == Decimal("300.00")  # 60% waste
        assert result2.severity == CheckSeverity.HIGH
        assert "40.0% utilized" in result2.description

    @pytest.mark.asyncio
    async def test_run_with_ri_opportunities(
        self, ri_check, mock_provider, sample_instances
    ):
        """Test running check with RI purchase opportunities."""
        # No underutilized RIs
        mock_provider.get_reserved_instances_utilization.return_value = {
            "underutilized": []
        }
        
        # Mock on-demand opportunities
        mock_provider.get_on_demand_ri_opportunities.return_value = [
            {
                "instance_type": "m5.large",
                "region": "us-east-1",
                "instance_count": 20,
                "on_demand_monthly_cost": 2000.0,
                "estimated_monthly_savings": 600.0,
                "savings_percentage": 30.0,
                "recommended_term": "1-year",
                "break_even_months": 8,
            },
            {
                "instance_type": "t3.large",
                "region": "us-west-2",
                "instance_count": 10,
                "on_demand_monthly_cost": 800.0,
                "estimated_monthly_savings": 200.0,
                "savings_percentage": 25.0,
                "recommended_term": "3-year",
                "break_even_months": 10,
            },
        ]
        
        results = await ri_check.run(mock_provider, sample_instances)
        
        assert len(results) == 2
        
        # Check first opportunity
        result1 = results[0]
        assert "m5.large" in result1.title
        assert result1.monthly_savings == Decimal("600.00")
        assert result1.severity == CheckSeverity.CRITICAL
        assert "20 on-demand instances" in result1.description
        assert "30%" in result1.description
        assert result1.effort_level == "low"
        
        # Check second opportunity
        result2 = results[1]
        assert "t3.large" in result2.title
        assert result2.monthly_savings == Decimal("200.00")
        assert result2.severity == CheckSeverity.HIGH

    @pytest.mark.asyncio
    async def test_run_with_well_utilized_ris(
        self, ri_check, mock_provider, sample_instances
    ):
        """Test that well-utilized RIs are not flagged."""
        # Mock RI with good utilization
        mock_provider.get_reserved_instances_utilization.return_value = {
            "underutilized": [
                {
                    "reservation_id": "ri-9999",
                    "instance_type": "m5.large",
                    "utilization_percentage": 95.0,  # Above threshold
                    "monthly_cost": 1000.0,
                }
            ]
        }
        
        mock_provider.get_on_demand_ri_opportunities.return_value = []
        
        results = await ri_check.run(mock_provider, sample_instances)
        
        assert len(results) == 0  # Should not flag well-utilized RIs

    def test_calculate_severity(self, ri_check):
        """Test severity calculation."""
        assert (
            ri_check._calculate_severity(Decimal("600"))
            == CheckSeverity.CRITICAL
        )
        assert (
            ri_check._calculate_severity(Decimal("200"))
            == CheckSeverity.HIGH
        )
        assert (
            ri_check._calculate_severity(Decimal("50"))
            == CheckSeverity.MEDIUM
        )