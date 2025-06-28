"""End-to-end tests for the new optimization checks."""

import json
import os
import tempfile
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from click.testing import CliRunner

from src.main import cli
from src.models.base import CloudProvider, Resource, ResourceType
from src.models.checks import CheckResult, CheckSeverity, CheckType


class TestNewChecksE2E:
    """End-to-end tests for new check implementations."""
    
    @pytest.fixture
    def cli_runner(self):
        """Create a CLI runner for testing."""
        return CliRunner()
    
    @pytest.fixture
    def mock_auth_manager(self):
        """Mock authentication manager."""
        with patch("src.utils.config.AuthManager") as mock:
            auth_manager = MagicMock()
            auth_manager.is_provider_configured.return_value = True
            auth_manager.get_provider_config.return_value = {
                "access_key_id": "test_key",
                "secret_access_key": "test_secret",
                "region": "us-east-1"
            }
            mock.return_value = auth_manager
            yield auth_manager
    
    @pytest.fixture
    def mock_provider_with_unattached_volumes(self):
        """Mock provider with unattached volumes."""
        provider = AsyncMock()
        provider.provider = CloudProvider.AWS
        
        # Mock list_resources to return volumes
        provider.list_resources.return_value = [
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
        ]
        
        # Mock volume info
        provider.get_volume_info.side_effect = [
            {
                "attached": False,
                "detached_at": "2024-01-01T00:00:00Z",
                "size_gb": 100,
                "volume_type": "gp3",
            },
            {"attached": True},  # Second volume is attached
        ]
        
        return provider
    
    @pytest.mark.asyncio
    async def test_e2e_unattached_volumes_check(
        self, cli_runner, mock_auth_manager, mock_provider_with_unattached_volumes
    ):
        """Test end-to-end flow for unattached volumes check."""
        with patch("src.providers.base.ProviderFactory.create") as mock_factory:
            mock_factory.return_value = mock_provider_with_unattached_volumes
            
            # Run the analyze command
            result = cli_runner.invoke(
                cli,
                ["analyze", "--provider", "aws", "--checks", "unattached_volume"]
            )
            
            assert result.exit_code == 0
            assert "Unattached Volume" in result.output
            assert "DataVolume" in result.output
            assert "$50.00/month" in result.output
            assert "BackupVolume" not in result.output  # Should not appear as it's attached
    
    @pytest.mark.asyncio
    async def test_e2e_old_snapshots_check(self, cli_runner, mock_auth_manager):
        """Test end-to-end flow for old snapshots check."""
        with patch("src.providers.base.ProviderFactory.create") as mock_factory:
            provider = AsyncMock()
            provider.provider = CloudProvider.AWS
            
            # Mock snapshots
            provider.list_resources.return_value = [
                Resource(
                    id="snap-1234",
                    name="OldSnapshot",
                    type=ResourceType.SNAPSHOT,
                    provider=CloudProvider.AWS,
                    region="us-east-1",
                    state="completed",
                    monthly_cost=Decimal("20.00"),
                    is_active=True,
                ),
            ]
            
            # Mock snapshot info
            provider.get_snapshot_info.return_value = {
                "created_at": "2023-01-01T00:00:00Z",  # Very old
                "size_gb": 100,
                "is_ami_snapshot": False,
                "has_backup_policy": False,
            }
            
            mock_factory.return_value = provider
            
            # Run the analyze command
            result = cli_runner.invoke(
                cli,
                ["analyze", "--provider", "aws", "--checks", "old_snapshot"]
            )
            
            assert result.exit_code == 0
            assert "Old Snapshot" in result.output
            assert "OldSnapshot" in result.output
            assert "$20.00/month" in result.output
    
    @pytest.mark.asyncio
    async def test_e2e_list_checks_includes_new_checks(self, cli_runner):
        """Test that list-checks command includes all new checks."""
        result = cli_runner.invoke(cli, ["list-checks"])
        
        assert result.exit_code == 0
        assert "Unattached Volume Detection" in result.output
        assert "Old Snapshot Detection" in result.output
        assert "Reserved Instances Utilization" in result.output
        assert "Savings Plans Coverage Analysis" in result.output
        assert "Database Right-Sizing" in result.output
    
    @pytest.mark.asyncio
    async def test_e2e_analyze_with_json_output(self, cli_runner, mock_auth_manager):
        """Test analyze command with JSON output for new checks."""
        with patch("src.providers.base.ProviderFactory.create") as mock_factory, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            
            provider = AsyncMock()
            provider.provider = CloudProvider.AWS
            
            # Mock resources and check results
            provider.list_resources.return_value = [
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
            ]
            
            provider.get_database_metrics.return_value = {
                "avg_cpu_percent": 15.0,
                "avg_memory_percent": 20.0,
                "max_cpu_percent": 40.0,
                "max_memory_percent": 45.0,
            }
            
            provider.get_database_info.return_value = {
                "instance_type": "db.r5.2xlarge",
                "engine": "postgres",
            }
            
            provider.get_database_sizing_recommendations.return_value = [
                {
                    "instance_type": "db.r5.xlarge",
                    "monthly_cost": 300.0,
                }
            ]
            
            mock_factory.return_value = provider
            
            # Run analyze with JSON output
            result = cli_runner.invoke(
                cli,
                [
                    "analyze",
                    "--provider", "aws",
                    "--checks", "right_sizing",
                    "--output", "json",
                    "--output-file", tmp.name
                ]
            )
            
            assert result.exit_code == 0
            assert f"Results saved to {tmp.name}" in result.output
            
            # Verify JSON content
            with open(tmp.name, 'r') as f:
                data = json.load(f)
            
            assert "results" in data
            assert len(data["results"]) > 0
            assert data["results"][0]["check_type"] == "right_sizing"
            assert data["results"][0]["resource"]["name"] == "ProductionDB"
            assert float(data["results"][0]["monthly_savings"]) == 200.0
            
            # Cleanup
            os.unlink(tmp.name)
    
    @pytest.mark.asyncio
    async def test_e2e_analyze_with_severity_filter(self, cli_runner, mock_auth_manager):
        """Test analyze command with severity filter."""
        with patch("src.providers.base.ProviderFactory.create") as mock_factory:
            provider = AsyncMock()
            provider.provider = CloudProvider.AWS
            
            # Mock multiple findings with different severities
            provider.get_reserved_instances_utilization.return_value = {
                "underutilized": [
                    {
                        "reservation_id": "ri-1234",
                        "instance_type": "m5.large",
                        "utilization_percentage": 60.0,
                        "monthly_cost": 1000.0,  # Will be HIGH severity
                    },
                    {
                        "reservation_id": "ri-5678",
                        "instance_type": "t3.small",
                        "utilization_percentage": 70.0,
                        "monthly_cost": 100.0,  # Will be MEDIUM severity
                    },
                ]
            }
            provider.get_on_demand_ri_opportunities.return_value = []
            provider.list_resources.return_value = []
            
            mock_factory.return_value = provider
            
            # Run with high severity filter
            result = cli_runner.invoke(
                cli,
                [
                    "analyze",
                    "--provider", "aws",
                    "--checks", "reserved_instance_optimization",
                    "--severity", "high"
                ]
            )
            
            assert result.exit_code == 0
            assert "ri-1234" in result.output
            assert "ri-5678" not in result.output  # Medium severity filtered out
    
    @pytest.mark.asyncio
    async def test_e2e_analyze_multiple_providers(self, cli_runner):
        """Test analyzing multiple providers with new checks."""
        with patch("src.utils.config.AuthManager") as mock_auth:
            auth_manager = MagicMock()
            auth_manager.get_configured_providers.return_value = [
                CloudProvider.AWS,
                CloudProvider.AZURE,
            ]
            auth_manager.is_provider_configured.return_value = True
            auth_manager.get_provider_config.return_value = {"region": "us-east-1"}
            mock_auth.return_value = auth_manager
            
            with patch("src.providers.base.ProviderFactory.create") as mock_factory:
                # Create different providers
                aws_provider = AsyncMock()
                aws_provider.provider = CloudProvider.AWS
                aws_provider.list_resources.return_value = []
                aws_provider.get_savings_plans_coverage.return_value = {
                    "coverage_percentage": 40.0,
                    "total_compute_spend": 10000.0,
                    "covered_spend": 4000.0,
                    "expiring_plans": [],
                }
                
                azure_provider = AsyncMock()
                azure_provider.provider = CloudProvider.AZURE
                azure_provider.list_resources.return_value = []
                
                mock_factory.side_effect = [aws_provider, azure_provider]
                
                # Run analyze for all providers
                result = cli_runner.invoke(cli, ["analyze"])
                
                assert result.exit_code == 0
                assert "AWS" in result.output
                assert "Azure" in result.output
                assert "Savings Plans Coverage" in result.output
    
    @pytest.mark.asyncio
    async def test_e2e_error_handling(self, cli_runner, mock_auth_manager):
        """Test error handling in end-to-end flow."""
        with patch("src.providers.base.ProviderFactory.create") as mock_factory:
            provider = AsyncMock()
            provider.provider = CloudProvider.AWS
            provider.list_resources.return_value = []
            
            # Mock an error in getting reserved instances
            provider.get_reserved_instances_utilization.side_effect = Exception(
                "API rate limit exceeded"
            )
            
            mock_factory.return_value = provider
            
            # Run the command - should handle error gracefully
            result = cli_runner.invoke(
                cli,
                ["analyze", "--provider", "aws", "--checks", "reserved_instance_optimization"]
            )
            
            # Should complete without crashing
            assert result.exit_code == 0
            # Error should be logged but not crash the program
    
    @pytest.mark.asyncio
    async def test_e2e_dry_run_mode(self, cli_runner, mock_auth_manager):
        """Test dry run mode with new checks."""
        result = cli_runner.invoke(
            cli,
            [
                "analyze",
                "--dry-run",
                "--checks", "unattached_volume,old_snapshot,reserved_instance_optimization"
            ]
        )
        
        assert result.exit_code == 0
        assert "Dry Run Mode" in result.output
        assert "unattached_volume" in result.output
        assert "old_snapshot" in result.output
        assert "reserved_instance_optimization" in result.output
    
    @pytest.mark.asyncio
    async def test_e2e_csv_output(self, cli_runner, mock_auth_manager):
        """Test CSV output with new checks."""
        with patch("src.providers.base.ProviderFactory.create") as mock_factory, \
             tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            
            provider = AsyncMock()
            provider.provider = CloudProvider.AWS
            
            # Mock unattached volume
            provider.list_resources.return_value = [
                Resource(
                    id="vol-1234",
                    name="UnattachedVolume",
                    type=ResourceType.VOLUME,
                    provider=CloudProvider.AWS,
                    region="us-east-1",
                    state="available",
                    monthly_cost=Decimal("50.00"),
                    is_active=True,
                ),
            ]
            
            provider.get_volume_info.return_value = {
                "attached": False,
                "detached_at": "2024-01-01T00:00:00Z",
                "size_gb": 100,
                "volume_type": "gp3",
            }
            
            mock_factory.return_value = provider
            
            # Run analyze with CSV output
            result = cli_runner.invoke(
                cli,
                [
                    "analyze",
                    "--provider", "aws",
                    "--checks", "unattached_volume",
                    "--output", "csv",
                    "--output-file", tmp.name
                ]
            )
            
            assert result.exit_code == 0
            assert f"Results saved to {tmp.name}" in result.output
            
            # Verify CSV content
            with open(tmp.name, 'r') as f:
                content = f.read()
            
            assert "UnattachedVolume" in content
            assert "vol-1234" in content
            assert "50.00" in content
            assert "unattached_volume" in content
            
            # Cleanup
            os.unlink(tmp.name)