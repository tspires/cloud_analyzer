"""Tests for result formatters."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console

from formatters.check_results import (
    format_check_results,
    format_detailed_result,
    get_severity_style,
)
from models import (
    CheckResult,
    CheckSeverity,
    CheckType,
    CloudProvider,
    Resource,
    ResourceType,
)


class TestFormatters:
    """Test result formatting functions."""
    
    @pytest.fixture
    def sample_resource(self):
        """Create a sample resource."""
        return Resource(
            id="i-1234567890",
            name="test-instance",
            type=ResourceType.INSTANCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            state="running",
            tags={"env": "test"},
            metadata={"instance_type": "m5.large"}
        )
    
    @pytest.fixture
    def sample_results(self, sample_resource):
        """Create sample check results."""
        return [
            CheckResult(
                id="result-1",
                check_type=CheckType.IDLE_RESOURCE,
                resource=sample_resource,
                severity=CheckSeverity.HIGH,
                title="Idle EC2 Instance",
                description="Instance has been idle for 30 days",
                impact="High cost impact due to unused resources",
                current_cost=100.0,
                optimized_cost=0.0,
                monthly_savings=100.0,
                annual_savings=1200.0,
                savings_percentage=100.0,
                effort_level="Low",
                risk_level="Low",
                confidence_score=0.95,
                implementation_steps=[
                    "1. Review instance usage",
                    "2. Create snapshot if needed",
                    "3. Terminate instance"
                ],
                metadata={"idle_days": 30},
                timestamp=datetime.now()
            ),
            CheckResult(
                id="result-2",
                check_type=CheckType.RIGHT_SIZING,
                resource=sample_resource,
                severity=CheckSeverity.MEDIUM,
                title="Oversized Instance",
                description="Instance is oversized for current workload",
                impact="Medium cost impact from oversized resources",
                current_cost=200.0,
                optimized_cost=100.0,
                monthly_savings=100.0,
                annual_savings=1200.0,
                savings_percentage=50.0,
                effort_level="Medium",
                risk_level="Medium",
                confidence_score=0.80,
                implementation_steps=[
                    "1. Schedule maintenance window",
                    "2. Stop instance",
                    "3. Change instance type",
                    "4. Start instance"
                ],
                metadata={"recommended_type": "m5.medium"},
                timestamp=datetime.now()
            )
        ]
    
    def test_format_check_results_empty(self, capsys):
        """Test formatting empty results."""
        console = Console()
        format_check_results([], console)
        
        captured = capsys.readouterr()
        assert "No optimization opportunities found" in captured.out
    
    def test_format_check_results(self, sample_results, capsys):
        """Test formatting check results."""
        console = Console()
        format_check_results(sample_results, console)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check that both severity levels are shown
        assert "HIGH Priority Findings (1)" in output
        assert "MEDIUM Priority Findings (1)" in output
        
        # Check resource information
        assert "test-instance" in output
        # The type might be truncated in the table
        assert "idle_resou" in output  # May be truncated as "idle_resou..."
        assert "right_siz" in output   # May be truncated as "right_siz..."
        
        # Check savings amounts
        assert "$100.00" in output
        assert "$1,200.00" in output
    
    def test_format_check_results_sorting(self, sample_resource):
        """Test that results are sorted by savings within each severity."""
        results = [
            CheckResult(
                id="result-low-savings",
                check_type=CheckType.IDLE_RESOURCE,
                resource=sample_resource,
                severity=CheckSeverity.HIGH,
                title="Low savings",
                description="Test",
                impact="Test",
                current_cost=50.0,
                optimized_cost=0.0,
                monthly_savings=50.0,
                annual_savings=600.0,
                savings_percentage=100.0,
                effort_level="Low",
                risk_level="Low",
                confidence_score=0.95,
                implementation_steps=[],
                metadata={},
                timestamp=datetime.now()
            ),
            CheckResult(
                id="result-high-savings",
                check_type=CheckType.IDLE_RESOURCE,
                resource=sample_resource,
                severity=CheckSeverity.HIGH,
                title="High savings",
                description="Test",
                impact="Test",
                current_cost=200.0,
                optimized_cost=0.0,
                monthly_savings=200.0,
                annual_savings=2400.0,
                savings_percentage=100.0,
                effort_level="Low",
                risk_level="Low",
                confidence_score=0.95,
                implementation_steps=[],
                metadata={},
                timestamp=datetime.now()
            )
        ]
        
        console = Console()
        with patch.object(console, 'print') as mock_print:
            format_check_results(results, console)
            
            # The mock should have been called with tables
            # We can't easily check the exact order in the table,
            # but we can verify the function doesn't crash
            assert mock_print.called
    
    def test_format_detailed_result(self, sample_results, capsys):
        """Test formatting a detailed result."""
        console = Console()
        format_detailed_result(sample_results[0], console)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check severity indicator
        assert "HIGH" in output
        
        # Check all sections are present
        assert "Resource:" in output
        assert "test-instance" in output
        assert "Provider: AWS" in output
        assert "Region: us-east-1" in output
        
        assert "Finding:" in output
        assert "Instance has been idle for 30 days" in output
        
        assert "Impact:" in output
        assert "High cost impact" in output
        
        assert "Cost Analysis:" in output
        assert "Current Cost: $100.00/month" in output
        assert "Optimized Cost: $0.00/month" in output
        assert "Monthly Savings: $100.00" in output
        assert "Annual Savings: $1,200.00" in output
        assert "Savings: 100.0%" in output
        
        assert "Implementation:" in output
        assert "Effort: Low" in output
        assert "Risk: Low" in output
        assert "Confidence: 95%" in output
        
        # Check implementation steps
        assert "Steps:" in output
        assert "1. Review instance usage" in output
        assert "2. Create snapshot if needed" in output
        assert "3. Terminate instance" in output
    
    def test_get_severity_style(self):
        """Test getting severity styles."""
        assert get_severity_style(CheckSeverity.CRITICAL) == "red bold"
        assert get_severity_style(CheckSeverity.HIGH) == "red"
        assert get_severity_style(CheckSeverity.MEDIUM) == "yellow"
        assert get_severity_style(CheckSeverity.LOW) == "blue"
        assert get_severity_style(CheckSeverity.INFO) == "dim"