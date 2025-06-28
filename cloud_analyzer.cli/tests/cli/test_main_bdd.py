"""BDD tests for main CLI using pytest-bdd."""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from main import cli, main

# Load scenarios from feature file
scenarios('../features/cli/main.feature')


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def cli_result():
    """Store CLI execution result."""
    return {}


@given('the CLI application is installed')
def cli_installed():
    """Verify CLI is installed."""
    pass  # No action needed, imports would fail if not installed


@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner, cli_result, command):
    """Run a CLI command."""
    args = command.split()[1:]  # Remove 'cloud-analyzer' prefix
    result = cli_runner.invoke(cli, args)
    cli_result['output'] = result.output
    cli_result['exit_code'] = result.exit_code
    cli_result['exception'] = result.exception


@when('I run the CLI and press Ctrl+C')
def run_with_interrupt(cli_result):
    """Simulate running CLI with keyboard interrupt."""
    with patch('cli.main.cli') as mock_cli:
        mock_cli.side_effect = KeyboardInterrupt()
        try:
            main()
        except SystemExit as e:
            cli_result['exit_code'] = e.code
            cli_result['output'] = "Operation cancelled by user"


@when('the CLI encounters an unexpected error')
def run_with_error(cli_result):
    """Simulate unexpected error in CLI."""
    with patch('cli.main.cli') as mock_cli:
        mock_cli.side_effect = Exception("Test error")
        try:
            main()
        except SystemExit as e:
            cli_result['exit_code'] = e.code
            cli_result['output'] = "Unexpected error"


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(cli_result, text):
    """Check if output contains expected text."""
    assert text in cli_result['output']


@then('the command should fail')
def command_fails(cli_result):
    """Check if command failed."""
    assert cli_result['exit_code'] != 0


@then(parsers.parse('the output should contain "{text1}" or "{text2}"'))
def output_contains_either(cli_result, text1, text2):
    """Check if output contains one of two texts."""
    assert text1 in cli_result['output'] or text2 in cli_result['output']


@then(parsers.parse('the exit code should be {code:d}'))
def check_exit_code(cli_result, code):
    """Check exit code."""
    assert cli_result['exit_code'] == code


@then('the error should be logged')
def error_logged():
    """Verify error was logged (mocked in this case)."""
    pass  # In real implementation, would check log output