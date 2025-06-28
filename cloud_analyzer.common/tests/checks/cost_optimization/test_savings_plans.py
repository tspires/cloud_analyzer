"""Tests for savings plans coverage check."""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock

from src.checks.cost_optimization.savings_plans import SavingsPlansCoverageCheck
from src.models.base import CloudProvider, Resource, ResourceType
from src.models.checks import CheckSeverity


@pytest.fixture
def sp_check():
    """Create a savings plans check instance."""
    return SavingsPlansCoverageCheck(target_coverage_percent=70.0)


@pytest.fixture
def mock_provider():
    """Create a mock cloud provider."""
    provider = AsyncMock()
    provider.provider = CloudProvider.AWS
    return provider


@pytest.fixture
def sample_resources():
    """Create sample compute resources."""
    return [
        Resource(
            id="i-1234",
            name="WebServer",
            type=ResourceType.INSTANCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="running",
            monthly_cost=Decimal("100.00"),
            is_active=True,
        ),
        Resource(
            id="func-5678",
            name="APIFunction",
            type=ResourceType.FUNCTION,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="active",
            monthly_cost=Decimal("50.00"),
            is_active=True,
        ),
        Resource(
            id="vol-9012",
            name="Storage",
            type=ResourceType.VOLUME,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="available",
            monthly_cost=Decimal("20.00"),
            is_active=True,
        ),
    ]


class TestSavingsPlansCoverageCheck:
    """Test savings plans coverage check."""

    def test_check_properties(self, sp_check):
        """Test check properties."""
        assert sp_check.name == "Savings Plans Coverage Analysis"
        assert sp_check.check_type.value == "savings_plan_optimization"
        assert CloudProvider.AWS in sp_check.supported_providers

    def test_filter_resources(self, sp_check, sample_resources):
        """Test resource filtering to compute resources only."""
        filtered = sp_check.filter_resources(sample_resources)
        assert len(filtered) == 2  # Instance and Function only
        assert all(
            r.type in [ResourceType.INSTANCE, ResourceType.FUNCTION, ResourceType.CONTAINER]
            for r in filtered
        )

    @pytest.mark.asyncio
    async def test_run_with_low_coverage(
        self, sp_check, mock_provider, sample_resources
    ):
        """Test running check with low savings plans coverage."""
        # Mock low coverage data
        mock_provider.get_savings_plans_coverage.return_value = {
            "coverage_percentage": 40.0,  # Below target of 70%
            "total_compute_spend": 10000.0,
            "covered_spend": 4000.0,
            "on_demand_spend": 6000.0,
            "expiring_plans": [],
        }
        
        results = await sp_check.run(mock_provider, sample_resources)
        
        assert len(results) == 1
        
        result = results[0]
        assert result.id == "sp-coverage-opportunity"
        assert "40.0%" in result.description
        assert "70.0%" in result.description
        assert result.severity == CheckSeverity.CRITICAL
        
        # Check savings calculation (30% additional coverage * 25% savings rate)
        assert result.monthly_savings == Decimal("750.00")
        assert result.annual_savings == Decimal("9000.00")
        assert result.effort_level == "low"

    @pytest.mark.asyncio
    async def test_run_with_good_coverage(
        self, sp_check, mock_provider, sample_resources
    ):
        """Test that good coverage doesn't generate recommendations."""
        # Mock good coverage data
        mock_provider.get_savings_plans_coverage.return_value = {
            "coverage_percentage": 85.0,  # Above target of 70%
            "total_compute_spend": 10000.0,
            "covered_spend": 8500.0,
            "on_demand_spend": 1500.0,
            "expiring_plans": [],
        }
        
        results = await sp_check.run(mock_provider, sample_resources)
        
        assert len(results) == 0  # No recommendations for good coverage

    @pytest.mark.asyncio
    async def test_run_with_expiring_plans(
        self, sp_check, mock_provider, sample_resources
    ):
        """Test detection of expiring savings plans."""
        # Mock data with expiring plans
        mock_provider.get_savings_plans_coverage.return_value = {
            "coverage_percentage": 75.0,  # Good coverage
            "total_compute_spend": 10000.0,
            "covered_spend": 7500.0,
            "on_demand_spend": 2500.0,
            "expiring_plans": [
                {
                    "plan_id": "sp-1234",
                    "plan_type": "Compute",
                    "days_until_expiry": 30,
                    "monthly_commitment": 1000.0,
                    "utilization_percentage": 95.0,
                    "expiry_date": "2024-01-30",
                },
                {
                    "plan_id": "sp-5678",
                    "plan_type": "EC2 Instance",
                    "days_until_expiry": 45,
                    "monthly_commitment": 500.0,
                    "utilization_percentage": 90.0,
                    "expiry_date": "2024-02-14",
                },
                {
                    "plan_id": "sp-9012",
                    "plan_type": "Compute",
                    "days_until_expiry": 90,  # Too far out
                    "monthly_commitment": 200.0,
                },
            ],
        }
        
        results = await sp_check.run(mock_provider, sample_resources)
        
        assert len(results) == 2  # Only plans expiring within 60 days
        
        # Check first expiring plan (30 days)
        result1 = results[0]
        assert "sp-1234" in result1.id
        assert result1.severity == CheckSeverity.HIGH  # <= 30 days
        assert "30 days" in result1.description
        assert "$1,000.00" in result1.description
        
        # Check second expiring plan (45 days)
        result2 = results[1]
        assert "sp-5678" in result2.id
        assert result2.severity == CheckSeverity.MEDIUM  # > 30 days
        assert "45 days" in result2.description

    @pytest.mark.asyncio
    async def test_run_with_region_filter(
        self, sp_check, mock_provider, sample_resources
    ):
        """Test that region filter doesn't affect global savings plans."""
        mock_provider.get_savings_plans_coverage.return_value = {
            "coverage_percentage": 40.0,
            "total_compute_spend": 10000.0,
            "covered_spend": 4000.0,
            "on_demand_spend": 6000.0,
            "expiring_plans": [],
        }
        
        # Savings plans are global, so region filter shouldn't matter
        results = await sp_check.run(mock_provider, sample_resources, region="us-west-2")
        
        assert len(results) == 1
        assert results[0].resource.region == "global"

    def test_calculate_severity(self, sp_check):
        """Test severity calculation."""
        assert (
            sp_check._calculate_severity(Decimal("600"))
            == CheckSeverity.CRITICAL
        )
        assert (
            sp_check._calculate_severity(Decimal("200"))
            == CheckSeverity.HIGH
        )
        assert (
            sp_check._calculate_severity(Decimal("50"))
            == CheckSeverity.MEDIUM
        )