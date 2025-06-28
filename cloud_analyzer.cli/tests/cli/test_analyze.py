"""Tests for the analyze command."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from commands.analyze import analyze, run_analysis
from models import CheckResult, CheckType, CloudProvider, CheckSeverity
import sys
import os

# Ensure src is in path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestAnalyzeCommand:
    """Test the analyze command."""
    
    @patch("commands.analyze.load_config")
    def test_analyze_no_config(self, mock_load_config, cli_runner):
        """Test analyze when no configuration exists."""
        mock_load_config.return_value = None
        result = cli_runner.invoke(analyze, [])
        assert result.exit_code == 0
        assert "No configuration found" in result.output
    
    @patch("commands.analyze.load_config")
    def test_analyze_missing_provider_config(self, mock_load_config, cli_runner):
        """Test analyze when specific provider config is missing."""
        mock_load_config.return_value = {"azure": {}}  # Missing AWS config
        result = cli_runner.invoke(analyze, ["--provider", "aws"])
        assert result.exit_code == 0
        assert "No configuration found for provider 'aws'" in result.output
    
    @patch("commands.analyze.load_config")
    def test_analyze_dry_run(self, mock_load_config, cli_runner):
        """Test analyze with dry-run flag."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"},
            "azure": {"subscription_id": "test-sub-123"},
            "gcp": {"project_id": "test-project-123"}
        }
        result = cli_runner.invoke(analyze, ["--dry-run"])
        assert result.exit_code == 0
        assert "Dry Run - Would analyze:" in result.output
        assert "AWS" in result.output
        assert "AZURE" in result.output
        assert "GCP" in result.output
    
    @patch("commands.analyze.load_config")
    def test_analyze_dry_run_single_provider(self, mock_load_config, cli_runner):
        """Test analyze dry-run with single provider."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        result = cli_runner.invoke(analyze, ["--provider", "aws", "--dry-run"])
        assert result.exit_code == 0
        assert "Dry Run - Would analyze:" in result.output
        assert "AWS" in result.output
    
    @patch("commands.analyze.load_config")
    def test_analyze_dry_run_with_region(self, mock_load_config, cli_runner):
        """Test analyze dry-run with region specified."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        result = cli_runner.invoke(analyze, ["--region", "us-west-2", "--dry-run"])
        assert result.exit_code == 0
        assert "us-west-2" in result.output
    
    @patch("commands.analyze.load_config")
    def test_analyze_dry_run_with_checks(self, mock_load_config, cli_runner):
        """Test analyze dry-run with specific checks."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        result = cli_runner.invoke(analyze, ["--checks", "idle_resource,right_sizing", "--dry-run"])
        assert result.exit_code == 0
        assert "idle_resource" in result.output
        assert "right_sizing" in result.output
    
    @patch("commands.analyze.asyncio.run")
    @patch("commands.analyze.load_config")
    def test_analyze_success(self, mock_load_config, mock_asyncio_run, cli_runner, mock_analyze_results):
        """Test successful analyze command."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        mock_asyncio_run.return_value = mock_analyze_results
        
        result = cli_runner.invoke(analyze, [])
        assert result.exit_code == 0
        assert "Starting cloud resource analysis" in result.output
        # Check that results are displayed
        assert "HIGH Priority Findings" in result.output or "i-1234567890abcdef0" in result.output
    
    @patch("commands.analyze.asyncio.run")
    @patch("commands.analyze.load_config")
    def test_analyze_with_severity_filter(self, mock_load_config, mock_asyncio_run, cli_runner, mock_analyze_results):
        """Test analyze with severity filter."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        mock_asyncio_run.return_value = mock_analyze_results
        
        result = cli_runner.invoke(analyze, ["--severity", "high"])
        assert result.exit_code == 0
        # Should only show HIGH severity findings
        assert "i-1234567890abcdef0" in result.output  # HIGH severity
        assert "i-0987654321fedcba0" not in result.output  # MEDIUM severity
    
    @patch("commands.analyze.asyncio.run")
    @patch("commands.analyze.load_config")
    def test_analyze_json_output(self, mock_load_config, mock_asyncio_run, cli_runner, mock_analyze_results):
        """Test analyze with JSON output format."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        mock_asyncio_run.return_value = mock_analyze_results
        
        result = cli_runner.invoke(analyze, ["--output", "json"])
        assert result.exit_code == 0
        # Output should be valid JSON (skip first line which is the status message)
        lines = result.output.strip().split('\n')
        json_output = '\n'.join(lines[1:]) if len(lines) > 1 else result.output
        if json_output.strip():
            output_json = json.loads(json_output)
            assert len(output_json) == 2
            assert output_json[0]["check_name"] == "idle-ec2-instances"
    
    @patch("commands.analyze.asyncio.run")
    @patch("commands.analyze.load_config")
    def test_analyze_json_output_to_file(self, mock_load_config, mock_asyncio_run, cli_runner, mock_analyze_results, tmp_path):
        """Test analyze with JSON output to file."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        mock_asyncio_run.return_value = mock_analyze_results
        output_file = tmp_path / "results.json"
        
        result = cli_runner.invoke(analyze, ["--output", "json", "--output-file", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        
        # Verify file contents
        with open(output_file) as f:
            data = json.load(f)
            assert len(data) == 2
            assert data[0]["check_name"] == "idle-ec2-instances"
    
    @patch("commands.analyze.asyncio.run")
    @patch("commands.analyze.load_config")
    def test_analyze_csv_output_to_file(self, mock_load_config, mock_asyncio_run, cli_runner, mock_analyze_results, tmp_path):
        """Test analyze with CSV output to file."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        mock_asyncio_run.return_value = mock_analyze_results
        output_file = tmp_path / "results.csv"
        
        result = cli_runner.invoke(analyze, ["--output", "csv", "--output-file", str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        
        # Verify CSV has content
        content = output_file.read_text()
        assert "check_name" in content
        assert "idle-ec2-instances" in content
    
    @patch("commands.analyze.load_config")
    def test_analyze_csv_without_file(self, mock_load_config, cli_runner):
        """Test CSV output without file specification."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        result = cli_runner.invoke(analyze, ["--output", "csv"])
        assert result.exit_code == 0
        assert "Error" in result.output
        assert "CSV output requires --output-file" in result.output
    
    @patch("commands.analyze.asyncio.run")
    @patch("commands.analyze.load_config")
    def test_analyze_with_exception(self, mock_load_config, mock_asyncio_run, cli_runner):
        """Test analyze when exception occurs."""
        mock_load_config.return_value = {
            "aws": {"profile": "test-profile"}
        }
        mock_asyncio_run.side_effect = Exception("Test error")
        
        result = cli_runner.invoke(analyze, [])
        assert result.exit_code != 0
        assert "Error during analysis" in result.output
    
    def test_analyze_specific_provider(self, cli_runner):
        """Test analyze with specific provider."""
        from unittest.mock import AsyncMock, patch
        
        with patch("commands.analyze.load_config") as mock_load_config:
            mock_load_config.return_value = {
                "aws": {"profile": "test-profile"}
            }
            
            # Mock run_analysis as an async function
            with patch("commands.analyze.run_analysis", new_callable=AsyncMock) as mock_run_analysis:
                mock_run_analysis.return_value = []
                
                result = cli_runner.invoke(analyze, ["--provider", "aws"])
                assert result.exit_code == 0
                # Verify correct providers were passed
                assert mock_run_analysis.called
                call_args = mock_run_analysis.call_args[0]
                providers = call_args[0]
                assert len(providers) == 1
                assert providers[0] == CloudProvider.AWS
    
    def test_analyze_with_region(self, cli_runner):
        """Test analyze with region specified."""
        from unittest.mock import AsyncMock, patch
        
        with patch("commands.analyze.load_config") as mock_load_config:
            mock_load_config.return_value = {
                "aws": {"profile": "test-profile"}
            }
            
            with patch("commands.analyze.run_analysis", new_callable=AsyncMock) as mock_run_analysis:
                mock_run_analysis.return_value = []
                
                result = cli_runner.invoke(analyze, ["--region", "eu-west-1"])
                assert result.exit_code == 0
                # Verify region was passed
                assert mock_run_analysis.called
                call_args = mock_run_analysis.call_args[0]
                region = call_args[1]
                assert region == "eu-west-1"
    
    def test_analyze_with_checks(self, cli_runner):
        """Test analyze with specific checks."""
        from unittest.mock import AsyncMock, patch
        
        with patch("commands.analyze.load_config") as mock_load_config:
            mock_load_config.return_value = {
                "aws": {"profile": "test-profile"}
            }
            
            with patch("commands.analyze.run_analysis", new_callable=AsyncMock) as mock_run_analysis:
                mock_run_analysis.return_value = []
                
                result = cli_runner.invoke(analyze, ["--checks", "idle_resource,right_sizing"])
                assert result.exit_code == 0
                # Verify checks were passed
                assert mock_run_analysis.called
                call_args = mock_run_analysis.call_args[0]
                check_types = call_args[2]
                assert check_types == ["idle_resource", "right_sizing"]


class TestAnalyzeHelpers:
    """Test analyze helper functions."""
    
    @pytest.mark.asyncio
    async def test_run_analysis_placeholder(self):
        """Test run_analysis function (currently a placeholder)."""
        from models import CloudProvider
        
        results = await run_analysis(
            [CloudProvider.AWS],
            "us-east-1",
            ["idle_resource"],
            {"aws": {}}
        )
        assert results == []  # Currently returns empty list