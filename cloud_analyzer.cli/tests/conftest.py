"""Pytest configuration and shared fixtures."""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_config_dir(tmp_path):
    """Mock the configuration directory to use temp directory."""
    with patch("utils.config.get_config_dir") as mock_get_dir:
        mock_get_dir.return_value = tmp_path
        yield tmp_path


@pytest.fixture
def mock_config(mock_config_dir):
    """Create a mock configuration with sample credentials."""
    config = {
        "aws": {
            "profile": "test-profile",
            "region": "us-east-1"
        },
        "azure": {
            "subscription_id": "test-sub-123",
            "tenant_id": "test-tenant-123",
            "client_id": "test-client-123",
            "client_secret": "test-secret-123"
        },
        "gcp": {
            "project_id": "test-project-123",
            "credentials_path": str(mock_config_dir / "service-account.json")
        }
    }
    
    # Create the service account file
    service_account_file = mock_config_dir / "service-account.json"
    service_account_file.write_text(json.dumps({"type": "service_account"}))
    
    with patch("utils.config.load_config") as mock_load:
        mock_load.return_value = config
        yield config


@pytest.fixture
def mock_check_registry():
    """Mock the check registry with sample checks."""
    from models import CheckInfo, CheckType, CloudProvider
    
    sample_checks = [
        CheckInfo(
            name="idle-ec2-instances",
            check_type=CheckType.IDLE_RESOURCE,
            description="Find idle EC2 instances",
            supported_providers=[CloudProvider.AWS]
        ),
        CheckInfo(
            name="oversized-instances",
            check_type=CheckType.RIGHT_SIZING,
            description="Find oversized compute instances",
            supported_providers=[CloudProvider.AWS, CloudProvider.AZURE, CloudProvider.GCP]
        ),
        CheckInfo(
            name="idle-vm-instances",
            check_type=CheckType.IDLE_RESOURCE,
            description="Find idle VM instances",
            supported_providers=[CloudProvider.AZURE]
        ),
    ]
    
    with patch("commands.list_checks.check_registry") as mock_registry:
        mock_registry.list_all.return_value = sample_checks
        yield mock_registry


@pytest.fixture
def mock_analyze_results():
    """Mock analyze results."""
    from datetime import datetime
    from models import CheckSeverity, CheckType
    
    class MockResource:
        def __init__(self, resource_id, resource_type):
            self.id = resource_id
            self.name = resource_id  # Use ID as name for simplicity
            self.type = resource_type
            self.provider = "aws"
            self.region = "us-east-1"
    
    class MockCheckResult:
        def __init__(self, **kwargs):
            self.id = kwargs.get('id', 'test-id')
            self.check_type = kwargs.get('check_type', CheckType.IDLE_RESOURCE)
            self.severity = kwargs.get('severity', CheckSeverity.HIGH)
            self.resource = kwargs.get('resource', MockResource("i-1234567890abcdef0", "EC2 Instance"))
            self.related_resources = kwargs.get('related_resources', [])
            self.title = kwargs.get('title', 'Idle EC2 Instance Found')
            self.description = kwargs.get('description', 'This EC2 instance appears to be idle')
            self.impact = kwargs.get('impact', 'Wasted compute resources')
            self.current_cost = kwargs.get('current_cost', 100.0)
            self.optimized_cost = kwargs.get('optimized_cost', 0.0)
            self.monthly_savings = kwargs.get('monthly_savings', 100.0)
            self.annual_savings = kwargs.get('annual_savings', 1200.0)
            self.savings_percentage = kwargs.get('savings_percentage', 100.0)
            self.effort_level = kwargs.get('effort_level', 'low')
            self.risk_level = kwargs.get('risk_level', 'low')
            self.implementation_steps = kwargs.get('implementation_steps', [])
            self.confidence_score = kwargs.get('confidence_score', 0.9)
            self.check_metadata = kwargs.get('check_metadata', {})
            self.checked_at = kwargs.get('checked_at', datetime.now())
            
            # For compatibility with tests expecting old structure
            self.check_name = kwargs.get('check_name', 'idle-ec2-instances')
            self.provider = self.resource.provider
            self.region = self.resource.region
            self.findings = kwargs.get('findings', [])
            self.metadata = kwargs.get('metadata', {})
            self.timestamp = self.checked_at
        
        def dict(self):
            """Convert to dictionary for JSON/CSV output."""
            return {
                "check_name": self.check_name,
                "check_type": self.check_type.value if hasattr(self.check_type, 'value') else str(self.check_type),
                "provider": self.provider,
                "region": self.region,
                "severity": self.severity.value if hasattr(self.severity, 'value') else str(self.severity),
                "resource_id": self.resource.id,
                "resource_type": self.resource.type,
                "title": self.title,
                "description": self.description,
                "current_cost": float(self.current_cost),
                "optimized_cost": float(self.optimized_cost),
                "monthly_savings": float(self.monthly_savings),
                "annual_savings": float(self.annual_savings),
                "savings_percentage": float(self.savings_percentage),
                "effort_level": self.effort_level,
                "risk_level": self.risk_level,
                "timestamp": self.timestamp.isoformat() if hasattr(self.timestamp, 'isoformat') else str(self.timestamp)
            }
    
    results = [
        MockCheckResult(
            id="result-1",
            check_name="idle-ec2-instances",
            check_type=CheckType.IDLE_RESOURCE,
            severity=CheckSeverity.HIGH,
            resource=MockResource("i-1234567890abcdef0", "EC2 Instance"),
            title="Idle EC2 Instance Found",
            description="This EC2 instance has been idle for 30 days",
            current_cost=100.0,
            optimized_cost=0.0,
            monthly_savings=100.0,
            annual_savings=1200.0,
            savings_percentage=100.0
        ),
        MockCheckResult(
            id="result-2",
            check_name="oversized-instances",
            check_type=CheckType.RIGHT_SIZING,
            severity=CheckSeverity.MEDIUM,
            resource=MockResource("i-0987654321fedcba0", "EC2 Instance"),
            title="Oversized EC2 Instance",
            description="This EC2 instance is oversized for its workload",
            current_cost=200.0,
            optimized_cost=100.0,
            monthly_savings=100.0,
            annual_savings=1200.0,
            savings_percentage=50.0
        )
    ]
    
    return results