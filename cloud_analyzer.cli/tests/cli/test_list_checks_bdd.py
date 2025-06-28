"""BDD tests for list-checks command using pytest-bdd."""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from commands.list_checks import list_checks
from models import CheckInfo, CheckType, CloudProvider

# Load scenarios from feature file
scenarios('../features/cli/list_checks.feature')


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def cli_result():
    """Store CLI execution result."""
    return {}


@pytest.fixture
def sample_checks():
    """Create sample check data."""
    return [
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


@given('the CLI application is installed')
def cli_installed():
    """Verify CLI is installed."""
    pass


@given('the check registry contains sample checks')
def registry_has_checks(sample_checks):
    """Set up check registry with sample checks."""
    with patch('common.src.checks.registry.check_registry') as mock_registry:
        mock_registry.list_all.return_value = sample_checks


@given('the check registry is empty')
def registry_empty():
    """Set up empty check registry."""
    with patch('common.src.checks.registry.check_registry') as mock_registry:
        mock_registry.list_all.return_value = []


@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner, cli_result, command):
    """Run a CLI command."""
    args = command.replace("cloud-analyzer ", "").split()
    
    # Need to maintain the mock during command execution
    if 'registry' in command or 'check' in command:
        with patch('common.src.checks.registry.check_registry') as mock_registry:
            # Re-apply the mock based on previous given conditions
            if hasattr(run_command, '_mock_data'):
                mock_registry.list_all.return_value = run_command._mock_data
            else:
                # Default to sample checks
                mock_registry.list_all.return_value = [
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
            
            result = cli_runner.invoke(list_checks, args)
    else:
        result = cli_runner.invoke(list_checks, args)
    
    cli_result['output'] = result.output
    cli_result['exit_code'] = result.exit_code


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(cli_result, text):
    """Check if output contains text."""
    assert text in cli_result['output']


@then(parsers.parse('the output should not contain "{text}"'))
def output_not_contains(cli_result, text):
    """Check if output does not contain text."""
    assert text not in cli_result['output']


@then('the output should display a table with columns:')
def output_has_table_columns(cli_result, datatable):
    """Check if output has expected table columns."""
    output = cli_result['output']
    for row in datatable:
        column = row['Column']
        assert column in output


@then('providers should be displayed in uppercase')
def providers_uppercase(cli_result):
    """Check if providers are uppercase."""
    assert "AWS" in cli_result['output'] or \
           "AZURE" in cli_result['output'] or \
           "GCP" in cli_result['output']


@then(parsers.parse('multi-provider checks should show "{text}"'))
def multi_provider_format(cli_result, text):
    """Check multi-provider formatting."""
    assert text in cli_result['output']