"""Integration test for all new checks."""

import asyncio
from decimal import Decimal
from unittest.mock import AsyncMock
import pytest

from src.checks.storage.unattached_volumes import UnattachedVolumesCheck
from src.checks.storage.old_snapshots import OldSnapshotsCheck
from src.checks.cost_optimization.reserved_instances import ReservedInstancesUtilizationCheck
from src.checks.cost_optimization.savings_plans import SavingsPlansCoverageCheck
from src.checks.database.database_sizing import DatabaseSizingCheck
from src.checks.registry import check_registry
from src.models.base import CloudProvider, Resource, ResourceType


@pytest.mark.asyncio
async def test_all_checks_registered():
    """Test that all new checks are properly registered."""
    # Get all registered checks
    all_checks = check_registry.list_all()
    check_names = [check.name for check in all_checks]
    
    # Verify our new checks are registered
    expected_checks = [
        "Unattached Volume Detection",
        "Old Snapshot Detection",
        "Reserved Instances Utilization",
        "Savings Plans Coverage Analysis",
        "Database Right-Sizing",
    ]
    
    for expected in expected_checks:
        assert expected in check_names, f"Check '{expected}' not found in registry"


@pytest.mark.asyncio
async def test_checks_integration():
    """Test all checks work together in an integration scenario."""
    # Create mock provider
    provider = AsyncMock()
    provider.provider = CloudProvider.AWS
    
    # Create sample resources
    resources = [
        # Unattached volume
        Resource(
            id="vol-1234",
            name="Unattached Volume",
            type=ResourceType.VOLUME,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="available",
            monthly_cost=Decimal("50.00"),
            is_active=True,
        ),
        # Old snapshot
        Resource(
            id="snap-5678",
            name="Old Snapshot",
            type=ResourceType.SNAPSHOT,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="completed",
            monthly_cost=Decimal("100.00"),
            is_active=True,
        ),
        # Instance for RI check
        Resource(
            id="i-9012",
            name="EC2 Instance",
            type=ResourceType.INSTANCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="running",
            monthly_cost=Decimal("200.00"),
            is_active=True,
        ),
        # Database for sizing check
        Resource(
            id="db-3456",
            name="RDS Database",
            type=ResourceType.DATABASE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="available",
            monthly_cost=Decimal("500.00"),
            is_active=True,
        ),
    ]
    
    # Mock provider responses
    provider.get_volume_info.return_value = {
        "attached": False,
        "last_attached": None,
    }
    
    provider.get_snapshot_info.return_value = {
        "created_at": "2024-01-01T00:00:00Z",
        "size_gb": 100,
        "is_ami_snapshot": False,
        "has_backup_policy": False,
    }
    
    provider.get_reserved_instances_utilization.return_value = {
        "underutilized": [{
            "reservation_id": "ri-test",
            "instance_type": "m5.large",
            "region": "us-east-1",
            "utilization_percentage": 50.0,
            "monthly_cost": 1000.0,
        }]
    }
    
    provider.get_on_demand_ri_opportunities.return_value = []
    
    provider.get_savings_plans_coverage.return_value = {
        "coverage_percentage": 40.0,
        "total_compute_spend": 5000.0,
        "covered_spend": 2000.0,
        "expiring_plans": [],
    }
    
    provider.get_database_metrics.return_value = {
        "avg_cpu_percent": 20.0,
        "avg_memory_percent": 25.0,
        "max_cpu_percent": 40.0,
        "max_memory_percent": 45.0,
    }
    
    provider.get_database_info.return_value = {
        "instance_type": "db.m5.xlarge",
    }
    
    provider.get_database_sizing_recommendations.return_value = [{
        "instance_type": "db.m5.large",
        "monthly_cost": 300.0,
    }]
    
    # Run all checks
    all_results = []
    
    checks = [
        UnattachedVolumesCheck(),
        OldSnapshotsCheck(),
        ReservedInstancesUtilizationCheck(),
        SavingsPlansCoverageCheck(),
        DatabaseSizingCheck(),
    ]
    
    for check in checks:
        if provider.provider in check.supported_providers:
            filtered = check.filter_resources(resources)
            results = await check.run(provider, filtered)
            all_results.extend(results)
    
    # Verify we got results from multiple checks
    assert len(all_results) > 0, f"Expected results but got {len(all_results)}"
    
    # Verify different check types
    check_types = {result.check_type for result in all_results}
    assert len(check_types) >= 3, f"Expected at least 3 check types but got {len(check_types)}: {check_types}"
    
    # Verify we have severities
    severities = {result.severity for result in all_results}
    assert len(severities) >= 1, f"Expected at least 1 severity but got {len(severities)}: {severities}"
    
    # Verify total savings
    total_savings = sum(result.monthly_savings for result in all_results)
    assert total_savings > 0, f"Expected positive savings but got ${total_savings}"
    
    print(f"\nIntegration test summary:")
    print(f"Total check results: {len(all_results)}")
    print(f"Check types found: {check_types}")
    print(f"Severities found: {severities}")
    print(f"Total monthly savings: ${total_savings}")
    
    # Print individual results for debugging
    for result in all_results:
        print(f"\n- {result.title}")
        print(f"  Type: {result.check_type}")
        print(f"  Severity: {result.severity}")
        print(f"  Monthly Savings: ${result.monthly_savings}")


if __name__ == "__main__":
    asyncio.run(test_all_checks_registered())
    asyncio.run(test_checks_integration())