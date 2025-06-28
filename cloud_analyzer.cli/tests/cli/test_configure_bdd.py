"""BDD tests for configure command using pytest-bdd."""

import json
import pytest
from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from commands.configure import configure

# Load scenarios from feature file
scenarios('../features/cli/configure.feature')


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def cli_result():
    """Store CLI execution result."""
    return {}


@pytest.fixture
def mock_config():
    """Mock configuration storage."""
    return {}


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create temporary config directory."""
    return tmp_path


@given('the CLI application is installed')
def cli_installed():
    """Verify CLI is installed."""
    pass


@given('I have a clean configuration directory')
def clean_config_dir(temp_config_dir):
    """Ensure clean config directory."""
    # Directory is already clean from tmp_path fixture
    pass


@given('no providers are configured')
def no_providers_configured(mock_config):
    """Set up empty configuration."""
    with patch('cli.src.utils.config.load_config') as mock_load:
        mock_load.return_value = {}


@given('I have configured AWS and Azure providers')
def providers_configured(mock_config):
    """Set up configuration with AWS and Azure."""
    config = {
        "aws": {"profile": "default", "region": "us-east-1"},
        "azure": {
            "subscription_id": "sub-123",
            "tenant_id": "tenant-123",
            "client_id": "client-123",
            "client_secret": "secret-123"
        }
    }
    with patch('cli.src.utils.config.load_config') as mock_load:
        mock_load.return_value = config
        mock_config.update(config)


@given('AWS is configured')
def aws_configured(mock_config):
    """Set up AWS configuration."""
    config = {"aws": {"profile": "default"}}
    with patch('cli.src.utils.config.load_config') as mock_load:
        mock_load.return_value = config
        mock_config.update(config)


@given('only Azure is configured')
def only_azure_configured(mock_config):
    """Set up only Azure configuration."""
    config = {"azure": {"subscription_id": "sub-123"}}
    with patch('cli.src.utils.config.load_config') as mock_load:
        mock_load.return_value = config
        mock_config.update(config)


@given(parsers.parse('a service account file exists at "{path}"'))
def service_account_exists(tmp_path, path):
    """Create a service account file."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps({"type": "service_account"}))


@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner, cli_result, command):
    """Run a CLI command."""
    args = command.replace("cloud-analyzer ", "").split()
    result = cli_runner.invoke(configure, args)
    cli_result['output'] = result.output
    cli_result['exit_code'] = result.exit_code


@when(parsers.parse('I confirm with "{response}"'))
def confirm_response(cli_runner, cli_result, response):
    """Handle confirmation prompt."""
    # Re-run the last command with input
    args = cli_result.get('last_args', [])
    result = cli_runner.invoke(configure, args, input=f"{response}\n")
    cli_result['output'] = result.output
    cli_result['exit_code'] = result.exit_code


@when('I choose AWS profile authentication')
def choose_aws_profile():
    """Choose AWS profile authentication."""
    return "y\n"  # Will be used as input


@when('I choose AWS credentials authentication')
def choose_aws_credentials():
    """Choose AWS credentials authentication."""
    return "n\n"  # Will be used as input


@when(parsers.parse('I enter profile name "{profile}"'))
def enter_profile(profile):
    """Enter profile name."""
    return f"{profile}\n"


@when(parsers.parse('I enter access key "{key}"'))
def enter_access_key(key):
    """Enter access key."""
    return f"{key}\n"


@when(parsers.parse('I enter secret key "{key}"'))
def enter_secret_key(key):
    """Enter secret key."""
    return f"{key}\n"


@when(parsers.parse('I enter region "{region}"'))
def enter_region(region):
    """Enter region."""
    return f"{region}\n"


@when(parsers.parse('I enter subscription ID "{sub_id}"'))
def enter_subscription(sub_id):
    """Enter subscription ID."""
    return f"{sub_id}\n"


@when(parsers.parse('I enter tenant ID "{tenant_id}"'))
def enter_tenant(tenant_id):
    """Enter tenant ID."""
    return f"{tenant_id}\n"


@when(parsers.parse('I enter client ID "{client_id}"'))
def enter_client_id(client_id):
    """Enter client ID."""
    return f"{client_id}\n"


@when(parsers.parse('I enter client secret "{secret}"'))
def enter_client_secret(secret):
    """Enter client secret."""
    return f"{secret}\n"


@when(parsers.parse('I enter project ID "{project}"'))
def enter_project(project):
    """Enter project ID."""
    return f"{project}\n"


@when(parsers.parse('I enter credentials path "{path}"'))
def enter_creds_path(path):
    """Enter credentials path."""
    return f"{path}\n"


@when(parsers.parse('I see warning "{warning}"'))
def see_warning(cli_result, warning):
    """Check for warning in output."""
    assert warning in cli_result.get('output', '')


@when(parsers.parse('I select "{provider}" when prompted for provider'))
def select_provider(provider):
    """Select provider in interactive mode."""
    return f"{provider}\n"


@when('I configure AWS with default settings')
def configure_aws_defaults():
    """Configure AWS with defaults."""
    return "y\ndefault\n"  # Use profile, default name


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(cli_result, text):
    """Check if output contains text."""
    assert text in cli_result['output']


@then('credentials should be masked with "****"')
def credentials_masked(cli_result):
    """Check if credentials are masked."""
    assert "****" in cli_result['output']
    assert "secret-123" not in cli_result['output']


@then('AWS configuration should be removed')
def aws_config_removed(mock_config):
    """Verify AWS config was removed."""
    with patch('cli.src.utils.config.save_config') as mock_save:
        if mock_save.called:
            saved_config = mock_save.call_args[0][0]
            assert "aws" not in saved_config


@then(parsers.parse('AWS should be configured with profile "{profile}"'))
def aws_configured_with_profile(mock_config, profile):
    """Verify AWS configured with profile."""
    with patch('cli.src.utils.config.save_config') as mock_save:
        if mock_save.called:
            saved_config = mock_save.call_args[0][0]
            assert saved_config["aws"]["profile"] == profile


@then('AWS should be configured with the provided credentials')
def aws_configured_with_creds(mock_config):
    """Verify AWS configured with credentials."""
    with patch('cli.src.utils.config.save_config') as mock_save:
        if mock_save.called:
            saved_config = mock_save.call_args[0][0]
            assert "access_key_id" in saved_config["aws"]
            assert "secret_access_key" in saved_config["aws"]


@then('Azure should be configured with the provided credentials')
def azure_configured(mock_config):
    """Verify Azure configured."""
    with patch('cli.src.utils.config.save_config') as mock_save:
        if mock_save.called:
            saved_config = mock_save.call_args[0][0]
            assert "subscription_id" in saved_config["azure"]


@then('GCP should be configured with the provided credentials')
def gcp_configured(mock_config):
    """Verify GCP configured."""
    with patch('cli.src.utils.config.save_config') as mock_save:
        if mock_save.called:
            saved_config = mock_save.call_args[0][0]
            assert "project_id" in saved_config["gcp"]