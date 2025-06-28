"""Tests for analyze helper functions."""

import csv
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from commands.analyze_helpers import (
    determine_providers,
    display_dry_run_info,
    display_summary,
    filter_results_by_severity,
    save_results_csv,
    save_results_json,
    validate_configuration,
)
from models import CheckResult, CheckType, CloudProvider, CheckSeverity, Resource, ResourceType


class TestValidateConfiguration:
    """Test validate_configuration function."""
    
    def test_validate_no_config(self, capsys):
        """Test validation with no configuration."""
        result = validate_configuration(None, "all")
        assert result is False
        captured = capsys.readouterr()
        assert "No configuration found" in captured.out
    
    def test_validate_empty_config(self, capsys):
        """Test validation with empty configuration."""
        result = validate_configuration({}, "all")
        assert result is False
        captured = capsys.readouterr()
        assert "No configuration found" in captured.out
    
    def test_validate_missing_provider(self, capsys):
        """Test validation when specific provider is missing."""
        config = {"aws": {}}
        result = validate_configuration(config, "azure")
        assert result is False
        captured = capsys.readouterr()
        assert "No configuration found for provider 'azure'" in captured.out
    
    def test_validate_all_providers(self):
        """Test validation with 'all' providers."""
        config = {"aws": {}, "azure": {}, "gcp": {}}
        result = validate_configuration(config, "all")
        assert result is True
    
    def test_validate_specific_provider(self):
        """Test validation with specific provider."""
        config = {"aws": {}, "azure": {}}
        result = validate_configuration(config, "aws")
        assert result is True


class TestDetermineProviders:
    """Test determine_providers function."""
    
    def test_determine_all_providers(self):
        """Test determining all configured providers."""
        config = {"aws": {}, "azure": {}, "gcp": {}}
        providers = determine_providers("all", config)
        assert len(providers) == 3
        assert CloudProvider.AWS in providers
        assert CloudProvider.AZURE in providers
        assert CloudProvider.GCP in providers
    
    def test_determine_specific_provider(self):
        """Test determining specific provider."""
        config = {"aws": {}, "azure": {}}
        providers = determine_providers("aws", config)
        assert len(providers) == 1
        assert providers[0] == CloudProvider.AWS
    
    def test_determine_subset_providers(self):
        """Test determining providers when only some are configured."""
        config = {"aws": {}, "gcp": {}}
        providers = determine_providers("all", config)
        assert len(providers) == 2
        assert CloudProvider.AWS in providers
        assert CloudProvider.GCP in providers
        assert CloudProvider.AZURE not in providers


class TestFilterResultsBySeverity:
    """Test filter_results_by_severity function."""
    
    @pytest.fixture
    def sample_results(self):
        """Create sample results with different severities."""
        from datetime import datetime
        
        # Create a sample resource
        resource = Resource(
            id="test-resource",
            name="test-resource",
            type=ResourceType.INSTANCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="running"
        )
        
        return [
            CheckResult(
                id="test-critical",
                check_type=CheckType.IDLE_RESOURCE,
                severity=CheckSeverity.CRITICAL,
                resource=resource,
                title="Critical Issue",
                description="Critical issue found",
                impact="Critical impact",
                current_cost=1000.0,
                optimized_cost=0.0,
                monthly_savings=1000.0,
                annual_savings=12000.0,
                savings_percentage=100.0,
                effort_level="Low",
                risk_level="Low",
                check_name="test-critical",
                provider=CloudProvider.AWS,
                region="us-east-1"
            ),
            CheckResult(
                id="test-high",
                check_type=CheckType.IDLE_RESOURCE,
                severity=CheckSeverity.HIGH,
                resource=resource,
                title="High Issue",
                description="High issue found",
                impact="High impact",
                current_cost=500.0,
                optimized_cost=0.0,
                monthly_savings=500.0,
                annual_savings=6000.0,
                savings_percentage=100.0,
                effort_level="Low",
                risk_level="Low",
                check_name="test-high",
                provider=CloudProvider.AWS,
                region="us-east-1"
            ),
            CheckResult(
                id="test-medium",
                check_type=CheckType.IDLE_RESOURCE,
                severity=CheckSeverity.MEDIUM,
                resource=resource,
                title="Medium Issue",
                description="Medium issue found",
                impact="Medium impact",
                current_cost=300.0,
                optimized_cost=100.0,
                monthly_savings=200.0,
                annual_savings=2400.0,
                savings_percentage=66.7,
                effort_level="Medium",
                risk_level="Medium",
                check_name="test-medium",
                provider=CloudProvider.AWS,
                region="us-east-1"
            ),
            CheckResult(
                id="test-low",
                check_type=CheckType.IDLE_RESOURCE,
                severity=CheckSeverity.LOW,
                resource=resource,
                title="Low Issue",
                description="Low issue found",
                impact="Low impact",
                current_cost=100.0,
                optimized_cost=50.0,
                monthly_savings=50.0,
                annual_savings=600.0,
                savings_percentage=50.0,
                effort_level="Low",
                risk_level="Low",
                check_name="test-low",
                provider=CloudProvider.AWS,
                region="us-east-1"
            ),
        ]
    
    def test_filter_all_severities(self, sample_results):
        """Test filtering with 'all' severity."""
        filtered = filter_results_by_severity(sample_results, "all")
        assert len(filtered) == 4
    
    def test_filter_critical_only(self, sample_results):
        """Test filtering for critical severity only."""
        filtered = filter_results_by_severity(sample_results, "critical")
        assert len(filtered) == 1
        assert filtered[0].severity == CheckSeverity.CRITICAL
    
    def test_filter_high_and_above(self, sample_results):
        """Test filtering for high severity and above."""
        filtered = filter_results_by_severity(sample_results, "high")
        assert len(filtered) == 2
        assert all(r.severity in [CheckSeverity.CRITICAL, CheckSeverity.HIGH] for r in filtered)
    
    def test_filter_medium_and_above(self, sample_results):
        """Test filtering for medium severity and above."""
        filtered = filter_results_by_severity(sample_results, "medium")
        assert len(filtered) == 3
        assert all(r.severity != CheckSeverity.LOW for r in filtered)


class TestSaveResults:
    """Test save results functions."""
    
    @pytest.fixture
    def sample_results(self):
        """Create sample results for testing."""
        from datetime import datetime
        
        return [
            CheckResult(
                id="test-check",
                check_type=CheckType.IDLE_RESOURCE,
                severity=CheckSeverity.HIGH,
                resource=Resource(
                    id="test-resource",
                    name="test-resource",
                    type=ResourceType.INSTANCE,
                    provider=CloudProvider.AWS,
                    region="us-east-1",
                    state="idle"
                ),
                title="Idle Instance",
                description="Instance has been idle",
                impact="Wasted resources",
                current_cost=100.0,
                optimized_cost=0.0,
                monthly_savings=100.0,
                annual_savings=1200.0,
                savings_percentage=100.0,
                effort_level="Low",
                risk_level="Low",
                check_name="test-check",
                provider=CloudProvider.AWS,
                region="us-east-1",
                metadata={"test": "data"}
            )
        ]
    
    def test_save_results_json(self, sample_results, tmp_path, capsys):
        """Test saving results to JSON file."""
        output_file = tmp_path / "results.json"
        save_results_json(sample_results, output_file)
        
        assert output_file.exists()
        captured = capsys.readouterr()
        # Path might be wrapped across lines
        assert "Results saved to" in captured.out
        assert str(output_file.name) in captured.out
        
        # Verify JSON content
        with open(output_file) as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["id"] == "test-check"
    
    def test_save_results_csv(self, sample_results, tmp_path, capsys):
        """Test saving results to CSV file."""
        output_file = tmp_path / "results.csv"
        save_results_csv(sample_results, output_file)
        
        assert output_file.exists()
        captured = capsys.readouterr()
        # Path might be wrapped across lines
        assert "Results saved to" in captured.out
        assert str(output_file.name) in captured.out
        
        # Verify CSV content
        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["id"] == "test-check"
    
    def test_save_empty_results_csv(self, tmp_path, capsys):
        """Test saving empty results to CSV."""
        output_file = tmp_path / "results.csv"
        save_results_csv([], output_file)
        
        assert not output_file.exists()
        captured = capsys.readouterr()
        assert "No results to save" in captured.out


class TestDisplayFunctions:
    """Test display functions."""
    
    @pytest.fixture
    def sample_results_with_savings(self):
        """Create sample results with savings data."""
        from datetime import datetime
        
        # Create sample resources
        resource1 = Resource(
            id="resource-1",
            name="resource-1",
            type=ResourceType.INSTANCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="idle"
        )
        
        return [
            CheckResult(
                id="test-check-1",
                check_type=CheckType.IDLE_RESOURCE,
                severity=CheckSeverity.HIGH,
                resource=resource1,
                title="Idle Resource",
                description="Resource has been idle",
                impact="Wasted cost",
                current_cost=100.0,
                optimized_cost=0.0,
                monthly_savings=100.0,
                annual_savings=1200.0,
                savings_percentage=100.0,
                effort_level="Low",
                risk_level="Low",
                check_name="test-check-1",
                provider=CloudProvider.AWS,
                region="us-east-1"
            ),
            CheckResult(
                id="test-check-2",
                check_type=CheckType.RIGHT_SIZING,
                severity=CheckSeverity.MEDIUM,
                resource=Resource(
                    id="resource-2",
                    name="resource-2",
                    type=ResourceType.INSTANCE,
                    provider=CloudProvider.AWS,
                    region="us-east-1",
                    state="running"
                ),
                title="Oversized Resource",
                description="Resource is oversized",
                impact="Wasted cost from oversizing",
                current_cost=200.0,
                optimized_cost=100.0,
                monthly_savings=100.0,
                annual_savings=1200.0,
                savings_percentage=50.0,
                effort_level="Medium",
                risk_level="Medium",
                check_name="test-check-2",
                provider=CloudProvider.AWS,
                region="us-east-1"
            )
        ]
    
    def test_display_summary(self, sample_results_with_savings, capsys):
        """Test displaying summary statistics."""
        display_summary(sample_results_with_savings)
        captured = capsys.readouterr()
        
        assert "Summary:" in captured.out
        assert "Total findings: 2" in captured.out
        assert "Potential monthly savings: $200.00" in captured.out
        assert "Potential annual savings: $2,400.00" in captured.out
    
    def test_display_summary_empty_results(self, capsys):
        """Test displaying summary with no results."""
        display_summary([])
        captured = capsys.readouterr()
        assert captured.out == ""
    
    def test_display_dry_run_info(self, capsys):
        """Test displaying dry run information."""
        providers = [CloudProvider.AWS, CloudProvider.AZURE]
        display_dry_run_info(providers, "us-east-1", ["idle_resource", "right_sizing"])
        
        captured = capsys.readouterr()
        assert "Dry Run - Would analyze:" in captured.out
        assert "AWS" in captured.out
        assert "AZURE" in captured.out
        assert "Region: us-east-1" in captured.out
        assert "Checks: idle_resource, right_sizing" in captured.out
    
    def test_display_dry_run_info_no_filters(self, capsys):
        """Test displaying dry run with no filters."""
        providers = [CloudProvider.GCP]
        display_dry_run_info(providers, None, None)
        
        captured = capsys.readouterr()
        assert "GCP" in captured.out
        assert "Regions: All configured regions" in captured.out
        assert "Checks: All available checks" in captured.out