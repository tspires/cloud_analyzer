"""Integration tests for full workflow with all new checks."""

import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.checks.registry import check_registry
from src.checks.storage.unattached_volumes import UnattachedVolumesCheck
from src.checks.storage.old_snapshots import OldSnapshotsCheck
from src.checks.cost_optimization.reserved_instances import ReservedInstancesUtilizationCheck
from src.checks.cost_optimization.savings_plans import SavingsPlansCoverageCheck
from src.checks.database.database_sizing import DatabaseSizingCheck
from src.models.base import CloudProvider, Resource, ResourceType
from src.providers.base import CloudProviderInterface


class MockAWSProvider(CloudProviderInterface):
    """Mock AWS provider for integration testing."""
    
    def __init__(self, credentials):
        super().__init__(credentials)
        self._volumes = []
        self._snapshots = []
        self._databases = []
        self._instances = []
    
    @property
    def provider(self) -> CloudProvider:
        return CloudProvider.AWS
    
    async def validate_credentials(self) -> bool:
        return True
    
    async def list_regions(self) -> list[str]:
        return ["us-east-1", "us-west-2", "eu-west-1"]
    
    async def list_resources(self, region=None, resource_types=None):
        """Return all mock resources."""
        resources = []
        resources.extend(self._volumes)
        resources.extend(self._snapshots)
        resources.extend(self._databases)
        resources.extend(self._instances)
        
        if region:
            resources = [r for r in resources if r.region == region]
        
        return resources
    
    async def list_instances(self, region: str):
        return [r for r in self._instances if r.region == region]
    
    async def list_volumes(self, region: str):
        return [r for r in self._volumes if r.region == region]
    
    async def list_snapshots(self, region: str):
        return [r for r in self._snapshots if r.region == region]
    
    async def list_databases(self, region: str):
        return [r for r in self._databases if r.region == region]
    
    async def list_load_balancers(self, region: str):
        return []
    
    async def list_ip_addresses(self, region: str):
        return []
    
    async def get_instance_metrics(self, instance_id: str, region: str, days: int = 7):
        return {
            "avg_cpu_percent": 45.0,
            "avg_memory_percent": 50.0,
            "avg_network_bytes": 1000000,
        }
    
    async def get_volume_metrics(self, volume_id: str, region: str, days: int = 7):
        return {}
    
    async def get_volume_info(self, volume_id: str, region: str):
        """Return volume info based on ID."""
        if volume_id == "vol-unattached-old":
            return {
                "attached": False,
                "detached_at": datetime.utcnow() - timedelta(days=30),
                "size_gb": 100,
                "volume_type": "gp3",
            }
        elif volume_id == "vol-unattached-new":
            return {
                "attached": False,
                "detached_at": datetime.utcnow() - timedelta(days=3),
                "size_gb": 50,
                "volume_type": "gp2",
            }
        else:
            return {"attached": True}
    
    async def get_snapshot_info(self, snapshot_id: str, region: str):
        """Return snapshot info based on ID."""
        if snapshot_id == "snap-old":
            return {
                "created_at": datetime.utcnow() - timedelta(days=90),
                "size_gb": 200,
                "is_ami_snapshot": False,
                "has_backup_policy": False,
                "volume_id": "vol-deleted",
            }
        elif snapshot_id == "snap-ami":
            return {
                "created_at": datetime.utcnow() - timedelta(days=60),
                "size_gb": 100,
                "is_ami_snapshot": True,
                "has_backup_policy": False,
            }
        else:
            return {
                "created_at": datetime.utcnow() - timedelta(days=10),
                "size_gb": 50,
            }
    
    async def get_database_metrics(self, database_id: str, region: str, days: int = 7):
        """Return database metrics based on ID."""
        if database_id == "db-oversized":
            return {
                "avg_cpu_percent": 15.0,
                "avg_memory_percent": 20.0,
                "max_cpu_percent": 45.0,
                "max_memory_percent": 50.0,
            }
        else:
            return {
                "avg_cpu_percent": 60.0,
                "avg_memory_percent": 70.0,
                "max_cpu_percent": 85.0,
                "max_memory_percent": 90.0,
            }
    
    async def get_database_info(self, database_id: str, region: str):
        """Return database info."""
        return {
            "instance_type": "db.r5.2xlarge",
            "engine": "postgres",
            "engine_version": "13.7",
            "multi_az": True,
            "storage_type": "gp3",
            "allocated_storage_gb": 500,
        }
    
    async def get_database_sizing_recommendations(
        self, database_id: str, region: str,
        target_cpu_utilization: float = 50.0,
        target_memory_utilization: float = 60.0
    ):
        """Return sizing recommendations."""
        if database_id == "db-oversized":
            return [
                {
                    "instance_type": "db.r5.xlarge",
                    "monthly_cost": 300.0,
                },
                {
                    "instance_type": "db.r5.large",
                    "monthly_cost": 150.0,
                },
            ]
        return []
    
    async def get_reserved_instances_utilization(self, region=None):
        """Return RI utilization data."""
        return {
            "underutilized": [
                {
                    "reservation_id": "ri-underused",
                    "instance_type": "m5.large",
                    "region": "us-east-1",
                    "utilization_percentage": 60.0,
                    "monthly_cost": 1000.0,
                    "instance_count": 10,
                    "platform": "Linux/UNIX",
                    "expiration_date": "2025-12-31",
                },
            ]
        }
    
    async def get_on_demand_ri_opportunities(self, resources, region=None):
        """Return RI opportunities."""
        return [
            {
                "instance_type": "m5.xlarge",
                "region": "us-east-1",
                "instance_count": 20,
                "on_demand_monthly_cost": 2000.0,
                "estimated_monthly_savings": 600.0,
                "savings_percentage": 30.0,
                "recommended_term": "1-year",
                "break_even_months": 8,
            },
        ]
    
    async def get_savings_plans_coverage(self, region=None):
        """Return savings plans coverage data."""
        return {
            "coverage_percentage": 40.0,
            "total_compute_spend": 10000.0,
            "covered_spend": 4000.0,
            "on_demand_spend": 6000.0,
            "expiring_plans": [
                {
                    "plan_id": "sp-expiring",
                    "plan_type": "Compute",
                    "days_until_expiry": 30,
                    "monthly_commitment": 1000.0,
                    "utilization_percentage": 95.0,
                    "expiry_date": "2024-02-01",
                },
            ],
        }
    
    async def estimate_monthly_cost(self, resource: Resource) -> float:
        return float(resource.monthly_cost)
    
    def add_test_resources(self):
        """Add test resources for integration testing."""
        # Add volumes
        self._volumes = [
            Resource(
                id="vol-unattached-old",
                name="OldUnattachedVolume",
                type=ResourceType.VOLUME,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="available",
                monthly_cost=Decimal("75.00"),
                is_active=True,
            ),
            Resource(
                id="vol-unattached-new",
                name="NewUnattachedVolume",
                type=ResourceType.VOLUME,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="available",
                monthly_cost=Decimal("25.00"),
                is_active=True,
            ),
            Resource(
                id="vol-attached",
                name="AttachedVolume",
                type=ResourceType.VOLUME,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="in-use",
                monthly_cost=Decimal("100.00"),
                is_active=True,
            ),
        ]
        
        # Add snapshots
        self._snapshots = [
            Resource(
                id="snap-old",
                name="VeryOldSnapshot",
                type=ResourceType.SNAPSHOT,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="completed",
                monthly_cost=Decimal("30.00"),
                is_active=True,
            ),
            Resource(
                id="snap-ami",
                name="AMISnapshot",
                type=ResourceType.SNAPSHOT,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="completed",
                monthly_cost=Decimal("20.00"),
                is_active=True,
            ),
            Resource(
                id="snap-recent",
                name="RecentSnapshot",
                type=ResourceType.SNAPSHOT,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="completed",
                monthly_cost=Decimal("10.00"),
                is_active=True,
            ),
        ]
        
        # Add databases
        self._databases = [
            Resource(
                id="db-oversized",
                name="OversizedDatabase",
                type=ResourceType.DATABASE,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="available",
                monthly_cost=Decimal("500.00"),
                is_active=True,
            ),
            Resource(
                id="db-rightsized",
                name="RightSizedDatabase",
                type=ResourceType.DATABASE,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="available",
                monthly_cost=Decimal("400.00"),
                is_active=True,
            ),
        ]
        
        # Add instances
        self._instances = [
            Resource(
                id="i-ondemand-1",
                name="OnDemandInstance1",
                type=ResourceType.INSTANCE,
                provider=CloudProvider.AWS,
                region="us-east-1",
                state="running",
                monthly_cost=Decimal("150.00"),
                is_active=True,
            ),
        ]


class TestFullWorkflowIntegration:
    """Test full workflow with all checks integrated."""
    
    @pytest.fixture
    def mock_provider(self):
        """Create a mock AWS provider with test data."""
        provider = MockAWSProvider({"access_key": "test"})
        provider.add_test_resources()
        return provider
    
    @pytest.mark.asyncio
    async def test_full_workflow_all_checks(self, mock_provider):
        """Test running all checks in a full workflow."""
        from src.checks.base import CheckRunner
        
        # Get all registered checks
        all_checks = [
            UnattachedVolumesCheck(),
            OldSnapshotsCheck(),
            ReservedInstancesUtilizationCheck(),
            SavingsPlansCoverageCheck(),
            DatabaseSizingCheck(),
        ]
        
        # Create check runner
        runner = CheckRunner(mock_provider)
        
        # Get all resources
        resources = await mock_provider.list_resources()
        
        # Run all checks
        all_results = []
        for check in all_checks:
            results = await runner.run_check(check, resources)
            all_results.extend(results)
        
        # Verify results
        assert len(all_results) > 0
        
        # Check for unattached volumes
        unattached_volume_results = [
            r for r in all_results
            if r.check_type == CheckType.UNATTACHED_VOLUME
        ]
        assert len(unattached_volume_results) == 1  # Only old unattached volume
        assert unattached_volume_results[0].resource.id == "vol-unattached-old"
        assert unattached_volume_results[0].monthly_savings == Decimal("75.00")
        
        # Check for old snapshots
        old_snapshot_results = [
            r for r in all_results
            if r.check_type == CheckType.OLD_SNAPSHOT
        ]
        assert len(old_snapshot_results) == 2  # Old snapshot and AMI snapshot
        assert any(r.resource.id == "snap-old" for r in old_snapshot_results)
        assert any(r.resource.id == "snap-ami" for r in old_snapshot_results)
        
        # Check for RI optimization
        ri_results = [
            r for r in all_results
            if r.check_type == CheckType.RESERVED_INSTANCE_OPTIMIZATION
        ]
        assert len(ri_results) >= 2  # Underutilized RI + opportunity
        
        # Check for savings plans
        sp_results = [
            r for r in all_results
            if r.check_type == CheckType.SAVINGS_PLAN_OPTIMIZATION
        ]
        assert len(sp_results) >= 2  # Low coverage + expiring plan
        
        # Check for database sizing
        db_results = [
            r for r in all_results
            if r.check_type == CheckType.RIGHT_SIZING
        ]
        assert len(db_results) == 1  # Only oversized database
        assert db_results[0].resource.id == "db-oversized"
        assert db_results[0].monthly_savings == Decimal("200.00")
    
    @pytest.mark.asyncio
    async def test_total_savings_calculation(self, mock_provider):
        """Test calculating total potential savings across all checks."""
        from src.checks.base import CheckRunner
        
        all_checks = [
            UnattachedVolumesCheck(),
            OldSnapshotsCheck(),
            DatabaseSizingCheck(),
        ]
        
        runner = CheckRunner(mock_provider)
        resources = await mock_provider.list_resources()
        
        # Run checks and calculate total savings
        total_monthly_savings = Decimal("0")
        total_annual_savings = Decimal("0")
        
        for check in all_checks:
            results = await runner.run_check(check, resources)
            for result in results:
                total_monthly_savings += result.monthly_savings
                total_annual_savings += result.annual_savings
        
        # Verify expected savings
        # Unattached volume: $75
        # Old snapshots: $30 + $20 = $50
        # Database sizing: $200
        # Total: $325/month
        assert total_monthly_savings == Decimal("325.00")
        assert total_annual_savings == Decimal("3900.00")
    
    @pytest.mark.asyncio
    async def test_region_filtering(self, mock_provider):
        """Test that region filtering works correctly."""
        from src.checks.base import CheckRunner
        
        # Add a resource in a different region
        mock_provider._volumes.append(
            Resource(
                id="vol-eu-west",
                name="EuropeVolume",
                type=ResourceType.VOLUME,
                provider=CloudProvider.AWS,
                region="eu-west-1",
                state="available",
                monthly_cost=Decimal("50.00"),
                is_active=True,
            )
        )
        
        check = UnattachedVolumesCheck()
        runner = CheckRunner(mock_provider)
        resources = await mock_provider.list_resources()
        
        # Run check with region filter
        results = await runner.run_check(check, resources, region="us-east-1")
        
        # Should not include EU volume
        assert all(r.resource.region == "us-east-1" for r in results)
        assert not any(r.resource.id == "vol-eu-west" for r in results)
    
    @pytest.mark.asyncio
    async def test_error_recovery(self, mock_provider):
        """Test that checks handle errors gracefully."""
        from src.checks.base import CheckRunner
        
        # Create a check that will encounter an error
        check = DatabaseSizingCheck()
        runner = CheckRunner(mock_provider)
        
        # Mock an error in get_database_info
        mock_provider.get_database_info = AsyncMock(
            side_effect=Exception("Database API error")
        )
        
        resources = await mock_provider.list_resources()
        
        # Should handle error gracefully and return empty results
        results = await runner.run_check(check, resources)
        assert len(results) == 0  # No results due to error
    
    @pytest.mark.asyncio
    async def test_check_priority_scoring(self, mock_provider):
        """Test that check results are properly prioritized."""
        from src.checks.base import CheckRunner
        
        all_checks = [
            UnattachedVolumesCheck(),
            DatabaseSizingCheck(),
        ]
        
        runner = CheckRunner(mock_provider)
        resources = await mock_provider.list_resources()
        
        all_results = []
        for check in all_checks:
            results = await runner.run_check(check, resources)
            all_results.extend(results)
        
        # Sort by priority score
        sorted_results = sorted(
            all_results,
            key=lambda r: r.priority_score,
            reverse=True
        )
        
        # Database sizing should have higher priority (higher savings, medium effort)
        # than unattached volume (lower savings, low effort)
        assert sorted_results[0].check_type == CheckType.RIGHT_SIZING
        assert sorted_results[0].resource.id == "db-oversized"