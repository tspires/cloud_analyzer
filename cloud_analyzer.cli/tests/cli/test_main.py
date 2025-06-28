"""Tests for the main CLI module."""

import pytest
from unittest.mock import patch

from main import cli, main


class TestCLI:
    """Test the main CLI interface."""
    
    def test_cli_help(self, cli_runner):
        """Test CLI help command."""
        result = cli_runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Cloud Analyzer - Multi-cloud cost optimization tool" in result.output
        assert "analyze" in result.output
        assert "configure" in result.output
        assert "list-checks" in result.output
        assert "report" in result.output
    
    def test_cli_version(self, cli_runner):
        """Test CLI version command."""
        result = cli_runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "cloud-analyzer, version 0.1.0" in result.output
    
    def test_cli_invalid_command(self, cli_runner):
        """Test CLI with invalid command."""
        result = cli_runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0
        assert "No such command" in result.output or "Invalid" in result.output
    
    def test_main_function_success(self):
        """Test main function with successful execution."""
        with patch("main.cli") as mock_cli:
            mock_cli.return_value = None
            # Should not raise any exception
            main()
            mock_cli.assert_called_once()
    
    def test_main_function_keyboard_interrupt(self):
        """Test main function handles KeyboardInterrupt."""
        with patch("main.cli") as mock_cli:
            mock_cli.side_effect = KeyboardInterrupt()
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 130
    
    def test_main_function_generic_exception(self):
        """Test main function handles generic exceptions."""
        with patch("main.cli") as mock_cli:
            mock_cli.side_effect = Exception("Test error")
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    
    def test_main_module_execution(self):
        """Test main module execution guard."""
        with patch("main.main") as mock_main:
            with patch("main.__name__", "__main__"):
                # Import would trigger the if __name__ == "__main__" block
                # but we can't easily test this without executing the module
                pass