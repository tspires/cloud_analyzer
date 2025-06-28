"""Tests for run_check command with new check types."""

from decimal import Decimal
from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from commands.run_check import run_check
from models import CheckResult, CheckSeverity, CheckType, CloudProvider, Resource, ResourceType


class TestRunCheckNewChecks:
    """Test the run-check command with new check types."""
    
    @pytest.mark.asyncio
    async def test_run_unattached_volumes_check(self, cli_runner, mock_auth_manager):
        """Test running unattached volumes check."""
        with patch("commands.run_check.check_registry") as mock_registry, \
             patch("commands.run_check.CloudProviderInterface") as mock_provider_class:
            
            # Mock check
            mock_check = MagicMock()
            mock_check.name = "Unattached Volume Detection"
            mock_check.check_type = CheckType.UNATTACHED_VOLUME
            mock_check.supported_providers = {CloudProvider.AWS}
            mock_registry.get.return_value = mock_check
            
            # Mock provider
            mock_provider = AsyncMock()
            mock_provider_class.from_auth.return_value = mock_provider
            
            # Mock resources
            mock_provider.list_resources.return_value = [
                Resource(
                    id="vol-1234",
                    name="UnattachedVolume",
                    type=ResourceType.VOLUME,
                    provider=CloudProvider.AWS,
                    region="us-east-1",
                    state="available",
                    monthly_cost=Decimal("50.00"),
                    is_active=True,
                )
            ]
            
            # Mock check results
            mock_runner = AsyncMock()
            mock_runner.run_check.return_value = [
                CheckResult(
                    id="unattached-vol-1234",
                    check_type=CheckType.UNATTACHED_VOLUME,
                    severity=CheckSeverity.MEDIUM,
                    resource=Resource(
                        id="vol-1234",
                        name="UnattachedVolume",
                        type=ResourceType.VOLUME,
                        provider=CloudProvider.AWS,
                        region="us-east-1",
                        state="available",
                        monthly_cost=Decimal("50.00"),
                        is_active=True,
                    ),
                    title="Unattached Volume: UnattachedVolume",
                    description="Volume has been unattached for 10 days",
                    impact="This unattached volume is incurring storage costs",
                    current_cost=Decimal("50.00"),
                    optimized_cost=Decimal("0.00"),
                    monthly_savings=Decimal("50.00"),
                    annual_savings=Decimal("600.00"),
                    savings_percentage=100.0,
                    effort_level="low",
                    risk_level="low",
                    implementation_steps=[
                        "1. Verify the volume is not needed",
                        "2. Create a snapshot if needed",
                        "3. Delete the volume",
                    ],
                )
            ]
            
            with patch("commands.run_check.CheckRunner", return_value=mock_runner):
                result = cli_runner.invoke(
                    run_check,
                    ["--provider", "aws", "--check", "Unattached Volume Detection"]
                )
            
            assert result.exit_code == 0
            assert "Running check: Unattached Volume Detection" in result.output
            assert "Found 1 optimization opportunities" in result.output
            assert "UnattachedVolume" in result.output
            assert "$50.00/month" in result.output
    
    @pytest.mark.asyncio
    async def test_run_reserved_instances_check(self, cli_runner, mock_auth_manager):
        """Test running reserved instances utilization check."""
        with patch("commands.run_check.check_registry") as mock_registry, \
             patch("commands.run_check.CloudProviderInterface") as mock_provider_class:
            
            # Mock check
            mock_check = MagicMock()
            mock_check.name = "Reserved Instances Utilization"
            mock_check.check_type = CheckType.RESERVED_INSTANCE_OPTIMIZATION
            mock_check.supported_providers = {CloudProvider.AWS}
            mock_registry.get.return_value = mock_check
            
            # Mock provider
            mock_provider = AsyncMock()
            mock_provider_class.from_auth.return_value = mock_provider
            
            # Mock resources
            mock_provider.list_resources.return_value = []
            
            # Mock check results
            mock_runner = AsyncMock()
            mock_runner.run_check.return_value = [
                CheckResult(
                    id="ri-underutilized-1234",
                    check_type=CheckType.RESERVED_INSTANCE_OPTIMIZATION,
                    severity=CheckSeverity.HIGH,
                    resource=Resource(
                        id="ri-1234",
                        name="RI: m5.large",
                        type=ResourceType.RESERVED_INSTANCE,
                        provider=CloudProvider.AWS,
                        region="us-east-1",
                        state="active",
                        monthly_cost=Decimal("1000.00"),
                        is_active=True,
                    ),
                    title="Underutilized Reserved Instance: m5.large",
                    description="Reserved instance is only 60.0% utilized",
                    impact="You're paying for reserved capacity that isn't being fully used",
                    current_cost=Decimal("1000.00"),
                    optimized_cost=Decimal("600.00"),
                    monthly_savings=Decimal("400.00"),
                    annual_savings=Decimal("4800.00"),
                    savings_percentage=40.0,
                    effort_level="medium",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review workloads",
                        "2. Ensure proper tagging",
                        "3. Consider modifying reservation",
                    ],
                )
            ]
            
            with patch("commands.run_check.CheckRunner", return_value=mock_runner):
                result = cli_runner.invoke(
                    run_check,
                    ["--provider", "aws", "--check", "Reserved Instances Utilization"]
                )
            
            assert result.exit_code == 0
            assert "Running check: Reserved Instances Utilization" in result.output
            assert "Underutilized Reserved Instance" in result.output
            assert "60.0% utilized" in result.output
            assert "$400.00/month" in result.output
    
    @pytest.mark.asyncio
    async def test_run_database_sizing_check(self, cli_runner, mock_auth_manager):
        """Test running database sizing check."""
        with patch("commands.run_check.check_registry") as mock_registry, \
             patch("commands.run_check.CloudProviderInterface") as mock_provider_class:
            
            # Mock check
            mock_check = MagicMock()
            mock_check.name = "Database Right-Sizing"
            mock_check.check_type = CheckType.RIGHT_SIZING
            mock_check.supported_providers = {CloudProvider.AWS, CloudProvider.AZURE}
            mock_registry.get.return_value = mock_check
            
            # Mock provider
            mock_provider = AsyncMock()
            mock_provider_class.from_auth.return_value = mock_provider
            
            # Mock resources
            mock_provider.list_resources.return_value = [
                Resource(
                    id="db-1234",
                    name="ProductionDB",
                    type=ResourceType.DATABASE,
                    provider=CloudProvider.AWS,
                    region="us-east-1",
                    state="available",
                    monthly_cost=Decimal("500.00"),
                    is_active=True,
                )
            ]
            
            # Mock check results
            mock_runner = AsyncMock()
            mock_runner.run_check.return_value = [
                CheckResult(
                    id="db-rightsize-1234",
                    check_type=CheckType.RIGHT_SIZING,
                    severity=CheckSeverity.HIGH,
                    resource=Resource(
                        id="db-1234",
                        name="ProductionDB",
                        type=ResourceType.DATABASE,
                        provider=CloudProvider.AWS,
                        region="us-east-1",
                        state="available",
                        monthly_cost=Decimal("500.00"),
                        is_active=True,
                    ),
                    title="Oversized Database: ProductionDB",
                    description="Database instance db.r5.2xlarge has low utilization",
                    impact="This database instance is oversized for its workload",
                    current_cost=Decimal("500.00"),
                    optimized_cost=Decimal("300.00"),
                    monthly_savings=Decimal("200.00"),
                    annual_savings=Decimal("2400.00"),
                    savings_percentage=40.0,
                    effort_level="medium",
                    risk_level="low",
                    implementation_steps=[
                        "1. Review workload patterns",
                        "2. Create backup",
                        "3. Resize database",
                    ],
                    check_metadata={
                        "current_instance_type": "db.r5.2xlarge",
                        "recommended_instance_type": "db.r5.xlarge",
                        "avg_cpu_percent": 15.0,
                        "avg_memory_percent": 20.0,
                    }
                )
            ]
            
            with patch("commands.run_check.CheckRunner", return_value=mock_runner):
                result = cli_runner.invoke(
                    run_check,
                    ["--provider", "aws", "--check", "Database Right-Sizing", "--output", "json"]
                )
            
            assert result.exit_code == 0
            # JSON output should contain the metadata
            assert "db.r5.2xlarge" in result.output
            assert "db.r5.xlarge" in result.output
            assert "15.0" in result.output  # CPU percentage