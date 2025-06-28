Feature: Generate Cost Optimization Reports
  As a cloud administrator
  I want to generate cost optimization reports
  So that I can share findings with stakeholders

  Background:
    Given the CLI application is installed
    And I have analysis results available

  Scenario: Generate HTML report with default filename
    When I run "cloud-analyzer report"
    Then the output should contain "Generating HTML report"
    And the output should contain "Report generated successfully"
    And a report file matching "cloud-cost-report-*.html" should be created

  Scenario: Generate report with custom output path
    When I run "cloud-analyzer report --output my-report.html"
    Then a file "my-report.html" should be created
    And the output should contain "Report generated successfully: my-report.html"

  Scenario: Generate Markdown report
    When I run "cloud-analyzer report --format markdown --output report.md"
    Then the output should contain "Generating MARKDOWN report"
    And a file "report.md" should be created
    And the file should contain "# Cloud Cost Optimization Report"

  Scenario: Generate PDF report
    When I run "cloud-analyzer report --format pdf --output report.pdf"
    Then the output should contain "Generating PDF report"
    And a file "report.pdf" should be created

  Scenario: Generate report with details
    When I run "cloud-analyzer report --include-details --output detailed-report.html"
    Then the report should include detailed findings
    And the output should contain "Report generated successfully"

  Scenario: Generate report from saved results
    Given I have a saved results file "results.json"
    When I run "cloud-analyzer report --from-file results.json --output report.html"
    Then the output should contain "Loading results from: results.json"
    And the output should contain "Report generated successfully"

  Scenario: Handle report generation errors
    Given report generation will fail
    When I run "cloud-analyzer report"
    Then the output should contain "Error generating report"
    And the command should fail

  Scenario Outline: Generate reports in different formats
    When I run "cloud-analyzer report --format <format> --output report.<extension>"
    Then the output should contain "Generating <FORMAT> report"
    And a file "report.<extension>" should be created

    Examples:
      | format   | extension | FORMAT   |
      | html     | html      | HTML     |
      | pdf      | pdf       | PDF      |
      | markdown | md        | MARKDOWN |