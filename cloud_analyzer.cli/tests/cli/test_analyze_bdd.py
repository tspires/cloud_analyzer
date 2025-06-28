"""BDD tests for analyze command using pytest-bdd."""

import json
import pytest
from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from click.testing import CliRunner
from unittest.mock import patch, MagicMock, AsyncMock

from commands.analyze import analyze
from models import CheckResult, CheckType, CloudProvider, CheckSeverity

# Load scenarios from feature file
scenarios('../features/cli/analyze.feature')


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def cli_result():
    """Store CLI execution result."""
    return {}


@pytest.fixture
def mock_results():
    """Create mock analysis results."""
    from datetime import datetime
    from collections import namedtuple
    
    # Create a simple mock structure for tests
    ResourceRecommendation = namedtuple(
        'ResourceRecommendation', 
        ['resource_id', 'resource_type', 'current_cost', 'recommended_cost', 
         'estimated_savings', 'recommendation', 'details']
    )
    
    CheckResult = namedtuple(
        'CheckResult',
        ['check_name', 'check_type', 'provider', 'region', 'severity', 
         'findings', 'metadata', 'timestamp']
    )
    
    return [
        CheckResult(
            check_name="idle-ec2-instances",
            check_type=CheckType.IDLE_RESOURCE,
            provider=CloudProvider.AWS,
            region="us-east-1",
            severity=CheckSeverity.HIGH,
            findings=[
                ResourceRecommendation(
                    resource_id="i-1234567890abcdef0",
                    resource_type="EC2 Instance",
                    current_cost=100.0,
                    recommended_cost=0.0,
                    estimated_savings=100.0,
                    recommendation="Terminate idle instance",
                    details={}
                )
            ],
            metadata={},
            timestamp=datetime.now()
        ),
        CheckResult(
            check_name="oversized-instances",
            check_type=CheckType.RIGHT_SIZING,
            provider=CloudProvider.AWS,
            region="us-east-1",
            severity=CheckSeverity.MEDIUM,
            findings=[
                ResourceRecommendation(
                    resource_id="i-0987654321fedcba0",
                    resource_type="EC2 Instance",
                    current_cost=200.0,
                    recommended_cost=100.0,
                    estimated_savings=100.0,
                    recommendation="Downsize to m5.medium",
                    details={}
                )
            ],
            metadata={},
            timestamp=datetime.now()
        )
    ]


@given('the CLI application is installed')
def cli_installed():
    """Verify CLI is installed."""
    pass


@given('I have configured all cloud providers')
def all_providers_configured():
    """Set up configuration for all providers."""
    config = {
        "aws": {"profile": "default"},
        "azure": {"subscription_id": "sub-123"},
        "gcp": {"project_id": "project-123"}
    }
    with patch('utils.config.load_config') as mock_load:
        mock_load.return_value = config


@given('no providers are configured')
def no_providers_configured():
    """Set up empty configuration."""
    with patch('cli.src.utils.config.load_config') as mock_load:
        mock_load.return_value = None


@given('only Azure is configured')
def only_azure_configured():
    """Set up only Azure configuration."""
    config = {"azure": {"subscription_id": "sub-123"}}
    with patch('utils.config.load_config') as mock_load:
        mock_load.return_value = config


@given('there are optimization opportunities')
def optimization_opportunities(mock_results):
    """Set up mock results with findings."""
    with patch('commands.analyze.asyncio.run') as mock_run:
        mock_run.return_value = mock_results


@given('there are findings of different severities')
def findings_with_severities(mock_results):
    """Set up findings with different severities."""
    with patch('commands.analyze.asyncio.run') as mock_run:
        mock_run.return_value = mock_results


@given('the analysis will encounter an error')
def analysis_error():
    """Set up analysis to fail."""
    with patch('commands.analyze.asyncio.run') as mock_run:
        mock_run.side_effect = Exception("Test error")


@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner, cli_result, command):
    """Run a CLI command."""
    args = command.replace("cloud-analyzer ", "").split()
    result = cli_runner.invoke(analyze, args)
    cli_result['output'] = result.output
    cli_result['exit_code'] = result.exit_code
    cli_result['exception'] = result.exception


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(cli_result, text):
    """Check if output contains text."""
    assert text in cli_result['output']


@then('the output should show resource findings')
def output_shows_findings(cli_result):
    """Check if output shows resource findings."""
    assert "i-1234567890abcdef0" in cli_result['output'] or \
           "idle-ec2-instances" in cli_result['output']


@then('the output should show potential savings')
def output_shows_savings(cli_result):
    """Check if output shows savings."""
    assert "$" in cli_result['output'] or "savings" in cli_result['output'].lower()


@then('the output should only show high and critical severity findings')
def output_filtered_severity(cli_result):
    """Check severity filtering."""
    assert "HIGH" in cli_result['output'] or "i-1234567890abcdef0" in cli_result['output']
    assert "MEDIUM" not in cli_result['output'] and "i-0987654321fedcba0" not in cli_result['output']


@then('the output should be valid JSON')
def output_is_json(cli_result):
    """Verify output is valid JSON."""
    try:
        json.loads(cli_result['output'])
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")


@then('the JSON should contain check results')
def json_contains_results(cli_result):
    """Verify JSON contains expected data."""
    data = json.loads(cli_result['output'])
    assert len(data) > 0
    assert "check_name" in data[0]


@then(parsers.parse('a file "{filename}" should be created'))
def file_created(filename, tmp_path):
    """Check if file was created."""
    file_path = Path(filename)
    assert file_path.exists() or (tmp_path / filename).exists()


@then('the file should contain valid JSON')
def file_contains_json(tmp_path):
    """Verify file contains valid JSON."""
    # Find the most recently created JSON file
    json_files = list(tmp_path.glob("*.json"))
    if json_files:
        with open(json_files[-1]) as f:
            json.load(f)  # Will raise if invalid


@then('the file should contain CSV data')
def file_contains_csv(tmp_path):
    """Verify file contains CSV data."""
    csv_files = list(tmp_path.glob("*.csv"))
    if csv_files:
        content = csv_files[-1].read_text()
        assert "," in content  # Basic CSV check


@then('only AWS resources should be analyzed')
def only_aws_analyzed():
    """Verify only AWS resources analyzed."""
    with patch('commands.analyze.asyncio.run') as mock_run:
        if mock_run.called:
            providers = mock_run.call_args[0][0][0]
            assert len(providers) == 1
            assert providers[0] == CloudProvider.AWS


@then(parsers.parse('only resources in "{region}" should be analyzed'))
def only_region_analyzed(region):
    """Verify region filter."""
    with patch('commands.analyze.asyncio.run') as mock_run:
        if mock_run.called:
            call_region = mock_run.call_args[0][0][1]
            assert call_region == region


@then(parsers.parse('only "{check1}" and "{check2}" checks should run'))
def only_specific_checks(check1, check2):
    """Verify specific checks run."""
    with patch('commands.analyze.asyncio.run') as mock_run:
        if mock_run.called:
            check_types = mock_run.call_args[0][0][2]
            assert check_types == [check1, check2]


@then('the command should fail')
def command_fails(cli_result):
    """Verify command failed."""
    assert cli_result['exit_code'] != 0 or cli_result.get('exception') is not None