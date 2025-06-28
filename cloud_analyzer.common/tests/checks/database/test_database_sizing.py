"""Tests for database sizing check."""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock

from src.checks.database.database_sizing import DatabaseSizingCheck
from src.models.base import CloudProvider, Resource, ResourceType
from src.models.checks import CheckSeverity


@pytest.fixture
def db_sizing_check():
    """Create a database sizing check instance."""
    return DatabaseSizingCheck(
        cpu_threshold=30.0,
        memory_threshold=30.0,
        days_to_check=7
    )


@pytest.fixture
def mock_provider():
    """Create a mock cloud provider."""
    provider = AsyncMock()
    provider.provider = CloudProvider.AWS
    return provider


@pytest.fixture
def sample_databases():
    """Create sample database resources."""
    return [
        Resource(
            id="db-1234",
            name="ProductionDB",
            type=ResourceType.DATABASE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="available",
            monthly_cost=Decimal("500.00"),
            is_active=True,
        ),
        Resource(
            id="db-5678",
            name="AnalyticsDB",
            type=ResourceType.DATABASE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="available",
            monthly_cost=Decimal("1000.00"),
            is_active=True,
        ),
        Resource(
            id="db-9012",
            name="TestDB",
            type=ResourceType.DATABASE,
            provider=CloudProvider.AWS,
            region="us-west-2",
            state="stopped",
            monthly_cost=Decimal("200.00"),
            is_active=False,
        ),
    ]


class TestDatabaseSizingCheck:
    """Test database sizing check."""

    def test_check_properties(self, db_sizing_check):
        """Test check properties."""
        assert db_sizing_check.name == "Database Right-Sizing"
        assert db_sizing_check.check_type.value == "right_sizing"
        assert CloudProvider.AWS in db_sizing_check.supported_providers

    def test_filter_resources(self, db_sizing_check, sample_databases):
        """Test resource filtering to active databases only."""
        # Add non-database resources
        resources = sample_databases + [
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
        
        filtered = db_sizing_check.filter_resources(resources)
        assert len(filtered) == 2  # Only active databases
        assert all(r.type == ResourceType.DATABASE and r.is_active for r in filtered)

    @pytest.mark.asyncio
    async def test_run_with_oversized_databases(
        self, db_sizing_check, mock_provider, sample_databases
    ):
        """Test running check with oversized databases."""
        # Mock metrics for databases
        mock_provider.get_database_metrics.side_effect = [
            {
                "avg_cpu_percent": 15.0,
                "avg_memory_percent": 20.0,
                "max_cpu_percent": 45.0,
                "max_memory_percent": 55.0,
            },
            {
                "avg_cpu_percent": 25.0,
                "avg_memory_percent": 28.0,
                "max_cpu_percent": 85.0,
                "max_memory_percent": 88.0,
            },
        ]
        
        # Mock database info
        mock_provider.get_database_info.side_effect = [
            {
                "instance_type": "db.r5.2xlarge",
                "engine": "postgres",
                "engine_version": "13.7",
                "multi_az": True,
                "storage_type": "gp3",
                "allocated_storage_gb": 500,
            },
            {
                "instance_type": "db.m5.4xlarge",
                "engine": "mysql",
                "engine_version": "8.0",
                "multi_az": False,
                "storage_type": "io1",
                "allocated_storage_gb": 1000,
            },
        ]
        
        # Mock sizing recommendations
        mock_provider.get_database_sizing_recommendations.side_effect = [
            [
                {
                    "instance_type": "db.r5.xlarge",
                    "monthly_cost": 300.0,
                }
            ],
            [
                {
                    "instance_type": "db.m5.2xlarge",
                    "monthly_cost": 600.0,
                }
            ],
        ]
        
        results = await db_sizing_check.run(mock_provider, sample_databases[:2])
        
        assert len(results) == 2
        
        # Check first result
        result1 = results[0]
        assert result1.resource.id == "db-1234"
        assert result1.monthly_savings == Decimal("200.00")
        assert result1.severity == CheckSeverity.HIGH
        assert "db.r5.2xlarge" in result1.description
        assert "db.r5.xlarge" in result1.description
        assert "15.0%" in result1.description
        assert result1.risk_level == "low"  # Max CPU/memory < 80%
        
        # Check second result
        result2 = results[1]
        assert result2.resource.id == "db-5678"
        assert result2.monthly_savings == Decimal("400.00")
        assert result2.severity == CheckSeverity.HIGH
        assert result2.risk_level == "medium"  # Max CPU/memory > 80%

    @pytest.mark.asyncio
    async def test_run_with_properly_sized_database(
        self, db_sizing_check, mock_provider, sample_databases
    ):
        """Test that properly sized databases are not flagged."""
        # Mock metrics showing good utilization
        mock_provider.get_database_metrics.return_value = {
            "avg_cpu_percent": 45.0,  # Above threshold
            "avg_memory_percent": 50.0,  # Above threshold
            "max_cpu_percent": 75.0,
            "max_memory_percent": 80.0,
        }
        
        results = await db_sizing_check.run(mock_provider, [sample_databases[0]])
        
        assert len(results) == 0  # Should not flag well-utilized databases

    @pytest.mark.asyncio
    async def test_run_with_small_savings(
        self, db_sizing_check, mock_provider, sample_databases
    ):
        """Test that databases with small savings are not flagged."""
        # Mock low utilization metrics
        mock_provider.get_database_metrics.return_value = {
            "avg_cpu_percent": 20.0,
            "avg_memory_percent": 25.0,
            "max_cpu_percent": 40.0,
            "max_memory_percent": 45.0,
        }
        
        mock_provider.get_database_info.return_value = {
            "instance_type": "db.t3.medium",
        }
        
        # Mock recommendation with minimal savings
        mock_provider.get_database_sizing_recommendations.return_value = [
            {
                "instance_type": "db.t3.small",
                "monthly_cost": 480.0,  # Only $20 savings (4%)
            }
        ]
        
        results = await db_sizing_check.run(mock_provider, [sample_databases[0]])
        
        assert len(results) == 0  # Should not flag < 10% savings

    @pytest.mark.asyncio
    async def test_run_with_high_risk_database(
        self, db_sizing_check, mock_provider, sample_databases
    ):
        """Test risk level calculation for high peak usage."""
        # Mock metrics with high peak usage
        mock_provider.get_database_metrics.return_value = {
            "avg_cpu_percent": 25.0,
            "avg_memory_percent": 28.0,
            "max_cpu_percent": 92.0,  # Very high peak
            "max_memory_percent": 95.0,  # Very high peak
        }
        
        mock_provider.get_database_info.return_value = {
            "instance_type": "db.m5.2xlarge",
        }
        
        mock_provider.get_database_sizing_recommendations.return_value = [
            {
                "instance_type": "db.m5.xlarge",
                "monthly_cost": 300.0,
            }
        ]
        
        results = await db_sizing_check.run(mock_provider, [sample_databases[0]])
        
        assert len(results) == 1
        assert results[0].risk_level == "high"  # Due to high peak usage

    @pytest.mark.asyncio
    async def test_run_with_region_filter(
        self, db_sizing_check, mock_provider, sample_databases
    ):
        """Test running check with region filter."""
        mock_provider.get_database_metrics.return_value = {
            "avg_cpu_percent": 20.0,
            "avg_memory_percent": 25.0,
            "max_cpu_percent": 40.0,
            "max_memory_percent": 45.0,
        }
        
        mock_provider.get_database_info.return_value = {
            "instance_type": "db.m5.xlarge",
        }
        
        mock_provider.get_database_sizing_recommendations.return_value = [
            {
                "instance_type": "db.m5.large",
                "monthly_cost": 150.0,
            }
        ]
        
        # Filter to us-west-2 (only inactive database is there)
        # First filter resources like CheckRunner would do
        filtered = db_sizing_check.filter_resources(sample_databases)
        results = await db_sizing_check.run(
            mock_provider, filtered, region="us-west-2"
        )
        
        assert len(results) == 0  # Inactive database is filtered out

    def test_calculate_severity(self, db_sizing_check):
        """Test severity calculation."""
        assert (
            db_sizing_check._calculate_severity(Decimal("600"))
            == CheckSeverity.CRITICAL
        )
        assert (
            db_sizing_check._calculate_severity(Decimal("200"))
            == CheckSeverity.HIGH
        )
        assert (
            db_sizing_check._calculate_severity(Decimal("50"))
            == CheckSeverity.MEDIUM
        )