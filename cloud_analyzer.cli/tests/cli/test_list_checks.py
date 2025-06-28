"""Tests for the list_checks command."""

from unittest.mock import patch

import pytest

from commands.list_checks import list_checks
from models import CheckInfo, CheckType, CloudProvider


class TestListChecksCommand:
    """Test the list-checks command."""
    
    def test_list_checks_all(self, cli_runner, mock_check_registry):
        """Test listing all checks."""
        result = cli_runner.invoke(list_checks, [])
        assert result.exit_code == 0
        assert "Available Optimization Checks" in result.output
        assert "idle-ec2-instances" in result.output
        assert "oversized-instances" in result.output
        assert "idle-vm-instances" in result.output
        assert "Total checks: 3" in result.output
    
    def test_list_checks_by_provider(self, cli_runner, mock_check_registry):
        """Test listing checks filtered by provider."""
        result = cli_runner.invoke(list_checks, ["--provider", "aws"])
        assert result.exit_code == 0
        assert "idle-ec2-instances" in result.output
        assert "oversized-instances" in result.output
        assert "idle-vm-instances" not in result.output  # Azure only
    
    def test_list_checks_by_type(self, cli_runner, mock_check_registry):
        """Test listing checks filtered by type."""
        result = cli_runner.invoke(list_checks, ["--type", "idle_resource"])
        assert result.exit_code == 0
        assert "idle-ec2-instances" in result.output
        assert "idle-vm-instances" in result.output
        assert "oversized-instances" not in result.output  # Different type
    
    def test_list_checks_invalid_type(self, cli_runner, mock_check_registry):
        """Test listing checks with invalid type."""
        result = cli_runner.invoke(list_checks, ["--type", "invalid_type"])
        assert result.exit_code == 0
        assert "Error" in result.output
        assert "Invalid check type" in result.output
        assert "Valid check types:" in result.output
    
    def test_list_checks_combined_filters(self, cli_runner, mock_check_registry):
        """Test listing checks with multiple filters."""
        result = cli_runner.invoke(list_checks, ["--provider", "aws", "--type", "idle_resource"])
        assert result.exit_code == 0
        assert "idle-ec2-instances" in result.output
        assert "oversized-instances" not in result.output  # Different type
        assert "idle-vm-instances" not in result.output  # Different provider
    
    def test_list_checks_no_matches(self, cli_runner, mock_check_registry):
        """Test listing checks when no matches found."""
        result = cli_runner.invoke(list_checks, ["--provider", "gcp", "--type", "idle_resource"])
        assert result.exit_code == 0
        assert "No checks found matching the criteria" in result.output
    
    def test_list_checks_summary_stats(self, cli_runner, mock_check_registry):
        """Test that summary statistics are shown."""
        result = cli_runner.invoke(list_checks, [])
        assert result.exit_code == 0
        assert "Total checks: 3" in result.output
        assert "Check types: 2" in result.output
        assert "idle_resource: 2 checks" in result.output
        assert "right_sizing: 1 checks" in result.output
    
    def test_list_checks_empty_registry(self, cli_runner):
        """Test listing checks when registry is empty."""
        with patch("commands.list_checks.check_registry") as mock_registry:
            mock_registry.list_all.return_value = []
            result = cli_runner.invoke(list_checks, [])
            assert result.exit_code == 0
            assert "No checks found matching the criteria" in result.output
    
    def test_list_checks_table_format(self, cli_runner, mock_check_registry):
        """Test that checks are displayed in table format."""
        result = cli_runner.invoke(list_checks, [])
        assert result.exit_code == 0
        # Table should have headers
        assert "Check Name" in result.output
        assert "Type" in result.output
        assert "Providers" in result.output
        assert "Description" in result.output
    
    def test_list_checks_provider_formatting(self, cli_runner, mock_check_registry):
        """Test that providers are formatted correctly."""
        result = cli_runner.invoke(list_checks, [])
        assert result.exit_code == 0
        # Providers should be uppercase and comma-separated
        assert "AWS" in result.output
        assert "AZURE" in result.output
        assert "GCP" in result.output
        assert "AWS, AZURE, GCP" in result.output  # For oversized-instances
    
    def test_list_new_check_types(self, cli_runner):
        """Test that new check types are properly listed."""
        with patch("commands.list_checks.check_registry") as mock_registry:
            # Mock the new checks
            from src.models.checks import CheckInfo
            mock_registry.list_all.return_value = [
                CheckInfo(
                    name="Unattached Volume Detection",
                    check_type=CheckType.UNATTACHED_VOLUME,
                    description="Identifies storage volumes that have been unattached",
                    supported_providers=[CloudProvider.AWS, CloudProvider.AZURE, CloudProvider.GCP]
                ),
                CheckInfo(
                    name="Old Snapshot Detection", 
                    check_type=CheckType.OLD_SNAPSHOT,
                    description="Identifies snapshots older than 30 days",
                    supported_providers=[CloudProvider.AWS, CloudProvider.AZURE, CloudProvider.GCP]
                ),
                CheckInfo(
                    name="Reserved Instances Utilization",
                    check_type=CheckType.RESERVED_INSTANCE_OPTIMIZATION,
                    description="Identifies underutilized reserved instances",
                    supported_providers=[CloudProvider.AWS]
                ),
                CheckInfo(
                    name="Savings Plans Coverage Analysis",
                    check_type=CheckType.SAVINGS_PLAN_OPTIMIZATION,
                    description="Analyzes current savings plans coverage",
                    supported_providers=[CloudProvider.AWS]
                ),
                CheckInfo(
                    name="Database Right-Sizing",
                    check_type=CheckType.RIGHT_SIZING,
                    description="Identifies database instances with low utilization",
                    supported_providers=[CloudProvider.AWS, CloudProvider.AZURE, CloudProvider.GCP]
                ),
            ]
            
            result = cli_runner.invoke(list_checks, [])
            assert result.exit_code == 0
            
            # Check that all new checks are listed
            assert "Unattached Volume Detection" in result.output
            assert "Old Snapshot Detection" in result.output
            assert "Reserved Instances Utilization" in result.output
            assert "Savings Plans Coverage Analysis" in result.output
            assert "Database Right-Sizing" in result.output
            
            # Check check types
            assert "unattached_volume" in result.output
            assert "old_snapshot" in result.output
            assert "reserved_instance_optimization" in result.output
            assert "savings_plan_optimization" in result.output
            
            # Check provider support
            assert "AWS, AZURE, GCP" in result.output  # For multi-provider checks
            assert result.output.count("AWS") >= 5  # All checks support AWS