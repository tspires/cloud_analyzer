Feature: Analyze Cloud Resources
  As a cloud administrator
  I want to analyze my cloud resources
  So that I can identify cost optimization opportunities

  Background:
    Given the CLI application is installed
    And I have configured all cloud providers

  Scenario: Analyze without configuration
    Given no providers are configured
    When I run "cloud-analyzer analyze"
    Then the output should contain "No configuration found"
    And the output should contain "Please run 'cloud-analyzer configure' first"

  Scenario: Analyze specific provider without configuration
    Given only Azure is configured
    When I run "cloud-analyzer analyze --provider aws"
    Then the output should contain "AWS is not configured"

  Scenario: Dry run analysis for all providers
    When I run "cloud-analyzer analyze --dry-run"
    Then the output should contain "Dry Run Mode"
    And the output should contain "Providers: AWS, Azure, GCP"

  Scenario: Dry run analysis for single provider
    When I run "cloud-analyzer analyze --provider aws --dry-run"
    Then the output should contain "Dry Run Mode"
    And the output should contain "Providers: AWS"

  Scenario: Dry run with region filter
    When I run "cloud-analyzer analyze --region us-west-2 --dry-run"
    Then the output should contain "Region: us-west-2"

  Scenario: Dry run with specific checks
    When I run "cloud-analyzer analyze --checks idle_resource,right_sizing --dry-run"
    Then the output should contain "Check types:"
    And the output should contain "idle_resource"
    And the output should contain "right_sizing"

  Scenario: Successful analysis with findings
    Given there are optimization opportunities
    When I run "cloud-analyzer analyze"
    Then the output should contain "Starting cloud resource analysis"
    And the output should show resource findings
    And the output should show potential savings

  Scenario: Analysis with severity filter
    Given there are findings of different severities
    When I run "cloud-analyzer analyze --severity high"
    Then the output should only show high and critical severity findings

  Scenario: Analysis with JSON output
    Given there are optimization opportunities
    When I run "cloud-analyzer analyze --output json"
    Then the output should be valid JSON
    And the JSON should contain check results

  Scenario: Analysis with JSON output to file
    Given there are optimization opportunities
    When I run "cloud-analyzer analyze --output json --output-file results.json"
    Then a file "results.json" should be created
    And the file should contain valid JSON
    And the output should contain "Results saved to results.json"

  Scenario: Analysis with CSV output to file
    Given there are optimization opportunities
    When I run "cloud-analyzer analyze --output csv --output-file results.csv"
    Then a file "results.csv" should be created
    And the file should contain CSV data
    And the output should contain "Results saved to results.csv"

  Scenario: CSV output without file
    When I run "cloud-analyzer analyze --output csv"
    Then the output should contain "Error"
    And the output should contain "CSV output requires --output-file"

  Scenario: Analysis for specific provider
    When I run "cloud-analyzer analyze --provider aws"
    Then only AWS resources should be analyzed

  Scenario: Analysis for specific region
    When I run "cloud-analyzer analyze --region eu-west-1"
    Then only resources in "eu-west-1" should be analyzed

  Scenario: Analysis with specific checks
    When I run "cloud-analyzer analyze --checks idle_resource,right_sizing"
    Then only "idle_resource" and "right_sizing" checks should run

  Scenario: Handle analysis errors gracefully
    Given the analysis will encounter an error
    When I run "cloud-analyzer analyze"
    Then the output should contain "Error during analysis"
    And the command should fail