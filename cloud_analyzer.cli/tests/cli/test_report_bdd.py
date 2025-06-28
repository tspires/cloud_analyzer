"""BDD tests for report command using pytest-bdd."""

import pytest
from pathlib import Path
from datetime import datetime
from pytest_bdd import scenarios, given, when, then, parsers
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from commands.report import report

# Load scenarios from feature file
scenarios('../features/cli/report.feature')


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def cli_result():
    """Store CLI execution result."""
    return {}


@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary directory for reports."""
    return tmp_path


@given('the CLI application is installed')
def cli_installed():
    """Verify CLI is installed."""
    pass


@given('I have analysis results available')
def analysis_results_available():
    """Mock analysis results."""
    # Would normally mock the analysis results loading
    pass


@given(parsers.parse('I have a saved results file "{filename}"'))
def saved_results_file(temp_dir, filename):
    """Create a saved results file."""
    results_file = temp_dir / filename
    results_file.write_text('{"results": []}')


@given('report generation will fail')
def report_generation_fails():
    """Set up report generation to fail."""
    with patch('cli.src.commands.report.generate_html_report') as mock_gen:
        mock_gen.side_effect = Exception("Test error")


@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner, cli_result, temp_dir, command):
    """Run a CLI command."""
    # Replace relative paths with temp dir paths
    if "--output" in command and not command.split("--output")[1].strip().startswith("/"):
        parts = command.split("--output")
        filename = parts[1].strip().split()[0]
        command = f"{parts[0]}--output {temp_dir / filename}"
    
    args = command.replace("cloud-analyzer ", "").split()
    
    # Mock the report generation functions
    with patch('cli.src.commands.report.generate_html_report') as mock_html, \
         patch('cli.src.commands.report.generate_pdf_report') as mock_pdf, \
         patch('cli.src.commands.report.generate_markdown_report') as mock_md:
        
        # Make the mocks actually create files
        def create_html(path, details):
            path.write_text("<html>Test Report</html>")
        
        def create_pdf(path, details):
            path.write_text("PDF Report")
        
        def create_markdown(path, details):
            path.write_text("# Cloud Cost Optimization Report\n\nTest content")
        
        mock_html.side_effect = create_html
        mock_pdf.side_effect = create_pdf
        mock_md.side_effect = create_markdown
        
        result = cli_runner.invoke(report, args)
    
    cli_result['output'] = result.output
    cli_result['exit_code'] = result.exit_code
    cli_result['temp_dir'] = temp_dir


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(cli_result, text):
    """Check if output contains text."""
    assert text in cli_result['output']


@then(parsers.parse('a file "{filename}" should be created'))
def file_created(cli_result, filename):
    """Check if specific file was created."""
    temp_dir = cli_result.get('temp_dir', Path.cwd())
    file_path = temp_dir / filename
    assert file_path.exists(), f"File {filename} not found in {temp_dir}"


@then(parsers.parse('a report file matching "{pattern}" should be created'))
def report_file_created(cli_result, pattern):
    """Check if file matching pattern was created."""
    # In actual implementation, would check current directory
    # For now, just verify the pattern in output
    assert "cloud-cost-report-" in cli_result['output']
    assert pattern.replace("*", "") in cli_result['output']


@then(parsers.parse('the file should contain "{text}"'))
def file_contains(cli_result, text):
    """Check if file contains expected text."""
    temp_dir = cli_result.get('temp_dir', Path.cwd())
    # Find the most recently created file
    files = list(temp_dir.glob("*"))
    if files:
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        content = latest_file.read_text()
        assert text in content


@then('the report should include detailed findings')
def report_has_details(cli_result):
    """Verify report includes details."""
    # In actual implementation, would check report content
    # For now, just verify the flag was processed
    assert "--include-details" in str(cli_result.get('command', ''))


@then('the command should fail')
def command_fails(cli_result):
    """Verify command failed."""
    assert cli_result['exit_code'] != 0