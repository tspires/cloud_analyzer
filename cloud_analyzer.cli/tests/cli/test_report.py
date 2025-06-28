"""Tests for the report command."""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from commands.report import (
    generate_html_report,
    generate_markdown_report,
    generate_pdf_report,
    report,
)


class TestReportCommand:
    """Test the report command."""
    
    def test_report_default_output(self, cli_runner):
        """Test report generation with default output path."""
        with patch("commands.report.generate_html_report") as mock_html:
            result = cli_runner.invoke(report, [])
            assert result.exit_code == 0
            assert "Generating HTML report" in result.output
            assert "Report generated successfully" in result.output
            
            # Check that output file has timestamp
            call_args = mock_html.call_args[0][0]
            assert "cloud-cost-report-" in str(call_args)
            assert ".html" in str(call_args)
    
    def test_report_custom_output(self, cli_runner, tmp_path):
        """Test report generation with custom output path."""
        output_file = tmp_path / "my-report.html"
        
        with patch("commands.report.generate_html_report") as mock_html:
            result = cli_runner.invoke(report, ["--output", str(output_file)])
            assert result.exit_code == 0
            
            # Check that custom output path was used
            call_args = mock_html.call_args[0][0]
            assert call_args == output_file
    
    def test_report_markdown_format(self, cli_runner, tmp_path):
        """Test markdown report generation."""
        output_file = tmp_path / "report.md"
        
        with patch("commands.report.generate_markdown_report") as mock_md:
            result = cli_runner.invoke(report, ["--format", "markdown", "--output", str(output_file)])
            assert result.exit_code == 0
            assert "Generating MARKDOWN report" in result.output
            
            mock_md.assert_called_once_with(output_file, False)
    
    def test_report_pdf_format(self, cli_runner, tmp_path):
        """Test PDF report generation."""
        output_file = tmp_path / "report.pdf"
        
        with patch("commands.report.generate_pdf_report") as mock_pdf:
            result = cli_runner.invoke(report, ["--format", "pdf", "--output", str(output_file)])
            assert result.exit_code == 0
            assert "Generating PDF report" in result.output
            
            mock_pdf.assert_called_once_with(output_file, False)
    
    def test_report_with_details(self, cli_runner, tmp_path):
        """Test report generation with details flag."""
        output_file = tmp_path / "report.html"
        
        with patch("commands.report.generate_html_report") as mock_html:
            result = cli_runner.invoke(report, ["--include-details", "--output", str(output_file)])
            assert result.exit_code == 0
            
            # Check that include_details=True was passed
            mock_html.assert_called_once_with(output_file, True)
    
    def test_report_from_file(self, cli_runner, tmp_path):
        """Test report generation from saved results file."""
        results_file = tmp_path / "results.json"
        results_file.write_text('{"results": []}')
        output_file = tmp_path / "report.html"
        
        with patch("commands.report.generate_html_report") as mock_html:
            result = cli_runner.invoke(report, [
                "--from-file", str(results_file),
                "--output", str(output_file)
            ])
            assert result.exit_code == 0
            # The path might be wrapped across lines, so check for the base message
            assert "Loading results from:" in result.output
            assert str(results_file.name) in result.output
    
    def test_report_with_exception(self, cli_runner):
        """Test report command when exception occurs."""
        with patch("commands.report.generate_html_report") as mock_html:
            mock_html.side_effect = Exception("Test error")
            
            result = cli_runner.invoke(report, [])
            # The command catches exceptions and returns non-zero exit code
            assert result.exit_code != 0
            assert "Error generating report:" in result.output
            assert "Test error" in result.output


class TestReportGenerators:
    """Test individual report generation functions."""
    
    def test_generate_html_report(self, tmp_path):
        """Test HTML report generation."""
        output_file = tmp_path / "report.html"
        generate_html_report(output_file, include_details=False)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "<!DOCTYPE html>" in content
        assert "Cloud Cost Optimization Report" in content
        assert "Executive Summary" in content
    
    def test_generate_pdf_report(self, tmp_path, capsys):
        """Test PDF report generation (placeholder)."""
        output_file = tmp_path / "report.pdf"
        generate_pdf_report(output_file, include_details=False)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "Cloud Cost Optimization Report" in content
        assert "PDF generation not yet implemented" in content
        
        captured = capsys.readouterr()
        assert "PDF generation not yet implemented" in captured.out
    
    def test_generate_markdown_report(self, tmp_path):
        """Test Markdown report generation."""
        output_file = tmp_path / "report.md"
        generate_markdown_report(output_file, include_details=False)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "# Cloud Cost Optimization Report" in content
        assert "## Executive Summary" in content
        assert "## Key Findings" in content
        assert "## Recommendations by Category" in content
        assert datetime.now().strftime("%Y-%m-%d") in content